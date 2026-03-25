from django.db import migrations


def enable_guong_mat_menu(apps, schema_editor):
    MenuItem = apps.get_model('core', 'MenuItem')
    MenuItem.objects.filter(
        title__iexact='Gương mặt MISers'
    ).update(
        link='/guong-mat-misers/',
        is_active=True
    )


def disable_guong_mat_menu(apps, schema_editor):
    MenuItem = apps.get_model('core', 'MenuItem')
    MenuItem.objects.filter(
        title__iexact='Gương mặt MISers',
        link='/guong-mat-misers/',
    ).update(
        is_active=False
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_update_training_program_names_and_menu_items'),
    ]

    operations = [
        migrations.RunPython(enable_guong_mat_menu, disable_guong_mat_menu),
    ]
