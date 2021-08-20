import cv2
import numpy as np

import momentum
import momentum.Artist

rootPath = "./"

imgPath = rootPath + "clock.jpg"
writePath = rootPath + "out.png"

steps = 120

artist = momentum.Artist.Artist(imgPath = imgPath)

print("\nBeginning descent process.")
print("\nImage Settings:")
print("    Input :", imgPath)
print("    Size  :", momentum.CONSTANTS.IMG_SIZE)
print("\nHyperparameters:")
print("    Steps       :", steps)
print("    Brush mass  :", momentum.CONSTANTS.BRUSH_MASS)
print("    Gravity     :", momentum.CONSTANTS.GRAVITY)
print("    Max Velocity:", momentum.CONSTANTS.MAX_VELOCITY)
print("    Drag        :", momentum.CONSTANTS.DRAG)

img = artist.paint(steps)

cv2.imwrite(writePath, img)

print("\nDescent complete! Output saved to:")
print("    ", writePath)