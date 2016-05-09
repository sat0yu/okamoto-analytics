#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
from abc import *

class BaseEvaluator(object):
    __metaclass__ = ABCMeta

    def __init__(self, segment_id, training):
        self.segment_id     = segment_id
        self.training       = list(training)
        self.statuses       = []

    def execute(self):
        self.evaluateForm()
        self.evaluatePace()
        return self.statuses

    def appenStatus(self, status):
        self.statuses.append(status)

    @abstractmethod
    def evaluateForm(self):
        raise NotImplementedError()

    @abstractmethod
    def evaluatePace(self):
        raise NotImplementedError()
