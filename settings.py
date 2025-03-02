import ctypes
ctypes.windll.user32.SetProcessDPIAware() # Cause pygame hates scaling ig

SCREEN_SIZE = (640, 480)