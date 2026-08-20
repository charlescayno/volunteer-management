import codecs
with codecs.open('monitor.html', 'r', 'utf-8') as f:
    c = f.read()

analytics_html = '''      <!-- Analytics Section -->
      <div id="analytics-section" class="mt-8 mb-6 hidden">
        <div class="flex items-center gap-2 mb-3">
          <span class="material-icons-round text-purple-400 text-sm">insights</span>
          <h2 class="text-sm font-bold text-white uppercase tracking-widest">Daily Analytics & Summary</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div class="bg-neutral-900 border border-neutral-800 rounded-xl p-4">
            <h3 class="text-xs font-bold text-neutral-500 uppercase tracking-widest mb-4">Busiest Time-In Hours</h3>
            <canvas id="timeChart" height="200"></canvas>
          </div>
          <div class="bg-neutral-900 border border-neutral-800 rounded-xl p-4">
            <h3 class="text-xs font-bold text-neutral-500 uppercase tracking-widest mb-4">Volunteers by Segment</h3>
            <canvas id="segmentChart" height="200"></canvas>
          </div>
        </div>
        <div class="bg-neutral-900 border border-neutral-800 rounded-xl p-4">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-xs font-bold text-neutral-500 uppercase tracking-widest">End-of-Day Summary</h3>
            <button id="copy-summary-btn" class="text-xs text-neutral-400 hover:text-white flex items-center gap-1 transition">
              <span class="material-icons-round text-[14px]">content_copy</span> Copy
            </button>
          </div>
          <textarea id="eod-summary" class="w-full bg-neutral-800 border border-neutral-700 rounded-lg p-3 text-sm text-neutral-300 font-mono resize-none focus:outline-none" rows="6" readonly></textarea>
        </div>
      </div>

'''
c = c.replace('<!-- Calendar View Section -->', analytics_html + '<!-- Calendar View Section -->')

# Add Chart.js to head or end of body
c = c.replace('<script src="monitor.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n    <script src="monitor.js"></script>')

with codecs.open('monitor.html', 'w', 'utf-8') as f:
    f.write(c)
