
class PalOption:
    def __init__(self, pal_id, name):
        self.pal_id = pal_id
        self.name = name

    def __str__(self):
        return f'{self.pal_id} {self.name}'
