import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('d:/NGHIA/WebsiteSchool')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
import django; django.setup()
from news.models import News
import re

leaking_articles = News.objects.filter(content__icontains='misvn')
count = leaking_articles.count()
print(f'Articles with remaining MISVN string: {count}')

total_imgs = 0
total_hrefs = 0

for a in leaking_articles:
    misvn_hrefs = re.findall(r'href="https?://misvn[^\"]*', a.content)
    misvn_imgs = re.findall(r'src="https?://misvn[^\"]*', a.content)
    if misvn_hrefs: total_hrefs += len(misvn_hrefs)
    if misvn_imgs: total_imgs += len(misvn_imgs)

print(f'Leaking Image SRCs: {total_imgs}')
print(f'Leaking HREFs (cross-links): {total_hrefs}')
