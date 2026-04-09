from django.db import migrations


def update_achievement_ielts_copy(apps, schema_editor):
    Achievement = apps.get_model("core", "Achievement")

    for achievement in Achievement.objects.all():
        changed_fields = []
        new_stat_label = (
            achievement.stat_label
            .replace("IELTS 5.0-7.5+", "IELTS 8.0")
            .replace("IELTS 5.0-7.5", "IELTS 8.0")
        )
        if new_stat_label != achievement.stat_label:
            achievement.stat_label = new_stat_label
            changed_fields.append("stat_label")
        new_description = (
            achievement.description
            .replace("IELTS 5.0-7.5+", "IELTS 8.0")
            .replace("IELTS 5.0-7.5", "IELTS 8.0")
        )
        if new_description != achievement.description:
            achievement.description = new_description
            changed_fields.append("description")
        if changed_fields:
            achievement.save(update_fields=changed_fields)


def revert_achievement_ielts_copy(apps, schema_editor):
    Achievement = apps.get_model("core", "Achievement")

    replacements = {
        "K12 đạt IELTS 8.0": "K12 đạt IELTS 5.0-7.5+",
        "Học sinh K12 đạt IELTS 8.0 & HSK 3-6": "Học sinh K12 đạt IELTS 5.0-7.5 & HSK 3-6",
        "Học sinh lớp 12 đạt chứng chỉ IELTS 8.0.": "Học sinh lớp 12 đạt chứng chỉ IELTS 5.0-7.5+.",
        "Học sinh đạt IELTS 8.0, HSK 3-6, nhiều em nhận học bổng toàn phần các trường đại học quốc tế": "Học sinh đạt IELTS 5.0-7.5, HSK 3-6, nhiều em nhận học bổng toàn phần các trường đại học quốc tế",
        "Trên 50% học sinh K12 đạt IELTS 8.0 & HSK 3-6. 15 học sinh đạt học bổng du học cao.": "Trên 50% học sinh K12 đạt IELTS 5.0-7.5 & HSK 3-6. 15 học sinh đạt học bổng du học cao.",
    }

    for achievement in Achievement.objects.all():
        changed_fields = []
        if achievement.stat_label in replacements:
            achievement.stat_label = replacements[achievement.stat_label]
            changed_fields.append("stat_label")
        if achievement.description in replacements:
            achievement.description = replacements[achievement.description]
            changed_fields.append("description")
        if changed_fields:
            achievement.save(update_fields=changed_fields)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0030_timetableupload"),
    ]

    operations = [
        migrations.RunPython(update_achievement_ielts_copy, revert_achievement_ielts_copy),
    ]
