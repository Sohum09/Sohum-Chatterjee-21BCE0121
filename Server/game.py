class Character:
    def __init__(self, name, player):
        self.name = name
        self.player = player

    def __str__(self):
        return f"{self.player}-{self.name}"

    def to_dict(self):
        return {'name': self.name, 'player': self.player}

class Pawn(Character):
    def valid_moves(self, position):
        x, y = position
        moves = []
        if x > 0:
            moves.append((x - 1, y))
        if x < 4:
            moves.append((x + 1, y))
        if y > 0:
            moves.append((x, y - 1))
        if y < 4:
            moves.append((x, y + 1))
        return moves

class Hero1(Character):
    def valid_moves(self, position):
        x, y = position
        moves = []
        if x > 1:
            moves.append((x - 2, y))
        if x < 3:
            moves.append((x + 2, y))
        if y > 1:
            moves.append((x, y - 2))
        if y < 3:
            moves.append((x, y + 2))
        return moves

class Hero2(Character):
    def valid_moves(self, position):
        x, y = position
        moves = []
        if x > 1 and y > 1:
            moves.append((x - 2, y - 2))
        if x > 1 and y < 3:
            moves.append((x - 2, y + 2))
        if x < 3 and y > 1:
            moves.append((x + 2, y - 2))
        if x < 3 and y < 3:
            moves.append((x + 2, y + 2))
        return moves

class Game:
    def __init__(self):
        self.board = [[None for _ in range(5)] for _ in range(5)]
        self.current_turn = 'A'
        self.setup_game()

    def setup_game(self):
        # Place pieces for Player A
        self.board[0][0] = Pawn('P1', 'A')
        self.board[0][1] = Hero1('H1', 'A')
        self.board[0][2] = Hero2('H2', 'A')
        # Place pieces for Player B
        self.board[4][0] = Pawn('P1', 'B')
        self.board[4][1] = Hero1('H1', 'B')
        self.board[4][2] = Hero2('H2', 'B')

    def move_character(self, command):
        piece_name, move = command.split(':')
        piece = self.find_piece(piece_name)
        if not piece:
            return False

        # Determine valid moves
        x, y = self.find_position(piece)
        valid_moves = piece.valid_moves((x, y))

        new_x, new_y = self.calculate_new_position(x, y, move)
        if (new_x, new_y) in valid_moves:
            # Move the piece
            self.board[new_x][new_y] = piece
            self.board[x][y] = None
            self.switch_turn()
            return True
        return False

    def find_piece(self, name):
        for row in self.board:
            for cell in row:
                if cell and cell.name == name:
                    return cell
        return None

    def find_position(self, piece):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == piece:
                    return (i, j)
        return None

    def calculate_new_position(self, x, y, move):
        if move == 'L':
            return (x, y - 1)
        if move == 'R':
            return (x, y + 1)
        if move == 'F':
            return (x - 1, y)
        if move == 'B':
            return (x + 1, y)
        if move == 'FL':
            return (x - 2, y - 2)
        if move == 'FR':
            return (x - 2, y + 2)
        if move == 'BL':
            return (x + 2, y - 2)
        if move == 'BR':
            return (x + 2, y + 2)
        return (x, y)

    def switch_turn(self):
        self.current_turn = 'B' if self.current_turn == 'A' else 'A'

    def get_board(self):
        return self.board
