
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
import django
django.setup()
from news.models import News, Category
from django.utils import timezone
from datetime import timedelta

html_text = '<p style="text-align:center;"><img src="/media/news/uwe_bristol/image_1.png" alt="Tin tức UWE" class="img-fluid rounded shadow-sm my-4 w-100"></p>\n<p>MIS MỞ RỘNG HỢP TÁC QUỐC TẾ VỚI UWE BRISTOL – PHENIKAA</p>\n<p>CƠ HỘI TIẾP CẬN GIÁO DỤC ANH QUỐC CÙNG GÓI HỌC BỔNG GẦN 1,8 TỶ ĐỒNG</p>\n<p>Trong bối cảnh giáo dục toàn cầu ngày càng mở rộng, việc lựa chọn một lộ trình đại học quốc tế với chi phí hợp lý đang trở thành mối quan tâm hàng đầu của nhiều phụ huynh.</p>\n<p>Nắm bắt nhu cầu đó, Trường Phổ thông Đa Trí Tuệ MIS chính thức mở rộng hợp tác chiến lược với Đại học Tây Anh Quốc – UWE Bristol (Vietnam – Phenikaa), mang đến thêm một hướng đi rõ ràng và bền vững cho học sinh sau THPT.</p>\n<p>ĐƯA CHUẨN GIÁO DỤC ANH QUỐC ĐẾN GẦN HƠN VỚI HỌC SINH VIỆT NAM</p>\n<p>UWE Bristol là một trong những đại học công lập hàng đầu tại Vương quốc Anh, hiện xếp hạng TOP 24/112 trường đại học tại Anh theo The Guardian 2023 . Thông qua hợp tác với Tập đoàn Phenikaa, chương trình đào tạo nguyên bản Anh Quốc được triển khai tại Việt Nam, đã được Bộ Giáo dục & Đào tạo công nhận.</p>\n<p>Chương trình đào tạo tập trung vào các lĩnh vực có tính ứng dụng cao và nhu cầu nhân lực lớn như:</p>\n<p>🔹 Kinh doanh & Marketing</p>\n<p>🔹 Kế toán & Tài chính</p>\n<p>🔹 Quản trị Kinh doanh</p>\n<p>🔹 Khoa học máy tính  - Trí tuệ nhân tạo (AI)</p>\n<p>Đây được xem là những ngành học phù hợp với xu thế phát triển “Future with AI – Future with Global Minds” mà MIS đang theo đuổi.</p>\n<p>🇬🇧 HỌC BỔNG COLUMBUS</p>\n<p>Điểm nhấn của hợp tác lần này là gói học bổng Columbus 2026 dành riêng cho học sinh MIS, với tổng giá trị lên tới 1.788.500.000 VNĐ.</p>\n<p>Học bổng được phân thành nhiều cấp độ (Diamond, Gold, Silver), không chỉ hỗ trợ học phí mà còn bao gồm:</p>\n<p>🔸 Hỗ trợ tham gia chương trình trải nghiệm học tập chuẩn Anh</p>\n<p>🔸 Cơ hội chuyển tiếp năm cuối tại UWE Bristol (Vương quốc Anh)</p>\n<p>🔸 Phát triển kỹ năng toàn diện trong môi trường quốc tế</p>\n<p>Đặc biệt, chương trình hướng đến các học sinh có năng lực học tập tốt, có định hướng rõ ràng và mong muốn phát triển trong môi trường toàn cầu, đồng thời đảm bảo mức chi phí hợp lý hơn so với lộ trình du học truyền thống.</p>\n<p>Qua đó, phụ huynh có thể tiếp cận thông tin một cách trực quan, rõ ràng, thay vì chỉ dừng lại ở các lựa chọn mang tính lý thuyết.</p>\n<p>Một quyết định đúng – có thể thay đổi cả hành trình tương lai của con.</p>\n<p>MIS x UWE BRISTOL – PHENIKAA</p>\n<p>Igniting a New Journey: Future with AI, Future with Heart, Future with Foreign Languages</p>\n<p style="text-align:center;"><img src="/media/news/uwe_bristol/image_2.png" alt="Tin tức UWE" class="img-fluid rounded shadow-sm my-4 w-100"></p>\n<p style="text-align:center;"><img src="/media/news/uwe_bristol/image_3.png" alt="Tin tức UWE" class="img-fluid rounded shadow-sm my-4 w-100"></p>'

# Create or get category
cat, _ = Category.objects.get_or_create(name="Tin tức", defaults={'slug': 'tin-tuc'})

# Prepare images
img_paths = ['news/uwe_bristol/image_1.png', 'news/uwe_bristol/image_2.png', 'news/uwe_bristol/image_3.png']

# Insert news
n = News.objects.create(
    title="MIS MỞ RỘNG HỢP TÁC QUỐC TẾ VỚI UWE BRISTOL",
    slug="mis-mo-rong-hop-tac-quoc-te-voi-uwe-bristol",
    category=cat,
    content=html_text,
    excerpt=html_text[:200].replace('<p>', '').replace('</p>', ''),
    is_featured=False, 
    created_at=timezone.now()
)
if img_paths:
    n.thumbnail.name = img_paths[0]
n.save()
print("Successfully inserted News article into Production Database!")
