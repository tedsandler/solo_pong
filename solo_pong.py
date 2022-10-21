# Import the pygame module
import sys
import numpy as np
import numpy.random as npr
import pygame


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def get_speed(thing):
    dx = thing.dx
    dy = thing.dy
    return np.sqrt(dx*dx + dy*dy)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.w = 150
        self.h = 25
        self.surf = pygame.Surface( (self.w, self.h) )
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect( center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50) )

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-12, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(12, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = 20
        self.w = size
        self.h = size
        self.surf = pygame.Surface( (self.w, self.h) )
        self.color = (206,250,5)
        pygame.draw.circle(self.surf, self.color, (self.w//2, self.h//2), 10)
        self.rect = self.surf.get_rect( center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2) )
        self.dx = 5 * npr.randn()
        self.dy = 6
        self.bounce_counter = 0

    def update(self, bounced):
        self.rect.move_ip(self.dx, self.dy)

        if self.rect.left <= 0:
            self.dx = abs(self.dx)
        if self.rect.right >= SCREEN_WIDTH:
            self.dx = -abs(self.dx)
        if self.rect.top <= 0:
            self.dy = abs(self.dy)
        if bounced:
            old_speed = get_speed(self)
            self.dx = self.dx + npr.randn() * 2
            self.dy = -abs(self.dy)
            new_speed = get_speed(self)
            self.dx = self.dx * (old_speed/new_speed)
            self.dy = self.dy * (old_speed/new_speed)
            self.bounce_counter = self.bounce_counter + 1
            if self.bounce_counter % 5 == 0:
                self.dx = self.dx*1.025
                self.dy = self.dy*1.025
            
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.dy = -abs(self.dy)
            print("oops!")


player = Player()
ball = Ball()
running = True


while running:

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player and ball based on user keypresses and new situation
    player.update(pressed_keys)
    is_collision = pygame.sprite.spritecollideany(player, [ball])
    ball.update(is_collision)

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)
    screen.blit(ball.surf, ball.rect)

    # Update the display
    pygame.display.flip()
