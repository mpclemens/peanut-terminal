#!/usr/bin/env python2
"""Terminal representation with ^-prefixed command sequences"""

import sys

###

class Terminal:
    """Represent a simple character terminal of ROWS x COLS characters"""

    _ROWS  = 10
    _COLS = 10

    def __init__(self, maxrows = _ROWS, maxcols = _COLS):
        """Set up a new empty terminal for input"""

        self._maxrows = maxrows
        self._maxcols = maxcols

        self.insert_mode = False
        self.row = 0
        self.col = 0

        self.clear_data()


    def clear_data(self):
        """Initialize to a grid of blanks"""
        self._data = [" " * self._maxcols] * self._maxrows


    def move_to(self, d_row, d_col):
        """Adjust the cursor location by a change in the row and/or column position, staying within bounds"""

        self.row += d_row
        self.col += d_col

        if self.row >= self._maxrows:
            self.row = self._maxrows-1
        elif self.row < 0:
            self.row = 0

        if self.col >= self._maxcols:
            self.col = self._maxcols-1
        elif self.col < 0:
            self.col = 0


    def go_to(self, new_row, new_col):
        """Set the cursor location to the new row and column position, staying within bounds"""
        self.move_to(new_row - self.row, new_col - self.col)


    def store(self, s):
        """Save the given string at the current row/col based on the insert mode"""

        the_row = self._data[self.row]

        if self.insert_mode:
            # Insert the new string at col, shifting old values to the right
            the_row = the_row[:self.col] + s + the_row[self.col:]
        else:
            # overwrite the existing string starting at col
            the_row = the_row[:self.col] + s + the_row[self.col+len(s):]

        self._data[self.row] = the_row[0:self._maxcols]


    def str(self):
        """Return the terminal as newline-delimited row strings"""
        rows = []
        for r in self._data:
            rows.append("".join(r))
        return "\n".join(rows)


    def interpret(self, s, echo=False):
        """Parse the input string for control commands (prefixed by ^) and plain text"""
        i = 0
        while i < len(s):

            if s[i] == "^":
                i += 1
                cmd = s[i]

                # subsequent characters are control sequence

                if cmd == "c":
                    # ^c - clear the entire screen; the cursor row and column do not change
                    self.clear_data()
                elif cmd == "h":
                    # ^h - move the cursor to row 0, column 0; the image on the screen is not changed
                    self.go_to(0,0)
                elif cmd == "b":
                    # ^b - move the cursor to the beginning of the current line; the cursor row does not change
                    self.move_to(0,-self.col)
                elif cmd == "d":
                    # ^d - move the cursor down one row if possible; the cursor column does not change
                    self.move_to(1,0)
                elif cmd == "u":
                    # ^u - move the cursor up one row, if possible; the cursor column does not change
                    self.move_to(-1,0)
                elif cmd == "l":
                    # ^l - move the cursor left one column, if possible; the cursor row does not change
                    self.move_to(0,-1)
                elif cmd == "r":
                    # ^r - move the cursor right one column, if possible; the cursor row does not change
                    self.move_to(0,1)
                elif cmd == "e":
                    # ^e - erase characters to the right of, and including, the cursor column on the cursor's row;
                    # the cursor row and column do not change
                    self.store(" " * self._maxcols) # will be truncated by store()
                elif cmd == "i":
                    # ^i - enter insert mode
                    self.insert_mode = True
                elif cmd == "o":
                    # ^o - enter overwrite mode
                    self.insert_mode = False
                elif cmd == "^":
                    # ^^ - write a circumflex (^) at the current cursor location, exactly as if it was not a special character;
                    # this is subject to the actions of the current mode (insert or overwrite)
                    self.store("^")
                elif cmd.isdigit():
                    # ^DD - move the cursor to the row and column specified; each D represents a decimal digit; the first
                    # D represents the new row number, and the second D represents the new column number
                    new_row = int(cmd)
                    i += 1
                    new_col = int(s[i])
                    self.go_to(new_row, new_col)

                if echo:
                    print self.str()

            else:
                # When a normal character (not part of a control sequence) arrives at the terminal, it is displayed on
                # the terminal screen in a manner that depends on the terminal mode
                self.store(s[i])
                self.move_to(0,1)

                if echo:
                    print self.str()

            i += 1

#

if __name__ == '__main__':
    filename = sys.argv[-1]
    fh = open(filename,"r")

    t = Terminal()

    for s in fh:
        t.interpret(s.rstrip("\n\r"))

    fh.close()
    print t.str()



