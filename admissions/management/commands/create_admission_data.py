from django.core.management.base import BaseCommand
from admissions.models import AdmissionInfo, AdmissionHighlight


class Command(BaseCommand):
    help = 'Create sample admission data'

    def handle(self, *args, **options):
        # Xóa dữ liệu cũ
        AdmissionInfo.objects.all().delete()
        
        # Mầm non
        mam_non = AdmissionInfo.objects.create(
            level='mam_non',
            title='Tuyển sinh Mầm non - Tiền Tiểu học 2025-2026',
            school_year='2025-2026',
            subtitle='Khởi đầu hành trình học tập với môi trường yêu thương và sáng tạo',
            age_range='2-5 tuổi',
            description='''Chương trình Mầm non MIS được thiết kế theo phương pháp giáo dục Đa trí tuệ (Multiple Intelligences), kết hợp với các phương pháp giáo dục tiên tiến như Montessori và Reggio Emilia.

Trẻ sẽ được phát triển toàn diện các mặt: thể chất, nhận thức, ngôn ngữ, tình cảm - xã hội và thẩm mỹ trong môi trường an toàn, yêu thương.

Chương trình song ngữ Anh - Việt từ 2 tuổi giúp trẻ làm quen và phát triển khả năng ngôn ngữ tự nhiên.''',
            requirements='''• Trẻ từ 2-5 tuổi tính đến thời điểm nhập học
• Có đủ sức khỏe để tham gia các hoạt động học tập
• Hồ sơ bao gồm:
  - Đơn xin nhập học (theo mẫu)
  - Bản sao giấy khai sinh
  - Sổ tiêm chủng
  - 04 ảnh 4x6
  - Bản sao sổ hộ khẩu/tạm trú''',
            tuition_info='''📌 Học phí tham khảo năm học 2025-2026:

• Học phí: 4.500.000 - 6.500.000 VNĐ/tháng (tùy độ tuổi)
• Bao gồm: học phí, ăn bán trú, đồ dùng học tập
• Chi phí khác: đồng phục, xe đưa đón (nếu có)

💡 Ưu đãi: Giảm 10% học phí khi đóng cả năm''',
            process='''1️⃣ Bước 1: Đăng ký tư vấn và tham quan trường
2️⃣ Bước 2: Nộp hồ sơ đăng ký
3️⃣ Bước 3: Tham gia buổi đánh giá năng lực (nếu có)
4️⃣ Bước 4: Nhận kết quả và hoàn tất thủ tục nhập học
5️⃣ Bước 5: Họp phụ huynh đầu năm''',
            benefits='''🎁 Ưu đãi đặc biệt:
• Miễn phí 100% học phí tháng đầu tiên
• Giảm 50% phí đăng ký nhập học
• Tặng bộ đồng phục trị giá 500.000đ
• Ưu đãi anh chị em ruột: Giảm thêm 10%''',
            icon='fas fa-baby',
            color='pink',
            is_active=True,
            is_featured=True,
            order=1
        )
        
        AdmissionHighlight.objects.create(
            admission=mam_non,
            title='Giáo viên bản ngữ',
            description='100% giờ tiếng Anh do giáo viên bản ngữ giảng dạy',
            icon='fas fa-globe',
            order=1
        )
        AdmissionHighlight.objects.create(
            admission=mam_non,
            title='Lớp học nhỏ',
            description='Tối đa 20 học sinh/lớp với 2-3 giáo viên phụ trách',
            icon='fas fa-users',
            order=2
        )
        
        # Tiểu học
        tieu_hoc = AdmissionInfo.objects.create(
            level='tieu_hoc',
            title='Tuyển sinh Tiểu học 2025-2026',
            school_year='2025-2026',
            subtitle='Xây dựng nền tảng vững chắc cho hành trình học tập',
            age_range='Lớp 1-5',
            description='''Chương trình Tiểu học MIS kết hợp giữa chương trình giáo dục của Bộ GD&ĐT và các yếu tố quốc tế, nhấn mạnh vào phát triển năng lực theo lý thuyết Đa trí tuệ.

Học sinh được học theo phương pháp Học tập hợp tác (HTHT), phát triển kỹ năng tư duy phản biện, giải quyết vấn đề và làm việc nhóm.

Chương trình STEAM được tích hợp từ lớp 1, giúp học sinh phát triển tư duy sáng tạo và kỹ năng công nghệ.''',
            requirements='''• Học sinh vào lớp 1: Sinh năm 2019 (tính theo năm)
• Học sinh các lớp khác: Có học bạ các năm trước
• Hồ sơ bao gồm:
  - Đơn xin nhập học (theo mẫu)
  - Bản sao giấy khai sinh
  - Học bạ (đối với lớp 2-5)
  - 04 ảnh 4x6
  - Bản sao sổ hộ khẩu''',
            tuition_info='''📌 Học phí tham khảo năm học 2025-2026:

• Học phí: 6.000.000 - 8.500.000 VNĐ/tháng
• Bao gồm: học phí, ăn bán trú, CLB buổi chiều
• Chi phí khác: đồng phục, sách giáo khoa, xe đưa đón

💡 Chính sách học bổng: Lên đến 50% học phí cho học sinh xuất sắc''',
            process='''1️⃣ Bước 1: Đăng ký và tham quan trường
2️⃣ Bước 2: Nộp hồ sơ đăng ký
3️⃣ Bước 3: Tham gia bài kiểm tra đầu vào
4️⃣ Bước 4: Phỏng vấn phụ huynh và học sinh
5️⃣ Bước 5: Nhận kết quả và hoàn tất nhập học''',
            benefits='''🎁 Học bổng Tài năng MIS:
• Học bổng 50%: Điểm thi đầu vào xuất sắc
• Học bổng 30%: Điểm thi đầu vào giỏi
• Học bổng 20%: Đăng ký sớm (Early Bird)
• Ưu đãi anh chị em ruột: Giảm 15%''',
            icon='fas fa-child',
            color='blue',
            is_active=True,
            order=2
        )
        
        AdmissionHighlight.objects.create(
            admission=tieu_hoc,
            title='STEAM từ lớp 1',
            description='Chương trình STEAM tích hợp với Robotics và Coding',
            icon='fas fa-robot',
            order=1
        )
        AdmissionHighlight.objects.create(
            admission=tieu_hoc,
            title='Tiếng Anh chuẩn Cambridge',
            description='Chuẩn bị cho các kỳ thi Cambridge YLE',
            icon='fas fa-certificate',
            order=2
        )
        
        # THCS
        thcs = AdmissionInfo.objects.create(
            level='thcs',
            title='Tuyển sinh THCS 2025-2026',
            school_year='2025-2026',
            subtitle='Phát triển toàn diện, sẵn sàng cho tương lai',
            age_range='Lớp 6-9',
            description='''Chương trình THCS MIS tập trung phát triển năng lực học thuật song song với kỹ năng sống và định hướng nghề nghiệp.

Học sinh được tham gia các CLB năng khiếu, dự án STEAM, và hoạt động trải nghiệm thực tế để phát triển các kỹ năng thế kỷ 21.

Chương trình đặc biệt chú trọng tiếng Anh giao tiếp và chuẩn bị cho các chứng chỉ quốc tế như IELTS, TOEFL Junior.''',
            requirements='''• Học sinh hoàn thành lớp 5 (vào lớp 6)
• Học sinh chuyển cấp: Có học bạ THCS
• Bài kiểm tra đầu vào: Toán, Tiếng Việt, Tiếng Anh
• Hồ sơ: Giấy khai sinh, học bạ, ảnh 4x6''',
            tuition_info='''📌 Học phí tham khảo năm học 2025-2026:

• Học phí: 8.000.000 - 12.000.000 VNĐ/tháng
• Bao gồm: học phí, CLB, hoạt động ngoại khóa

💡 Học bổng lên đến 100% cho học sinh đạt HSG cấp Thành phố''',
            process='''1️⃣ Đăng ký trực tuyến hoặc tại trường
2️⃣ Tham gia kỳ thi tuyển sinh
3️⃣ Phỏng vấn (nếu đạt điểm)
4️⃣ Công bố kết quả
5️⃣ Hoàn tất hồ sơ nhập học''',
            icon='fas fa-user-graduate',
            color='green',
            is_active=True,
            order=3
        )
        
        # THPT
        thpt = AdmissionInfo.objects.create(
            level='thpt',
            title='Tuyển sinh THPT 2025-2026',
            school_year='2025-2026',
            subtitle='Định hướng tương lai, chinh phục đại học',
            age_range='Lớp 10-12',
            description='''Chương trình THPT MIS định hướng học sinh theo các tổ hợp môn phù hợp với nguyện vọng đại học và nghề nghiệp.

Học sinh được đào tạo chuyên sâu các môn thi THPT Quốc gia, đồng thời có cơ hội tham gia các chương trình chuẩn bị du học.

Hỗ trợ đăng ký và chuẩn bị hồ sơ du học các nước: Mỹ, Anh, Úc, Canada, Singapore...''',
            requirements='''• Tốt nghiệp THCS
• Điểm trung bình các môn từ 6.5 trở lên
• Hạnh kiểm Khá trở lên
• Tham gia kỳ thi tuyển sinh của trường''',
            tuition_info='''📌 Học phí tham khảo năm học 2025-2026:

• Học phí: 10.000.000 - 15.000.000 VNĐ/tháng
• Bao gồm: học phí, ôn thi ĐH, hướng nghiệp

💡 Học bổng 100% cho Thủ khoa kỳ thi tuyển sinh''',
            process='''1️⃣ Đăng ký dự thi
2️⃣ Thi tuyển (Toán, Văn, Anh)
3️⃣ Phỏng vấn định hướng
4️⃣ Công bố kết quả và học bổng
5️⃣ Nhập học''',
            benefits='''🎓 Cam kết đầu ra:
• 100% học sinh tốt nghiệp THPT
• 95%+ đỗ Đại học
• Hỗ trợ 100% hồ sơ du học''',
            icon='fas fa-graduation-cap',
            color='purple',
            is_active=True,
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('Da tao du lieu mau tuyen sinh thanh cong!'))
