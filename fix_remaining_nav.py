#!/usr/bin/env python3
import re

files = [
    'blog/kept-vs-echoes-vs-chatgpt-exporter/index.html',
    'blog/obsidian-notion-tana-ai-conversations/index.html',
    'blog/search-across-ai-conversations/index.html',
    'blog/second-opinion-another-ai-10-seconds/index.html',
    'blog/share-ai-conversation-snippets-formatting/index.html',
    'blog/stop-re-explaining-your-codebase-to-every-ai/index.html',
    'blog/transfer-context-chatgpt-claude/index.html',
    'blog/why-ai-platforms-will-never-index-each-other/index.html',
    'blog/why-local-first-matters/index.html',
    'blog/claude-for-architecture-chatgpt-for-code-keeping-context.html'
]

for file in files:
    try:
        with open(file, 'r') as f:
            content = f.read()
        
        # Find and remove the duplicate block after the media query
        # Look for the pattern where there's a closing brace from the media query
        # followed by indented rules that should be removed
        pattern = r'(\n}\n)(  \.related-grid[^}]*?footer[^}]*?\n})'
        
        if re.search(pattern, content):
            # Replace with just the first closing brace
            content = re.sub(pattern, r'\1', content)
            
            with open(file, 'w') as f:
                f.write(content)
            print(f"Fixed: {file}")
        else:
            print(f"Pattern not found in: {file}")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")