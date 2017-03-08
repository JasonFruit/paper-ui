import os
import pygame
import math
from core import ScreenDrawer

class FrameBufferDrawer(ScreenDrawer):
    def __init__(self):
        
        "Initializes a new pygame screen using the framebuffer"
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        ScreenDrawer.__init__(self, width=self.size[0], height=self.size[1])
        
        # print("Framebuffer size: %d x %d" % (self.size[0], self.size[1]))
        self.display = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.display.fill((255, 255, 255))
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
        pass

    def send(self):
        
        self.display.fill((255, 255, 255))
        scrn = self.screen.convert("RGB").tobytes()
        img = pygame.image.fromstring(scrn, (1280,1024), "RGB")
        self.display.blit(img, (0,0))
        pygame.display.update()
    def clear(self):
        self.new_screen()
        self.send()
