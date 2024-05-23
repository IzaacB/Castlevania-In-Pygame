from settings import *
    
test_tiles = {
    0   :   pygame.image.load('Tiles/Tile1.png'),
    1   :   pygame.image.load('Tiles/Tile2.png'),
    2   :   pygame.image.load('Tiles/Tile3.png'),
    3   :   pygame.image.load('Tiles/Tile4.png'),
    4   :   pygame.image.load('Tiles/Tile5.png'),
    5   :   pygame.image.load('Tiles/Tile6.png'),
    6   :   pygame.image.load('Tiles/Tile7.png'),

    7   :   pygame.image.load('Tiles/Tile8.png'),#PLATFORM
    8   :   pygame.image.load('Tiles/Tile8.png'),#WALL

    9   :   pygame.image.load('Tiles/Tile9.png'),
    "WALL": [8],
    "PLAT": [1, 6, 7, 0]
}