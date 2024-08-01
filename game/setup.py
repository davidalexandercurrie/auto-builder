import curses
import config
import colors


def initialize_windows():
    print("Initializing windows...")
    config.status_win = curses.newwin(3, 50, 0, 0)
    config.map_win = curses.newwin(config.MAP_HEIGHT, config.MAP_WIDTH * 2 + 5, 5, 5)
    config.key_win = curses.newwin(10, 30, 4, 60)

    config.status_win.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))
    config.map_win.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))
    config.key_win.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))
