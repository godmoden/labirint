from pygame import *
window = display.set_mode((600,500))
picture = image.load('fon_pacmena.jpg')
display.set_caption('Рекардо милос унижает хейтера на глазах!')
run = True
win_width = 600
win_height = 500

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
    
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # идем вверх
            for p in platforms_touched:
                self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали


    def fire(self):
        bullet = Bullet('dizlike.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__( picture, w, h, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 420:
            self.direction = 'right'
        if self.rect.x >= 600 - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
w1 = GameSprite('stena.jpg', 80, 400, 300, 100)
w2 = GameSprite('stena.jpg', 200, 80, 100, 250)

packman = Player('Recardomilos.png', 80, 80, 0, 400, 5, 5)
final = GameSprite('youprool.png', 80, 80, 520, 420)

barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
platforms_touched = sprite.spritecollide(packman, barriers, False)

monster = Enemy('monster.png', 80, 80, 420, 80, 4)
monsters = sprite.Group()
monsters.add(monster)

bullets = sprite.Group()

finish = False

class Bullet(sprite.Sprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(self, picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 600+10:
            self.kill()

while run:
    time.delay (50)
    window.blit(picture,(0,0))
    packman.reset()
    final.reset()
    sprite.groupcollide(bullets, barriers, True, False)

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
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if finish != True:
        window.blit(picture, (0,0))
        packman.update()
        bullets.update()
        packman.reset()
        final.reset()
        barriers.draw(window)
        bullets.draw(window)
        
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)

        if sprite.collide_rect(packman, final):
            finish = True
            img = image.load('win_1.jpg')
            window.fill((255,255,255))
            window.blit(transform.scale(img,(win_width, win_height)),(0,0))

        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('geme_over.jpg')
            window.fill((255,255,255))
            window.blit(transform.scale(img,(win_width, win_height)),(0,0))

    display.update()