art-tui(1)

# NAME

art-tui - draw a framed message in the terminal

# SYNOPSIS

*art-tui* [_MESSAGE_]

*art-tui* --dump [_MESSAGE_]

# DESCRIPTION

*art-tui* clears the terminal, draws a frame around the screen and prints
_MESSAGE_ in the centre, then waits for a key press.

With *--dump* the program prints the ncurses version and the computed
position of the message for a 24x80 screen without entering curses mode.
