import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class PhanTichCamXucTaiChinh:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Từ điển cảm xúc với trọng số
        self.tu_dien_tich_cuc = {
            # Xu hướng tăng mạnh
            'tăng mạnh': 2.0, 'bứt phá': 2.0, 'đột phá': 2.0, 'tăng vọt': 2.0, 'bùng nổ': 2.0,
            'kỷ lục': 2.0, 'vượt trội': 2.0, 'tăng kịch trần': 2.0, 'thăng hoa': 2.0,
            
            # Tín hiệu tích cực
            'tăng': 1.0, 'lãi': 1.0, 'lợi nhuận': 1.0, 'tích cực': 1.0, 'phát triển': 1.0,
            'cải thiện': 1.0, 'triển vọng': 1.0, 'kỳ vọng': 1.0, 'ổn định': 1.0,
            'tích lũy': 1.0, 'dòng tiền': 1.0, 'thanh khoản tốt': 1.0, 'khối ngoại mua': 1.5,
            
            # Tín hiệu thị trường
            'vượt đỉnh': 1.5, 'điểm cản': 1.0, 'hỗ trợ mạnh': 1.0, 'xu hướng tăng': 1.5,
            'đáy': 1.0, 'tạo đáy': 1.0, 'vùng tích lũy': 1.0, 'breakout': 1.5
        }
        
        self.tu_dien_tieu_cuc = {
            # Xu hướng giảm mạnh
            'giảm mạnh': -2.0, 'sụt giảm': -2.0, 'lao dốc': -2.0, 'giảm sàn': -2.0,
            'bán tháo': -2.0, 'đổ vỡ': -2.0, 'khủng hoảng': -2.0, 'giảm kịch sàn': -2.0,
            
            # Tín hiệu tiêu cực
            'giảm': -1.0, 'lỗ': -1.0, 'thua lỗ': -1.0, 'tiêu cực': -1.0, 'rủi ro': -1.0,
            'khó khăn': -1.0, 'bất ổn': -1.0, 'lo ngại': -1.0, 'căng thẳng': -1.0,
            'áp lực': -1.0, 'khối ngoại bán': -1.5, 'thanh khoản thấp': -1.0,
            
            # Tín hiệu thị trường
            'vỡ nợ': -2.0, 'điều chỉnh': -1.0, 'test đáy': -1.0, 'xu hướng giảm': -1.5,
            'đảo chiều': -1.0, 'gap down': -1.5, 'margin call': -2.0, 'cắt lỗ': -1.5
        }
        
    def lay_tin_tuc(self, url):
        """Lấy nội dung tin tức từ URL"""
        try:
            # Kiểm tra URL có hợp lệ không
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            print(f"Đang phân tích URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # Kiểm tra tình trạng phản hồi
            if response.status_code != 200:
                print(f"Lỗi tình trạng HTTP {response.status_code} từ URL: {url}")
                return "", ""
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Xử lý theo từng trang web
            if 'cafef.vn' in url:
                tieu_de = soup.find('h1', class_='title').text.strip() if soup.find('h1', class_='title') else ""
                noi_dung = soup.find('div', class_='detail-content').text.strip() if soup.find('div', class_='detail-content') else ""
            
            elif 'vnexpress.net' in url:
                tieu_de = soup.find('h1', class_='title-detail').text.strip() if soup.find('h1', class_='title-detail') else ""
                noi_dung = soup.find('article', class_='fck_detail').text.strip() if soup.find('article', class_='fck_detail') else ""
            
            elif 'theleader.vn' in url:
                tieu_de = soup.find('h1', class_='article-title').text.strip() if soup.find('h1', class_='article-title') else ""
                noi_dung = soup.find('div', class_='article-content').text.strip() if soup.find('div', class_='article-content') else ""
            
            elif 'tinnhanhchungkhoan.vn' in url:
                tieu_de = soup.find('h1', class_='title').text.strip() if soup.find('h1', class_='title') else ""
                noi_dung = soup.find('div', class_='article-body').text.strip() if soup.find('div', class_='article-body') else ""
            
            elif 'ndh.vn' in url:
                tieu_de = soup.find('h1', class_='title-detail').text.strip() if soup.find('h1', class_='title-detail') else ""
                noi_dung = soup.find('div', class_='fck_detail').text.strip() if soup.find('div', class_='fck_detail') else ""
            
            else:
                # Mặc định cho các trang khác - cải thiện khả năng phát hiện
                tieu_de = ""
                noi_dung = ""
                
                # Tìm tiêu đề
                title_tags = soup.find_all(['h1', 'h2'], class_=['title', 'article-title', 'post-title', 'entry-title'])
                for tag in title_tags:
                    if len(tag.text.strip()) > 10:
                        tieu_de = tag.text.strip()
                        break
                
                if not tieu_de and soup.find('h1'):
                    tieu_de = soup.find('h1').text.strip()
                
                # Tìm nội dung
                content_divs = soup.find_all(['div', 'article'], class_=['content', 'article-content', 'post-content', 'entry-content', 'detail'])
                for div in content_divs:
                    content = div.text.strip()
                    if len(content) > 200:
                        noi_dung = content
                        break
                
                if not noi_dung:
                    noi_dung = ''.join([p.text.strip() for p in soup.find_all('p') if len(p.text.strip()) > 20])
            
            # Lọc bỏ các ký tự đặc biệt và chuẩn hóa nội dung
            tieu_de = ' '.join(tieu_de.split())
            noi_dung = ' '.join(noi_dung.split())
            
            # Kiểm tra nội dung có hợp lệ
            if len(tieu_de) < 5 or len(noi_dung) < 100:
                print(f"Nội dung không đủ từ URL: {url}. Tiêu đề ({len(tieu_de)} ký tự), Nội dung ({len(noi_dung)} ký tự)")
                return "", ""
                
            print(f"Phân tích thành công URL: {url}. Tiêu đề: {tieu_de[:30]}...")
            return tieu_de, noi_dung
            
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối khi truy cập {url}: {str(e)}")
            return "", ""
        except Exception as e:
            print(f"Lỗi khi lấy tin tức từ {url}: {str(e)}")
            return "", ""
# Thuật toán lexicon based
    def phan_tich_cam_xuc(self, van_ban):
        """Phân tích cảm xúc của văn bản sử dụng từ điển có trọng số"""
        van_ban = van_ban.lower()
        diem_tich_cuc = 0
        diem_tieu_cuc = 0
        so_tu_tich_cuc = 0
        so_tu_tieu_cuc = 0
        
        # Tính điểm có trọng số
        for tu, trong_so in self.tu_dien_tich_cuc.items():
            if tu in van_ban:
                diem_tich_cuc += trong_so
                so_tu_tich_cuc += 1
        
        for tu, trong_so in self.tu_dien_tieu_cuc.items():
            if tu in van_ban:
                diem_tieu_cuc += abs(trong_so)  
                so_tu_tieu_cuc += 1
        
        # Tính điểm tổng hợp
        diem_tong_hop = diem_tich_cuc - diem_tieu_cuc
        
        # Xác định mức độ cảm xúc
        if diem_tong_hop > 3:
            sentiment = 'very_positive'
        elif diem_tong_hop > 1:
            sentiment = 'positive'
        elif diem_tong_hop < -3:
            sentiment = 'very_negative'
        elif diem_tong_hop < -1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return sentiment, so_tu_tich_cuc, so_tu_tieu_cuc, diem_tong_hop
# Tính trọng số thời gian
    def tinh_diem_cam_xuc(self, danh_sach_tin):
        """Tính điểm cảm xúc tổng hợp từ danh sách tin tức với trọng số thời gian"""
        tong_diem = 0
        tong_trong_so = 0
        
        for i, tin in enumerate(danh_sach_tin):
            # Tin mới hơn có trọng số cao hơn
            trong_so = 1 + (i / len(danh_sach_tin))
            _, _, _, diem = self.phan_tich_cam_xuc(tin)
            
            tong_diem += diem * trong_so
            tong_trong_so += trong_so
        
        return tong_diem / tong_trong_so if tong_trong_so > 0 else 0

    def du_doan_xu_huong(self, diem_cam_xuc):
        """Dự đoán xu hướng thị trường và đưa ra khuyến nghị giao dịch"""
        if diem_cam_xuc > 3:
            trend = "TĂNG MẠNH 📈📈"
            conclusion = (
                "Thị trường đang có xu hướng tăng rất mạnh với nhiều tín hiệu tích cực.\n\n" 
                "💰 Khuyến nghị giao dịch:\n" 
                "- Nên MUA vào với các cổ phiếu có nền tảng tốt\n"
                "- Tăng tỷ trọng cổ phiếu trong danh mục\n"
                "- Có thể sử dụng đòn bẩy tùy theo khẩu vị rủi ro"
            )
        elif diem_cam_xuc > 1:
            trend = "TĂNG 📈"
            conclusion = (
                "Thị trường đang có xu hướng tăng nhẹ.\n\n"
                "💰 Khuyến nghị giao dịch:\n"
                "- Có thể MUA thêm cổ phiếu chọn lọc\n"
                "- Giữ tỷ trọng cổ phiếu ở mức vừa phải\n"
                "- Hạn chế sử dụng đòn bẩy"
            )
        elif diem_cam_xuc < -3:
            trend = "GIẢM MẠNH 📉📉"
            conclusion = (
                "Thị trường đang có xu hướng giảm mạnh với nhiều tín hiệu tiêu cực.\n\n"
                "💰 Khuyến nghị giao dịch:\n"
                "- Nên BÁN bớt vị thế và chờ đợi cơ hội mới\n"
                "- Giảm tỷ trọng cổ phiếu xuống mức tối thiểu\n"
                "- Không sử dụng đòn bẩy\n"
                "- Có thể xem xét sử dụng công cụ phòng hộ"
            )
        elif diem_cam_xuc < -1:
            trend = "GIẢM 📉"
            conclusion = (
                "Thị trường đang có xu hướng giảm nhẹ.\n\n"
                "💰 Khuyến nghị giao dịch:\n"
                "- Hạn chế MUA MỚI\n"
                "- Cân nhắc bán một phần cổ phiếu để bảo toàn lợi nhuận\n"
                "- Không sử dụng đòn bẩy"
            )
        else:
            trend = "ĐI NGANG ↔️"
            conclusion = (
                "Thị trường đang trong trạng thái đi ngang, chưa có xu hướng rõ rệt.\n\n"
                "💰 Khuyến nghị giao dịch:\n"
                "- Chờ đợi tín hiệu rõ ràng hơn\n"
                "- Giao dịch thận trọng, khối lượng nhỏ\n"
                "- Tập trung vào các cổ phiếu có nền tảng tốt"
            )
        return trend, conclusion



    def ve_bieu_do_so_sanh(self, tich_cuc_list, tieu_cuc_list):
        """Vẽ biểu đồ cột so sánh tỷ lệ phần trăm từ tích cực và tiêu cực"""
        plt.figure(figsize=(10, 6))
        
        # Tính tỷ lệ phần trăm cho mỗi bài viết
        ty_le_tich_cuc = []
        ty_le_tieu_cuc = []
        
        for tich_cuc, tieu_cuc in zip(tich_cuc_list, tieu_cuc_list):
            tong = tich_cuc + tieu_cuc
            if tong > 0:
                ty_le_tich_cuc.append((tich_cuc / tong) * 100)
                ty_le_tieu_cuc.append((tieu_cuc / tong) * 100)
            else:
                ty_le_tich_cuc.append(0)
                ty_le_tieu_cuc.append(0)
        
        # Vẽ biểu đồ cột
        x = range(len(ty_le_tich_cuc))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], ty_le_tich_cuc, width, label='Từ tích cực (%)', color='green', alpha=0.7)
        plt.bar([i + width/2 for i in x], ty_le_tieu_cuc, width, label='Từ tiêu cực (%)', color='red', alpha=0.7)
        
        # Thêm giá trị phần trăm lên đỉnh cột
        for i in x:
            plt.text(i - width/2, ty_le_tich_cuc[i], f'{ty_le_tich_cuc[i]:.1f}%', 
                     ha='center', va='bottom')
            plt.text(i + width/2, ty_le_tieu_cuc[i], f'{ty_le_tieu_cuc[i]:.1f}%', 
                     ha='center', va='bottom')
        
        plt.xlabel('Bài viết')
        plt.ylabel('Tỷ lệ (%)')
        plt.title('Tỷ lệ từ tích cực và tiêu cực trong các bài viết')
        plt.legend()
        plt.xticks(x, [f'Bài {i+1}' for i in x])
        
        # Đặt giới hạn trục y từ 0 đến 100%
        plt.ylim(0, 100)
        
        # Lưu biểu đồ
        plt.savefig('static/bieu_do_so_sanh.png', bbox_inches='tight')
        plt.close()


