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

# Custom CSS for Premium SaaS Aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Overrides */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F1F5F9;
    }
    
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }
    
    h1, h2, h3, .title-style {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Premium Title Section */
    .title-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.45), rgba(15, 23, 42, 0.55));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .title-left {
        flex: 1;
        min-width: 300px;
    }
    
    .gradient-title {
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.03em;
    }
    
    .subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        font-weight: 400;
        line-height: 1.4;
    }
    
    /* Live Status Badge */
    .status-badge {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #34D399;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.05);
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.6s infinite;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        70% {
            transform: scale(1);
            box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
        }
        100% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.65) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: transparent;
        transition: background 0.3s ease;
    }
    
    .glass-card.vol-card::before { background: #6366F1; }
    .glass-card.growth-card::before { background: #10B981; }
    .glass-card.ticket-card::before { background: #A855F7; }
    .glass-card.categories-card::before { background: #FB7185; }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 255, 255, 0.12);
        box-shadow: 0 20px 40px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* KPI Metrics Styling */
    .kpi-label {
        color: #94A3B8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-value {
        color: #F8FAFC;
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        margin: 0.4rem 0;
        letter-spacing: -0.02em;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .delta-up {
        color: #34D399;
    }
    
    .delta-down {
        color: #F87171;
    }
    
    /* Insight Cards Section */
    .insight-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.45) 0%, rgba(15, 23, 42, 0.55) 100%);
        border-left: 4px solid #6366F1;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        border-right: 1px solid rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .insight-card:hover {
        transform: scale(1.01);
        border-right-color: rgba(255, 255, 255, 0.08);
    }
    
    .insight-card.travel { border-left-color: #818CF8; }
    .insight-card.grocery { border-left-color: #34D399; }
    .insight-card.insurance { border-left-color: #C084FC; }
    .insight-card.education { border-left-color: #FB7185; }
    .insight-card.utilities { border-left-color: #F59E0B; }
    
    .insight-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: #F8FAFC;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    .insight-body {
        color: #CBD5E1;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .insight-source {
        color: #64748B;
        font-size: 0.75rem;
        margin-top: 0.6rem;
        font-style: italic;
    }
    
    /* Custom Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: transparent !important;
        border: none !important;
        color: #94A3B8 !important;
        font-family: 'Outfit', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        padding: 0 8px;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #818CF8 !important;
        font-weight: 600;
    }
    
    /* Custom Intelligence Banner */
    .insight-banner {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(192, 132, 252, 0.04) 100%);
        border: 1px solid rgba(99, 102, 241, 0.16);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(8px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.05);
    }
    
    .banner-icon {
        font-size: 1.6rem;
        line-height: 1;
        margin-top: 0.1rem;
    }
    
    .banner-content {
        flex: 1;
    }
    
    .banner-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        color: #818CF8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }
    
    .banner-body {
        color: #E2E8F0;
        font-size: 1rem;
        line-height: 1.55;
    }
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

# ----------------- SIDEBAR (METRIC INDEX & METHODOLOGY) -----------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0; text-align: center;">
        <span style="font-size: 2.5rem;">⚡</span>
        <h2 style="font-family: 'Outfit', sans-serif; font-weight: 700; color: #F8FAFC; margin-top: 0.5rem; margin-bottom: 0;">UPI Pulse</h2>
        <span style="color: #64748B; font-size: 0.85rem;">NPCI Merchant Category Analytics</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown(f"""
    ### 📂 Dataset Profile
    - **Data Span:** Jan 2022 – {latest_month.strftime('%b %Y')}
    - **Frequency:** Monthly aggregates
    - **Cleaned Files:** 52 monthly reports
    - **Coverage:** {active_categories} standard merchant segments
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### ⚙️ Momentum Score
    Measures category-specific growth velocity relative to the total UPI network growth rate:
    
    $$\\text{Velocity Score} = \\frac{\\Delta \\text{ Category Vol }}{\\Delta \\text{ Network Vol }}$$
    
    - **Score > 1.0:** Growing faster than the network (Outperforming)
    - **Score = 1.0:** Parity with overall growth rate
    - **Score < 1.0:** Lagging overall network velocity
    
    ### 👤 Publisher
    *Sai Krishna A Ramu*  
    *Portfolio Project*
    """, unsafe_allow_html=True)

# ----------------- PREMIUM HEADER BLOCK -----------------
st.markdown(f"""
<div class="title-container">
    <div class="title-left">
        <h1 class="gradient-title">UPI Merchant Category Pulse</h1>
        <div class="subtitle">Surfacing micro-consumer trends and category growth dynamics across India's payment ecosystem</div>
    </div>
    <div class="status-badge">
        <span class="pulse-dot"></span>
        <span>LIVE UPDATES: {latest_month.strftime('%B %Y')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- SECTION A: MARKET OVERVIEW (KPI CARDS) -----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card vol-card">
        <div class="kpi-label">Latest Month Volume</div>
        <div class="kpi-value">{(total_vol_latest / 1_000_000_000):.2f} B</div>
        <div class="kpi-delta delta-up">⚡ P2M Txns</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card growth-card">
        <div class="kpi-label">Network YoY Volume Growth</div>
        <div class="kpi-value">+{global_yoy_vol_growth:.1f}%</div>
        <div class="kpi-delta delta-up">▲ vs. Prior Year</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card ticket-card">
        <div class="kpi-label">Network Average Ticket</div>
        <div class="kpi-value">₹{global_avg_ticket:.2f}</div>
        <div class="kpi-delta {'delta-up' if global_avg_ticket_delta >= 0 else 'delta-down'}">
            {'▲' if global_avg_ticket_delta >= 0 else '▼'} {abs(global_avg_ticket_delta):.1f}% YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card categories-card">
        <div class="kpi-label">Active Categories</div>
        <div class="kpi-value">{active_categories}</div>
        <div class="kpi-delta delta-up">● Standardized MCCs</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- PLOTLY BEAUTIFICATION HELPER -----------------
def style_plotly_fig(fig):
    fig.update_layout(
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#F8FAFC"),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="rgba(255,255,255,0.1)",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#F8FAFC")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.05)",
        linecolor="rgba(255, 255, 255, 0.1)",
        tickfont=dict(color="#94A3B8"),
        titlefont=dict(color="#F8FAFC")
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.05)",
        linecolor="rgba(255, 255, 255, 0.1)",
        tickfont=dict(color="#94A3B8"),
        titlefont=dict(color="#F8FAFC")
    )
    return fig

# ----------------- DASHBOARD TABS -----------------
tab_overview, tab_leaderboard, tab_deepdive = st.tabs([
    "📊 Network Overview & Insights", 
    "🏆 Momentum Leaderboard", 
    "🔍 Category Deep Dive"
])

# ----------------- TAB 1: OVERVIEW & INSIGHT CARDS -----------------
with tab_overview:
    col_left, col_right = st.columns([13, 11])
    
    with col_left:
        st.markdown("### 📈 Aggregated P2M Ecosystem Trend")
        
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
            line=dict(color="#818CF8", width=3.5)
        ))
        fig_network.add_trace(go.Scatter(
            x=overall_df["month"], 
            y=overall_df["value_cr"], 
            name="Value (Crore INR)", 
            yaxis="y2",
            line=dict(color="#C084FC", width=3, dash="dash")
        ))
        
        annotations = [
            dict(
                x=datetime.date(2023, 11, 1),
                y=overall_df[overall_df["month"] == "2023-11-01"]["volume"].values[0] / 1_000_000,
                xref="x", yref="y1",
                text="Festive Peak Q4 '23",
                showarrow=True, arrowhead=2, arrowcolor="#818CF8",
                ax=-40, ay=-40,
                bordercolor="#818CF8", borderwidth=1, borderpad=4,
                bgcolor="rgba(15, 23, 42, 0.85)", opacity=0.9
            ),
            dict(
                x=datetime.date(2024, 11, 1),
                y=overall_df[overall_df["month"] == "2024-11-01"]["volume"].values[0] / 1_000_000,
                xref="x", yref="y1",
                text="Festive Peak Q4 '24",
                showarrow=True, arrowhead=2, arrowcolor="#818CF8",
                ax=-40, ay=-40,
                bordercolor="#818CF8", borderwidth=1, borderpad=4,
                bgcolor="rgba(15, 23, 42, 0.85)", opacity=0.9
            ),
            dict(
                x=datetime.date(2025, 6, 1),
                y=overall_df[overall_df["month"] == "2025-06-01"]["volume"].values[0] / 1_000_000,
                xref="x", yref="y1",
                text="Admission season spike",
                showarrow=True, arrowhead=2, arrowcolor="#FB7185",
                ax=40, ay=30,
                bordercolor="#FB7185", borderwidth=1, borderpad=4,
                bgcolor="rgba(15, 23, 42, 0.85)", opacity=0.9
            )
        ]
        
        fig_network.update_layout(
            xaxis=dict(title=""),
            yaxis=dict(
                title=dict(text="Volume (Millions)", font=dict(color="#818CF8")),
                tickfont=dict(color="#818CF8"),
                gridcolor="rgba(255, 255, 255, 0.05)"
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
            template="plotly_dark"
        )
        style_plotly_fig(fig_network)
        st.plotly_chart(fig_network, use_container_width=True)
        
    with col_right:
        st.markdown("### 💡 Key Spending Insights")
        
        # Calculate specific metrics for insights dynamically
        travel_latest = latest_df[latest_df["category"] == "Travel & Transport"]
        travel_ms_3m = travel_latest["momentum_score_3m"].values[0] if not travel_latest.empty else 2.41
        travel_avg_ticket = travel_latest["avg_ticket"].values[0] if not travel_latest.empty else 3200

        grocery_history = df[df["category"] == "Grocery & Supermarkets"].sort_values("month")
        grocery_ticket_start = grocery_history["avg_ticket"].iloc[0] if len(grocery_history) > 0 else 800
        grocery_ticket_end = grocery_history["avg_ticket"].iloc[-1] if len(grocery_history) > 0 else 580
        grocery_ticket_drop_pct = (grocery_ticket_start - grocery_ticket_end) / grocery_ticket_start * 100

        insurance_latest = latest_df[latest_df["category"] == "Insurance & Financial Services"]
        ins_ms_3m = insurance_latest["momentum_score_3m"].values[0] if not insurance_latest.empty else 1.85
        ins_share = insurance_latest["volume_share_pct"].values[0] if not insurance_latest.empty else 1.5

        edu_history = df[df["category"] == "Education"]
        edu_peak_index = edu_history[edu_history["month"].dt.month.isin([5, 6, 7])]["seasonality_index"].mean() if len(edu_history) > 0 else 1.45

        util_latest = latest_df[latest_df["category"] == "Utilities & Bill Payment"]
        util_ms_3m = util_latest["momentum_score_3m"].values[0] if not util_latest.empty else 0.85
        util_share = util_latest["volume_share_pct"].values[0] if not util_latest.empty else 8.5

        st.markdown(f"""
        <div class="insight-card travel">
            <div class="insight-title">✈️ Travel Outpacing Overall Network</div>
            <div class="insight-body">Travel & hospitality spending is the core growth engine, growing <b>{travel_ms_3m:.1f}x faster</b> than the overall P2M network. It also boasts the highest transaction size (<b>₹{travel_avg_ticket:,.0f}</b>) among all tracked categories.</div>
            <div class="insight-source">Source: NPCI UPI Ecosystem Statistics, {latest_month.strftime('%b %Y')}</div>
        </div>
        
        <div class="insight-card grocery">
            <div class="insight-title">🛒 Grocery Commoditization (Micro-Tickets)</div>
            <div class="insight-body">Grocery represents the highest overall volume share, but its average ticket size has dropped <b>{grocery_ticket_drop_pct:.0f}%</b> (from ₹{grocery_ticket_start:.0f} to ₹{grocery_ticket_end:.0f}), signaling extensive penetration of small basket values into local kiranas.</div>
            <div class="insight-source">Source: NPCI UPI Statistics</div>
        </div>
        
        <div class="insight-card insurance">
            <div class="insight-title">🛡️ Insurance & Financial Services Surging</div>
            <div class="insight-body">Financial services are growing off a small base with a high momentum of <b>{ins_ms_3m:.2f}</b>. However, overall volume share remains low at <b>{ins_share:.1f}%</b>, indicating significant untapped addressable market remaining.</div>
            <div class="insight-source">Source: NPCI UPI Statistics, {latest_month.strftime('%b %Y')}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 2: LEADERBOARD -----------------
with tab_leaderboard:
    st.markdown("### 🏆 Category Velocity Leaderboard")
    
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
    leaderboard_df["vol_mn"] = leaderboard_df["volume"] / 1_000_000
    
    if "Momentum" in sort_by:
        sort_col = f"momentum_score_{window_suffix}"
        leaderboard_df = leaderboard_df.dropna(subset=[sort_col])
        leaderboard_df = leaderboard_df.sort_values(by=sort_col, ascending=True)
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
        
    colors = []
    for val in leaderboard_df[f"momentum_score_{window_suffix}"]:
        if pd.isna(val):
            colors.append("#64748B")
        elif val > 1.5:
            colors.append("#10B981") # emerald
        elif val >= 0.8:
            colors.append("#F59E0B") # amber
        else:
            colors.append("#EF4444") # red
            
    fig_lead = go.Figure(go.Bar(
        x=leaderboard_df[sort_col] if "Growth" not in sort_by else leaderboard_df["yoy_growth_pct"],
        y=leaderboard_df["category"],
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.05)", width=1)),
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
        xaxis=dict(title=x_label),
        yaxis=dict(title=""),
        margin=dict(l=40, r=40, t=10, b=20),
        barcornerradius=6,
        template="plotly_dark",
        height=450
    )
    style_plotly_fig(fig_lead)
    st.plotly_chart(fig_lead, use_container_width=True)

# ----------------- TAB 3: CATEGORY DEEP DIVE -----------------
with tab_deepdive:
    st.markdown("### 🔍 Merchant Category Deep Dive")
    
    all_categories = sorted(df["category"].unique())
    selected_category = st.selectbox("Select a Merchant Category for Granular Analysis", all_categories, index=0)
    
    cat_df = df[df["category"] == selected_category].sort_values("month")
    cat_latest = cat_df.iloc[-1] if len(cat_df) > 0 else None
    cat_py = cat_df[cat_df["month"] <= closest_py_month].iloc[-1] if len(cat_df[cat_df["month"] <= closest_py_month]) > 0 else None
    
    if cat_latest is not None:
        vol_latest_mn = cat_latest["volume"] / 1_000_000
        val_latest_cr = cat_latest["value_cr"]
        ticket_latest = cat_latest["avg_ticket"]
        share_latest = cat_latest["volume_share_pct"]
        ms_latest = cat_latest["momentum_score_3m"]
        
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
            
        st.markdown(f"""
        <div class="insight-banner">
            <div class="banner-icon">💡</div>
            <div class="banner-content">
                <div class="banner-title">Category Intelligence Summary</div>
                <div class="banner-body">{highlight_msg}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
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
        
    st.write("")
    
    # 4-chart Grid for Category Deep Dive
    dcol1, dcol2 = st.columns(2)
    
    with dcol1:
        # Chart 1: Volume Trend
        fig_vol = px.area(cat_df, x="month", y="volume", 
                          title=f"Monthly Transaction Volume Trend - {selected_category}",
                          labels={"volume": "Volume (Absolute)", "month": "Month"},
                          template="plotly_dark")
        fig_vol.update_traces(line_color="#818CF8", fillcolor="rgba(129, 140, 248, 0.15)", line_width=2.5)
        fig_vol.update_layout(
            margin=dict(l=40, r=40, t=40, b=20)
        )
        style_plotly_fig(fig_vol)
        st.plotly_chart(fig_vol, use_container_width=True)
    
        # Chart 2: Average Ticket Size Trend
        fig_ticket = px.line(cat_df, x="month", y="avg_ticket",
                             title=f"Average Ticket Size Trend (INR) - {selected_category}",
                             labels={"avg_ticket": "Ticket Size (₹)", "month": "Month"},
                             template="plotly_dark")
        fig_ticket.update_traces(line=dict(color="#10B981", width=3))
        fig_ticket.update_layout(
            margin=dict(l=40, r=40, t=40, b=20)
        )
        style_plotly_fig(fig_ticket)
        st.plotly_chart(fig_ticket, use_container_width=True)
    
    with dcol2:
        # Chart 3: Value Trend
        fig_val = px.area(cat_df, x="month", y="value_cr", 
                          title=f"Monthly Transaction Value Trend (Cr INR) - {selected_category}",
                          labels={"value_cr": "Value (Crores)", "month": "Month"},
                          template="plotly_dark")
        fig_val.update_traces(line_color="#C084FC", fillcolor="rgba(192, 132, 252, 0.15)", line_width=2.5)
        fig_val.update_layout(
            margin=dict(l=40, r=40, t=40, b=20)
        )
        style_plotly_fig(fig_val)
        st.plotly_chart(fig_val, use_container_width=True)
    
        # Chart 4: Volume Share % over time
        fig_share_t = px.line(cat_df, x="month", y="volume_share_pct",
                               title=f"Network Volume Wallet Share % - {selected_category}",
                               labels={"volume_share_pct": "Volume Share %", "month": "Month"},
                               template="plotly_dark")
        fig_share_t.update_traces(line=dict(color="#FB7185", width=3))
        fig_share_t.update_layout(
            margin=dict(l=40, r=40, t=40, b=20)
        )
        style_plotly_fig(fig_share_t)
        st.plotly_chart(fig_share_t, use_container_width=True)
        
    st.write("")
    
    # 🔄 YoY Seasonal Overlay Comparison
    cat_df["year"] = cat_df["month"].dt.year
    cat_df["month_num"] = cat_df["month"].dt.month
    cat_df["month_name"] = cat_df["month"].dt.strftime("%b")
    cat_df = cat_df.sort_values(by="month_num")
    
    fig_overlay = px.line(cat_df, x="month_name", y="volume", color="year",
                          title=f"YoY Monthly Seasonal Patterns - {selected_category}",
                          labels={"volume": "Volume (Absolute)", "month_name": "Month"},
                          category_orders={"month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]},
                          template="plotly_dark")
    fig_overlay.update_layout(
        margin=dict(l=40, r=40, t=40, b=20)
    )
    style_plotly_fig(fig_overlay)
    st.plotly_chart(fig_overlay, use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; margin-top: 3.5rem; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1.5rem;">
    📊 <b>UPI Merchant Category Pulse Dashboard</b> | Sourced from official NPCI UPI Ecosystem Statistics.<br>
    Created by <i>Sai Krishna A Ramu</i> as a Portfolio Project.
</div>
""", unsafe_allow_html=True)
