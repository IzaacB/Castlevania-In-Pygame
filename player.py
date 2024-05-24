from settings import *
from sprite_data import *
from objects import *

class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.accel_x = 0
        self.accel_y = 0

        self.idle_speed = 60
        self.jump_speed = 30
        self.crouch_speed = 30

        self.jump_force = 200
        self.gravity = 10

        #Define hitboxes:
        self.head = [8, 0]
        self.torso = [8, 16]
        self.legs = [8, 32]

        self.state = "IDLE"
        self.dir = "RIGHT"
        self.grounded = True
        self.can_stand = True

        self.anim_speed = 8
        self.anim_state = self.state
        self.sprites = simon_sprites
        self.animations = simon_anim
        self.anim = Anim(self.sprites)

    def update_collision(self):
        self.legs = [8 + self.x, 32 + self.y]
        self.torso = [8 + self.x, 16 + self.y]
        self.head = [8 + self.x, self.y]

    def update(self, walls, platforms, keys, delta_time):
        if self.state == "IDLE":
            self.handle_idle_state(keys)
        if self.state == "JUMPING":
            self.handle_jumping_state(keys)
        if self.state == "CROUCHING":
            self.handle_crouching_state(keys)

        self.move_and_collide(walls, platforms, delta_time)

        return [self.x, self.y, self.anim.play(self.animations[self.anim_state + self.dir], self.anim_speed, delta_time)]

    def move_and_collide(self, walls, platforms, delta_time):
        self.x += self.accel_x * delta_time
        self.y -= self.accel_y * delta_time

        self.grounded = False
        self.can_stand = True
        for plat in platforms:
            self.col_t, self.col_b, self.col_l, self.col_r = plat[1], plat[1] + 16, plat[0], plat[0] + 16
            self.hit_t, self.hit_b, self.hit_l, self.hit_r = self.legs[1], self.legs[1] + 16, self.legs[0], self.legs[0] + 16

            if abs(self.hit_t - self.col_t) > abs(self.hit_l - self.col_l):
                if self.hit_t <= self.col_b and self.hit_b >= self.col_t:
                    if self.hit_t - self.col_t <= 0:
                        self.y = self.col_t - 16 - (self.hit_t - self.y)
                        self.grounded = True
                self.update_collision()

        for wall in walls:
            #Leg wall collision:
            self.col_t, self.col_b, self.col_l, self.col_r = wall[1], wall[1] + 16, wall[0], wall[0] + 16
            self.hit_t, self.hit_b, self.hit_l, self.hit_r = self.legs[1], self.legs[1] + 16, self.legs[0], self.legs[0] + 16

            if abs(self.hit_t - self.col_t) >= abs(self.hit_l - self.col_l):
                if self.hit_t <= self.col_b and self.hit_b >= self.col_t:
                    if self.hit_t - self.col_t <= 0:
                        self.y = self.col_t - 16 - (self.hit_t - self.y)
                        self.grounded = True
                self.update_collision()
            else:
                if self.hit_l <= self.col_r and self.hit_r >= self.col_l:
                    if self.hit_l - self.col_l <= 0:
                        self.x = self.col_l - 16 - (self.hit_l - self.x)
                    else:
                        self.x = self.col_r - (self.hit_l - self.x)
                self.update_collision()

            #Torso wall collision:
            self.hit_t, self.hit_b, self.hit_l, self.hit_r = self.torso[1], self.torso[1] + 16, self.torso[0], self.torso[0] + 16

            if abs(self.hit_t - self.col_t) <= abs(self.hit_l - self.col_l):
                if self.hit_l <= self.col_r and self.hit_r >= self.col_l:
                    if self.hit_l - self.col_l <= 0:
                        self.x = self.col_l - 16 - (self.hit_l - self.x)
                    else:
                        self.x = self.col_r - (self.hit_l - self.x)
                self.update_collision()

            #Head wall collision:
            if not self.state == "CROUCHING":
                self.hit_t, self.hit_b, self.hit_l, self.hit_r = self.head[1] - 1, self.head[1] + 16, self.head[0], self.head[0] + 16

                if abs(self.hit_t - self.col_t) >= abs(self.hit_l - self.col_l):
                    if self.hit_t <= self.col_b and self.hit_b >= self.col_t:
                        if self.hit_t - self.col_t >= 0:
                            self.y = self.col_b - (self.hit_t - self.y)
                            self.accel_y = 0
                    self.update_collision()
                else:
                    if self.hit_l <= self.col_r and self.hit_r >= self.col_l:
                        if self.hit_l - self.col_l <= 0:
                            self.x = self.col_l - 16 - (self.hit_l - self.x)
                        else:
                            self.x = self.col_r - (self.hit_l - self.x)
                    self.update_collision()

            else:
                if abs(self.hit_t - self.col_t) >= abs(self.hit_l - self.col_l):
                    if self.hit_t <= self.col_b and self.hit_b >= self.col_t:
                        self.can_stand = False
                else:
                    if self.hit_l <= self.col_r and self.hit_r >= self.col_l:
                        self.can_stand = False
     
    def handle_idle_state(self, keys):
        self.accel_y = 0
        self.anim_speed = 8

        if keys[pygame.K_d]:
            self.accel_x = self.idle_speed
            self.anim_state = "WALKING"
            self.dir = "RIGHT"
        elif keys[pygame.K_a]:
            self.accel_x = - self.idle_speed
            self.anim_state = "WALKING"
            self.dir = "LEFT"
        else:
            self.accel_x = 0
            self.anim_state = self.state

        if keys[pygame.K_DOWN]:
            self.accel_y = self.jump_force

        if not self.grounded:
            self.state = "JUMPING"

        elif keys[pygame.K_s]:
            self.state = "CROUCHING"

    def handle_jumping_state(self, keys):
        self.accel_x = 0
        self.anim_speed = 8
        self.anim_state = self.state
        self.accel_y -= self.gravity

        if keys[pygame.K_d]:
            self.accel_x = self.idle_speed
            self.dir = "RIGHT"
        elif keys[pygame.K_a]:
            self.accel_x = -self.idle_speed
            self.dir = "LEFT"
        
        if self.grounded:
            self.state = "IDLE"

    def handle_crouching_state(self, keys):
        self.anim_speed = 4
        self.accel_y = 0
        if keys[pygame.K_d]:
            self.accel_x = self.crouch_speed
            self.anim_state = "CROUCHWALKING"
            self.dir = "RIGHT"

        elif keys[pygame.K_a]:
            self.accel_x = - self.crouch_speed
            self.anim_state = "CROUCHWALKING"
            self.dir = "LEFT"

        else:
            self.accel_x = 0
            self.anim_state = self.state

        if not self.grounded:
            self.state = "JUMPING"

        if not keys[pygame.K_s] and self.can_stand:
            self.state = "IDLE"