class LotteryResult:
    def __init__(self, date, results):
        self.date = date
        self.results = results
    
    def get_prize(self, prize_name):
        return self.results.get(prize_name, [])
    
    def check_number(self, number):
        """Kiểm tra xem số có trúng thưởng không"""
        for prize, numbers in self.results.items():
            if number in numbers:
                return f"Số {number} trúng {prize}"
        return f"Số {number} không trúng thưởng"
    
    def display_results(self):
        print(f"Kết quả xổ số ngày {self.date}:")
        for prize, numbers in self.results.items():
            print(f"{prize}: {', '.join(numbers)}")


# Dữ liệu mẫu
data = {
    "date": "3/22/2025",
    "results": {
        "ĐB": ["67411"],
        "G.1": ["76269"],
        "G.2": ["09566", "70821"],
        "G.3": ["29974", "44691", "53443", "48589", "71026", "30438"],
        "G.4": ["9683", "2509", "1563", "5848"],
        "G.5": ["5399", "4431", "0701", "0461", "2014", "0170"],
        "G.6": ["106", "938", "486"],
        "G.7": ["06", "51", "15", "09"]
    }
}

# Tạo đối tượng LotteryResult
lottery = LotteryResult(data["date"], data["results"])

# Hiển thị kết quả
lottery.display_results()

# Kiểm tra số có trúng không
print(lottery.check_number("67411"))  # Kiểm tra số đặc biệt
print(lottery.check_number("12345"))  # Kiểm tra số không trúng
