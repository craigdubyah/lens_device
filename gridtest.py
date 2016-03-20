
from SimpleCV import *
cam = Camera()
disp = Display()



import gi, time, gtk
from gi.repository import GObject
import RPi.GPIO as GPIO
gi.require_version('Gtk', '3.0')


xpos,ypos,xcoord,ycoord = 15,15,15,15
 
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
    coord_transform()
    set_pixel(xcoord,ycoord,4)
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
        time.sleep(0.00001)
 
def fill_rectangle(x1, y1, x2, y2, color):
    for x in range(x1, x2):
        for y in range(y1, y2):
            screen[y][x] = color
 

def coord_transform():
	global xcoord, ycoord, xpos, ypos
	ypos = ypos % 32
	xpos = xpos % 32
	xcoord =31-(xpos + 32*(ypos//16))
	ycoord=ypos - 16*(ypos//16)
	
def set_pixel(x, y, color):
    screen[y][x] = color


def pressUL(self, data=None):
	global xpos,ypos
	xpos -=1
	ypos +=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)

def pressU(self, data=None):
	global xpos,ypos
	ypos +=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)

def pressUR(self, data=None):
	global xpos,ypos
	xpos +=1
	ypos +=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)

def pressL(self, data=None):
	global xpos,ypos
	xpos -=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)
	
def pressR(self, data=None):
	global xpos,ypos
	xpos +=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)

def pressDL(self, data=None):
	global xpos,ypos
	xpos -=1
	ypos -=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)
	
	
def pressD(self, data=None):
	global xpos,ypos
	ypos -=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)
	
def pressDR(self, data=None):
	global xpos,ypos
	xpos +=1
	ypos -=1
	fill_rectangle(0,0,64,16,0)
	print "x is " + str(xpos) + " y is " + str(ypos)


def pressSnap(self, data=None):
	print "Snap a picture"
		
from gi.repository import Gtk

class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Grid Example")

        grid = Gtk.Grid()
        self.add(grid)

        buttonUL = Gtk.Button(label="UL")
        buttonU = Gtk.Button(label="U")
        buttonUR = Gtk.Button(label="UR")
        buttonL = Gtk.Button(label="L")
        buttonSnap = Gtk.Button(label="Snap")
        buttonR = Gtk.Button(label="R")
        buttonDL = Gtk.Button(label="DL")
        buttonD = Gtk.Button(label="D")
        buttonDR = Gtk.Button(label="DR")

        grid.attach(buttonUL,0,0,1,1)
        grid.attach(buttonU,1,0,1,1)
        grid.attach(buttonUR,2,0,1,1)
        grid.attach(buttonL,0,1,1,1)
        grid.attach(buttonSnap,1,1,1,1)
        grid.attach(buttonR,2,1,1,1)
        grid.attach(buttonDL,0,2,1,1)
        grid.attach(buttonD,1,2,1,1)
        grid.attach(buttonDR,2,2,1,1)
        
        buttonUL.connect("pressed", pressUL, None)
        buttonU.connect("pressed", pressU, None)
        buttonUR.connect("pressed", pressUR, None)
        buttonL.connect("pressed", pressL, None)
        buttonSnap.connect("pressed", pressSnap, None)
        buttonR.connect("pressed", pressR, None)
        buttonDL.connect("pressed", pressDL, None)
        buttonD.connect("pressed", pressD, None)
        buttonDR.connect("pressed", pressDR, None)
        
	def led_cycle(self, data="none"):
		refresh()
		return True
			
	def camera_cycle(self, data="none"):
		img = cam.getImage()
		img.save(disp)
		return True
        
        self.timeout_id = GObject.timeout_add(20, led_cycle, None)
        self.timeout_ds = GObject.timeout_add(2000, camera_cycle, None)
        

win = GridWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
