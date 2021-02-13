BTN_UP = 0

class JoystickInputHandler:
    
    # Testar lite git då
    # I'm thinking that the configuration after being loaded through load_conf_for_joystick would
    # look something like this. It would be similar in KeyboardInputHandler but without the grouping
    # into axis, btn and so on.
    #
    # This way, when you detect a buttonpress you can just lookup key_conf['btn'][btn_id] where btn_id
    # is the button that was pressed. Or if you detext an axis motion you can just lookup
    # key_conf['axis'][axis_value] where axis_value is the value returned from the axis
    #
    #
    # key_conf = {
    #     'axis' = {
    #         (-1,0) = 'up',
    #         (1,0) = 'down'
    #         (0,-1) = 'left'
    #         (0,1) = 'right'
    #     },
    #     'btn' = {
    #         0 = 'start'
    #         1 = 'a',
    #         2 = 'b',
    #         3 = 'y',
    #         4 = 'x',
    #         5 = 'l',
    #         ...
    #     },
    #     'hat' = {
    #         ...
    #     },
    #     ...?
    # }
    
    def __init__(self, joystick_id, player_id):
        self.load_conf_for_joystick(player_id)
        self.joystick = pygame.joystick.Joystick(joystick_id)
        self.joystick.init()
    
    # Load configuration for the joystick
    def load_conf_for_joystick(self, player_id_id):
        # Search conf for lines that matches input_player#_?_btn where # is the player_id
        # and the ? is the string for the button in retroarch.cfg
    
    # Listen for joystick input and do stuff with it    
    def handle_it(self):
        while 1:
            axes = self.joystick.get_numaxes()
            
            for i in range( axes ):
                axis = self.joystick.get_axis( i )
                textPrint.print1(screen, 'Axis {} value: {}'.format(i, axis) )
                
            buttons = self.joystick.get_numbuttons()

            for i in range( buttons ):
                button = joystick.get_button( i )
                textPrint.print1(screen, 'Button {:>2} value: {}'.format(i,button) )
                
            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrint.print1(screen, 'Number of hats: {}'.format(hats) )

            for i in range( hats ):
                hat = joystick.get_hat( i )
                textPrint.print1(screen, 'Hat {} value: {}'.format(i, str(hat)) )

class KeyboardInputHandler:

    def __init__(self, player_id):
        # Do something fun
        
    # Load configuration for the keyboard
    def load_conf_for_joystick(self, player_id):
        # Search conf for lines that matches input_player#_? where # is the player_id
        # and the ? is the string for the button in retroarch.cfg    
    
    # Listen for keyboard input and do stuff with it
    def handle_it(self):
        pygame.key.set_repeat(199,69)#(delay,interval)
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # What action should we do?
                    if event.key == K_UP:
                    # And then draw the result of our action
                    pygame.display.flip()
                elif event.type == QUIT:
                    exit(menu)
                else:
                    count = 0
            pygame.time.wait(8)
        
