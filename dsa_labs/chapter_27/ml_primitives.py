"""Machine Learning Primitives (Chapter 27)."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

# ----------------------------------------------------------------------------
# Stable softmax, and the log-sum-exp identity behind it
# ----------------------------------------------------------------------------

def softmax(logits: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax.

    softmax(x) == softmax(x - c) for any constant c, because the shift
    cancels between numerator and denominator. Choosing c = max(x) makes
    the largest exponent exactly 0, so exp() can never overflow.

    Without the shift, a logit of 800 gives inf/inf = nan -- and the nan
    propagates silently through everything downstream.

    Time O(n), Space O(n).
    """
    shifted = logits - np.max(logits, axis=axis, keepdims=True)
    exponentiated = np.exp(shifted)
    return exponentiated / np.sum(exponentiated, axis=axis, keepdims=True)


def log_softmax(logits: np.ndarray, axis: int = -1) -> np.ndarray:
    """log(softmax(x)), computed WITHOUT forming softmax first.

    log(softmax(x)) = x - max - log(sum(exp(x - max)))

    Taking log(softmax(x)) directly underflows to -inf whenever a
    probability rounds to zero, which is common for a 128k vocabulary.
    This form never forms the small probability at all.
    """
    shifted = logits - np.max(logits, axis=axis, keepdims=True)
    return shifted - np.log(np.sum(np.exp(shifted), axis=axis, keepdims=True))


def cross_entropy(logits: np.ndarray, targets: np.ndarray) -> float:
    """Mean cross-entropy over a batch, from LOGITS not probabilities.

    Computing softmax then log() loses precision twice and can produce
    -inf for a confidently wrong prediction. Frameworks expose a
    from-logits variant for exactly this reason, and using it is not an
    optimisation -- it is a correctness requirement.

    Time O(batch * classes).
    """
    if logits.ndim != 2:
        raise ValueError("expected a (batch, classes) logit array")
    if targets.shape[0] != logits.shape[0]:
        raise ValueError("batch size mismatch between logits and targets")
    log_probs = log_softmax(logits, axis=-1)
    return float(-log_probs[np.arange(len(targets)), targets].mean())

# ----------------------------------------------------------------------------
# K-Means with the empty-cluster case handled
# ----------------------------------------------------------------------------

def kmeans(points: np.ndarray, k: int, *, max_iterations: int = 100,
           tolerance: float = 1e-4, seed: int = 0
           ) -> tuple[np.ndarray, np.ndarray, int]:
    """Lloyd's algorithm with k-means++ initialisation.

    Returns (centroids, labels, iterations_run).

    Time  O(i * n * k * d) -- FOUR dimensions, and which dominates decides
          where to optimise. On 768-dim embeddings, d usually dominates.
    Space O(n * k) for the distance matrix.

    Two details that are always graded:
      * empty clusters -- a centroid with no assigned points has a zero
        denominator; re-seeding it at the furthest point is the standard
        repair and keeps k clusters alive.
      * convergence -- stop when centroids stop moving, not after a fixed
        iteration count.
    """
    if points.ndim != 2:
        raise ValueError("points must be a 2-D (n, d) array")
    n, d = points.shape
    if not 1 <= k <= n:
        raise ValueError(f"k must be in 1..{n}, got {k}")

    rng = np.random.default_rng(seed)
    centroids = _kmeans_plus_plus(points, k, rng)
    labels = np.zeros(n, dtype=np.int64)

    for iteration in range(1, max_iterations + 1):
        # --- assignment step -------------------------------------------
        # ||a-b||^2 = ||a||^2 - 2 a.b + ||b||^2 : one matmul, no (n,k,d)
        # intermediate. The naive broadcast would allocate n*k*d floats,
        # which at n=1e6, k=100, d=768 is 300 GB.
        distances = (
            (points ** 2).sum(axis=1)[:, None]
            - 2 * points @ centroids.T
            + (centroids ** 2).sum(axis=1)[None, :]
        )
        new_labels = distances.argmin(axis=1)

        # --- update step -----------------------------------------------
        new_centroids = np.zeros_like(centroids)
        for cluster in range(k):
            members = points[new_labels == cluster]
            if len(members) == 0:
                # Empty cluster: re-seed at the point furthest from any
                # centroid. Leaving it in place would make it permanently
                # empty; deleting it would silently return fewer than k.
                furthest = distances.min(axis=1).argmax()
                new_centroids[cluster] = points[furthest]
            else:
                new_centroids[cluster] = members.mean(axis=0)

        shift = float(np.linalg.norm(new_centroids - centroids))
        centroids, labels = new_centroids, new_labels
        if shift < tolerance:
            return centroids, labels, iteration
    return centroids, labels, max_iterations


def _kmeans_plus_plus(points: np.ndarray, k: int,
                      rng: np.random.Generator) -> np.ndarray:
    """Seed centroids far apart, proportional to squared distance.

    Random initialisation can place two centroids inside one true cluster,
    which Lloyd's algorithm cannot recover from -- it converges to a local
    minimum and stays there. k-means++ gives an O(log k) expected
    approximation guarantee for the cost of k passes.
    """
    n = len(points)
    centroids = [points[rng.integers(n)]]
    for _ in range(1, k):
        squared = np.min(
            [((points - c) ** 2).sum(axis=1) for c in centroids], axis=0)
        total = squared.sum()
        if total == 0:                      # all points identical
            centroids.append(points[rng.integers(n)])
            continue
        probabilities = squared / total
        centroids.append(points[rng.choice(n, p=probabilities)])
    return np.array(centroids)

# ----------------------------------------------------------------------------
# Attention, with the two details that are always checked
# ----------------------------------------------------------------------------

def scaled_dot_product_attention(
    queries: np.ndarray,      # (..., L_q, d_k)
    keys: np.ndarray,         # (..., L_k, d_k)
    values: np.ndarray,       # (..., L_k, d_v)
    mask: np.ndarray | None = None,   # True where attention is ALLOWED
) -> tuple[np.ndarray, np.ndarray]:
    """Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V.

    Returns (output, attention_weights).

    Time  O(L_q * L_k * d) for the scores plus O(L_q * L_k * d_v) for the
          weighted sum -- quadratic in sequence length, which is the entire
          motivation for every efficient-attention variant.
    Space O(L_q * L_k) for the score matrix, which is what actually runs
          out of memory at long context.

    The two graded details:
      * the 1/sqrt(d_k) scale -- without it, dot products grow with d_k,
        softmax saturates, and gradients vanish;
      * masking with -inf BEFORE the softmax, not zeroing probabilities
        after, so the surviving distribution stays normalised.
    """
    d_k = queries.shape[-1]
    if keys.shape[-1] != d_k:
        raise ValueError("queries and keys must share the last dimension")
    if keys.shape[-2] != values.shape[-2]:
        raise ValueError("keys and values must have the same sequence length")

    scores = queries @ np.swapaxes(keys, -1, -2) / np.sqrt(d_k)

    if mask is not None:
        # -inf, not 0: after softmax, exp(-inf) = 0 exactly and the
        # remaining probabilities still sum to 1. Zeroing AFTER softmax
        # leaves an un-normalised distribution.
        scores = np.where(mask, scores, -np.inf)

    weights = softmax(scores, axis=-1)
    return weights @ values, weights


def causal_mask(length: int) -> np.ndarray:
    """Lower-triangular mask: position i may attend to positions <= i.

    True means ALLOWED. Getting the polarity backwards is a bug that still
    trains -- to a much worse model -- because the network adapts to
    whatever it is shown.
    """
    return np.tril(np.ones((length, length), dtype=bool))

# ----------------------------------------------------------------------------
# Precision, recall, F1, and the conventions that need stating
# ----------------------------------------------------------------------------

def classification_metrics(y_true: np.ndarray, y_pred: np.ndarray
                           ) -> dict[str, float]:
    """Binary precision, recall and F1 from 0/1 arrays.

    The zero-denominator conventions are decisions, not details, and an
    interviewer will ask:
      * precision with no positive predictions: 1.0 (vacuously precise --
        the classifier made no claims, so none were wrong). Some
        libraries return 0.0. STATE which you chose.
      * recall with no actual positives: 1.0 (nothing to find).
      * F1 with both zero: 0.0, since the harmonic mean is undefined.

    Time O(n), Space O(1). Vectorised: no Python loop over examples.
    """
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    tp = int(np.count_nonzero((y_pred == 1) & (y_true == 1)))
    fp = int(np.count_nonzero((y_pred == 1) & (y_true == 0)))
    fn = int(np.count_nonzero((y_pred == 0) & (y_true == 1)))

    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) else 0.0)
    return {"precision": precision, "recall": recall, "f1": f1,
            "tp": tp, "fp": fp, "fn": fn}


def roc_auc(scores: np.ndarray, labels: np.ndarray) -> float:
    """AUC via the rank-sum (Mann-Whitney U) identity.

    AUC is the probability that a random positive outranks a random
    negative. The rank formulation computes it in O(n log n) instead of
    O(P*N) pairwise comparisons, and handles ties correctly by using
    average ranks.

    Time O(n log n), Space O(n).
    """
    positives = int(np.count_nonzero(labels == 1))
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        raise ValueError("AUC is undefined with only one class present")

    order = np.argsort(scores, kind="mergesort")   # stable, for tie handling
    ranks = np.empty(len(scores), dtype=np.float64)
    ranks[order] = np.arange(1, len(scores) + 1)

    # Average ranks within tied score groups, or ties bias the result.
    sorted_scores = scores[order]
    start = 0
    for end in range(1, len(sorted_scores) + 1):
        if end == len(sorted_scores) or sorted_scores[end] != sorted_scores[start]:
            if end - start > 1:
                ranks[order[start:end]] = ranks[order[start:end]].mean()
            start = end

    rank_sum = ranks[labels == 1].sum()
    return float((rank_sum - positives * (positives + 1) / 2)
                 / (positives * negatives))

# ----------------------------------------------------------------------------
# KNN: partition, not sort
# ----------------------------------------------------------------------------
from collections import Counter

def knn_predict(train_x: np.ndarray, train_y: np.ndarray,
                query_x: np.ndarray, k: int) -> np.ndarray:
    """k-nearest-neighbour classification by majority vote.

    Time  O(q * n * d) for distances + O(q * n) for the partition.
    Space O(q * n) for the distance matrix.

    argpartition is O(n) against argsort's O(n log n), and we only need
    the k nearest -- not their order. At n = 1e6 and k = 10 that is the
    difference between 20n and n comparisons.
    """
    if k < 1 or k > len(train_x):
        raise ValueError(f"k must be in 1..{len(train_x)}")
    distances = (
        (query_x ** 2).sum(1)[:, None]
        - 2 * query_x @ train_x.T
        + (train_x ** 2).sum(1)[None, :]
    )
    neighbours = np.argpartition(distances, k - 1, axis=1)[:, :k]

    predictions = np.empty(len(query_x), dtype=train_y.dtype)
    for i, idx in enumerate(neighbours):
        votes = Counter(train_y[idx].tolist())
        best = max(votes.values())
        # Deterministic tie-break: smallest label wins. Without an explicit
        # rule the result depends on dict ordering, which is not a property
        # anyone should rely on.
        predictions[i] = min(label for label, c in votes.items() if c == best)
    return predictions

# ----------------------------------------------------------------------------
# ml_primitives.py (excerpt) -- logistic regression
# ----------------------------------------------------------------------------

from dataclasses import dataclass



def sigmoid(x: np.ndarray) -> np.ndarray:
    """Numerically stable logistic function.

    exp(-x) overflows for large NEGATIVE x. The piecewise form uses
    1/(1+exp(-x)) where x >= 0 and exp(x)/(1+exp(x)) where x < 0, so the
    exponent argument is always <= 0 and cannot overflow.

    The naive one-liner returns inf, then nan, for x below about -709 --
    and confidently-wrong predictions are exactly where that happens.
    """
    out = np.empty_like(x, dtype=np.float64)
    positive = x >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-x[positive]))
    exp_x = np.exp(x[~positive])
    out[~positive] = exp_x / (1.0 + exp_x)
    return out


@dataclass
class LogisticRegression:
    """Binary logistic regression trained by full-batch gradient descent.

    Gradient of the mean log-loss:  X^T (sigmoid(Xw + b) - y) / n
    Derivation: d/dz of log-loss is (sigmoid(z) - y), and dz/dw is X.
    The sigmoid derivative cancels exactly, which is why log-loss is the
    natural objective for this model.

    Time  O(iterations * n * d), Space O(d).
    """
    learning_rate: float = 0.1
    iterations: int = 1_000
    l2: float = 0.0
    tolerance: float = 1e-7

    weights: np.ndarray | None = None
    bias: float = 0.0
    loss_history: list[float] | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegression":
        if X.ndim != 2:
            raise ValueError("X must be a 2-D (n, d) array")
        if len(X) != len(y):
            raise ValueError("X and y must have the same number of rows")
        if not set(np.unique(y)).issubset({0, 1}):
            raise ValueError("y must contain only 0 and 1")

        n, d = X.shape
        self.weights = np.zeros(d)
        self.bias = 0.0
        self.loss_history = []

        for _ in range(self.iterations):
            probabilities = sigmoid(X @ self.weights + self.bias)
            error = probabilities - y

            grad_w = X.T @ error / n + self.l2 * self.weights
            grad_b = float(error.mean())     # NOT regularised: penalising
                                             # the intercept shifts the
                                             # decision boundary for no reason
            self.weights -= self.learning_rate * grad_w
            self.bias -= self.learning_rate * grad_b

            # Clip inside the log, not the probability: log(0) is -inf and
            # a single confidently-wrong example would make the loss -inf.
            eps = 1e-12
            loss = float(-np.mean(
                y * np.log(probabilities + eps)
                + (1 - y) * np.log(1 - probabilities + eps)))
            loss += 0.5 * self.l2 * float(self.weights @ self.weights)
            self.loss_history.append(loss)

            if len(self.loss_history) > 1 and \
               abs(self.loss_history[-2] - loss) < self.tolerance:
                break
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.weights is None:
            raise RuntimeError("model is not fitted")
        return sigmoid(X @ self.weights + self.bias)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(np.int64)


def information_gain(labels: np.ndarray, left_mask: np.ndarray) -> float:
    """Entropy reduction from a binary split. Time O(n + c).

    Used to evaluate a candidate decision-tree split. Computing this
    naively per candidate is O(n) each and O(n^2) per feature; a real
    implementation sorts once and maintains class counts incrementally so
    each candidate is O(1).
    """
    def entropy(subset: np.ndarray) -> float:
        if subset.size == 0:
            return 0.0
        _, counts = np.unique(subset, return_counts=True)
        p = counts / counts.sum()
        return float(-(p * np.log2(p)).sum())

    n = len(labels)
    left, right = labels[left_mask], labels[~left_mask]
    weighted = (len(left) * entropy(left) + len(right) * entropy(right)) / n
    return entropy(labels) - weighted

