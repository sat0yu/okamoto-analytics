#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
from BaseEvaluator import *
from Status import *
from math import sqrt

class PushupEvaluator(BaseEvaluator):
    IDEAL_PACE = 1

    def __init__(self, segment_id, training):
        super(PushupEvaluator, self).__init__(segment_id, training)

    def countPushupIteration(self):
        count = 0
        isDown = True if self.training[0].elbowCosTheta > 0 else False
        for b in self.training[1:]:
            print(b.elbowCosTheta)
            if(isDown and b.elbowCosTheta < 0):
                isDown = False
                count += 1
            elif(not(isDown) and b.elbowCosTheta >= 0):
                isDown = True

        return count

    def evaluatePace(self):
        count = self.countPushupIteration()
        if(count > SquatEvaluator.IDEAL_PACE):
            # value:1 -> fast
            st = Status(self.segment_id, "pace", 1)
            self.appenStatus(st)
        elif(count < SquatEvaluator.IDEAL_PACE):
            # value:2 -> slow
            st = Status(self.segment_id, "pace", 2)
            self.appenStatus(st)

    def evaluateForm(self):
        # select the frame where the user's arms is most extended
        heighest_pos, target = -(0x01<<31), None
        for b in self.training:
            neckPos = b.getJoint("Neck")
            if neckPos[1] > heighest_pos and b.elbowCosTheta < 0:
                heighest_pos, target = neckPos[1], b

        if(onWorking):
            self.isValidHipPosition(target)

    def isValidHipPosition(self, body):
        hipPos      = body.getAveragePosition("Hip")
        shoulderPos = body.getAveragePosition("Shoulder")
        anklePos    = body.getAveragePosition("Ankle")

        vecAnkleShoulder= [(shoulderPos[0] - anklePos[0]), (shoulderPos[1] - anklePos[1])]
        vecAnkleHip     = [(hipPos[0] - anklePos[0]), (hipPos[1] - anklePos[1])]
        normVecAnkleShoulder = sqrt(vecAnkleShoulder[0]*vecAnkleShoulder[0] + vecAnkleShoulder[1]*vecAnkleShoulder[1])
        outer_product   = vecAnkleShoulder[0]*vecAnkleHip[1] - vecAnkleShoulder[1]*vecAnkleHip[0]
        distHipBodyLine = abs(outer_product) / float(normVecAnkleShoulder)
        print(distHipBodyLine)

        if(distHipBodyLine < -0.25*normVecAnkleShoulder):
            st = Status(self.segment_id, "form", 5)
            self.appenStatus(st)
        elif(distHipBodyLine > 0.25*normVecAnkleShoulder):
            st = Status(self.segment_id, "form", 6)
            self.appenStatus(st)
