#!/usr/bin/python
'''
This program just shows off a simple example of using GTK with SimpleCV

This example interfaces with a Camera in real time

It's a very simple way to update an image using python and GTK.
The image is being updated as the slider is moved.
The only amount of SimpleCV code is found in the process_image() function

'''
import RPi.GPIO as GPIO
import time
print __doc__

import gtk
import SimpleCV
import gobject

cam = SimpleCV.Camera()

class app(gtk.Window):

	#Program Settings (You can change these)
	x_pos = 15
	y_pos = 15
	max_x = 31
	min_x = 0
	max_y = 31
	min_y = 0
	window_width = 500
	window_height = 500
	refresh_rate = 100 #in milliseconds
	#End Program Settings
	
	#Variables
	current_image = None

	#This function setup's the program
	def __init__(self):
		super(app, self).__init__()
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_title("LED controller")
		self.set_decorated(True)
		self.set_has_frame(False)
		self.set_resizable(False)
		self.set_default_size(self.window_width,self.window_height)
		self.connect("destroy", gtk.main_quit)
		vbox = gtk.VBox(spacing=4)


		#Setup the horizontal slider bar
		scaleX = gtk.HScale()
		scaleX.set_range(self.min_x, self.max_x)
		scaleX.set_size_request(500, 25)
		scaleX.set_value(self.x_pos)
		scaleX.connect("value-changed", self.update_x)
		vbox.add(scaleX)
		
		#Setup the vertical slider bar
		scaleY = gtk.VScale()
		scaleY.set_range(self.min_y, self.max_y)
		scaleY.set_size_request(25, 500)
		scaleY.set_value(self.y_pos)
		scaleY.connect("value-changed", self.update_y)
		vbox.add(scaleY)

		#Setup the information label
		info = gtk.Label()
		info.set_label("Move the slider to move the LED")
		vbox.add(info)

		#Add the image to the display
		#new_image = self.process_image()
		#converted_image = gtk.gdk.pixbuf_new_from_array(new_image, gtk.gdk.COLORSPACE_RGB, 8)
		#image = gtk.Image()
		#image.set_from_pixbuf(converted_image)
		#image.show()
		#vbox.add(image)


		gobject.timeout_add(self.refresh_rate, self.refresh)
		#self.current_image = image
		self.add(vbox)
		self.show_all()


	def refresh(self):
		#self.update_image()
		return True



	def update_LED(self):
		self.show_all()
		

	#This function is called anything the slider is moved
	def update_x(self, w):
		#grab the value from the slider
		self.x_pos = w.get_value()
		self.update_LED()
		
	def update_y(self, w):
		#grab the value from the slider
		self.y_pos = w.get_value()
		self.update_LED()
		
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

program1 = app()
gtk.main()
