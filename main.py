import pygame
pygame.init()


background_image = pygame.image.load('background.png')  
background_image = pygame.transform.scale(background_image, (800, 500))

class Player:
    def __init__(self, x, y, width, height, image):
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))  # Зміна розміру зображення
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.gravity = 0.5
        self.jump_power = -10
        self.vel_y = 0
        self.can_jump = False
        self.jumps = 2

    def move(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for w in walls:
            if self.rect.colliderect(w.rect):
                self.jumps = 2
                if self.vel_y > 0:
                    self.rect.bottom = w.rect.top
                    self.vel_y = 0
                    self.can_jump = True
                elif self.vel_y < 0:
                    self.rect.top = w.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power
            if self.jumps <= 1:     
                self.can_jump = False
            self.jumps -= 1 

    def move_horizontal(self, dx):
        self.jumps = 2
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect): 
                if dx > 0:
                    self.rect.right = wall.rect.left
                    self.vel_y = 0.1

                elif dx < 0:
                    self.rect.left = wall.rect.right  
                    self.vel_y = 0.1


class Wall:
    def __init__(self, x, y, width, height, color=(22, 26, 31)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

# створення головного вікна
window = pygame.display.set_mode((500, 500))

# створення персонажа
player = Player(100, 100, 50, 50, 'player.png')

# створення стін
walls = [
    Wall(20, 100, 200, 1000),
    Wall(350, 100, 150, 400),
    Wall(100, 450, 500, 400),
]

# кольори
white = (255, 255, 255)

# створення об'єкту "годинник" для встановлення частоти кадрів
clock = pygame.time.Clock()

# головний цикл гри
game = True
move_left = False
move_right = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_w:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_a:
                move_left = False

    window.blit(background_image, (0, 0))
    player.move()

    if move_right:
        player.move_horizontal(3)
    if move_left:
        player.move_horizontal(-3)

    for wall in walls:
        wall.draw(window)

    window.blit(player.image, (player.rect.x, player.rect.y))
   

    clock.tick(60)
    pygame.display.update()

pygame.quit()