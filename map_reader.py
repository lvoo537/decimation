import pygame


def process_map_data(image_list, map_data1, tile_size):
    obstacles_list = []
    for i, row in enumerate(map_data1):
        for j, col in enumerate(row):
            # skipping all the -1's in the map data
            if col >= 0:
                image = image_list[col]
                image_rect = image.get_rect()
                image_rect.x = j * tile_size
                image_rect.y = i * tile_size
                if (col>=5 and col <=10) or(col == 16) or (col == 20) or (col>=23 and col <=26) or (col>=23 and col <=26)or (col==32)or (col>=35 and col <=37)or (col==39) or (col>=48 and col <=49) or (col == 52) or (col>=54 and col <=57)or (col>=65 and col <=66) or (col == 68) or (col>=70 and col <=71) or (col>=80 and col <=95) or (col>=97 and col <=103) or (col == 106) or (col>=129 and col <=131) or col ==133 or(col == 122) or col == 124 or col ==126 or (col==141) or (col ==143):
                    tup = (image,image_rect)
                    obstacles_list.append(tup)
    return obstacles_list



def draw(obstacle_list: list,screen):
    for element in obstacle_list:
        screen.blit(element[0],element[1])
