import pygame, math, os, sys
from pygame.locals import *

global e_colorkey
e_colorkey = (255,255,255)


def set_global_colorkey(colorkey):
    global e_colorkey
    e_colorkey = colorkey





# quit
def qt():
    pygame.quit()
    sys.exit()





# screen sizing
def videoresize(event):
    window_size = (event.w, event.h)
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    return window_size, screen


def set_fullscreen(monitor_size):
    screen = pygame.display.set_mode(monitor_size, pygame.SCALED + pygame.FULLSCREEN)
    return monitor_size, screen


def toggle_fullscreen(screen_size):
    pygame.display.toggle_fullscreen()
    screen = pygame.display.set_mode(screen_size, pygame.SCALED + pygame.RESIZABLE)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
    return screen_size, screen





# mouse
mouse = 0
def mouse_events(surf):
    global mouse
    mx, my = pygame.mouse.get_pos()
    istant_window_size = pygame.display.get_window_size()
    clicks = pygame.mouse.get_pressed()
    if mouse:
        mouse.x, mouse.y = mx/istant_window_size[0]*surf.get_width(), my/istant_window_size[1]*surf.get_height()
    else:
        mouse = pygame.Rect(mx/istant_window_size[0]*surf.get_width(), my/istant_window_size[1]*surf.get_height(), 1, 1)
    return clicks, mouse




# load image
def load_img(path, colorkey=(255,255,255)):
    img = pygame.image.load('data/images/' + path).convert()
    img.set_colorkey(colorkey)
    return img





# 2d collisions test
def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list


def precise_collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        collision = surface_mask_collision(object_1,obj)
        if collision:
            collision_list.append((obj, collision))
    return collision_list



# 2d physics object
class physics_obj(object):
   
    def __init__(self,x,y,width,height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.x = x
        self.y = y

    def move(self,movement,platforms,ramps=[]):
        self.x += movement[0]
        self.rect.x = int(self.x)
        block_hit_list = collision_test(self.rect,platforms)
        collision_types = {'top':False,'bottom':False,'right':False,'left':False,'slant_bottom':False,'data':[]}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
                markers[0] = True
            elif movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([block,markers])
            self.x = self.rect.x
        self.y += movement[1]
        self.rect.y = int(self.y)
        block_hit_list = collision_test(self.rect,platforms)
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([block,markers])
            self.change_y = 0
            self.y = self.rect.y
        return collision_types





# entity stuff
def simple_entity(x,y,e_type):
    return entity(x,y,1,1,e_type)


def flip(img,boolean=True):
    return pygame.transform.flip(img,boolean,False)


def blit_center(surf,surf2,pos):
    x = int(surf2.get_width()/2)
    y = int(surf2.get_height()/2)
    surf.blit(surf2,(pos[0]-x,pos[1]-y))
 
class entity(object):
    global animation_database, animation_higher_database
   
    def __init__(self,x,y,width,height,e_type,swap_colors=[],sub_entities=[]): # x, y, size_x, size_y, type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.obj = physics_obj(x,y,width,height)
        self.animation = None
        self.image = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.offset = [0,0]
        self.rotation = 0
        self.type = e_type # used to determine animation set among other things
        self.action_timer = 0
        self.action = ''
        self.set_action('idle') # overall action for the entity
        self.entity_data = {}
        self.alpha = None
        self.swap_colors = swap_colors
        self.sub_entities = sub_entities
 
    def set_pos(self,x,y):
        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y
        self.obj.rect.x = x
        self.obj.rect.y = y
 
    def move(self,momentum,platforms,ramps=[]):
        collisions = self.obj.move(momentum,platforms,ramps)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions
 
    def rect(self):
        return pygame.Rect(self.x,self.y,self.size_x,self.size_y)
 
    def set_flip(self,boolean):
        self.flip = boolean
 
    def set_animation_tags(self,tags):
        self.animation_tags = tags
 
    def set_animation(self,sequence):
        self.animation = sequence
        self.animation_frame = 0
 
    def set_action(self,action_id,force=False):
        if (self.action == action_id) and (force == False):
            pass
        else:
            self.action = action_id
            anim = animation_higher_database[self.type][action_id]
            self.animation = anim[0]
            self.set_animation_tags(anim[1])
            self.animation_frame = 0

    def get_entity_angle(entity_2):
        x1 = self.x+int(self.width/2)
        y1 = self.y+int(self.height/2)
        x2 = entity_2.x+int(entity_2.width/2)
        y2 = entity_2.y+int(entity_2.height/2)
        angle = math.atan((y2-y1)/(x2-x1))
        if x2 < x1:
            angle += math.pi
        return angle

    def get_center(self):
        x = self.x+int(self.width/2)
        y = self.y+int(self.height/2)
        return [x,y]
 
    def clear_animation(self):
        self.animation = None
 
    def set_image(self,image):
        self.image = image
 
    def set_offset(self,offset):
        self.offset = offset
 
    def set_frame(self,amount):
        self.animation_frame = amount
 
    def handle(self):
        self.action_timer += 1
        self.change_frame(1)
 
    def change_frame(self,amount):
        self.animation_frame += amount
        if self.animation != None:
            while self.animation_frame < 0:
                if 'loop' in self.animation_tags:
                    self.animation_frame += len(self.animation)
                else:
                    self.animation = 0
            while self.animation_frame >= len(self.animation):
                if 'loop' in self.animation_tags:
                    self.animation_frame -= len(self.animation)
                else:
                    self.animation_frame = len(self.animation)-1
 
    def get_current_img(self):
        if self.animation == None:
            if self.image != None:
                return flip(self.image,self.flip)
            else:
                return None
        else:
            return flip(animation_database[self.animation[self.animation_frame]],self.flip)

    def is_last_frame(self):
        return animation_database[self.animation[self.animation_frame]] is animation_database[self.animation[-1]]

    def get_drawn_img(self):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            return image_to_render, center_x, center_y
 
    def display(self,surface,scroll):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            for color in self.swap_colors:
                image_to_render = swap_color(image_to_render, color[0], color[1])
            blit_center(surface,image_to_render,(int(self.x)-scroll[0]+self.offset[0]+center_x,int(self.y)-scroll[1]+self.offset[1]+center_y))

    def swap_entity(self, index, pos_fix):
        self.sub_entities[index].swap_colors = self.swap_colors
        if self not in self.sub_entities[index].sub_entities:
            self.sub_entities[index].sub_entities += [self]
        self = self.sub_entities[index]
        if self.flip:
            self.set_pos(self.sub_entities[0].x+pos_fix[1][0],self.sub_entities[0].y+pos_fix[1][1])
        else:
            self.set_pos(self.sub_entities[0].x+pos_fix[0][0],self.sub_entities[0].y+pos_fix[0][1])
        return self

    def animation_shift(self, animation_id, pos_fix):
        self.set_action(animation_id)
        if self.flip:
            self.set_pos(self.x+pos_fix[1][0],self.y+pos_fix[1][1])
        else:
            self.set_pos(self.x+pos_fix[0][0],self.y+pos_fix[0][1])

        



def mask_collision(surface_1, surface_2, offset_1, offset_2):
    mask_1 = pygame.mask.from_surface(surface_1)
    mask_2 = pygame.mask.from_surface(surface_2)
    offset = (int(offset_1[0]-offset_2[0]),int(offset_1[1]-offset_2[1]))
    return mask_2.overlap(mask_1, offset)


def surface_mask_collision(obj_1, obj_2):
    offset_1 = (obj_1[1].x, obj_1[1].y)
    offset_2 = (obj_2.x, obj_2.y)
    surface_1 = obj_1[0]
    surface_2 = pygame.Surface(offset_2)
    return mask_collision(surface_1, surface_2, offset_1, offset_2)


# animation stuff
global animation_database
animation_database = {}
 
global animation_higher_database
animation_higher_database = {}


def get_animation_database():
    global animation_higher_database
    return animation_higher_database


def animation_sequence(sequence,base_path,colorkey=(255,255,255),transparency=255):
    global animation_database
    result = []
    for frame in sequence:
        image_id = base_path + base_path.split('/')[-2] + '_' + str(frame[0])
        image = pygame.image.load(image_id + '.png').convert()
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        animation_database[image_id] = image.copy()
        for i in range(frame[1]):
            result.append(image_id)
    return result
 
 
def get_frame(ID):
    global animation_database
    return animation_database[ID]


def load_animations(path):
    global animation_higher_database, e_colorkey
    f = open(path + 'animations.txt','r')
    data = f.read()
    f.close()
    for animation in data.split('\n'):
        sections = animation.split(' ')
        anim_path = sections[0]
        entity_info = anim_path.split('/')
        entity_type = entity_info[0]
        animation_id = entity_info[1]
        timings = sections[1].split(';')
        tags = sections[2].split(';')
        sequence = []
        n = 0
        for timing in timings:
            sequence.append([n,int(timing)])
            n += 1
        anim = animation_sequence(sequence,path + anim_path,e_colorkey)
        if entity_type not in animation_higher_database:
            animation_higher_database[entity_type] = {}
        animation_higher_database[entity_type][animation_id] = [anim.copy(),tags]


def new_load_animations(animations_path):
    global animation_higher_database, e_colorkey
    for folder in os.listdir(animations_path):
        path = animations_path+folder+'/'
        with open(path + 'animations.txt','r') as f:
            data = f.read()
        entity_type = path.split('/')[-2]
        for animation in data.split('\n'):
            if animation == '':
                continue
            sections = animation.split(' ')
            anim_path = sections[0]
            entity_info = anim_path.split('/')
            animation_id = entity_info[0]
            timings = sections[1].split(';')
            tags = sections[2].split(';')
            sequence = []
            n = 0
            for timing in timings:
                sequence.append([n,int(timing)])
                n += 1
            anim = animation_sequence(sequence,path + anim_path,e_colorkey)
            if entity_type not in animation_higher_database:
                animation_higher_database[entity_type] = {}
            animation_higher_database[entity_type][animation_id] = [anim.copy(),tags]


def sub_render_animations(render_path):
    with open(render_path+'render.txt', 'r') as r:
        paths = r.read()
    for string in paths.split('\n'):
        if string[0] == '#':
            continue
        path, bits = string.split(' ')
        base_path = render_path + '_render_/' + path + '.png'
        bit = int(bits)
        anim = pygame.image.load(base_path).convert()
        base_path = render_path+path+'/'
        frame_count = 0
        try:
            os.mkdir(base_path)
        except:
            pass
        for pixel in range(anim.get_width()):
            if pixel%bit+frame_count == bit-1+frame_count:
                frame_img = clip(anim, pixel-bit+1+frame_count, 0, bit, anim.get_height())
                img = pygame.Surface((bit,anim.get_height()))
                frame_img.set_colorkey((176,18,10))
                img.fill((255,255,255))
                img.blit(frame_img, (0,0))
                pygame.image.save(img, base_path+'/'+base_path.split('/')[-2]+'_'+str(frame_count)+'.png')
                frame_count += 1

                
def render_animations(render_path):
    for folder in os.listdir(render_path):
        sub_render_animations(render_path+folder+'/')


def get_attributes(path):
    all_attr = {}
    for folder in os.listdir(path):
        with open(path+folder+'/skills.txt') as f:
            attributes = f.read()
        all_attr[folder] = []
        for index, attrib in enumerate(attributes.split('\n\n')):
            all_attr[folder].append({})
            for attr in attrib.split('\n'):
                sub_attr = attr.split(' ')
                if sub_attr[1] == 'True':
                    all_attr[folder][index][sub_attr[0]] = True
                elif sub_attr[1] == 'False':
                    all_attr[folder][index][sub_attr[0]] = False
                elif sub_attr[1][0] in '-1234567890':
                    if '.' in sub_attr[1]:
                        all_attr[folder][index][sub_attr[0]] = float(sub_attr[1])
                    else:
                        all_attr[folder][index][sub_attr[0]] = int(sub_attr[1])
                else:
                    all_attr[folder][index][sub_attr[0]] = sub_attr[1]
    return all_attr
            



# particles
def particle_file_sort(l):
    l2 = []
    for obj in l:
        l2.append(int(obj[:-4]))
    l2.sort()
    l3 = []
    for obj in l2:
        l3.append(str(obj) + '.png')
    return l3

global particle_images
particle_images = {}


def load_particle_images(path):
    global particle_images, e_colorkey
    file_list = os.listdir(path)
    for folder in file_list:
        try:
            img_list = os.listdir(path + '/' + folder)
            img_list = particle_file_sort(img_list)
            images = []
            for img in img_list:
                images.append(pygame.image.load(path + '/' + folder + '/' + img).convert())
            for img in images:
                img.set_colorkey(e_colorkey)
            particle_images[folder] = images.copy()
        except:
            pass


class particle(object):

    def __init__(self,x,y,particle_type,motion,decay_rate,start_frame,custom_color=None):
        self.x = x
        self.y = y
        self.type = particle_type
        self.motion = motion
        self.decay_rate = decay_rate
        self.color = custom_color
        self.frame = start_frame

    def draw(self,surface,scroll):
        global particle_images
        if self.frame > len(particle_images[self.type])-1:
            self.frame = len(particle_images[self.type])-1
        if self.color == None:
            blit_center(surface,particle_images[self.type][int(self.frame)],(self.x-scroll[0],self.y-scroll[1]))
        else:
            blit_center(surface,swap_color(particle_images[self.type][int(self.frame)],(255,255,255),self.color),(self.x-scroll[0],self.y-scroll[1]))

    def update(self):
        self.frame += self.decay_rate
        running = True
        if self.frame > len(particle_images[self.type])-1:
            running = False
        self.x += self.motion[0]
        self.y += self.motion[1]
        return running
        




# palette swap
def swap_color(img,old_c,new_c):
    global e_colorkey
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img,(0,0))
    surf.set_colorkey(e_colorkey)
    return surf





# custom font
def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


class Font():
    def __init__(self, path):
        self.spacing = 0
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.','-',',',':','+','\'','!','?','(',')','/','_','=','\\','[',']','*','"','<','>',';','%','{','}']
        font_img = pygame.image.load(path).convert()
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 200:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc, scale):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(pygame.transform.scale(self.characters[char], (5*scale,7*scale)), (loc[0] + x_offset*scale, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing





# visual functions
def perfect_outline(surf, img, loc):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((0,0,0))
    surf.blit(mask_surf,(loc[0]-1,loc[1]))
    surf.blit(mask_surf,(loc[0]+1,loc[1]))
    surf.blit(mask_surf,(loc[0],loc[1]-1))
    surf.blit(mask_surf,(loc[0],loc[1]+1))





# buttons
class Button():
    def __init__(self, loc, img_path, pressed_img_path=False, swap_colors=[]):
        self.img = load_img(img_path)
        self.rect = pygame.Rect(loc, (self.img.get_width(),self.img.get_height()))
        self.selection = False
        self.flip = False
        self.swap_colors = swap_colors
        if len(self.swap_colors) == 2:
            self.swap_colors = (self.swap_colors, (0,0))
        if pressed_img_path:
            self.pressed = False
            self.pressed_img = load_img(pressed_img_path)
            self.released_img = load_img(img_path)

    def selection_swap_check(self, rect):
        if self.rect.colliderect(rect):
            if not self.selection:
                for color in self.swap_colors:
                    self.img = swap_color(self.img, color[0], color[1])
            self.selection = True
            return True
        else:
            if self.selection:
                for color in self.swap_colors:
                    self.img = swap_color(self.img, color[1], color[0])
            self.selection = False
            return False

    def render(self, surf):
        surf.blit(self.img, (self.rect.x, self.rect.y))





# weapons
class Weapon():
    def __init__(self, loc, img_path, tag):
        self.img = load_img(img_path)
        self.rect = pygame.Rect(loc,(self.img.get_width(),self.img.get_height()))
        self.tag = tag

    def render_map(self, surf, scroll):
        surf.blit(self.img, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

    def render(self, surf, loc):
        surf.blit(self.img, loc)

    def scale_render(self, surf, loc, scale=1):
        surf.blit(pygame.transform.scale(self.img, (round(self.rect.width*scale),round(self.rect.height*scale))), loc)

    def equip_render(self, surf, loc, rotation, flipped):
        if flipped:
            surf.blit(flip(pygame.transform.rotate(self.img, rotation)), loc)
        else:
            surf.blit(pygame.transform.rotate(self.img, rotation), loc)

    def collision_test(self, rect):
        return self.rect.colliderect(rect)

    def copy(self):
        return self






# Controllers
def get_controllers():
    controllers = []
    for controller in range(pygame.joystick.get_count()):
        controllers.append(pygame.joystick.Joystick(controller))
        controllers[-1].init()
    return controllers


def get_controller_events(controller):
    axes = []
    buttons = []
    for axis in range(controller.get_numaxes()):
        axes.append(controller.get_axis(axis))
    for button in range(controller.get_numbuttons()):
        buttons.append(controller.get_button(button))
    return axes, buttons


###-------------------- SIMPLE CONTROLLER GUIDE --------------------###

#Buttons
#0 	X
#1 	Circle
#2 	Square
#3 	Triangle
#4 	Share
#5 	PS
#6 	Options
#7 	L3
#8 	R3
#9 	L1
#10 	R1
#11 	Down Arrow
#12 	Up Arrow 
#13 	Left Arrow
#14 	Right Arrow
#15 	D-Pad

#Axes
#0	L Right-Left
#1	L Up-Down
#2	R Right-Left
#3	R Up-Down
#4	L2
#5	R2

###-----------------------------------------------------------------###













