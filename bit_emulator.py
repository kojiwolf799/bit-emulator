# bit_emulator.py
import pygame
import sys
from framebuffer import FrameBuffer

pygame.init()

WIDTH = 128
HEIGHT = 128
SCALE = 4

screen = pygame.display.set_mode(
    (WIDTH*SCALE, HEIGHT*SCALE)
)

pygame.display.set_caption("Bit Emulator")

clock = pygame.time.Clock()


# ---------------- DISPLAY EMULATOR ----------------

class Display:

    Color = type("Color", (), {
        "Cyan": (0,255,255),
        "Green": (0,255,0),
        "White": (255,255,255),
        "Black": (0,0,0)
    })

    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT))

    def fill(self,color):
        self.surface.fill(color)

    def rect(self,x,y,w,h,color,filled=True):
        pygame.draw.rect(
            self.surface,
            color,
            (x,y,w,h)
        )

    def text(self,text,x,y,color=(255,255,255)):
        font = pygame.font.SysFont(None,12)
        img = font.render(str(text),True,color)
        self.surface.blit(img,(x,y))

    def blit(self, image, x, y, transparent=None):

        if isinstance(image, FrameBuffer):

            image = image.to_surface(transparent)


        self.surface.blit(
            image,
            (x,y)
        )


    def commit(self):
        scaled = pygame.transform.scale(
            self.surface,
            (WIDTH*SCALE,HEIGHT*SCALE)
        )

        screen.blit(scaled,(0,0))
        pygame.display.flip()



display = Display()



# ---------------- BUTTON EMULATOR ----------------

class Buttons:

    def __init__(self):
        self.press = {}
        self.release = {}

    def on_press(self,key,func):
        self.press[key]=func

    def on_release(self,key,func):
        self.release[key]=func


    def scan(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:

                if event.key in self.press:
                    self.press[event.key]()


            if event.type == pygame.KEYUP:

                if event.key in self.release:
                    self.release[event.key]()


buttons = Buttons()



# Fake Bit buttons

class ButtonNames:
    A = pygame.K_a
    B = pygame.K_b


Buttons = ButtonNames



def begin():
    pass
