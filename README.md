# Demo Data Dashboard

Dashboard Python dùng Streamlit. Hỗ trợ tải CSV/Excel, lọc dữ liệu, KPI, biểu đồ và xuất CSV.

## Chạy trên máy
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run app.py
```

## Deploy miễn phí lên Streamlit Community Cloud
1. Tạo repository GitHub mới.
2. Upload `app.py` và `requirements.txt` (có thể upload cả README).
3. Mở https://share.streamlit.io/ và đăng nhập bằng GitHub.
4. Chọn Create app, repository, branch `main`, file `app.py`.
5. Chọn Deploy.

## Định dạng CSV/Excel
Các cột bắt buộc: `Ngày`, `Danh mục`, `Lượt truy cập`, `Chuyển đổi`, `Chi phí`.

Ví dụ:
```csv
Ngày,Danh mục,Lượt truy cập,Chuyển đổi,Chi phí
2026-01-01,SEO,1200,24,300000
2026-02-01,Content,900,18,180000
```

Lưu ý: Đây là demo không có đăng nhập và không lưu dữ liệu tải lên lâu dài. Không dùng dữ liệu cá nhân/nhạy cảm.
