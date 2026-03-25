from django.db import migrations


def seed_award_cards(apps, schema_editor):
    Achievement = apps.get_model('core', 'Achievement')
    awards = [
        {
            'title': 'Top 10 Thương hiệu tiêu biểu Châu Á - Thái Bình Dương',
            'description': 'Vinh danh 2025 tại chương trình Thương hiệu tiêu biểu Châu Á - Thái Bình Dương.',
            'icon': 'fas fa-award',
            'tags': '2025',
            'category': 'competition',
            'color': 'red',
        },
        {
            'title': 'Top 50 Thương hiệu nổi tiếng ASEAN',
            'description': 'Vinh danh 2025 tại chương trình Thương hiệu nổi tiếng ASEAN.',
            'icon': 'fas fa-globe',
            'tags': '2025',
            'category': 'competition',
            'color': 'amber',
        },
        {
            'title': 'Sản phẩm & Dịch vụ Chất lượng Vàng Việt Nam',
            'description': 'Vinh danh 2025 tại chương trình Chất lượng Vàng Việt Nam.',
            'icon': 'fas fa-medal',
            'tags': '2025',
            'category': 'competition',
            'color': 'red',
        },
    ]

    for item in awards:
        Achievement.objects.update_or_create(
            title=item['title'],
            defaults={
                'description': item['description'],
                'stat_value': '',
                'stat_label': '',
                'icon': item['icon'],
                'tags': item['tags'],
                'category': item['category'],
                'color': item['color'],
                'is_stat': False,
                'is_card': True,
                'is_active': True,
            }
        )


def remove_award_cards(apps, schema_editor):
    Achievement = apps.get_model('core', 'Achievement')
    Achievement.objects.filter(
        title__in=[
            'Top 10 Thương hiệu tiêu biểu Châu Á - Thái Bình Dương',
            'Top 50 Thương hiệu nổi tiếng ASEAN',
            'Sản phẩm & Dịch vụ Chất lượng Vàng Việt Nam',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_seed_home_achievements'),
    ]

    operations = [
        migrations.RunPython(seed_award_cards, remove_award_cards),
    ]
