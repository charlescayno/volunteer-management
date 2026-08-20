import os

html_path = 'monitor.html'
js_path = 'monitor.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_btn = '''<button id="sync-sheets-btn" class="flex items-center gap-1.5 text-xs text-neutral-500 hover:text-green-400 bg-neutral-900 border border-neutral-800 hover:border-green-900 rounded-lg px-3 py-2.5 transition duration-150" title="Sync all data to Google Sheets">
          <span class="material-icons-round text-sm">sync</span>
          <span id="sync-sheets-label">Sync Sheets</span>
        </button>'''

new_btn = '''<a href="https://ccfph-my.sharepoint.com/:x:/g/personal/liveprod_volunteers_volunteers_ccf_org_ph/IQBNwUtq9KbGQrQv-zDRz5D4AaUSWTFCZ-lw0PCTr1GpJxQ?e=vUAp7V" target="_blank" id="open-logsheet-btn" class="flex items-center gap-1.5 text-xs text-neutral-500 hover:text-blue-400 bg-neutral-900 border border-neutral-800 hover:border-blue-900 rounded-lg px-3 py-2.5 transition duration-150" title="Open Comms Usage Logsheet">
          <span class="material-icons-round text-sm">open_in_new</span>
          <span>Open Logsheet</span>
        </a>'''

html = html.replace(old_btn, new_btn)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Disable syncToSheets
js = js.replace('''function syncToSheets(payload) {
  fetch(SHEETS_API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(payload)
  }).then((res) => {
    if (res.ok) return res.json();
    throw new Error('Sheets API error: ' + res.status);
  }).then((data) => {
    console.log('Sheets sync result:', data);
  }).catch((err) => console.warn('Sheets sync failed:', err));
}''', '''function syncToSheets(payload) {
  // Google Sheets sync disabled; using SharePoint directly
}''')

# Remove the manual sync button listener
import re
js = re.sub(r'// =============================\n// Manual Sync to Google Sheets\n// =============================\ndocument\.getElementById\("sync-sheets-btn"\)\.addEventListener\("click", async \(\) => \{[\s\S]*?\}\);\n', '', js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
