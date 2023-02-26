'''
GUESS COLOR!
guess_color.py
'''

import datetime
import json
import math
import os
import random
from time import sleep
from typing import Any
from PIL import Image, ImageDraw


def input_tool(
    first_message: str,
    rule: str,
    error_message: str,
    rule_function: Any,
) -> str:
    '''
    Get valid value based on rule_function
    '''
    # notice message
    print(f'> {first_message} {rule}: ', end='')
    # first input
    input_str = input()
    # when rule_function(input_str) return false
    # since it's invalid
    while not rule_function(input_str):
        # notice again and get input
        print(f'> {error_message}')
        print(f'> {first_message} {rule}: ', end='')
        input_str = input()
    # until it's valid
    return input_str


def get_random_color():
    '''
    get random color
    '''
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return f"#{c1:02x}{c2:02x}{c3:02x}"


def get_variant_color(hex_color: str, variant: float) -> str:
    '''
    get variant color
    '''
    c1 = change_color_value(hex_color[1:3], variant)
    c2 = change_color_value(hex_color[3:5], variant)
    c3 = change_color_value(hex_color[5:7], variant)
    return f"#{c1:02x}{c2:02x}{c3:02x}"


def change_color_value(c: str, variant: float) -> int:
    '''
    change color value
    '''
    variant = int(variant)
    value = random.randint(-variant, variant)
    if 0 < value < variant / 2:
        value = int(variant / 2)
    elif -variant / 2 < value <= 0:
        value = int(-variant / 2)
    result = int(c, base=16) + value
    result = min(result, 255)
    result = max(result, 0)
    return result


def generate_image(
    h_blocks: int,
    v_blocks: int,
    main_color: str,
    variant_color: str,
    fake_h: int,
    fake_v: int,
) -> None:
    '''
    generate image
    '''

    if max(h_blocks, v_blocks) > GuessColorConstance.IMAGE_MAX_SIZE:
        raise ValueError(
            f'h_blocks ({h_blocks}) or v_blocks ({v_blocks}) is bigger than ' +
            f'IMAGE_MAX_SIZE ({GuessColorConstance.IMAGE_MAX_SIZE})')
    if min(h_blocks, v_blocks) < 2:
        raise ValueError(
            f'h_blocks ({h_blocks}) or v_blocks ({v_blocks}) is smaller than 2'
        )

    single_block_size = int(GuessColorConstance.IMAGE_MAX_SIZE / max(
        h_blocks,
        v_blocks,
    ))
    im = Image.new(
        'RGB',
        (
            single_block_size * h_blocks + h_blocks - 1,
            single_block_size * v_blocks + v_blocks - 1,
        ),
        'gray',
    )
    draw = ImageDraw.Draw(im)
    for i in range(h_blocks):
        for j in range(v_blocks):
            draw.rectangle(
                (
                    i * single_block_size + i,
                    j * single_block_size + j,
                    (i + 1) * single_block_size + i - 1,
                    (j + 1) * single_block_size + j - 1,
                ),
                variant_color if i == fake_h and j == fake_v else main_color,
            )

    del draw
    im.save('color_pic.png', 'PNG')


def show_menu() -> None:
    '''
    show menu
    '''
    print(f'Welcome to {GuessColorConstance.GUESS_COLOR_GAME_NAME}'.center(50))
    print('Menu'.center(50, '-'))
    for k, v in GuessColorConstance.INDEX_TO_FUNC_DICT.items():
        print(f'{k}. {v[0]}'.center(46).center(50, '|'))
    print(''.center(50, '-'))


def show_notice(notice: str, end_str: str, times: int = 3) -> None:
    '''
    show notice
    '''
    sleep(1.5)
    for i in notice:
        print(i, end='')
        sleep(0.1)
    for _ in range(0, times):
        print(end_str, end='')
        sleep(0.5)


def how_to_play() -> None:
    '''
    game introduction
    '''


def new_game() -> None:
    '''
    New game
    '''
    round_index = 1
    image_grid = 2
    guess_color_game = GuessColorGame()
    while True:
        h_blocks = image_grid
        v_blocks = image_grid
        fake_h = random.randint(0, image_grid - 1)
        fake_v = random.randint(0, image_grid - 1)
        main_color = get_random_color()
        variant_color = get_variant_color(
            main_color,
            16 * math.exp(-image_grid / 54),
        )
        guess_color_game.details.append(
            GuessColorGameDetail(
                main_color,
                variant_color,
                h_blocks,
                v_blocks,
                fake_h,
                fake_v,
            ))

        os.system('cls')
        print(
            f'IT\'S ROUND {round_index} NOW! It\'s {h_blocks}*{v_blocks} grid NOW!',
        )
        generate_image(
            h_blocks,
            v_blocks,
            main_color,
            variant_color,
            fake_h,
            fake_v,
        )
        if input() != 'y':
            break
        else:
            round_index += 1
            if image_grid < 16 and round_index % 3 == 0:
                image_grid *= 2
            elif image_grid < 24:
                image_grid += 1
    print(f'CONGRATULATION! YOU WON {round_index-1} TIMES!')
    guess_color_game.end_date = str(datetime.datetime.now())
    guess_color_game.won_games = round_index - 1
    save_guess_color_game(guess_color_game)
    show_notice('Backing to Menu', '.')


def history() -> None:
    '''
    show game history
    '''


def game_exit() -> None:
    '''
    exit game
    '''
    show_notice('See You Next Time', '❤️️', 1)
    exit()


class GuessColorConstance():
    '''
    save needed constance
    '''
    GUESS_COLOR_GAME_NAME: str = 'GUESS COLOR'
    INDEX_TO_FUNC_DICT = {
        '0': ['HOW TO PLAY', how_to_play],
        '1': ['New Game', new_game],
        '2': ['History', history],
        '3': ['Exit', game_exit],
    }
    IMAGE_MAX_SIZE: int = 512


class ClassEncoderHelper(json.JSONEncoder):
    '''
    json helper
    '''

    def default(self, o):
        return o.__dict__


class GuessColorGameDetail():
    '''
    save game details
    '''
    main_color: str
    variant_color: str
    h_blocks: int
    v_blocks: int
    fake_h: int
    fake_v: int

    def __init__(
        self,
        main_color: str,
        variant_color: str,
        h_blocks: int,
        v_blocks: int,
        fake_h: int,
        fake_v: int,
    ) -> None:
        self.main_color = main_color
        self.variant_color = variant_color
        self.h_blocks = h_blocks
        self.v_blocks = v_blocks
        self.fake_h = fake_h
        self.fake_v = fake_v


class GuessColorGame():
    '''
    save game info
    '''
    play_date: str
    end_date: str
    won_games: int
    details: list[GuessColorGameDetail]

    def __init__(self) -> None:
        self.play_date = str(datetime.datetime.now())
        self.end_date = ''
        self.won_games = 0
        self.details = []


def save_guess_color_game(guess_color_game: GuessColorGame):
    '''
    save guess color game to json
    '''
    with open('database.json', 'r+', encoding='utf-8') as f:
        json_list: list = json.load(f)
        json_list.append(guess_color_game)
        f.seek(0)
        f.truncate()
        f.write(json.dumps(
            json_list,
            cls=ClassEncoderHelper,
            indent=4,
        ))


if __name__ == '__main__':
    os.system('cls')

    with open('database.json', 'a+', encoding='utf-8') as f:
        f.seek(0)
        if len(f.read()) == 0:
            f.write('[]')

    show_notice(f'Welcome to {GuessColorConstance.GUESS_COLOR_GAME_NAME}', '!')
    while True:
        os.system('cls')
        show_menu()
        input_str = input_tool(
            'Please Enter Your Choose',
            rule='',
            error_message='Invalid Choose',
            rule_function=lambda input_str: input_str.strip() in
            GuessColorConstance.INDEX_TO_FUNC_DICT,
        ).strip()
        GuessColorConstance.INDEX_TO_FUNC_DICT[input_str][1]()
