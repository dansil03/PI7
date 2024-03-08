import unittest
from isolation_game import IsolationGame  # Zorg ervoor dat je class correct geïmporteerd wordt
import numpy as np

class TestIsolationGame(unittest.TestCase):

    def test_terminal_state_win(self):
        game = IsolationGame()
        # Stel een scenario in waarin een speler vastzit en het spel zou moeten eindigen
        game.board = np.array([
            ['X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', '2', 'X', 'X'],
            [' ', 'X', 'X', 'X', 'X', 'X'],
            [' ', 'X', '1', ' ', ' ', 'X'],
            [' ', ' ', ' ', ' ', ' ', 'X']])
        game.player_positions = [(4, 2), (2, 5)]  # Stel de posities van de spelers in
        game.player = 1  # Speler 1 is aan de beurt
        self.assertTrue(game.terminal_state(game.player_positions[game.player - 1]))

    def test_move_valid(self):
        game = IsolationGame()
        self.assertTrue(game.move(0, 1))  # Eerste zet van speler 1 zou geldig moeten zijn
        
    def test_move_invalid(self):
        game = IsolationGame()
        game.move(0, 1)  # Eerste zet van speler 1
        self.assertFalse(game.move(0, 1))  # Probeer dezelfde zet opnieuw, zou ongeldig moeten zijn

    # Voeg hier meer tests toe

if __name__ == '__main__':
    unittest.main()
