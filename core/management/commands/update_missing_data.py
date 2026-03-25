# -*- coding: utf-8 -*-
"""
Django management command to update missing data
Run: python manage.py update_missing_data
"""
from django.core.management.base import BaseCommand
from core.models import SchoolInfo, Campus, Partner, FounderMessage


class Command(BaseCommand):
    help = 'Update missing data in database for acceptance testing'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("[START] BAT DAU CAP NHAT DU LIEU THIEU")
        self.stdout.write("=" * 60)

        self.update_school_social_links()
        self.update_campuses()
        self.update_partners()
        self.update_founder_message()

        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("[DONE] HOAN THANH CAP NHAT DU LIEU!"))
        self.stdout.write("=" * 60)

    def update_school_social_links(self):
        self.stdout.write("\n[1] Cap nhat link mang xa hoi...")
        school_info = SchoolInfo.get_active()
        if not school_info:
            self.stdout.write(self.style.ERROR("[X] Khong tim thay SchoolInfo"))
            return

        school_info.facebook_url = school_info.facebook_url or "https://www.facebook.com/misschool.edu.vn"
        school_info.youtube_url = school_info.youtube_url or "https://www.youtube.com/@hethonggiaoduc_mis"
        school_info.tiktok_url = school_info.tiktok_url or "https://www.tiktok.com/@truong_mis"
        school_info.zalo_url = school_info.zalo_url or "https://zalo.me/truongmis"
        school_info.save()

        self.stdout.write(self.style.SUCCESS(f"[OK] Updated social links for SchoolInfo"))

    def update_campuses(self):
        self.stdout.write("\n[2] Cap nhat thong tin Campus...")
        school_info = SchoolInfo.get_active()

        cau_giay, created = Campus.objects.update_or_create(
            name="Co so Cau Giay",
            defaults={
                'school': school_info,
                'address': "So 1 Nguyen Van Huyen, Dich Vong, Cau Giay, Ha Noi",
                'phone': "024 60 278 666",
                'email': "tuyensinh@mis.edu.vn",
                'is_primary': True,
                'is_active': True,
                'order': 1,
            }
        )
        self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] Campus: {cau_giay.name}"))

        hoa_lac, created = Campus.objects.update_or_create(
            name="Co so Lang Hoa Lac",
            defaults={
                'school': school_info,
                'address': "Khu Cong nghe cao Hoa Lac, Thach That, Ha Noi",
                'phone': "024 60 278 666",
                'email': "tuyensinh@mis.edu.vn",
                'is_primary': False,
                'is_active': True,
                'order': 2,
            }
        )
        self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] Campus: {hoa_lac.name}"))

    def update_partners(self):
        self.stdout.write("\n[3] Cap nhat danh sach doi tac...")
        partners_data = [
            {"name": "Aptech Vietnam", "url": "https://aptechvietnam.com.vn/", "partner_type": "technology"},
            {"name": "MathExpress", "url": "https://mathexpress.vn/", "partner_type": "education"},
            {"name": "Jaxtina", "url": "https://jaxtina.com/", "partner_type": "education"},
            {"name": "Du hoc Quoc te Thoi Dai", "url": "http://duhocthoidai.com/", "partner_type": "international"},
            {"name": "STEAM Academy", "url": "https://steamacademy.edu.vn/", "partner_type": "education"},
            {"name": "RoboHub", "url": "https://robohub.vn/", "partner_type": "technology"},
            {"name": "Robotanan", "url": "https://www.robotanan.com/", "partner_type": "technology"},
            {"name": "Umbalena", "url": "https://umbalena.vn/", "partner_type": "education"},
            {"name": "Rice-INS", "url": "https://www.rice-ins.com/", "partner_type": "technology"},
        ]

        for idx, partner_info in enumerate(partners_data):
            partner, created = Partner.objects.update_or_create(
                name=partner_info["name"],
                defaults={
                    'url': partner_info["url"],
                    'partner_type': partner_info["partner_type"],
                    'is_active': True,
                    'show_in_marquee': True,
                    'order': idx,
                }
            )
            self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] Partner: {partner.name}"))

    def update_founder_message(self):
        self.stdout.write("\n[4] Cap nhat thong diep nguoi sang lap...")
        message, created = FounderMessage.objects.update_or_create(
            founder_name="Ong Hoang Van Luoc",
            defaults={
                'founder_title': "Tong Giam doc Dieu hanh - He thong Giao duc Da Tri Tue MIS",
                'main_quote': "Hoc de tu do, sang tao - Hoc de hanh phuc, tro thanh phien ban tot nhat cua chinh minh.",
                'greeting': "Ba me va cac con hoc sinh than men,",
                'full_message': """Trong thoi dai so hoa va toan cau hoa, giao duc khong chi la truyen dat kien thuc ma con la khoi day tiem nang, dam me va ca tinh rieng biet cua moi hoc sinh.

"Khac biet tao nen ban sac. Khai pha khac biet, chinh la trao cho moi dua tre co hoi tro thanh phien ban tot nhat cua chinh minh."

Tai MIS, chung toi tin rang moi hoc sinh la mot "hat giong doc dao". Chung toi tao ra moi truong noi su khac biet duoc ton trong, sang tao duoc khuyen khich, va long nhan ai cung tinh than toan cau duoc nuoi duong moi ngay.

MIS la tien phong trong doi moi giao duc tai Viet Nam voi tu duy "Glocal" - tu duy toan cau, ban sac dia phuong, chuan bi cho nhung ca nhan co the tu duy doc lap, yeu thuong, ket noi va dung vung truoc moi thay doi.

Chung toi day hoc sinh khong chi de gioi ma con de dan dat cuoc song cua chinh minh va tao ra gia tri cho cong dong.

MIS cam ket voi "Giao duc vi con nguoi", ho tro hoc sinh xuat sac ve hoc thuat, phat trien nhan cach va kien cuong cho mot tuong lai ben vung, hanh phuc.""",
                'closing_message': "Hay dong hanh cung chung toi, de khac biet la diem khoi dau cua vi dai!\n\nTran trong!",
                'is_active': True,
            }
        )
        self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] FounderMessage: {message.founder_name}"))
