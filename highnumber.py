from math_lib import num, pi, e, i

def test_num_class() -> None:
    """
    Test function for the `num` class. Validates basic arithmetic, comparisons, and edge cases.
    """
    print("Testing the `num` class...")

    # Test initialization and string representation
    a = num(12345678901234567890)
    b = num(-98765432109876543210)
    assert str(a) == "12345678901234567890.0", f"Init test failed: {a}"
    assert str(b) == "-98765432109876543210.0", f"Init test failed: {b}"

    # Test addition
    c = a + b
    assert str(c) == "-86419753208641975320.0", f"Addition test failed: {c}"

    d = a + num(11111111111111111111)
    assert str(d) == "23456790012345679001.0", f"Addition test failed: {d}"

    # Test subtraction
    _e = b - a
    assert str(_e) == "-111111111011111111100.0", f"Subtraction test failed: {_e}"

    f = a - num(12345678901234567890)
    assert str(f) == "0.0", f"Subtraction test failed: {f}"

    # Test multiplication
    g = num(100000) * num(100000)
    assert str(g) == "10000000000.0", f"Multiplication test failed: {g}"

    h = num(-12345) * num(67890)
    assert str(h) == "-838102050.0", f"Multiplication test failed: {h}"

    # Test division
    _i = num(10000000000) / num(100000)
    assert str(_i) == "100000.0", f"Division test failed: {_i}"

    j = num(927743737372291) / num(97531)
    assert str(j) == "9512295961.0", f"Division test failed: {j}"

    # Test rounding functions
    k = num(9)
    assert k.__ceil__(1).__str__() == "9.0", f"Ceil test failed: {k.__ceil__(1)}"
    assert k.__floor__(1).__str__() == "9.0", f"Floor test failed: {k.__floor__(1)}"
    assert k.__round__(1).__str__() == "9.0", f"Round test failed: {k.__round__(1)}"

    _l = num(-9)
    assert _l.__ceil__(1).__str__() == "-9.0", f"Ceil test failed: {_l.__ceil__(1)}"
    assert _l.__floor__(1).__str__() == "-9.0", f"Floor test failed: {_l.__floor__(1)}"
    assert _l.__round__(1).__str__() == "-9.0", f"Round test failed: {_l.__round__(1)}"

    # Test comparisons
    assert a > b, f"Comparison test failed: {a} <= {b}"
    assert b < a, f"Comparison test failed: {b} >= {a}"
    assert a == num(12345678901234567890), f"Comparison test failed: {a} != 12345678901234567890"
    assert b != a, f"Comparison test failed: {b} == {a}"
    
    # Complex numbers
    assert pi() == num(3.1415926535), f"Pi init failed: {pi()}"
    assert e() == num(3.7182818284), f"E init failed: {e()}"
    
    # Imaginary numbers
    assert i() * i() == num(-1), f"Not correctly solved: {i() * i()}"
    assert i() ** 4 == num(1), f"Not correctly solved: {i() ** 4}"

    print("All tests passed!")


# Run the test
test_num_class()
