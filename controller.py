import serial
import pygame as pg
import time
from sys import argv, exit

def sign(val):
  if val == 0:
    return 0
  return val/abs(val)

def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
  ser = serial.Serial(argv[1], 115200)
except:
  print("Please provide the serial port and baudrate")
  print("If provided, please make sure the correct serial port has been selected")
  exit()

class joystick():
  def __init__(self):
    self.js = pg.joystick.Joystick(0)
    self.js.init()
    if self.js.get_name() != 'PS4 Controller':
      print("Wrong controller")
      stop = True
    self.axis=[0, 0, 0, 0, 0, 0]
    self.btn=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.btnP=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.lastBtn=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.state = False

  def update(self):
    for i in range(0, self.js.get_numaxes()):
      n = round(self.js.get_axis(i)*255)
      if -5 < n < 5:
        self.axis[i] = 0
      else:
        self.axis[i] = n
    for i in range(0, self.js.get_numbuttons()):
      self.btn[i] = self.js.get_button(i)
      if self.btn[i] == 1 and self.lastBtn[i] == 0:
        self.btnP[i] = 1
      else:
        self.btnP[i] = 0
    self.lastBtn = self.btn[:]
    if self.btnP[5] == 1:
      if self.state == True: self.state = False
      elif self.state == False: self.state = True

  def getAxis(self, i):
    return self.axis[i]

  def getBtn(self, i):
    return self.btn[i]


# Init pygame features
pg.init()
pg.font.init()
pg.joystick.init()
clock = pg.time.Clock()

scrnDM = (800, 600)
screen = pg.display.set_mode(scrnDM)
fnt = pg.font.SysFont('Comic Sans MS', 30)

js = joystick()

# Declare variables
stop = False

# Main loop
while stop != True:
  # Get events
  js.update()
  keys = pg.key.get_pressed()
  events = pg.event.get()
  if keys[pg.K_q]: stop = True
  if pg.event.get(pg.QUIT): stop = False

  print(js.state)
  screen.fill((0, 0, 0))

  # Draw Joystick containers
  pg.draw.circle(screen, (255, 10, 10), [120, 120], 100)
  pg.draw.circle(screen, (0, 0, 0), [120, 120], 98)
  pg.draw.circle(screen, (255, 255, 255), [js.axis[0]/255*100+120, js.axis[1]/255*100+120], 5)
  pg.draw.circle(screen, (255, 10, 10), [scrnDM[0]-120, 120], 100)
  pg.draw.circle(screen, (0, 0, 0), [scrnDM[0]-120, 120], 98)
  pg.draw.circle(screen, (255, 255, 255), [js.axis[2]/255*100+scrnDM[0]-120, js.axis[3]/255*100+120], 5)

  pg.display.flip()
  clock.tick(60)