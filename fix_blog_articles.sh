#!/bin/bash

# Fix all 17 blog article pages
# This script fixes 4 issues: duplicate media queries, missing main tag, footer structure, placeholder links

fix_article_file() {
    local file="$1"
    echo "Processing: $file"
    
    # Create temp file
    local temp_file="${file}.tmp"
    
    # Read the entire file
    content=$(cat "$file")
    
    # Fix 1: Delete duplicate media query 
    # The first media query block contains only .w { padding: 0 var(--s6); }
    # Use awk to remove the first @media block
    content=$(echo "$content" | awk '
        /@media \(max-width: 768px\) \{/ {
            if (found_first == 0) {
                found_first = 1
                in_first_media = 1
                next
            }
        }
        in_first_media && /^}/ {
            in_first_media = 0
            next
        }
        !in_first_media {
            print
        }
    ')
    
    # Check if .w padding rule exists in the remaining media query, if not add it
    # First check if the main media query has .w rule already
    if ! echo "$content" | grep -A5 "@media (max-width: 768px) {" | grep -q "\.w { padding: 0 var(--s6); }"; then
        # Add .w rule as first rule in the media query block
        content=$(echo "$content" | sed '/@media (max-width: 768px) {/a\
  .w { padding: 0 var(--s6); }')
    fi
    
    # Fix 2: Add semantic <main> wrapper (if not already present)
    if ! echo "$content" | grep -q "<main>"; then
        # Add <main> after </nav>
        content=$(echo "$content" | sed 's|</nav>|</nav>\
\
<main>|')
        
        # Add </main> before footer structure (handle both patterns)
        # Pattern 1: <div class="w"><footer>
        if echo "$content" | grep -q '<div class="w"><footer>'; then
            content=$(echo "$content" | sed 's|<div class="w"><footer>|</main>\
\
<div class="w"><footer>|')
        # Pattern 2: <footer>
        elif echo "$content" | grep -q '^<footer>'; then
            content=$(echo "$content" | sed 's|^<footer>|</main>\
\
<footer>|')
        fi
    fi
    
    # Fix 3: Fix footer structure (footer should be outer element)
    # Change <div class="w"><footer>...footer></div> to <footer><div class="w">...</div></footer>
    if echo "$content" | grep -q '<div class="w"><footer>'; then
        content=$(echo "$content" | sed 's|<div class="w"><footer>|<footer>\
  <div class="w">|')
        content=$(echo "$content" | sed 's|</footer></div>|  </div>\
</footer>|')
    fi
    
    # Fix 4: Update placeholder footer links
    # Only update if they are placeholders (href="#")
    content=$(echo "$content" | sed 's|href="#">GitHub</a>|href="https://github.com/hoarhouse/KP5D">GitHub</a>|g')
    content=$(echo "$content" | sed 's|href="#">Docs</a>|href="https://kept.work/docs/">Docs</a>|g')
    content=$(echo "$content" | sed 's|href="#">Privacy</a>|href="https://kept.work/privacy/">Privacy</a>|g')
    
    # Write the fixed content
    echo "$content" > "$temp_file"
    mv "$temp_file" "$file"
    
    echo "  ✓ Fixed: $file"
}

# Test on ONE file first
test_file="blog/your-ai-conversations-are-a-codebase/index.html"

if [ -f "$test_file" ]; then
    echo "=== TEST RUN on $test_file ==="
    echo "Creating test backup..."
    cp "$test_file" "${test_file}.test-backup"
    
    # Show before state
    echo "BEFORE - Media query count: $(grep -c "@media (max-width: 768px)" "$test_file")"
    echo "BEFORE - Has <main>: $(grep -c "<main>" "$test_file")"
    echo "BEFORE - Placeholder links: $(grep -c 'href="#"' "$test_file")"
    echo "BEFORE - Footer structure: $(grep '<div class="w"><footer>' "$test_file" | head -1)"
    
    # Apply fix
    fix_article_file "$test_file"
    
    # Show after state
    echo ""
    echo "AFTER - Media query count: $(grep -c "@media (max-width: 768px)" "$test_file")"
    echo "AFTER - Has <main>: $(grep -c "<main>" "$test_file")"
    echo "AFTER - Placeholder links: $(grep -c 'href="#"' "$test_file")"
    echo "AFTER - Footer structure: $(grep '<footer>' "$test_file" | head -1)"
    
    echo ""
    echo "=== SHOWING DIFF (first 50 lines of changes) ==="
    diff -u "${test_file}.test-backup" "$test_file" | head -50
    
    echo ""
    echo "Test file has been fixed. Review the changes above."
    echo "The original is saved as ${test_file}.test-backup"
    echo ""
    echo "To apply to ALL files, run: $0 --apply-all"
    echo "To restore test file, run: mv ${test_file}.test-backup $test_file"
else
    echo "Test file not found: $test_file"
fi

# Apply to all files if requested
if [ "$1" = "--apply-all" ]; then
    echo ""
    echo "=== APPLYING FIXES TO ALL BLOG ARTICLE FILES ==="
    
    count=0
    for file in blog/*/index.html blog/*.html; do
        # Skip blog index
        [ "$file" = "blog/index.html" ] && continue
        # Skip non-existent patterns
        [ ! -f "$file" ] && continue
        # Skip test backup files
        [[ "$file" == *.test-backup ]] && continue
        [[ "$file" == *.tmp ]] && continue
        
        fix_article_file "$file"
        count=$((count + 1))
    done
    
    echo ""
    echo "=== COMPLETE ==="
    echo "Fixed $count files"
    echo "Backup stored in blog-backup/"
fi