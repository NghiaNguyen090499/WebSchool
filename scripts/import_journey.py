"""
Import 9 Journey Programs into database + copy static images to media folder.
Run with: python manage.py shell < scripts/import_journey.py
"""
import os
import shutil
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from csr.models import JourneyProgram, JourneyImage

# Base paths
BASE_DIR = r"d:\NGHIA\WebsiteSchool"
STATIC_BASE = os.path.join(BASE_DIR, "static", "images", "csr", "journey")
MEDIA_BASE = os.path.join(BASE_DIR, "media", "csr", "journey")

def copy_image(static_rel_path, media_rel_path):
    """Copy image from static to media, return media-relative path for ImageField."""
    src = os.path.join(STATIC_BASE, static_rel_path)
    dst_dir = os.path.join(MEDIA_BASE, os.path.dirname(media_rel_path))
    dst = os.path.join(MEDIA_BASE, media_rel_path)
    
    if not os.path.exists(src):
        print(f"  WARNING: Source not found: {src}")
        return None
    
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst)
    return f"csr/journey/{media_rel_path}"


# === 9 Journey Programs ===
programs_data = [
    {
        "title": "Đồng Hành Cùng Trẻ Khuyết Tật – Mái Ấm Thánh Tâm",
        "period": "2008 – 2017",
        "icon": "fa-hand-holding-heart",
        "short_description": "Trong suốt giai đoạn 2008 – 2015, nhà trường đã duy trì hành trình đồng hành cùng trẻ khuyết tật tại Mái ấm Thánh Tâm (Xuy Xá) – Mỹ Đức – Hà Nội.",
        "full_description": "Trong suốt giai đoạn 2008 – 2015, nhà trường đã duy trì hành trình đồng hành cùng trẻ khuyết tật tại Mái ấm Thánh Tâm (Xuy Xá) – Mỹ Đức – Hà Nội.<br><br>Nhà trường thường xuyên hỗ trợ thực phẩm, nhu yếu phẩm thiết yếu, đồng thời mang đến những hoạt động giao lưu, sẻ chia và động viên tinh thần cho các em nhỏ có hoàn cảnh đặc biệt.<br><br>Hành trình ấy không chỉ giúp các em tại mái ấm nhận được sự quan tâm từ cộng đồng, mà còn trở thành những bài học sống động về lòng trắc ẩn, sự biết ơn và trách nhiệm xã hội cho học sinh.<br><br>Tinh thần đó tiếp tục được kế thừa trong các hoạt động thiện nguyện và giáo dục giá trị sống của MIS cho đến ngày hôm nay.",
        "tags": "10 năm đồng hành\nGiáo viên & Phụ huynh",
        "order": 1,
        "is_featured": True,
        "cover_src": "treem-xuy-xa/468246557_10160598783586769_6864523863867831894_n.jpg",
        "gallery": [
            ("treem-xuy-xa/468246557_10160598783586769_6864523863867831894_n.jpg", "Mái ấm Thánh Tâm"),
            ("treem-xuy-xa/468226235_10160598787941769_6076533293195101408_n.jpg", "Hoạt động giao lưu"),
            ("treem-xuy-xa/468234135_10160598789016769_7004185870070989234_n.jpg", "Sẻ chia yêu thương"),
            ("treem-xuy-xa/468307414_10160598780561769_4201918769551981347_n.jpg", "Đồng hành cùng trẻ"),
            ("treem-xuy-xa/468582993_10160732804891769_6984337565610680957_n.jpg", "Khoảnh khắc đáng nhớ"),
        ],
    },
    {
        "title": "Mang Yêu Thương Về Vùng Lũ",
        "period": "2009 – 2025",
        "icon": "fa-cloud-showers-heavy",
        "short_description": 'Hành trình "Mang yêu thương về vùng lũ" của MCF đã để lại trong lòng mỗi thành viên MIS những cảm xúc khó quên – đến với những nơi mà người dân phải gồng mình chống chọi với thiên tai.',
        "full_description": 'Hành trình "Mang yêu thương về vùng lũ" của MCF đã để lại trong lòng mỗi thành viên MIS những cảm xúc khó quên.<br><br>MCF đã đến với những nơi mà người dân phải gồng mình chống chọi với thiên tai, với những thành phố ngập trong bùn rác. Nhìn thấy tận mắt những bản làng bị cô lập, những cây cầu bị cuốn trôi – nỗi xót xa không khỏi trĩu nặng trong tim.<br><br>Để hỗ trợ bà con tái thiết lại cuộc sống, MCF đã trao tặng những vật phẩm thiết yếu như gạo, đồ dùng sinh hoạt, quần áo, chăn ấm, và nhu yếu phẩm hàng ngày.<br><br>Hành trình này là minh chứng rõ ràng cho tình người, sự đoàn kết, và sức mạnh cộng đồng.',
        "tags": "16 năm hoạt động\n8 đợt thiện nguyện",
        "order": 2,
        "is_featured": True,
        "cover_src": "yeu-thuong-vung-lu/anh_1.jpg",
        "gallery": [
            ("yeu-thuong-vung-lu/anh_1.jpg", "Vùng lũ"),
            ("yeu-thuong-vung-lu/anh_2.jpg", "Trao quà"),
            ("yeu-thuong-vung-lu/anh_3.jpg", "Hỗ trợ bà con"),
            ("yeu-thuong-vung-lu/anh_4.jpg", "Thiện nguyện"),
            ("yeu-thuong-vung-lu/anh_5.jpg", "Đoàn kết"),
        ],
    },
    {
        "title": "Trung Thu Nơi Đỉnh Trời – Mèo Vạc, Hà Giang",
        "period": "2017 – 2025",
        "icon": "fa-moon",
        "short_description": "Có những mùa trăng, ánh sáng không chỉ ngập tràn phố thị, mà còn dịu dàng vượt núi, ôm ấp những con đường đất miền cao – nơi MCF mang Trung thu về với trẻ em Mèo Vạc, Hà Giang.",
        "full_description": 'Có những mùa trăng, ánh sáng không chỉ ngập tràn phố thị, mà còn dịu dàng vượt núi, ôm ấp những con đường đất miền cao – nơi MCF mang Trung thu về với trẻ em Mèo Vạc, Hà Giang.<br><br>Trung Thu năm nay là hương vị ngọt ngào của bánh nướng, bánh dẻo mà có thể là lần đầu được nếm thử trên môi những bạn nhỏ Trà Mần – Sơn Vĩ – Mèo Vạc.<br><br>Hành trình "Trung thu sẻ chia" đã trở thành nhịp điệu thường niên của trái tim MCF. Mang theo không chỉ là những món quà vật chất, mà là cả tấm lòng muốn sẻ chia, muốn gửi gắm yêu thương.<br><br>Trung Thu này, dưới vầng trăng vùng cao, thầy trò chúng tôi thấu hiểu hơn hai chữ "sum vầy".',
        "tags": "Mèo Vạc – Hà Giang\nTrung thu sẻ chia",
        "order": 3,
        "is_featured": True,
        "cover_src": "trung-thu-bien-gioi/anh_1.jpg",
        "gallery": [
            ("trung-thu-bien-gioi/anh_1.jpg", "Trung thu vùng cao"),
            ("trung-thu-bien-gioi/anh_2.jpg", "Trao quà"),
            ("trung-thu-bien-gioi/anh_3.jpg", "Niềm vui"),
            ("trung-thu-bien-gioi/anh_4.jpg", "Sẻ chia"),
            ("trung-thu-bien-gioi/anh_5.jpg", "Mèo Vạc"),
            ("trung-thu-bien-gioi/anh_6.jpg", "Hành trình"),
            ("trung-thu-bien-gioi/anh_7.jpg", "Yêu thương"),
        ],
    },
    {
        "title": "Thư Viện Kết Nghĩa",
        "period": "2017 – 2019",
        "icon": "fa-book-open",
        "short_description": "Chương trình hỗ trợ xây dựng và trao tặng thư viện sách cho các trường học vùng khó khăn, góp phần lan tỏa văn hóa đọc và tạo cơ hội tiếp cận tri thức.",
        "full_description": "Chương trình hỗ trợ xây dựng và trao tặng thư viện sách cho các trường học vùng khó khăn, góp phần lan tỏa văn hóa đọc và tạo cơ hội tiếp cận tri thức.<br><br>Tại nhiều điểm trường vùng sâu, các em học sinh chưa từng có cơ hội tiếp xúc với sách truyện hay sách tham khảo. Thư Viện Kết Nghĩa ra đời với sứ mệnh mang tri thức đến gần hơn với cộng đồng.",
        "tags": "Thư viện sách\nTrường vùng khó khăn",
        "order": 4,
        "is_featured": False,
        "cover_src": None,
        "gallery": [],
    },
    {
        "title": "Sharing & Caring – Đẩy Lùi Covid-19",
        "period": "2020",
        "icon": "fa-shield-virus",
        "short_description": 'Hành trình 8 ngày "Sharing is Caring" – MCF trao tặng thực phẩm sạch từ trang trại giáo dục MIS, hỗ trợ cộng đồng trong giai đoạn cách ly toàn xã hội.',
        "full_description": 'Hành trình 8 ngày "Sharing is Caring" – MCF trao tặng thực phẩm sạch từ trang trại giáo dục MIS, hỗ trợ cộng đồng trong giai đoạn cách ly toàn xã hội.<br><br><strong>Ngày 1:</strong> Trao 50 phần quà tới UBND phường Dịch Vọng.<br><strong>Ngày 2:</strong> Trao 131 phần quà tại xóm chạy thận.<br><strong>Ngày 3:</strong> Gửi 100 suất quà tới xóm trọ bệnh nhân Bệnh viện K Tân Triều.<br><strong>Ngày 4:</strong> Hỗ trợ người lao động nghèo phía sau chợ Long Biên.<br><strong>Ngày 5:</strong> Trao quà cho người vô gia cư trên phố Hà Nội.<br><strong>Ngày 6:</strong> Trao 1000 quả trứng + 200kg rau sạch tại Sư đoàn 308.<br><strong>Ngày 7:</strong> Quay trở lại Bệnh viện K với 130 phần quà.<br><strong>Ngày 8:</strong> Trao cho 100 hộ khó khăn & 80 gia đình bệnh nhân tại Viện Nhi TW.',
        "tags": "8 ngày chia sẻ\nĐẩy lùi Covid-19",
        "order": 5,
        "is_featured": False,
        "cover_src": "sharing-caring-covid/anh_1.jpg",
        "gallery": [
            ("sharing-caring-covid/anh_1.jpg", "Sharing & Caring"),
            ("sharing-caring-covid/anh_2.jpg", "Trao quà"),
            ("sharing-caring-covid/anh_3.jpg", "Hỗ trợ cộng đồng"),
            ("sharing-caring-covid/anh_4.jpg", "Chia sẻ yêu thương"),
            ("sharing-caring-covid/anh_5.jpg", "Đoàn kết"),
            ("sharing-caring-covid/anh_6.jpg", "Vượt qua đại dịch"),
            ("sharing-caring-covid/anh_7.jpg", "MCF trao quà"),
        ],
    },
    {
        "title": "Save the Doctor – Tri Ân Y Bác Sĩ",
        "period": "2020 – 2021",
        "icon": "fa-user-md",
        "short_description": "Chương trình tri ân và hỗ trợ các y bác sĩ tuyến đầu chống dịch, thể hiện tinh thần trách nhiệm xã hội của cộng đồng MIS.",
        "full_description": "Chương trình tri ân và hỗ trợ các y bác sĩ tuyến đầu chống dịch, thể hiện tinh thần trách nhiệm xã hội của cộng đồng MIS.<br><br>Trong thời điểm đại dịch Covid-19 bùng phát, MIS đã chung tay cùng cộng đồng gửi lời tri ân đến các chiến sĩ áo trắng – những người đã không quản ngại hiểm nguy, ngày đêm chiến đấu vì sức khỏe cộng đồng.",
        "tags": "Hỗ trợ y tế\nTri ân bác sĩ",
        "order": 6,
        "is_featured": False,
        "cover_src": None,
        "gallery": [],
    },
    {
        "title": "Sống Như Những Đoá Hoa – Dấn Thân & Nối Kết",
        "period": "Hàng năm",
        "icon": "fa-hospital-user",
        "short_description": "Những hạt mầm yêu thương, sẻ chia đã hình thành trong nhân cách MISers – từ những chuyến thiện nguyện do chính các con khởi xướng, thăm bệnh nhân nhi và người vô gia cư.",
        "full_description": 'Những hạt mầm yêu thương, sẻ chia đã hình thành trong nhân cách MISers – từ những chuyến thiện nguyện do chính các con khởi xướng, thăm bệnh nhân nhi và người vô gia cư.<br><br>Tối ngày 14.01.2023, tập thể 9A1 đã cùng nhau thực hiện hoạt động thiện nguyện do chính các con khởi xướng – mang những chiếc bánh chưng nhỏ xinh từ lễ hội "Bên nhau là Tết" đến với bệnh nhân nhi ung thư tại Bệnh viện Nhi Trung ương và người vô gia cư tại Hà Nội.<br><br><em>"Con đã tự nhủ với bản thân là mình quá may mắn khi còn có được một cơ thể lành lặn, một sức khoẻ tốt thì hãy nên biết quý trọng cuộc sống mà mình đang có." – Nguyễn Hoàng Phương Anh, 9A1</em><br><br>Đó chính là bài học GRACE mà MIS luôn hướng tới: <strong>Gratitude</strong> – Biết ơn, <strong>Respect</strong> – Tôn trọng, <strong>Accountability</strong> – Trách nhiệm, <strong>Courage</strong> – Can đảm, <strong>Engagement</strong> – Dấn thân & Nối kết.',
        "tags": "Bệnh nhân nhi\nGRACE Values",
        "order": 7,
        "is_featured": False,
        "cover_src": "dong-hanh-khuyet-tat/1.jpg",
        "gallery": [
            ("dong-hanh-khuyet-tat/1.jpg", "Đồng hành"),
            ("dong-hanh-khuyet-tat/2.jpg", "Sẻ chia"),
            ("dong-hanh-khuyet-tat/3.jpg", "Yêu thương"),
            ("dong-hanh-khuyet-tat/4.jpg", "Kết nối"),
            ("dong-hanh-khuyet-tat/5.jpg", "GRACE Values"),
        ],
    },
    {
        "title": "Xuân Yêu Thương – Mùa Xuân Đâm Chồi Từ Hạt Mầm GRACE",
        "period": "Mỗi dịp Tết",
        "icon": "fa-gift",
        "short_description": "MISers tự gây quỹ từ bánh handmade, bán hàng, kêu gọi cộng đồng – rồi chính các con lên đường mang quà đến Cao Bằng, Ninh Bình và những nơi thiếu thốn.",
        "full_description": 'MISers tự gây quỹ từ bánh handmade, bán hàng, kêu gọi cộng đồng – rồi chính các con lên đường mang quà đến Cao Bằng, Ninh Bình và những nơi thiếu thốn.<br><br>Tại Cao Bằng, trong chương trình "Xuân trên bản xa" tại các điểm trường thuộc xã Quảng Lâm – những thùng quà, đồ chơi và hơi ấm mùa xuân được gửi gắm đến các bé mầm non.<br><br>Tại Ninh Bình, trong "Hội chợ 0 đồng" ở xã Lý Nhân – những gian hàng đầy ắp yêu thương được chính MISers trao tặng cho ông bà có hoàn cảnh khó khăn.<br><br>Hành trình hơn 10 năm trao yêu thương của MCF không chỉ trao quà mà trao truyền cảm hứng để mỗi MISer học cách trở thành một công dân biết rung động với những điều tử tế.',
        "tags": "Quà Tết\nHạt mầm GRACE",
        "order": 8,
        "is_featured": False,
        "cover_src": "xuan-yeu-thuong/1.jpg",
        "gallery": [
            ("xuan-yeu-thuong/1.jpg", "Xuân yêu thương"),
            ("xuan-yeu-thuong/2.jpg", "Trao quà"),
            ("xuan-yeu-thuong/3.jpg", "Hội chợ 0 đồng"),
            ("xuan-yeu-thuong/4.jpg", "Bản xa"),
        ],
    },
    {
        "title": "Hơi Ấm Những Ngày Đầu Đông & Hỗ Trợ Trường Học",
        "period": "Các dự án đặc biệt",
        "icon": "fa-school",
        "short_description": "MCF chung tay hỗ trợ Trường Mầm non Gia Phú B – Điện Biên một căn bếp nhỏ xinh để mùa đông này thầy cô đỡ vất vả hơn và các con có những bữa ăn ấm nóng hơn.",
        "full_description": 'MCF chung tay hỗ trợ Trường Mầm non Gia Phú B – Điện Biên một căn bếp nhỏ xinh để mùa đông này thầy cô đỡ vất vả hơn và các con có những bữa ăn ấm nóng hơn.<br><br><em>"Khi bạn đối xử tốt với một người lạ – một người có thể chẳng bao giờ gặp lại bạn – là một hành động có sức mạnh thay đổi cuộc đời một con người." – Bernadette Russell</em><br><br>MCF mong rằng những hành động nhỏ bé truyền cảm hứng đến những thế hệ học sinh về LÒNG TỐT & sức mạnh của sự ĐOÀN KẾT.<br><br>Ngoài ra, MIS còn hỗ trợ sửa sân trường tại Quản Bạ – Hà Giang, chương trình "Nấu ăn cho em", "Đường Hy Vọng" và hỗ trợ mua máy thở tặng bé Hà Vy.',
        "tags": "Sửa trường học\nNấu ăn cho em\nĐường Hy Vọng",
        "order": 9,
        "is_featured": False,
        "cover_src": "ho-tro-sua-truong/1.jpg",
        "gallery": [
            ("ho-tro-sua-truong/1.jpg", "Hỗ trợ sửa trường"),
            ("ho-tro-sua-truong/2.jpg", "Căn bếp nhỏ"),
        ],
    },
]


def run():
    print("=== Importing 9 Journey Programs ===\n")
    
    # Clear existing data
    deleted_count = JourneyProgram.objects.all().delete()[0]
    if deleted_count:
        print(f"Cleared {deleted_count} existing records.\n")
    
    for data in programs_data:
        print(f"▸ {data['title'][:50]}...")
        
        # Copy cover image
        cover_path = ""
        if data["cover_src"]:
            folder = data["cover_src"].split("/")[0]
            filename = data["cover_src"].split("/")[-1]
            media_path = f"covers/{folder}_{filename}"
            result = copy_image(data["cover_src"], media_path)
            if result:
                cover_path = result
                print(f"  ✓ Cover: {result}")
        
        # Create program
        program = JourneyProgram.objects.create(
            title=data["title"],
            period=data["period"],
            icon=data["icon"],
            short_description=data["short_description"],
            full_description=data["full_description"],
            tags=data["tags"],
            order=data["order"],
            is_active=True,
            is_featured=data["is_featured"],
        )
        
        # Set cover image if exists
        if cover_path:
            program.cover_image = cover_path
            program.save(update_fields=["cover_image"])
        
        # Copy gallery images
        for idx, (img_src, caption) in enumerate(data.get("gallery", []), start=1):
            folder = img_src.split("/")[0]
            filename = img_src.split("/")[-1]
            media_path = f"gallery/{folder}_{filename}"
            img_result = copy_image(img_src, media_path)
            
            if img_result:
                JourneyImage.objects.create(
                    program=program,
                    image=img_result,
                    caption=caption,
                    order=idx,
                    is_active=True,
                )
                print(f"  ✓ Gallery [{idx}]: {caption}")
        
        print()
    
    total = JourneyProgram.objects.count()
    total_imgs = JourneyImage.objects.count()
    featured = JourneyProgram.objects.filter(is_featured=True).count()
    print(f"=== Done! {total} programs, {total_imgs} gallery images, {featured} featured ===")


run()
