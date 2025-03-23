from aiohttp import web
import json
from bs4 import BeautifulSoup
import requests

url = "https://ketqua.me/xsmb-xo-so-mien-bac"
# Giả lập User-Agent để tránh bị chặn
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
# Gửi yêu cầu HTTP GET đến trang web
response = requests.get(url, headers=headers)
response.encoding = "utf-8"  # Đặt mã hóa sang UTF-8
response.raise_for_status()  # Kiểm tra lỗi HTTP
# Phân tích HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

async def get_date(request):
    date_text = ""
    # Tìm thẻ <div> có class "title-link-item mb_date_info"
    date_div = soup.find("div", class_="title-link-item mb_date_info")

    # Kiểm tra nếu tìm thấy
    if date_div:
        date_link = date_div.find_all("a")  # Tìm thẻ <a> bên trong <div>
        
        if date_link:
            date_text = date_link[2].text.strip()  # Lấy nội dung văn bản bên trong <a>
            #print("✅ Ngày xổ số:", date_text)
        else:
            print("❌ Không tìm thấy thẻ <a> bên trong .title-link-item mb_date_info")
    else:
        print("❌ Không tìm thấy thẻ <div> với class 'title-link-item mb_date_info'")

    return web.json_response(data=date_text)

async def get_results(request):
    # Tìm bảng có id="table-22"
    table = soup.find("table", id="table-22")

    # Tạo dictionary để lưu dữ liệu
    result = {}

    # Kiểm tra nếu bảng tồn tại
    if table:
        # Lấy tất cả các hàng trong bảng
        rows = table.find_all("tr")

        # Duyệt qua từng hàng
        for row in rows:
            # Lấy tất cả các ô trong hàng (cả <th> và <td>)
            cells = row.find_all(["th", "td"])

            # Lấy nội dung của từng ô và loại bỏ khoảng trắng thừa
            cell_values = [cell.text.strip() for cell in cells]

            if(cell_values[0] == ""):
                continue

            # Nếu danh sách có ít nhất 2 phần tử (tên giải + số)
            if len(cell_values) >= 2:
                # Lưu vào dictionary (tách số bằng khoảng trắng)
                result[cell_values[0]] = cell_values[1].split()  
    else:
        print("❌ Không tìm thấy bảng với id='table-22'")

    return web.json_response(result)

app = web.Application()
app.router.add_get('/xsmb/get_date', get_date)
app.router.add_get('/xsmb/get_results', get_results)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
