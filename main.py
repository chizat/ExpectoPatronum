#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
from time import sleep
import pi3d
import logging
import os
import random

logger = logging.getLogger('patronus')
hdlr = logging.FileHandler('patronus.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.propagate = False
logger.info("Starting Program")

#black backgroud left transparent during development
BACKGROUND = (0.0,0.0,0.0,1.0)

#set display, this is fullscreen but I really don't know why or how
DISPLAY = pi3d.Display.create(background=BACKGROUND,x=0, y=0, frames_per_second=15)

#not a clue what this does
shader = pi3d.Shader("uv_flat")

alpha_step = 0.01

#set up sprites for each image
img_dir = "images"

images = []

logger.info("Loading images")

for file in os.listdir(img_dir):
	images.append(pi3d.ImageSprite(img_dir + "/" + file, shader, w = 20, h = 15));
logger.info("Images loaded")

#allow keyboard input (temporary final product with use the GPIO  header)
mykeys = pi3d.Keyboard()

image_displayed = 0
working = 0

#this funtion fades the skull image onto the screen
def fade_in(image):
    logger.info("Fade In")
    alpha = 0
    while DISPLAY.loop_running():
        image.set_alpha(alpha)
        image.draw()
        alpha = (alpha + alpha_step)
        if alpha > 1.01:
            break
    logger.info("Fade In End")

def fade_out(image):
    logger.info("Fade Out")
    alpha = 1
    while DISPLAY.loop_running():
        image.set_alpha(alpha)
        image.draw()
        alpha = (alpha - alpha_step)
        if alpha < 0:
	    break
    image.set_alpha(-1)
    image.draw()
    logger.info("Fade Out End")

#main program loop          
action = 0
while True:
    action = mykeys.read()
    logger.info(action)
    if action == 32 and working == 0 and image_displayed == 0: #s for skull
	logger.info("Space for face in")
	image_displayed = 1
	working = 1
	curr_image = random.choice(images)
        fade_in(curr_image)
	working = 0
        action = 0
    if action == 32 and working == 0 and image_displayed == 1: #space
	logger.info("Space for face out")
	working = 1
        fade_out(curr_image)
	working = 0
	image_displayed = 0
        action = 0
    if action == 27: #esc for exit
        action = 0
        mykeys.close()
        DISPLAY.destroy()
        break


