"""
============================================================
  AUTOSCALING ANALYSIS — MISSION CONTROL DASHBOARD
  Streamlit Demo | Real-time server fleet simulation
============================================================
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import math
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# 0.  PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ AutoScale Mission Control",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# 1.  GLOBAL CSS  — Mission-Control dark theme
# ──────────────────────────────────────────────
CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;500;700&display=swap');

/* ── Root palette ── */
:root {
    --bg-deep:    #04060d;
    --bg-card:    #0b0f1a;
    --bg-card2:   #111828;
    --border:     #1e2a45;
    --cyan:       #00e5ff;
    --cyan-dim:   #00e5ff33;
    --green:      #39ff14;
    --green-dim:  #39ff1433;
    --amber:      #ffb300;
    --amber-dim:  #ffb30033;
    --red:        #ff3b5c;
    --red-dim:    #ff3b5c33;
    --text-hi:    #e8edf5;
    --text-lo:    #6b7a99;
}

/* ── Reset & body ── */
html, body { background: var(--bg-deep) !important; }
.stApp {
    background: var(--bg-deep);
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-hi);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
.stApp header                { display: none !important; }
.stApp .stSidebar            { display: none !important; }
#MainMenu, footer            { visibility: hidden !important; }
.block-container              { padding: 12px 18px !important; max-width: 100% !important; }

/* ── Titles ── */
h1 { font-family: 'Orbitron', monospace !important; color: var(--cyan) !important;
      font-size: 1.55rem !important; letter-spacing: 3px; text-transform: uppercase;
      margin-bottom: 2px !important; }
h3 { font-family: 'Orbitron', monospace !important; color: var(--cyan) !important;
      font-size: 0.72rem !important; letter-spacing: 2px; text-transform: uppercase;
      margin: 0 !important; opacity: 0.85; }

/* ── Card glass ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.6;
}

/* ── Big metric number ── */
.metric-num {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--cyan);
    line-height: 1.1;
}
.metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78rem;
    color: var(--text-lo);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 3px;
}
.metric-unit { font-size: 1rem; color: var(--text-lo); }

/* ── Status badge ── */
.badge {
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.badge-live   { background: var(--green-dim); color: var(--green); border: 1px solid var(--green); }
.badge-warn   { background: var(--amber-dim); color: var(--amber); border: 1px solid var(--amber); }
.badge-crit   { background: var(--red-dim);   color: var(--red);   border: 1px solid var(--red); }
.badge-idle   { background: var(--cyan-dim);  color: var(--cyan);  border: 1px solid var(--cyan); }

/* ── Pulse animation for LIVE ── */
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 4px var(--green); }
    50%      { box-shadow: 0 0 12px var(--green), 0 0 20px var(--green-dim); }
}
.pulse { animation: pulse-dot 1.8s ease-in-out infinite; }

/* ── Server card grid ── */
.server-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }
.server-card {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 8px;
    text-align: center;
    transition: all 0.35s ease;
}
.server-card.active   { border-color: var(--green); box-shadow: 0 0 10px var(--green-dim); }
.server-card.scaling  { border-color: var(--amber); box-shadow: 0 0 14px var(--amber-dim);
                         animation: pulse-amber 0.6s ease 3; }
.server-card.inactive { opacity: 0.25; }
@keyframes pulse-amber {
    0%, 100% { transform: scale(1); }
    50%      { transform: scale(1.06); }
}

/* ── Progress bar (CPU) ── */
.cpu-bar-bg {
    width: 100%; height: 7px; background: var(--bg-deep); border-radius: 4px;
    margin-top: 6px; overflow: hidden;
}
.cpu-bar-fill {
    height: 100%; border-radius: 4px;
    transition: width 0.4s ease, background 0.4s ease;
}

/* ── Scaling event log ── */
.event-row {
    display: flex; align-items: center; gap: 10px;
    padding: 5px 0; border-bottom: 1px solid var(--border);
    font-family: 'Share Tech Mono', monospace; font-size: 0.72rem;
}
.event-row:last-child { border-bottom: none; }
.event-time { color: var(--text-lo); min-width: 80px; }

/* ── Tabs override ── */
.stTabs [data-baseid="tab-bar"] { border-bottom: 1px solid var(--border) !important; }
.stTabs button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    color: var(--text-lo) !important;
    border: none !important;
    background: transparent !important;
    padding: 6px 18px !important;
}
.stTabs button[aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important;
    background: var(--cyan-dim) !important;
}

/* ── Buttons ── */
.stButton button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 2px !important;
    border-radius: 6px !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-card2) !important;
    color: var(--text-hi) !important;
    transition: all 0.25s !important;
}
.stButton button:hover {
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 10px var(--cyan-dim) !important;
}

/* ── Selectbox / widget dark ── */
.stSelectbox select, .stSlider input {
    background: var(--bg-card2) !important;
    color: var(--text-hi) !important;
    border-color: var(--border) !important;
}
.stSlider .stSlider-track { background: var(--cyan) !important; }

/* ── Alert override ── */
.stAlert { border-radius: 8px !important; font-family: 'Rajdhani', sans-serif !important; }

/* ── Plotly chart containers ── */
.stPlotly { border-radius: 8px; overflow: hidden; }
</style>
"""


# ──────────────────────────────────────────────
# 2.  DATA GENERATION  — Realistic NASA-style traffic
# ──────────────────────────────────────────────

def generate_nasa_traffic(total_hours: int = 72) -> pd.DataFrame:
    """
    Simulate 72 h (3 days) of HTTP-request traffic that mirrors
    the NASA Jul-1995 log characteristics:
      • Daily sinusoidal cycle (peak ~14:00 UTC)
      • Weekly-style weekend dip (we fake it with day-2 dip)
      • A sharp DDoS-style spike at hour 38
      • A "storm-off" gap at hour 52-53  (0 traffic)
      • Gaussian noise layered on top
    """
    np.random.seed(42)
    minutes = total_hours * 60                          # 1-min resolution base
    t = np.arange(minutes)

    # base daily cycle
    daily   = 3000 + 2500 * np.sin(2 * np.pi * t / 1440 - np.pi / 2)   # peak noon
    # slight weekly pattern (day-2 = "weekend" dip)
    weekly  = np.where((t >= 1440) & (t < 2880), 0.7, 1.0)
    # noise
    noise   = np.random.normal(0, 300, minutes)
    # combine
    raw     = (daily * weekly + noise).clip(min=50)

    # ── DDoS spike at hour 38 (minute 2280), lasts 25 min ──
    spike_center = 2280
    spike_window = np.exp(-0.5 * ((t - spike_center) / 6) ** 2)
    raw += spike_window * 18_000                        # huge burst

    # ── "Storm" gap  hour 52-53 ──
    storm_start, storm_end = 3120, 3180
    raw[storm_start:storm_end] = 0

    # ── byte size: ~2-8 KB per request, correlated ──
    bytes_per_req = np.random.uniform(2000, 8000, minutes)
    total_bytes   = (raw * bytes_per_req).astype(int)

    # ── error rate  (higher during spike / storm edges) ──
    error_base = np.random.beta(1, 30, minutes)
    error_base[spike_center - 5: spike_center + 30] += 0.15
    error_base[storm_end: storm_end + 40] += 0.08
    error_rate = error_base.clip(0, 1)

    timestamps = pd.date_range("2025-08-20 00:00", periods=minutes, freq="1min")

    df = pd.DataFrame({
        "timestamp":  timestamps,
        "requests":   raw.astype(int),
        "bytes":      total_bytes,
        "error_rate": error_rate,
    })
    return df


def aggregate(df: pd.DataFrame, window_min: int) -> pd.DataFrame:
    """Resample to *window_min*-minute buckets."""
    df2 = df.set_index("timestamp").resample(f"{window_min}min").agg(
        requests=("requests", "sum"),
        bytes   =("bytes",    "sum"),
        error_rate=("error_rate", "mean"),
    ).reset_index()
    return df2


# ──────────────────────────────────────────────
# 3.  FORECAST  — simple but realistic prediction
# ──────────────────────────────────────────────

def simple_forecast(series: np.ndarray, horizon: int = 12) -> np.ndarray:
    """
    Exponential-smoothing-style forecast + slight trend.
    Returns *horizon* future values.  Very fast, no heavy deps.
    """
    alpha, beta = 0.35, 0.08
    level   = series[-1]
    trend   = (series[-1] - series[-2]) * beta if len(series) > 1 else 0.0
    out     = []
    for _ in range(horizon):
        level += trend
        out.append(level)
        # mean-revert
        level = alpha * level + (1 - alpha) * np.mean(series[-max(len(series), 20):])
    return np.array(out).clip(min=0)


# ──────────────────────────────────────────────
# 4.  AUTOSCALER  — threshold + cooldown logic
# ──────────────────────────────────────────────

class Autoscaler:
    """
    Stateful autoscaler that mirrors the contest rules:
      • scale-out  if forecast > high_thresh  for *sustain* ticks
      • scale-in   if forecast < low_thresh   for *sustain* ticks
      • cooldown   prevents flapping
    """
    def __init__(self, min_servers=2, max_servers=12,
                 high_thresh=4500, low_thresh=1800,
                 sustain=5, cooldown=10,
                 per_server_capacity=1200):
        self.min_s          = min_servers
        self.max_s          = max_servers
        self.high_thresh    = high_thresh
        self.low_thresh     = low_thresh
        self.sustain        = sustain          # ticks above/below thresh
        self.cooldown       = cooldown         # ticks to wait after action
        self.cap            = per_server_capacity
        # state
        self.servers        = min_servers
        self.cooldown_left  = 0
        self.above_count    = 0
        self.below_count    = 0
        self.events         = []               # (tick, action, servers_after)

    def step(self, tick: int, predicted_load: float) -> int:
        if self.cooldown_left > 0:
            self.cooldown_left -= 1
            return self.servers

        if predicted_load > self.high_thresh:
            self.above_count  += 1
            self.below_count   = 0
        elif predicted_load < self.low_thresh:
            self.below_count  += 1
            self.above_count   = 0
        else:
            self.above_count   = 0
            self.below_count   = 0

        action = None
        if self.above_count >= self.sustain and self.servers < self.max_s:
            needed = math.ceil(predicted_load / self.cap)
            self.servers = min(needed, self.max_s)
            action = "SCALE-OUT ↑"
            self.cooldown_left = self.cooldown
            self.above_count   = 0
        elif self.below_count >= self.sustain and self.servers > self.min_s:
            needed = max(math.ceil(predicted_load / self.cap), self.min_s)
            self.servers = needed
            action = "SCALE-IN  ↓"
            self.cooldown_left = self.cooldown
            self.below_count   = 0

        if action:
            self.events.append((tick, action, self.servers))

        return self.servers


# ──────────────────────────────────────────────
# 5.  PRE-COMPUTE full simulation for each granularity
# ──────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def precompute_simulation():
    """Run full sim once; cache result."""
    raw_df  = generate_nasa_traffic(total_hours=72)

    results = {}
    for g in [1, 5, 15]:
        agg = aggregate(raw_df, g).reset_index(drop=True)
        n   = len(agg)

        # run forecast + autoscaler across every tick
        scaler       = Autoscaler(
            high_thresh = 4500 * g,   # scale thresholds with granularity
            low_thresh  = 1800 * g,
            sustain     = max(2, 5 // g),
            cooldown    = max(3, 10 // g),
            per_server_capacity = 1200 * g,
        )
        forecasts    = np.zeros(n)
        server_hist  = np.zeros(n, dtype=int)
        cpu_hist     = np.zeros(n)
        events       = []

        for i in range(n):
            # naive forecast horizon = 12 ticks ahead (already computed at i)
            window = agg["requests"].values[:i+1]
            if i >= 3:
                fcast = simple_forecast(window, horizon=1)[0]
            else:
                fcast = window[-1]
            forecasts[i] = fcast

            srv = scaler.step(i, fcast)
            server_hist[i] = srv
            cap = srv * 1200 * g
            cpu_hist[i]    = min((agg["requests"].values[i] / cap) * 100, 100) if cap > 0 else 100

        events = scaler.events

        results[g] = {
            "df":         agg,
            "forecasts":  forecasts,
            "servers":    server_hist,
            "cpu":        cpu_hist,
            "events":     events,
        }
    return results, raw_df


# ──────────────────────────────────────────────
# 6.  COST MODEL
# ──────────────────────────────────────────────
COST_PER_SERVER_HOUR = 0.045   # USD  (e.g. small EC2)

def compute_cost(server_hist: np.ndarray, minutes_per_tick: int) -> float:
    """Total $ for the simulation window."""
    server_hours = server_hist.sum() * (minutes_per_tick / 60.0)
    return server_hours * COST_PER_SERVER_HOUR


# ──────────────────────────────────────────────
# 7.  PLOTLY CHART BUILDERS
# ──────────────────────────────────────────────

def _dark_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(family="Orbitron", size=11, color="#6b7a99"),
                   x=0.02, xanchor="left"),
        paper_bgcolor="#04060d",
        plot_bgcolor="#0b0f1a",
        margin=dict(l=42, r=18, t=32, b=32),
        font=dict(family="Share Tech Mono", size=10, color="#6b7a99"),
        xaxis=dict(showgrid=True, gridcolor="#1e2a45", showline=False,
                   tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor="#1e2a45", showline=False,
                   tickfont=dict(size=9)),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center",
                    font=dict(size=9)),
    )


def chart_main(agg_df, forecasts, servers, pointer, gran_label):
    """
    Main chart: actual requests, forecast overlay, server count (secondary y).
    Shows a sliding window of ±30 ticks around *pointer*.
    """
    n      = len(agg_df)
    lo     = max(0, pointer - 30)
    hi     = min(n, pointer + 15)
    ts     = agg_df["timestamp"].values[lo:hi]
    actual = agg_df["requests"].values[lo:hi]
    fcast  = forecasts[lo:hi]
    srv    = servers[lo:hi]
    # split actual into past / future relative to pointer
    split  = pointer - lo

    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"secondary_y": True}]],
    )

    # ── Actual (past) ──
    fig.add_trace(go.Scatter(
        x=ts[:split], y=actual[:split],
        mode="lines", name="Actual (past)",
        line=dict(color="#00e5ff", width=2.2),
    ), secondary_y=False)

    # ── Actual (future / unseen) — dimmed ──
    fig.add_trace(go.Scatter(
        x=ts[split:], y=actual[split:],
        mode="lines", name="Actual (future)",
        line=dict(color="#00e5ff", width=1.2, dash="dot"),
        opacity=0.35,
    ), secondary_y=False)

    # ── Forecast ──
    fig.add_trace(go.Scatter(
        x=ts, y=fcast,
        mode="lines", name="Forecast",
        line=dict(color="#ffb300", width=1.8, dash="dash"),
    ), secondary_y=False)

    # ── Forecast cone (±15 %) ──
    upper = fcast * 1.15
    lower = fcast * 0.85
    fig.add_trace(go.Scatter(
        x=ts, y=upper, mode="lines",
        line=dict(width=0), showlegend=False,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=ts, y=lower, mode="lines", name="Forecast ± 15 %",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(255,179,0,0.06)",
    ), secondary_y=False)

    # ── Server count ──
    fig.add_trace(go.Scatter(
        x=ts, y=srv,
        mode="lines+markers", name="Servers",
        line=dict(color="#39ff14", width=2),
        marker=dict(size=4, color="#39ff14"),
    ), secondary_y=True)

    # ── NOW line ──
    now_ts = agg_df["timestamp"].values[pointer]
    fig.add_shape(
        type="line",
        x0=now_ts, x1=now_ts, y0=0, y1=1,
        yref="y domain",
        line=dict(color="#ff3b5c", width=2, dash="dot"),
    )
    fig.add_annotation(
        x=now_ts, y=1, yref="y domain",
        text="NOW", showarrow=False,
        font=dict(family="Orbitron", size=9, color="#ff3b5c"),
        xanchor="left",
    )

    fig.update_layout(
        **_dark_layout(f"LIVE TRAFFIC  |  granularity: {gran_label}"),
        height=310,
    )
    fig.update_yaxes(title_text="Requests / window", secondary_y=False,
                     title_font=dict(size=9, color="#6b7a99"))
    fig.update_yaxes(title_text="Servers", secondary_y=True, range=[0, 14],
                     title_font=dict(size=9, color="#39ff14"))
    fig.update_xaxes(range=[ts[0], ts[-1]])

    return fig


def chart_cpu_errors(agg_df, cpu_hist, pointer):
    """Dual-axis: CPU % + error rate."""
    n  = len(agg_df)
    lo = max(0, pointer - 30)
    hi = min(n, pointer + 15)
    ts = agg_df["timestamp"].values[lo:hi]
    cpu= cpu_hist[lo:hi]
    err= agg_df["error_rate"].values[lo:hi] * 100

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=ts, y=cpu, mode="lines", name="CPU %",
        line=dict(color="#ff8c00", width=1.8),
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=ts, y=err, mode="lines", name="Error Rate %",
        line=dict(color="#ff3b5c", width=1.5, dash="dash"),
    ), secondary_y=True)

    # danger band at 80 % CPU
    fig.add_hrect(y0=80, y1=100, fillcolor="rgba(255,59,92,0.07)",
                  line_color="none", secondary_y=False)

    fig.update_layout(**_dark_layout("CPU & ERROR RATE"), height=200)
    fig.update_yaxes(title_text="CPU %",       range=[0, 105], secondary_y=False,
                     title_font=dict(size=9))
    fig.update_yaxes(title_text="Error Rate %", range=[0, 30],  secondary_y=True,
                     title_font=dict(size=9, color="#ff3b5c"))
    return fig


def chart_cost_comparison(sim_results):
    """Bar chart: total cost across 3 granularities."""
    labels, costs = [], []
    for g in [1, 5, 15]:
        labels.append(f"{g} min")
        costs.append(compute_cost(sim_results[g]["servers"], g))
    colors = ["#00e5ff", "#ffb300", "#39ff14"]

    fig = go.Figure(data=[go.Bar(
        x=labels, y=costs,
        marker_color=colors,
        marker_line_color=["#04060d"]*3,
        marker_line_width=2,
        text=[f"${c:.3f}" for c in costs],
        textposition="outside",
        textfont=dict(family="Share Tech Mono", size=11, color="#e8edf5"),
    )])
    layout = _dark_layout("COST COMPARISON  (72-hour window)")
    layout["height"] = 200
    layout["bargap"] = 0.45
    layout["yaxis"] = dict(title_text="Total Cost (USD)", title_font=dict(size=9),
                           showgrid=True, gridcolor="#1e2a45", range=[0, max(costs)*1.25])
    fig.update_layout(**layout)
    return fig


# ──────────────────────────────────────────────
# 8.  SERVER-CARD HTML builder
# ──────────────────────────────────────────────

def server_cards_html(active: int, max_s: int = 12, scaling_tick: int = -1,
                      current_tick: int = 0):
    """
    Return raw HTML for the server fleet grid.
    *scaling_tick* — if an event just happened within last 2 ticks, pulse that card.
    """
    cards = []
    for i in range(max_s):
        if i < active:
            cls = "server-card active"
            icon= "🟢"
            lbl = f"S-{i+1}"
            # cpu approx
            cpu_pct = min(int(np.random.uniform(30, 95)), 95)
        else:
            cls = "server-card inactive"
            icon= "⚪"
            lbl = f"S-{i+1}"
            cpu_pct = 0

        # pulse if this server just got added
        if scaling_tick >= 0 and (current_tick - scaling_tick) <= 2 and i >= (active - 2) and i < active:
            cls += " scaling"

        bar_color = "#39ff14" if cpu_pct < 60 else ("#ffb300" if cpu_pct < 80 else "#ff3b5c")

        cards.append(f"""
        <div class="{cls}">
            <div style="font-size:1.4rem">{icon}</div>
            <div style="font-family:'Share Tech Mono';font-size:0.72rem;color:#e8edf5">{lbl}</div>
            <div class="cpu-bar-bg">
                <div class="cpu-bar-fill" style="width:{cpu_pct}%;background:{bar_color}"></div>
            </div>
            <div style="font-family:'Share Tech Mono';font-size:0.6rem;color:#6b7a99;margin-top:3px">{cpu_pct}% CPU</div>
        </div>
        """)

    return f'<div class="server-grid">{"".join(cards)}</div>'


# ──────────────────────────────────────────────
# 9.  EVENT LOG HTML
# ──────────────────────────────────────────────

def event_log_html(events, agg_df, pointer, max_show=6):
    """Show most recent scaling events relative to current pointer."""
    # filter events up to pointer
    visible = [(t, a, s) for (t, a, s) in events if t <= pointer]
    visible = visible[-max_show:]          # last N
    rows    = []
    for t, action, srv in reversed(visible):
        ts_str = str(agg_df["timestamp"].values[t])[:16].replace("T", " ")
        color  = "#39ff14" if "OUT" in action else "#ff3b5c"
        badge  = "badge-live" if "OUT" in action else "badge-crit"
        rows.append(f"""
        <div class="event-row">
            <span class="event-time">{ts_str}</span>
            <span class="badge {badge}">{action}</span>
            <span style="color:#6b7a99">→ {srv} servers</span>
        </div>
        """)
    if not rows:
        rows.append('<div class="event-row"><span style="color:#6b7a99">No events yet …</span></div>')
    return "\n".join(rows)


# ──────────────────────────────────────────────
# 10.  ANOMALY DETECTOR  (simple z-score)
# ──────────────────────────────────────────────

def detect_anomaly(series: np.ndarray, pointer: int, window: int = 20, z_thresh: float = 2.5):
    """Return True if current value is anomalous."""
    if pointer < window:
        return False
    recent = series[pointer - window: pointer]
    mu, sigma = recent.mean(), recent.std()
    if sigma == 0:
        return False
    return abs(series[pointer] - mu) / sigma > z_thresh


# ──────────────────────────────────────────────
# 11.  MAIN  APP
# ──────────────────────────────────────────────

def main():
    st.markdown(CSS, unsafe_allow_html=True)

    # ── pre-compute ──
    sim, raw_df = precompute_simulation()

    # ── session state init ──
    if "pointer" not in st.session_state:
        st.session_state["pointer"]     = 30
    if "playing" not in st.session_state:
        st.session_state["playing"]     = False
    if "gran" not in st.session_state:
        st.session_state["gran"]        = 1
    if "speed" not in st.session_state:
        st.session_state["speed"]       = 5

    gran   = st.session_state["gran"]
    speed  = st.session_state["speed"]
    data   = sim[gran]
    agg_df = data["df"]
    n_ticks= len(agg_df)
    pointer= st.session_state["pointer"]
    pointer= min(pointer, n_ticks - 1)

    # ── TOP BAR ──────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:14px;padding:6px 0 10px 0">
        <span style="font-family:'Orbitron',monospace;font-size:1.3rem;
              color:#00e5ff;letter-spacing:4px;font-weight:900">⚡ AUTOSCALE</span>
        <span style="font-family:'Rajdhani',sans-serif;font-size:0.82rem;
              color:#6b7a99;letter-spacing:1px">MISSION CONTROL  /  REAL-TIME SIMULATION</span>
        <span class="badge badge-live pulse" style="margin-left:auto">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    # ── ROW 1: controls + top metrics ──────────
    ctrl_col, m1, m2, m3, m4 = st.columns([2.2, 1, 1, 1, 1], gap="small")

    # ─ Controls ─
    with ctrl_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Simulation Controls</h3>', unsafe_allow_html=True)

        # granularity tabs
        g_tabs = st.tabs(["⏱  1 min", "⏱  5 min", "⏱  15 min"])
        for idx, g_val in enumerate([1, 5, 15]):
            with g_tabs[idx]:
                if st.session_state["gran"] != g_val:
                    st.session_state["gran"]    = g_val
                    st.session_state["pointer"] = min(
                        st.session_state["pointer"],
                        len(sim[g_val]["df"]) - 1
                    )
                    st.rerun()

        # play / pause + speed
        btn_col1, btn_col2, spd_col = st.columns([1, 1, 2], gap="small")
        with btn_col1:
            if st.button("▶  PLAY" if not st.session_state["playing"] else "⏸  PAUSE",
                         use_container_width=True):
                st.session_state["playing"] = not st.session_state["playing"]
        with btn_col2:
            if st.button("⏮  RESET", use_container_width=True):
                st.session_state["pointer"] = 30
                st.session_state["playing"] = False
        with spd_col:
            st.session_state["speed"] = st.selectbox(
                "Speed", [1, 2, 5, 10, 20],
                index=[1,2,5,10,20].index(st.session_state["speed"]),
                label_visibility="collapsed",
            )

        # manual scrub slider
        st.session_state["pointer"] = st.slider(
            "Scrub timeline",
            min_value=5,
            max_value=n_ticks - 1,
            value=min(st.session_state["pointer"], n_ticks - 1),
            label_visibility="collapsed",
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # ─ Top metric cards ─
    active_servers = int(data["servers"][pointer])
    current_req    = int(agg_df["requests"].values[pointer])
    current_cpu    = data["cpu"][pointer]
    current_err    = agg_df["error_rate"].values[pointer] * 100
    total_cost     = compute_cost(data["servers"][:pointer+1], gran)

    is_anomaly = detect_anomaly(agg_df["requests"].values, pointer)
    anomaly_tag = '<span class="badge badge-crit" style="margin-left:8px">⚠ ANOMALY</span>' if is_anomaly else ""

    for col, label, value, unit, color, extra in [
        (m1, "SERVERS",    active_servers,  "",      "#39ff14", ""),
        (m2, "REQUESTS",   current_req,     f"/{gran}m", "#00e5ff", anomaly_tag),
        (m3, "AVG CPU",    f"{current_cpu:.0f}", "%", "#ffb300" if current_cpu < 80 else "#ff3b5c", ""),
        (m4, "COST SO FAR", f"{total_cost:.3f}", "USD", "#e8edf5", ""),
    ]:
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;min-height:90px;
                 display:flex;flex-direction:column;align-items:center;justify-content:center">
                <div class="metric-label">{label}</div>
                <div class="metric-num" style="color:{color}">{value}<span class="metric-unit">{unit}</span></div>
                {extra}
            </div>
            """, unsafe_allow_html=True)

    # ── ROW 2: main chart (full width) ──────────
    gran_label = f"{gran}-minute"
    fig_main = chart_main(agg_df, data["forecasts"], data["servers"], pointer, gran_label)
    st.plotly_chart(fig_main, use_container_width=True, config={"displayModeBar": False})

    # ── ROW 3: server fleet  |  cpu/err chart  |  event log ──
    srv_col, cpu_col, evt_col = st.columns([1.4, 2.2, 1.4], gap="small")

    with srv_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Server Fleet</h3>', unsafe_allow_html=True)
        # find last event tick for pulse
        last_evt_tick = -1
        for (t, a, s) in data["events"]:
            if t <= pointer:
                last_evt_tick = t
        st.markdown(
            server_cards_html(active_servers, max_s=12,
                              scaling_tick=last_evt_tick, current_tick=pointer),
            unsafe_allow_html=True,
        )
        st.markdown(f"""
        <div style="margin-top:10px;font-family:'Share Tech Mono';font-size:0.7rem;
             color:#6b7a99;border-top:1px solid #1e2a45;padding-top:6px">
            Capacity: {active_servers * 1200 * gran:,} req/{gran}m  |
            Load:     {current_req:,} req/{gran}m
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cpu_col:
        fig_cpu = chart_cpu_errors(agg_df, data["cpu"], pointer)
        st.plotly_chart(fig_cpu, use_container_width=True, config={"displayModeBar": False})

    with evt_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Scaling Events</h3>', unsafe_allow_html=True)
        st.markdown(
            event_log_html(data["events"], agg_df, pointer),
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 4: cost comparison (bottom) ──────────
    cost_col, info_col = st.columns([1.3, 1], gap="small")
    with cost_col:
        fig_cost = chart_cost_comparison(sim)
        st.plotly_chart(fig_cost, use_container_width=True, config={"displayModeBar": False})

    with info_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Autoscaler Policy</h3>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family:'Rajdhani',sans-serif;font-size:0.85rem;color:#a8b8d4;
             line-height:1.7">
            <b style="color:#00e5ff">Scale-out</b>  when forecast &gt; threshold
                — sustained {max(2, 5//gran)} ticks<br>
            <b style="color:#ff3b5c">Scale-in </b>  when forecast &lt; threshold
                — sustained {max(2, 5//gran)} ticks<br>
            <b style="color:#ffb300">Cooldown </b>  {max(3, 10//gran)} ticks after
                any action<br>
            <b style="color:#e8edf5">Min / Max</b>  2  …  12 servers<br>
            <b style="color:#e8edf5">Unit cost </b> ${COST_PER_SERVER_HOUR} / server·h<br><br>
            <span style="color:#6b7a99;font-size:0.78rem">
                Thresholds auto-scale with granularity so
                the policy stays meaningful at 1 m / 5 m / 15 m.
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── AUTO-ADVANCE (play mode) ──
    if st.session_state["playing"] and pointer < n_ticks - 1:
        time.sleep(0.18)                         # ~5 FPS
        st.session_state["pointer"] = min(pointer + speed, n_ticks - 1)
        if st.session_state["pointer"] >= n_ticks - 1:
            st.session_state["playing"] = False  # stop at end
        st.rerun()


# ──────────────────────────────────────────────
if __name__ == "__main__":
    main()
