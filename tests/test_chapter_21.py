"""Unit tests for Chapter 21."""
from __future__ import annotations
import numpy as np
from dsa_labs.chapter_21.quantization import quantize, dequantize
from dsa_labs.chapter_21.leetcode_solutions import hamming_weight, single_number, divide

def test_quantize():
    x = np.array([-1.0, 0.0, 1.0], dtype=np.float32)
    q = quantize(x, bits=8)
    deq = dequantize(q)
    assert np.allclose(x, deq, atol=0.05)

def test_hamming_weight():
    assert hamming_weight(11) == 3
    assert hamming_weight(128) == 1

def test_single_number():
    assert single_number([2, 2, 3, 2]) == 3
    assert single_number([0, 1, 0, 1, 0, 1, 99]) == 99

def test_divide():
    assert divide(10, 3) == 3
    assert divide(7, -3) == -2
