import pystray
from PIL import Image

from check_process import *
from settings import *

class Tray:
    def __init__(self):
        self.icon = Image.open('../images/knu_cse.ico')
        self.icon.visible = True
        
        self.menu = pystray.Menu(
            pystray.MenuItem('Settings', config_settings),
            pystray.MenuItem('Exit', self.exit_action)
        )
        
        self.tray = pystray.Icon('QR Code Scanner', self.icon, 'QR Code Scanner', self.menu)
        self.tray.run()
        