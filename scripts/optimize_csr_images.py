"""
Optimize CSR gallery images:
1. Create web-optimized versions (max 1200px wide, quality 82, WebP)
2. Create thumbnail versions (max 200px wide, quality 75, WebP)
"""
import os
from PIL import Image

SOURCE_DIR = r"d:\NGHIA\WebsiteSchool\media\csr\ngoi-truong-lon"
OUTPUT_WEB = os.path.join(SOURCE_DIR, "web")
OUTPUT_THUMB = os.path.join(SOURCE_DIR, "thumb")

os.makedirs(OUTPUT_WEB, exist_ok=True)
os.makedirs(OUTPUT_THUMB, exist_ok=True)

IMAGES = [
    'MIS00390.jpg', 'MIS00421.jpg', 'DSCF9287.jpg', 'IMG_0110.jpg',
    'MIS00657.jpg', 'MIS00827.jpg', 'DSCF9350.jpg', 'MIS01168.jpg',
    'IMG_0487.jpg', 'MIS01377.jpg', 'MIS00999.jpg', 'MIS01535.jpg'
]

WEB_MAX_WIDTH = 1200
WEB_QUALITY = 82
THUMB_MAX_WIDTH = 200
THUMB_QUALITY = 75

total_original = 0
total_web = 0
total_thumb = 0

for filename in IMAGES:
    src = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(src):
        print(f"SKIP: {filename} not found")
        continue
    
    orig_size = os.path.getsize(src)
    total_original += orig_size
    
    img = Image.open(src)
    img = img.convert('RGB')
    
    name = os.path.splitext(filename)[0]
    
    # Web version
    web_path = os.path.join(OUTPUT_WEB, f"{name}.webp")
    w, h = img.size
    if w > WEB_MAX_WIDTH:
        ratio = WEB_MAX_WIDTH / w
        new_size = (WEB_MAX_WIDTH, int(h * ratio))
        web_img = img.resize(new_size, Image.LANCZOS)
    else:
        web_img = img.copy()
    web_img.save(web_path, 'WEBP', quality=WEB_QUALITY, method=4)
    web_size = os.path.getsize(web_path)
    total_web += web_size
    
    # Thumbnail version
    thumb_path = os.path.join(OUTPUT_THUMB, f"{name}.webp")
    ratio = THUMB_MAX_WIDTH / w
    thumb_size_calc = (THUMB_MAX_WIDTH, int(h * ratio))
    thumb_img = img.resize(thumb_size_calc, Image.LANCZOS)
    thumb_img.save(thumb_path, 'WEBP', quality=THUMB_QUALITY, method=4)
    t_size = os.path.getsize(thumb_path)
    total_thumb += t_size
    
    print(f"{filename}: {orig_size//1024}KB -> web: {web_size//1024}KB, thumb: {t_size//1024}KB")

print(f"\n{'='*60}")
print(f"ORIGINAL TOTAL: {total_original/1024/1024:.1f}MB")
print(f"WEB TOTAL:      {total_web/1024/1024:.1f}MB  (giam {(1-total_web/total_original)*100:.0f}%)")
print(f"THUMB TOTAL:    {total_thumb/1024/1024:.1f}MB")
print(f"ALL OPTIMIZED:  {(total_web+total_thumb)/1024/1024:.1f}MB  (giam {(1-(total_web+total_thumb)/(total_original*2))*100:.0f}% so voi tai ca 2)")
