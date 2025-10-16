import pygame
import random


# Initialize the mixer
pygame.mixer.init()

# Load sound effects
sound_paddle_hit = pygame.mixer.Sound("sounds/paddle_hit.wav")
sound_wall_bounce = pygame.mixer.Sound("sounds/wall_bounce.wav")
sound_score = pygame.mixer.Sound("sounds/score.wav")



class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            sound_wall_bounce.play()  # 🆕 Play bounce sound

    def check_collision(self, player, ai):
        ball_rect = self.rect()

        if ball_rect.colliderect(player.rect()):
            self.velocity_x = abs(self.velocity_x)  # move right
            self.x = player.rect().right
            sound_paddle_hit.play()  # 🆕 Paddle hit sound

        elif ball_rect.colliderect(ai.rect()):
            self.velocity_x = -abs(self.velocity_x)  # move left
            self.x = ai.rect().left - self.width
            sound_paddle_hit.play()  # 🆕 Paddle hit sound

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        sound_score.play()  # 🆕 Play scoring sound

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)