import pygame
from Cells import Icosphere

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import randint

def make_starting_state(x):
   for face in x.faces:
      face.value = randint(0, 1)

def main():
   pygame.init()
   display = (800,600)
   pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

   x = Icosphere(3)
   x.calcNeighbours()
   make_starting_state(x)
   #x.faces[25].value = 1
   #x.faces[26].value = 1
   #x.faces[27].value = 1
   for face in x.faces:
      face.update_color()

   gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

   glTranslatef(0.0,0.0, -5)
   glEnable(GL_DEPTH_TEST)
   glRotatef(-1, 3, 1, 1)
   loop = 0
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
            glVertex3fv(vertex)
      glEnd()

      loop += 1
      if loop == 20:
         loop = 0
         for face in x.faces:
            face.cal_next_value()

         for face in x.faces:
            face.change_to_next_value()
            face.update_color()

      pygame.display.flip()
      pygame.time.wait(10)

main()