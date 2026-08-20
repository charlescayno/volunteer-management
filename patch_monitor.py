import codecs

with codecs.open('monitor.js', 'r', 'utf-8') as f:
    c = f.read()

# 1. Update duration highlight
c = c.replace('const duration = calcDuration(h);', 'const durationMs = calcDurationMs(h);\n        const isOverdue = durationMs > 28800000; // 8 hours\n        const duration = calcDuration(h);')

# In grid view
c = c.replace('<div class="text-xs text-neutral-500 font-mono flex-shrink-0">${duration}</div>', '<div class="text-xs font-mono flex-shrink-0 flex items-center gap-1 ${isOverdue ? \'text-red-400 font-bold animate-pulse\' : \'text-neutral-500\'}">${isOverdue ? \'<span class="material-icons-round text-[10px]">warning</span>\' : \'\'}${duration}</div>')

# In table view
c = c.replace('td(`<span class="font-mono text-neutral-400">${calcDuration(log)}</span>`)', 'td(calcDurationMs(log) > 28800000 ? `<span class="font-mono text-red-400 font-bold animate-pulse flex items-center gap-1"><span class="material-icons-round text-[10px]">warning</span>${calcDuration(log)}</span>` : `<span class="font-mono text-neutral-400">${calcDuration(log)}</span>`)')

# Ensure auto-logout function is defined and called
auto_logout_code = '''
// =============================
// Auto-Logout Past Days
// =============================
async function enforceAutoLogout(allDatesObj) {
  const today = getPHDate();
  let updates = {};
  
  for (const [dateStr, dateLogs] of Object.entries(allDatesObj)) {
    if (dateStr >= today) continue; // Skip today and future
    
    for (const [key, log] of Object.entries(dateLogs)) {
      if (!log.timeOut && log.status !== 'pending') {
        const fakeTimeOut = new Date(dateStr + 'T02:00:00').toISOString(); // 2:00 AM next day roughly
        updates[`logs/${dateStr}/${key}/timeOut`] = fakeTimeOut;
        updates[`logs/${dateStr}/${key}/status`] = null;
        
        if (log.commsId && log.commsId !== "NONE" && log.commsId !== "N/A") {
           // Release comms
           await db.ref(`comms/${log.commsId}`).update({ status: "available", assignedTo: null, assignedTime: null });
        }
      }
    }
  }
  
  if (Object.keys(updates).length > 0) {
    await db.ref().update(updates);
    console.log("Auto-logged out overdue logs from previous days.");
  }
}
'''
c = auto_logout_code + '\n' + c

# hook it into loadPreviousLogs
c = c.replace('const allDates = snapshot.val() || {};\n    allPreviousEntries = [];', 'const allDates = snapshot.val() || {};\n    enforceAutoLogout(allDates);\n    allPreviousEntries = [];')

with codecs.open('monitor.js', 'w', 'utf-8') as f:
    f.write(c)
