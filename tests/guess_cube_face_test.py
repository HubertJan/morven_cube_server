from morven_cube_server.helper.guess_cube_face import calculate_edge_cube_top_sticker, StandardCubeColors, calculate_up_cube_face, StandardCubePattern, convert_pattern_string_to_standard_cube_pattern


def test_calculate_edge_cube_top_sticker():
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.FRONT, StandardCubeColors.RIGHT) == StandardCubeColors.UP
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.BACK, StandardCubeColors.DOWN) == StandardCubeColors.LEFT
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.LEFT, StandardCubeColors.BACK) == StandardCubeColors.DOWN
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.BACK, StandardCubeColors.LEFT) == StandardCubeColors.UP
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.RIGHT, StandardCubeColors.BACK) == StandardCubeColors.UP
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.DOWN, StandardCubeColors.BACK) == StandardCubeColors.RIGHT
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.UP, StandardCubeColors.FRONT) == StandardCubeColors.RIGHT
    assert calculate_edge_cube_top_sticker(
        StandardCubeColors.UP, StandardCubeColors.RIGHT) == StandardCubeColors.BACK


def test_calculate_up_cube_face():
    pattern = convert_pattern_string_to_standard_cube_pattern(
        "FLBUULFFLFDURRDBUBUUDDFFBRDDBLRDRFLLRLRULFUDRRBDBBBUFL")

    calculated_up = calculate_up_cube_face(
        pattern,
    )
    actual_up = pattern.up
    assert calculated_up.is_complete()
    assert calculated_up.top_left == actual_up.top_left
    assert calculated_up.top_right == actual_up.top_right
    assert calculated_up.bottom_left == actual_up.bottom_left
    assert calculated_up.bottom_right == actual_up.bottom_right
