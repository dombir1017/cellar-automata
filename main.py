import pygame
from VertData import Cube, Icosphere

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def main():
   pygame.init()
   display = (800,600)
   pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

   x = Icosphere(2)
   x.sort_vert_data()


   gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

   glTranslatef(0.0,0.0, -5)

   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()
      glRotatef(1, 3, 1, 1)
      glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
      
      glBegin(GL_LINES)
      for vertex in x.get_vert_data():
         glVertex3fv(vertex)
      glEnd()

      pygame.display.flip()
      pygame.time.wait(10)

main()