from curses.panel import bottom_panel
from operator import le
from re import U
import re
from cube_image_scanner.models.standard_cube_face import StandardCubeFace, StandardCubeColors
from cube_image_scanner.models.standard_cube_pattern import StandardCubePattern


def convert_standard_cube_pattern_to_pattern_string(pattern: StandardCubePattern) -> str:
    pattern_string = ""
    pattern_string += _convert_face_to_string(pattern.up)
    pattern_string += _convert_face_to_string(pattern.right)
    pattern_string += _convert_face_to_string(pattern.front)
    pattern_string += _convert_face_to_string(pattern.down)
    pattern_string += _convert_face_to_string(pattern.left)
    pattern_string += _convert_face_to_string(pattern.back)
    return pattern_string


def _convert_face_to_string(face: StandardCubeFace) -> str:
    pattern_string = ""
    for sticker in face:
        pattern_string += _convert_standard_cube_color_to_pattern_string_char(
            sticker)
    return pattern_string


def convert_pattern_string_to_standard_cube_pattern(pattern_string: str) -> StandardCubePattern:
    pattern_list = list(pattern_string)
    if len(pattern_list) != 54:
        raise Exception("Invalid pattern")
    faces: list[list[str]] = []
    for face_index in range(0, 6):
        faces.append(pattern_list[face_index*9: face_index*9+9])
    standard_faces: list[StandardCubeFace] = []
    for stickers in faces:
        standard_faces.append(StandardCubeFace(
            top_left=_convert_pattern_string_char_to_standard_cube_color(
                stickers[0]),

            top_middle=_convert_pattern_string_char_to_standard_cube_color(
                stickers[1]),

            top_right=_convert_pattern_string_char_to_standard_cube_color(
                stickers[2]),

            center_left=_convert_pattern_string_char_to_standard_cube_color(
                stickers[3]),

            center_right=_convert_pattern_string_char_to_standard_cube_color(
                stickers[5]),

            bottom_left=_convert_pattern_string_char_to_standard_cube_color(
                stickers[6]),

            bottom_middle=_convert_pattern_string_char_to_standard_cube_color(
                stickers[7]),

            bottom_right=_convert_pattern_string_char_to_standard_cube_color(
                stickers[8])
        ))
    return StandardCubePattern(
        up=standard_faces[0],
        right=standard_faces[1],
        front=standard_faces[2],
        down=standard_faces[3],
        left=standard_faces[4],
        back=standard_faces[5]
    )


def _convert_pattern_string_char_to_standard_cube_color(pattern_char: str) -> StandardCubeColors:
    match pattern_char:
        case "U":
            return StandardCubeColors.UP
        case "F":
            return StandardCubeColors.FRONT
        case "D":
            return StandardCubeColors.DOWN
        case "B":
            return StandardCubeColors.BACK
        case "L":
            return StandardCubeColors.LEFT
        case "R":
            return StandardCubeColors.RIGHT
    raise Exception("Invalid input")


def _convert_standard_cube_color_to_pattern_string_char(color: StandardCubeColors) -> str:
    match color:
        case StandardCubeColors.UP:
            return "U"
        case StandardCubeColors.FRONT:
            return "F"
        case StandardCubeColors.DOWN:
            return "D"
        case StandardCubeColors.BACK:
            return "B"
        case StandardCubeColors.LEFT:
            return "L"
        case StandardCubeColors.RIGHT:
            return "R"
    raise Exception("Invalid input")


def calculate_up_cube_face(patttern_with_missing_up: StandardCubePattern) -> StandardCubeFace:
    if not (patttern_with_missing_up.left.is_complete() and patttern_with_missing_up.right.is_complete() and patttern_with_missing_up.front.is_complete() and patttern_with_missing_up.back.is_complete() and patttern_with_missing_up.down.is_complete()):
        raise Exception("All faces apart from Up face have to be complete.")
    bottom_right_sticker = calculate_edge_cube_top_sticker(
        patttern_with_missing_up.front.top_right, patttern_with_missing_up.right.top_left)  # type: ignore
    top_right_sticker = calculate_edge_cube_top_sticker(
        patttern_with_missing_up.right.top_right, patttern_with_missing_up.back.top_left)  # type: ignore
    top_left_sticker = calculate_edge_cube_top_sticker(
        patttern_with_missing_up.back.top_right, patttern_with_missing_up.left.top_left)  # type: ignore
    bottom_left_sticker = calculate_edge_cube_top_sticker(
        patttern_with_missing_up.left.top_right, patttern_with_missing_up.front.top_left)  # type: ignore
    up_face = StandardCubeFace(
        top_left=top_left_sticker,
        top_right=top_right_sticker,
        bottom_left=bottom_left_sticker,
        bottom_right=bottom_right_sticker,
        bottom_middle=None,
        center_left=None,
        center_right=None,
        top_middle=None,
    )
    pattern = patttern_with_missing_up.clone(up=up_face)
    missing_sticker = calculate_missing_sticker(pattern)
    guessed_colors: list[StandardCubeColors] = []
    while len(guessed_colors) != 4:
        for color in missing_sticker.keys():
            if len(guessed_colors) == 4:
                continue
            if missing_sticker[color] == 0:
                continue
            missing_sticker[color] -= 1
            guessed_colors.append(color)
    complete_up_face = StandardCubeFace(
        top_left=top_left_sticker,
        top_right=top_right_sticker,
        bottom_left=bottom_left_sticker,
        bottom_right=bottom_right_sticker,
        bottom_middle=guessed_colors[0],
        center_left=guessed_colors[1],
        center_right=guessed_colors[2],
        top_middle=guessed_colors[3]
    )
    return complete_up_face


def calculate_missing_sticker(pattern: StandardCubePattern) -> dict[StandardCubeColors, int]:
    color_counter = calculate_total_sticker_of_each_color(pattern)
    missing_colors = {}
    for key, value in color_counter.items():
        if key is None:
            continue
        if value < 8:
            missing_colors[key] = 8 - value
    return missing_colors


def calculate_total_sticker_of_each_color(pattern: StandardCubePattern) -> dict[StandardCubeColors, int]:
    total_counter = {}
    for face in pattern:
        counter = count_colors(face)
        for key, value in counter.items():
            if not key in total_counter:
                total_counter[key] = 0
            total_counter[key] += value
    for color in StandardCubeColors:
        if not color in total_counter:
            total_counter[color] = 0
    return total_counter


def count_colors(face: StandardCubeFace) -> dict[StandardCubeColors, int]:
    counter = {}
    for sticker in face:
        if sticker not in counter:
            counter[sticker] = 0
        counter[sticker] += 1
    return counter


def calculate_edge_cube_top_sticker(front_sticker: StandardCubeColors, right_sticker: StandardCubeColors) -> StandardCubeColors:
    a = _get_value(front_sticker)
    b = _get_value(right_sticker)
    c0 = _get_missing_number(a[0], b[0])
    is_increasing = (b[0] < c0 and not (b[0] == 0 and c0 == 2)
                     ) or (b[0] == 2 and c0 == 0)
    should_value_change = (a[1] == 0 and is_increasing) or (
        a[1] == 1 and not is_increasing)
    c = (c0, not b[1] if should_value_change else b[1])
    return _get_color_of_value(c)


def _get_missing_number(a: int, b: int) -> int:
    if a > 2 or b > 2 or a < 0 or b < 0:
        raise Exception("Numbers have to be 0, 1 or 2.")
    if a != 0 and b != 0:
        return 0
    if a != 1 and b != 1:
        return 1
    return 2


_x_colors = [StandardCubeColors.LEFT, StandardCubeColors.RIGHT]
_y_colors = [StandardCubeColors.UP, StandardCubeColors.DOWN]
_z_colors = [StandardCubeColors.FRONT, StandardCubeColors.BACK]


def _get_value(color: StandardCubeColors) -> tuple[int, bool]:
    if color in _x_colors:
        return (0, _x_colors.index(color) == 1)
    if color in _y_colors:
        return (1, _y_colors.index(color) == 1)
    if color in _z_colors:
        return (2, _z_colors.index(color) == 1)
    raise Exception()


def _get_color_of_value(value: tuple[int, bool]) -> StandardCubeColors:
    match(value[0]):
        case 0:
            return _x_colors[1 if value[1] else 0]
        case 1:
            return _y_colors[1 if value[1] else 0]
        case 2:
            return _z_colors[1 if value[1] else 0]
    raise Exception
