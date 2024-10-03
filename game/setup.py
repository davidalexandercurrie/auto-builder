import curses
import config
import colors
import threading


def initialize_windows():
    print("Initializing windows...")
    config.status_win = curses.newwin(3, 50, 0, 0)
    config.status_win.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))

    config.map_win = curses.newwin(config.MAP_HEIGHT, config.MAP_WIDTH * 4 + 5, 5, 5)
    config.map_win.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))

    config.turn_timer_win = curses.newwin(2, config.MAP_WIDTH * 4 + 1, 3, 5)
    config.turn_timer_win.bkgd(" ", curses.color_pair(colors.BLACK_ON_YELLOW))

    config.key_win = curses.newwin(10, 30, 4, 80)
    config.key_win.bkgd(" ", curses.color_pair(colors.WHITE_ON_BLUE))
