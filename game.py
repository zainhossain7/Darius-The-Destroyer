import sys
import subprocess
import importlib.util

# Check if pygame is installed, if not install it
if importlib.util.find_spec("pygame") is None:
    print("Pygame is not installed. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Pygame installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install Pygame. Please install it manually using: pip install pygame")
        sys.exit(1)

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
BLOCK_WIDTH = 30
BLOCK_HEIGHT = 30
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
PLAYER_SPEED = 5
BLOCK_SPEED = 3
BULLET_SPEED = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Block Shooter")

class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - self.height - 10
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= PLAYER_SPEED
        if direction == "right" and self.x < WINDOW_WIDTH - self.width:
            self.x += PLAYER_SPEED
        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class Block:
    def __init__(self):
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bounced = False

    def move(self):
        self.y += BLOCK_SPEED
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

class Bullet:
    def __init__(self, x, y):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x + PLAYER_WIDTH // 2 - self.width // 2
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y -= BULLET_SPEED
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

def main():
    clock = pygame.time.Clock()
    player = Player()
    blocks = []
    bullets = []
    block_spawn_timer = 0
    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x, player.y))

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")

        # Spawn blocks
        block_spawn_timer += 1
        if block_spawn_timer >= 60:  # Spawn block every 60 frames
            blocks.append(Block())
            block_spawn_timer = 0

        # Update bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < -bullet.height:
                bullets.remove(bullet)

        # Update blocks and check collisions
        for block in blocks[:]:
            block.move()
            
            # Check bullet collisions
            for bullet in bullets[:]:
                if block.rect.colliderect(bullet.rect):
                    blocks.remove(block)
                    bullets.remove(bullet)
                    player.health = min(150, player.health + 10)  # Add health, max 150
                    break

            # Check if block hits bottom
            if block.y >= WINDOW_HEIGHT:
                if not block.bounced:
                    player.health -= 10  # Reduce health
                    block.bounced = True
                block.y = WINDOW_HEIGHT - block.height
                
            # Remove block if it's bounced and gone off screen
            if block.bounced and block.y < -block.height:
                blocks.remove(block)

        # Clear screen
        screen.fill(BLACK)

        # Draw everything
        player.draw()
        for bullet in bullets:
            bullet.draw()
        for block in blocks:
            block.draw()

        # Draw health bar
        health_text = f"Health: {player.health}"
        font = pygame.font.Font(None, 36)
        text = font.render(health_text, True, WHITE)
        screen.blit(text, (10, 10))

        # Check game over
        if player.health <= 0:
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main() 