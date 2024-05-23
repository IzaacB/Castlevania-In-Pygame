from settings import *

class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def render(self, tiles):
        self.final_render = []

        for i in range(0, len(tiles)):
            if tiles[i][0] >= self.x - 16 and tiles[i][0] + 16 <= self.x + 16 + window_width:
                if tiles[i][1] >= self.y - 16 and tiles[i][1] + 16 <= self.y + 16 + window_height:#Check if x and y values for each tile are within the camera rect.
                    self.final_render.append([tiles[i][0] - self.x, tiles[i][1] - self.y, tiles[i][2]])#Offset each tile based on distance from the camera, and render at origin.
                    
        return self.final_render
    
class Tilemap():
    def __init__(self, map_data, tile_data, origin_x, origin_y): #This will be used for each room, so the origin coordinates make it easier when placing.
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.map_data = map_data
        self.tile_data = tile_data#Initialize class variables to self.
        
    def render(self):#Interpret the tiles into an array of elements that consist of [x, y, sprite].
        self.walls = []
        self.platforms = []
        self.decor = []
        for y in range(0, len(self.map_data)):
            for x in range(0, len(self.map_data[y])):
                if self.map_data[y][x] in self.tile_data["WALL"]:
                    self.walls.append([x * 16 + self.origin_x, y * 16 + self.origin_y, self.tile_data[self.map_data[y][x]]])

                elif self.map_data[y][x] in self.tile_data["PLAT"]:
                    self.platforms.append([x * 16 + self.origin_x, y * 16 + self.origin_y, self.tile_data[self.map_data[y][x]]])
                else:
                    self.decor.append([x * 16 + self.origin_x, y * 16 + self.origin_y, self.tile_data[self.map_data[y][x]]])
                
        return self.walls, self.platforms, self.decor
    
class Anim():
    def __init__(self, sprite_data):
        self.sprite_data = sprite_data #Initialize sprite data to anim.
        self.last_anim = 0
        self.current_anim = 0
        self.current_frame = 0
        
    def play(self, anim_data, anim_speed, delta_time):
        try:
            self.current_anim = anim_data#Record current animation.
            
            if self.current_anim == self.last_anim:#Check if the animation is still playing.
                if self.current_frame + anim_speed * delta_time <= len(self.current_anim):
                    self.current_frame += anim_speed * delta_time#Play animation.
                
                else:
                    self.current_frame = 0#Loop animation
                    
            else:#If it switched to a different animation, reset the loop.
                self.current_frame = 0
                
            self.last_anim = self.current_anim#Record the last animation played.
            
            return(self.sprite_data[self.current_anim[int(np.floor(self.current_frame))]])
        except:
            return(self.sprite_data[0])