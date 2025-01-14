from pygame import *
'''Clases requeridas'''

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.side = "derecha"
        if self.rect.x >= win_width - 85:
            self.side = "izquierda"
        if self.side == "izquierda":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x 
        self.rect.y = wall_y
        
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

background = transform.scale(image.load("background.jpg"), (win_width, win_height))

player = Player('hero.png', 5, win_width - 80, 4)

monster = Enemy('cyborg.png', win_width - 80, 280, 2)

final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 20, 450, 10)
w3 = Wall(154, 205, 50, 100, 20, 450, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()

font = font.Font(None, 70)
win = font.render('¡GANASTE!', True, (255, 215, 0))
lose = font.render('¡PERDISTE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
Kick = mixer.Sound('Kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()
            
        player.reset()
        monster.reset()
        final.reset()
            
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
            
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2)or sprite.collide_rect(player, w3):
            finish = True
            window.blit(lose, (200, 200))
            Kick.play()
                
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()
                
    display.update()
    clock.tick(FPS)