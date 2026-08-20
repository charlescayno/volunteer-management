import codecs
import re

with codecs.open('monitor.js', 'r', 'utf-8') as f:
    c = f.read()

analytics_js = '''
// =============================
// Analytics & EOD Summary
// =============================
let timeChartInst = null;
let segChartInst = null;

function renderAnalytics() {
  const anSec = document.getElementById("analytics-section");
  if (!anSec) return;
  
  const allLogsArr = Object.values(allLogs).filter(l => l.status !== "pending");
  if (allLogsArr.length === 0) {
    anSec.classList.add("hidden");
    return;
  }
  
  anSec.classList.remove("hidden");

  // 1. Process Data
  const hourCounts = {};
  const segmentCounts = {};
  let totalHours = 0;
  let missingComms = [];
  
  const activeVolIds = new Set();
  const completedVolIds = new Set();

  allLogsArr.forEach(log => {
    // Unique vols
    if (log.volunteerId) {
      if (!log.timeOut) activeVolIds.add(log.volunteerId);
      else completedVolIds.add(log.volunteerId);
    }
    
    // Segments
    const seg = log.segment || "Unknown";
    segmentCounts[seg] = (segmentCounts[seg] || 0) + 1;
    
    // Hours (Time In)
    if (log.timeIn) {
      const d = new Date(log.timeIn);
      const hStr = d.getHours() + ":00";
      hourCounts[hStr] = (hourCounts[hStr] || 0) + 1;
    }
    
    // Total Hours
    if (log.timeIn && log.timeOut) {
      const ms = new Date(log.timeOut) - new Date(log.timeIn);
      totalHours += ms / (1000 * 60 * 60);
    } else if (log.timeIn) {
      const ms = new Date() - new Date(log.timeIn);
      totalHours += ms / (1000 * 60 * 60);
    }
    
    // Missing comms
    if (!log.timeOut && log.commsId && log.commsId !== "NONE" && log.commsId !== "N/A") {
      missingComms.push(`${log.commsId} (${log.name || "Unknown"})`);
    }
  });

  const totalUnique = new Set([...activeVolIds, ...completedVolIds]).size;

  // 2. Render Charts
  const ctxTime = document.getElementById('timeChart');
  const ctxSeg = document.getElementById('segmentChart');

  if (timeChartInst) timeChartInst.destroy();
  if (segChartInst) segChartInst.destroy();

  Chart.defaults.color = '#737373';

  if (ctxTime) {
    // Sort hours
    const sortedHours = Object.keys(hourCounts).sort((a,b) => parseInt(a) - parseInt(b));
    const hData = sortedHours.map(k => hourCounts[k]);
    timeChartInst = new Chart(ctxTime, {
      type: 'bar',
      data: {
        labels: sortedHours,
        datasets: [{ label: 'Time-Ins', data: hData, backgroundColor: '#38bdf8', borderRadius: 4 }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } }
    });
  }

  if (ctxSeg) {
    const segLabels = Object.keys(segmentCounts);
    const segData = Object.values(segmentCounts);
    // tailwind neutral-700 to sky-400 palette
    const colors = ['#38bdf8', '#818cf8', '#a78bfa', '#c084fc', '#e879f9', '#f472b6', '#fb7185', '#5eead4', '#94a3b8'];
    segChartInst = new Chart(ctxSeg, {
      type: 'doughnut',
      data: {
        labels: segLabels,
        datasets: [{ data: segData, backgroundColor: colors, borderWidth: 1, borderColor: '#171717' }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }
    });
  }

  // 3. EOD Summary
  const summaryEl = document.getElementById("eod-summary");
  if (summaryEl) {
    const dateStr = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    let txt = `📅 EOD Summary - ${dateStr}\n\n`;
    txt += `👥 Total Unique Volunteers: ${totalUnique}\n`;
    txt += `⏱️ Total Hours Served: ${totalHours.toFixed(1)} hrs\n`;
    txt += `✅ Completed Shifts: ${allLogsArr.filter(l => l.timeOut).length}\n`;
    txt += `🟡 Still Active: ${allLogsArr.filter(l => !l.timeOut).length}\n\n`;
    
    if (missingComms.length > 0) {
      txt += `⚠️ UNRETURNED COMMS (${missingComms.length}):\n`;
      missingComms.forEach(c => txt += ` - ${c}\n`);
    } else {
      txt += `📻 All Comms Returned! 🎉\n`;
    }
    
    summaryEl.value = txt;
  }
}

document.getElementById("copy-summary-btn")?.addEventListener("click", () => {
  const summaryEl = document.getElementById("eod-summary");
  if (summaryEl) {
    summaryEl.select();
    document.execCommand("copy");
    showToast("Summary copied to clipboard", "content_copy", "text-sky-400");
  }
});

'''
c = c + '\n' + analytics_js

c = c.replace('renderTable();\n  },', 'renderTable();\n    if (typeof renderAnalytics === "function") renderAnalytics();\n  },')

with codecs.open('monitor.js', 'w', 'utf-8') as f:
    f.write(c)
