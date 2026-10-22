// Meeting-to-Tasks Agent Frontend App
const API_BASE = "";

// State
let currentTeam = [
  { name: "Rahul Verma", role: "Frontend Lead", email: "rahul@company.com" },
  { name: "Siddharth Rao", role: "DevOps Engineer", email: "siddharth@company.com" },
  { name: "Sneha Reddy", role: "Product Manager", email: "sneha@company.com" }
];

let lastAnalysisResult = null;

// DOM Elements
const trelloStatusPill = document.getElementById("trelloStatusPill");
const trelloStatusText = document.getElementById("trelloStatusText");
const resetDbBtn = document.getElementById("resetDbBtn");
const runAgentBtn = document.getElementById("runAgentBtn");
const transcriptIdInput = document.getElementById("transcriptId");
const transcriptTextInput = document.getElementById("transcriptText");
const charCountSpan = document.getElementById("charCount");
const teamTableBody = document.getElementById("teamTableBody");
const addMemberBtn = document.getElementById("addMemberBtn");
const statusTag = document.getElementById("statusTag");

// Sections
const duplicateAlertBox = document.getElementById("duplicateAlertBox");
const duplicateAlertText = document.getElementById("duplicateAlertText");
const duplicateAlertMeta = document.getElementById("duplicateAlertMeta");

const clarificationsSection = document.getElementById("clarificationsSection");
const clarificationsList = document.getElementById("clarificationsList");
const clarificationsCount = document.getElementById("clarificationsCount");

const confirmedSection = document.getElementById("confirmedSection");
const confirmedList = document.getElementById("confirmedList");
const confirmedCount = document.getElementById("confirmedCount");
const confirmedEmpty = document.getElementById("confirmedEmpty");

const tentativeSection = document.getElementById("tentativeSection");
const tentativeList = document.getElementById("tentativeList");
const tentativeCount = document.getElementById("tentativeCount");

const verificationSection = document.getElementById("verificationSection");
const verificationList = document.getElementById("verificationList");
const verificationCount = document.getElementById("verificationCount");

const boardCardsGrid = document.getElementById("boardCardsGrid");
const refreshCardsBtn = document.getElementById("refreshCardsBtn");

// Stepper
const steps = [
  document.getElementById("step1"),
  document.getElementById("step2"),
  document.getElementById("step3"),
  document.getElementById("step4"),
  document.getElementById("step5")
];

function setStep(stepNum) {
  steps.forEach((el, idx) => {
    if (idx + 1 <= stepNum) {
      el.classList.add("active");
    } else {
      el.classList.remove("active");
    }
  });
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  renderTeamTable();
  checkTrelloStatus();
  fetchBoardCards();
  loadScenario("TC1");

  // Event Listeners
  runAgentBtn.addEventListener("click", runAnalysis);
  resetDbBtn.addEventListener("click", resetDatabase);
  refreshCardsBtn.addEventListener("click", fetchBoardCards);
  addMemberBtn.addEventListener("click", addTeamMember);

  transcriptTextInput.addEventListener("input", () => {
    charCountSpan.textContent = `${transcriptTextInput.value.length} characters`;
  });

  // Scenario Buttons
  document.querySelectorAll(".test-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const scenarioId = btn.getAttribute("data-scenario");
      loadScenario(scenarioId);
    });
  });
});

// Trello Connection Check
async function checkTrelloStatus() {
  try {
    const res = await fetch(`${API_BASE}/api/status`);
    const data = await res.json();
    if (data.status === "CONNECTED") {
      trelloStatusText.innerHTML = `<strong>Trello: Connected</strong> (List: <em>${data.lists.find(l => l.id === data.target_list_id)?.name || 'This Week'}</em>)`;
      trelloStatusPill.querySelector(".status-indicator").className = "status-indicator live";
    } else {
      trelloStatusText.textContent = "Trello Error";
      trelloStatusPill.querySelector(".status-indicator").className = "status-indicator error";
    }
  } catch (err) {
    trelloStatusText.textContent = "Offline";
    trelloStatusPill.querySelector(".status-indicator").className = "status-indicator error";
  }
}

// Fetch Live Cards from Trello List
async function fetchBoardCards() {
  try {
    const res = await fetch(`${API_BASE}/api/cards`);
    const data = await res.json();
    if (data.status === "SUCCESS") {
      renderBoardCards(data.cards);
    }
  } catch (err) {
    boardCardsGrid.innerHTML = `<div class="empty-board-msg">Failed to fetch cards: ${err.message}</div>`;
  }
}

function renderBoardCards(cards) {
  if (!cards || cards.length === 0) {
    boardCardsGrid.innerHTML = `<div class="empty-board-msg">No cards currently in this list.</div>`;
    return;
  }
  boardCardsGrid.innerHTML = cards.map(c => `
    <div class="live-trello-card">
      <div class="card-name">${escapeHtml(c.name)}</div>
      <div class="card-footer">
        <span>Due: ${c.due ? c.due.substring(0, 10) : 'None'}</span>
        <a href="${c.shortUrl}" target="_blank" class="btn btn-xs btn-ghost">View in Trello ↗</a>
      </div>
    </div>
  `).join("");
}

// Render Team Roster Table
function renderTeamTable() {
  teamTableBody.innerHTML = currentTeam.map((m, idx) => `
    <tr>
      <td><input class="team-input" type="text" value="${escapeHtml(m.name)}" data-idx="${idx}" data-field="name"></td>
      <td><input class="team-input" type="text" value="${escapeHtml(m.role || '')}" data-idx="${idx}" data-field="role"></td>
      <td><input class="team-input" type="text" value="${escapeHtml(m.email || '')}" data-idx="${idx}" data-field="email"></td>
      <td><button class="del-btn" onclick="removeTeamMember(${idx})" title="Remove member">×</button></td>
    </tr>
  `).join("");

  // Attach change listeners
  teamTableBody.querySelectorAll(".team-input").forEach(input => {
    input.addEventListener("change", (e) => {
      const idx = parseInt(e.target.dataset.idx);
      const field = e.target.dataset.field;
      currentTeam[idx][field] = e.target.value.trim();
    });
  });
}

function addTeamMember() {
  currentTeam.push({ name: "New Member", role: "Contributor", email: "" });
  renderTeamTable();
}

window.removeTeamMember = function(idx) {
  currentTeam.splice(idx, 1);
  renderTeamTable();
};

// Load Test Scenario
async function loadScenario(scenarioId) {
  try {
    const res = await fetch(`${API_BASE}/api/test-scenario/${scenarioId}`);
    if (!res.ok) throw new Error("Scenario not found");
    const data = await res.json();

    transcriptIdInput.value = data.transcript_id;
    transcriptTextInput.value = data.transcript;
    charCountSpan.textContent = `${data.transcript.length} characters`;
    currentTeam = data.team;
    renderTeamTable();

    // Reset previous outputs
    clearOutputs();
    setStep(1);
    statusTag.textContent = `Scenario Loaded (${scenarioId})`;

    // Highlight active test button
    document.querySelectorAll(".test-btn").forEach(btn => {
      if (btn.getAttribute("data-scenario") === scenarioId) {
        btn.style.borderColor = "var(--primary)";
      } else {
        btn.style.borderColor = "var(--border-color)";
      }
    });

  } catch (err) {
    alert("Error loading scenario: " + err.message);
  }
}

// Clear Outputs
function clearOutputs() {
  duplicateAlertBox.classList.add("hidden");
  clarificationsSection.classList.add("hidden");
  clarificationsList.innerHTML = "";
  confirmedList.innerHTML = "";
  confirmedCount.textContent = "0";
  confirmedEmpty.style.display = "block";
  tentativeSection.classList.add("hidden");
  tentativeList.innerHTML = "";
  verificationSection.classList.add("hidden");
  verificationList.innerHTML = "";
  verificationCount.textContent = "0";
}

// Run Analysis
async function runAnalysis() {
  const transcriptId = transcriptIdInput.value.trim() || "MEET-001";
  const transcriptText = transcriptTextInput.value.trim();

  if (!transcriptText) {
    alert("Please enter or select a meeting transcript.");
    return;
  }

  setStep(2);
  statusTag.textContent = "Agent Planning...";
  runAgentBtn.disabled = true;
  runAgentBtn.innerHTML = "<span>⚙️ Analyzing Decisions & Owners...</span>";

  try {
    const res = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        transcript_id: transcriptId,
        transcript_text: transcriptText,
        team_members: currentTeam
      })
    });

    const data = await res.json();
    lastAnalysisResult = data;
    renderAnalysisResult(data);

  } catch (err) {
    alert("Agent Analysis Failed: " + err.message);
  } finally {
    runAgentBtn.disabled = false;
    runAgentBtn.innerHTML = "<span>⚡ Run Meeting Agent</span>";
  }
}

// Render Results
function renderAnalysisResult(data) {
  clearOutputs();
  setStep(3);

  // Check TC4: Duplicate Detected
  if (data.status === "DUPLICATE_DETECTED") {
    statusTag.textContent = "TC4: Duplicate Blocked";
    duplicateAlertBox.classList.remove("hidden");
    duplicateAlertText.textContent = data.message;
    duplicateAlertMeta.textContent = data.evidence;
    return;
  }

  statusTag.textContent = "Analysis Complete";

  // Check TC2: Clarifications / Ambiguity
  if (data.clarifications_needed && data.clarifications_needed.length > 0) {
    clarificationsSection.classList.remove("hidden");
    clarificationsCount.textContent = data.clarifications_needed.length;
    renderClarifications(data.clarifications_needed);
  }

  // Check TC3: Tentative Items
  if (data.unresolved_items && data.unresolved_items.length > 0) {
    tentativeSection.classList.remove("hidden");
    tentativeCount.textContent = data.unresolved_items.length;
    renderTentativeItems(data.unresolved_items);
  }

  // Check TC1: Confirmed Tasks
  if (data.created_tasks && data.created_tasks.length > 0) {
    confirmedEmpty.style.display = "none";
    confirmedCount.textContent = data.created_tasks.length;
    renderConfirmedTasks(data.created_tasks);
  } else {
    confirmedEmpty.style.display = "block";
  }
}

// Render Ambiguity Cards (TC2)
function renderClarifications(clarifications) {
  clarificationsList.innerHTML = clarifications.map((c, idx) => `
    <div class="clarify-card">
      <div class="clarify-question">❓ ${escapeHtml(c.question)}</div>
      <div class="quote-box">"${escapeHtml(c.quote)}"</div>
      <div class="clarify-options">
        <span style="font-size:0.75rem; color:#FEF08A; align-self:center;">Select intended owner:</span>
        ${c.matching_candidates.map(candidate => `
          <button class="btn-resolve" onclick="resolveAmbiguity(${idx}, '${escapeHtml(candidate.name)}', '${escapeHtml(candidate.role || '')}')">
            👤 ${escapeHtml(candidate.name)} (${escapeHtml(candidate.role || 'Member')})
          </button>
        `).join("")}
      </div>
    </div>
  `).join("");
}

// Resolve Ambiguity to Confirmed Task
window.resolveAmbiguity = function(clarifyIdx, chosenName, chosenRole) {
  const clarification = lastAnalysisResult.clarifications_needed[clarifyIdx];
  if (!clarification) return;

  // Extract due date from quote if present
  let dueDate = "Wednesday";
  const dateMatch = clarification.quote.match(/by\s+([A-Za-z0-9\-,\s]+?)(?:\.|$|,)/i);
  if (dateMatch) dueDate = dateMatch[1].trim();

  const resolvedTask = {
    id: `${clarification.id}-RESOLVED`,
    title: clarification.quote,
    owner: chosenName,
    owner_role: chosenRole,
    due_date: dueDate,
    quote: clarification.quote,
    target_board: "My Trello board",
    target_list: "This Week",
    status: "AWAITING_HUMAN_APPROVAL"
  };

  // Add to confirmed tasks list
  if (!lastAnalysisResult.created_tasks) lastAnalysisResult.created_tasks = [];
  lastAnalysisResult.created_tasks.push(resolvedTask);

  // Remove from clarifications
  lastAnalysisResult.clarifications_needed.splice(clarifyIdx, 1);

  // Re-render
  renderAnalysisResult(lastAnalysisResult);
};

// Render Tentative Items (TC3)
function renderTentativeItems(items) {
  tentativeList.innerHTML = items.map(item => `
    <div class="tentative-card">
      <div class="tentative-quote">"${escapeHtml(item.quote)}"</div>
      <div class="tentative-reason">⚠️ <strong>Filter Reason:</strong> ${escapeHtml(item.reason)}</div>
    </div>
  `).join("");
}

// Render Confirmed Tasks Pending Approval (TC1 / Step 4)
function renderConfirmedTasks(tasks) {
  confirmedList.innerHTML = tasks.map((task, idx) => `
    <div class="task-item-card" id="taskCard-${idx}">
      <div class="task-card-header">
        <div class="task-title">📌 ${escapeHtml(task.title)}</div>
        <div class="task-tags">
          <span class="owner-pill">👤 ${escapeHtml(task.owner)} (${escapeHtml(task.owner_role || 'Lead')})</span>
          <span class="due-pill">📅 Due: ${escapeHtml(task.due_date || 'This Week')}</span>
        </div>
      </div>
      <div class="quote-box">"${escapeHtml(task.quote)}"</div>
      <div class="task-card-footer">
        <span class="target-info">Target: <strong>${escapeHtml(task.target_board)}</strong> ➔ <strong>${escapeHtml(task.target_list)}</strong></span>
        <button class="btn btn-primary btn-sm" id="approveBtn-${idx}" onclick="approveTask(${idx})">
          🛡️ Approve & Push to Trello
        </button>
      </div>
    </div>
  `).join("");
}

// Step 4 & 5: Human Approval & Independent Verification
window.approveTask = async function(idx) {
  const task = lastAnalysisResult.created_tasks[idx];
  if (!task) return;

  const btn = document.getElementById(`approveBtn-${idx}`);
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = "<span>⏳ Pushing to Trello & Verifying...</span>";
  }

  setStep(4);
  statusTag.textContent = "Step 4: Executing Approval...";

  try {
    const res = await fetch(`${API_BASE}/api/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        task: task,
        transcript_url: `Meeting ID: ${transcriptIdInput.value.trim()}`
      })
    });

    const result = await res.json();
    if (!result.success) throw new Error("Approval execution failed");

    setStep(5);
    statusTag.textContent = "Step 5: Card Verified!";

    // Update Task Card UI
    if (btn) {
      btn.className = "btn btn-secondary btn-sm";
      btn.innerHTML = `✅ Pushed to Trello (<a href="${result.trello_card_url}" target="_blank" style="color:var(--primary);text-decoration:underline;">View Card</a>)`;
    }

    // Add to Verification Section
    verificationSection.classList.remove("hidden");
    const vCount = parseInt(verificationCount.textContent || "0") + 1;
    verificationCount.textContent = vCount;

    renderVerificationResult(task, result);
    fetchBoardCards();

  } catch (err) {
    alert("Approval Error: " + err.message);
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = "🛡️ Approve & Push to Trello";
    }
  }
};

// Render Step 5 Independent Verification
function renderVerificationResult(task, result) {
  const v = result.verification;
  const cardHtml = `
    <div class="verify-card">
      <div class="verify-header">
        <div>
          <strong>Verification for: [${escapeHtml(task.owner)}] ${escapeHtml(task.title)}</strong>
          <span style="font-size:0.75rem; color:var(--text-muted); display:block;">Card ID: ${v.card_id}</span>
        </div>
        <div style="display:flex; gap:0.5rem; align-items:center;">
          <a href="${result.trello_card_url}" target="_blank" class="btn btn-xs btn-secondary">Open Card ↗</a>
          <span class="verify-badge">${v.verified ? "VERIFIED (Step 5 PASSED)" : "VERIFICATION FAILED"}</span>
        </div>
      </div>

      <div class="verify-audit-grid">
        <div class="audit-field">
          <strong>Owner Verification</strong>
          <span class="${v.observed.owner_matched ? 'matched' : ''}">
            ${v.observed.owner_matched ? '✓ Matched: ' + v.intended.owner : '✗ Mismatch'}
          </span>
        </div>
        <div class="audit-field">
          <strong>Due Date Verification</strong>
          <span class="${v.observed.date_matched ? 'matched' : ''}">
            ${v.observed.date_matched ? '✓ Matched: ' + (v.intended.due_date || 'Standard') : '✗ Mismatch'}
          </span>
        </div>
        <div class="audit-field">
          <strong>Transcript Link Verification</strong>
          <span class="${v.observed.transcript_ref_found ? 'matched' : ''}">
            ${v.observed.transcript_ref_found ? '✓ Linked to Transcript' : '✗ Missing'}
          </span>
        </div>
      </div>
    </div>
  `;
  verificationList.insertAdjacentHTML("afterbegin", cardHtml);
}

// Reset Database
async function resetDatabase() {
  if (!confirm("Reset the SQLite audit database? This clears processed transcript hashes so you can re-run tests from scratch.")) {
    return;
  }
  try {
    const res = await fetch(`${API_BASE}/api/reset-db`, { method: "POST" });
    const data = await res.json();
    alert("Database reset: " + data.message);
    clearOutputs();
    setStep(1);
  } catch (err) {
    alert("Reset failed: " + err.message);
  }
}

// Helper: Escape HTML
function escapeHtml(text) {
  if (!text) return "";
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.toString().replace(/[&<>"']/g, m => map[m]);
}
