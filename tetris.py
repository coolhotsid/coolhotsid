import curses
import random
import time

# Tetris game constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
TICK_RATE = 0.5  # seconds per tick

# Define the shapes as lists of rotation states. Each rotation state is a list of
# coordinate offsets from the shape's origin. The origin (0,0) is the top-left of
# the shape's bounding box. Shapes are taken from the classic Tetris set.
SHAPES = {
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    'O': [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],
    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

COLORS = [1, 2, 3, 4, 5, 6, 7]

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.rot = 0
        self.x = BOARD_WIDTH // 2 - 2
        self.y = 0

    def cells(self):
        return SHAPES[self.shape][self.rot]

    def rotate(self):
        self.rot = (self.rot + 1) % len(SHAPES[self.shape])


def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def draw_board(stdscr, board, current):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            value = board[y][x]
            ch = '█' if value else ' '
            stdscr.addstr(y, x * 2, ch * 2)

    if current:
        for dx, dy in current.cells():
            x = current.x + dx
            y = current.y + dy
            if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                stdscr.addstr(y, x * 2, '██')

    stdscr.refresh()


def check_collision(board, piece, dx=0, dy=0, rot=False):
    rot_index = piece.rot
    if rot:
        rot_index = (rot_index + 1) % len(SHAPES[piece.shape])
    for px, py in SHAPES[piece.shape][rot_index]:
        x = piece.x + px + dx
        y = piece.y + py + dy
        if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
            return True
        if board[y][x]:
            return True
    return False


def place_piece(board, piece):
    for px, py in piece.cells():
        x = piece.x + px
        y = piece.y + py
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            board[y][x] = 1


def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    while len(new_board) < BOARD_HEIGHT:
        new_board.insert(0, [0] * BOARD_WIDTH)
    return new_board, lines_cleared


def game_loop(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(int(TICK_RATE * 1000))

    board = create_board()
    current = Piece(random.choice(list(SHAPES.keys())))
    score = 0

    while True:
        draw_board(stdscr, board, current)
        stdscr.addstr(0, BOARD_WIDTH * 2 + 2, f'Score: {score}')

        key = stdscr.getch()
        if key == curses.KEY_LEFT and not check_collision(board, current, dx=-1):
            current.x -= 1
        elif key == curses.KEY_RIGHT and not check_collision(board, current, dx=1):
            current.x += 1
        elif key == curses.KEY_DOWN and not check_collision(board, current, dy=1):
            current.y += 1
        elif key == curses.KEY_UP and not check_collision(board, current, rot=True):
            current.rotate()
        elif key == ord('q'):
            break

        if not check_collision(board, current, dy=1):
            current.y += 1
        else:
            place_piece(board, current)
            board, cleared = clear_lines(board)
            score += cleared * 100
            current = Piece(random.choice(list(SHAPES.keys())))
            if check_collision(board, current):
                stdscr.addstr(BOARD_HEIGHT // 2, BOARD_WIDTH - 4, 'GAME OVER')
                stdscr.refresh()
                time.sleep(2)
                break


def main():
    curses.wrapper(game_loop)


if __name__ == '__main__':
    main()
