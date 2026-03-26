import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = requests.get('https://misvn.edu.vn/wp-json/wp/v2/posts?per_page=1')
print("Status:", res.status_code)
if res.status_code == 200:
    print(res.json())
