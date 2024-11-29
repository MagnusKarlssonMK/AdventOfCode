from day09 import Stream

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Stream("{}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 1

def test_part1_2() -> None:
    test_input = Stream("{{{}}}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 6

def test_part1_3() -> None:
    test_input = Stream("{{},{}}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 5

def test_part1_4() -> None:
    test_input = Stream("{{{},{},{{}}}}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 16

def test_part1_5() -> None:
    test_input = Stream("{<a>,<a>,<a>,<a>}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 1

def test_part1_6() -> None:
    test_input = Stream("{{<ab>},{<ab>},{<ab>},{<ab>}}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 9

def test_part1_7() -> None:
    test_input = Stream("{{<!!>},{<!!>},{<!!>},{<!!>}}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 9

def test_part1_8() -> None:
    test_input = Stream("{{<a!>},{<a!>},{<a!>},{<ab>}}")
    p1, _ = test_input.get_score_and_garbage()
    assert p1 == 3

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Stream("<>")
    _, p2 = test_input.get_score_and_garbage()
    assert p2 == 0

def test_part2_2() -> None:
    test_input = Stream("<random characters>")
    _, p2 = test_input.get_score_and_garbage()
    assert p2 == 17

def test_part2_3() -> None:
    test_input = Stream("<<<<>")
    _, p2 = test_input.get_score_and_garbage()
    assert p2 == 3

def test_part2_4() -> None:
    test_input = Stream("<{!>}>")
    _, p2 = test_input.get_score_and_garbage()
    assert p2 == 2

def test_part2_5() -> None:
    test_input = Stream("<!!>")
    _, p2 = test_input.get_score_and_garbage()
    assert p2 == 0

def test_part2_6() -> None:
    test_input = Stream("<!!!>>")
    _, p2 = test_input.get_score_and_garbage()
    assert p2 == 0

def test_part2_7() -> None:
    test_input = Stream("<{o\"i!a,<{i<a>")
    _, p2 = test_input.get_score_and_garbage()
    assert p2 == 10
