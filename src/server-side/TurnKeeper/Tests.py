import unittest
import TurnKeeper
import time

player_list = ['gunga', 'munga', 'junga', 'bunga']

class TestTurkKeeper(unittest.TestCase):


    #asserts that index is 0 and gunga returns true
    def test_is_turn(self):

        tk = TurnKeeper.TurnKeeper(player_list,3)
        self.assertEqual(tk.is_turn('gunga'), True)
        self.assertEqual(tk.is_turn('munga'), False)

    #calls next player function 3 times, resulting in the length of the list -1
    #compares the index to 3.
    #calls function again to roll it back over to 0
    def test_next_player(self):

        tk = TurnKeeper.TurnKeeper(player_list,3)
        tk.next_player()
        tk.next_player()
        tk.next_player()
        final_value = 3

        self.assertEqual(tk.index, final_value)

        tk.next_player()

        self.assertEqual(tk.index, 0)

    #Starts a timer, which runs on a different thread.
    #Value of index is checked to make sure it is incremented by one
    def test_start_turn_timer(self):

        tk = TurnKeeper.TurnKeeper(player_list, 1)
        first_val = tk.index
        tk.start_turn_timer()
        time.sleep(1.1)
        last_val = tk.index

        self.assertNotEqual(first_val, last_val)
    
if __name__ == '__main__':
    unittest.main()