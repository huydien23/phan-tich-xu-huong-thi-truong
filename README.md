# Phân tích cảm xúc tin tức tài chính

Chương trình này phân tích cảm xúc từ tin tức tài chính tiếng Việt để dự đoán xu hướng thị trường.

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Tính năng

- Thu thập tin tức tài chính từ các nguồn trực tuyến
- Phân tích cảm xúc văn bản tiếng Việt
- Tính toán điểm cảm xúc tổng hợp
- Dự đoán xu hướng thị trường
- Vẽ biểu đồ xu hướng cảm xúc theo thời gian

## Sử dụng

### Chạy ứng dụng web:
```bash
python app.py
```

Sau đó, mở trình duyệt và truy cập địa chỉ: http://localhost:5000

Để phân tích xu hướng:
1. Dán các URL tin tức tài chính vào ô văn bản (mỗi URL một dòng)
2. Nhấn nút "Phân tích"
3. Xem kết quả phân tích và dự đoán xu hướng

### Sử dụng từ dòng lệnh:
```bash
python phan_tich_cam_xuc.py
```

## Kết quả

- Điểm cảm xúc tổng hợp từ -1 đến 1
- Dự đoán xu hướng: TĂNG 📈, GIẢM 📉, hoặc ĐI NGANG ↔️
- Biểu đồ xu hướng được lưu trong file 'bieu_do_so_sanh.png' trong thư mục static

## Xử lý lỗi thường gặp

- Nếu gặp lỗi khi phân tích URL, hãy kiểm tra định dạng URL và đảm bảo website có thể truy cập được
- Nếu gặp lỗi "metadata-generation-failed" khi cài đặt, hãy kiểm tra định dạng của file requirements.txt. File này phải là văn bản thuần túy không chứa comments kiểu code (//), chỉ chứa tên gói và phiên bản.
- Đảm bảo môi trường Python của bạn tương thích với các phiên bản thư viện được liệt kê.
