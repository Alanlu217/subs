import pygame
import cv2
import numpy

#This shows an image weirdly...
screen_width, screen_height = 640, 480

class camera():
  def __init__(self, camera_index, color, size):
    self.camera = cv2.VideoCapture(camera_index)
    self.camera.set(3, size[0])
    self.camera.set(4, size[1])
    self.color = color

  def getCamFrame(self):
    retval,frame = self.camera.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if not self.color:
      frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    frame = numpy.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame

  def blitCamFrame(self, screen, xy):
    screen.blit(self.getCamFrame(), xy)

cam = camera(0, True, (480, 360))
screen = pygame.display.set_mode((screen_width, screen_height))

running = True
while running:
  for event in pygame.event.get(): #process events since last loop cycle
    if event.type == pygame.KEYDOWN:
      running = False

  screen.fill(0) #set pygame screen to black
  cam.blitCamFrame(screen, (0, 0))
  pygame.display.flip()
cv2.destroyAllWindows()