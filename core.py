import os
from pervasive import PervasiveDisplay
from key_events import ExclusiveKeyReader
from PIL import Image, ImageFont, ImageDraw
from epd_func import convert

class ScreenDrawer(object):
    def __init__(self, width=800, height=480):
        self.screen = None
        self.width = width
        self.height = height
        self.font = ImageFont.truetype("fonts/RobotoMono-Bold.ttf", size=15)
        self.display = PervasiveDisplay()
    def new_screen(self):
        self.screen = Image.new("1",
                                (self.width, self.height),
                                1)
        self._drawer = ImageDraw.Draw(self.screen)
    def text(self, x, y, text):
        self._drawer.text((x, y), text, font=self.font)
    def rectangle(self, x, y, x1, y1, fill=False):
        self._drawer.rectangle([x, y, x1, y1],
                               outline=0,
                               fill=fill and 0 or 1)
    def line(self, x, y, x1, y1):
        self._drawer.line([x, y, x1, y1])
    def clear(self):
        self.new_screen()
        self.send()
    def epd(self):
        return convert(self.screen)
    def screenshot(self, fn):
        self.screen.save(fn)
    def send(self):
        self.screen = self.screen.rotate(270)
        self.display.reset_data_pointer()
        self.display.send_image(self.epd())
        self.display.update_display()

class DebugScreenDrawer(ScreenDrawer):
    def __init__(self, directory, width=800, height=480):
        ScreenDrawer.__init__(self, width, height)
        self.directory = directory
        self.screen_num = 0
    def send(self):
        fn = str(self.screen_num).zfill(5) + ".png"
        self.screenshot(os.path.join(self.directory,
                                     fn))
        self.screen_num += 1
    def clear(self):
        self.new_screen()
        self.send()
