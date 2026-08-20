from decimal import Decimal
from django.core.management.base import BaseCommand
from core.models import Category, Course, Instructor

class Command(BaseCommand):
    help = 'Create safe demo catalog records; never creates admin users or reads passwords.'

    def handle(self, *args, **options):
        categories = {}
        for name, description in [
            ('Leadership', 'Executive learning for modern leaders.'),
            ('Strategy', 'Clear thinking for complex decisions.'),
            ('Communication', 'Presence, influence, and meaningful connection.'),
        ]:
            categories[name], _ = Category.objects.get_or_create(name=name, defaults={'description': description})
        instructor, _ = Instructor.objects.get_or_create(
            name='CourseHub Faculty',
            defaults={'bio': 'Practitioners and educators shaping the next generation of work.'},
        )
        catalog = [
            ('The Executive Mindset', 'A practical masterclass for decisive, thoughtful leadership.', 'Leadership', Decimal('0.00')),
            ('The Art of Clear Thinking', 'Build a sharper mental model for complex decisions.', 'Strategy', Decimal('149.00')),
            ('Presence & Influence', 'Communicate with warmth, clarity, and authority.', 'Communication', Decimal('189.00')),
        ]
        for title, description, category, price in catalog:
            course, created = Course.objects.get_or_create(
                title=title,
                defaults={'description': description, 'category': categories[category], 'instructor': instructor, 'price': price, 'is_published': True},
            )
            self.stdout.write(self.style.SUCCESS(f'{course.title}: {"created" if created else "existing"}'))
        self.stdout.write(self.style.SUCCESS('Premium CourseHub catalog ready.'))
