#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  controlLED.py
#  
#  Copyright 2016  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import pygame, time
from pygame.locals import *

from SimpleCV import *
cam = Camera()
disp = Display()


pygame.init()
screen = pygame.display.set_mode((640, 480))
#pygame.display.set_caption('Pygame Keyboard Test')
#pygame.mouse.set_visible(0)
xpos=15
ypos=15

import RPi.GPIO as GPIO
import time
 
delay = 0.001
 
GPIO.setmode(GPIO.BCM)
red1_pin = 17
green1_pin = 18
blue1_pin = 22
red2_pin = 23
green2_pin = 24
blue2_pin = 25
clock_pin = 3
a_pin = 7
b_pin = 8
c_pin = 9
latch_pin = 4
oe_pin = 2
 
GPIO.setup(red1_pin, GPIO.OUT)
GPIO.setup(green1_pin, GPIO.OUT)
GPIO.setup(blue1_pin, GPIO.OUT)
GPIO.setup(red2_pin, GPIO.OUT)
GPIO.setup(green2_pin, GPIO.OUT)
GPIO.setup(blue2_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(a_pin, GPIO.OUT)
GPIO.setup(b_pin, GPIO.OUT)
GPIO.setup(c_pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)
GPIO.setup(oe_pin, GPIO.OUT)
 
screen = [[0 for x in xrange(64)] for x in xrange(16)]
 
def clock():
    GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)
 
def latch():
    GPIO.output(latch_pin, 1)
    GPIO.output(latch_pin, 0)
 
def bits_from_int(x):
    a_bit = x & 1
    b_bit = x & 2
    c_bit = x & 4
    return (a_bit, b_bit, c_bit)
 
def set_row(row):
    #time.sleep(delay)
    a_bit, b_bit, c_bit = bits_from_int(row)
    GPIO.output(a_pin, a_bit)
    GPIO.output(b_pin, b_bit)
    GPIO.output(c_pin, c_bit)
    #time.sleep(delay)
 
def set_color_top(color):
    #time.sleep(delay)
    red, green, blue = bits_from_int(color)
    GPIO.output(red1_pin, red)
    GPIO.output(green1_pin, green)
    GPIO.output(blue1_pin, blue)
    #time.sleep(delay)
 
def set_color_bottom(color):
    #time.sleep(delay)
    red, green, blue = bits_from_int(color)
    GPIO.output(red2_pin, red)
    GPIO.output(green2_pin, green)
    GPIO.output(blue2_pin, blue)
    #time.sleep(delay)
 
def refresh():
    for row in range(8):
        GPIO.output(oe_pin, 1)
        set_color_top(0)
        set_row(row)
        #time.sleep(delay)
        for col in range(64):
            set_color_top(screen[row][col])
            set_color_bottom(screen[row+8][col])
            clock()
        #GPIO.output(oe_pin, 0)
        latch()
        GPIO.output(oe_pin, 0)
        time.sleep(delay)
 
def fill_rectangle(x1, y1, x2, y2, color):
    for x in range(x1, x2):
        for y in range(y1, y2):
            screen[y][x] = color
 
 
def set_pixel(x, y, color):
    screen[y][x] = color

#set_pixel(10,1,1) 
#set_pixel(10,2,2)
#set_pixel(10,3,3)
#fill_rectangle(0, 0, 12, 12, 1)
#fill_rectangle(20, 4, 30, 15, 2)
#fill_rectangle(15, 0, 19, 7, 7)
 
while True:
	fill_rectangle(0,0,64,16,0)
	xcoord=31-(xpos + 32*(ypos//16))
	ycoord=ypos - 16*(ypos//16)
	set_pixel(xcoord,ycoord,4)
	refresh()
	for event in pygame.event.get():
		if (event.type == KEYDOWN):
			keystatus=pygame.key.get_pressed()
			if (keystatus[pygame.K_UP]):ypos+=1
			if (keystatus[pygame.K_DOWN]):ypos-=1
			if (keystatus[pygame.K_RIGHT]):xpos+=1
			if (keystatus[pygame.K_LEFT]):xpos-=1
			if (keystatus[pygame.K_x]):exit()
			
			if (xpos<0):xpos=0
			if (xpos>31):xpos=31
			
			if (ypos<0):ypos=0
			if (ypos>31):ypos=31
			
			xpos = xpos % 32
			ypos = ypos % 32
			
			time.sleep(0.03)
			print "x is " + str(xpos) + " y is " + str(ypos)
			print "xcoord is " + str(xcoord) + " ycoord is " + str(ycoord)
			#img = cam.getImage()
			#img.save(disp)
			


