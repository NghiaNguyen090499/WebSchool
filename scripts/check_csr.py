import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from csr.models import CSRProject, CSRImage

projects = CSRProject.objects.all()
for p in projects:
    print(f"ID={p.id}, order={p.order}, active={p.is_active}, title={p.title}")
    imgs = CSRImage.objects.filter(project=p)
    for i in imgs:
        print(f"  ImgID={i.id}, image={i.image.name}, active={i.is_active}")
print(f"\nTotal projects: {projects.count()}")
print(f"Total images: {CSRImage.objects.count()}")
