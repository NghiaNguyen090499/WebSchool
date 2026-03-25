import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from about.models import AboutPage, AboutSection

page = AboutPage.objects.filter(page_type='whymis').first()
if page:
    print(f"Page: {page.title}")
    print(f"Page image: {page.image.name if page.image else 'None'}")
    print(f"Page content: {page.content[:200] if page.content else 'None'}")
    print(f"\nSections:")
    for s in page.sections.all().order_by('order'):
        print(f"  order={s.order} layout={s.layout} title={s.title}")
        print(f"    eyebrow={s.eyebrow}")
        print(f"    subtitle={s.subtitle[:80] if s.subtitle else 'None'}")
        print(f"    content={s.content[:120] if s.content else 'None'}")
        print(f"    image={s.image.name if s.image else 'None'}")
        print(f"    kpi={s.kpi[:80] if s.kpi else 'None'}")
        print(f"    timeline={s.timeline[:80] if s.timeline else 'None'}")
        print()
else:
    print("No whymis page found")
