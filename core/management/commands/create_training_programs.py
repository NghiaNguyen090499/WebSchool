import json
from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import TrainingProgram, TrainingProgramGroup
from core.utils.program_content import get_program_block, get_program_year

DATA_PATH = Path(__file__).with_name('training_programs_data.json')
TARGET_BLOCK_BY_SLUG = {
    'tieng-anh-tai-nang': 'overview_english',
    'tieng-trung-tai-nang': 'overview_chinese',
}


def _target_lines_from_block(block):
    targets = block.get('targets', {}) if isinstance(block, dict) else {}
    standard = targets.get('standard', {})
    talent = targets.get('talent', {})
    talent_thpt = targets.get('talent_thpt', {})

    lines = []
    if standard.get('ielts') or standard.get('hsk'):
        lines.append(
            f"Tuyến chuẩn: IELTS {standard.get('ielts', 'NEED_CONFIRM')}, "
            f"HSK {standard.get('hsk', 'NEED_CONFIRM')}"
        )
    if talent.get('ielts') or talent.get('hsk'):
        lines.append(
            f"Tuyến tài năng: IELTS {talent.get('ielts', 'NEED_CONFIRM')}, "
            f"HSK {talent.get('hsk', 'NEED_CONFIRM')}"
        )

    if talent_thpt.get('ielts') or talent_thpt.get('hsk'):
        thpt_segments = []
        if talent_thpt.get('ielts'):
            thpt_segments.append(f"IELTS {talent_thpt['ielts']}")
        if talent_thpt.get('hsk'):
            thpt_segments.append(f"HSK {talent_thpt['hsk']}")
        lines.append(f"Tuyến tài năng THPT: {', '.join(thpt_segments)}")
    return lines


def _strip_target_lines(text):
    lines = [line.strip() for line in (text or '').splitlines() if line.strip()]
    return [line for line in lines if 'IELTS' not in line and 'HSK' not in line]


def _apply_target_profile_overrides(program_payload):
    block_key = TARGET_BLOCK_BY_SLUG.get(program_payload.get('slug'))
    if not block_key:
        return

    block = get_program_block(block_key)
    target_lines = _target_lines_from_block(block)
    if not target_lines:
        return

    curriculum_lines = _strip_target_lines(program_payload.get('curriculum', ''))
    highlight_lines = _strip_target_lines(program_payload.get('highlights', ''))

    program_payload['curriculum'] = '\n'.join(curriculum_lines + target_lines)
    program_payload['highlights'] = '\n'.join(highlight_lines + target_lines)
    program_payload['achievements'] = '\n'.join(
        [f"Chuẩn đầu ra {line.lower()}" for line in target_lines]
    )


class Command(BaseCommand):
    help = 'Create specialized training programs based on MIS program data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Creating training programs...'))

        if not DATA_PATH.exists():
            raise FileNotFoundError(f'Missing data file: {DATA_PATH}')

        data = json.loads(DATA_PATH.read_text(encoding='utf-8-sig'))
        group_data = dict(data.get('group', {}))
        group_slug = group_data.pop('slug', None)
        if not group_slug:
            raise ValueError('Missing group.slug in training_programs_data.json')

        group, _ = TrainingProgramGroup.objects.update_or_create(
            slug=group_slug,
            defaults=group_data,
        )
        TrainingProgramGroup.objects.exclude(slug=group_slug).update(is_active=False)

        programs_data = list(data.get('programs', []))
        for item in programs_data:
            _apply_target_profile_overrides(item)

        active_slugs = [item.get('slug') for item in programs_data if item.get('slug')]
        allowed_fields = {
            field.name
            for field in TrainingProgram._meta.concrete_fields
            if field.name not in {'id', 'group'}
        }

        created_count = 0
        updated_count = 0

        for item in programs_data:
            slug = item.get('slug')
            if not slug:
                continue

            defaults = {key: value for key, value in item.items() if key in allowed_fields}
            defaults.pop('slug', None)
            defaults['group'] = group

            program, created = TrainingProgram.objects.update_or_create(
                slug=slug,
                defaults=defaults,
            )

            if created:
                created_count += 1
                print(f'[+] Created: {slug}')
            else:
                updated_count += 1
                print(f'[~] Updated: {slug}')

        TrainingProgram.objects.exclude(slug__in=active_slugs).update(is_active=False)

        print(
            f'\n[OK] Successfully processed {len(programs_data)} training programs: '
            f'{created_count} created, {updated_count} updated ({get_program_year()})'
        )
