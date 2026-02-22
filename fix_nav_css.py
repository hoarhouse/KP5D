#!/usr/bin/env python3
"""
Fix nav visibility issue by removing orphaned CSS and ensuring proper media query structure
"""

import os
import re
from pathlib import Path

def fix_nav_css_in_file(file_path):
    """Fix the nav CSS structure in a single file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find and remove the orphaned CSS block (lines with indented rules after .wa but before nav)
    # These are typically lines like:
    #   .wa { padding: 0 var(--s6); }
    #   .hamburger { display: block; }
    #   ... etc ...
    # }
    # Without a proper @media wrapper
    
    fixed_lines = []
    skip_orphan = False
    orphan_start = -1
    
    for i, line in enumerate(lines):
        # Detect start of orphaned block - indented CSS after .wa definition
        if i > 0 and '.wa { max-width: var(--article)' in lines[i-1] and line.startswith('  .'):
            skip_orphan = True
            orphan_start = i
            print(f"  Found orphaned CSS starting at line {i+1}")
            continue
        
        # Detect end of orphaned block - single closing brace
        if skip_orphan and line.strip() == '}':
            skip_orphan = False
            print(f"  Removed orphaned CSS block (lines {orphan_start+1}-{i+1})")
            continue
        
        # Skip lines in orphaned block
        if skip_orphan:
            continue
            
        fixed_lines.append(line)
    
    # Now ensure the media query has the correct mobile rules
    content = ''.join(fixed_lines)
    
    # Find the media query and ensure it has all needed rules
    media_pattern = r'@media \(max-width: 768px\) \{([^}]*(?:\{[^}]*\}[^}]*)*)\}'
    
    def fix_media_query_content(match):
        rules = match.group(1)
        
        # Check what's missing and add it
        needed_rules = []
        
        if '.w { padding: 0 var(--s6)' not in rules:
            needed_rules.append('  .w { padding: 0 var(--s6); }')
        if '.wa { padding: 0 var(--s6)' not in rules:
            needed_rules.append('  .wa { padding: 0 var(--s6); }')
        if '.hamburger { display: block' not in rules:
            needed_rules.append('  .hamburger { display: block; }')
        if 'position: fixed; top: 56px' not in rules:
            needed_rules.append('  .nav-r { position: fixed; top: 56px; left: 0; right: 0; background: var(--white); border-bottom: 1px solid var(--c5); padding: var(--s5) var(--s6); flex-direction: column; align-items: flex-start; gap: var(--s4); transform: translateY(-100%); opacity: 0; visibility: hidden; transition: all 0.3s; }')
        if '.nav-r.active { transform: translateY(0)' not in rules:
            needed_rules.append('  .nav-r.active { transform: translateY(0); opacity: 1; visibility: visible; }')
        if '.nav-r a { width: 100%' not in rules and '.nav-r a:not(.btn)' in rules:
            # Need to add the general rule for all nav links in mobile
            needed_rules.append('  .nav-r a { width: 100%; padding: var(--s2) 0; }')
        
        if needed_rules:
            # Add the rules at the beginning of the media query
            new_rules = '\n' + '\n'.join(needed_rules) + rules
            return '@media (max-width: 768px) {' + new_rules + '}'
        else:
            return match.group(0)
    
    content = re.sub(media_pattern, fix_media_query_content, content, flags=re.DOTALL)
    
    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Fix all blog article files"""
    
    print("=== FIXING NAV CSS IN BLOG ARTICLES ===\n")
    
    # Test on one file first
    test_file = "blog/your-ai-conversations-are-a-codebase/index.html"
    
    if os.path.exists(test_file):
        print(f"Testing on: {test_file}")
        fix_nav_css_in_file(test_file)
        print(f"✓ Fixed: {test_file}\n")
        
        # Show verification
        os.system(f"echo 'Checking fixed file:' && grep -c '\\.hamburger.*display: none' '{test_file}' && echo 'Has hamburger display:none' && grep -c 'visibility: hidden' '{test_file}' && echo 'visibility:hidden count'")
        
        response = input("\nProceed with all files? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Process all blog article files
    blog_dir = Path('blog')
    processed = 0
    
    for subdir in blog_dir.iterdir():
        if subdir.is_dir():
            index_file = subdir / 'index.html'
            if index_file.exists():
                print(f"Fixing: {index_file}")
                fix_nav_css_in_file(str(index_file))
                processed += 1
    
    # Also process blog/*.html (but not index.html)
    for html_file in blog_dir.glob('*.html'):
        if html_file.name != 'index.html':
            print(f"Fixing: {html_file}")
            fix_nav_css_in_file(str(html_file))
            processed += 1
    
    print(f"\n=== COMPLETE ===")
    print(f"Processed {processed} files")

if __name__ == "__main__":
    main()