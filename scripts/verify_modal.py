import os, sys, json, re, django
sys.path.insert(0, '.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()
from django.test import RequestFactory
from about.views import page_detail
rf = RequestFactory()
req = rf.get("/about/whymis/")
resp = page_detail(req, page_type="whymis")
html = resp.content.decode("utf-8")
match = re.search(r'class="js-fd">(.*?)</script>', html, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    print(f"Modal data: {len(data)} items")
    for i, item in enumerate(data):
        title = item.get("title", "")
        content = item.get("content", "")
        print(f"  {i+1}. {title[:60]}")
        print(f"     Content: {len(content)} chars")
else:
    print("No modal JSON data found!")
