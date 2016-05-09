#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
import datetime

class Status:
    def __init__(self, segment_id, status_type, status_value):
        self.segment_id     = segment_id
        self.status_type    = status_type
        self.status_value   = status_value

    def serialize(self):
        now = datetime.datetime.now()
        return {
            "segment_id"    : self.segment_id,
            "type"          : self.status_type,
            "value"         : self.status_value,
            "created_at"    : now.strftime('%Y-%m-%d %H:%M:%S'),
            "complete_f"    : False,
        }
