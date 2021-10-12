import serial
import pygame as pg
import time
from sys import argv, exit
from pygame.locals import *
import cv2
import threading
import numpy
import traceback
from struct import unpack

def sign(val):
  if val == 0:
    return 0
  return val/abs(val)

def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Open serial port
if len(argv) == 3:
  testing = False
  try:
    ser = serial.Serial(argv[2], 115200, timeout=0.1)
  except:
    print("Please provide the serial port and baudrate")
    print("If provided, please make sure the correct serial port has been selected")
    exit()
else:
  testing = True

class joystick():
  def __init__(self):
    self.axis=[0, 0, 0, 0, 0, 0]
    self.btn=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.btnP=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.lastBtn=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.state = False
    self.on = True
    try:
      self.js = pg.joystick.Joystick(0)
      self.js.init()
      print(self.js.get_name())
    except: self.on = False; print("No Joystick")

  def update(self):
    if self.on:
      # Update axis
      for i in range(0, self.js.get_numaxes()):
        n = round(self.js.get_axis(i)*255)
        if -5 < n < 5:
          self.axis[i] = 0
        else:
          self.axis[i] = n

      # Update buttons
      for i in range(0, self.js.get_numbuttons()):
        self.btn[i] = self.js.get_button(i)
        if self.btn[i] == 1 and self.lastBtn[i] == 0:
          self.btnP[i] = 1
        else:
          self.btnP[i] = 0
      self.lastBtn = self.btn[:]

      # Change state if button 6 is pressed
      if self.btnP[stateKey] == 1:
        if self.state == True: self.state = False
        elif self.state == False: self.state = True


  def getAxis(self, i):
    return self.axis[i]

  def getBtn(self, i):
    return self.btn[i]

class camera():
  def __init__(self, camera_index, color, size):
    self.camera = cv2.VideoCapture(camera_index)
    self.camera.set(3, size[0])
    self.camera.set(4, size[1])
    self.color = color
    self.size = size
    self.lastFrame = None

  def getCamFrame(self):
    if js.btn[0]:
      return self.lastFrame
    else:
      retval,frame = self.camera.read()
      if retval != True:
        frame = self.lastFrame
      frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
      if not self.color:
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
      frame = numpy.rot90(frame)
      frame = pg.surfarray.make_surface(frame)
      self.lastFrame = frame
    return frame

  def blitCamFrame(self, screen, xy):
    frame = pg.transform.flip(pg.transform.scale(self.getCamFrame(), (self.size[0], self.size[1])), True, False)
    screen.blit(frame, [xy[0]-self.size[0]/2, xy[1]-self.size[1]/2])

def updateGUI():
  # Draw Joystick containers
  # Left Joystick
  pg.draw.circle(screen, BLUE, [120, scrnDM[1]-120], 100)
  pg.draw.circle(screen, (0, 0, 0), [120, scrnDM[1]-120], 98)
  pg.draw.circle(screen, RED if js.btn[10] else WHITE, [js.axis[0]/255*100+120, js.axis[1]/255*100+scrnDM[1]-120], 15)

  # Right Joystick
  pg.draw.circle(screen, BLUE, [scrnDM[0]-120, scrnDM[1]-120], 100)
  pg.draw.circle(screen, (0, 0, 0), [scrnDM[0]-120, scrnDM[1]-120], 98)
  pg.draw.circle(screen, RED if js.btn[11] else WHITE, [js.axis[2]/255*100+scrnDM[0]-120, js.axis[5]/255*100+scrnDM[1]-120], 15)

  # Left Trigger
  pg.draw.rect(screen, BLUE, [120, 280, 10, 255])
  pg.draw.circle(screen, RED if js.btn[4] else WHITE, [125, 280+(js.getAxis(3)+255)/2], 15)
  # Right Trigger
  pg.draw.rect(screen, BLUE, [scrnDM[0]-120, 280, 10, 255])
  pg.draw.circle(screen, RED if js.btn[5] else WHITE, [scrnDM[0]-115, 280+(js.getAxis(4)+255)/2], 15)

  # Display information
  text = fnt.render(f'Enabled: {js.state}', False, (0 if js.state else 255, 255 if js.state else 0, 0))
  screen.blit(text, [20, 20])

  # Only change text color if data exists
  if inpt[0] != None:
    inpt[0] = round(inpt[0]*10)/10

    # If temperature greater than 60 degrees, make text red
    if inpt[0] < 60: color1 = WHITE
    else: color1 = RED
    if js.state == False: color1 = GREY

    # If volts is less than 9, make text red
    if inpt[0] > 9: color2 = WHITE
    else: color2 = RED
    if js.state == False: color2 = GREY
  else: 
    color1 = WHITE
    color2 = WHITE

  text = fnt.render(f'Amps: {amps}', False, WHITE if amps == None or js.state else GREY)
  screen.blit(text, [20, 60])
  text = fnt.render(f'Temp: {inpt[0]}', False, color1)
  screen.blit(text, [20, 100])
  text = fnt.render(f'Volts: {inpt[1]}', False, color2)
  screen.blit(text, [20, 140])

  pg.draw.rect(screen, BLUE, [scrnDM[0]/2-cam.size[0]/2-12, scrnDM[1]/2-cam.size[1]/2-12, cam.size[0]+24, cam.size[1]+24])
  pg.draw.rect(screen, BLACK, [scrnDM[0]/2-cam.size[0]/2-9, scrnDM[1]/2-cam.size[1]/2-9, cam.size[0]+18, cam.size[1]+18])
  cam.blitCamFrame(screen, (scrnDM[0]/2, scrnDM[1]/2))

def getState(val, msg):
  res = 0
  msg <<= 2
  if val > 1: msg |= 2
  elif val < -1: msg |= 1
  elif val == 0: msg |= 0
  return msg

def listCams():
  index = 0
  arr = []
  while True:
      cap = cv2.VideoCapture(index)
      if not cap.read()[0]:
          break
      else:
          arr.append(index)
      cap.release()
      index += 1
  return arr

def getCamImg():
  global curImg, stop
  while not stop:
    curImg = cam.getCamFrame()

# Init pygame features
pg.init()
pg.font.init()
pg.joystick.init()

clock = pg.time.Clock()

scrnDM = (1200, 800)
screen = pg.display.set_mode(scrnDM)
fnt = pg.font.SysFont('Arial', 28)
RQST = pg.USEREVENT+1
pg.time.set_timer(RQST, 1500)

# Create classes
js = joystick()
cam = camera(int(argv[1]), True, (586, 442))

# Setup Camera thread
camThread = threading.Thread(target=getCamImg)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BLUE = (10, 10, 255)
RED = (255, 10, 10)
GREEN = (10, 255, 10)

# Declare variables
stop = False
lightOn = False
defualtMsg = [0xAF, 0x54, 0, 0, 0, 0]
msg = defualtMsg
lastMsg = defualtMsg

xjoy = 0
yjoy = 1
stateKey = 12
LTrig = 3
RTrig = 4
power = 1
maxAmps = 9; maxTotal = (0.1 * maxAmps + 0.2945)*256
amps = None
resp = [0, 0, 0, 0, 0]
inpt = [None, None]
request = False
verbose = False
mtr1 = 0
mtr2 = 0
mtr3 = 0

# Msg numbers
ctrl = 1
ctrl2 = 2
MOTOR1 = 4
MOTOR2 = 3
MOTOR3 = 5

# Start Camthread
camThread.start()

# Main loop
try:
  while stop != True:
    # Get events
    js.update()
    keys = pg.key.get_pressed()
    events = pg.event.get()
    if RQST in [event.type for event in events] and js.state: request = True
    if keys[pg.K_q] and keys[pg.K_p]: stop = True
    if js.btn[8] and js.btn[9]: stop = True
    if pg.event.get(pg.QUIT): stop = True

    # Start on Graphics
    screen.fill((0, 0, 0))
    updateGUI()

    if js.state:
      # reset message
      msg = defualtMsg[:]

      # Toggle lights on button 2 press
      if js.btnP[2]: lightOn = not lightOn
      msg[ctrl] = 0x2A # Set byte to correct byte
      msg[ctrl] <<= 1 # Right shift by one to allow space for lightOn bit
      msg[ctrl] |= lightOn # Set bit on or off depending on button status

      # Set bit on or off depending on state
      msg[ctrl2] |= 1 if js.state else 0
      msg[ctrl2] <<= 1

      # Every 1.5 seconds, computer will request
      if request:
        msg[ctrl2] |= 1
      else:
        msg[ctrl2] |= 0

      # Calculate motor 3 values / Up Down
      mtr3 = -int(((js.getAxis(RTrig) - js.getAxis(LTrig))/2))
      msg[ctrl2] = getState(mtr3, msg[ctrl2])
      msg[MOTOR3] = abs(mtr3)

      # Calculate motor 2 values / Right
      mtr2 = -max(min(-js.getAxis(yjoy)-js.getAxis(xjoy), 255), -255)
      msg[ctrl2] = getState(mtr2, msg[ctrl2])
      msg[MOTOR2] = abs(mtr2)

      # Calculate motor 1 values / Left
      mtr1 = -max(min(-js.getAxis(yjoy)+js.getAxis(xjoy), 255), -255)
      msg[ctrl2] = getState(mtr1, msg[ctrl2])
      msg[MOTOR1] = abs(mtr1)

      # Scale down values to fit under a set amount of amps
      total = msg[MOTOR1] + msg[MOTOR2] + msg[MOTOR3]
      if total > maxTotal:
        power = total/maxTotal
        for i in range(3, 6):
          msg[i] /= power
          msg[i] = int(msg[i])

      # Calculate the amps used
      totalPercentage = msg[MOTOR1]/256 + msg[MOTOR2]/256 + msg[MOTOR3]/256
      amps = 10 * totalPercentage - 2.9
      amps = 0 if amps < 0 else amps
      amps = round(amps*100)/100

      # Make sure message is valid
      if len(msg) != len(defualtMsg):
        msg = defualtMsg

      # Only send message if changed
      if msg != lastMsg and not testing:
        # print(msg, lastMsg)
        ser.write(msg)
        time.sleep(0.005) # Allow time for data to send
        if request:
          try: # In case of message failure
            request = False # Reset request
            ret = ser.read(5) # Read 5 bytes from serial
            if ret == b'': # If nothing sent back
              print("timeout") # raise exception
              raise serial.serialutil.SerialTimeoutException
            else: # If message is valid
              resp = unpack("5B", ret)
              temp = bytearray(resp[:4])
              inpt[0] = unpack('<f', temp)[0]
              inpt[1] = resp[4]/10
              while ser.in_waiting: # Get rid of all other bytes
                ser.read()
          except:
            print("Message Error")

      # Update lastMsg
      lastMsg = msg[:]
    # If disabled, turn off all Arduino features
    elif not testing:
      ser.write(defualtMsg)

    # If touchpad pressed, print debug info
    if js.btnP[13]: verbose = not verbose
    if verbose: print([mtr1, mtr2, mtr3])

    # Update display
    pg.display.flip()
    clock.tick(60)
except:
  # Print error message if there is one
  traceback.print_exc()
finally:
  # On exit, tell arduino to turn all motors off
  if not testing:
    ser.write(defualtMsg)
  # Wait for camthread to stop
  camThread.join()