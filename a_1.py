"""
    Shoutout PvC
    Used lab 3 solutions from Prof. Michael Nixon as a template for my pygame
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# https://freepngimg.com/save/26525-army/850x1080
player_image = pygame.image.load("img/enemy_agent.png").convert_alpha()
# https://png.pngtree.com/png-vector/20221116/ourmid/pngtree-fighter-jet-military-plane-vector-png-image_6457508.png
enemy_image = pygame.image.load("img/plane.png").convert_alpha()
# https://p7.hiclipart.com/preview/134/753/311/star-night-sky-clip-art-night-stars-cliparts.jpg
background_image = pygame.image.load("img/background.png").convert_alpha()
# https://png.pngtree.com/png-vector/20190814/ourmid/pngtree-cartoon-bomb-background-and-explosive-light-vector---illustration-png-image_1692128.jpg
bomb_image = pygame.image.load("img/bomb2.png").convert_alpha()
# https://i.pinimg.com/736x/5c/00/2d/5c002d216d2fe0782d3f535333091bd2.jpg
health_image = pygame.image.load("img/extra_life2.png").convert_alpha()
# https://png.pngtree.com/png-clipart/20210513/ourmid/pngtree-cartoon-explosion-flame-light-effect-png-image_3268966.jpg
explosion_image = pygame.image.load("img/explosion.png").convert_alpha()
# https://images.rawpixel.com/image_png_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA2L2pvYjk0OC0xODItcF8xLnBuZw.png
enemy_image2 = pygame.image.load("img/plane2.png").convert_alpha()
# https://www.shutterstock.com/image-vector/blood-splatter-icon-high-quality-260nw-2174321057.jpg
explosion_image2 = pygame.image.load("img/explosion2.png").convert_alpha()

score = 0  # Initialize score to 0
lives = 3  # Initialize lives to 3


class Block(pygame.sprite.Sprite):
    """ This class represents the blocks. """

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(enemy_image, (65, 50))
        self.image.set_colorkey(pygame.color.THECOLORS['white'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 1  # Set x velocity to 1

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.x < 0 or self.rect.right > SCREEN_WIDTH:
            self.velocity_x *= -1
            self.rect.y += self.rect.height / 1
        if self.rect.bottom > SCREEN_HEIGHT:
            global score
            score -= 1
            if score < 0:
                pygame.event.post(pygame.event.Event(pygame.QUIT))


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (67, 99))
        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.lives = lives
        self.rect.x = SCREEN_WIDTH / 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Got this line of code from stackoverflow so that the player does not go out of the screen
        # https://stackoverflow.com/questions/67280788/x-position-of-bullet-in-pygame
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def lose_life(self):
        self.lives -= 1


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self, velocity):
        super().__init__()
        self.velocity = velocity

    def update(self):
        self.rect.y += self.velocity


class PlayerBullet(Bullet):
    """ This class represents the Player Bullet.
        This class inherits the Bullet class."""

    def __init__(self):
        super().__init__(-2)
        self.image = pygame.Surface([4, 10])
        self.image.fill(pygame.color.THECOLORS['red'])
        self.rect = self.image.get_rect()


class EnemyBullet(Bullet):
    """ This class represents the Enemy Bullet.
        This class inherits the Bullet class."""
    def __init__(self):
        super().__init__(3)
        self.image = pygame.Surface([4, 10])
        self.image.fill(pygame.color.THECOLORS['white'])
        self.rect = self.image.get_rect()


class MainMenu:
    """ This class represents the main menu of the game. """

    def __init__(self):
        self.running = False
        # Used stackoverflow examples so that I can scale the background properly
        # https://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame
        self.background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.difficulty = None  # Variable to store the chosen difficulty level

    def draw(self):
        # https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
        # From pygame docs, I used SysFont
        screen.blit(self.background, (0, 0))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Shootout PvC", True, pygame.color.THECOLORS['white'])
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))
        screen.blit(text, text_rect)
        font = pygame.font.SysFont(None, 30)
        prompt = font.render("CHOOSE DIFFICULTY :", True, pygame.color.THECOLORS['green'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 150))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("Press 1 For Easy", True, pygame.color.THECOLORS['green'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 100))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("Press 2 For Medium", True, pygame.color.THECOLORS['green'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 50))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("Press 3 For Hard", True, pygame.color.THECOLORS['green'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("HOW TO PLAY :", True, pygame.color.THECOLORS['orange'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 - 150))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("- Use Arrow Keys To Move Left/Right", True, pygame.color.THECOLORS['orange'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 - 100))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("- Press Space Bar To Shoot Bullets", True, pygame.color.THECOLORS['orange'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 - 50))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("- Use Blocks To Protect Yourself Against Enemy Bullets", True, pygame.color.THECOLORS[
            'orange'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("- Eliminate All Enemy Jets To Move To Next Level", True, pygame.color.THECOLORS['orange'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 + 50))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("- Player Has 3 Lives", True, pygame.color.THECOLORS['orange'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 + 100))
        screen.blit(prompt, prompt_rect)
        prompt = font.render("- Watch Out For Bombs!", True, pygame.color.THECOLORS['orange'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 + 150))
        screen.blit(prompt, prompt_rect)

    def run(self):
        self.draw()
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Choose difficulty
                    if event.key == pygame.K_1:
                        waiting = False
                        self.difficulty = "Easy"
                    elif event.key == pygame.K_2:
                        waiting = False
                        self.difficulty = "Medium"
                    elif event.key == pygame.K_3:
                        waiting = False
                        self.difficulty = "Hard"


class Defense(pygame.sprite.Sprite):
    """ This class represents the defense blocks protecting the player. """

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(pygame.color.THECOLORS['green'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3  # Initialize health attribute for defense blocks

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Remove the defense block if health drops to or below 0


class Bomb(pygame.sprite.Sprite):
    """ This class represents the Enemy Bomb."""
    def __init__(self, explosion_radius):
        super().__init__()
        self.image = bomb_image
        self.rect = self.image.get_rect()
        self.rect.x = 0  # Initial x-coordinate
        self.rect.y = 0  # Initial y-coordinate
        self.velocity_y = 2
        self.explosion_radius = explosion_radius # Initialize explosion radius

    def update(self):
        self.rect.y += self.velocity_y


class Explosion(pygame.sprite.Sprite):
    """ This class represents the explosion when the enemy gets hit . """
    def __init__(self, position):
        super().__init__()
        self.image = explosion_image
        self.rect = self.image.get_rect(center=position)  # center the explosion image
        self.duration = 0.2  # Duration of explosion animation in seconds
        self.start_time = pygame.time.get_ticks()

    def update(self):
        # Check if it's time to remove the explosion
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration * 1000:
            self.kill()  # Remove the explosion sprite from the game


class Explosion2(pygame.sprite.Sprite):
    """ This class represents the explosion when the player gets hit . """
    def __init__(self, position):
        super().__init__()
        self.image = explosion_image2
        self.rect = self.image.get_rect(center=position)  # Center the explosion
        self.duration = 0.15  # Duration of explosion animation in seconds
        self.start_time = pygame.time.get_ticks()

    def update(self):
        # Check if it's time to remove the explosion
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration * 1000:
            self.kill()


class ExtraLife(pygame.sprite.Sprite):
    """ This class represents the extra life feature in the game. """
    def __init__(self, element, duration):
        super().__init__()
        self.element = element
        self.duration = duration
        self.image = health_image
        self.rect = self.image.get_rect()

    def apply_effect(self, player):
        if self.element == 'health':
            # Only applies if players lives is below 3
            if player.lives < 3:
                player.lives += 1  # Increase player's lives

    def update(self):
        self.rect.y += 1  # Make power-up fall down the screen


class Boss(pygame.sprite.Sprite):
    """ This class represents the boss enemy. """
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_image2, (100, 75))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH  # Start the boss off-screen to the right
        self.rect.y = SCREEN_HEIGHT - 700
        self.velocity_x = -2
        self.last_bomb_time = pygame.time.get_ticks()
        self.bomb_drop_delay = 2000  # Adjust the delay between bomb drops
        self.bomb_velocity = 2

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.right < 0:
            self.kill()  # Remove the boss sprite when it moves off-screen

    def drop_bomb(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bomb_time > self.bomb_drop_delay:
            bomb = Bomb(explosion_radius=30)  # Create a bomb with an explosion radius of 30 pixels
            bomb.rect.centerx = self.rect.centerx
            bomb.rect.bottom = self.rect.bottom
            bomb.velocity_y = self.bomb_velocity
            self.last_bomb_time = current_time
            return bomb
        return None


class Game:
    """ This class represents the Game. It contains all the game objects. """

    def __init__(self):
        self.num_blocks = 25
        self.running = False
        self.all_sprites_list = pygame.sprite.Group()
        self.block_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        self.background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level = 1
        self.bomb_list = pygame.sprite.Group()
        self.last_bomb_time = pygame.time.get_ticks()
        self.power_ups = pygame.sprite.Group()
        self.last_power_up_spawn_time = pygame.time.get_ticks()
        self.explosion_list = pygame.sprite.Group()
        self.explosion_list2 = pygame.sprite.Group()
        self.boss = None  # Initialize boss as None initially
        self.boss_spawned = False  # Track if boss has been spawned for the current level
        self.defense_block_list = pygame.sprite.Group()
        self.boss_velocity_increase = 1
        self.game_over_reason = None  # Initialize game over reason as None initially

        # Enemy positions coordinates
        enemy_positions = [
            (100, 100), (200, 100), (300, 100), (400, 100), (500, 100),
            (600, 100), (700, 100), (800, 100), (900, 100), (1000, 100),
            (100, 200), (200, 200), (300, 200), (400, 200), (500, 200),
            (600, 200), (700, 200), (800, 200), (900, 200), (1000, 200),
        ]

        for pos in enemy_positions:
            block = Block(pos[0], pos[1])
            self.block_list.add(block)
            self.all_sprites_list.add(block)

        for x in range(600, 700, 10):
            for y in range(500, 530, 10):
                defense_block_positions = [(x, y)]

                for pos in defense_block_positions:
                    defense_block = Defense(pos[0], pos[1])
                    self.defense_block_list.add(defense_block)
                    self.all_sprites_list.add(defense_block)

        for x in range(400, 500, 10):
            for y in range(500, 530, 10):
                defense_block_positions = [(x, y)]

                for pos in defense_block_positions:
                    defense_block = Defense(pos[0], pos[1])
                    self.defense_block_list.add(defense_block)
                    self.all_sprites_list.add(defense_block)

        for x in range(200, 300, 10):
            for y in range(500, 530, 10):
                defense_block_positions = [(x, y)]

                for pos in defense_block_positions:
                    defense_block = Defense(pos[0], pos[1])
                    self.defense_block_list.add(defense_block)
                    self.all_sprites_list.add(defense_block)

        for x in range(800, 900, 10):
            for y in range(500, 530, 10):
                defense_block_positions = [(x, y)]

                for pos in defense_block_positions:
                    defense_block = Defense(pos[0], pos[1])
                    self.defense_block_list.add(defense_block)
                    self.all_sprites_list.add(defense_block)

        self.player = Player()
        self.all_sprites_list.add(self.player)

    def spawn_power_up(self):
        # Randomly spawn a power-up
        power_up = ExtraLife(element='health', duration=0)  # Health power-up
        power_up.rect.x = random.randint(0, SCREEN_WIDTH - power_up.rect.width)
        power_up.rect.y = 0  # Spawn at the top of the screen
        self.power_ups.add(power_up)

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.level == 1:
                        bullet = PlayerBullet()
                        bullet.rect.x = self.player.rect.center[0]
                        bullet.rect.y = self.player.rect.y
                        self.all_sprites_list.add(bullet)
                        self.bullet_list.add(bullet)
                    elif self.level > 1:  # For level 2 and beyond, player shoots two bullets at once
                        bullet1 = PlayerBullet()
                        bullet1.rect.x = self.player.rect.center[0] - 10
                        bullet1.rect.y = self.player.rect.y
                        bullet2 = PlayerBullet()
                        bullet2.rect.x = self.player.rect.center[0] + 10
                        bullet2.rect.y = self.player.rect.y
                        self.all_sprites_list.add(bullet1, bullet2)
                        self.bullet_list.add(bullet1, bullet2)

    def update(self):
        for enemy in self.block_list:
            # Check for collisions with defense blocks
            defense_block_hit_list = pygame.sprite.spritecollide(enemy, self.defense_block_list, False)
            for defense_block in defense_block_hit_list:
                # Game over condition if enemy reaches below defense block
                self.running = False  # End the game
                self.game_over_reason = "Enemies Breached Defense!"

        for enemy in self.block_list:
            die_roll = random.randrange(0, 1000)
            if die_roll > 996:
                b = EnemyBullet()
                b.rect.x = enemy.rect.center[0]
                b.rect.y = enemy.rect.bottom
                self.enemy_bullet_list.add(b)
                self.all_sprites_list.add(b)

        self.all_sprites_list.update()

        for bullet in self.bullet_list:
            block_hit_list = pygame.sprite.spritecollide(
                bullet, self.block_list, True)
            for block in block_hit_list:
                explosion = Explosion(block.rect.center)
                self.all_sprites_list.add(explosion)
                self.explosion_list.add(explosion)

                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
                global score
                score += 10

            if bullet.rect.y < (0 - bullet.rect.height):
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

            defense_block_hit_list = pygame.sprite.spritecollide(bullet, self.defense_block_list, True)
            for defense_block in defense_block_hit_list:
                bullet.kill()

        for bullet in self.enemy_bullet_list:
            if pygame.sprite.spritecollide(self.player, self.enemy_bullet_list, True):
                self.player.lose_life()
                block1 = Block(self.player.rect.x, self.player.rect.y)
                explosion = Explosion2(block1.rect.center)
                self.all_sprites_list.add(explosion)
                self.explosion_list.add(explosion)

                if self.player.lives < 0:
                    self.player.kill()
                    self.running = False

            defense_block_hit_list = pygame.sprite.spritecollide(bullet, self.defense_block_list, True)
            for defense_block in defense_block_hit_list:
                bullet.kill()  # Remove the bullet upon hitting a defense block

        # Check if all enemies are killed to proceed to the next level
        for new_lvl in range(0, 5):
            if len(self.block_list) == 0:
                self.level += 1
                self.spawn_boss()
                self.boss_spawned = True
                # Clear bullets from the previous level
                self.bullet_list.empty()
                self.enemy_bullet_list.empty()
                # Add new enemies
                enemy_positions = [
                    (100, 100), (200, 100), (300, 100), (400, 100), (500, 100),
                    (600, 100), (700, 100), (800, 100), (900, 100), (1000, 100),
                    (100, 200), (200, 200), (300, 200), (400, 200), (500, 200),
                    (600, 200), (700, 200), (800, 200), (900, 200), (1000, 200),
                ]
                for pos in enemy_positions:
                    block = Block(pos[0], pos[1])
                    self.block_list.add(block)
                    self.all_sprites_list.add(block)

        # Check for collisions between bombs and the player
        player_hit_bombs = pygame.sprite.spritecollide(self.player, self.bomb_list, True)
        for bomb in player_hit_bombs:
            self.player.kill()
            self.running = False  # Decrease player's health
            self.game_over_reason = "You got BOMBED"

        for bomb in self.bomb_list:
            defense_block_hit_list = pygame.sprite.spritecollide(bomb, self.defense_block_list, True)

        # Check if any bombs have reached the bottom of the screen
        for bomb in self.bomb_list:
            if bomb.rect.y >= SCREEN_HEIGHT:
                bomb.kill()  # Remove the bomb from the game

        bullet_hit_bombs = pygame.sprite.groupcollide(self.bullet_list, self.bomb_list, True, True)
        for bullet, bombs in bullet_hit_bombs.items():
            for bomb in bombs:
                # Trigger explosion at bomb's position
                explosion = Explosion(bomb.rect.center)
                self.all_sprites_list.add(explosion)
                self.explosion_list.add(explosion)

        self.power_ups.update()

        # Check for collisions between player and power-ups
        power_up_hits = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        for power_up in power_up_hits:
            power_up.apply_effect(self.player)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_power_up_spawn_time > 10000:  # Spawn frequency here
            self.spawn_power_up()
            self.last_power_up_spawn_time = current_time

        if self.boss:
            bomb = self.boss.drop_bomb()
            if bomb:
                self.bomb_list.add(bomb)
                self.all_sprites_list.add(bomb)

        if self.player.lives < 0:
            self.running = False
            self.game_over_reason = "You ran out of lives."

    def spawn_boss(self):
        self.boss = Boss()
        self.boss.bomb_velocity += self.boss_velocity_increase * self.level
        self.all_sprites_list.add(self.boss)

    def draw(self):
        screen.blit(self.background, (0, 0))
        self.all_sprites_list.draw(screen)
        font = pygame.font.SysFont(None, 25)
        text = font.render(f'Lives: {self.player.lives}', True, pygame.color.THECOLORS['green'])
        screen.blit(text, (10, 10))  # Display lives on the top left
        score_text = font.render(f'Score: {score}', True, pygame.color.THECOLORS['green'])
        screen.blit(score_text, (10, 30))  # Display score below lives
        self.bomb_list.draw(screen)
        self.power_ups.draw(screen)

        for lvl_ in range(20):
            default_level = font.render(f'LEVEL {self.level}', True, pygame.color.THECOLORS['green'])
            screen.blit(default_level, (SCREEN_WIDTH - 100, 10))

    def run(self):
        menu = MainMenu()
        menu.run()  # Run the main menu
        self.running = True
        clock = pygame.time.Clock()
        enemy_bullet_velocity = 3  # Default velocity
        if menu.difficulty == "Medium":
            enemy_bullet_velocity += 5
        elif menu.difficulty == "Hard":
            enemy_bullet_velocity += 7
        while self.running:
            for enemy_bullet in self.enemy_bullet_list:
                enemy_bullet.velocity = enemy_bullet_velocity

            self.poll()
            self.update()
            self.draw()  # Call the draw method
            pygame.display.flip()
            clock.tick(60)

        # Game over, ask if the player wants to play again
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render(f"Game Over! {self.game_over_reason}", True, pygame.color.THECOLORS['green'])
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(game_over_text, game_over_rect)
        font = pygame.font.SysFont(None, 30)
        prompt = font.render("Press 'Y' to play again or 'N' to quit", True, pygame.color.THECOLORS['green'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(prompt, prompt_rect)
        pygame.display.flip()

        # Wait for the player's input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        waiting = False
                        g = Game()
                        g.run()
                    elif event.key == pygame.K_n:
                        waiting = False
                        pygame.quit()
                        sys.exit()


if __name__ == '__main__':
    g = Game()
    g.run()
    pygame.quit()
    sys.exit()
