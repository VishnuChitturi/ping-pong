import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.winning_score = 5  # 🆕 default target


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)
        
    def check_game_over(self, screen):
        winner = None
        if self.player_score >= self.winning_score:
            winner = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner = "AI Wins!"

        if winner:
            # Display winner message
            screen.fill((0, 0, 0))
            message = self.font.render(winner, True, WHITE)
            rect = message.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(message, rect)

            pygame.display.flip()
            pygame.time.delay(1500)

            # 🆕 Show replay menu
            self.show_replay_menu(screen)

    def show_replay_menu(self, screen):
        screen.fill((0, 0, 0))

        # Render menu text
        title = self.font.render("Choose Replay Mode:", True, WHITE)
        options = [
            self.font.render("Press 3 for Best of 3", True, WHITE),
            self.font.render("Press 5 for Best of 5", True, WHITE),
            self.font.render("Press 7 for Best of 7", True, WHITE),
            self.font.render("Press ESC to Exit", True, WHITE),
        ]

        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 80))
        screen.blit(title, title_rect)

        for i, opt in enumerate(options):
            rect = opt.get_rect(center=(self.width // 2, self.height // 2 - 20 + i * 40))
            screen.blit(opt, rect)

        pygame.display.flip()

        # 🕹 Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 2  # Best of 3 → first to 2
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 3  # Best of 5 → first to 3
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 4  # Best of 7 → first to 4
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # 🆕 Reset scores and ball for a new match
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        self.check_game_over(screen)