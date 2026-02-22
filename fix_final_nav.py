#!/usr/bin/env python3
import re

files = [
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
            lines = f.readlines()
        
        # Find the problematic section - look for lines after media query closing brace
        # that contain the nav-r rules
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check if this is a closing brace followed by indented rules
            if line.strip() == '}' and i + 1 < len(lines):
                # Check if next line starts with indented content
                next_line = lines[i + 1]
                if next_line.startswith('  .') and 'nav-r a:not(.btn)' in ''.join(lines[i+1:i+10]):
                    # Found the problematic section
                    fixed_lines.append(line)  # Keep the closing brace
                    
                    # Skip all the indented rules until we hit another closing brace
                    j = i + 1
                    while j < len(lines):
                        if lines[j].strip() == '}':
                            i = j  # Skip to this position
                            break
                        j += 1
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
            
            i += 1
        
        # Write the fixed content
        with open(file, 'w') as f:
            f.writelines(fixed_lines)
        
        print(f"Fixed: {file}")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")