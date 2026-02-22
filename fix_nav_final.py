#!/usr/bin/env python3
"""
Fix nav visibility by removing orphaned CSS rules and ensuring proper structure
"""

import os
import re
from pathlib import Path

def fix_article_nav(file_path):
    """Fix nav CSS in a single article file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the orphaned CSS block that sits between .wa definition and nav
    # This is the problematic section with indented rules without proper wrapper
    # Pattern: .wa { max-width... }\n  .wa { padding... }\n  .hamburger...\n}
    
    # Replace the broken section with just the .wa definition
    pattern = r'(\.wa \{ max-width: var\(--article\); margin: 0 auto; padding: 0 var\(--s9\); \})\s*\n(?:  \..*?\n)+\}'
    content = re.sub(pattern, r'\1', content, flags=re.MULTILINE)
    
    # Ensure desktop .nav-r is visible (no visibility/opacity rules)
    # Find the desktop .nav-r rule and ensure it's correct
    content = re.sub(
        r'\.nav-r \{ display: flex; align-items: center; gap: var\(--s7\);.*?\}',
        '.nav-r { display: flex; align-items: center; gap: var(--s7); }',
        content,
        count=1
    )
    
    # Ensure .hamburger defaults to display: none on desktop
    if '.hamburger { display: none;' not in content:
        # Find the hamburger rule and ensure it starts with display: none
        content = re.sub(
            r'\.hamburger \{[^}]*\}',
            '.hamburger { display: none; background: none; border: none; cursor: pointer; padding: var(--s2); }',
            content,
            count=1
        )
    
    # Ensure media query has proper mobile rules
    # Find media query and check its content
    media_match = re.search(r'@media \(max-width: 768px\) \{([^}]*(?:\{[^}]*\}[^}]*)*)\}', content, re.DOTALL)
    
    if media_match:
        media_content = media_match.group(1)
        
        # Check if essential mobile rules are missing
        needs_update = False
        new_rules = []
        
        if '.w { padding: 0 var(--s6)' not in media_content:
            new_rules.append('  .w { padding: 0 var(--s6); }')
            needs_update = True
        
        if '.wa { padding: 0 var(--s6)' not in media_content:
            new_rules.append('  .wa { padding: 0 var(--s6); }')
            needs_update = True
            
        if '.hamburger { display: block' not in media_content:
            new_rules.append('  .hamburger { display: block; }')
            needs_update = True
            
        if 'position: fixed; top: 56px' not in media_content:
            new_rules.append('  .nav-r { position: fixed; top: 56px; left: 0; right: 0; background: var(--white); border-bottom: 1px solid var(--c5); padding: var(--s5) var(--s6); flex-direction: column; align-items: flex-start; gap: var(--s4); transform: translateY(-100%); opacity: 0; visibility: hidden; transition: all 0.3s; }')
            needs_update = True
            
        if '.nav-r.active { transform: translateY(0)' not in media_content:
            new_rules.append('  .nav-r.active { transform: translateY(0); opacity: 1; visibility: visible; }')
            needs_update = True
        
        if needs_update:
            # Add new rules at the beginning of media query
            new_media = '@media (max-width: 768px) {\n' + '\n'.join(new_rules) + media_content + '}'
            content = content[:media_match.start()] + new_media + content[media_match.end():]
    
    # Save the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Process all blog article files"""
    
    print("=== FIXING NAV CSS IN ALL BLOG ARTICLES ===\n")
    
    # Get all blog article files  
    blog_dir = Path('blog')
    files_to_fix = []
    
    # Get blog/*/index.html
    for subdir in blog_dir.iterdir():
        if subdir.is_dir():
            index_file = subdir / 'index.html'
            if index_file.exists():
                files_to_fix.append(str(index_file))
    
    # Get blog/*.html (except index.html)
    for html_file in blog_dir.glob('*.html'):
        if html_file.name != 'index.html':
            files_to_fix.append(str(html_file))
    
    # Process each file
    for file_path in sorted(files_to_fix):
        print(f"Fixing: {file_path}")
        fix_article_nav(file_path)
        print(f"  ✓ Done")
    
    print(f"\n=== COMPLETE ===")
    print(f"Fixed {len(files_to_fix)} files")

if __name__ == "__main__":
    main()