import pygame
import os
from pygame.locals import *
from pygame.constants import KEYDOWN
pygame.font.init()

Width = 900
Height = 500
FPS = 60
White = (255,255,255)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
Font = pygame.font.SysFont('comicsans', 30)
Font_Win = pygame.font.SysFont("comicsans", 60)

Ship1 = pygame.image.load(os.path.join("Resources\Space Ship Skins\Skin 2", "Green Spaceship.png"))
Ship2 = pygame.image.load(os.path.join("Resources\Space Ship Skins\Skin 2", "Red Spaceship.png"))
Background = pygame.transform.scale(pygame.image.load(os.path.join("Resources\Backgrounds", "Background_1.jpg")),(Width, Height))
Ship_velocity = 2
Side_divider = pygame.Rect(Width//2 - 1, 0, 2, Height)

window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Space Shooter 1.0")

Ship1_resize = pygame.transform.scale(Ship1, (Width/12, Height/10))
Ship1_rotate = pygame.transform.rotate(Ship1_resize, 270)

Ship2_resize = pygame.transform.scale(Ship2, (Width/12, Height/10))
Ship2_rotate = pygame.transform.rotate(Ship2_resize, 90)

Bullet_velocity = 10
Bullet_count = 5

Ship1_hit = pygame.USEREVENT + 1
Ship2_hit = pygame.USEREVENT + 2

def draw_window_elemet(Ship1_hitbox, Ship2_hitbox, Ship1_bullet, Ship2_bullet, Ship1_health, Ship2_health):

    window.blit(Background, (0,0))
    pygame.draw.rect(window, (0, 0, 0), Side_divider)
    window.blit(Ship1_rotate, (Ship1_hitbox.x, Ship1_hitbox.y))    
    window.blit(Ship2_rotate, (Ship2_hitbox.x, Ship2_hitbox.y))
    Ship1_health_text = Font.render("Health: " + str(Ship1_health), 1, White)
    Ship2_health_text = Font.render("Health: " + str(Ship2_health), 1, White)
    window.blit(Ship1_health_text, (10, 10))
    window.blit(Ship2_health_text, (Width - Ship2_health_text.get_width() - 10,10))

    for bullet in Ship1_bullet:
        pygame.draw.rect(window,Red, bullet)

    for bullet in Ship2_bullet:
        pygame.draw.rect(window,Yellow, bullet)
    
    pygame.display.update()

def Ship1_movement(keys_pressed, Ship1_hitbox):

    if keys_pressed[pygame.K_a] and Ship1_hitbox.x - Ship_velocity > 0:
            Ship1_hitbox.x -= Ship_velocity
    if keys_pressed[pygame.K_d] and Ship1_hitbox.x + Ship1_hitbox.height + Ship_velocity < Side_divider.x:
            Ship1_hitbox.x += Ship_velocity
    if keys_pressed[pygame.K_w] and Ship1_hitbox.y - Ship_velocity >0:
            Ship1_hitbox.y -= Ship_velocity
    if keys_pressed[pygame.K_s] and Ship1_hitbox.y + Ship1_hitbox.width + Ship_velocity + 2 < Height:
            Ship1_hitbox.y += Ship_velocity

def Ship2_movement(keys_pressed, Ship2_hitbox):

    if keys_pressed[pygame.K_KP4] and Ship2_hitbox.x - Ship_velocity > Side_divider.x + Side_divider.width/2:
            Ship2_hitbox.x -= Ship_velocity
    if keys_pressed[pygame.K_KP6] and Ship2_hitbox.x + Ship2_hitbox.height + Ship_velocity < Width:
            Ship2_hitbox.x += Ship_velocity
    if keys_pressed[pygame.K_KP8] and Ship2_hitbox.y - Ship_velocity - 1> 0:
            Ship2_hitbox.y -= Ship_velocity
    if keys_pressed[pygame.K_KP5] and Ship2_hitbox.y + Ship2_hitbox.width + Ship_velocity - 1 < Height:
            Ship2_hitbox.y += Ship_velocity

def handle_bullets(Ship1_bullet, Ship2_bullet, Ship1_hitbox, Ship2_hitbox):

    for bullet in Ship1_bullet:
        bullet.x += Bullet_velocity
        if Ship2_hitbox.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Ship2_hit))
            Ship1_bullet.remove(bullet)
        elif bullet.x > Width:
            Ship1_bullet.remove(bullet)

    for bullet in Ship2_bullet:
        bullet.x -= Bullet_velocity
        if Ship1_hitbox.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Ship1_hit))
            Ship2_bullet.remove(bullet)
        elif bullet.x < 0:
            Ship2_bullet.remove(bullet) 
    
def winner(text):
    draw_text = Font_Win.render(text, 1, White)
    window.blit(draw_text, (Width/2 - draw_text.get_width()/2, Height/2 - draw_text.get_width()/2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():

    Ship1_hitbox = pygame.Rect(Width/5, Height/2 , Width/12, Height/10)
    Ship2_hitbox = pygame.Rect(Width/1.4, Height/2 , Width/12, Height/10)

    Ship1_bullet = []
    Ship2_bullet = []

    Ship1_health = 10
    Ship2_health = 10

    running = True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False 
                
                if event.key == pygame.K_LCTRL and len(Ship1_bullet) < Bullet_count:
                    bullet = pygame.Rect(Ship1_hitbox.x + Ship1_hitbox.width, Ship1_hitbox.y + Ship1_hitbox.height//2, 10, 5)
                    Ship1_bullet.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(Ship2_bullet) < Bullet_count:
                    bullet = pygame.Rect(Ship2_hitbox.x, Ship2_hitbox.y + Ship2_hitbox.height//2, 10, 5)
                    Ship2_bullet.append(bullet)
            
            if event.type == Ship1_hit:
                Ship1_health -= 1
            
            if event.type == Ship2_hit:
                Ship2_health -= 1
        
        Winner = ""

        if Ship1_health <= 0:
            Winner = "Player 2 Wins!"

        if Ship2_health <= 0:
            Winner = "Player 1 Wins!"

        if Winner != "":
            winner(Winner)
            break

        keys_pressed = pygame.key.get_pressed()

        Ship1_movement(keys_pressed, Ship1_hitbox)
        Ship2_movement(keys_pressed, Ship2_hitbox)

        handle_bullets(Ship1_bullet, Ship2_bullet, Ship1_hitbox, Ship2_hitbox)

        draw_window_elemet(Ship1_hitbox, Ship2_hitbox, Ship1_bullet, Ship2_bullet, Ship1_health, Ship2_health)
        
    pygame.quit

if __name__ == "__main__":
    main()