class Letter:
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time):
        self.data_wyslania = data_wyslania     # 0
        self.data_dotarcia = data_dotarcia     # 1
        self.miejsce_wysylki = miejsce_wysylki # 2 
        self.miejsce_celu = miejsce_celu       # 3
        self.typ = typ                         # 4
        self.numer_przesylki = numer_przesylki # 5
        self.ilosc_dni_roboczych = ilosc_dni_roboczych # 6
        self.on_time = on_time # 0 - late, 1 - on time, 2 - unknown

    def self_print(self):
        print(self.data_wyslania)
        print(self.data_dotarcia)
        print(self.miejsce_wysylki)
        print(self.miejsce_celu)
        print(self.typ)
        print(self.numer_przesylki)
        print(self.on_time)
        print(self.ilosc_dni_roboczych)
        print("-------------------------------")

    def to_dict(self):
        return {
            'data_wyslania': self.data_wyslania,
            'data_dotarcia': self.data_dotarcia,
            'ilosc_dni_roboczych': self.ilosc_dni_roboczych,
            'czy_na_czas': self.on_time,
            'typ': self.typ,
            'numer_przesylki': self.numer_przesylki,
            'miejsce_wysylki': self.miejsce_wysylki,
            'miejsce_celu': self.miejsce_celu
        }
    def to_file(self):
        line = str(self.data_wyslania) + ';' + str(self.data_dotarcia)  + ';' + str(self.miejsce_wysylki) + ';' + str(self.miejsce_celu) + ';' + str(self.typ) + ';' + str(self.numer_przesylki) + ';' + str(self.on_time) + ';' + str(self.ilosc_dni_roboczych)
        return line


class Letter_ext(Letter):
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time, dystans, czas):
        super().__init__(data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time)
        self.dystans = dystans
        self.czas = czas

    def self_print(self):
        print("-------------------------------")
        print(self.data_wyslania)
        print(self.data_dotarcia)
        print(self.miejsce_wysylki)
        print(self.miejsce_celu)
        print(self.typ)
        print(self.numer_przesylki)
        print(self.on_time)
        print(self.ilosc_dni_roboczych)
        print(self.dystans)
        print(self.czas)
        print("-------------------------------")

    def to_dict(self):
        return {
            'data_wyslania': self.data_wyslania,
            'data_dotarcia': self.data_dotarcia,
            'ilosc_dni_roboczych': self.ilosc_dni_roboczych,
            'czy_na_czas': self.on_time,
            'typ': self.typ,
            'numer_przesylki': self.numer_przesylki,
            'miejsce_wysylki': self.miejsce_wysylki,
            'miejsce_celu': self.miejsce_celu,
            'dystans': self.dystans,
            'czas': self.czas
        }

    def to_file(self):
        line = str(self.data_wyslania) + ';' + str(self.data_dotarcia)  + ';' + str(self.miejsce_wysylki) + ';' + str(self.miejsce_celu) + ';' + str(self.typ) + ';' + str(self.numer_przesylki) + ';' + str(self.on_time) + ';' + str(self.ilosc_dni_roboczych) + ';' + str(self.dystans) + ';' + str(self.czas)
        return line
