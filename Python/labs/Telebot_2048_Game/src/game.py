from random import *
from PIL import Image, ImageDraw, ImageFont


BACKGROUND_COLOR = (187, 173, 160)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

FONT_SIZE = 40
FONT_PATH = "./Arciform.ttf"
FONT_COLOR = (119, 110, 101)


GRID_SIZE = 4
START_TILES = 2
WIN_TILE = 2048
TILE_SIZE = 100
MARGIN = 10

def _init_field():

    field = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for _ in range(START_TILES):
        _add_tile(field)

    return field


def _add_tile(field):

    empty_coords = [[], []]
    count = 0

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if field[i][j] == 0:
                empty_coords[0].append(i)
                empty_coords[1].append(j)
                count += 1

    if count == 0: return

    random_index = randint(0, count - 1)
    row = empty_coords[0][random_index]
    col = empty_coords[1][random_index]

    if randint(1, 100) <= 10: field[row][col] = 4
    else: field[row][col] = 2


def _print_field(field):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            print('{:<4d}'.format(field[i][j]), end=' ')
        print()


def _draw_field(field, user_id):
    image = Image.new('RGB', (GRID_SIZE * TILE_SIZE + MARGIN * (GRID_SIZE + 1),
                              GRID_SIZE * TILE_SIZE + MARGIN * (GRID_SIZE + 1)), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell = field[i][j]
            color = TILE_COLORS.get(cell, TILE_COLORS[2048])
            x = j * TILE_SIZE + (j + 1) * MARGIN
            y = i * TILE_SIZE + (i + 1) * MARGIN

            draw.rectangle([x, y, x + TILE_SIZE, y + TILE_SIZE], fill=color)

            if cell != 0:
                text = str(cell)
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_x = x + (TILE_SIZE - (text_bbox[2] - text_bbox[0])) / 2
                text_y = y + (TILE_SIZE - (text_bbox[3] - text_bbox[1])) / 2
                draw.text((text_x, text_y), text, fill=FONT_COLOR, font=font)

    image.save(f"game_grid_{user_id}.png")



def move(field, direction, score):

    if direction == 'a':
        return move_left(field, score)

    elif direction == 'd':
        return move_right(field, score)

    elif direction == 'w':
        return move_up(field, score)

    elif direction == 's':
        return move_down(field, score)

    return field, score


def move_left(field, score):

    new_field = []

    for row in field:

        new_row = [num for num in row if num != 0]

        for i in range(len(new_row) - 1):

            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                score += new_row[i]
                new_row[i + 1] = 0

        new_row = [num for num in new_row if num != 0]

        new_row += [0] * (len(row) - len(new_row))
        new_field.append(new_row)

    return new_field, score

def move_right(field, score):

    new_field = []

    for row in field:

        new_row = [i for i in row if i != 0][::-1]

        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                score += new_row[i]
                new_row[i + 1] = 0

        new_row = [i for i in new_row if i != 0]
        new_row += [0] * (len(row) - len(new_row))

        new_field.append(new_row[::-1])

    return new_field, score


def move_up(field, score):

    num_rows = len(field)
    num_cols = len(field[0])

    for j in range(num_cols):

        col = [field[i][j] for i in range(num_rows)]

        new_col = [i for i in col if i != 0]

        for i in range(len(new_col) - 1):
            if new_col[i] == new_col[i + 1]:
                new_col[i] *= 2
                score += new_col[i]
                new_col[i + 1] = 0

        new_col = [i for i in new_col if i != 0]
        new_col += [0] * (num_rows - len(new_col))

        for i in range(num_rows):
            field[i][j] = new_col[i]

    return field, score


def move_down(field, score):
    num_rows = len(field)
    num_cols = len(field[0])

    for j in range(num_cols):

        col = [field[i][j] for i in range(num_rows)]

        new_col = [num for num in col if num != 0]

        for i in range(len(new_col) - 1, 0, -1):
            if new_col[i] == new_col[i - 1]:
                new_col[i] *= 2
                score += new_col[i]
                new_col[i - 1] = 0

        new_col = [0] * (num_rows - len(new_col)) + [num for num in new_col if num != 0]

        if len(new_col) != num_rows:
            new_col = [0] * (num_rows - len(new_col)) + new_col

        for i in range(num_rows):
            field[i][j] = new_col[i]

    return field, score


def _game_over(field):

    if any(0 in row for row in field):
        return False

    for row in field:
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1]:
                return False

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if field[j][i] == field[j + 1][i]:
                return False

    return True


def start_game(): 
    turns = 0

    field = _init_field()

    while True:

        _draw_field(field)
        _print_field(field)

        direction_move = input('Enter move: ').lower()

        if direction_move == 'p':
            break

        if direction_move in ['w', 'a', 's', 'd']:

            old_field = [row[:] for row in field]

            field = move(field, direction_move)

            if field != old_field: _add_tile(field)

            if _game_over(field):
                print("Game over!")

                break

            turns += 1