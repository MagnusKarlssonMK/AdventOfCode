from day07 import CalibrationData

# ----------- Parts 1 & 2 ------------

def test_parts1_2_1() -> None:
    test_string = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''
    test_input = CalibrationData(test_string)
    p1, p2 = test_input.get_calibration_result()
    assert p1 == 3749
    assert p2 == 11387
