from json_csv_compare.backend.compare import compare_lines


def test_simple_compare():
    lines1 = ["hello"]
    lines2 = ["hello"]
    missing, new, changed = compare_lines(lines1, lines2)
    assert len(missing) == 0
    assert len(new) == 0
    assert len(changed) == 0


def test_simple_compare_new():
    lines1 = ["hello"]
    lines2 = ["hello", "world"]
    missing, new, changed = compare_lines(lines1, lines2)
    assert len(missing) == 0
    assert len(new) == 1
    assert len(changed) == 0

def test_simple_compare_missing():
    lines2 = ["hello"]
    lines1 = ["hello", "world"]
    missing, new, changed = compare_lines(lines1, lines2)
    assert len(missing) == 1
    assert len(new) == 0
    assert len(changed) == 0

def test_simple_compare_changed():
    lines1 = ["hello"]
    lines2 = ["hello world"]
    missing, new, changed = compare_lines(lines1, lines2)
    assert len(missing) == 0
    assert len(new) == 0
    assert len(changed) == 1

if __name__ == "__main__":
    test_simple_compare_new()