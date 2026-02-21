#!/usr/bin/env python3
"""
Fix all 17 blog article pages
Fixes 4 issues: duplicate media queries, missing main tag, footer structure, placeholder links
"""

import os
import re
from pathlib import Path

def fix_article_file(file_path):
    """Fix all issues in a single blog article file"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Remove duplicate media queries (keep only the last/most complete one)
    # Count media queries
    media_pattern = r'@media \(max-width: 768px\) \{[^}]*(?:\{[^}]*\}[^}]*)*\}'
    media_matches = list(re.finditer(media_pattern, content, re.MULTILINE | re.DOTALL))
    
    if len(media_matches) > 1:
        print(f"  Found {len(media_matches)} media queries, consolidating...")
        # Remove all but the last one (which typically has all the rules)
        for match in media_matches[:-1]:
            content = content[:match.start()] + content[match.end():]
            # Recalculate positions after removal
            media_matches = list(re.finditer(media_pattern, content, re.MULTILINE | re.DOTALL))
    
    # Fix 2: Add semantic <main> wrapper (if not already present)
    if '<main>' not in content:
        print("  Adding <main> wrapper...")
        # Add <main> after </nav>
        content = content.replace('</nav>', '</nav>\n\n<main>')
        
        # Add </main> before footer
        # Look for footer patterns
        if '<div class="w"><footer>' in content:
            content = content.replace('<div class="w"><footer>', '</main>\n\n<div class="w"><footer>')
        elif re.search(r'^\s*<footer>', content, re.MULTILINE):
            content = re.sub(r'(^\s*<footer>)', r'</main>\n\n\1', content, count=1, flags=re.MULTILINE)
    
    # Fix 3: Fix footer structure (footer should be outer element)
    # Change <div class="w"><footer>...</footer></div> to <footer><div class="w">...</div></footer>
    if '<div class="w"><footer>' in content:
        print("  Fixing footer structure...")
        content = content.replace('<div class="w"><footer>', '<footer>\n  <div class="w">')
        content = content.replace('</footer></div>', '  </div>\n</footer>')
    
    # Fix 4: Update placeholder footer links
    # Only update if they are placeholders (href="#")
    if 'href="#"' in content:
        print("  Updating placeholder links...")
        content = content.replace('href="#">GitHub</a>', 'href="https://github.com/hoarhouse/KP5D">GitHub</a>')
        content = content.replace('href="#">Docs</a>', 'href="https://kept.work/docs/">Docs</a>')
        content = content.replace('href="#">Privacy</a>', 'href="https://kept.work/privacy/">Privacy</a>')
    
    # Only write if something changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed: {file_path}")
    else:
        print(f"  ✓ No changes needed: {file_path}")
    
    return True

def main():
    """Process all blog article files"""
    print("=== APPLYING FIXES TO ALL BLOG ARTICLE FILES ===")
    print()
    
    # Get all blog article files
    blog_files = []
    
    # Pattern 1: blog/*/index.html
    blog_dir = Path('blog')
    for subdir in blog_dir.iterdir():
        if subdir.is_dir():
            index_file = subdir / 'index.html'
            if index_file.exists():
                blog_files.append(str(index_file))
    
    # Pattern 2: blog/*.html (but not blog/index.html)
    for html_file in blog_dir.glob('*.html'):
        if html_file.name != 'index.html':
            blog_files.append(str(html_file))
    
    # Process each file
    count = 0
    for file_path in sorted(blog_files):
        if fix_article_file(file_path):
            count += 1
    
    print()
    print("=== COMPLETE ===")
    print(f"Processed {count} files")

if __name__ == "__main__":
    main()