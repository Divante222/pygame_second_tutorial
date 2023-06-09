import pygame
import csv
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World
pygame.init()



screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('dungeon crawler')

#create clock for maintaining frame rate
clock = pygame.time.Clock()

# define game variables
level = 3
screen_scroll = [0,0]


## define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20) # second argument is how big the font will be


# helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))


# load heart images
heart_empty =  scale_img(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_half =  scale_img(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)
heart_full =  scale_img(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)


#load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f'assets/images/items/coin_f{x}.png').convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)


# load potion image
red_potion = scale_img(pygame.image.load('assets/images/items/potion_red.png').convert_alpha(), constants.POTION_SCALE)

item_images = []

item_images.append(coin_images)
item_images.append(red_potion)

#load weapon images
bow_image = scale_img(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.WEAPON_SCALE)




#load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f'assets/images/tiles/{x}.png').convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)



#load character image
mob_animations = []
mob_types = ["elf", 'imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']
animation_types = ['idle', 'run']


for mob in mob_types:
    #load images
    animation_list = []
    for animation in animation_types:
        # reset temporary list of images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)
    

#function for outputting text onto the screen
def draw_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


# function for displaying game info
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0,0, constants.SCREEN_WIDTH, 50) )
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    #draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))


    # level
    draw_text('Level: ' + str(level), font, constants.WHITE, constants.SCREEN_WIDTH /2, 15)

    #show score
    draw_text(f'X{player.score}', font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)


#create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

#load in level data and create world
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter= ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)




world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)


# def draw_grid():
#     for x in range(30):
#         pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
#         pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_WIDTH, x * constants.TILE_SIZE, ))













# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    

    def update(self):
        #reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # move damage text up
        self.rect.y -= 1
        #delete the counter after a few seconds
        self.counter += 1
        if self.counter> 30:
            self.kill()


# ## create player
player = world.player

# create enemy 
# enemy = Character(300, 300, 100, mob_animations, 1)


# create players weapon
bow = Weapon(bow_image, arrow_image)

# extract enemies from world data
enemy_list = world.character_list
# enemy_list.append(enemy)

# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()

# # temporary damage text
# damage_text = DamageText(300, 400, '15', constants.RED)
# damage_text_group.add(damage_text)

item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images,True)
item_group.add(score_coin)
#ad the items from the level data
for item in world.item_list:
    item_group.add(item)






run = True
while run:
    #control framerate 
    clock.tick(constants.FPS)


    screen.fill(constants.BG)

    # draw_grid()
    world.draw(screen)
    #calculate player movement
    dx = 0
    dy = 0  
    
    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED
    
    # move player
    screen_scroll = player.move(dx, dy)


    #creating enemies
    for enemy in enemy_list:
        enemy.ai(screen_scroll)
        enemy.update()
    for enemy in enemy_list:
        enemy.draw(screen)
    
    
    
    
    #update all objects
    world.update(screen_scroll)
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    
    # arrow_group.draw(screen)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage),constants.RED)
            damage_text_group.add(damage_text)



    damage_text_group.update()
    damage_text_group.draw(screen)


    
    item_group.update(screen_scroll , player)
    item_group.draw(screen)


    
    draw_info()
    score_coin.draw(screen)

    #draw player on screen 
    
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
                
            if event.key == pygame.K_d:
                moving_right = True
                
            if event.key == pygame.K_w:
                moving_up = True
               
            if event.key == pygame.K_s:
                moving_down = True

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
                
            if event.key == pygame.K_d:
                moving_right = False
                
            if event.key == pygame.K_w:
                moving_up = False
               
            if event.key == pygame.K_s:
                moving_down = False
   
    

    pygame.display.update()



pygame.quit()