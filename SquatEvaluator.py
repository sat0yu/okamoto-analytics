#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
from BaseEvaluator import *
from Status import *

class SquatEvaluator(BaseEvaluator):
    IDEAL_PACE = 1

    def __init__(self, segment_id, training):
        super(SquatEvaluator, self).__init__(segment_id, training)

    def countSquatIteration(self):
        count = 0
        isErect = True if self.training[0].kneeCosTheta < 0 else False
        for b in self.training[1:]:
            # print(b.kneeCosTheta)
            if(isErect and b.kneeCosTheta >= 0):
                isErect = False
                count += 1
            elif(not(isErect) and b.kneeCosTheta < 0):
                isErect = True

        return count

    def evaluatePace(self):
        count = self.countSquatIteration()
        if(count > SquatEvaluator.IDEAL_PACE):
            # value:1 -> fast
            st = Status(self.segment_id, "pace", 1)
            self.appenStatus(st)
        elif(count < SquatEvaluator.IDEAL_PACE):
            # value:2 -> slow
            st = Status(self.segment_id, "pace", 2)
            self.appenStatus(st)

    def evaluateForm(self):
        # select the frame where the user's hip
        # locates the lowest position in the training
        onWorking, lowest_pos, target = False, (0x01<<31), None
        for b in self.training:
            hipPos = b.getLowerPosition("Hip")
            if hipPos[1] < lowest_pos and b.kneeCosTheta > 0:
                onWorking, lowest_pos, target = True, hipPos[1], b

        if(onWorking):
            self.isValidDirection(target)
            self.isValidHipPosition(target)
            self.isValidKneePosition(target)

    def isValidDirection(self, body):
        direction = body.getDirection()
        if( direction * direction == 0 ):
            st = Status(self.segment_id, "form", 1)
            self.appenStatus(st)

    def isValidHipPosition(self, body):
        hipPos      = body.getLowerPosition("Hip")
        kneePos     = body.getAveragePosition("Knee")
        anklePos    = body.getUpperPosition("Ankle")
        baseHeight  = kneePos[1] - anklePos[1]
        if( hipPos[1] < kneePos[1] - baseHeight/2):
            st = Status(self.segment_id, "form", 2)
            self.appenStatus(st)
        elif( hipPos[1] > kneePos[1] + baseHeight/2):
            st = Status(self.segment_id, "form", 3)
            self.appenStatus(st)

    def isValidKneePosition(self, body):
        direction   = body.getDirection()
        hipPos      = body.getAveragePosition("Hip")
        kneePos     = body.getAveragePosition("Knee")
        anklePos    = body.getAveragePosition("Ankle")
        X_centerLeg = 0.75*kneePos[0] + 0.25*hipPos[0]
        if(direction < 0 and X_centerLeg < anklePos[0]):
            st = Status(self.segment_id, "form", 4)
            self.appenStatus(st)
