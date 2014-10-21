#!/usr/bin/python
from wiimote import Wiimote
import cwiid
import time

import pi3d
import logging
import os
import random

wii = Wiimote()
wii.connect_wiimote()
wii.connection_fun()

logger = logging.getLogger('patronus')
hdlr = logging.FileHandler('patronus.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.info("Starting Program")

used_sec = 0
validation_sec = 10

#black backgroud left transparent during development
BACKGROUND = (0.0,0.0,0.0,1.0)

#set display, this is fullscreen but I really don't know why or how
DISPLAY = pi3d.Display.create(background=BACKGROUND,x=0, y=0, frames_per_second=15)

#not a clue what this does
shader = pi3d.Shader("uv_flat")

alpha_step_in = 0.01
alpha_step_out = 0.02

#set up sprites for each image
img_dir = "images"

images = []

logger.info("Loading images")

for file in os.listdir(img_dir):
	images.append(pi3d.ImageSprite(img_dir + "/" + file, shader, w = 20, h = 15));
logger.info("Images loaded")

image_displayed = 0
working = 0

def fade_in(image):
    DISPLAY.add_sprites(image)
    start = time.clock();
    logger.info("Fade In")
    alpha = 0
    while DISPLAY.loop_running():
        image.set_alpha(alpha)
        image.draw()
        alpha = (alpha + alpha_step_in)
        if alpha > 1.01:
            break
    end = time.clock()
    logger.info("Fade In End " + repr(end - start))

def fade_out(image):
    start = time.clock();
    logger.info("Fade Out")
    alpha = 1
    while DISPLAY.loop_running():
        image.set_alpha(alpha)
        image.draw()
        alpha = (alpha - alpha_step_out)
        if alpha < 0:
	    break
    end = time.clock()
    DISPLAY.remove_sprites(image)
    logger.info("Fade Out End " + repr(end - start))

#main program loop          
while DISPLAY.loop_running():

    sec = time.localtime(time.time()).tm_sec
    if(sec % validation_sec == 0 and sec != used_sec):
        wii.validate_connection()
        used_sec = sec

    buttons = wii.wiimote.state['buttons']

    if (buttons & cwiid.BTN_A) and working == 0 and image_displayed == 0:
        image_displayed = 1
        working = 1
        curr_image = random.choice(images)
        fade_in(curr_image)
        working = 0
    if (buttons & cwiid.BTN_B) and working == 0 and image_displayed == 1: 
        working = 1
        fade_out(curr_image)
        working = 0
        image_displayed = 0
    if (buttons & cwiid.BTN_1) and working == 0 and image_displayed == 0:
        image_displayed = 1
        working = 1
        fade_in(curr_image)
        working = 0
#    if (buttons & cwiid.BTN_HOME):
#        logger.info("Exit")
#        DISPLAY.destroy()
#        break
