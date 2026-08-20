import codecs
import re

with codecs.open('monitor.html', 'r', 'utf-8') as f:
    c = f.read()

# Make sure End of day summary text box is completely removed too
c = re.sub(r'<div class="bg-neutral-900 border border-neutral-800 rounded-xl p-4">\s*<div class="flex justify-between items-center mb-2">\s*<h3 class="text-xs font-bold text-neutral-500 uppercase tracking-widest">End-of-Day Summary</h3>[\s\S]*?</textarea>\s*</div>', '', c)

with codecs.open('monitor.html', 'w', 'utf-8') as f:
    f.write(c)
