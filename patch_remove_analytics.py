import codecs
import re

with codecs.open('monitor.html', 'r', 'utf-8') as f:
    c = f.read()

# Remove the entire analytics section
c = re.sub(r'\s*<!-- Analytics Section -->\s*<div id="analytics-section"[\s\S]*?</div>\s*</div>\s*', '\n\n', c)
# Remove Chart.js script
c = re.sub(r'\s*<script src="https://cdn\.jsdelivr\.net/npm/chart\.js"></script>', '', c)

with codecs.open('monitor.html', 'w', 'utf-8') as f:
    f.write(c)

with codecs.open('monitor.js', 'r', 'utf-8') as f:
    j = f.read()

# Remove renderAnalytics JS block
j = re.sub(r'// =============================\n// Analytics & EOD Summary[\s\S]*?showToast\("Summary copied to clipboard", "content_copy", "text-sky-400"\);\s*\}\s*\);\s*', '', j)
# Remove renderAnalytics call in load block
j = re.sub(r'\n\s*renderAnalytics\(\);', '', j)

with codecs.open('monitor.js', 'w', 'utf-8') as f:
    f.write(j)
