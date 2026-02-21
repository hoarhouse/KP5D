#!/bin/bash

# Fix all 17 blog article pages - Version 2
# This script fixes 4 issues: duplicate media queries, missing main tag, footer structure, placeholder links

fix_article_file() {
    local file="$1"
    echo "Processing: $file"
    
    # Create temp file
    local temp_file="${file}.tmp"
    
    # Read the entire file
    content=$(cat "$file")
    
    # Count how many media queries exist
    media_count=$(echo "$content" | grep -c "@media (max-width: 768px)")
    
    if [ "$media_count" -gt 1 ]; then
        echo "  Found $media_count media queries, consolidating..."
        
        # Remove the FIRST media query block (keeping the second one which has all rules)
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
    elif [ "$media_count" -eq 0 ]; then
        echo "  No media query found, adding one..."
        
        # Add a complete media query block before </style>
        media_block="@media (max-width: 768px) {
  .w { padding: 0 var(--s6); }
  .wa { padding: 0 var(--s6); }
  .hamburger { display: block; }
  .nav-r { display: none; position: absolute; top: 60px; right: 0; background: var(--white); flex-direction: column; gap: var(--s4); padding: var(--s5); border-radius: var(--r); box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
  .nav-r.active { display: flex; }
  .nav-r a:not(.btn) { display: none; }
  .nav-r.active a:not(.btn) { display: block; width: 100%; padding: var(--s2) 0; border-bottom: 1px solid var(--c6); }
  .nav-r.active .btn { width: auto; display: inline-block; margin-top: 16px; color: #fff; }
  .article-header { padding: 100px 0 var(--s6); }
  .article-body { padding-bottom: var(--s8); font-size: 1rem; }
  .article-body h2 { font-size: 1.5rem; margin: var(--s8) 0 var(--s4); }
  .article-body h3 { font-size: 1.15rem; margin: var(--s7) 0 var(--s3); }
}"
        
        content=$(echo "$content" | sed "s|</style>|${media_block}\n</style>|")
    else
        echo "  Media query OK, checking for .w padding rule..."
        
        # Check if .w padding rule exists in the media query
        if ! echo "$content" | grep -A20 "@media (max-width: 768px)" | grep -q "\.w.*padding.*var(--s6)"; then
            echo "  Adding .w padding rule to media query..."
            # Add .w rule as first rule in the media query block
            content=$(echo "$content" | sed '/@media (max-width: 768px) {/a\
  .w { padding: 0 var(--s6); }')
        fi
    fi
    
    # Fix 2: Add semantic <main> wrapper (if not already present)
    if ! echo "$content" | grep -q "<main>"; then
        echo "  Adding <main> wrapper..."
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
        echo "  Fixing footer structure..."
        content=$(echo "$content" | sed 's|<div class="w"><footer>|<footer>\
  <div class="w">|')
        content=$(echo "$content" | sed 's|</footer></div>|  </div>\
</footer>|')
    fi
    
    # Fix 4: Update placeholder footer links
    # Only update if they are placeholders (href="#")
    if echo "$content" | grep -q 'href="#"'; then
        echo "  Updating placeholder links..."
        content=$(echo "$content" | sed 's|href="#">GitHub</a>|href="https://github.com/hoarhouse/KP5D">GitHub</a>|g')
        content=$(echo "$content" | sed 's|href="#">Docs</a>|href="https://kept.work/docs/">Docs</a>|g')
        content=$(echo "$content" | sed 's|href="#">Privacy</a>|href="https://kept.work/privacy/">Privacy</a>|g')
    fi
    
    # Write the fixed content
    echo "$content" > "$temp_file"
    mv "$temp_file" "$file"
    
    echo "  ✓ Fixed: $file"
}

# Apply to all files
echo "=== APPLYING FIXES TO ALL BLOG ARTICLE FILES ==="
echo ""

count=0
for file in blog/*/index.html blog/*.html; do
    # Skip blog index
    [ "$file" = "blog/index.html" ] && continue
    # Skip non-existent patterns
    [ ! -f "$file" ] && continue
    # Skip backup files
    [[ "$file" == *.test-backup ]] && continue
    [[ "$file" == *.tmp ]] && continue
    
    fix_article_file "$file"
    count=$((count + 1))
done

echo ""
echo "=== COMPLETE ==="
echo "Fixed $count files"