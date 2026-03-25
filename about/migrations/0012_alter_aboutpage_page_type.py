from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("about", "0011_alter_aboutsection_layout"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutpage",
            name="page_type",
            field=models.CharField(
                choices=[
                    ("mission", "V\xe1\xbb\x81 ch\xc3\xbang t\xc3\xb4i"),
                    ("vision", "Gi\xc3\xa1 tr\xe1\xbb\x8b c\xe1\xbb\x91t l\xc3\xb5i"),
                    ("principal", "L\xe1\xbb\x8bch s\xe1\xbb\xad h\xc3\xacnh th\xc3\xa0nh"),
                    ("strengths", "8 \xc4\x91i\xe1\xbb\x83m m\xe1\xba\xa1nh kh\xc3\xa1c bi\xe1\xbb\x87t"),
                    ("strategy", "Chi\xe1\xba\xbfn l\xc6\xb0\xe1\xbb\xa3c ph\xc3\xa1t tri\xe1\xbb\x83n"),
                    ("structure", "C\xc6\xa1 c\xe1\xba\xa5u t\xe1\xbb\x95 ch\xe1\xbb\xa9c MIS"),
                    ("culture", "Quy \xc4\x91\xe1\xbb\x8bnh v\xc4\x83n h\xc3\xb3a MIS"),
                    ("boarding", "M\xc3\xb4i tr\xc6\xb0\xe1\xbb\x9dng n\xe1\xbb\x99i tr\xc3\xba"),
                    ("happiness", "Tr\xc6\xb0\xe1\xbb\x9dng V\xc4\x83n minh \xe2\x80\x93 H\xe1\xba\xa1nh ph\xc3\xbac"),
                    ("liberal", "Gi\xc3\xa1o d\xe1\xbb\xa5c khai ph\xc3\xb3ng"),
                    ("academics", "T\xe1\xbb\x95ng quan Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh Gi\xc3\xa1o d\xe1\xbb\xa5c"),
                    ("preschool", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh M\xe1\xba\xa7m non (3-6 tu\xe1\xbb\x95i)"),
                    ("primary", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh Ti\xe1\xbb\x83u h\xe1\xbb\x8dc (L\xe1\xbb\x9bp 1-5)"),
                    ("middle", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh THCS (L\xe1\xbb\x9bp 6-9)"),
                    ("high", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh THPT (L\xe1\xbb\x9bp 10-12)"),
                    ("overview_math", "T\xe1\xbb\x95ng quan Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh m\xc3\xb4n To\xc3\xa1n"),
                    ("overview_literature", "T\xe1\xbb\x95ng quan Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh m\xc3\xb4n Ng\xe1\xbb\xaf v\xc4\x83n"),
                    ("overview_english", "T\xe1\xbb\x95ng quan Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh Ti\xe1\xba\xbfng Anh"),
                    ("overview_chinese", "T\xe1\xbb\x95ng quan Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh Ti\xe1\xba\xbfng Trung"),
                    ("tnst", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh Tr\xe1\xba\xa3i nghi\xe1\xbb\x87m s\xc3\xa1ng t\xe1\xba\xa1o (TNST)"),
                    ("steam", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh STEAM v\xe1\xbb\x9bi C\xc3\xb4ng ngh\xe1\xbb\x87 s\xc3\xa1ng t\xe1\xba\xa1o"),
                    ("robotics", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh Robotic"),
                    ("lifeskills", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh K\xe1\xbb\xb9 n\xc4\x83ng s\xe1\xbb\x91ng"),
                    ("creative_movement", "Ch\xc6\xb0\xc6\xa1ng tr\xc3\xacnh T\xc3\xa2m v\xe1\xba\xa5n \xc4\x91\xe1\xbb\x99ng"),
                    ("schedule_2025", "Khung K\xe1\xba\xbf ho\xe1\xba\xa1ch n\xe1\xba\xb1m h\xe1\xbb\x8dc 2025-2026"),
                    ("schedule_hd", "Khung K\xe1\xba\xbf ho\xe1\xba\xa1ch H\xc4\x90 ph\xc3\xb2ng tr\xc3\xa0\xc3\xa0o n\xe1\xba\xb1m h\xe1\xbb\x8dc 2025-2026"),
                    ("whymis", "T\xe1\xba\xa1i sao ch\xe1\xbb\x8dn MIS?"),
                    ("strategy_2025_2028", "Strategy 2025-2028"),
                    ("vision_2033", "Vision 2033"),
                    ("future_ai", "Future With AI"),
                ],
                max_length=30,
                unique=True,
            ),
        ),
    ]
