# -*- coding: utf-8 -*-
from django.db import migrations


def update_training_program_names(apps, schema_editor):
    TrainingProgram = apps.get_model('core', 'TrainingProgram')
    updates = {
        'steam-chat-luong-cao': {
            'name': 'HỆ STEAM & CHẤT LƯỢNG CAO CÔNG NGHỆ',
            'short_name': 'HỆ STEAM & CHẤT LƯỢNG CAO CÔNG NGHỆ',
        },
        'toan-tai-nang-cong-nghe-moi': {
            'name': 'HỆ TÀI NĂNG TOÁN HỌC',
            'short_name': 'HỆ TÀI NĂNG TOÁN HỌC',
        },
        'tieng-anh-tai-nang': {
            'name': 'HỆ TIẾNG ANH TÀI NĂNG',
            'short_name': 'HỆ TIẾNG ANH TÀI NĂNG',
        },
        'tieng-trung-tai-nang': {
            'name': 'HỆ TÀI NĂNG NGÔN NGỮ - TIẾNG TRUNG',
            'short_name': 'HỆ TÀI NĂNG NGÔN NGỮ - TIẾNG TRUNG',
        },
    }

    for slug, values in updates.items():
        TrainingProgram.objects.filter(slug=slug).update(**values)


def deactivate_placeholder_menu_items(apps, schema_editor):
    MenuItem = apps.get_model('core', 'MenuItem')
    items = MenuItem.objects.filter(link__in=['', '#'])
    for item in items:
        if item.children.exists():
            continue
        if item.is_active:
            item.is_active = False
            item.save(update_fields=['is_active'])


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0011_mediaasset'),
    ]

    operations = [
        migrations.RunPython(update_training_program_names, migrations.RunPython.noop),
        migrations.RunPython(deactivate_placeholder_menu_items, migrations.RunPython.noop),
    ]
