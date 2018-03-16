class Beer:

    def __init__(self, name, size, style, price):
        self.name = name
        self.size = size
        self.style = style
        self.price = price

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def get_style(self):
        return self.style

    def get_price(self):
        return self.price
