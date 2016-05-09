#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
from SquatEvaluator import *
from PushupEvaluator import *

ITEM_MAPPING = {
    "squat"     : SquatEvaluator,
    "pushup"    : PushupEvaluator,
}
def evaluatorFactory(segment_id, item, training):
    if not ITEM_MAPPING.has_key(item):
        raise ValueException("given an invalid item")
    cls = ITEM_MAPPING[item]
    return cls(segment_id, training)
