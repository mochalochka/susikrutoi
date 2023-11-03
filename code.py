from pygame import*
font.init()
class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    

    def update(self):
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
            platform_touched = sprite.spritecollide(self, barriers, False)
            if self.x_speed > 0:
                for p in platform_touched:
                    self.rect.right = min (self.rect.right, p.rect.left)
            elif self.x_speed < 0:
                for p in platform_touched:
                    self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y > 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed

            platform_touched = sprite.spritecollide(self, barriers, False)
            if self.y_speed > 0:
                for p in platform_touched:
                    self.rect.bottom = min(self.rect.bottom, p.rect.top)
            elif self.y_speed < 0:
                for p in platform_touched:
                    self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed


    def update(self):
        if self.rect.x <= 420:
            self.side = 'right' 
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= win_width + 10:
            self.kill()
finish = True
win_height = 500
win_width = 700
window = display.set_mode((win_width, win_height))
display.set_caption('supersus')
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
back = (234, 45, 79)
w1 = GameSprite('platform.png', 370, 100, 50, 400)
w2 = GameSprite('platform.png', 100, 150, 100, 20)
packman = Player('heroplayer.png', 5, 5, 80, 80, 0, 0)
bullets = sprite.Group()
monsters = Enemy('monster.png', win_width - 400, 100, 60, 60, 5)
monster = sprite.Group()
monster.add(monsters)
clock = time.Clock()




text = font.Font("Roboto-Black.ttf", 40)
win = text.render('Win', True, (250, 250, 0))
lose = text.render('Lose', True, (250, 250, 0))
fin_jpg = GameSprite('finish.jpg', 650, 450, 50, 50)
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)


run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5   
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
    if finish == True:
        window.blit(background,(0, 0))
     
        packman.reset()

        packman.update()
        barriers.draw(window)
        monster.draw(window)
        monster.update()
        bullets.update()
        bullets.draw(window)

        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monster, True, True)          
 
        fin_jpg.reset()
        if sprite.collide_rect(packman, fin_jpg):
            finish = False
            window.blit(win,(100, 0))
        if sprite.spritecollide(packman, monster, False):
            finish = False
            window.blit(lose,(100, 0)) 
    display.update()

    
    clock.tick(60)