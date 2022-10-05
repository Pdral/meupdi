import time


class Cacto:

    def __init__(self):
        self.agua_min = 1
        self.agua = 3
        self.luz_min = 2
        self.temp_min = 25
        self.temp_max = 32
        self.viva = True
        self.perigo_agua = 0
        self.perigo_luz = 0
        self.perigo_temp = 0
        self.name = 'Cacto'

    def consome_agua(self):
        while self.agua > 0:
            self.agua -= 1
            time.sleep(10)

    def regar(self):
        self.agua = 5

    def verifica_ambiente(self, luz_amb, temp_amb):
        if self.agua < self.agua_min:
            self.perigo_agua += 1
        else:
            self.perigo_agua = 0
        if luz_amb < self.luz_min:
            self.perigo_luz += 1
        else:
            self.perigo_luz = 0
        if temp_amb not in [range(self.temp_min, self.temp_max)]:
            self.perigo_temp += 1
        else:
            self.perigo_temp = 0
        if self.perigo_agua+self.perigo_luz+self.perigo_temp > 9:
            self.viva = False

    def cria_dict(self):
        data = {'agua': self.agua, 'agua_min': self.agua_min, 'luz': self.luz_min,
                'temp_min': self.temp_min, 'temp_max': self.temp_max, 'name': self.name}
        return data