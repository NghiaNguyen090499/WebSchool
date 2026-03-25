from django.db import models
from core.validators import validate_youtube_url
from core.utils.youtube import extract_youtube_id


class CoreValue(models.Model):
    GROUP_CHOICES = [
        ('grace', 'GRACE (Giá trị cốt lõi)'),
        ('5xin', '5 Xin'),
        ('5biet', '5 Biết'),
        ('5khong', '5 Không'),
        ('other', 'Khác'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Icon class name (e.g., 'fas fa-graduation-cap')")
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='other', verbose_name="Nhóm giá trị")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['group', 'order']
        verbose_name = 'Giá trị cốt lõi'
        verbose_name_plural = 'Giá trị cốt lõi'
    
    def __str__(self):
        return f"{self.get_group_display()} - {self.title}"


class CoreValuesPage(models.Model):
    title = models.CharField(max_length=200, default="Giá trị cốt lõi")
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        default="Đa trí tuệ - đa phương pháp - đa trải nghiệm & một nhân cách",
    )
    grace_title = models.CharField(max_length=100, default="GRACE")
    social_title = models.CharField(max_length=200, default="Trách nhiệm xã hội")
    social_content = models.TextField(blank=True)

    image = models.ImageField(upload_to="core_values/", blank=True, null=True)
    image_heading = models.CharField(max_length=200, blank=True, default="MIS hỗ trợ xây mới")
    image_title = models.CharField(max_length=200, blank=True, default="Trường Mầm non Háng Phù Loa")
    image_location = models.CharField(max_length=200, blank=True, default="Mồ Dề - Mù Cang Chải - Yên Bái")

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Giá trị cốt lõi"
        verbose_name_plural = "Giá trị cốt lõi"

    def __str__(self):
        return self.title


class Statistic(models.Model):
    label = models.CharField(max_length=100)
    value = models.IntegerField()
    icon = models.CharField(max_length=100, help_text="Icon class name")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Statistic'
        verbose_name_plural = 'Statistics'
    
    def __str__(self):
        return f"{self.label}: {self.value}"




class MenuItem(models.Model):
    POSITION_CHOICES = [
        ('header', 'Header/Navbar'),
        ('footer', 'Footer'),
        ('sidebar', 'Sidebar'),
    ]
    
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200, help_text="URL path or Django URL name (e.g. '/about/' or 'core:home')")
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome class (e.g. 'fas fa-home')")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='header')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
    
    def __str__(self):
        return self.title
    
    def get_link(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse(self.link)
        except NoReverseMatch:
            return self.link


class TrainingProgramGroup(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    eyebrow = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Training Program Group'
        verbose_name_plural = 'Training Program Groups'

    def __str__(self):
        return self.title


class TrainingProgram(models.Model):
    """Model for specialized training programs at MIS.

    The docx 2026-2027 defines 3 training systems:
      1. Hệ STEAM Chuẩn / CLC
      2. Hệ Tài năng Toán – Công nghệ mới
      3. Hệ Tài năng Ngôn ngữ (English + Chinese sub-tracks)

    We keep the original 5 PROGRAM_CHOICES for backward compatibility and
    add ``system_group`` to logically group programs per the docx structure.
    """

    PROGRAM_CHOICES = [
        ('steam', 'Hệ STEAM'),
        ('steam_clc', 'Hệ STEAM Chất lượng cao'),
        ('math', 'Hệ Tài năng Toán và Công nghệ mới'),
        ('english', 'Hệ Tài năng Tiếng Anh'),
        ('chinese', 'Hệ Tài năng Tiếng Trung'),
    ]

    SYSTEM_GROUP_CHOICES = [
        ('steam', 'Hệ STEAM Chuẩn / CLC'),
        ('math_tech', 'Hệ Tài năng Toán – Công nghệ mới'),
        ('language', 'Hệ Tài năng Ngôn ngữ'),
    ]

    group = models.ForeignKey(
        TrainingProgramGroup,
        on_delete=models.SET_NULL,
        related_name='programs',
        blank=True,
        null=True,
    )

    system_group = models.CharField(
        max_length=20,
        choices=SYSTEM_GROUP_CHOICES,
        default='steam',
        verbose_name="Nhóm hệ đào tạo (docx 2026-2027)",
        help_text="Nhóm theo cấu trúc 3 hệ trong tài liệu chính thức",
    )

    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug URL")
    name = models.CharField(max_length=200, verbose_name="Tên hệ đào tạo")
    short_name = models.CharField(max_length=100, verbose_name="Tên ngắn")
    tagline = models.CharField(max_length=300, verbose_name="Slogan")
    description = models.TextField(verbose_name="Mô tả chi tiết")
    
    # Partner information
    partner_name = models.CharField(max_length=200, verbose_name="Tên đối tác")
    partner_description = models.TextField(verbose_name="Giới thiệu đối tác")
    partner_logo = models.ImageField(upload_to='training_programs/partners/', blank=True, null=True, verbose_name="Logo đối tác")
    
    # Program content
    highlights = models.TextField(verbose_name="Điểm nổi bật", help_text="Mỗi dòng là một điểm nổi bật")
    curriculum = models.TextField(verbose_name="Nội dung chương trình", blank=True)
    achievements = models.TextField(verbose_name="Thành tích", blank=True)
    commitments = models.TextField(verbose_name="Cam kết", blank=True)
    
    # Grade levels
    grade_levels = models.CharField(max_length=100, default="Tiểu học - THPT", verbose_name="Cấp học áp dụng")
    
    # UI styling
    icon = models.CharField(max_length=50, default="fas fa-graduation-cap", verbose_name="Icon class")
    color = models.CharField(max_length=20, default="primary", verbose_name="Màu chủ đạo", 
                            help_text="primary, accent, blue, green, purple, orange")
    image = models.ImageField(upload_to='training_programs/', blank=True, null=True, verbose_name="Ảnh đại diện")
    
    # Display settings
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Hệ đào tạo'
        verbose_name_plural = 'Các hệ đào tạo'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:training_program_detail', kwargs={'slug': self.slug})
    
    def get_highlights_list(self):
        """Return highlights as a list"""
        return [h.strip() for h in self.highlights.split('\n') if h.strip()]
    
    def get_achievements_list(self):
        """Return achievements as a list"""
        return [a.strip() for a in self.achievements.split('\n') if a.strip()]
    
    def get_commitments_list(self):
        """Return commitments as a list"""
        return [c.strip() for c in self.commitments.split('\n') if c.strip()]


class SchoolInfo(models.Model):
    """
    PHẦN A – THÔNG TIN CHUNG VỀ TRƯỜNG
    Model để quản lý thông tin chung về trường
    """
    # 1. Tên đầy đủ của trường (VN & EN)
    name_vn = models.CharField(max_length=200, verbose_name="Tên đầy đủ (Tiếng Việt)")
    name_en = models.CharField(max_length=200, verbose_name="Tên đầy đủ (Tiếng Anh)")
    
    # 2. Tên viết tắt / Brand name
    short_name = models.CharField(max_length=50, verbose_name="Tên viết tắt / Brand name", blank=True)
    
    # 3. Địa chỉ campus
    address = models.TextField(verbose_name="Địa chỉ campus")
    
    # 4. Số điện thoại hotline chính
    hotline = models.CharField(max_length=20, verbose_name="Số điện thoại hotline chính")
    
    # 5. Email tuyển sinh chính thức
    admissions_email = models.EmailField(verbose_name="Email tuyển sinh chính thức")
    
    # 6. Website hiện tại (nếu có)
    current_website = models.URLField(verbose_name="Website hiện tại", blank=True)
    
    # 7. Fanpage / Social Media
    facebook_url = models.URLField(verbose_name="Facebook", blank=True)
    youtube_url = models.URLField(verbose_name="YouTube", blank=True)
    tiktok_url = models.URLField(verbose_name="TikTok", blank=True)
    zalo_url = models.URLField(verbose_name="Zalo", blank=True)
    instagram_url = models.URLField(verbose_name="Instagram", blank=True)
    linkedin_url = models.URLField(verbose_name="LinkedIn", blank=True)
    
    # Logo và branding
    logo = models.ImageField(upload_to='school_info/', blank=True, null=True, verbose_name="Logo trường")
    favicon = models.ImageField(upload_to='school_info/', blank=True, null=True, verbose_name="Favicon")
    
    # Email chung
    general_email = models.EmailField(verbose_name="Email chung", blank=True)
    
    # Mô tả ngắn
    short_description = models.TextField(verbose_name="Mô tả ngắn về trường", blank=True)
    
    # Cài đặt
    is_active = models.BooleanField(default=True, verbose_name="Đang sử dụng")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Thông tin trường'
        verbose_name_plural = 'Thông tin trường'
    
    def __str__(self):
        return self.name_vn
    
    @classmethod
    def get_active(cls):
        """Lấy thông tin trường đang hoạt động"""
        return cls.objects.filter(is_active=True).first()


class Campus(models.Model):
    """Campus locations for the school."""
    school = models.ForeignKey(
        SchoolInfo,
        on_delete=models.CASCADE,
        related_name='campuses',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200, verbose_name="Tên cơ sở")
    address = models.TextField(verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    map_embed_url = models.TextField(blank=True, verbose_name="Google Maps embed URL")
    is_primary = models.BooleanField(default=False, verbose_name="Cơ sở chính")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    order = models.IntegerField(default=0, verbose_name="Thứ tự")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Cơ sở'
        verbose_name_plural = 'Các cơ sở'

    def __str__(self):
        return self.name

class WebsiteGoal(models.Model):
    """
    PHẦN B – ĐỊNH HƯỚNG WEBSITE MỚI
    Mục tiêu chính của website
    """
    GOAL_CHOICES = [
        ('tuyen_sinh', 'Tuyển sinh'),
        ('giao_duc', 'Giáo dục & Đào tạo'),
        ('truyen_thong', 'Truyền thông & Marketing'),
        ('ket_noi', 'Kết nối phụ huynh'),
        ('tin_tuc', 'Tin tức & Sự kiện'),
        ('tuyen_dung', 'Tuyển dụng'),
        ('khac', 'Khác'),
    ]
    
    goal_type = models.CharField(max_length=20, choices=GOAL_CHOICES, verbose_name="Loại mục tiêu")
    description = models.TextField(verbose_name="Mô tả chi tiết", blank=True)
    priority = models.IntegerField(default=0, verbose_name="Độ ưu tiên", help_text="Số càng lớn, ưu tiên càng cao")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    class Meta:
        ordering = ['-priority', 'goal_type']
        verbose_name = 'Mục tiêu website'
        verbose_name_plural = 'Mục tiêu website'
    
    def __str__(self):
        return self.get_goal_type_display()


class StudentLifePage(models.Model):
    """
    PHẦN C – 4️⃣ Trang Đời sống học sinh
    Quản lý nội dung trang đời sống học sinh
    """
    title = models.CharField(max_length=200, verbose_name="Tiêu đề trang")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL slug")
    description = models.TextField(verbose_name="Mô tả ngắn")
    content = models.TextField(verbose_name="Nội dung chi tiết", blank=True)
    
    # Banner
    banner_image = models.ImageField(upload_to='student_life/', blank=True, null=True, verbose_name="Ảnh banner")
    
    # Các phần nội dung
    activities = models.TextField(verbose_name="Hoạt động", blank=True, help_text="Mỗi dòng là một hoạt động")
    clubs = models.TextField(verbose_name="Câu lạc bộ", blank=True, help_text="Mỗi dòng là một CLB")
    events = models.TextField(verbose_name="Sự kiện", blank=True, help_text="Mô tả các sự kiện")
    facilities = models.TextField(verbose_name="Cơ sở vật chất", blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta title")
    meta_description = models.TextField(blank=True, verbose_name="Meta description")
    
    # Display
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    order = models.IntegerField(default=0, verbose_name="Thứ tự")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Trang Đời sống học sinh'
        verbose_name_plural = 'Trang Đời sống học sinh'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:student_life')
    
    def get_activities_list(self):
        """Return activities as a list"""
        return [a.strip() for a in self.activities.split('\n') if a.strip()]
    
    def get_clubs_list(self):
        """Return clubs as a list"""
        return [c.strip() for c in self.clubs.split('\n') if c.strip()]


class HeroSlide(models.Model):
    """
    Model quản lý Hero Slider trên trang chủ
    """
    SLIDE_TYPE_CHOICES = [
        ('welcome', 'Welcome/Giới thiệu'),
        ('admissions', 'Tuyển sinh'),
        ('program', 'Chương trình học'),
        ('activities', 'Hoạt động'),
        ('event', 'Sự kiện'),
        ('other', 'Khác'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Tiêu đề chính")
    title_highlight = models.CharField(max_length=200, blank=True, verbose_name="Phần highlight của tiêu đề")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Tiêu đề phụ")
    slogan = models.CharField(max_length=200, blank=True, verbose_name="Slogan", 
                              default="Giáo dục con tim – Kiến tạo giá trị sống")
    description = models.TextField(blank=True, verbose_name="Mô tả ngắn")
    
    # Badge/Tag
    badge_text = models.CharField(max_length=100, blank=True, verbose_name="Badge text",
                                  help_text="VD: 'Đang mở đăng ký', 'Chương trình đặc biệt'")
    badge_icon = models.CharField(max_length=50, blank=True, verbose_name="Badge icon",
                                  help_text="FontAwesome class, VD: 'fas fa-calendar-check'")
    slide_type = models.CharField(max_length=20, choices=SLIDE_TYPE_CHOICES, default='welcome',
                                  verbose_name="Loại slide")
    
    # CTA Buttons
    cta_primary_text = models.CharField(max_length=100, blank=True, verbose_name="Nút chính - Text")
    cta_primary_url = models.CharField(max_length=200, blank=True, verbose_name="Nút chính - URL")
    cta_primary_icon = models.CharField(max_length=50, blank=True, verbose_name="Nút chính - Icon",
                                        help_text="VD: 'fas fa-arrow-right'")
    cta_secondary_text = models.CharField(max_length=100, blank=True, verbose_name="Nút phụ - Text")
    cta_secondary_url = models.CharField(max_length=200, blank=True, verbose_name="Nút phụ - URL")
    
    # Image
    image = models.ImageField(upload_to='hero/', verbose_name="Ảnh nền", 
                              help_text="Kích thước khuyến nghị: 1920x1080px")
    
    # Display settings
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'
    
    def __str__(self):
        return f"{self.title} ({self.get_slide_type_display()})"


class Achievement(models.Model):
    """
    Model quản lý thành tích nổi bật hiển thị trên trang chủ
    """
    CATEGORY_CHOICES = [
        ('academic', 'Học thuật'),
        ('competition', 'Cuộc thi'),
        ('language', 'Ngôn ngữ'),
        ('scholarship', 'Học bổng'),
        ('sports', 'Thể thao'),
        ('arts', 'Nghệ thuật'),
        ('technology', 'Công nghệ'),
        ('other', 'Khác'),
    ]
    
    COLOR_CHOICES = [
        ('red', 'Đỏ'),
        ('amber', 'Vàng cam'),
        ('green', 'Xanh lá'),
        ('blue', 'Xanh dương'),
        ('purple', 'Tím'),
        ('pink', 'Hồng'),
    ]
    
    # Stat Card (số liệu thống kê)
    stat_value = models.CharField(max_length=50, verbose_name="Giá trị thống kê",
                                  help_text="VD: '98%', '7.5', 'HSK6', '50+'")
    stat_label = models.CharField(max_length=100, verbose_name="Nhãn thống kê",
                                  help_text="VD: 'Tỷ lệ đậu Đại học'")
    
    # Achievement Detail Card
    title = models.CharField(max_length=200, verbose_name="Tiêu đề thành tích")
    description = models.TextField(verbose_name="Mô tả chi tiết")
    icon = models.CharField(max_length=50, default="fas fa-trophy", verbose_name="Icon",
                            help_text="FontAwesome class")
    image = models.ImageField(
        upload_to="achiement/",
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Optional image for achievement card",
    )
    
    # Tags
    tags = models.CharField(max_length=300, blank=True, verbose_name="Tags",
                            help_text="Các tag cách nhau bởi dấu phẩy, VD: 'ASMO, Kangaroo, SASMO'")
    
    # Categorization
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic',
                                verbose_name="Danh mục")
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='red',
                             verbose_name="Màu chủ đạo")
    
    # Type: stat (for stats grid) or card (for achievement cards)
    is_stat = models.BooleanField(default=False, verbose_name="Hiển thị dạng thống kê",
                                  help_text="Tick để hiển thị trong phần số liệu thống kê")
    is_card = models.BooleanField(default=True, verbose_name="Hiển thị dạng card",
                                  help_text="Tick để hiển thị trong phần achievement cards")
    year = models.IntegerField(default=2025, verbose_name="Năm đạt được")
    
    # Display settings
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Thành tích'
        verbose_name_plural = 'Thành tích nổi bật'
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Return tags as a list"""
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class ParentTestimonial(models.Model):
    """
    Model quản lý chia sẻ của phụ huynh
    """
    # Parent info
    parent_name = models.CharField(max_length=100, verbose_name="Tên phụ huynh",
                                   help_text="VD: 'PHHS Đức Minh'")
    student_class = models.CharField(max_length=50, verbose_name="Lớp học sinh",
                                     help_text="VD: '2S2', '12A5'")
    photo = models.ImageField(upload_to='testimonials/', verbose_name="Ảnh phụ huynh",
                              help_text="Ảnh khổ dọc, tỉ lệ 2:3")
    
    # Content
    title = models.CharField(max_length=200, verbose_name="Tiêu đề chia sẻ",
                             help_text="VD: 'Phụ huynh chia sẻ về hành trình học tập'")
    short_quote = models.TextField(verbose_name="Trích dẫn ngắn",
                                   help_text="Hiển thị trên carousel")
    full_content = models.TextField(verbose_name="Nội dung đầy đủ",
                                    help_text="Hiển thị trong modal")
    
    # Achievement highlight
    achievement = models.CharField(max_length=200, blank=True, verbose_name="Thành tích con",
                                   help_text="VD: 'HSK6 năm lớp 11', 'Học bổng toàn phần ĐH Ngôn ngữ Bắc Kinh'")
    
    # Video
    video_url = models.URLField(blank=True, verbose_name="URL Video",
                                help_text="Google Drive hoặc YouTube embed URL")
    has_video = models.BooleanField(default=False, verbose_name="Có video")
    
    # Display settings
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Chia sẻ phụ huynh'
        verbose_name_plural = 'Chia sẻ phụ huynh'
    
    def __str__(self):
        return f"{self.parent_name} - {self.student_class}"


class Partner(models.Model):
    """
    Model quản lý đối tác hợp tác
    """
    PARTNER_TYPE_CHOICES = [
        ('education', 'Đối tác giáo dục'),
        ('training', 'Đối tác đào tạo'),
        ('technology', 'Đối tác công nghệ'),
        ('language', 'Đối tác ngoại ngữ'),
        ('community', 'Đối tác cộng đồng'),
        ('international', 'Đối tác quốc tế'),
        ('sponsor', 'Nhà tài trợ'),
        ('other', 'Khác'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Tên đối tác")
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, verbose_name="Logo",
                             help_text="Kích thước khuyến nghị: 200x100px, nền trong suốt")
    url = models.URLField(verbose_name="Website đối tác", blank=True)
    description = models.TextField(blank=True, verbose_name="Mô tả ngắn")
    
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPE_CHOICES, 
                                    default='education', verbose_name="Loại đối tác")
    
    # Display settings
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    show_in_marquee = models.BooleanField(default=True, verbose_name="Hiển thị trên marquee trang chủ")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Đối tác'
        verbose_name_plural = 'Đối tác hợp tác'
    
    def __str__(self):
        return self.name


class FounderMessage(models.Model):
    """
    Model quản lý thông điệp người sáng lập
    """
    founder_name = models.CharField(max_length=100, verbose_name="Tên người sáng lập")
    founder_title = models.CharField(max_length=200, verbose_name="Chức danh")
    founder_photo = models.ImageField(upload_to='founder/', blank=True, null=True,
                                      verbose_name="Ảnh chân dung",
                                      help_text="Ảnh tròn, tỉ lệ 1:1")
    
    # Quote - hiển thị ở ngoài
    main_quote = models.TextField(verbose_name="Trích dẫn chính",
                                  help_text="Câu quote ngắn hiển thị trên trang chủ")
    
    # Full message - hiển thị trong modal
    greeting = models.CharField(max_length=200, blank=True, verbose_name="Lời chào",
                                default="Ba mẹ và các con học sinh thân mến,")
    full_message = models.TextField(verbose_name="Thông điệp đầy đủ")
    closing_message = models.TextField(blank=True, verbose_name="Lời kết")
    
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Thông điệp người sáng lập'
        verbose_name_plural = 'Thông điệp người sáng lập'
    
    def __str__(self):
        return f"Thông điệp - {self.founder_name}"
    
    @classmethod
    def get_active(cls):
        """Lấy thông điệp đang hiển thị"""
        return cls.objects.filter(is_active=True).first()


class StudentSpotlight(models.Model):
    """
    Model quản lý Gương mặt học sinh nổi bật
    """
    CATEGORY_CHOICES = [
        ('academic', 'Học thuật'),
        ('competition', 'Cuộc thi'),
        ('language', 'Ngôn ngữ'),
        ('scholarship', 'Học bổng'),
        ('sports', 'Thể thao'),
        ('arts', 'Nghệ thuật'),
        ('leadership', 'Lãnh đạo'),
        ('other', 'Khác'),
    ]
    
    # Student info
    student_name = models.CharField(max_length=100, verbose_name="Tên học sinh")
    student_class = models.CharField(max_length=50, verbose_name="Lớp",
                                     help_text="VD: '12A5', '9S1', 'Khóa 2022-2025'",null=True, blank=True)
    photo = models.ImageField(upload_to='student_spotlight/', verbose_name="Ảnh học sinh",
                              help_text="Ảnh chân dung hoặc ảnh nhận giải, tỉ lệ 4:3 hoặc 16:9")
    
    # Achievement
    title = models.CharField(max_length=200, verbose_name="Tiêu đề thành tích",
                            help_text="VD: 'Huy chương Vàng ASMO 2025'")
    achievement = models.TextField(verbose_name="Mô tả thành tích",
                                   help_text="Chi tiết về thành tích đạt được")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic',
                               verbose_name="Danh mục")
    
    # Quote
    quote = models.TextField(blank=True, verbose_name="Trích dẫn từ học sinh",
                            help_text="Câu nói/chia sẻ của học sinh (tùy chọn)")
    
    # Tags for achievements
    tags = models.CharField(max_length=300, blank=True, verbose_name="Tags thành tích",
                           help_text="VD: 'ASMO, Huy chương Vàng, Toán học'. Cách nhau bởi dấu phẩy")
    
    # Link to full news article (optional)
    article_url = models.URLField(blank=True, verbose_name="Link bài viết chi tiết",
                                  help_text="Link đến bài viết đầy đủ (nếu có)")
    
    # Display settings
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật trên trang chủ",
                                      help_text="Tick để hiển thị trên carousel trang chủ")
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Gương mặt học sinh'
        verbose_name_plural = 'Gương mặt học sinh nổi bật'
    
    def __str__(self):
        return f"{self.student_name} - {self.title}"
    
    def get_tags_list(self):
        """Return tags as a list"""
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class Podcast(models.Model):
    """
    Model quản lý Podcast - Tiếng nói MISERs
    """
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    description = models.TextField(blank=True, verbose_name="Mô tả ngắn")
    youtube_url = models.URLField(
        verbose_name="Link YouTube",
        help_text="VD: https://youtu.be/Q6C89WUHoNg",
        validators=[validate_youtube_url],
    )
    thumbnail = models.ImageField(upload_to='podcasts/', blank=True, null=True,
                                  verbose_name="Ảnh thumbnail",
                                  help_text="Nếu để trống sẽ tự động lấy từ YouTube")
    
    # Host/Guest info
    host_name = models.CharField(max_length=100, blank=True, verbose_name="Người dẫn")
    guest_name = models.CharField(max_length=100, blank=True, verbose_name="Khách mời")
    
    # Duration
    duration = models.CharField(max_length=20, blank=True, verbose_name="Thời lượng",
                               help_text="VD: '15:30', '1:02:45'")
    
    # Episode info
    episode_number = models.PositiveIntegerField(default=1, verbose_name="Số tập")
    published_date = models.DateField(blank=True, null=True, verbose_name="Ngày phát hành")
    
    # Display settings
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-episode_number', '-published_date', 'order']
        verbose_name = 'Podcast'
        verbose_name_plural = 'Tiếng nói MISERs - Podcasts'
    
    def __str__(self):
        return f"Ep.{self.episode_number}: {self.title}"
    
    def get_youtube_id(self):
        """Extract YouTube video ID from URL"""
        return extract_youtube_id(self.youtube_url)
    
    def get_embed_url(self):
        """Get YouTube embed URL"""
        video_id = self.get_youtube_id()
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None
    
    def get_thumbnail_url(self):
        """Get thumbnail URL - use uploaded or YouTube default"""
        if self.thumbnail:
            return self.thumbnail.url
        video_id = self.get_youtube_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None


class Pillar(models.Model):
    """Trụ cột giáo dục"""
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, help_text="FontAwesome class (e.g., 'fas fa-heart')")
    short_description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Trụ cột giáo dục"
        verbose_name_plural = "Trụ cột giáo dục"

    def __str__(self):
        return self.title


class Facility(models.Model):
    """Cơ sở vật chất và tiện ích"""
    CATEGORY_CHOICES = [
        ("classroom", "Phòng học"),
        ("lab", "Phòng lab"),
        ("utility", "Tiện ích"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="facilities/", blank=True, null=True)
    map_embed = models.TextField(blank=True, help_text="Google Maps embed iframe hoặc URL.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Cơ sở vật chất"
        verbose_name_plural = "Cơ sở vật chất"

    def __str__(self):
        return self.name


class MediaAsset(models.Model):
    FILE_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
        ("doc", "Document"),
        ("other", "Other"),
    ]

    CATEGORY_CHOICES = [
        ("home", "Home"),
        ("about", "About"),
        ("admissions", "Admissions"),
        ("academics", "Academics"),
        ("student_life", "Student Life"),
        ("news", "News"),
        ("awards", "Awards"),
        ("events", "Events"),
        ("csr", "CSR"),
        ("gallery", "Gallery"),
        ("unmapped", "Unmapped"),
    ]

    USAGE_RIGHTS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    file = models.FileField(upload_to="mis/2026/", blank=True, null=True)
    file_webp = models.ImageField(upload_to="mis/2026/", blank=True, null=True)
    file_jpeg = models.ImageField(upload_to="mis/2026/", blank=True, null=True)
    poster = models.ImageField(upload_to="mis/2026/", blank=True, null=True)

    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default="image")
    original_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="unmapped")
    tags = models.JSONField(default=list, blank=True)
    page_target = models.CharField(max_length=200, blank=True)
    block_target = models.CharField(max_length=200, blank=True)

    caption = models.CharField(max_length=300, blank=True)
    alt_text = models.CharField(max_length=300, blank=True)
    notes = models.TextField(blank=True)

    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)

    is_approved = models.BooleanField(default=False)
    needs_consent = models.BooleanField(default=False)
    contains_student = models.BooleanField(default=False)
    contains_parent = models.BooleanField(default=False)
    source = models.CharField(max_length=100, default="drive_2026")
    usage_rights_status = models.CharField(
        max_length=20,
        choices=USAGE_RIGHTS_CHOICES,
        default="pending",
    )

    checksum = models.CharField(max_length=64)
    file_size = models.PositiveBigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug"], name="mediaasset_slug_idx"),
            models.Index(fields=["checksum", "file_size"], name="mediaasset_checksum_size_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["checksum", "file_size"],
                name="mediaasset_unique_checksum_size",
            ),
        ]

    def __str__(self):
        return self.original_name


class ProgramOverviewPage(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    hero_image_url = models.URLField(blank=True)
    hero_image = models.ImageField(upload_to="program_overview/hero/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Trang chương trình tổng quan"
        verbose_name_plural = "Trang chương trình tổng quan"

    def __str__(self):
        return self.title


class ProgramOverviewImage(models.Model):
    page = models.ForeignKey(
        ProgramOverviewPage,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image_url = models.URLField()
    image = models.ImageField(upload_to="program_overview/pages/", blank=True, null=True)
    alt_text = models.CharField(max_length=300, blank=True)
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Ảnh chương trình tổng quan"
        verbose_name_plural = "Ảnh chương trình tổng quan"

    def __str__(self):
        return f"{self.page.title} - {self.order + 1}"


class MISPrototypeSiteContent(models.Model):
    year = models.CharField(max_length=9, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    badge = models.CharField(max_length=255, blank=True)
    lead = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)

    cta_primary_label = models.CharField(max_length=120, blank=True)
    cta_primary_href = models.CharField(max_length=255, blank=True)
    cta_primary_icon = models.CharField(max_length=100, blank=True)
    cta_secondary_label = models.CharField(max_length=120, blank=True)
    cta_secondary_href = models.CharField(max_length=255, blank=True)
    cta_secondary_icon = models.CharField(max_length=100, blank=True)

    metrics = models.JSONField(default=list, blank=True)

    source_doc = models.CharField(max_length=255, default="tmp_mis_program_2026_2027")
    approved_at = models.DateTimeField(null=True, blank=True)
    version = models.CharField(max_length=50, default="2026.1")

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year"]
        verbose_name = "MIS Prototype Site Content"
        verbose_name_plural = "MIS Prototype Site Content"

    def __str__(self):
        return f"{self.year} - {self.title}"


class MISPrototypePage(models.Model):
    page_key = models.SlugField(max_length=50)
    year = models.CharField(max_length=9, db_index=True)

    nav_label = models.CharField(max_length=120)
    title = models.CharField(max_length=255)
    browser_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    body_html = models.TextField(blank=True)
    blocks = models.JSONField(default=list, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    source_doc = models.CharField(max_length=255, default="tmp_mis_program_2026_2027")
    approved_at = models.DateTimeField(null=True, blank=True)
    version = models.CharField(max_length=50, default="2026.1")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["year", "order", "page_key"]
        constraints = [
            models.UniqueConstraint(
                fields=["year", "page_key"],
                name="mis_prototype_unique_year_key",
            )
        ]
        verbose_name = "MIS Prototype Page"
        verbose_name_plural = "MIS Prototype Pages"

    def __str__(self):
        return f"{self.year} - {self.page_key}"


class ProgramContentSource(models.Model):
    """DB-backed source for curriculum/program payloads (DB-first, JSON fallback)."""

    year = models.CharField(max_length=9, unique=True, db_index=True)
    content = models.JSONField(default=dict, blank=True)

    source_doc = models.CharField(max_length=255, default="program_content_json_import")
    approved_at = models.DateTimeField(null=True, blank=True)
    version = models.CharField(max_length=50, default="1.0")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year"]
        verbose_name = "Program Content Source"
        verbose_name_plural = "Program Content Sources"

    def __str__(self):
        return f"{self.year} - {self.version}"
