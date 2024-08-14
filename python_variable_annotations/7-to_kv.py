#!/usr/bin/env python3
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> tuple:
    return (k, v * v)
