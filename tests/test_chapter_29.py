"""Unit tests for Chapter 29."""
from __future__ import annotations
from dsa_labs.chapter_29.inference_cache import InferenceCache
from dsa_labs.chapter_29.rate_limiter import TokenBucketLimiter
from dsa_labs.chapter_29.point_in_time import PointInTimeFeatureStore
from dsa_labs.chapter_29.leetcode_solutions import MyStack, LRUCache, LFUCache

def test_inference_cache():
    cache = InferenceCache(capacity_bytes=1000)
    cache.put("k1", "val1", size_bytes=100)
    assert cache.get("k1") == "val1"
    assert cache.get("k2") is None

def test_rate_limiter():
    limiter = TokenBucketLimiter(capacity=5.0, refill_rate_per_second=1.0)
    assert limiter.allow("user1", cost=3.0) is True
    assert limiter.allow("user1", cost=3.0) is False

def test_point_in_time():
    store = PointInTimeFeatureStore()
    store.put("e1", 10.0, 100.0)
    store.put("e1", 20.0, 200.0)
    assert store.get("e1", 5.0) is None
    assert store.get("e1", 15.0) == 100.0
    assert store.get("e1", 25.0) == 200.0

def test_mystack():
    st = MyStack()
    st.push(1)
    st.push(2)
    assert st.top() == 2
    assert st.pop() == 2
    assert st.empty() is False

def test_lru_cache():
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)
    assert lru.get(2) == -1

def test_lfu_cache():
    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    assert lfu.get(1) == 1
    lfu.put(3, 3)
    assert lfu.get(2) == -1
    assert lfu.get(3) == 3
