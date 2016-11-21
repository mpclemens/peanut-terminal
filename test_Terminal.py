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

    def test_interpret_relative_moves(self):
        # Up, Down, Right, and Left, leaving a character behind after the moves
        #
        # Note that the cursor moves to the right after each character, so the
        # additional ^l sequences back it up into the expected position for
        # the next write
        #
        t = Terminal()

        t.go_to(4,4)
        t.interpret("^uU^d^d^lD^l^u^rR^l^l^lL")

        self.assertEqual(t.str(),"""          
          
          
    U     
   L R    
    D     
          
          
          
          ""","Result does not match")


    def test_interpret_row_column_moves(self):
        # Go to X,Y and Home, Beginning of Row, Erase from cursor, and Clear all
        t = Terminal()

        t.interpret("^i^90abcdefghijkklmnop")
        self.assertEqual(t.str(),
                         """          
          
          
          
          
          
          
          
          
abcdefghip""","Result does not match after last-row insert")


        t.interpret("^i^00==========")
        t.interpret("^i^40++++++++++")
        t.interpret("^i^90^e")
        t.interpret("^i^30----------")        
        t.interpret("^i^10^^^^^^^^^^^^^^^^^^^^")
        t.interpret("^i^20**********")


        self.assertEqual(t.str(),
                         """==========
^^^^^^^^^^
**********
----------
++++++++++
          
          
          
          
          ""","Result does not match after inserts and clearing last row")

        t.interpret("^h^e^11^e^22^e^33^e^44^e")

        self.assertEqual(t.str(),
                         """          
^         
**        
---       
++++      
          
          
          
          
          ""","Result does not match after making triangle of deletions")

        t.interpret("^b^e")

        self.assertEqual(t.str(),
                         """          
^         
**        
---       
          
          
          
          
          
          ""","Result does not match after beginning of row/erase sequence")

        r_before = t.row
        c_before = t.col
        t.interpret("^c")

        self.assertEqual(t.str(),
                         """          
          
          
          
          
          
          
          
          
          ""","Result does not match after clear-all")

        self.assertEqual(t.row, r_before)
        self.assertEqual(t.col, c_before)


    def test_challenge_data(self):
        """Run the command sequence presented in the challenge"""

        # Note: the trailing backslashes in the sample data caused Python to ignore them:
        # appending a space after the \ tells Python's """ intepreter to leave the \ alone
        
        data = """^h^c
^04^^
^13/ \^d^b  /   \ 
^u^d^d^l^l^l^l^l^l^l^l^l
^r^r^l^l^d<CodeEval >^l^l^d/^b \ 
^d^r^r^66/^b  \ 
^b^d   \ /
^d^l^lv^d^b===========^i^94O123456
789^94A=======^u^u^u^u^u^u^l^l\^o^b^r/
"""

        t = Terminal()

        for s in data.splitlines():
            t.interpret(s)        

        self.assertEqual(t.str(),
"""    ^     
   / \    
  /   \   
 /     \  
<CodeEval>
 \     /  
  \   /   
   \ /    
    v     
====A=====""","Result does not match sample output")
        
        
#

if __name__ == '__main__':
    unittest.main()

