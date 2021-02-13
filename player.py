import pygame
import time

class Player():
    
    current_file = ''
    current_pos = 0.0
    
    def __init__(self):
        pygame.mixer.init()
        
    def play(self, file):
        if file == self.current_file:
            return
        
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1, 0.0) # Start at 0.0 and repeat an infinite amount of times
        self.current_file = file
        
    def stop(self):
        pygame.mixer.music.stop()
        
    def pause(self):
        pygame.mixer.music.pause()
        
    def resume(self):
        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play(-1, 0.0) # Start at 0.0 and repeat an infinite amount of times