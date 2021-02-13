#!/usr/bin/python3

import sys
import pygame
from pygame.locals import *
import subprocess
import os
from scroll_menu import Menu
import pygame.mixer
from conf import Config
from player import Player
from reset_button_handler import GPIOButtonHandler
import copy

global current_proc
global is_only_one_game

if not pygame.font.get_init():
    pygame.font.init()
        
def exit(menu):
    menu.destroy()
    pygame.display.quit()
    sys.exit()
    
def return_to_menu():
    global current_proc
    if current_proc != None:
        current_proc.kill()

def start_game_if_alone(conf):
    global current_proc
    global is_only_one_game
    files = 0
    filepath = ""
    emulator_command = []
    for dirname, dirnames, filenames in os.walk(conf.get_conf_for_label('root')['dir']):
        # print path to all filenames.
        conf_for_dir = conf.get_conf_for_dir(dirname)
        rom_suffixes = conf_for_dir['rom_suffixes']
        emulator_command = copy.deepcopy(conf_for_dir['emulator_command'])
        for filename in filenames:
            if filename[filename.rfind('.'):].lower() in rom_suffixes or len(rom_suffixes) == 0:
                files += 1
                filepath = os.path.join(dirname, filename)
                for i in range(len(emulator_command)):
                    if emulator_command[i].find('%ROM%') == -1:
                        continue
                    emulator_command[i] = emulator_command[i].replace('%ROM%', filepath)
    if files == 1:
        is_only_one_game = True
        current_proc = subprocess.Popen(emulator_command)
        current_proc.wait()
    else:
        is_only_one_game = False


if __name__ == "__main__":
    global current_proc
    global is_only_one_game
    current_proc = None
    reset_handler = GPIOButtonHandler(return_to_menu, 13)
    reset_handler.start()
    
    conf = Config()
    
    is_only_one_game = True
    while is_only_one_game:
        start_game_if_alone(conf)
    
    player = Player()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #0,6671875 and 0,(6) of HD resoultion
    
    menu = Menu(conf, player)
    menu.set_dir(conf.get_conf_for_label('root')['dir'])
    menu.render(screen, full_update = True)
    
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pygame.key.set_repeat(199,69)#(delay,interval)
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # What action should we do?
                if event.key == K_UP:
                    menu.move_selection(-1)
                    menu.render(screen)
                if event.key == K_DOWN:
                    menu.move_selection(1)
                    menu.render(screen)
                if event.key == K_RETURN:
                    #menu = 
                    selected_menu_item = menu.menu_items[menu.selected_menu_item]
                    if selected_menu_item.action.action_type == 'navigate':
                        menu.set_dir(menu.menu_items[menu.selected_menu_item].action.action)
                        menu.render(screen, full_update = True)
                    elif selected_menu_item.action.action_type == 'execute':
                        player.pause()
                        pygame.display.quit()
                        current_proc = subprocess.Popen(selected_menu_item.action.action)
                        current_proc.wait()
                        player.resume()
                        pygame.display.init()
                        pygame.mouse.set_visible(False)
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #0,6671875 and 0,(6) of HD resoultion
                        menu.render(screen, full_update = True)
                if event.key == K_ESCAPE:
                    exit(menu)
            elif event.type == QUIT:
                exit(menu)
	
	#### JOYPAD CONFIGURATION ####
        axis0 = round(joystick.get_axis(0))
        axis1 = round(joystick.get_axis(1))
        if axis1 == -1:
            menu.move_selection(-1)
            menu.render(screen)
        if axis1 == 1:
            menu.move_selection(1)
            menu.render(screen)
        if axis0 == -1:
            menu.move_selection(-3)
            menu.render(screen)       
        if axis0 == 1:
            menu.move_selection(3)
            menu.render(screen)   
            #menu = 
        if joystick.get_button( 0 ) == 1:
            selected_menu_item = menu.menu_items[menu.selected_menu_item]
            if selected_menu_item.action.action_type == 'navigate':
                menu.set_dir(menu.menu_items[menu.selected_menu_item].action.action)
                menu.render(screen, full_update = True)
            elif selected_menu_item.action.action_type == 'execute':
                player.pause()
                pygame.display.quit()
                current_proc = subprocess.Popen(selected_menu_item.action.action)
                current_proc.wait()
                current_proc = None
                player.resume()
                pygame.display.init()
                pygame.mouse.set_visible(False)
                screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #0,6671875 and 0,(6) of HD resoultion
                menu.render(screen, full_update = True)
        if joystick.get_button( 1 ) == 1:
            menu.set_dir(menu.back_action.action)
            menu.render(screen, full_update = True)
        pygame.time.wait(8)
       
