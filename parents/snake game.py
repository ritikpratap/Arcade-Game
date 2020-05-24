import pygame , sys, random, time

from os import path
img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')

#window size
width = 500
height = 425

#frames per second
fps = 50
clock = pygame.time.Clock()

#initialize pygame and mixer to add sounds
pygame.init()
pygame.mixer.init()
pygame.font.init()

#colours
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

#========================================PLAYERS================================
def newenemy():
     m = enemy()
     foe.add(m)
     group.add(m)
     
font = pygame.font.SysFont('comicsansms',20)

def display_points(surf, score):
    text = font.render('score: '+ str(score), True, white)
    surf.blit(text,[0,0])
    
class snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (40,40))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 17
        #pygame.draw.circle(self.image, blue, self.rect.center, self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = height-60
        self.speedx = 0
        self.shield = 3
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8    
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx

        if self.rect.right > width:
            self.rect.x = width-self.rect.width
        if self.rect.left < 0:
            self.rect.x = 0
        
    def shoot(self):
         time.sleep = 0.25
         bullet = Bullet(self.rect.centerx, self.rect.top)
         group.add(bullet)
         bullets.add(bullet)
         shoot_sound.play()

#=================================BIRDS=========================================

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(foe_img, (50,40))
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .65/ 2)
        #pygame.draw.circle(self.image, blue, self.rect.center, self.radius)
        self.rect.x = random.randrange(width - self.rect.width)
        self.speedy = random.randrange(1,5)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,9)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now -self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed)%360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height or self.rect.right < 0 or self.rect.left > width:
            self.rect.x = random.randrange(width-self.rect.width)
            self.rect.y = -10
            self.speedy = random.randrange(1,5)

#==================================BULLETS===================================
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (15,20))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        self.rect.y += self.speedy

#to display screen and give it a name
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('arcade game')

#=========================GRAPHICS========================================

background = pygame.image.load(path.join(img_dir, 'Starbasesnow.png')).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir,'plane.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir,'laser.png')).convert()
foe_img = pygame.image.load(path.join(img_dir,'bird.png')).convert()

#=========================SOUNDS=======================================
shoot_sound = pygame.mixer.Sound(path.join(sound_dir,'Laser_Shoot.wav'))
expl_sound = pygame.mixer.Sound(path.join(sound_dir,'Explosion4.wav'))
pygame.mixer.music.load(path.join(sound_dir, 'spaceship.wav'))
pygame.mixer.music.set_volume(1)

#this will create a new group of sprites or moving object
group = pygame.sprite.Group()
foe = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = snake()
group.add(player)
for i in range(10):
    newenemy()

score = 0
prcntg = 100
pygame.mixer.music.play(loops=-1)

#=========================loop in which game is running======================
playing = True
while playing:
    #to check if the game is running at right speed
    clock.tick(fps)
    #inputs or events given from outside
    for event in pygame.event.get():
        #closing the window
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                 playing = False
            if event.key == pygame.K_SPACE:
                 player.shoot()
                 
 #============================update section==============================
    group.update()
    
    #to check collision
    hits = pygame.sprite.groupcollide(foe, bullets, True, True)
    for hit in hits:
        score += 10
        expl_sound.play()
        newenemy()
    hits = pygame.sprite.spritecollide(player, foe, True, pygame.sprite.collide_circle)
    for hit in hits:
         player.shield -= 1
         if player.shield <= 0:
              playing = False
        
    #drawing anything
    screen.fill(black)
    screen.blit(background, background_rect)
    #this will draw all sprites on the screen
    group.draw(screen)
    display_points(screen, score)
    pygame.display.update()
pygame.quit()
