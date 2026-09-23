"""Unit tests for Chapter 27."""
from __future__ import annotations
import numpy as np
from dsa_labs.chapter_27.ml_primitives import sigmoid, LogisticRegression, scaled_dot_product_attention

def test_sigmoid():
    x = np.array([-1000.0, 0.0, 1000.0])
    s = sigmoid(x)
    assert np.isclose(s[0], 0.0)
    assert np.isclose(s[1], 0.5)
    assert np.isclose(s[2], 1.0)

def test_logistic_regression():
    X = np.array([[1.0, 2.0], [2.0, 1.0], [3.0, 4.0], [4.0, 3.0]])
    y = np.array([0, 0, 1, 1])
    lr = LogisticRegression(learning_rate=0.1, iterations=100)
    lr.fit(X, y)
    assert lr.weights is not None
    preds = lr.predict(X)
    assert len(preds) == 4

def test_attention():
    Q = np.random.randn(2, 4, 8)
    K = np.random.randn(2, 4, 8)
    V = np.random.randn(2, 4, 8)
    out, weights = scaled_dot_product_attention(Q, K, V)
    assert out.shape == (2, 4, 8)
    assert weights.shape == (2, 4, 4)
    assert np.allclose(weights.sum(axis=-1), 1.0)
