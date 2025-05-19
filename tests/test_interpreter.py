from src.interpreter import interpret


def test_print():
    interpret("examples/hello.joy")
