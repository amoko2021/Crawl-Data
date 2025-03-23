class Lottery:
    def __init__(self, date, result):
        self.date = date
        self.result = result

    def show(self):
        print(f"date : {self.date}, result : {self.result}")