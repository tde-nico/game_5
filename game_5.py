import pygame
import data.engine as e
clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Caption')

fullscreen = False
MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SCREEN_SIZE = (736, 414)
WINDOW_SIZE = SCREEN_SIZE
DISPLAY_SURFACE = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
display = pygame.Surface(DISPLAY_SURFACE)

#pygame.mouse.set_visible(False)

true_scroll = [0,0]
n = 0

background = pygame.image.load('data/images/ground/background_0.png')

all_attributes = e.get_attributes('data/images/entities/')
for entity in all_attributes:
    for skill in range(len(all_attributes[entity])):
        all_attributes[entity][skill]['pos_fix'] = ((all_attributes[entity][skill]['pos_fix_x'],all_attributes[entity][skill]['pos_fix_y']),
                                                    (all_attributes[entity][skill]['pos_fix_x_flipped'],all_attributes[entity][skill]['pos_fix_y']))
        all_attributes[entity][skill]['pos_reset'] = ((all_attributes[entity][skill]['pos_reset_x'],all_attributes[entity][skill]['pos_reset_y']),
                                                    (all_attributes[entity][skill]['pos_reset_x_flipped'],all_attributes[entity][skill]['pos_reset_y']))

e.render_animations('data/images/entities/')
e.new_load_animations('data/images/entities/')
controllers = e.get_controllers()
players = []
swap_colors = [
    [], # blue
    [((26,35,126),(176,18,10)),((59,80,206),(196,20,17)),((78,108,239),(221,25,29)),((3,169,244),(232,78,64))], # red
    [((26,35,126),(13,83,2)),((59,80,206),(5,111,0)),((78,108,239),(10,143,8)),((3,169,244),(43,175,43))], # green
    [((26,35,126),(245,127,23)),((59,80,206),(249,168,37)),((78,108,239),(253,216,53)),((3,169,244),(255,241,118))], # yellow
    [((26,35,126),(74,20,140)),((59,80,206),(123,31,162)),((78,108,239),(156,39,176)),((3,169,244),(186,104,200))], # purple
    [((26,35,126),(194,24,91)),((59,80,206),(233,30,99)),((78,108,239),(236,64,122)),((3,169,244),(240,98,146))], # pink
    [((26,35,126),(191,54,12)),((59,80,206),(216,67,21)),((78,108,239),(244,81,30)),((3,169,244),(255,112,67))], # orange
    [((26,35,126),(62,39,35)),((59,80,206),(78,52,46)),((78,108,239),(109,76,65)),((3,169,244),(141,110,99))], # brown
    [((26,35,126),(37,155,36)),((59,80,206),(43,175,43)),((78,108,239),(66,189,65)),((3,169,244),(114,213,114))], # lime
    [((0,0,0),(196,20,17)),((26,35,126),(0,0,0)),((59,80,206),(0,0,0)),((78,108,239),(38,50,56)),((3,169,244),(38,50,56))], # black
    [((26,35,126),(55,71,79)),((59,80,206),(69,90,100)),((78,108,239),(84,110,122)),((3,169,244),(120,144,156))], # grey
    [((26,35,126),(189,189,189)),((59,80,206),(224,224,224)),((78,108,239),(238,238,238)),((3,169,244),(255,255,254))], # white
    [((26,35,126),(0,172,193)),((59,80,206),(0,188,212)),((78,108,239),(38,198,218)),((3,169,244),(128,222,234))], # cyan
    [((26,35,126),(130,119,23)),((59,80,206),(158,157,36)),((78,108,239),(175,180,43)),((3,169,244),(192,202,51))], # gold
    [((26,35,126),()),((59,80,206),()),((78,108,239),()),((3,169,244),())],
    ]



def start():
    players=[]
    sample = {
            #'entity': e.entity(20,20,8,8,'slime',sub_entities=[e.entity(0,0,55,66,'demon')]),
            'speed': 2,
            'moving_right': False,
            'moving_left': False,
            'moving_down': False,
            'vertical_momentum': 0,
            'air_timer': 0,
            #'kinetic_energy': [0,0],

            'cooldowns': {'dash': 0},

            'attacks': all_attributes['slime'],           
            #'attacks': [{'id':False,'tag':'axe_smash','pos_fix':((-16,-19),(-20,-19)),'pos_reset':((16,19),(20,19))},
            #            {'id':False,'tag':'cutter','pos_fix':((-17,-23),(-28,-23)),'pos_reset':((20,8),(25,8))}],
            'action_end': True,

            'trasformation': False,
            'sub_entity': 0,
            'sub_entity_specs': [{'trasformation_fix':((-33,-80),(-32,-80)),'end_trasformation_fix':((5,22),(13,22))},
                                 {'trasformation_fix':((-22,-62),(-22,-62)),'end_trasformation_fix':((5,22),(13,22))}],
            
            'counter_attack': 0,
            'hit': False,
            'life': 100,
            'death': False,
            'dead': False,
            }
    for player in range(len(controllers)):
        new_sample = sample.copy()
        new_sample['entity'] = e.entity(20,20,8,8,'slime',sub_entities=[e.entity(0,0,55,66,'demon')])
        new_sample['entity'].set_pos(270-240//(player+1),new_sample['entity'].y)
        new_sample['entity'].swap_colors = swap_colors[player]
        new_sample['kinetic_energy'] = [0,0]
        new_sample['controller'] = controllers[player]
        players.append(new_sample)
    if controllers == []:
        for player in range(2):
            new_sample = sample.copy()
            new_sample['entity'] = e.entity(20,20,8,8,'slime',sub_entities=[e.entity(0,0,55,66,'demon'), e.entity(0,0,30,50,'astral')])
            new_sample['entity'].set_pos(270-240//(player+1),new_sample['entity'].y)
            new_sample['entity'].swap_colors = swap_colors[player]
            new_sample['kinetic_energy'] = [0,0]
            players.append(new_sample)
    return players
        



players = start()
grass_image = pygame.image.load('data/images/ground/grass.png')
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load('data/images/ground/dirt.png')

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2'],
            ['0','0','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','1'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','1','1'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','1','1','1'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','1','1','1','1'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1','1','1','1','1'],]


def standard_events(event):
    global screen, fullscreen, WINDOW_SIZE, MONITOR_SIZE, SCREEN_SIZE
    if event.type == QUIT: # quit
        e.qt()
    if event.type == VIDEORESIZE and not fullscreen: # video resizing
        WINDOW_SIZE, screen = e.videoresize(event)
    if event.type == KEYDOWN:
        if event.key == K_DELETE: # quit
            e.qt()
        if event.key == K_F11: # fullscreen
            fullscreen = not fullscreen
            if fullscreen:
                WINDOW_SIZE, screen = e.set_fullscreen(MONITOR_SIZE)
            else:
                WINDOW_SIZE, screen = e.toggle_fullscreen(SCREEN_SIZE)




def ground_generation():
    tile_rects = []
    t = TILE_SIZE
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image,(x*t,y*t))
            elif tile == '2':
                display.blit(grass_image,(x*t,y*t))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*t,y*t,t,t))
            x += 1
        y += 1
    return tile_rects




def player_main():
    players_list = players.copy()
    while players_list:
        player = players_list.pop(0)

        for cooldown in player['cooldowns']:
            if player['cooldowns'][cooldown]:
                player['cooldowns'][cooldown] -= 1
        
        player_movement = [0,0]
        if player['moving_right']:
            player_movement[0] += player['speed']
        if player['moving_left']:
            player_movement[0] -= player['speed']
        player_movement[1] += player['vertical_momentum']
        player['vertical_momentum'] += 0.2
        if player['vertical_momentum'] > 3:
            player['vertical_momentum'] = 3
        if player['moving_down']:
            if player['vertical_momentum'] != 0.2:
                player['vertical_momentum'] = abs(player['vertical_momentum'])*2
            else:
                player['entity'].set_action('shifted')


        if player['trasformation']:
            player['action_end'] = False
            if not player['action_end'] and player['entity'].is_last_frame():
                player['trasformation'] = False
                player['action_end'] = True
                player['entity'] = player['entity'].swap_entity(player['sub_entity'], player['sub_entity_specs'][player['sub_entity']]['end_trasformation_fix'])
                player['attacks'] = all_attributes[player['entity'].type]
                player['entity'].set_action('idle')
                
        else:
            for attack in range(len(player['attacks'])):
                if player['attacks'][attack]['id'] and player['action_end']:
                    player['entity'].animation_shift(player['attacks'][attack]['tag'], player['attacks'][attack]['pos_fix'])
                    player['attacks'][attack]['id'] = False
                    player['action_end'] = False
                    break
            if player['action_end']:
                if player_movement[0] == 0 and player['entity'].action != 'shifted':
                    player['entity'].set_action('idle')
                if player_movement[0] > 0:
                    player['entity'].set_flip(False)
                    player['entity'].set_action('run')
                if player_movement[0] < 0:
                    player['entity'].set_flip(True)
                    player['entity'].set_action('run')

                if player['kinetic_energy'][0] >= .1 or player['kinetic_energy'][0] <= -.1:
                    player_movement[0] += player['kinetic_energy'][0]
                    if player['kinetic_energy'][0] > 0:
                        player['kinetic_energy'][0] -= .1
                    else:
                        player['kinetic_energy'][0] += .1
                if player['kinetic_energy'][1] >= .1 or player['kinetic_energy'][1] <= -.1:
                    player_movement[1] += player['kinetic_energy'][1]
                    if player['kinetic_energy'][1] > 0:
                        player['kinetic_energy'][1] -= .1
                    else:
                        player['kinetic_energy'][1] += .1

                collision_types = player['entity'].move(player_movement,tile_rects)

                if collision_types['left'] or collision_types['right']:
                    player['kinetic_energy'][0] *= -1
                if collision_types['top']:
                    player['kinetic_energy'][1] *= -1
                if collision_types['bottom']:
                    player['kinetic_energy'][1] *= -1
                    player['air_timer'] = 0
                    player['vertical_momentum'] = 0
                else:
                    player['air_timer'] += 1
                
                if player['vertical_momentum'] < -1 or player['vertical_momentum'] > 1:
                    player['entity'].set_action('jump')

            if player['death'] and player['entity'].is_last_frame():
                player['dead'] = True
                continue
            if not player['action_end']:
                player['counter_attack'] += 1
            else:
                player['counter_attack'] = 0

            if not player['action_end'] and player['entity'].is_last_frame():
                for attack in range(len(player['attacks'])):
                    if player['attacks'][attack]['tag'] == player['entity'].action:
                        player['entity'].animation_shift('idle', player['attacks'][attack]['pos_reset'])
                        break
                player['action_end'] = True

        player['entity'].change_frame(1)
        player['entity'].display(display, [0,0])




def player_collision_check():
    players_list = players.copy()
    while players_list:
        player_1 = players_list.pop(0)
        current_player_2 = 0
        while current_player_2 < len(players_list):
            player_2 = players_list[current_player_2]
            current_player_2 += 1
            if player_2['hit'] and player_1['action_end']:
                player_2['hit'] = False
                continue
            if player_1['hit'] or player_2['hit']:
                continue
            p1 = player_1['entity']
            p2 = player_2['entity']
            collision = e.mask_collision(p1.get_current_img(),p2.get_current_img(),(p1.x,p1.y),(p2.x,p2.y))
            if collision and not player_1['action_end'] and not player_2['action_end']:
                if player_1['counter_attack'] > player_2['counter_attack']:
                    player_2['hit'] = True
                    player_2['life'] -= 30
                elif player_1['counter_attack'] < player_2['counter_attack']:
                    player_1['hit'] = True
                    player_1['life'] -= 30
                else:
                    print('TIE')
            elif collision and not player_1['action_end'] and not player_2['death']:
                player_2['hit'] = True
                player_2['life'] -= 30
                player_2['kinetic_energy'][0] += (player_2['entity'].width/2-collision[0])*1.5
                player_2['kinetic_energy'][1] += (player_2['entity'].height/2-collision[1])*1.5




def death_check():
    players_list = players.copy()
    while players_list:
        player = players_list.pop(0)
        if player['life'] <= 0:
            for attack in range(len(player['attacks'])):
                if player['attacks'][attack]['id']:
                    player['entity'].animation_shift('death', player['attacks'][attack]['pos_reset'])
                    break
            player['entity'].animation_shift('death', ((-4,-8),(-4,-8)))
            player['action_end'] = False
            player['death'] = True
            player['life'] = 1





def controller_events():
    for controller in range(len(players)):
        axes, buttons = e.get_controller_events(players[controller]['controller'])
        dead_zone = .5
        if axes[0] <= -dead_zone or buttons[13]: players[controller]['moving_left'] = True
        else: players[controller]['moving_left'] = False
        if axes[0] >= dead_zone or buttons[14]: players[controller]['moving_right'] = True
        else: players[controller]['moving_right'] = False
        if (axes[1]<=-dead_zone or buttons[11] or buttons[0]) and players[controller]['air_timer']<6: players[controller]['vertical_momentum']=-5
        if axes[1] >= dead_zone or buttons[12]: players[controller]['moving_down'] = True
        else: players[controller]['moving_down'] = False
        if buttons[3] and players[controller]['action_end']:
            players[controller]['attacks']['heavy'] = True





def events(players):
    for event in pygame.event.get():
        standard_events(event)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                e.qt()
            if event.key == K_d:
                players[0]['moving_right'] = True
            if event.key == K_a:
                players[0]['moving_left'] = True
            if event.key == K_w:
                if players[0]['air_timer'] < 6:
                    players[0]['vertical_momentum'] = -5
            if event.key == K_s:
                players[0]['moving_down'] = True
                if players[0]['air_timer'] > 6:
                    players[0]['kinetic_energy'][1] += 5
            if event.key == K_l and players[0]['action_end']:
                players[0]['attacks'][0]['id'] = True
            if event.key == K_k and players[0]['action_end']:
                players[0]['attacks'][1]['id'] = True
            if event.key == K_m:
                if not players[0]['cooldowns']['dash']:
                    players[0]['cooldowns']['dash'] = 60 * 2
                    if players[0]['moving_right']:
                        players[0]['kinetic_energy'][0] += players[0]['speed']*2
                    if players[0]['moving_left']:
                        players[0]['kinetic_energy'][0] -= players[0]['speed']*2
                    if players[0]['moving_down']:
                        players[0]['kinetic_energy'][1] += players[0]['speed']*2
                    else:
                        players[0]['kinetic_energy'][1] -= players[0]['speed']*2
            if event.key == K_t:
                players[0]['entity'].animation_shift('trasformation_'+players[0]['entity'].sub_entities[players[0]['sub_entity']].type,
                                                     players[0]['sub_entity_specs'][players[0]['sub_entity']]['trasformation_fix'])
                players[0]['trasformation'] = True
                players[0]['sub_entity'] = 0
            if event.key == K_c:
                players[0]['sub_entity'] = 0
            if event.key == K_v:
                players[0]['sub_entity'] = 1
            if event.key == K_p:
                players[0]['entity'].swap_colors = swap_colors[swap_colors.index(players[0]['entity'].swap_colors)+1]
            if event.key == K_o:
                players[0]['entity'].swap_colors = swap_colors[swap_colors.index(players[0]['entity'].swap_colors)-1]
            if event.key == K_n:
                players = start()
        if event.type == KEYUP:
            if event.key == K_d:
                players[0]['moving_right'] = False
            if event.key == K_a:
                players[0]['moving_left'] = False
            if event.key == K_s:
                players[0]['moving_down'] = False
    return players






while 1:
    display.blit(background, (0,0))

    clicks, mouse = e.mouse_events(display)

    tile_rects = ground_generation()

    player_main()

    players_list = players.copy()
    while players_list:
        player = players_list.pop(0)
        if player['dead'] or player['entity'].y > DISPLAY_SURFACE[1]+10:
            players.remove(player)

    player_collision_check()    
            
    death_check()
        
    if controllers:
        controller_events()
    
    players = events(players)

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)





    
