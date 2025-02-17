from day07 import BagRules

TEST_STRING_1 = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''

TEST_STRING_2 = '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = BagRules(TEST_STRING_1)
    assert test_input.countcontainedin('shiny gold') == 4

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = BagRules(TEST_STRING_1)
    assert test_input.countbagscontainedin('shiny gold') == 32

def test_part2_2() -> None:
    test_input = BagRules(TEST_STRING_2)
    assert test_input.countbagscontainedin('shiny gold') == 126
