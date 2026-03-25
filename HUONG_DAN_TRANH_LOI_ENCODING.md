# HƯỚNG DẪN: Tránh Lỗi Encoding Tiếng Việt

## Vấn đề gặp phải

Khi làm việc với tiếng Việt trong Django, có thể gặp lỗi encoding khiến text hiển thị sai như:
- "Tên cơ sở" → "TA¦n c'­ s ¯Y"
- "Địa chỉ" → "Ž? ¯<a ch ¯%"

## Nguyên nhân

1. Editor không sử dụng UTF-8
2. Copy-paste từ nguồn khác encoding
3. File được mở bằng editor sai encoding

## Giải pháp

### 1. Cấu hình Editor (VS Code)

Thêm vào `settings.json`:

```json
{
  "files.encoding": "utf8",
  "files.eol": "\n",
  "files.autoGuessEncoding": false
}
```

### 2. Thêm header vào file Python

Luôn thêm dòng này ở đầu file Python:

```python
# -*- coding: utf-8 -*-
```

### 3. Git configuration

Tạo file `.gitattributes` ở root project:

```
*.py text eol=lf encoding=utf-8
*.html text eol=lf encoding=utf-8
*.css text eol=lf encoding=utf-8
*.js text eol=lf encoding=utf-8
```

### 4. Kiểm tra encoding của file

**Windows (PowerShell)**:
```powershell
Get-Content "path/to/file.py" -Encoding utf8 | Select-Object -First 5
```

**Linux/Mac**:
```bash
file -bi path/to/file.py
```

### 5. Nguyên tắc khi code

✅ **NÊN**:
- Sử dụng Unicode strings cho tiếng Việt
- Khai báo encoding UTF-8 ở đầu file
- Sử dụng `verbose_name="Tên tiếng Việt"` trực tiếp

❌ **KHÔNG NÊN**:
- Copy-paste từ Word/Excel
- Mở file bằng Notepad (Windows)
- Thay đổi encoding khi file đã có content

### 6. Sửa lỗi nếu xảy ra

Nếu file bị lỗi encoding:

**Cách 1: Sử dụng script Python**
```python
# fix_encoding.py
with open('file.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace corrupted text
content = content.replace('TA¦n c\\'­ s ¯Y', 'Tên cơ sở')

with open('file.py', 'w', encoding='utf-8') as f:
    f.write(content)
```

**Cách 2: Manual**
1. Backup file
2. Copy toàn bộ nội dung
3. Xóa file cũ
4. Tạo file mới với UTF-8
5. Paste và sửa lại các text tiếng Việt

### 7. Kiểm tra sau khi sửa

```bash
# Kiểm tra Django
python manage.py check

# Tạo migrations (nếu có thay đổi)
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Best Practices

1. **Luôn sử dụng UTF-8** cho tất cả files
2. **Thêm encoding declaration** ở đầu file Python
3. **Kiểm tra editor settings** trước khi code
4. **Test ngay** sau khi thêm tiếng Việt
5. **Commit thường xuyên** để dễ rollback nếu cần

## Checklist trước khi commit

- [ ] File được mở bằng UTF-8
- [ ] Tiếng Việt hiển thị đúng trong editor
- [ ] `python manage.py check` không có lỗi
- [ ] Django admin hiển thị đúng (nếu thay đổi models)
- [ ] Git diff không có ký tự lạ

---

📌 **Lưu ý**: Nếu gặp lỗi encoding phức tạp, sử dụng script Python để sửa tự động thay vì sửa thủ công.
