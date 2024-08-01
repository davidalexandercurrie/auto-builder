import curses


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)


WHITE_ON_BLUE = 1
GREEN_ON_BLACK = 2
RED_ON_BLACK = 3
BLACK_ON_YELLOW = 4
BLACK_ON_WHITE = 5
