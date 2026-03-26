import urllib.request as r
import re, os
import concurrent.futures

BASE_URL = 'https://tkb.misvn.edu.vn/'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(BASE_DIR, 'media', 'tkb')
os.makedirs(DEST, exist_ok=True)

visited = set()
to_visit = set(['']) # root

def fetch(path):
    if path in visited: return
    visited.add(path)
    try:
        url = BASE_URL + path
        resp = r.urlopen(url)
        content = resp.read()
        
        # save
        save_path = os.path.join(DEST, path if path else 'index.htm')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(content)
            
        print(f"Downloaded: {path}")
        
        # simple link extraction for static timetable
        if path.endswith('.htm') or path.endswith('.html') or not path:
            text = content.decode('utf-8', errors='ignore')
            links = re.findall(r'(?:src|href)=[\'"]([a-zA-Z0-9_\-\.]+?(?:\.htm|\.css|\.js|\.png|\.jpg|\.gif))[\'"]', text, re.I)
            for link in links:
                if link not in visited:
                    to_visit.add(link)
    except Exception as e:
        print(f"Failed {path}: {e}")

while to_visit:
    path = to_visit.pop()
    fetch(path)

print("Done crawling!")
