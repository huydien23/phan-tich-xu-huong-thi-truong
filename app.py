from flask import Flask, render_template, request, redirect, url_for, flash
from phan_tich_cam_xuc import PhanTichCamXucTaiChinh
import os

app = Flask(__name__)
app.secret_key = 'xu_huong_thi_truong_secret_key'

# Đảm bảo thư mục static tồn tại
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Lấy danh sách URLs từ form
        urls_text = request.form.get('urls', '')
        raw_urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        # Kiểm tra xem có URL nào được nhập không
        if not raw_urls:
            flash('Vui lòng nhập ít nhất một URL tin tức!', 'error')
            return redirect(url_for('index'))
        
        # Khởi tạo phân tích cảm xúc
        analyzer = PhanTichCamXucTaiChinh()
        
        # Thu thập và phân tích tin tức
        results = []
        tich_cuc_list = []
        tieu_cuc_list = []
        tong_diem = 0
        urls_thanh_cong = 0
        
        for url in raw_urls:
            try:
                # Chuẩn hóa URL
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                # Lấy nội dung từ URL
                tieu_de, noi_dung = analyzer.lay_tin_tuc(url)
                
                if not tieu_de or not noi_dung:
                    results.append({
                        'url': url,
                        'tieu_de': 'Không thể truy cập hoặc phân tích URL này',
                        'trang_thai': 'error',
                        'diem': 0
                    })
                    continue
                
                # Phân tích cảm xúc
                sentiment, so_tu_tich_cuc, so_tu_tieu_cuc, diem = analyzer.phan_tich_cam_xuc(tieu_de + " " + noi_dung)
                
                # Lưu kết quả
                tich_cuc_list.append(so_tu_tich_cuc)
                tieu_cuc_list.append(so_tu_tieu_cuc)
                tong_diem += diem
                urls_thanh_cong += 1
                
                # Thêm vào kết quả
                results.append({                                                              
                    'url': url,           
                    'tieu_de': tieu_de[:100] + '...' if len(tieu_de) > 100 else tieu_de,
                    'sentiment': sentiment,
                    'so_tu_tich_cuc': so_tu_tich_cuc,
                    'so_tu_tieu_cuc': so_tu_tieu_cuc,
                    'diem': diem,
                    'trang_thai': 'success'
                })
            except Exception as e:
                print(f"Lỗi khi xử lý URL {url}: {str(e)}")
                results.append({
                    'url': url,
                    'tieu_de': f'Lỗi: {str(e)[:50]}...' if len(str(e)) > 50 else f'Lỗi: {str(e)}',
                    'trang_thai': 'error',
                    'diem': 0
                })
        
        # Kiểm tra nếu không có URL nào thành công
        if urls_thanh_cong == 0:
            flash('Không thể phân tích tất cả các URL được cung cấp! Vui lòng kiểm tra và thử lại.', 'error')
            return redirect(url_for('index'))
        
        # Tính điểm trung bình chỉ từ các URL thành công
        diem_trung_binh = tong_diem / urls_thanh_cong
        
        # Vẽ biểu đồ và dự đoán xu hướng
        try:
            if tich_cuc_list and tieu_cuc_list:
                analyzer.ve_bieu_do_so_sanh(tich_cuc_list, tieu_cuc_list)
                xu_huong, ket_luan = analyzer.du_doan_xu_huong(diem_trung_binh)
            else:
                xu_huong = "KHÔNG XÁC ĐỊNH ❓"
                ket_luan = "Không đủ dữ liệu để phân tích xu hướng"
        except Exception as chart_error:
            print(f"Lỗi khi tạo biểu đồ: {str(chart_error)}")
            xu_huong = "KHÔNG XÁC ĐỊNH ❓"
            ket_luan = f"Lỗi khi tạo biểu đồ phân tích: {str(chart_error)}"
        
        return render_template('results.html', 
                               results=results, 
                               diem_trung_binh=diem_trung_binh, 
                               xu_huong=xu_huong, 
                               ket_luan=ket_luan,
                               thanh_cong=urls_thanh_cong,
                               tong_urls=len(raw_urls))
    except Exception as e:
        flash(f'Đã xảy ra lỗi: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
