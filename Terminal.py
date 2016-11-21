#!/usr/bin/env python2
"""Terminal representation"""

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

        self.row = new_row
        self.col = new_col

        if self.row >= self._maxrows:
            self.row = self._maxrows-1
        elif self.row < 0:
            self.row = 0

        if self.col >= self._maxcols:
            self.col = self._maxcols-1
        elif self.col < 0:
            self.col = 0


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


    def display(self):
        """Output the stringified data"""
        print self.str()


    def interpret(self, s):
        """Parse the input string for control commands (prefixed by ^), optionally printing after each command"""
        
