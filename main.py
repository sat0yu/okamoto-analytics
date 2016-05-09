#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
import ConfigParser
import pymongo
from logging import getLogger,FileHandler
from abc import *
from EvaluatorHelper import *
from SquatEvaluator import *
from PushupEvaluator import *
from Body import *
from MongoHelper import *
from Status import *
import random
import time
import os
import sys

def main(config, logger):
    # connect database and fetch the lastest segment
    target_segment = None
    mongo = None
    try:
        mongo           = MongoHelper(config)
        target_segment  = mongo.getLastSegment()
        lastest_result  = mongo.getLastResult()
    except ValueError as e:
        logger.exception(e)
        print(target_segment)
        logger.error(target_segment)
        return -1

    if mongo is None:
        logger.error("can not establish a connection")
        return -1
    elif target_segment is None:
        logger.error("something is wrong")
        return -1
    else:
        logger.info("fetch the newest segment from mongodb")

    # build a body object for each frame
    # and evaluate it based on current training
    logger.info("start evaluation of the user training")
    segment_id  = target_segment["_id"]
    segment_item= target_segment["item"]
    frames      = target_segment["frames"]
    training    = map(Body.create_body_from_frame, frames)

    # check if the lastest result is
    # for the current target_segment
    if(lastest_result is not None and segment_id == lastest_result["segment_id"]):
        logger.info("the current segment has been already evaluated")
        return 0

    # evaluate the training
    evl = evaluatorFactory(segment_id, segment_item, training)
    logger.info("start evaluation; segment_item:%s" % segment_item)
    statuses = evl.execute()

    for st in statuses: print(st.type, st.value)

    # insert an error into mongodb
    numStatuses = len(statuses)
    if(numStatuses > 0):
        random_idx  = random.randint(0, numStatuses-1)
        result      = statuses[random_idx]
        mongo.insertResult(result)
        logger.info("insert new status")
        return 0

if __name__ == "__main__":
    # load settings
    config = ConfigParser.SafeConfigParser()
    config.read("./okamoto.conf")
    config = {
        'retry_delay'           : int( config.get("common",      "retry_delay") ),
        'logger_file'           : config.get("logger",      "file"),
        'logger_display_level'  : int( config.get("logger", "display_level") ),
        'logger_write_level'    : int( config.get("logger", "write_level") ),
        'host'                  : config.get("mongo",       "host"),
        'port'                  : config.get("mongo",       "port"),
        'database'              : config.get("mongo",       "database"),
        'source_collection'     : config.get("mongo",       "source_collection"),
        'result_collection'     : config.get("mongo",       "result_collection"),
    }

    # setup logger
    logger              = getLogger(__name__)
    file_handler        = FileHandler(config["logger_file"], 'a+')
    file_handler.setLevel(config["logger_write_level"])
    logger.addHandler(file_handler)
    logger.setLevel(config["logger_display_level"])

    # run every second
    retry_delay = config["retry_delay"]
    status      = True
    while True:
        try:
            returned = main(config, logger)
            if returned == 0:
                status = True
                retry_delay = config["retry_delay"]
            if returned < 0:
                status = False
                retry_delay *= 2
        except Exception as e:
            logger.exception(e)
            if(status):
                status = False
            else:
                retry_delay *= 2

        logger.info("retry after %d-seconds" % retry_delay)
        time.sleep(retry_delay)
