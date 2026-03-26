import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('d:/NGHIA/WebsiteSchool')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
import django; django.setup()
from news.models import News
import re

arts = News.all_objects.filter(content__icontains='misvn')
for a in arts:
    hrefs = re.findall(r'href="https?://misvn[^\"]*', a.content)
    imgs = re.findall(r'src="https?://misvn[^\"]*', a.content)
    if hrefs or imgs:
        print(f"[{a.title}]")
        print("HREFS:", hrefs)
        print("IMGS:", imgs)
