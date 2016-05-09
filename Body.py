#coding: utf-8;
from __future__ import division, print_function, unicode_literals
from future_builtins import *
from math import sqrt,acos,degrees

class Body:
    NAME_MAPPING = {
        "SpineBase"     : 0,
        "SpineMid"      : 1,
        "Neck"          : 2,
        "Head"          : 3,
        "ShoulderLeft"  : 4,
        "ElbowLeft"     : 5,
        "WristLeft"     : 6,
        "HandLeft"      : 7,
        "ShoulderRight" : 8,
        "ElbowRight"    : 9,
        "WristRight"    : 10,
        "HandRight"     : 11,
        "HipLeft"       : 12,
        "KneeLeft"      : 13,
        "AnkleLeft"     : 14,
        "FootLeft"      : 15,
        "HipRight"      : 16,
        "KneeRight"     : 17,
        "AnkleRight"    : 18,
        "FootRight"     : 19,
        "SpineShoulder" : 20,
        "HandTipLeft"   : 21,
        "ThumbLeft"     : 22,
        "HandTipRight"  : 23,
        "ThumbRight"    : 24,
    }

    @staticmethod
    def create_body_from_frame(frame):
        ## frame["coordinates"] is a list that consists of joint coordinates
        return Body(frame["coordinates"])

    def calcKneeCosTheta(self):
        hip     = self.getAveragePosition("Hip")
        knee    = self.getAveragePosition("Knee")
        ankle   = self.getAveragePosition("Ankle")
        vecKneeHip      = [(hip[0] - knee[0]), (hip[1] - knee[1])]
        vecKneeAncle    = [(ankle[0] - knee[0]), (ankle[1] - knee[1])]
        normVecKneeHip  = sqrt(vecKneeHip[0]*vecKneeHip[0] + vecKneeHip[1]*vecKneeHip[1])
        normVecKneeAnkle= sqrt(vecKneeAncle[0]*vecKneeAncle[0] + vecKneeAncle[1]*vecKneeAncle[1])
        innerProduct    = vecKneeHip[0]*vecKneeAncle[0] + vecKneeHip[1]*vecKneeAncle[1]
        if(normVecKneeHip * normVecKneeAnkle != 0):
            cos_theta   = innerProduct / float(normVecKneeHip) / float(normVecKneeAnkle)
            return cos_theta
        else:
            return None

    def calcElbowCosTheta(self):
        elbow       = self.getAveragePosition("Elbow")
        Shoulder    = self.getAveragePosition("Shoulder")
        hand        = self.getAveragePosition("Hand")
        vecElbowShoulder    = [(shoulder[0] - elbow[0]), (shoulder[1] - elbow[1])]
        vecElbowHand        = [(ankle[0] - elbow[0]), (ankle[1] - elbow[1])]
        normVecElbowShoulder= sqrt(vecElbowShoulder[0]*vecElbowShoulder[0] \
                                    + vecElbowShoulder[1]*vecElbowShoulder[1])
        normVecElbowHand    = sqrt(vecElbowHand[0]*vecElbowHand[0] + vecElbowHand[1]*vecElbowHand[1])
        innerProduct        = vecElbowShoulder[0]*vecElbowHand[0] + vecElbowShoulder[1]*vecElbowHand[1]
        if(normVecElbowShoulder * normVecElbowHand != 0):
            cos_theta   = innerProduct / float(normVecElbowShoulder) / float(normVecElbowHand)
            return cos_theta
        else:
            return None

    def __init__(self, frame):
        self._frame         = frame
        self.kneeCosTheta   = self.calcKneeCosTheta()
        self.elbowCosTheta  = self.calcElbowCosTheta()

    def getJoint(self, joint_name):
        key = Body.NAME_MAPPING[joint_name]
        return self._frame[key]

    def getDirection(self):
        leftHand    = self.getJoint("HandLeft")
        RightHand   = self.getJoint("HandRight")
        head        = self.getJoint("Head")
        if head[0] < leftHand[0] < RightHand[0]:
            return -1
        elif leftHand[0] < RightHand[0] < head[0]:
            return 1
        elif leftHand[0] < head[0] < RightHand[0]:
            return 0
        else:
            return 0

    def getLowerPosition(self, prefix):
        left    = self.getJoint(prefix + "Left")
        right   = self.getJoint(prefix + "Right")
        return (left if left[1] < right[1] else right)

    def getAveragePosition(self, prefix):
        left    = self.getJoint(prefix + "Left")
        right   = self.getJoint(prefix + "Right")
        return ((left[0]+right[0])/2., (left[1]+right[1])/2.)

    def getUpperPosition(self, prefix):
        left    = self.getJoint(prefix + "Left")
        right   = self.getJoint(prefix + "Right")
        return (left if left[1] > right[1] else right)

