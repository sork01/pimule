import pygame
from pygame.locals import *
import os
from conf import Config
import copy

class Menu:
    
    def set_rom_in_command(self, command, rom):
        new_command = copy.deepcopy(command)
        for i in range(len(command)):
            if command[i].find('%ROM%') == -1:
                continue
                
            new_command[i] = command[i].replace('%ROM%', rom)
        
        return new_command
    
    def is_dir_empty(self, dir):
        for dir, dirnames, filenames in os.walk(dir):
            if len(filenames) > 0:
                return False
        return True
    # Load a directory into the menu
    def load_dir(self):
        # Only add a "../" option if we're not in the root directory
        if os.path.abspath(self.dir) != os.path.abspath(self.root_dir):
            self.add_menu_item(Menu.MenuItem('../', Menu.Action(os.path.abspath(os.path.dirname(self.dir)), 'navigate')))
            self.back_action = Menu.Action(os.path.abspath(os.path.dirname(self.dir)), 'navigate')
        
        folder_list = []
        file_list = []
        
        for item in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, item)):
                # Create a menu item that has a navigation action for the directory
                if not self.is_dir_empty(os.path.abspath(os.path.join(self.dir, item))):
                    dir_conf = self.conf.get_conf_for_dir(os.path.join(self.dir, item))
                    dir_name = item
                    if not dir_conf['inherited'] and 'name' in dir_conf:
                        dir_name = dir_conf['name']
                    folder_list.append(Menu.MenuItem(dir_name + '/', Menu.Action(os.path.abspath(os.path.join(self.dir, item)), 'navigate')))
            elif os.path.isfile(os.path.join(self.dir, item)):
                # Create a menu item that has an execute action for the file
                if item[item.rfind('.'):].lower() in self.rom_suffixes or len(self.rom_suffixes) == 0:
                    file_list.append(Menu.MenuItem(item, Menu.Action(self.set_rom_in_command(self.emulator_command, os.path.join(self.dir, item)), 'execute')))
        
        # Sorts by the text of the menu item
        folder_list.sort(key=lambda x: x.text)
        file_list.sort(key=lambda x: x.text)
        
        # Add the menu items to the menu
        for item in folder_list:
            self.add_menu_item(item)
        for item in file_list:
            self.add_menu_item(item)
                
    # Represents a row in the menu.
    class MenuRow:
        def __init__(self, top, left, padding, font, font_color):
            self.top = top
            self.left = left
            self.padding = padding
            self.font = font
            self.font_color = font_color
            
        def set_content(self, menu_item):
            self.menu_item = menu_item
        
        def render(self, dest_surface):
            self.text_area = self.font.render(self.menu_item.text, 1, self.font_color) # Create text area with text
            self.text_container = self.text_area.get_rect()             # Get container for the text
            
            self.text_container.left = self.left
            self.text_container.top = self.top + self.padding
            pygame.display.update(dest_surface.blit(self.text_area, self.text_container))       
    
    # Represents an item in the menu
    class MenuItem:
        def __init__(self, text, action):
            self.text = text
            self.action = action
    
    # Represents an action to be done when selecting a menu item
    class Action:
        def __init__(self, action, action_type):
            self.action = action
            self.action_type = action_type
    
    def __init__(self, conf, player):
        self.conf = conf
        self.player = player
        pygame.display.init() 
        pygame.mouse.set_visible(False)
        
        self.root_dir = conf.get_conf_for_label('root')['dir']
    
    # Set the directory that the menu should show
    def set_dir(self, dir):
        # Load from conf
        conf = self.conf.get_conf_for_dir(dir)
        self.dir = conf['dir']
        if 'emulator_command' in conf:
            self.emulator_command = conf['emulator_command']
        else:
            self.emulator_command = ''
        if 'rom_suffixes' in conf:
            self.rom_suffixes = conf['rom_suffixes']
        else:
            self.rom_suffixes = []
        self.bg = pygame.image.load(conf['background_image']).convert() 
        self.font = pygame.font.Font(conf['font'], conf['font_size'])
        self.font_color = conf['font_color']
        self.font_size = conf['font_size']
        self.menu_width = conf['menu_width']
        self.menu_items_to_show = conf['menu_items_to_show']
        self.menu_item_padding = conf['menu_item_padding']
        self.menu_background_color = conf['menu_background_color']
        self.menu_border_color = conf['menu_border_color']
        self.menu_border_width = conf['menu_border_width']
        self.select_rect_color = conf['select_rect_color']
        self.player.play(conf['sound'])

        # Initialize the height that one row in the menu should have and stuff like that
        self.menu_items = []
        self.menu_rows = []
        self.menu_start = 0
        self.selected_menu_item = 0;
        
        self.initialize_menu_structure()
        self.load_dir()
        
    # Set the directory which is the root directory
    def set_root_dir(self, root_dir):
        self.root_dir = root_dir
    
    # Add a menu item to the menu
    def add_menu_item(self, menu_item):
        self.menu_items.append(menu_item)
    
    # Initialize the rows in the menu.(The height of the menu, menu rows and where the menu rows should be located)
    def initialize_menu_structure(self):
        self.row_height = self.font.render("", 1, (0, 0, 0)).get_rect().height + 2 * self.menu_item_padding # Fulfix
        self.menu_height = self.menu_items_to_show * self.row_height
        for i in range(self.menu_items_to_show):
            top = (self.row_height)*i
            menu_row = Menu.MenuRow(top, self.menu_item_padding, self.menu_item_padding, self.font, self.font_color)
            self.menu_rows.append(menu_row)
    
    # Move our selection according to the move parameter
    def move_selection(self, move):
        if self.selected_menu_item >= self.menu_items_to_show/2 and self.selected_menu_item < len(self.menu_items) - self.menu_items_to_show/2:
            self.menu_start += move
            self.menu_start = max(0, self.menu_start)
        
        self.selected_menu_item += move 
        if self.selected_menu_item < 0:
            self.selected_menu_item = len(self.menu_items) - 1
            self.menu_start = max(0, len(self.menu_items) - self.menu_items_to_show)
        elif self.selected_menu_item >= len(self.menu_items):
            self.selected_menu_item = 0
            self.menu_start = 0
    
    # Render background and menu onto dest_surface
    def render(self, dest_surface, full_update=False):
        # Calculate position stuff first
        self.left = dest_surface.get_rect().centerx - self.menu_width / 2
        self.top = dest_surface.get_rect().centery - self.menu_height / 2
        
        # If the background image isn't as big as the screen, resize it to fill the screen
        if self.bg.get_size() != dest_surface.get_size():
            self.bg = pygame.transform.scale(self.bg, dest_surface.get_size())
        
        # (Re-)render the background to the whole screen or just the are where the menu is
        if full_update:
            dest_surface.blit(self.bg, (0, 0)) # Background
        else:
            dest_surface.blit(self.bg, (self.left,self.top), (self.left, self.top, self.menu_width, self.menu_height)) # Background
        
        self.draw_menu_window(dest_surface)         # White window with border
        
        menu = pygame.Surface((self.menu_width, self.menu_height))  # Create the menu
        menu.set_colorkey(0,0)
        
        pygame.draw.rect(menu,self.select_rect_color,self.create_select_rect()) # draw selection rectangle
        
        # Here comes the items in the menu
        i = 0
        for menu_row in self.menu_rows:
            if self.menu_start + i >= len(self.menu_items):
                break
            menu_row.set_content(self.menu_items[self.menu_start + i])
            menu_row.render(menu)
            i = i + 1
        if full_update:
            dest_surface.blit(menu,(self.left, self.top))
            pygame.display.flip()
        else:
            pygame.display.update(dest_surface.blit(menu,(self.left, self.top)))
    
    # Draw the window that works lika a background fpr the menu with borders
    def draw_menu_window(self, dest_surface):
        menu2 = pygame.Surface((self.menu_width, self.menu_height))
        menu2.fill(self.menu_background_color)
        menu2.set_alpha(100)
        dest_surface.blit(menu2,(self.left, self.top))
        
        # The borders
        pygame.draw.rect(dest_surface, self.menu_border_color, (self.left - self.menu_border_width, self.top - self.menu_border_width, self.menu_border_width, self.menu_height + 2 * self.menu_border_width))
        pygame.draw.rect(dest_surface, self.menu_border_color, (self.left + self.menu_width, self.top - self.menu_border_width, self.menu_border_width, self.menu_height + 2 * self.menu_border_width))
        pygame.draw.rect(dest_surface, self.menu_border_color, (self.left - self.menu_border_width, self.top - self.menu_border_width, self.menu_width + 2 * self.menu_border_width, self.menu_border_width))
        pygame.draw.rect(dest_surface, self.menu_border_color, (self.left - self.menu_border_width, self.top + self.menu_height, self.menu_width + 2 * self.menu_border_width, self.menu_border_width))
    
    # Create a selection rectangle at the location for the currently selected item
    def create_select_rect(self):
        top = self.menu_rows[self.selected_menu_item - self.menu_start].top
        left = 0
        height = self.row_height
        width = self.menu_width
        return (left,top ,width, height)
    
    # Destroy the menu, currently only stops the player (sound).
    def destroy(self):
        self.player.stop()