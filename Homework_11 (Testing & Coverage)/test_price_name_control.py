import pytest
from price_name_control import Book


def test_price_control_max():
    b = Book("William Faulkner", "The Sound and the Fury", 100)
    assert b.price == 100

def test_price_control_max_negative():
    with pytest.raises(ValueError) as e:
        Book("William Faulkner", "The Sound and the Fury", 101)

def test_price_control_min():
    b = Book("William Faulkner", "The Sound and the Fury", 1)
    assert b.price == 1

def test_price_control_min_negative():
    with pytest.raises(ValueError) as e:
        Book("William Faulkner", "The Sound and the Fury", 0)

def test_name_control_author():
    b = Book("William Faulkner", "The Sound and the Fury", 12)
    assert b.author == "William Faulkner"

def test_name_control_author_negative():
    with pytest.raises(ValueError) as e:
        b = Book("William Faulkner", "The Sound and the Fury", 12)
        b.author = "Hans Fallada"

def test_name_control_bookname():
    b = Book("William Faulkner", "The Sound and the Fury", 12)
    assert b.name == "The Sound and the Fury"

def test_name_control_bookname_negative():
    with pytest.raises(ValueError) as e:
        b = Book("William Faulkner", "The Sound and the Fury", 12)
        b.name = "Wolf unter Woelfen"
