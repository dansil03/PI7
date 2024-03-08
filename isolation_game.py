import numpy as np
import pygame 


class IsolationGame: 
    def __init__(self):
        self.board = np.array([[' ' for _ in range(6)] for _ in range(6)])
        self.board[0, 0] = '1'  # Speler 1 startpositie
        self.board[5, 5] = '2'  # Speler 2 startpositie
        self.player = 1
        self.player_positions = [(0, 0), (5, 5)]  # Houdt de posities van de spelers bij 
        self.game_over = False
    
    def __str__(self):
        board_str = '\n'.join([' '.join(row) for row in self.board])
        return board_str
    
    def is_move_valid(self, x, y, new_x, new_y):
        if not (0 <= new_x < 6 and 0 <= new_y < 6):
            return False
        if self.board[new_x, new_y] != ' ':
            return False
        
        # controleert of de zet geldig is (voor een koningin)
        dx = new_x - x
        dy = new_y - y
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False
        if dx == 0 and dy == 0:
            return False
        
        # controleert voor blokkades
        step_x = 1 if dx > 0 else -1 if dx < 0 else 0
        step_y = 1 if dy > 0 else -1 if dy < 0 else 0
        steps = max(abs(dx), abs(dy))
        for step in range(1, steps):
            if self.board[x + step * step_x, y + step * step_y] != ' ':
                return False
        return True

    def move(self, new_x, new_y):
        if self.game_over:
            print("Game is already over.")
            return False
        
        current_position = self.player_positions[self.player - 1]
        if self.is_move_valid(*current_position, new_x, new_y):
            self.board[current_position] = 'X'  # Markeer het oude vak als geblokkeerd
            self.board[new_x, new_y] = str(self.player)
            self.player_positions[self.player - 1] = (new_x, new_y)  # Update de positie
            
            self.player = 1 if self.player == 2 else 2  # Wissel van speler
            
            # Controleer na de zet of de volgende speler geen geldige zetten meer heeft
            if self.terminal_state(self.player_positions[self.player - 1]):
                print(f"Game over. Player {3 - self.player} wins!")
                self.game_over = True
            return True 
        else: 
            print("Invalid move") 
        return False

    def terminal_state(self, player_position):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        x, y = player_position
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            # Controleer of de nieuwe positie binnen het bord is en of het veld leeg is.
            if 0 <= new_x < 6 and 0 <= new_y < 6 and self.board[new_x, new_y] == ' ':
                return False  # Er is een geldige zet gevonden
        return True  # Geen geldige zetten gevonden, spel is voorbij

class IsolationGamePygame: 
    def __init__(self): 
        pygame.init() 
        self.font = pygame.font.SysFont("arial", 36)
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.game = IsolationGame()
        self.cell_size = 100
        self.running = True

    def draw_board(self):
        for x in range(6):
            for y in range(6):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, pygame.Color('grey' if (x + y) % 2 == 0 else 'white'), rect)
                if self.game.board[y, x] == '1' or self.game.board[y, x] == '2':
                    pygame.draw.circle(self.screen, pygame.Color('black' if self.game.board[y, x] == '1' else 'red'), rect.center, self.cell_size // 3)
                elif self.game.board[y, x] == 'X':
                    pygame.draw.line(self.screen, pygame.Color('blue'), rect.topleft, rect.bottomright, 5)
                    pygame.draw.line(self.screen, pygame.Color('blue'), rect.bottomleft, rect.topright, 5)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if self.game.game_over:
                    self.show_game_over_message(3 - self.game.player)  # Toon bericht met de winnaar
                    pygame.time.wait(5000)  # Wacht 5 seconden
                    self.running = False  # Stop de game loop

                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Bepaal de cel waarin geklikt is
                    x, y = event.pos
                    grid_y, grid_x = x // self.cell_size, y // self.cell_size  # Draai x en y om
                    
                    # Voer de zet uit als de speler die aan de beurt is
                    if self.game.is_move_valid(*self.game.player_positions[self.game.player - 1], grid_x, grid_y):
                        self.game.move(grid_x, grid_y)
                    else:
                        print("Invalid move")


            self.screen.fill(pygame.Color('black'))
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def show_game_over_message(self, winner):
        message = f"Game Over. Player {winner} wins!"
        text_surface = self.font.render(message, True, pygame.Color('orange'))
        text_rect = text_surface.get_rect(center=(300, 300))  # Centreer het bericht
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()  # Update het scherm om het bericht te tonen

if __name__ == "__main__":
    game_vis = IsolationGamePygame()
    game_vis.run() 