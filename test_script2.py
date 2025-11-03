from script2 import add

def test_add():
    assert add(20, 20) == 40
def test_add_fail():
    assert add(5, 5) == 11
