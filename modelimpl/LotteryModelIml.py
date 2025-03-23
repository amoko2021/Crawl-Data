from bs4 import BeautifulSoup
import requests
from model.Lottery import Lottery
import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

class LotteryModelIml():   
    def __init__(self):
        self.api_base_url = os.getenv("URL")
        # Lấy ngày từ API
        date_response = requests.get(f"{self.api_base_url}/get_date")
        self.date = date_response.json()     
        # Lấy kết quả từ API
        results_response = requests.get(f"{self.api_base_url}/get_results")
        self.results = results_response.json()


    def get_data(self):

        return Lottery(self.date, self.results)

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