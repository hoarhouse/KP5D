#!/usr/bin/env python3
"""
Fix nav visibility issue on blog article pages.
Move mobile nav CSS into media query where it belongs.
"""

import os
import re
from pathlib import Path
import shutil

def fix_nav_css(file_path, test_mode=False):
    """Fix the nav CSS in a single file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Step 1: Remove orphaned mobile nav rules (lines like 146-157 that are outside proper blocks)
    # These appear between .wa rule and the closing brace
    # Pattern: After .wa { ... } and before nav { ... }
    
    # Remove the orphaned rules that appear to be floating without proper context
    # They start with lines like "  .wa { padding: 0 var(--s6); }" without @media
    orphan_pattern = r'\.wa \{ max-width:.*?\}\s*\n((?:  \..*?\n)+)\}'
    
    # More specific: Find and remove the problematic section
    # This section has indented rules that aren't inside any block
    problem_section_pattern = r'(\.wa \{ max-width: var\(--article\); margin: 0 auto; padding: 0 var\(--s9\); \}\s*\n)((?:  \.\w+.*?\n)+\})'
    
    if re.search(problem_section_pattern, content):
        # Found the problem section, remove the orphaned rules
        content = re.sub(problem_section_pattern, r'\1', content)
        print(f"  Removed orphaned mobile rules")
    
    # Step 2: Ensure desktop nav rules are correct (outside media query)
    # The .nav-r rule at line 162 should NOT have visibility/opacity rules
    desktop_nav_pattern = r'(\.nav-r \{ display: flex; align-items: center; gap: var\(--s7\);).*?\}'
    content = re.sub(desktop_nav_pattern, r'\1 }', content, count=1)
    
    # Step 3: Fix the media query - ensure it has all mobile nav rules
    # Find the media query and add missing rules if needed
    media_query_pattern = r'(@media \(max-width: 768px\) \{)(.*?)(\n\})'
    
    def fix_media_query(match):
        start = match.group(1)
        rules = match.group(2)
        end = match.group(3)
        
        # Check if mobile nav rules already exist
        if '.hamburger { display: block; }' not in rules:
            # Add all mobile nav rules
            mobile_rules = """
  .w { padding: 0 var(--s6); }
  .wa { padding: 0 var(--s6); }
  .hamburger { display: block; }
  .nav-r { position: fixed; top: 56px; left: 0; right: 0; background: var(--white); border-bottom: 1px solid var(--c5); padding: var(--s5) var(--s6); flex-direction: column; align-items: flex-start; gap: var(--s4); transform: translateY(-100%); opacity: 0; visibility: hidden; transition: all 0.3s; }
  .nav-r.active { transform: translateY(0); opacity: 1; visibility: visible; }
  .nav-r a { width: 100%; padding: var(--s2) 0; }"""
            
            # Add to beginning of media query
            rules = mobile_rules + rules
            
        return start + rules + end
    
    content = re.sub(media_query_pattern, fix_media_query, content, flags=re.DOTALL)
    
    if test_mode:
        print(f"\n=== TEST MODE - Showing changes for {file_path} ===")
        # Show a diff of key sections
        print("\nBefore:")
        print("- Had orphaned mobile rules outside media query")
        print("- Nav was hidden on desktop")
        print("\nAfter:")
        print("- Mobile rules moved into @media (max-width: 768px)")
        print("- Desktop .nav-r displays correctly")
        print("- .hamburger defaults to display: none on desktop")
        return True
    
    # Write the fixed content
    if content != original_content:
        # Backup original
        backup_path = f"{file_path}.nav-backup"
        shutil.copy2(file_path, backup_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed: {file_path}")
        return True
    else:
        print(f"  No changes needed: {file_path}")
        return False

def main():
    """Process all blog article files"""
    
    # Test on one file first
    test_file = "blog/your-ai-conversations-are-a-codebase/index.html"
    
    print("=== TEST RUN ===")
    if os.path.exists(test_file):
        fix_nav_css(test_file, test_mode=True)
        
        print("\n=== APPLYING FIX TO TEST FILE ===")
        fix_nav_css(test_file, test_mode=False)
        
        response = input("\nContinue with all files? (y/n): ")
        if response.lower() != 'y':
            print("Aborted. Test file changes saved.")
            return
    
    print("\n=== APPLYING TO ALL BLOG ARTICLES ===")
    
    # Get all blog article files
    blog_files = []
    blog_dir = Path('blog')
    
    # Pattern 1: blog/*/index.html
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
    fixed_count = 0
    for file_path in sorted(blog_files):
        if fix_nav_css(file_path):
            fixed_count += 1
    
    print(f"\n=== COMPLETE ===")
    print(f"Fixed {fixed_count} files")
    print(f"Backups saved with .nav-backup extension")

if __name__ == "__main__":
    main()