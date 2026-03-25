from django.core.management.base import BaseCommand
from core.models import CoreValue


class Command(BaseCommand):
    help = 'Add core values based on MIS website information'

    def handle(self, *args, **options):
        # Dữ liệu Core Values dựa trên website MIS
        core_values_data = [
            {
                'title': 'Học để tự do, sáng tạo',
                'description': 'MIS khuyến khích học sinh phát triển tư duy độc lập, sáng tạo và tự do trong học tập, tạo nền tảng cho sự phát triển toàn diện.',
                'icon': 'fas fa-lightbulb',
                'order': 1
            },
            {
                'title': 'Học để Hạnh phúc',
                'description': 'Giáo dục tại MIS không chỉ là truyền đạt kiến thức mà còn là nuôi dưỡng niềm vui, hạnh phúc trong học tập và cuộc sống.',
                'icon': 'fas fa-heart',
                'order': 2
            },
            {
                'title': 'Thông minh để Hạnh phúc',
                'description': 'Phát triển trí tuệ đa dạng giúp học sinh không chỉ thông minh mà còn biết cách sử dụng trí tuệ để tạo ra hạnh phúc cho bản thân và cộng đồng.',
                'icon': 'fas fa-brain',
                'order': 3
            },
            {
                'title': 'Đa Trí Tuệ',
                'description': 'MIS áp dụng lý thuyết Đa Trí Tuệ, phát triển toàn diện 8 loại trí thông minh: ngôn ngữ, logic-toán học, không gian, vận động, âm nhạc, giao tiếp, nội tâm và tự nhiên.',
                'icon': 'fas fa-star',
                'order': 4
            },
            {
                'title': 'Văn minh – Hạnh phúc',
                'description': 'MIS hướng tới xây dựng một môi trường giáo dục văn minh, nơi mọi thành viên đều cảm thấy hạnh phúc, được tôn trọng và phát triển.',
                'icon': 'fas fa-dove',
                'order': 5
            },
            {
                'title': 'Thông minh – Xanh – Sáng tạo',
                'description': 'MIS xây dựng môi trường học tập thông minh, thân thiện với môi trường và khuyến khích sáng tạo trong mọi hoạt động giáo dục.',
                'icon': 'fas fa-leaf',
                'order': 6
            },
            {
                'title': 'Giáo dục khai phóng',
                'description': 'Chương trình giáo dục khai phóng giúp học sinh phát triển tư duy phản biện, khả năng tự học và sẵn sàng đón nhận những thách thức mới.',
                'icon': 'fas fa-book-open',
                'order': 7
            },
            {
                'title': 'Học tập hợp tác',
                'description': 'MIS chú trọng phương pháp học tập hợp tác (HTHT), giúp học sinh phát triển kỹ năng làm việc nhóm, giao tiếp và giải quyết vấn đề.',
                'icon': 'fas fa-users',
                'order': 8
            },
        ]

        created_count = 0
        updated_count = 0

        for value_data in core_values_data:
            core_value, created = CoreValue.objects.update_or_create(
                title=value_data['title'],
                defaults={
                    'description': value_data['description'],
                    'icon': value_data['icon'],
                    'order': value_data['order']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {core_value.title}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated: {core_value.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully processed {len(core_values_data)} core values: '
                f'{created_count} created, {updated_count} updated'
            )
        )







