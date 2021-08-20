import cv2
import numpy as np
import random
import math

import momentum.CONSTANTS

class Surface:
    def __init__(
        self,
        imgPath
    ):

        self.img = self.LoadImg(imgPath)
        self.gradients = {}

    def Get(self, y, x):
        return self.img[int(y), int(x)]

    def Gradient(self, y, x):

        if (y, x) in self.gradients:
            return self.gradients[(y, x)]

        val = self.Get(y, x)

        grads = {}
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                yPos = y + j
                xPos = x + i
                
                if yPos < 0 or yPos >= momentum.CONSTANTS.IMG_SIZE[0]:
                    continue

                if xPos < 0 or xPos >= momentum.CONSTANTS.IMG_SIZE[1]:
                    continue

                grad = int(self.Get(yPos, xPos)) - int(val)
                grads[(j, i)] = grad

        self.gradients[(y, x)] = grads
        
        return grads

    def GetForce(self, brush):
        val = self.Get(brush.position.y, brush.position.x)
        
        forward = self.PixelDirection(brush.velocity)

        if forward.y == 0 and forward.x == 0:
            lowestNeighbor = self.GetLowestNeighbor(forward.y, forward.x)

            if lowestNeighbor is None:
                brush.Die()
                return momentum.Vec2.Vec2(0, 0)

            neighbors = self.GetNeighborPixels(lowestNeighbor.y, lowestNeighbor.x)
        else:
            neighbors = self.GetNeighborPixels(forward.y, forward.x)

        left = neighbors["left"]
        right = neighbors["right"]

        fPos = self.ClampPosition(brush.position.y + forward.y, brush.position.x + forward.x)
        uPos = self.ClampPosition(brush.position.y + right.y, brush.position.x + right.x)
        vPos = self.ClampPosition(brush.position.y + left.y, brush.position.x + left.x)

        forwardVal = self.Get(fPos.y, fPos.x)
        uVal = self.Get(uPos.y, uPos.x)
        vVal = self.Get(vPos.y, vPos.x)
        
        u = right.Subtract(forward)
        v = left.Subtract(forward)

        u = u.ToList(True)
        v = v.ToList(True)

        u.append(uVal - forwardVal)
        v.append(vVal - forwardVal)

        u = np.array(u)
        v = np.array(v)

        norm = np.cross(u, v)
        magnitude = np.linalg.norm(norm)
        #print("   ", norm, right, left)
        #print(forwardVal, uVal, vVal)
        if magnitude != 0:
            norm = norm / magnitude

        gravity = momentum.Vec2.Vec2(
            norm[1] * momentum.CONSTANTS.GRAVITY, 
            norm[0] * momentum.CONSTANTS.GRAVITY
        )

        return gravity

    def GetNeighborPixels(self, y, x):
        if y == -1 and x == -1:
            return { "left": momentum.Vec2.Vec2(0, -1), "right": momentum.Vec2.Vec2(-1, 0) }
        elif y == -1 and x == 0:
            return { "left": momentum.Vec2.Vec2(0, -1), "right": momentum.Vec2.Vec2(0, 1) }
        elif y == -1 and x == 1:
            return { "left": momentum.Vec2.Vec2(-1, 0), "right": momentum.Vec2.Vec2(0, 1) }
        elif y == 0 and x == 1:
            return { "left": momentum.Vec2.Vec2(-1, 0), "right": momentum.Vec2.Vec2(1, 0) }
        elif y == 1 and x == 1:
            return { "left": momentum.Vec2.Vec2(0, 1), "right": momentum.Vec2.Vec2(1, 0) }
        elif y == 1 and x == 0:
            return { "left": momentum.Vec2.Vec2(0, 1), "right": momentum.Vec2.Vec2(0, -1) }
        elif y == 1 and x == -1:
            return { "left": momentum.Vec2.Vec2(1, 0), "right": momentum.Vec2.Vec2(0, -1) }
        elif y == 0 and x == -1:
            return { "left": momentum.Vec2.Vec2(1, 0), "right": momentum.Vec2.Vec2(-1, 0) }

        return None

    def PixelDirection(self, vector):

        theta = math.atan2(vector.y, vector.x)
        theta = theta * 180 / math.pi

        if theta >= 0:
            if theta < 22.5:
                return momentum.Vec2.Vec2(0, 1)
            elif theta < 67.5:
                return momentum.Vec2.Vec2(1, 1)
            elif theta < 112.5:
                return momentum.Vec2.Vec2(1, 0)
            elif theta < 157.5:
                return momentum.Vec2.Vec2(1, -1)
            else:
                return momentum.Vec2.Vec2(0, -1)
        else:
            if -theta < 22.5:
                return momentum.Vec2.Vec2(0, 1)
            elif -theta < 67.5:
                return momentum.Vec2.Vec2(-1, 1)
            elif -theta < 112.5:
                return momentum.Vec2.Vec2(-1, 0)
            elif -theta < 157.5:
                return momentum.Vec2.Vec2(-1, -1)
            else:
                return momentum.Vec2.Vec2(0, -1)

    def GetLowestNeighbor(self, y, x):
        lowesti = None
        lowestj = None
        lowestVal = 1000000000

        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                if i == j:
                    continue

                yPos = y + j
                xPos = x + i

                if yPos < 0 or yPos >= momentum.CONSTANTS.IMG_SIZE[0] or xPos < 0 or xPos >= momentum.CONSTANTS.IMG_SIZE[1]:
                    continue

                val = self.Get(yPos, xPos)

                if val < lowestVal:
                    lowesti = i
                    lowestj = j

        if lowestj is None:
            return None

        return momentum.Vec2.Vec2(lowestj, lowesti)

    def LoadImg(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, momentum.CONSTANTS.IMG_SIZE)

        img = img[:, :, 0]
        img = img / 255

        return img

    def ClampPosition(self, y, x):
        return momentum.Vec2.Vec2(
            max(0, min(y, momentum.CONSTANTS.IMG_SIZE[0] - 1)),
            max(0, min(x, momentum.CONSTANTS.IMG_SIZE[1] - 1)),
        )