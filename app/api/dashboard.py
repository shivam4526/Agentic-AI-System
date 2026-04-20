from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["dashboard"])


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Agentic AI Platform</title>
  <style>
    :root {
      --paper: #f7f3ea;
      --paper-deep: #efe5d2;
      --surface: rgba(255, 250, 244, 0.86);
      --surface-strong: rgba(255, 252, 247, 0.96);
      --ink: #1e1b18;
      --muted: #655d54;
      --line: rgba(57, 48, 36, 0.12);
      --line-strong: rgba(57, 48, 36, 0.24);
      --navy: #17324d;
      --teal: #0f766e;
      --amber: #b7791f;
      --red: #b42318;
      --violet: #53389e;
      --navy-soft: #dce7f0;
      --teal-soft: #daf4ee;
      --amber-soft: #fff2d8;
      --red-soft: #fee4e2;
      --violet-soft: #eee5ff;
      --hero: linear-gradient(135deg, #19384f 0%, #2d6170 44%, #5b9c90 100%);
      --shadow-xl: 0 28px 90px rgba(31, 25, 16, 0.16);
      --shadow-lg: 0 18px 48px rgba(33, 28, 20, 0.10);
      --radius-2xl: 34px;
      --radius-xl: 28px;
      --radius-lg: 22px;
      --radius-md: 18px;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
      background:
        radial-gradient(circle at top left, rgba(15, 118, 110, 0.14), transparent 24%),
        radial-gradient(circle at top right, rgba(183, 121, 31, 0.10), transparent 18%),
        linear-gradient(180deg, #fcfaf7 0%, var(--paper) 58%, var(--paper-deep) 100%);
    }

    body.drawer-open {
      overflow: hidden;
    }

    .shell {
      width: min(1320px, calc(100vw - 32px));
      margin: 28px auto 42px;
      display: grid;
      gap: 20px;
    }

    .hero {
      position: relative;
      overflow: hidden;
      border-radius: 40px;
      background: var(--hero);
      color: white;
      padding: 34px;
      box-shadow: var(--shadow-xl);
    }

    .hero::before,
    .hero::after {
      content: "";
      position: absolute;
      border-radius: 50%;
      pointer-events: none;
    }

    .hero::before {
      width: 320px;
      height: 320px;
      right: -110px;
      top: -90px;
      background: radial-gradient(circle, rgba(255,255,255,0.18), transparent 68%);
      animation: drift 14s ease-in-out infinite;
    }

    .hero::after {
      width: 240px;
      height: 240px;
      left: 40%;
      bottom: -110px;
      background: radial-gradient(circle, rgba(255,255,255,0.12), transparent 72%);
      animation: drift 18s ease-in-out infinite reverse;
    }

    @keyframes drift {
      0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
      50% { transform: translate3d(10px, -12px, 0) scale(1.05); }
    }

    @keyframes riseIn {
      from { opacity: 0; transform: translateY(18px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes drawerIn {
      from { transform: translateX(28px); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    h1, h2, h3, p { margin: 0; }

    .eyebrow {
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 12px;
      opacity: 0.8;
      margin-bottom: 12px;
    }

    .hero-grid {
      position: relative;
      z-index: 1;
      display: grid;
      grid-template-columns: 1.16fr 0.84fr;
      gap: 28px;
      align-items: end;
    }

    .hero-copy h1 {
      font-size: clamp(2.6rem, 4.7vw, 4.8rem);
      line-height: 0.94;
      max-width: 10ch;
      margin-bottom: 16px;
    }

    .hero-copy p {
      max-width: 62ch;
      color: rgba(255,255,255,0.86);
      line-height: 1.6;
      font-size: 1.04rem;
    }

    .metric-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .metric-card {
      appearance: none;
      width: 100%;
      text-align: left;
      padding: 18px;
      border-radius: 24px;
      border: 1px solid rgba(255,255,255,0.14);
      background: rgba(255,255,255,0.08);
      color: white;
      cursor: pointer;
      backdrop-filter: blur(10px);
      transition: transform 180ms ease, border-color 180ms ease, background 180ms ease, box-shadow 180ms ease;
    }

    .metric-card:hover,
    .metric-card.active {
      transform: translateY(-3px) scale(1.01);
      border-color: rgba(255,255,255,0.34);
      background: rgba(255,255,255,0.14);
      box-shadow: 0 18px 34px rgba(18, 23, 32, 0.18);
    }

    .metric-icon {
      width: 42px;
      height: 42px;
      border-radius: 14px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 14px;
      background: rgba(255,255,255,0.14);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,0.10);
    }

    .metric-icon svg {
      width: 22px;
      height: 22px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.8;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .metric-label {
      text-transform: uppercase;
      letter-spacing: 0.16em;
      font-size: 12px;
      opacity: 0.78;
      margin-bottom: 10px;
    }

    .metric-value {
      font-size: 1.9rem;
      font-weight: 700;
      line-height: 1.05;
      margin-bottom: 6px;
    }

    .metric-note {
      color: rgba(255,255,255,0.78);
      font-size: 0.95rem;
      line-height: 1.45;
    }

    .board {
      display: grid;
      grid-template-columns: 1.02fr 0.98fr;
      gap: 20px;
    }

    .stack {
      display: grid;
      gap: 20px;
    }

    .panel {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: var(--radius-2xl);
      box-shadow: var(--shadow-lg);
      padding: 24px;
      backdrop-filter: blur(12px);
      animation: riseIn 280ms ease;
    }

    .panel-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 16px;
    }

    .subtle {
      color: var(--muted);
      line-height: 1.6;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }

    .stat-card {
      border-radius: 22px;
      border: 1px solid var(--line);
      background: var(--surface-strong);
      padding: 16px;
      min-height: 124px;
      display: grid;
      gap: 8px;
    }

    .stat-label {
      color: var(--muted);
      font-size: 0.92rem;
    }

    .stat-value {
      font-size: 1.95rem;
      font-weight: 700;
    }

    .micro-chart {
      height: 34px;
      display: flex;
      align-items: end;
      gap: 6px;
    }

    .bar {
      flex: 1;
      min-width: 10px;
      border-radius: 999px 999px 4px 4px;
      background: linear-gradient(180deg, rgba(15, 118, 110, 0.78), rgba(15, 118, 110, 0.18));
      transition: height 220ms ease;
    }

    .bar.fail {
      background: linear-gradient(180deg, rgba(180, 35, 24, 0.78), rgba(180, 35, 24, 0.18));
    }

    .bar.queue {
      background: linear-gradient(180deg, rgba(83, 56, 158, 0.78), rgba(83, 56, 158, 0.18));
    }

    form {
      display: grid;
      gap: 14px;
    }

    textarea {
      width: 100%;
      min-height: 150px;
      resize: vertical;
      border-radius: 22px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.9);
      color: var(--ink);
      font: inherit;
      padding: 18px;
      transition: box-shadow 180ms ease, border-color 180ms ease, transform 180ms ease;
    }

    textarea:focus {
      outline: none;
      border-color: rgba(15, 118, 110, 0.42);
      box-shadow: 0 0 0 5px rgba(15, 118, 110, 0.11);
      transform: translateY(-1px);
    }

    .example-row,
    .actions,
    .status-row,
    .toggle-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }

    .chip,
    .ghost-button,
    .toggle,
    .task-card {
      font: inherit;
    }

    .chip,
    .ghost-button,
    .toggle {
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.88);
      color: var(--ink);
      cursor: pointer;
      transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
    }

    .chip { padding: 10px 14px; }

    .primary {
      border: 0;
      border-radius: 999px;
      padding: 14px 20px;
      background: linear-gradient(135deg, var(--navy), var(--teal));
      color: white;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 16px 28px rgba(23, 50, 77, 0.22);
      transition: transform 160ms ease, opacity 160ms ease;
    }

    .ghost-button,
    .toggle { padding: 11px 15px; }

    .chip:hover,
    .ghost-button:hover,
    .toggle:hover,
    .task-card:hover,
    .primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 24px rgba(36, 30, 22, 0.08);
    }

    .toggle.active {
      background: var(--navy);
      color: white;
      border-color: var(--navy);
    }

    .primary:disabled {
      opacity: 0.7;
      cursor: wait;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border-radius: 999px;
      padding: 9px 13px;
      font-size: 14px;
      font-weight: 600;
      background: var(--navy-soft);
      color: var(--navy);
    }

    .badge.warn { background: var(--amber-soft); color: var(--amber); }
    .badge.success { background: var(--teal-soft); color: var(--teal); }
    .badge.danger { background: var(--red-soft); color: var(--red); }
    .badge.violet { background: var(--violet-soft); color: var(--violet); }

    .summary-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin: 16px 0;
    }

    .summary-card {
      border-radius: 20px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.78);
      padding: 16px;
    }

    .summary-card span {
      display: block;
      color: var(--muted);
      font-size: 0.92rem;
      margin-bottom: 8px;
    }

    .summary-card strong {
      font-size: 1.7rem;
    }

    .progress-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }

    .step-card {
      border-radius: 20px;
      padding: 16px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.72);
      display: grid;
      gap: 8px;
      transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
    }

    .step-card.active {
      transform: translateY(-2px);
      border-color: rgba(183, 121, 31, 0.4);
      background: linear-gradient(180deg, #fff8ea, #fff0cd);
    }

    .step-card.done {
      transform: translateY(-2px);
      border-color: rgba(15, 118, 110, 0.28);
      background: linear-gradient(180deg, #effbf7, #daf4ec);
    }

    .step-label {
      text-transform: uppercase;
      letter-spacing: 0.14em;
      font-size: 12px;
      color: var(--muted);
    }

    .step-title {
      font-size: 1rem;
      font-weight: 700;
    }

    .result-box {
      min-height: 220px;
      border-radius: 24px;
      border: 1px solid var(--line);
      padding: 20px;
      background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(247, 250, 247, 0.90));
      white-space: pre-wrap;
      line-height: 1.7;
    }

    .timeline,
    .task-list {
      display: grid;
      gap: 12px;
      max-height: 540px;
      overflow: auto;
      padding-right: 4px;
    }

    .event-card,
    .task-card {
      border-radius: 22px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.84);
      padding: 16px;
    }

    .event-card {
      display: grid;
      gap: 8px;
    }

    .event-card.latest {
      border-color: rgba(15, 118, 110, 0.28);
      background: linear-gradient(180deg, rgba(240, 253, 250, 0.95), rgba(255,255,255,0.88));
    }

    .event-top,
    .task-top {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
    }

    .event-label,
    .task-title {
      font-size: 15px;
      font-weight: 700;
    }

    .event-time,
    .task-meta {
      font-size: 13px;
      color: var(--muted);
    }

    .event-card pre {
      margin: 0;
      padding: 14px;
      border-radius: 16px;
      background: #f5f7f8;
      color: #253545;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: "SFMono-Regular", Menlo, Consolas, monospace;
      font-size: 12px;
    }

    .technical-only { display: none; }
    body.show-technical .technical-only { display: block; }

    .task-card {
      appearance: none;
      width: 100%;
      text-align: left;
      cursor: pointer;
      transition: transform 180ms ease, border-color 180ms ease;
    }

    .task-card.active {
      border-color: rgba(83, 56, 158, 0.36);
      background: linear-gradient(180deg, rgba(246, 243, 255, 0.92), rgba(255,255,255,0.84));
    }

    .empty {
      border-radius: 22px;
      border: 1px dashed var(--line-strong);
      background: rgba(255,255,255,0.56);
      padding: 18px;
      color: var(--muted);
    }

    .drawer-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(20, 24, 33, 0.36);
      opacity: 0;
      pointer-events: none;
      transition: opacity 180ms ease;
      z-index: 20;
    }

    .drawer {
      position: fixed;
      top: 0;
      right: 0;
      width: min(460px, calc(100vw - 18px));
      height: 100vh;
      background: rgba(255, 252, 247, 0.98);
      border-left: 1px solid var(--line);
      box-shadow: -22px 0 50px rgba(31, 25, 16, 0.16);
      padding: 24px;
      transform: translateX(104%);
      transition: transform 220ms ease;
      z-index: 21;
      overflow: auto;
    }

    body.drawer-open .drawer-backdrop {
      opacity: 1;
      pointer-events: auto;
    }

    body.drawer-open .drawer {
      transform: translateX(0);
      animation: drawerIn 220ms ease;
    }

    .drawer-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
      margin-bottom: 16px;
    }

    .icon-badge {
      width: 48px;
      height: 48px;
      border-radius: 16px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: white;
      background: linear-gradient(135deg, var(--navy), var(--teal));
      margin-bottom: 12px;
    }

    .icon-badge svg {
      width: 24px;
      height: 24px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.9;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .close-button {
      width: 40px;
      height: 40px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: white;
      cursor: pointer;
      font: inherit;
    }

    .drawer-grid {
      display: grid;
      gap: 12px;
      margin-top: 16px;
    }

    .drawer-card {
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.86);
      padding: 14px;
    }

    .drawer-card strong {
      display: block;
      margin-bottom: 6px;
    }

    @media (max-width: 1120px) {
      .hero-grid,
      .board {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 820px) {
      .shell {
        width: min(100vw - 18px, 100%);
        margin-top: 18px;
      }

      .hero, .panel { padding: 20px; }
      .metric-grid, .stats-grid, .summary-grid, .progress-grid { grid-template-columns: 1fr; }
      .hero-copy h1 { max-width: none; }
    }
  </style>
</head>
<body>
  <div class="drawer-backdrop" id="drawer-backdrop"></div>
  <aside class="drawer" id="feature-drawer" aria-hidden="true">
    <div class="drawer-head">
      <div>
        <div class="icon-badge" id="drawer-icon"></div>
        <h2 id="drawer-title">Feature details</h2>
        <p class="subtle" id="drawer-description">Click a hero card to inspect its role in the system.</p>
      </div>
      <button class="close-button" id="drawer-close" type="button">✕</button>
    </div>
    <div class="example-row" id="drawer-badges"></div>
    <div class="drawer-grid" id="drawer-grid"></div>
  </aside>

  <main class="shell">
    <section class="hero">
      <div class="hero-grid">
        <div class="hero-copy">
          <div class="eyebrow">Agentic AI System</div>
          <h1>Multi-step tasks with live orchestration visibility.</h1>
          <p>Submit a request, watch progress unfold in real time, and receive polished results through a responsive multi-agent workflow.</p>
        </div>
        <div class="metric-grid">
          <button class="metric-card active" type="button" data-feature="pipeline">
            <div class="metric-icon"><svg viewBox="0 0 24 24"><path d="M5 6h5v5H5z"/><path d="M14 6h5v5h-5z"/><path d="M9 11v3a2 2 0 0 0 2 2h2"/><path d="M14 18h5v-5h-5z"/></svg></div>
            <div class="metric-label">Pipeline</div>
            <div class="metric-value">Async</div>
            <div class="metric-note">Explore how requests move from API to planner, scheduler, worker, and result delivery.</div>
          </button>
          <button class="metric-card" type="button" data-feature="streaming">
            <div class="metric-icon"><svg viewBox="0 0 24 24"><path d="M4 17c2.2-2.2 4.7-3.3 8-3.3S17.8 14.8 20 17"/><path d="M7 13c1.4-1.3 3.1-2 5-2s3.6.7 5 2"/><path d="M10 9c.6-.5 1.3-.8 2-.8s1.4.3 2 .8"/><path d="M12 19h.01"/></svg></div>
            <div class="metric-label">Streaming</div>
            <div class="metric-value">SSE Live</div>
            <div class="metric-note">See how users receive partial results and replayed events in real time.</div>
          </button>
          <button class="metric-card" type="button" data-feature="queue">
            <div class="metric-icon"><svg viewBox="0 0 24 24"><path d="M6 7h12"/><path d="M6 12h12"/><path d="M6 17h8"/><path d="M18 15v4"/><path d="M16 17h4"/></svg></div>
            <div class="metric-label">Queue</div>
            <div class="metric-value">Redis</div>
            <div class="metric-note">Inspect message-driven coordination, retries, task state, and event persistence.</div>
          </button>
          <button class="metric-card" type="button" data-feature="agents">
            <div class="metric-icon"><svg viewBox="0 0 24 24"><path d="M12 5v14"/><path d="M5 9l7-4 7 4"/><path d="M5 15l7 4 7-4"/><path d="M5 9v6"/><path d="M19 9v6"/></svg></div>
            <div class="metric-label">Agents</div>
            <div class="metric-value">3 Roles</div>
            <div class="metric-note">Understand the Retriever, Analyzer, and Writer responsibility boundaries.</div>
          </button>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <h2>Operational Snapshot</h2>
          <p class="subtle">Live counters and compact charts summarize throughput, completions, failures, and recently queued work using the current task history.</p>
        </div>
      </div>
      <div class="stats-grid">
        <article class="stat-card">
          <div class="stat-label">Total tasks</div>
          <div class="stat-value" id="stat-total">0</div>
          <div class="micro-chart" id="chart-total"></div>
        </article>
        <article class="stat-card">
          <div class="stat-label">Completed</div>
          <div class="stat-value" id="stat-completed">0</div>
          <div class="micro-chart" id="chart-completed"></div>
        </article>
        <article class="stat-card">
          <div class="stat-label">Failed</div>
          <div class="stat-value" id="stat-failed">0</div>
          <div class="micro-chart" id="chart-failed"></div>
        </article>
        <article class="stat-card">
          <div class="stat-label">In queue / running</div>
          <div class="stat-value" id="stat-active">0</div>
          <div class="micro-chart" id="chart-active"></div>
        </article>
      </div>
    </section>

    <section class="board">
      <div class="stack">
        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>Run a Task</h2>
              <p class="subtle">Accept a complex user task, break it into multiple steps, assign those steps to specialist agents, and surface the result in a polished user-facing panel.</p>
            </div>
          </div>
          <form id="task-form">
            <textarea id="task-input" placeholder="Example: Write a professional leave email for 3 days, research customer churn drivers, or prepare an executive brief."></textarea>
            <div class="example-row">
              <button class="chip" type="button" data-example="Write a professional leave email for 3 days.">3-day leave email</button>
              <button class="chip" type="button" data-example="Research customer churn drivers and create an executive summary.">Executive summary</button>
              <button class="chip" type="button" data-example="Gather customer feedback themes and draft a short action plan.">Action plan</button>
            </div>
            <div class="actions">
              <button class="primary" id="submit-button" type="submit">Launch Task</button>
              <button class="ghost-button" id="clear-button" type="button">Clear</button>
            </div>
          </form>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>Current Task</h2>
              <p class="subtle" id="task-caption">Submit a task or select one from recent runs.</p>
            </div>
          </div>
          <div class="status-row">
            <span class="badge violet" id="task-status">idle</span>
            <span class="badge" id="task-id">no task selected</span>
          </div>
          <div class="summary-grid">
            <article class="summary-card"><span>Progress</span><strong id="progress-value">0/3</strong></article>
            <article class="summary-card"><span>Events</span><strong id="event-count">0</strong></article>
          </div>
          <div class="progress-grid">
            <article class="step-card" data-step="1"><div class="step-label">Step 1</div><div class="step-title">Retriever</div><div class="subtle">Fetch supporting context and relevant data.</div></article>
            <article class="step-card" data-step="2"><div class="step-label">Step 2</div><div class="step-title">Analyzer</div><div class="subtle">Analyze the retrieved context and extract insights.</div></article>
            <article class="step-card" data-step="3"><div class="step-label">Step 3</div><div class="step-title">Writer</div><div class="subtle">Generate the final user-facing response.</div></article>
          </div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>Final Result</h2>
            </div>
          </div>
          <div class="result-box" id="final-result">No result yet.</div>
        </section>
      </div>

      <div class="stack">
        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>Live Activity</h2>
              <p class="subtle">Track streaming status changes as the task progresses through queueing, execution, completion, or failure.</p>
            </div>
            <div class="toggle-row">
              <button class="toggle" id="technical-toggle" type="button">Show technical details</button>
            </div>
          </div>
          <div class="timeline" id="timeline">
            <div class="empty">No events yet. Launch a task to see the agentic workflow come alive.</div>
          </div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2>Recent Tasks</h2>
              <p class="subtle">Replay older runs to inspect the system’s streaming behavior and final results without re-submitting a request.</p>
            </div>
          </div>
          <div class="task-list" id="task-list">
            <div class="empty">No tasks available yet.</div>
          </div>
        </section>
      </div>
    </section>
  </main>

  <script>
    const FEATURE_CONTENT = {
      pipeline: {
        icon: '<svg viewBox="0 0 24 24"><path d="M5 6h5v5H5z"/><path d="M14 6h5v5h-5z"/><path d="M9 11v3a2 2 0 0 0 2 2h2"/><path d="M14 18h5v-5h-5z"/></svg>',
        title: "Async Pipeline",
        description: "Requests move smoothly from intake to planning, execution, and final delivery without blocking the rest of the experience.",
        badges: ["Async", "Responsive", "Coordinated flow"],
        cards: [
          { title: "Accept a complex task", body: "The API stores the request as a durable task record before planning starts." },
          { title: "Break into steps", body: "The planner decomposes the task into retriever, analyzer, and writer stages with dependencies." },
          { title: "Non-blocking orchestration", body: "Scheduling and worker execution stay asynchronous so multiple tasks can move concurrently." },
          { title: "Scalable direction", body: "This pattern can expand to multi-worker pools, dedicated planners, and agent-specific queues." }
        ]
      },
      streaming: {
        icon: '<svg viewBox="0 0 24 24"><path d="M4 17c2.2-2.2 4.7-3.3 8-3.3S17.8 14.8 20 17"/><path d="M7 13c1.4-1.3 3.1-2 5-2s3.6.7 5 2"/><path d="M10 9c.6-.5 1.3-.8 2-.8s1.4.3 2 .8"/><path d="M12 19h.01"/></svg>',
        title: "Streaming Responses",
        description: "Live status updates keep the experience transparent, giving users instant feedback while work continues in the background.",
        badges: ["Live updates", "SSE", "Real-time UX"],
        cards: [
          { title: "Live progress", body: "Every meaningful state transition is published so the user sees motion before the final answer arrives." },
          { title: "Replay support", body: "Recent event history is stored so the dashboard can catch up even after a task completes." },
          { title: "Human-friendly surface", body: "The final panel stays readable while raw payloads remain optional." },
          { title: "Evaluator depth", body: "Technical mode exposes the detailed event payloads for architecture review." }
        ]
      },
      queue: {
        icon: '<svg viewBox="0 0 24 24"><path d="M6 7h12"/><path d="M6 12h12"/><path d="M6 17h8"/><path d="M18 15v4"/><path d="M16 17h4"/></svg>',
        title: "Redis Queue and State",
        description: "The coordination layer keeps work organized, durable, and easy to observe as tasks move across the platform.",
        badges: ["Queue", "State", "Resilience"],
        cards: [
          { title: "Message-driven communication", body: "The API, scheduler, and worker communicate through queue messages instead of direct blocking calls." },
          { title: "Fault tolerance", body: "Transient failures are retried with exponential backoff and terminal failures are persisted." },
          { title: "State visibility", body: "Task status, intermediate outputs, and final results stay queryable through the same backend." },
          { title: "Production readiness", body: "The design can evolve toward partitioned queues or durable event stores as volume grows." }
        ]
      },
      agents: {
        icon: '<svg viewBox="0 0 24 24"><path d="M12 5v14"/><path d="M5 9l7-4 7 4"/><path d="M5 15l7 4 7-4"/><path d="M5 9v6"/><path d="M19 9v6"/></svg>',
        title: "Specialized Agents",
        description: "Each specialist has a focused role, making the workflow easier to extend, reason about, and trust.",
        badges: ["Specialists", "Modular", "Extendable"],
        cards: [
          { title: "Retriever", body: "Collects internal or external context and prepares structured source material for downstream work." },
          { title: "Analyzer", body: "Turns context into insights, guidance, and reasoning summaries for the final response." },
          { title: "Writer", body: "Produces the final user-facing answer such as leave emails, summaries, and executive briefs." },
          { title: "Extensibility", body: "You can add validators, reviewers, or tool-using specialists without redesigning the full pipeline." }
        ]
      }
    };

    const metricCards = Array.from(document.querySelectorAll(".metric-card"));
    const drawer = document.getElementById("feature-drawer");
    const drawerBackdrop = document.getElementById("drawer-backdrop");
    const drawerClose = document.getElementById("drawer-close");
    const drawerIcon = document.getElementById("drawer-icon");
    const drawerTitle = document.getElementById("drawer-title");
    const drawerDescription = document.getElementById("drawer-description");
    const drawerBadges = document.getElementById("drawer-badges");
    const drawerGrid = document.getElementById("drawer-grid");

    const taskForm = document.getElementById("task-form");
    const taskInput = document.getElementById("task-input");
    const submitButton = document.getElementById("submit-button");
    const clearButton = document.getElementById("clear-button");
    const technicalToggle = document.getElementById("technical-toggle");
    const taskStatus = document.getElementById("task-status");
    const taskId = document.getElementById("task-id");
    const taskCaption = document.getElementById("task-caption");
    const timeline = document.getElementById("timeline");
    const taskList = document.getElementById("task-list");
    const finalResult = document.getElementById("final-result");
    const progressValue = document.getElementById("progress-value");
    const eventCount = document.getElementById("event-count");
    const stepCards = Array.from(document.querySelectorAll(".step-card"));
    const exampleButtons = Array.from(document.querySelectorAll("[data-example]"));

    const statTotal = document.getElementById("stat-total");
    const statCompleted = document.getElementById("stat-completed");
    const statFailed = document.getElementById("stat-failed");
    const statActive = document.getElementById("stat-active");

    let source = null;
    let activeTaskId = null;
    let currentEvents = [];
    let lastTasks = [];

    function pretty(value) {
      if (value === null || value === undefined || value === "") return "No additional content.";
      return typeof value === "string" ? value : JSON.stringify(value, null, 2);
    }

    function statusClass(status) {
      if (status === "failed") return "danger";
      if (["queued", "planning", "running", "in_progress"].includes(status)) return "warn";
      if (status === "completed") return "success";
      return "violet";
    }

    function eventSummary(event) {
      if (event.status === "queued") return "This step has been accepted and placed into the execution queue.";
      if (event.status === "in_progress") return "An agent is actively working on this step now.";
      if (event.status === "step_completed") return "The step finished successfully and unlocked the next action.";
      if (event.status === "completed") return "The full task completed and the final answer is ready.";
      if (event.status === "failed") return "The task hit a failure state after processing.";
      return "The task state changed.";
    }

    function setStatus(status, id) {
      taskStatus.textContent = status || "idle";
      taskStatus.className = `badge ${statusClass(status || "idle")}`.trim();
      taskId.textContent = id || "no task selected";
      taskId.className = "badge";
    }

    function openDrawer(featureKey) {
      const feature = FEATURE_CONTENT[featureKey];
      if (!feature) return;

      metricCards.forEach((card) => card.classList.toggle("active", card.dataset.feature === featureKey));
      drawerIcon.innerHTML = feature.icon;
      drawerTitle.textContent = feature.title;
      drawerDescription.textContent = feature.description;
      drawerBadges.innerHTML = "";
      drawerGrid.innerHTML = "";

      feature.badges.forEach((badge) => {
        const span = document.createElement("span");
        span.className = "badge";
        span.textContent = badge;
        drawerBadges.appendChild(span);
      });

      feature.cards.forEach((item) => {
        const card = document.createElement("article");
        card.className = "drawer-card";
        card.innerHTML = `<strong>${item.title}</strong><p class="subtle">${item.body}</p>`;
        drawerGrid.appendChild(card);
      });

      document.body.classList.add("drawer-open");
      drawer.setAttribute("aria-hidden", "false");
    }

    function closeDrawer() {
      document.body.classList.remove("drawer-open");
      drawer.setAttribute("aria-hidden", "true");
      metricCards.forEach((card) => card.classList.remove("active"));
    }

    function resetProgress() {
      stepCards.forEach((card) => { card.className = "step-card"; });
      progressValue.textContent = "0/3";
    }

    function updateProgress(events) {
      const completed = new Set(
        events.filter((event) => event.status === "step_completed" && event.step_id).map((event) => String(event.step_id))
      );
      const active = [...events].reverse().find((event) => ["queued", "in_progress"].includes(event.status) && event.step_id);

      stepCards.forEach((card) => {
        const step = card.dataset.step;
        card.className = "step-card";
        if (completed.has(step)) {
          card.classList.add("done");
        } else if (active && String(active.step_id) === step) {
          card.classList.add("active");
        }
      });

      progressValue.textContent = `${completed.size}/3`;
    }

    function renderEvents() {
      eventCount.textContent = String(currentEvents.length);
      updateProgress(currentEvents);

      if (!currentEvents.length) {
        timeline.innerHTML = '<div class="empty">No events yet. Launch a task to see the agentic workflow come alive.</div>';
        return;
      }

      timeline.innerHTML = "";
      [...currentEvents].reverse().forEach((event, index) => {
        const article = document.createElement("article");
        article.className = `event-card ${index === 0 ? "latest" : ""}`;
        const title = event.step ? `Step ${event.step_id}: ${event.step}` : "Task-level event";
        article.innerHTML = `
          <div class="event-top">
            <div>
              <div class="event-label">${event.status}</div>
              <div class="event-time">${title}</div>
            </div>
            <div class="event-time">${new Date(event.timestamp).toLocaleTimeString()}</div>
          </div>
          <div class="subtle">${eventSummary(event)}</div>
          <div class="technical-only"><pre>${pretty(event.partial_result ?? event.error)}</pre></div>
        `;
        timeline.appendChild(article);
      });
    }

    function addEvent(event) {
      currentEvents.push(event);
      renderEvents();
    }

    function resetTaskView() {
      currentEvents = [];
      finalResult.textContent = "No result yet.";
      eventCount.textContent = "0";
      resetProgress();
      renderEvents();
    }

    function renderChart(containerId, values, type = "normal") {
      const container = document.getElementById(containerId);
      container.innerHTML = "";
      const safeValues = values.length ? values : [0];
      const max = Math.max(...safeValues, 1);
      safeValues.forEach((value) => {
        const bar = document.createElement("div");
        bar.className = `bar ${type === "failed" ? "fail" : type === "queue" ? "queue" : ""}`.trim();
        bar.style.height = `${Math.max((value / max) * 30, value > 0 ? 8 : 4)}px`;
        container.appendChild(bar);
      });
    }

    function updateStats(tasks) {
      lastTasks = tasks;
      const total = tasks.length;
      const completed = tasks.filter((task) => task.status === "completed").length;
      const failed = tasks.filter((task) => task.status === "failed").length;
      const active = tasks.filter((task) => ["queued", "running", "planning"].includes(task.status)).length;

      statTotal.textContent = String(total);
      statCompleted.textContent = String(completed);
      statFailed.textContent = String(failed);
      statActive.textContent = String(active);

      const recent = tasks.slice(-6);
      renderChart("chart-total", recent.map((_, index) => index + 1));
      renderChart("chart-completed", recent.map((task) => task.status === "completed" ? 1 : 0));
      renderChart("chart-failed", recent.map((task) => task.status === "failed" ? 1 : 0), "failed");
      renderChart("chart-active", recent.map((task) => ["queued", "running", "planning"].includes(task.status) ? 1 : 0), "queue");
    }

    async function loadTasks() {
      const response = await fetch("/api/v1/tasks");
      const tasks = await response.json();
      updateStats(tasks);
      taskList.innerHTML = "";

      if (!tasks.length) {
        taskList.innerHTML = '<div class="empty">No tasks available yet.</div>';
        return;
      }

      tasks.slice().reverse().forEach((task) => {
        const card = document.createElement("button");
        card.type = "button";
        card.className = `task-card ${task.task_id === activeTaskId ? "active" : ""}`;
        card.innerHTML = `
          <div class="task-top">
            <div class="task-title">${task.user_task}</div>
            <span class="badge ${statusClass(task.status)}">${task.status}</span>
          </div>
          <div class="task-meta">${new Date(task.created_at).toLocaleString()}</div>
          <div class="task-meta">${task.task_id}</div>
        `;
        card.addEventListener("click", () => selectTask(task.task_id, true));
        taskList.appendChild(card);
      });
    }

    async function selectTask(id, clearFirst = false) {
      if (source) source.close();
      activeTaskId = id;
      if (clearFirst) resetTaskView();

      const response = await fetch(`/api/v1/tasks/${id}`);
      const payload = await response.json();
      const task = payload.task;
      setStatus(task.status, task.task_id);
      taskCaption.textContent = task.user_task;
      finalResult.textContent = task.final_result || "Waiting for final result...";
      await loadTasks();

      source = new EventSource(`/api/v1/stream/${id}`);
      source.onmessage = (message) => {
        const event = JSON.parse(message.data);
        addEvent(event);
        setStatus(event.status, event.task_id);
        if (event.status === "completed") {
          finalResult.textContent = pretty(event.partial_result);
          source.close();
          loadTasks();
        }
        if (event.status === "failed") {
          finalResult.textContent = pretty(event.error || "Task failed");
          source.close();
          loadTasks();
        }
      };
      source.onerror = () => {
        if (source) source.close();
      };
    }

    exampleButtons.forEach((button) => {
      button.addEventListener("click", () => {
        taskInput.value = button.dataset.example;
        taskInput.focus();
      });
    });

    clearButton.addEventListener("click", () => {
      taskInput.value = "";
      taskInput.focus();
    });

    technicalToggle.addEventListener("click", () => {
      document.body.classList.toggle("show-technical");
      technicalToggle.classList.toggle("active");
      technicalToggle.textContent = document.body.classList.contains("show-technical") ? "Hide technical details" : "Show technical details";
    });

    metricCards.forEach((card) => {
      card.addEventListener("click", () => openDrawer(card.dataset.feature));
    });

    drawerBackdrop.addEventListener("click", closeDrawer);
    drawerClose.addEventListener("click", closeDrawer);
    window.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeDrawer();
    });

    taskForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const task = taskInput.value.trim();
      if (!task) return;

      submitButton.disabled = true;
      submitButton.textContent = "Launching...";
      resetTaskView();

      const response = await fetch("/api/v1/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),
      });
      const payload = await response.json();
      await selectTask(payload.task_id);

      submitButton.disabled = false;
      submitButton.textContent = "Launch Task";
    });

    updateStats([]);
    loadTasks();
  </script>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    return HTMLResponse(DASHBOARD_HTML)
