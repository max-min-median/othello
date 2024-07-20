class Board:
    
    ROWS = 8
    COLS = 8
    SYMBOLS = "-OX"
    def __init__(self, board=None, string=None):
        self._moves = None
        if string:
            p1_disks, p2_disks = string.count('1'), string.count('2')
            if abs(p1_disks - p2_disks) > 1: raise ValueError("Invalid number of disks of each colour!")
            self.player = 2 if p1_disks > p2_disks else 1
            self.board = [[int(string[row * Board.COLS + col]) for col in range(Board.COLS)] for row in range(Board.ROWS)]
        elif board:
            self.board = [[elem for elem in row] for row in board.board]
            self.player = board.player
        else:
            self.board = [[0] * Board.COLS for _ in range(Board.ROWS)]
            r = (Board.ROWS-1) // 2
            c = (Board.COLS-1) // 2
            self.board[r][c] = self.board[r+1][c+1] = 1
            self.board[r][c+1] = self.board[r+1][c] = 2
            self.player = 1
            
    @property
    def copy(self):
        return Board(board=self)

    def __repr__(self):
        repr = [" " + "".join([" " + chr(65 + col) for col in range(Board.COLS)])]
        for i in range(Board.ROWS):
            repr.append(f"{i+1}" + "".join([" " + Board.SYMBOLS[sqr] for sqr in self.board[i]]))
        return "\n".join(repr)

    @property
    def moves(self):
        if self._moves is not None: return self._moves
        self._moves = {}
        opponent = 3 - self.player
        for r in range(Board.ROWS):
            for c in range(Board.COLS):
                valid = False
                if self.board[r][c] != 0: continue
                for dr, dc in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                    flag = 0   # 1 = met opponent disk, 2 = met own disk after
                    r2, c2 = r+dr, c+dc
                    while 0 <= r2 < Board.ROWS and 0 <= c2 < Board.COLS and flag != 2:
                        if self.board[r2][c2] == 0: break
                        elif self.board[r2][c2] == opponent:
                            flag = 1
                            r2 += dr; c2 += dc
                        elif self.board[r2][c2] == self.player:
                            if flag == 0: break  # no opponent pieces in between
                            flag = 2
                    else:
                        if flag != 2: continue
                        if not valid: board_after = self.copy
                        valid = True
                        while (r2, c2) != (r, c):
                            board_after.board[r2][c2] = self.player
                            r2 -= dr; c2 -= dc
                if valid:
                    board_after.board[r][c] = self.player
                    board_after.player = 3 - board_after.player
                    self._moves[r, c] = board_after

        return self._moves

    @staticmethod
    def tup_to_A1(tup):
        col, row = tup
        return f"{chr(col + 65)}{row + 1}"

    @staticmethod
    def A1_to_tup(A1):
        import re
        A1 = A1.strip().upper()
        if not (m := re.match(r"([A-Z])(\d+)", A1)):
            raise ValueError("Invalid move string")
        col, row = m.groups()
        col = ord(col) - 65
        row = int(row) - 1
        if not 0 <= col < Board.COLS or not 0 <= row < Board.ROWS:
            raise ValueError("Invalid row/column")
        return row, col


a = Board(string='11002222'
                 '01211111'
                 '01122211'
                 '02122211'
                 '02122211'
                 '01120022'
                 '01022212'
                 '01102211'
)

b = Board()

while True:
    print('\n', b, sep='')
    while True:
        move = input(f"Move ({Board.SYMBOLS[b.player]}): ")
        try:
            move = Board.A1_to_tup(move)
            if move in b.moves: break
            print("Invalid move")
        except ValueError as e:
            print(e)
    b = b.moves[move]
