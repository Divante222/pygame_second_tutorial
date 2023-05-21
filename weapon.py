import pygame
import math


class Weapon():
    def __init__(self, image, arrow_image):
        self.origional_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.origional_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = 300
        arrow = None
        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery) # pygame y coordinates increase down the screen

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        #get mouse clicks
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        #reset mouse click
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.origional_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/ 2)), (self.rect.centery - int(self.image.get_height() / 2))))    
    



class Arrow(pygame.sprite.Sprite):
    def __init__(self,image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.origional_image = image
        self.angle = angle
        self.angle
        self.image = pygame.transform.rotate(self.origional_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/ 2)), (self.rect.centery - int(self.image.get_height() / 2))))
        

