import codecs
import re

with codecs.open('monitor.html', 'r', 'utf-8') as f:
    c = f.read()

# 1. Add Force Time-Out All Button
active_header = """          <div class="flex items-center gap-2 mb-2">
            <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            <button id="active-section-toggle" class="flex items-center gap-2 text-left group flex-1 min-w-0">
              <h2 class="text-sm font-bold text-white uppercase tracking-widest">Active</h2>
              <span id="active-table-count" class="text-xs text-neutral-500 font-mono"></span>
              <span class="material-icons-round text-neutral-500 text-sm group-hover:text-white transition" id="active-toggle-icon">expand_less</span>
            </button>"""
new_active_header = """          <div class="flex items-center justify-between gap-2 mb-2">
            <div class="flex items-center gap-2 flex-1 min-w-0">
              <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
              <button id="active-section-toggle" class="flex items-center gap-2 text-left group">
                <h2 class="text-sm font-bold text-white uppercase tracking-widest">Active</h2>
                <span id="active-table-count" class="text-xs text-neutral-500 font-mono"></span>
                <span class="material-icons-round text-neutral-500 text-sm group-hover:text-white transition" id="active-toggle-icon">expand_less</span>
              </button>
            </div>
            <button id="force-timeout-all-btn" class="text-xs bg-red-600/20 text-red-400 hover:bg-red-600 hover:text-white transition rounded px-3 py-1 font-bold border border-red-600/30 flex items-center gap-1">
              <span class="material-icons-round text-[14px]">logout</span> Time Out All
            </button>
"""
c = c.replace(active_header, new_active_header)

# 2. Add History Overlay
calendar_header = '<!-- Calendar View Section -->'
history_overlay = """<!-- History Overlay -->
      <div id="history-overlay" class="mt-8 mb-6 bg-neutral-900 border border-neutral-800 rounded-xl p-8 text-center flex flex-col items-center justify-center">
        <span class="material-icons-round text-sky-400 text-4xl mb-3">history</span>
        <h2 class="text-lg font-bold text-white mb-2">Past Logs History</h2>
        <p class="text-sm text-neutral-400 mb-6 max-w-md">To keep the live dashboard fast, the entire history database is not loaded by default. Load it now to use the Calendar and Search past logs.</p>
        <button id="load-history-btn" class="bg-sky-500 hover:bg-sky-400 text-white font-bold py-2 px-6 rounded-lg shadow-lg transition flex items-center gap-2">
          <span class="material-icons-round text-sm">download</span> Load History
        </button>
      </div>
      
      <div id="history-container" class="hidden">
"""
c = c.replace(calendar_header, history_overlay + '\n' + calendar_header)

# Add closing div for history-container right before script imports
c = c.replace('<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>', '</div>\n    <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>')

with codecs.open('monitor.html', 'w', 'utf-8') as f:
    f.write(c)

# Now patch monitor.js
with codecs.open('monitor.js', 'r', 'utf-8') as f:
    j = f.read()

# Remove loadPreviousLogs() from page load
j = re.sub(r'// Load previous logs on page load\nloadPreviousLogs\(\);\n', '', j)

# Hook up load history btn and force time-out all btn
js_additions = """
// =============================
// Features: Force Time-Out All & Lazy Load History
// =============================

document.getElementById("force-timeout-all-btn")?.addEventListener("click", async () => {
  const activeLogs = Object.entries(allLogs).filter(([k, l]) => !l.timeOut && l.status !== "pending" && l.status !== "pending-out");
  if (activeLogs.length === 0) {
    showToast("No active volunteers right now.", "info", "text-sky-400");
    return;
  }
  
  if (!confirm(`Are you sure you want to force time-out all ${activeLogs.length} active volunteers?`)) return;

  const now = new Date().toISOString();
  showToast(`Timing out ${activeLogs.length} volunteers...`, "hourglass_top", "text-amber-400");

  for (const [key, log] of activeLogs) {
    await db.ref(`logs/${todayDate}/${key}`).update({
      timeOut: now,
      status: null,
      commsStatusOut: "OK"
    });
    if (log.commsId && log.commsId !== "NONE" && log.commsId !== "N/A") {
      await releaseCommsOrAutoAssign(log.commsId);
    }
    syncToSheets({ action: "timeOut", logKey: key, timeOut: now, timeIn: log.timeIn });
  }

  showToast("All active volunteers timed out", "check_circle", "text-green-400");
});

document.getElementById("load-history-btn")?.addEventListener("click", () => {
  const btn = document.getElementById("load-history-btn");
  btn.innerHTML = `<span class="material-icons-round text-sm animate-spin">refresh</span> Loading...`;
  btn.disabled = true;
  
  // Call loadPreviousLogs, but we need to intercept it to show the UI
  // since loadPreviousLogs runs async but uses .once with a callback
  db.ref("logs").once("value", (snapshot) => {
    const allDates = snapshot.val() || {};
    // enforceAutoLogout(allDates); // We'll handle this separately
    allPreviousEntries = [];
    Object.entries(allDates).forEach(([date, dateLogs]) => {
      Object.entries(dateLogs).forEach(([key, log]) => {
        if (log.status === "pending") return;
        allPreviousEntries.push({ key, date, ...log });
      });
    });
    prevLogsPage = 1;
    renderPreviousLogsTable();
    renderLargeCalendar();
    
    document.getElementById("history-overlay").classList.add("hidden");
    document.getElementById("history-container").classList.remove("hidden");
    showToast("History loaded successfully", "history", "text-sky-400");
  });
});

// Run lightweight enforceAutoLogout for yesterday only
function enforceYesterdayAutoLogout() {
  const yesterday = new Date(Date.now() - 86400000);
  // Adjust for PH timezone (UTC+8)
  const tzOffset = 8 * 60 * 60 * 1000;
  const localYesterday = new Date(yesterday.getTime() + tzOffset);
  const yesterdayStr = localYesterday.toISOString().split('T')[0];
  
  db.ref(`logs/${yesterdayStr}`).once("value", (snap) => {
    const data = snap.val();
    if (data) {
      enforceAutoLogout({ [yesterdayStr]: data });
    }
  });
}
// Run it shortly after page load
setTimeout(enforceYesterdayAutoLogout, 2000);
"""

# Replace the old `db.ref("logs").once("value", ...)` inside loadPreviousLogs since it conflicts.
# Actually we can just leave loadPreviousLogs alone and overwrite its functionality by re-declaring it,
# but it's cleaner to just not use it if we re-implemented the fetch in the button click. 
# Wait, `loadPreviousLogs()` is still used by "Refresh" buttons or something?
# Let's check if loadPreviousLogs is called anywhere else.
# It is defined on line 1282. We can just disable the original `db.ref("logs").once` inside it.

j = re.sub(r'function loadPreviousLogs\(\) \{[\s\S]*?prevLogsPage = 1;\s*renderPreviousLogsTable\(\);\s*renderLargeCalendar\(\);\s*\}\);', 'function loadPreviousLogs() { /* replaced by lazy loading */ }', j)

j += '\n' + js_additions

with codecs.open('monitor.js', 'w', 'utf-8') as f:
    f.write(j)

