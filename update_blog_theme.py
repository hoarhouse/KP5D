import os, re, glob

# ── New nav HTML (replaces everything from <nav> to </nav>) ──
NEW_NAV = '''<nav>
  <div class="w">
    <a href="/KP5D/" class="nav-logo">
      <div class="nav-logo-mark">
        <svg viewBox="0 0 14 14" fill="none">
          <rect x="2" y="2" width="4" height="4" rx="1" fill="#070709"/>
          <rect x="8" y="2" width="4" height="4" rx="1" fill="#070709"/>
          <rect x="2" y="8" width="4" height="4" rx="1" fill="#070709"/>
          <rect x="8" y="8" width="4" height="4" rx="1" fill="#070709" opacity="0.4"/>
        </svg>
      </div>
      <span class="nav-logo-text">Kept</span>
    </a>
    <div class="nav-links">
      <a href="/KP5D/">Home</a>
      <a href="/KP5D/blog/">Blog</a>
    </div>
    <div class="nav-cta">
      <a href="/KP5D/#cta" class="btn btn-primary">Join waitlist</a>
    </div>
  </div>
</nav>'''

# ── New footer HTML (replaces everything from <footer> to </footer>) ──
NEW_FOOTER = '''<footer>
  <div class="w">
    <div class="foot-inner">
      <span class="foot-left">Kept &middot; An E-Group Labs product &middot; 2026</span>
      <div class="foot-right">
        <a href="https://github.com/hoarhouse/KP5D" target="_blank">GitHub</a>
        <a href="/KP5D/blog/">Blog</a>
        <a href="/KP5D/privacy.html">Privacy</a>
      </div>
    </div>
  </div>
</footer>'''

# ── New font imports + CSS link (replaces old font links and inline style block) ──
NEW_HEAD_STYLES = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700&family=Instrument+Serif:ital@0;1&family=DM+Mono:ital,wght@0,300;0,400;0,500&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/KP5D/blog/blog.css">'''

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Replace font preconnects + link + inline <style> block with new imports
    # Pattern: from first <link rel="preconnect" to end of </style>
    html = re.sub(
        r'<link rel="preconnect".*?</style>',
        NEW_HEAD_STYLES,
        html,
        count=1,
        flags=re.DOTALL
    )

    # 2. Replace nav block
    html = re.sub(
        r'<nav>.*?</nav>',
        NEW_NAV,
        html,
        count=1,
        flags=re.DOTALL
    )

    # 3. Replace footer block
    html = re.sub(
        r'<footer>.*?</footer>',
        NEW_FOOTER,
        html,
        count=1,
        flags=re.DOTALL
    )

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated: {path}")
    else:
        print(f"No changes: {path}")

# Process blog/index.html
process_file('blog/index.html')

# Process all article index.html files
for path in glob.glob('blog/*/index.html'):
    process_file(path)

print("Done.")