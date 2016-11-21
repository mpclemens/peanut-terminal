#!/usr/bin/env python2

import unittest

from Terminal import *

#

class test_Terminal(unittest.TestCase):
    
    def test_setup(self):
        t = Terminal(3,5)
        self.assertFalse(t.insert_mode,"Should be in overstrike mode at create time")
        self.assertEqual(t.row,0,"Should be in row zero at create time")
        self.assertEqual(t.col,0,"Should be in column zero at create time")

        self.assertEqual(t.str(), "     \n     \n     ", "Should be three newline-terminated rows of spaces")

    def test_move_to(self):
        t = Terminal()

        t.move_to(5,5)
        self.assertEqual(t.row,5,"Should be in row five after move")
        self.assertEqual(t.col,5,"Should be in column five after move")

        t.move_to(10,1) # exceeds the maximum rows
        self.assertEqual(t.row,9,"Should be in row nine after move")
        self.assertEqual(t.col,6,"Should be in column six after move")

        t.move_to(0,10) # exceeds the maximum columns
        self.assertEqual(t.row,9,"Should be in row nine after move")
        self.assertEqual(t.col,9,"Should be in column nine after move")

        t.move_to(-10,0) # below the minimum rows
        self.assertEqual(t.row,0,"Should be in row zero after move")
        self.assertEqual(t.col,9,"Should still be in column nine after move")

        t.move_to(0,-10) # below the minimum rows
        self.assertEqual(t.row,0,"Should still be in row zero after move")
        self.assertEqual(t.col,0,"Should be in column zero after move")

        # normal moves - rows

        t.move_to(1,0) 
        self.assertEqual(t.row,1,"Should be in row one after move")
        self.assertEqual(t.col,0,"Should be in column zero after move")
        
        t.move_to(1,0) 
        self.assertEqual(t.row,2,"Should be in row two after move")
        self.assertEqual(t.col,0,"Should be in column zero after move")

        t.move_to(-1,0)
        self.assertEqual(t.row,1,"Should be in row one after move")
        self.assertEqual(t.col,0,"Should be in column zero after move")

        # normal moves - columns

        t.move_to(0,1) 
        self.assertEqual(t.row,1,"Should be in row one after move")
        self.assertEqual(t.col,1,"Should be in column one after move")
        
        t.move_to(0,-1)
        self.assertEqual(t.row,1,"Should be in row two after move")
        self.assertEqual(t.col,0,"Should be in column zero after move")

        t.move_to(0,1) 
        self.assertEqual(t.row,1,"Should be in row one after move")
        self.assertEqual(t.col,1,"Should be in column one after move")

    def test_go_to(self):
        t = Terminal()

        t.go_to(5,5)
        self.assertEqual(t.row,5,"Should be in row five after go")
        self.assertEqual(t.col,5,"Should be in column five after go")

        t.go_to(10,1) # exceeds the maximum rows
        self.assertEqual(t.row,9,"Should be in row nine after go")
        self.assertEqual(t.col,1,"Should be in column one after go")

        t.go_to(0,10) # exceeds the maximum columns
        self.assertEqual(t.row,0,"Should be in row zero after go")
        self.assertEqual(t.col,9,"Should be in column nine after go")

        t.go_to(-10,-10) # below the minimums
        self.assertEqual(t.row,0,"Should be in row zero after go")
        self.assertEqual(t.col,0,"Should be in column zero after go")

        t.go_to(10,10) # above the maximums
        self.assertEqual(t.row,9,"Should be in row nine after go")
        self.assertEqual(t.col,9,"Should be in column nine after go")
        
    def test_store_single_row(self):
        # Basic checking insert vs. overwrite mode
        t = Terminal(1,10)

        t.store("The cat sat down")
        self.assertEqual(t.str(),"The cat sa","String should be truncated")

        t.go_to(0,4)
        t.store("CAR")
        self.assertEqual(t.str(),"The CAR sa","String should have overwritten data")

        t.insert_mode = True
        t.go_to(0,0)
        t.store("*Now*")
        self.assertEqual(t.str(),"*Now*The C","String should should show inserted data")

        t.go_to(0,0)
        t.store("1234567890")
        self.assertEqual(t.str(),"1234567890","String should have been replaced by insert: " + t.str())

        t.go_to(0,5)
        t.store("abc")
        self.assertEqual(t.str(),"12345abc67","String should have insert in the middle: " + t.str())

        t.insert_mode = False
        t.go_to(0,2)
        t.store("XYZ")
        self.assertEqual(t.str(),"12XYZabc67","String should have overwrite near the start: " + t.str())

#

if __name__ == '__main__':
    unittest.main()

