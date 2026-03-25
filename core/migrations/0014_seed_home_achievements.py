from django.db import migrations


def seed_home_achievements(apps, schema_editor):
    Achievement = apps.get_model('core', 'Achievement')

    stats = [
        {
            'stat_value': '50%+',
            'stat_label': 'K12 đạt IELTS 5.0-7.5+',
            'title': 'Kết quả IELTS',
            'description': 'Học sinh lớp 12 đạt chứng chỉ IELTS 5.0-7.5+.',
            'category': 'language',
            'color': 'red',
        },
        {
            'stat_value': '50%+',
            'stat_label': 'K12 đạt HSK 3-6',
            'title': 'Thành tích HSK',
            'description': 'Học sinh lớp 12 đạt chứng chỉ HSK 3-6.',
            'category': 'language',
            'color': 'amber',
        },
        {
            'stat_value': '98%',
            'stat_label': 'Đỗ đại học hàng đầu VN',
            'title': 'Tỷ lệ đỗ Đại học',
            'description': 'Tỷ lệ trúng tuyển các trường đại học hàng đầu Việt Nam.',
            'category': 'academic',
            'color': 'green',
        },
    ]

    for item in stats:
        Achievement.objects.update_or_create(
            stat_value=item['stat_value'],
            stat_label=item['stat_label'],
            defaults={
                'title': item['title'],
                'description': item['description'],
                'icon': 'fas fa-trophy',
                'tags': '',
                'category': item['category'],
                'color': item['color'],
                'is_stat': True,
                'is_card': False,
                'is_active': True,
            }
        )


def remove_home_achievements(apps, schema_editor):
    Achievement = apps.get_model('core', 'Achievement')
    Achievement.objects.filter(
        stat_value__in=['50%+', '98%'],
        stat_label__in=[
            'K12 đạt IELTS 5.0-7.5+',
            'K12 đạt HSK 3-6',
            'Đỗ đại học hàng đầu VN',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_enable_guong_mat_menu'),
    ]

    operations = [
        migrations.RunPython(seed_home_achievements, remove_home_achievements),
    ]
