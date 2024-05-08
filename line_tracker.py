# Grace Mahoney
# November 15, 2023
# Challenge: drive along a line

from XRPLib.defaults import *
import time

    
# negative 'direction' turns left, positive 'direction' turns right, 0 does not turn
def turn(direction):
    if(direction > 0):
        drivetrain.set_effort(0.5, -0.8)
        while(reflectance.get_right() <= 0.9):
            drivetrain.set_effort(0.5,-0.8)
        drivetrain.set_effort(0.0,0.0)
    elif(direction < 0):
        drivetrain.set_effort(-0.8,0.5)
        while(reflectance.get_left() <= 0.9):
            drivetrain.set_effort(-0.8,0.5)
        drivetrain.set_effort(0.0,0.0)
    time.sleep(1)
    

def line_track():
    base_effort = 0.6
    KP = 1

    avgR = (reflectance.get_left() + reflectance.get_right())/2
    while (not(avgR <= 0.83)): # Table reflectance is about 0.83
        #print("L:", reflectance.get_left(), "R:", reflectance.get_right())
        avgR = (reflectance.get_left() + reflectance.get_right())/2
        
        if(avgR >= 0.9):
            print("at node")
            drivetrain.set_effort(0.5,0.5)
            time.sleep(0.25)
            drivetrain.set_effort(0,0)
        
        error = reflectance.get_left() - reflectance.get_right()
        print(error)
        drivetrain.set_effort(base_effort - error * KP, base_effort + error * KP)
        time.sleep(0.01)
    drivetrain.set_effort(0,0)
    print("done")


line_track()
turn(-1)