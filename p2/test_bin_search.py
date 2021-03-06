from bin_search import bin_search


def test_empty_array():
    assert bin_search([], 0) == 0


def test_single_present_element():
    assert bin_search([1], 1) == 1


def test_single_absent_element_greater():
    assert bin_search([3], 1) == 0


def test_single_absent_element_lesser():
    assert bin_search([0], 1) == 1


def test_middle_present_element():
    assert bin_search([1,2,3], 2) == 2


def test_right_present_element():
    assert bin_search([1,2,3], 3) == 3


def test_left_present_element():
    assert bin_search([1,2,3], 1) == 1


def test_middle_absent_element():
    assert bin_search([1,2,3,5,6,7], 4) == 3


def test_left_absent_element():
    assert bin_search([1,2,3,5,6,7], 0) == 0


def test_right_absent_element():
    assert bin_search([1,2,3,5,6,7], 8) == 6


def test_many_equal_elements_middle():
    assert bin_search([1,2,3,3,3,4,5,6], 3) == 5


def test_many_equal_elements_left():
    assert bin_search([1,1,1,1,2,3,3,3,4,5,6], 1) == 4


def test_many_equal_elements_right():
    assert bin_search([1,2,3,3,3,4,5,6,7,7,7,7], 7) == 12


def test_unsorted_array_yields_arbitrary_result():
    assert bin_search([1,6,2,3,5], 4) == 4
