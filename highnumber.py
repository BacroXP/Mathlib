from math_lib import num

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
    e = b - a
    assert str(e) == "-111111111011111111100.0", f"Subtraction test failed: {e}"

    f = a - num(12345678901234567890)
    assert str(f) == "0.0", f"Subtraction test failed: {f}"

    # Test multiplication
    g = num(100000) * num(100000)
    assert str(g) == "10000000000.0", f"Multiplication test failed: {g}"

    h = num(-12345) * num(67890)
    assert str(h) == "-838102050.0", f"Multiplication test failed: {h}"

    # Test division
    i = num(10000000000) / num(100000)
    assert str(i) == "100000.0", f"Division test failed: {i}"

    j = num(927743737372291) / num(97531)
    assert str(j) == "9512295961.0", f"Division test failed: {j}"

    # Test rounding functions
    k = num(9)
    assert k.__ceil__(1).__str__() == "9.0", f"Ceil test failed: {k.__ceil__(1)}"
    assert k.__floor__(1).__str__() == "9.0", f"Floor test failed: {k.__floor__(1)}"
    assert k.__round__(1).__str__() == "9.0", f"Round test failed: {k.__round__(1)}"

    l = num(-9)
    assert l.__ceil__(1).__str__() == "-9.0", f"Ceil test failed: {l.__ceil__(1)}"
    assert l.__floor__(1).__str__() == "-9.0", f"Floor test failed: {l.__floor__(1)}"
    assert l.__round__(1).__str__() == "-9.0", f"Round test failed: {l.__round__(1)}"

    # Test comparisons
    assert a > b, f"Comparison test failed: {a} <= {b}"
    assert b < a, f"Comparison test failed: {b} >= {a}"
    assert a == num(12345678901234567890), f"Comparison test failed: {a} != 12345678901234567890"
    assert b != a, f"Comparison test failed: {b} == {a}"

    print("All tests passed!")


# Run the test
test_num_class()
