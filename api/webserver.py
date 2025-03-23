from aiohttp import web, ClientSession
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, time as dt_time, timedelta

# URL trang web cần lấy dữ liệu
URL = "https://ketqua.me/xsmb-xo-so-mien-bac"
HEADERS = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
from datetime import datetime, time as dt_time, timedelta

# URL trang web cần lấy dữ liệu
URL = "https://ketqua.me/xsmb-xo-so-mien-bac"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Biến toàn cục lưu kết quả mới nhất
latest_data = {"date": "", "results": {}}
last_updated_date = None  # Ngày cập nhật cuối cùng

async def fetch_data():
    """Hàm tải dữ liệu từ trang web"""
    global latest_data, last_updated_date

    async with ClientSession() as session:
        try:
            async with session.get(URL, headers=HEADERS) as response:
                response.raise_for_status()
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            print(f"❌ Lỗi khi fetch dữ liệu: {e}")

# Biến toàn cục lưu kết quả mới nhất
latest_data = {"date": "", "results": {}}
last_updated_date = None  # Ngày cập nhật cuối cùng

async def fetch_data():
    """Hàm tải dữ liệu từ trang web"""
    global latest_data, last_updated_date

    async with ClientSession() as session:
        try:
            async with session.get(URL, headers=HEADERS) as response:
                response.raise_for_status()
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Lấy ngày xổ số
                date_text = ""
                date_div = soup.find("div", class_="title-link-item mb_date_info")
                if date_div:
                    date_links = date_div.find_all("a")
                    if len(date_links) > 2:
                        date_text = date_links[2].text.strip()

                # Lấy kết quả xổ số
                result_table = soup.find("table", id="table-22")
                results = {}

                if result_table:
                    for row in result_table.find_all("tr"):
                        cells = row.find_all(["th", "td"])
                        cell_values = [cell.text.strip() for cell in cells]

                        if cell_values and cell_values[0]:  # Bỏ qua hàng rỗng
                            results[cell_values[0]] = cell_values[1:]

                # Cập nhật dữ liệu nếu có thay đổi
                latest_data["date"] = date_text
                latest_data["results"] = results
                last_updated_date = datetime.now().date()  # Lưu ngày cập nhật

                print(f"✅ Dữ liệu đã được cập nhật vào {last_updated_date}!")
        except Exception as e:
            print(f"❌ Lỗi khi fetch dữ liệu: {e}")

async def wait_until_next_update():
    """Chờ đến 18h00 mỗi ngày để cập nhật dữ liệu"""
    global last_updated_date

    while True:
        now = datetime.now()
        next_update_time = datetime.combine(now.date(), dt_time(19, 50))  # Cập nhật lúc 18h00
        
        if now >= next_update_time:  # Nếu đã qua 18h, chờ đến 18h ngày mai
            next_update_time += timedelta(days=1)

        sleep_seconds = (next_update_time - now).total_seconds()
        print(f"🕒 Chờ {sleep_seconds / 3600:.2f} giờ đến lần cập nhật tiếp theo ({next_update_time})")

        await asyncio.sleep(sleep_seconds)  # Đợi đến thời điểm cần cập nhật
        await fetch_data()  # Cập nhật dữ liệu

async def get_date(request):
    """API trả về ngày xổ số"""
    return web.json_response({"date": latest_data["date"]})

async def get_results(request):
    """API trả về kết quả xổ số"""
    return web.json_response(latest_data["results"])

app = web.Application()
app.router.add_get('/xsmb/get_date', get_date)
app.router.add_get('/xsmb/get_results', get_results)

# Khởi động background task khi server chạy
async def on_startup(app):
    app.loop.create_task(wait_until_next_update())

app.on_startup.append(on_startup)

# Khởi động background task khi server chạy
async def on_startup(app):
    app.loop.create_task(wait_until_next_update())

app.on_startup.append(on_startup)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
    web.run_app(app, host='0.0.0.0', port=8080)
