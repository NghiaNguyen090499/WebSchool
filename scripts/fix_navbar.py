#!/usr/bin/env python
"""Fix navbar template - run with: python scripts/fix_navbar.py"""
import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
django.setup()

from django.template import engines

content = open('templates/core/includes/navbar.html', encoding='utf-8').read()
lines = content.split('\n')

print(f"Total lines: {len(lines)}")

# Line 377 (0-indexed: 376) has the extra endif
print(f"Line 377: {lines[376].strip()}")

engine = engines['django']

# Test removing line 377
test_lines = lines.copy()
del test_lines[376]  # Remove line 377 (0-indexed)
test_content = '\n'.join(test_lines)

try:
    template = engine.from_string(test_content)
    print("SUCCESS: Removing line 377 fixes the template!")
    
    # Save the fixed file
    with open('templates/core/includes/navbar.html', 'w', encoding='utf-8') as f:
        f.write(test_content)
    print("Fixed file saved!")
except Exception as e:
    print(f"Removing line 377 didn't help: {e}")
