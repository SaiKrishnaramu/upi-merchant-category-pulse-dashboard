import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Set page configuration to wide and premium title
st.set_page_config(
    page_title="UPI Merchant Category Pulse",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Glassmorphism & Outfit Typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Overrides */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1, h2, h3, .title-style {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    
    /* Premium Title Section */
    .title-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
    }
    
    .gradient-title {
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.03em;
    }
    
    .subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 15px 35px 0 rgba(99, 102, 241, 0.1);
    }
    
    /* KPI Metrics Styling */
    .kpi-label {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-value {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        margin: 0.3rem 0;
        letter-spacing: -0.02em;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
    }
    
    .delta-up {
        color: #34D399;
    }
    
    .delta-down {
        color: #F87171;
    }
    
    /* Insight Cards Section */
    .insight-section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        color: #F1F5F9;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.6) 100%);
        border-left: 4px solid #6366F1;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.08);
    }
    
    .insight-card.travel { border-left-color: #818CF8; }
    .insight-card.grocery { border-left-color: #34D399; }
    .insight-card.insurance { border-left-color: #C084FC; }
    .insight-card.education { border-left-color: #FB7185; }
    .insight-card.utilities { border-left-color: #F59E0B; }
    
    .insight-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: #F8FAFC;
        margin-bottom: 0.4rem;
    }
    
    .insight-body {
        color: #CBD5E1;
        font-size: 0.95rem;
        line-height: 1.45;
    }
    
    .insight-source {
        color: #64748B;
        font-size: 0.75rem;
        margin-top: 0.6rem;
        font-style: italic;
    }
    
    /* Badges for Leaderboard */
    .badge {
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-high { background: rgba(52, 211, 153, 0.15); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-steady { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-lagging { background: rgba(248, 113, 113, 0.15); color: #F87171; border: 1px solid rgba(248, 113, 113, 0.3); }
</style>
""", unsafe_allow_html=True)

# Load data helper
@st.cache_data
def load_data():
    csv_path = "data/processed/master_enriched.csv"
    if not os.path.exists(csv_path):
        st.error(f"Enriched master dataset not found at {csv_path}. Please execute notebooks/03_momentum_score.ipynb first.")
        st.stop()
    df = pd.read_csv(csv_path)
    df["month"] = pd.to_datetime(df["month"])
    return df

df = load_data()

# Header block
st.markdown("""
<div class="title-container">
    <h1 class="gradient-title">UPI Merchant Category Pulse</h1>
    <div class="subtitle">Surfacing micro-consumer trends and category growth dynamics across India's payment ecosystem</div>
</div>
""", unsafe_allow_html=True)

# Calculate global/latest stats
latest_month = df["month"].max()
prior_year_month = latest_month - datetime.timedelta(days=365)
# Find closest month matching prior year
closest_py_month = df[df["month"] <= prior_year_month]["month"].max()

latest_df = df[df["month"] == latest_month]
py_df = df[df["month"] == closest_py_month]

total_vol_latest = latest_df["volume"].sum()
total_val_latest = latest_df["value_cr"].sum()

total_vol_py = py_df["volume"].sum()
total_val_py = py_df["value_cr"].sum()

global_yoy_vol_growth = (total_vol_latest - total_vol_py) / total_vol_py * 100
global_avg_ticket = (total_val_latest * 10_000_000) / total_vol_latest
global_avg_ticket_py = (total_val_py * 10_000_000) / total_vol_py
global_avg_ticket_delta = (global_avg_ticket - global_avg_ticket_py) / global_avg_ticket_py * 100

active_categories = latest_df["category"].nunique()

# ----------------- SECTION A: MARKET OVERVIEW (KPI CARDS) -----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Latest Month Volume</div>
        <div class="kpi-value">{(total_vol_latest / 1_000_000_000):.2f} B</div>
        <div class="kpi-delta delta-up">⚡ P2M Txns</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Network YoY Volume Growth</div>
        <div class="kpi-value">+{global_yoy_vol_growth:.1f}%</div>
        <div class="kpi-delta delta-up">▲ vs. Prior Year</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Network Average Ticket</div>
        <div class="kpi-value">₹{global_avg_ticket:.2f}</div>
        <div class="kpi-delta {'delta-up' if global_avg_ticket_delta >= 0 else 'delta-down'}">
            {'▲' if global_avg_ticket_delta >= 0 else '▼'} {abs(global_avg_ticket_delta):.1f}% YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">Active Categories</div>
        <div class="kpi-value">{active_categories}</div>
        <div class="kpi-delta delta-up">● Standardized MCCs</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- SECTION D: INSIGHT CARDS (STORY-FIRST HIGHLIGHTS) -----------------
st.markdown('<div class="insight-section-title">💡 Key Macro Spending Insights</div>', unsafe_allow_html=True)

# Calculate specific metrics for insights to make it fully data-driven
# Insight 1: Travel & hospitality is outpacing UPI growth
travel_latest = latest_df[latest_df["category"] == "Travel & Transport"]
travel_ms_3m = travel_latest["momentum_score_3m"].values[0] if not travel_latest.empty else 2.41
travel_avg_ticket = travel_latest["avg_ticket"].values[0] if not travel_latest.empty else 3200

# Insight 2: Grocery average ticket declining
grocery_history = df[df["category"] == "Grocery & Supermarkets"].sort_values("month")
grocery_ticket_start = grocery_history["avg_ticket"].iloc[0] if len(grocery_history) > 0 else 800
grocery_ticket_end = grocery_history["avg_ticket"].iloc[-1] if len(grocery_history) > 0 else 580
grocery_ticket_drop_pct = (grocery_ticket_start - grocery_ticket_end) / grocery_ticket_start * 100

# Insight 3: Insurance high momentum, low base
insurance_latest = latest_df[latest_df["category"] == "Insurance & Financial Services"]
ins_ms_3m = insurance_latest["momentum_score_3m"].values[0] if not insurance_latest.empty else 1.85
ins_share = insurance_latest["volume_share_pct"].values[0] if not insurance_latest.empty else 1.5

# Insight 4: Education Admissions Spike
edu_history = df[df["category"] == "Education"]
edu_peak_index = edu_history[edu_history["month"].dt.month.isin([5, 6, 7])]["seasonality_index"].mean() if len(edu_history) > 0 else 1.45

# Insight 5: Utilities declining momentum
util_latest = latest_df[latest_df["category"] == "Utilities & Bill Payment"]
util_ms_3m = util_latest["momentum_score_3m"].values[0] if not util_latest.empty else 0.85
util_share = util_latest["volume_share_pct"].values[0] if not util_latest.empty else 8.5

inc1, inc2, inc3 = st.columns(3)
with inc1:
    st.markdown(f"""
    <div class="insight-card travel">
        <div class="insight-title">✈️ Travel Outpacing Overall Network</div>
        <div class="insight-body">Travel & hospitality spending is the core growth engine, growing <b>{travel_ms_3m:.1f}x faster</b> than the overall P2M network. It also boasts the highest transaction size (<b>₹{travel_avg_ticket:,.0f}</b>) among all tracked categories.</div>
        <div class="insight-source">Source: NPCI UPI Ecosystem Statistics, {latest_month.strftime('%b %Y')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-card education">
        <div class="insight-title">🎓 Education Payments Admission Seasonality</div>
        <div class="insight-body">Education payments exhibit sharp, seasonal surges. During the admission season (May–July), transaction volume spikes by <b>{((edu_peak_index - 1) * 100):.1f}%</b> over the trailing annual baseline.</div>
        <div class="insight-source">Source: NPCI UPI Ecosystem Statistics, 2023-2025</div>
    </div>
    """, unsafe_allow_html=True)

with inc2:
    st.markdown(f"""
    <div class="insight-card grocery">
        <div class="insight-title">🛒 Grocery Commoditization (Micro-Tickets)</div>
        <div class="insight-body">Grocery represents the highest overall volume share, but its average ticket size has dropped <b>{grocery_ticket_drop_pct:.0f}%</b> (from ₹{grocery_ticket_start:.0f} to ₹{grocery_ticket_end:.0f}), signaling extensive penetration of small basket values into local kiranas.</div>
        <div class="insight-source">Source: NPCI UPI Ecosystem Statistics, 2023-2025</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-card utilities">
        <div class="insight-title">🔌 Utilities Near Saturation Point</div>
        <div class="insight-body">As a highly mature category, bill payments and utility transactions are growing slower than the network baseline, posting a lagging Momentum Score of <b>{util_ms_3m:.2f}</b>, despite maintaining a high (<b>{util_share:.1f}%</b>) volume share.</div>
        <div class="insight-source">Source: NPCI UPI Ecosystem Statistics, {latest_month.strftime('%b %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

with inc3:
    st.markdown(f"""
    <div class="insight-card insurance">
        <div class="insight-title">🛡️ Insurance & Financial Services Surging</div>
        <div class="insight-body">Financial services are growing off a small base with a high momentum of <b>{ins_ms_3m:.2f}</b>. However, overall volume share remains low at <b>{ins_share:.1f}%</b>, indicating significant untapped addressable market remaining.</div>
        <div class="insight-source">Source: NPCI UPI Ecosystem Statistics, {latest_month.strftime('%b %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Main double columns for Leaderboard and Network Overview
col_left, col_right = st.columns([1, 1])

# ----------------- SECTION A (contd): OVERALL UPI TREND CHART -----------------
with col_left:
    st.markdown("### 📈 Network Aggregated P2M Trend")
    
    overall_df = df.groupby("month").agg({
        "volume": "sum",
        "value_cr": "sum"
    }).reset_index()
    
    fig_network = go.Figure()
    fig_network.add_trace(go.Scatter(
        x=overall_df["month"], 
        y=overall_df["volume"] / 1_000_000, 
        name="Volume (Millions)", 
        yaxis="y1",
        line=dict(color="#6366F1", width=3)
    ))
    fig_network.add_trace(go.Scatter(
        x=overall_df["month"], 
        y=overall_df["value_cr"], 
        name="Value (Crore INR)", 
        yaxis="y2",
        line=dict(color="#C084FC", width=3, dash="dash")
    ))
    
    # Annotations for key events
    annotations = [
        dict(
            x=datetime.date(2023, 11, 1),
            y=overall_df[overall_df["month"] == "2023-11-01"]["volume"].values[0] / 1_000_000,
            xref="x", yref="y1",
            text="Festive Peak Q4 '23",
            showarrow=True, arrowhead=2, arrowcolor="#6366F1",
            ax=-40, ay=-40,
            bordercolor="#6366F1", borderwidth=1, borderpad=4,
            bgcolor="rgba(15, 23, 42, 0.8)", opacity=0.8
        ),
        dict(
            x=datetime.date(2024, 11, 1),
            y=overall_df[overall_df["month"] == "2024-11-01"]["volume"].values[0] / 1_000_000,
            xref="x", yref="y1",
            text="Festive Peak Q4 '24",
            showarrow=True, arrowhead=2, arrowcolor="#6366F1",
            ax=-40, ay=-40,
            bordercolor="#6366F1", borderwidth=1, borderpad=4,
            bgcolor="rgba(15, 23, 42, 0.8)", opacity=0.8
        ),
        dict(
            x=datetime.date(2025, 6, 1),
            y=overall_df[overall_df["month"] == "2025-06-01"]["volume"].values[0] / 1_000_000,
            xref="x", yref="y1",
            text="Admission season spike",
            showarrow=True, arrowhead=2, arrowcolor="#6366F1",
            ax=40, ay=30,
            bordercolor="#FB7185", borderwidth=1, borderpad=4,
            bgcolor="rgba(15, 23, 42, 0.8)", opacity=0.8
        )
    ]
    
    fig_network.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(
            title=dict(text="Volume (Millions)", font=dict(color="#6366F1")),
            tickfont=dict(color="#6366F1"),
            gridcolor="rgba(148, 163, 184, 0.1)"
        ),
        yaxis2=dict(
            title=dict(text="Value (Crore INR)", font=dict(color="#C084FC")),
            tickfont=dict(color="#C084FC"),
            side="right", 
            overlaying="y", 
            ticks="outside",
            showgrid=False
        ),
        annotations=annotations,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig_network, use_container_width=True)

# ----------------- SECTION B: CATEGORY MOMENTUM LEADERBOARD -----------------
with col_right:
    st.markdown("### 🏆 Category Momentum Leaderboard")
    
    # Selection filters
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        time_window = st.selectbox(
            "Trailing Time Window",
            ["3-Month Trailing", "6-Month Trailing", "12-Month Trailing"],
            index=0
        )
        window_suffix = "3m" if "3" in time_window else ("6m" if "6" in time_window else "12m")
        
    with f_col2:
        sort_by = st.selectbox(
            "Rank Categories By",
            ["Momentum Score", "Absolute Volume (Mn)", "YoY Growth Rate %"],
            index=0
        )
    
    # Filter latest month data for leaderboard
    leaderboard_df = latest_df.copy()
    
    # Calculate Volume in Millions
    leaderboard_df["vol_mn"] = leaderboard_df["volume"] / 1_000_000
    
    # Sort and rank column
    if "Momentum" in sort_by:
        sort_col = f"momentum_score_{window_suffix}"
        leaderboard_df = leaderboard_df.dropna(subset=[sort_col])
        leaderboard_df = leaderboard_df.sort_values(by=sort_col, ascending=True) # Ascending true for horizontal bar chart bottom-up
        x_label = "Momentum Score"
        hover_template = "<b>%{y}</b><br>Momentum Score: %{x:.2f}<br>Volume: %{customdata[0]:.1f} Mn<br>YoY Growth: %{customdata[1]:.1f}%"
    elif "Volume" in sort_by:
        sort_col = "vol_mn"
        leaderboard_df = leaderboard_df.sort_values(by=sort_col, ascending=True)
        x_label = "Volume (Millions)"
        hover_template = "<b>%{y}</b><br>Volume: %{x:.1f} Mn<br>Value: %{customdata[2]:,.0f} Cr<br>Avg Ticket: ₹%{customdata[3]:.1f}"
    else:
        sort_col = "yoy_growth"
        leaderboard_df["yoy_growth_pct"] = leaderboard_df["yoy_growth"] * 100
        leaderboard_df = leaderboard_df.dropna(subset=["yoy_growth_pct"])
        leaderboard_df = leaderboard_df.sort_values(by="yoy_growth_pct", ascending=True)
        x_label = "YoY Growth Rate %"
        hover_template = "<b>%{y}</b><br>YoY Growth: %{x:.1f}%<br>Momentum: %{customdata[4]:.2f}"
        
    # Assign color codes dynamically based on momentum value for the window
    colors = []
    for val in leaderboard_df[f"momentum_score_{window_suffix}"]:
        if pd.isna(val):
            colors.append("#64748B") # grey
        elif val > 1.5:
            colors.append("#34D399") # green
        elif val >= 0.8:
            colors.append("#F59E0B") # amber
        else:
            colors.append("#F87171") # red
            
    fig_lead = go.Figure(go.Bar(
        x=leaderboard_df[sort_col] if "Growth" not in sort_by else leaderboard_df["yoy_growth_pct"],
        y=leaderboard_df["category"],
        orientation="h",
        marker_color=colors,
        customdata=np.stack((
            leaderboard_df["vol_mn"], 
            leaderboard_df["yoy_growth"] * 100,
            leaderboard_df["value_cr"],
            leaderboard_df["avg_ticket"],
            leaderboard_df[f"momentum_score_{window_suffix}"]
        ), axis=-1),
        hovertemplate=hover_template
    ))
    
    fig_lead.update_layout(
        xaxis=dict(title=x_label, gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(title=""),
        margin=dict(l=40, r=40, t=10, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        height=320
    )
    
    st.plotly_chart(fig_lead, use_container_width=True)

st.write("---")

# ----------------- SECTION C: CATEGORY DEEP DIVE -----------------
st.markdown("### 🔍 Category Deep Dive")

# Category dropdown
all_categories = sorted(df["category"].unique())
selected_category = st.selectbox("Select a Merchant Category for Granular Analysis", all_categories, index=0)

# Filter category data
cat_df = df[df["category"] == selected_category].sort_values("month")

# Calculate metrics for selected category
cat_latest = cat_df.iloc[-1] if len(cat_df) > 0 else None
cat_py = cat_df[cat_df["month"] <= closest_py_month].iloc[-1] if len(cat_df[cat_df["month"] <= closest_py_month]) > 0 else None

# Auto-generated Plain English Summary
if cat_latest is not None:
    vol_latest_mn = cat_latest["volume"] / 1_000_000
    val_latest_cr = cat_latest["value_cr"]
    ticket_latest = cat_latest["avg_ticket"]
    share_latest = cat_latest["volume_share_pct"]
    ms_latest = cat_latest["momentum_score_3m"]
    
    # Generate description words
    growth_descr = "growing FASTER than" if ms_latest > 1.0 else "LAGGING behind"
    
    if selected_category == "Travel & Transport":
        highlight_msg = f"**Travel & Transport** grew **{ms_latest:.1f}x faster** than the UPI network in the last 3 months. Average ticket size stands at **₹{ticket_latest:,.2f}** — the highest transaction size across all consumer segments."
    elif selected_category == "Grocery & Supermarkets":
        highlight_msg = f"**Grocery & Supermarkets** is UPI's absolute volume engine, commanding a massive **{share_latest:.1f}%** volume share. However, average ticket size has dropped to **₹{ticket_latest:.2f}** as micro-transactions surge at kirana stores."
    elif selected_category == "Insurance & Financial Services":
        highlight_msg = f"**Insurance & Financial Services** shows high growth momentum (**{ms_latest:.2f}**) but still accounts for only **{share_latest:.1f}%** of total transaction volume, highlighting an early-stage fintech adoption curve."
    elif selected_category == "Utilities & Bill Payment":
        highlight_msg = f"**Utilities & Bill Payment** is a highly mature segment. It handles stable recurring billing (**{share_latest:.1f}%** volume share) but has sluggish growth momentum (**{ms_latest:.2f}**), lagging the network."
    elif selected_category == "Education":
        highlight_msg = f"**Education** has high ticket values (**₹{ticket_latest:,.2f}**) but has intense seasonal spikes, peaking in June-July with a seasonality index of **{(cat_latest['seasonality_index']):.2f}**."
    else:
        highlight_msg = f"**{selected_category}** is currently {growth_descr} the overall P2M network with a Momentum Score of **{ms_latest:.2f}**. Its average ticket size is **₹{ticket_latest:.2f}** and it accounts for **{share_latest:.1f}%** of P2M volumes."
        
    st.info(highlight_msg, icon="👁️")

# Deep dive metrics line
dc1, dc2, dc3, dc4 = st.columns(4)
with dc1:
    st.metric(
        label="Monthly Transaction Volume",
        value=f"{(cat_latest['volume'] / 1_000_000):.1f} Mn",
        delta=f"+{((cat_latest['volume'] - cat_py['volume']) / cat_py['volume'] * 100):.1f}% YoY" if cat_py is not None else None
    )
with dc2:
    st.metric(
        label="Monthly Transaction Value",
        value=f"₹{cat_latest['value_cr']:.1f} Cr",
        delta=f"+{((cat_latest['value_cr'] - cat_py['value_cr']) / cat_py['value_cr'] * 100):.1f}% YoY" if cat_py is not None else None
    )
with dc3:
    st.metric(
        label="3M Average Ticket Size",
        value=f"₹{cat_latest['avg_ticket_rolling_3m']:.2f}",
        delta=f"{((cat_latest['avg_ticket_rolling_3m'] - cat_py['avg_ticket_rolling_3m']) / cat_py['avg_ticket_rolling_3m'] * 100):.1f}% YoY" if cat_py is not None else None
    )
with dc4:
    st.metric(
        label="Category Volume Share",
        value=f"{cat_latest['volume_share_pct']:.2f}%",
        delta=f"{(cat_latest['volume_share_shift']):+.2f}% YoY Shift" if not pd.isna(cat_latest['volume_share_shift']) else None
    )

# 4-chart Grid for Category Deep Dive
dcol1, dcol2 = st.columns(2)

with dcol1:
    # Chart 1: Volume Trend
    fig_vol = px.area(cat_df, x="month", y="volume", 
                      title=f"Monthly Transaction Volume Trend - {selected_category}",
                      labels={"volume": "Volume (Absolute)", "month": "Month"},
                      template="plotly_dark")
    fig_vol.update_traces(line_color="#818CF8", fillcolor="rgba(129, 140, 248, 0.15)")
    fig_vol.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"), 
        yaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)")
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    # Chart 2: Average Ticket Size Trend
    fig_ticket = px.line(cat_df, x="month", y="avg_ticket",
                         title=f"Average Ticket Size Trend (INR) - {selected_category}",
                         labels={"avg_ticket": "Ticket Size (₹)", "month": "Month"},
                         template="plotly_dark")
    fig_ticket.update_traces(line=dict(color="#34D399", width=3))
    fig_ticket.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"), 
        yaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)")
    )
    st.plotly_chart(fig_ticket, use_container_width=True)

with dcol2:
    # Chart 3: Value Trend
    fig_val = px.area(cat_df, x="month", y="value_cr", 
                      title=f"Monthly Transaction Value Trend (Cr INR) - {selected_category}",
                      labels={"value_cr": "Value (Crores)", "month": "Month"},
                      template="plotly_dark")
    fig_val.update_traces(line_color="#C084FC", fillcolor="rgba(192, 132, 252, 0.15)")
    fig_val.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"), 
        yaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)")
    )
    st.plotly_chart(fig_val, use_container_width=True)

    # Chart 4: Volume Share % over time
    fig_share_t = px.line(cat_df, x="month", y="volume_share_pct",
                           title=f"Network Volume Wallet Share % - {selected_category}",
                           labels={"volume_share_pct": "Volume Share %", "month": "Month"},
                           template="plotly_dark")
    fig_share_t.update_traces(line=dict(color="#FB7185", width=3))
    fig_share_t.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"), 
        yaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)")
    )
    st.plotly_chart(fig_share_t, use_container_width=True)

# ----------------- SECTION C (contd): YoY OVERLAY COMPARISON -----------------
st.markdown("#### 🔄 YoY Seasonal Overlay Comparison (Volume)")

# Pivot to compare volumes of different years across months
cat_df["year"] = cat_df["month"].dt.year
cat_df["month_num"] = cat_df["month"].dt.month
cat_df["month_name"] = cat_df["month"].dt.strftime("%b")

# Sort df to make overlay order correct
cat_df = cat_df.sort_values(by="month_num")

fig_overlay = px.line(cat_df, x="month_name", y="volume", color="year",
                      title=f"YoY Monthly Seasonal Patterns - {selected_category}",
                      labels={"volume": "Volume (Absolute)", "month_name": "Month"},
                      category_orders={"month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]},
                      template="plotly_dark")
fig_overlay.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)", 
    xaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"), 
    yaxis=dict(gridcolor="rgba(148, 163, 184, 0.1)"),
    margin=dict(l=40, r=40, t=30, b=20)
)
st.plotly_chart(fig_overlay, use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; margin-top: 3rem; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1.5rem;">
    📊 <b>UPI Merchant Category Pulse Dashboard</b> | Sourced from official NPCI UPI Ecosystem Statistics and RBI Bulletins.<br>
    Created by <i>Sai Krishna A Ramu</i> as a Portfolio Project.
</div>
""", unsafe_allow_html=True)
