# Создать класс Book с аттрибутами price, author, name.
# Автор и название книги не должны меняться.(Выкидываем ValueError)
# Цена может меняться, но должна находится в пределах: 0 < price <= 100


class PriceControl:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if value <= 0 or value > 100:
            raise ValueError
        instance.__dict__[self.name] = value

class NameControl:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if instance.__dict__.get(self.name):
            raise ValueError
        instance.__dict__[self.name] = value

class Book:
    author = NameControl()
    name = NameControl()
    price = PriceControl()

    def __init__(self, author, name, price):
        self.author = author
        self.name = name
        self.price = price
