import os
import django

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from core.models import CoreValue, Achievement, Facility

def run():
    print("Populating data...")

    # --- Core Values ---
    # GRACE
    grace_values = [
        {"title": "G-ratitude | Biết ơn", "description": "Biết ơn cha mẹ, thầy cô và cuộc sống.", "icon": "fas fa-pray", "group": "grace", "order": 1},
        {"title": "R-espect | Tôn trọng", "description": "Tôn trọng bản thân, tôn trọng người khác và sự khác biệt.", "icon": "fas fa-hand-holding-heart", "group": "grace", "order": 2},
        {"title": "A-ccountability | Trách nhiệm", "description": "Chịu trách nhiệm về hành động và lời nói của mình.", "icon": "fas fa-balance-scale", "group": "grace", "order": 3},
        {"title": "C-ourage | Can đảm", "description": "Can đảm đối mặt thử thách và sửa sai.", "icon": "fas fa-fist-raised", "group": "grace", "order": 4},
        {"title": "E-ngagement | Dấn thân", "description": "Sẵn sàng tham gia, đóng góp và kết nối.", "icon": "fas fa-users", "group": "grace", "order": 5},
    ]

    # 5 XIN
    nam_xin = [
        {"title": "Xin chào", "description": "Lời chào cao hơn mâm cỗ", "icon": "fas fa-hand-paper", "group": "5xin", "order": 1},
        {"title": "Xin lỗi", "description": "Dũng cảm nhận lỗi", "icon": "fas fa-user-injured", "group": "5xin", "order": 2},
        {"title": "Xin phép", "description": "Tôn trọng quy tắc", "icon": "fas fa-check-square", "group": "5xin", "order": 3},
        {"title": "Xin cảm ơn", "description": "Biết ơn người giúp đỡ", "icon": "fas fa-heart", "group": "5xin", "order": 4},
        {"title": "Xin hỏi", "description": "Ham học hỏi", "icon": "fas fa-question-circle", "group": "5xin", "order": 5},
    ]

    # 5 BIET
    nam_biet = [
        {"title": "Biết ơn", "description": "Trân trọng những gì đang có", "icon": "fas fa-spa", "group": "5biet", "order": 1},
        {"title": "Biết lắng nghe", "description": "Thấu hiểu người khác", "icon": "fas fa-assistive-listening-systems", "group": "5biet", "order": 2},
        {"title": "Biết chia sẻ", "description": "Lan tỏa yêu thương", "icon": "fas fa-share-alt", "group": "5biet", "order": 3},
        {"title": "Biết nhường nhịn", "description": "Bình tĩnh và vị tha", "icon": "fas fa-hand-holding", "group": "5biet", "order": 4},
        {"title": "Biết tự học", "description": "Chủ động khám phá tri thức", "icon": "fas fa-book-reader", "group": "5biet", "order": 5},
    ]

    # 5 KHONG
    nam_khong = [
        {"title": "Không nói dối", "description": "Trung thực là cốt lõi", "icon": "fas fa-comment-slash", "group": "5khong", "order": 1},
        {"title": "Không bạo lực", "description": "Yêu thương và hòa bình", "icon": "fas fa-ban", "group": "5khong", "order": 2},
        {"title": "Không gian lận", "description": "Công bằng trong thi cử", "icon": "fas fa-times-circle", "group": "5khong", "order": 3},
        {"title": "Không vô lễ", "description": "Kính trên nhường dưới", "icon": "fas fa-thumbs-down", "group": "5khong", "order": 4},
        {"title": "Không lãng phí", "description": "Tiết kiệm tài nguyên", "icon": "fas fa-trash-alt", "group": "5khong", "order": 5},
    ]

    all_values = grace_values + nam_xin + nam_biet + nam_khong
    
    # Clean up old values first to avoid duplicates
    CoreValue.objects.all().delete()
    
    for val in all_values:
        CoreValue.objects.create(**val)
        
    print("Core Values populated.")

    # --- Achievements ---
    # Clean up old achievements
    Achievement.objects.all().delete()
    
    achievements = [
        {
            "title": "STEAM & Robotics",
            "description": "02 Giải Vàng, 04 Giải Đồng tại STEAM Cup Quốc tế Malaysia 2025. Dẫn đầu đoàn Việt Nam.",
            "stat_value": "06",
            "stat_label": "Huy chương Quốc tế",
            "category": "technology",
            "color": "red",
            "year": 2025,
            "tags": "STEAM, Robotics, STEAM Cup"
        },
        {
            "title": "Olympic Quốc Tế (ASMO)",
            "description": "Cấp Quốc gia: 17 Vàng, 24 Bạc. Cấp Thành phố: 12 Vàng, 2 Bạc. Quốc tế (Vòng 2): 2 Vàng, 1 Bạc.",
            "stat_value": "58",
            "stat_label": "Giải thưởng ASMO",
            "category": "academic",
            "color": "blue",
            "year": 2025,
            "tags": "ASMO, Toán, Khoa học, Tiếng Anh"
        },
        {
            "title": "Năng Lực Ngôn Ngữ",
            "description": "50% Học sinh K12 đạt IELTS 5.0 - 7.5. 98% đỗ Đại học Top đầu. 15 học bổng du học.",
            "stat_value": "100%",
            "stat_label": "Đỗ Đại học",
            "category": "language",
            "color": "green",
            "year": 2025,
            "tags": "IELTS, Du học, Đại học"
        }
    ]

    for ach in achievements:
        Achievement.objects.create(**ach)
        
    print("Achievements populated.")

    # --- Facilities ---
    # Clean up old facilities
    Facility.objects.all().delete()
    
    facilities = [
        {
            "name": "MIS Pandora Landscape",
            "category": "utility",
            "description": "Trang trại giáo dục đa dạng sinh học 6ha - Nơi học sinh hòa mình với thiên nhiên, trải nghiệm nông nghiệp và nghệ thuật ngoài trời.",
            "image": "", # Placeholder, will be manually updated or left blank
            "order": 1
        },
        {
            "name": "Trường học Xanh (Green School)",
            "category": "utility",
            "description": "Hệ thống điện năng lượng mặt trời cung cấp 50% nhu cầu, giáo dục ý thức bảo vệ môi trường và phát triển bền vững.",
            "image": "", # Placeholder
            "order": 2
        }
    ]

    for fac in facilities:
        Facility.objects.create(**fac)
        
    print("Facilities populated.")

    print("Data population complete.")

if __name__ == "__main__":
    run()
