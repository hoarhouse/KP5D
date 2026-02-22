#!/usr/bin/env python3
"""
Remove orphaned CSS rules that are breaking nav visibility
"""

import re
from pathlib import Path

def remove_orphaned_css(file_path):
    """Remove orphaned CSS between .wa definition and its improper closing brace"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is the .wa definition line
        if '.wa { max-width: var(--article)' in line:
            # Add this line
            fixed_lines.append(line)
            i += 1
            
            # Skip all indented lines until we hit a single closing brace
            # These are the orphaned rules
            while i < len(lines):
                if lines[i].strip() == '}':
                    # Skip this closing brace too - it's the orphan block closer
                    i += 1
                    break
                elif lines[i].startswith('  '):
                    # Skip indented orphaned rule
                    i += 1
                else:
                    # Hit a non-indented line, stop skipping
                    break
        else:
            # Normal line, keep it
            fixed_lines.append(line)
            i += 1
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

def main():
    """Fix all blog article files"""
    
    blog_dir = Path('blog')
    count = 0
    
    # Process all article files
    for subdir in blog_dir.iterdir():
        if subdir.is_dir():
            index_file = subdir / 'index.html'
            if index_file.exists():
                print(f"Cleaning: {index_file}")
                remove_orphaned_css(index_file)
                count += 1
    
    # Also process standalone HTML files
    for html_file in blog_dir.glob('*.html'):
        if html_file.name != 'index.html':
            print(f"Cleaning: {html_file}")
            remove_orphaned_css(html_file)
            count += 1
    
    print(f"\nCleaned {count} files")

if __name__ == "__main__":
    main()