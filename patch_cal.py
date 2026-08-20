import os

def update_file(filename, task):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    content = task(content)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

js_addition = """
// =============================
// Large Calendar View
// =============================
let largeCalYear = new Date().getFullYear();
let largeCalMonth = new Date().getMonth();

function renderLargeCalendar() {
  const grid = document.getElementById("large-cal-grid");
  const label = document.getElementById("large-cal-month");
  if (!grid || !label) return;

  label.textContent = new Date(largeCalYear, largeCalMonth, 1).toLocaleDateString([], { month: "long", year: "numeric" });

  const firstDay = new Date(largeCalYear, largeCalMonth, 1).getDay();
  const daysInMonth = new Date(largeCalYear, largeCalMonth + 1, 0).getDate();

  // Group entries by date
  const logCounts = {};
  allPreviousEntries.forEach(e => {
    logCounts[e.date] = (logCounts[e.date] || 0) + 1;
  });

  grid.innerHTML = "";
  for (let i = 0; i < firstDay; i++) {
    const emptyDiv = document.createElement("div");
    emptyDiv.className = "p-2 min-h-[80px] rounded-lg bg-neutral-900/50 border border-neutral-800/50 opacity-50";
    grid.appendChild(emptyDiv);
  }

  const todayStr = new Date().toLocaleDateString("en-CA").split("T")[0]; // YYYY-MM-DD local

  for (let d = 1; d <= daysInMonth; d++) {
    const dayBtn = document.createElement("button");
    dayBtn.className = "relative p-2 min-h-[80px] flex flex-col items-start justify-start rounded-lg border border-neutral-800 bg-neutral-900 hover:border-neutral-600 transition text-left group overflow-hidden";
    
    // Format YYYY-MM-DD
    const m = String(largeCalMonth + 1).padStart(2, "0");
    const day = String(d).padStart(2, "0");
    const dateStr = `${largeCalYear}-${m}-${day}`;
    
    const count = logCounts[dateStr] || 0;
    const isToday = dateStr === todayStr;

    let html = `<span class="text-xs font-semibold ${isToday ? 'text-sky-400' : 'text-neutral-400 group-hover:text-white'}">${d}</span>`;
    
    if (count > 0) {
      html += `<div class="mt-auto w-full">
        <div class="bg-sky-500/10 border border-sky-500/20 text-sky-400 text-[10px] font-bold px-1.5 py-1 rounded w-full text-center truncate">
          ${count} Log${count !== 1 ? 's' : ''}
        </div>
      </div>`;
    }

    dayBtn.innerHTML = html;

    if (count > 0 || isToday) {
      dayBtn.addEventListener("click", () => {
        // Jump to previous logs and filter
        prevLogsDateFilter = dateStr;
        const calLabel = document.getElementById("prev-logs-calendar-label");
        calLabel.textContent = new Date(dateStr + "T00:00:00").toLocaleDateString([], { month: "short", day: "numeric", year: "numeric" });
        document.getElementById("prev-logs-calendar-btn").classList.add("border-white/30", "text-white");
        
        // Show previous logs section if hidden
        const prevLogsSec = document.getElementById("previous-logs-section");
        if (prevLogsSec.classList.contains("hidden")) {
           prevLogsSec.classList.remove("hidden");
        }
        
        prevLogsPage = 1;
        filterAndRenderPreviousLogs();
        
        // Scroll to it
        document.getElementById("previous-logs-section").scrollIntoView({ behavior: 'smooth' });
      });
    } else {
      dayBtn.classList.add("cursor-default", "hover:border-neutral-800");
    }

    grid.appendChild(dayBtn);
  }
}

document.getElementById("large-cal-prev")?.addEventListener("click", () => {
  largeCalMonth--;
  if (largeCalMonth < 0) { largeCalMonth = 11; largeCalYear--; }
  renderLargeCalendar();
});

document.getElementById("large-cal-next")?.addEventListener("click", () => {
  largeCalMonth++;
  if (largeCalMonth > 11) { largeCalMonth = 0; largeCalYear++; }
  renderLargeCalendar();
});

// Call renderLargeCalendar when logs load
"""

def task_js(c):
    # Insert right before the generic exports/bottom of file or after renderCalendar
    c = c.replace('renderCalendar();', 'renderCalendar();\n        renderLargeCalendar();')
    c = c.replace('renderPrevLogsPills();\n    renderCalendar();', 'renderPrevLogsPills();\n    renderCalendar();\n    renderLargeCalendar();')
    c = c + '\n' + js_addition
    return c

update_file('monitor.js', task_js)
print("Updated JS")
