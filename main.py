import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import randint
import time

from VertData import Icosphere

def make_starting_state(x):
   for face in x.faces:
      v = randint(0, 100) / 100
      face.value = 1 if randint(0, 100) > 80 else 0

def main():
   pygame.init()
   display = (800,600)
   pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
   gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

   glTranslatef(0.0,0.0, -5)
   glEnable(GL_DEPTH_TEST)
   glRotatef(-1, 3, 1, 1)

   x = Icosphere(3)
   print(f"Number of faces: {len(x.faces)}")
   x.calcNeighbours()
   make_starting_state(x)
   x.update_color()

   t1 = time.time()
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()

      glRotatef(1, 3, 1, 1)
      glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
      
      glBegin(GL_TRIANGLES)
      for face in x.faces:
         for vertex in face.get_vert_data():
            glColor3f(*face.color)
            glVertex3fv((vertex.x, vertex.y, vertex.z))
      glEnd()

      if time.time() - t1 >= 1:
         for face in x.faces:
            face.cal_next_value()

         for face in x.faces:
            face.change_to_next_value()
            face.recalc_color_from_value()
         t1 = time.time()

      pygame.display.flip()
      pygame.time.wait(10)

main()