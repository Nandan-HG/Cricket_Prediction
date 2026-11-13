
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IPL Eye-In Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. LOAD DATASETS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"


@st.cache_data
def load_data():

    ball = pd.read_csv(DATA_DIR / "ball_metrics.csv")
    phase = pd.read_csv(DATA_DIR / "phase_metrics.csv")
    bootstrap = pd.read_csv(DATA_DIR / "bootstrap_results.csv")

    return ball, phase, bootstrap


try:
    ball, phase, bootstrap = load_data()

except Exception as e:
    st.error(f"Unable to load project data: {e}")
    st.stop()


# =========================================================
# 3. CUSTOM CSS DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background-color: #111C2E;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 700;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17263B, #1D3048);
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #2B425E;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

[data-testid="stMetricValue"] {
    color: #2DD4BF !important;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #B8C7D9 !important;
}

hr {
    border-color: #2B3C52;
}

[data-testid="stSidebar"] p {
    color: #DCE6F1;
}

.stButton button {
    border-radius: 8px;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. CHART THEME HELPER
# =========================================================

def style_chart(fig, height=420):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#111C2E",
        font=dict(
            color="#E2E8F0",
            size=12
        ),
        title_font_size=19,
        height=height,
        margin=dict(
            l=25,
            r=25,
            t=60,
            b=35
        ),
        hoverlabel=dict(
            bgcolor="#17263B",
            font_color="white"
        )
    )

    return fig


# =========================================================
# 5. SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown("""
<h1 style="font-size:27px;color:white;">
🏏 IPL EYE-IN
</h1>
<p style="color:#94A3B8;">
Cricket Analytics Dashboard
</p>
""", unsafe_allow_html=True)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Eye-In Rankings",
        "Player Deep Dive",
        "Player Comparison",
        "Dismissal Analysis",
        "Phase Analysis"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("""
<p style="font-size:13px;color:#94A3B8;">
PROJECT INFORMATION
</p>
<p style="color:#CBD5E1;">
IPL Ball-by-Ball Analysis
</p>
<p style="color:#94A3B8;font-size:12px;">
Historical Cricket Analytics
</p>
""", unsafe_allow_html=True)


# =========================================================
# 6. PROFESSIONAL DASHBOARD HEADER
# =========================================================

st.markdown("""
<style>
.dashboard-header {
    background: linear-gradient(120deg, #14263F, #155E63);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #31566A;
    margin-bottom: 25px;
}
.dashboard-header h1 {
    color: white;
    font-size: 38px;
    margin: 0 0 8px 0;
}
.dashboard-header h3 {
    color: #99F6E4;
    font-size: 21px;
    font-weight: 500;
    margin: 0 0 10px 0;
}
.dashboard-header p {
    color: #D5E5F0;
    font-size: 15px;
    margin: 0;
}
</style>
<div class="dashboard-header"><h1>🏏 IPL EYE-IN</h1><h3>How Many Balls Until a Batter Gets Set?</h3><p>Exploring batting performance, scoring patterns and dismissal frequency using IPL data.</p></div>
""", unsafe_allow_html=True)


# =========================================================
# 7. OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.header("📊 Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Raw Deliveries", "295,732")
    col2.metric("Faced Ball Records", "285,856")
    col3.metric("Batter Innings", "18,837")
    col4.metric("Dismissals", "14,084")

    st.divider()

    left, right = st.columns(2)

    # TOP EYE-IN IMPROVEMENTS

    with left:

        st.subheader("🏆 Top Eye-In Improvements")

        top = bootstrap.nlargest(
            10, "improvement"
        ).sort_values("improvement")

        fig = px.bar(
            top,
            x="improvement",
            y="batter",
            orientation="h",
            color="improvement",
            color_continuous_scale="Teal",
            labels={
                "improvement": "Improvement (SR points)",
                "batter": "Batter"
            }
        )

        fig.update_traces(
            hovertemplate=(
                "Batter: %{y}<br>"
                "Improvement: %{x:.2f}"
                "<extra></extra>"
            )
        )

        style_chart(fig, 450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # DISMISSAL FREQUENCY

    with right:

        st.subheader("⚡ Dismissal Frequency")

        ball_view = ball[ball["enough_data"]]

        fig = px.line(
            ball_view,
            x="ball_faced_number",
            y="dismissal_rate_pct",
            markers=True,
            labels={
                "ball_faced_number": "Ball Faced",
                "dismissal_rate_pct": "Dismissal Frequency (%)"
            }
        )

        fig.update_traces(
            line_color="#F59E0B",
            marker_color="#F59E0B",
            line_width=3
        )

        style_chart(fig, 450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("Understanding Eye-In Improvement")

    st.markdown("""
    Eye-In Improvement compares a batter's strike rate
    during two periods:

    - **Early period:** First 10 balls.
    - **Excluded period:** Balls 11–20.
    - **Later period:** Ball 21 onwards.

    **Formula:**

    Later-period Strike Rate − First-10-ball Strike Rate
    """)

    st.info(
        "A positive value indicates that the batter's "
        "scoring rate increased between the two periods."
    )


# =========================================================
# 8. EYE-IN RANKINGS PAGE
# =========================================================

elif page == "Eye-In Rankings":

    st.header("🏆 Eye-In Improvement Rankings")

    st.write(
        "Explore batters based on their improvement "
        "in scoring rate."
    )

    ranked = bootstrap.sort_values(
        "improvement",
        ascending=False
    )

    st.subheader("Batter Rankings")

    ranking_table = ranked[
        [
            "batter",
            "first_10_strike_rate",
            "after_20_strike_rate",
            "improvement",
            "first_period_innings",
            "later_period_innings"
        ]
    ].copy()

    ranking_table.columns = [
        "Batter",
        "First 10 Balls SR",
        "After 20 Balls SR",
        "Eye-In Improvement",
        "First-Period Innings",
        "Later-Period Innings"
    ]

    st.dataframe(
        ranking_table.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Player Improvement Chart")

    fig = px.bar(
        ranked.sort_values("improvement"),
        x="improvement",
        y="batter",
        orientation="h",
        color="improvement",
        color_continuous_scale="Teal",
        labels={
            "improvement": "Improvement (SR points)",
            "batter": "Batter"
        }
    )

    style_chart(fig, 450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# 9. PLAYER DEEP DIVE PAGE
# =========================================================

elif page == "Player Deep Dive":

    st.header("🏏 Player Deep Dive")

    st.write(
        "Explore individual batter performance "
        "and understand their Eye-In Improvement."
    )

    st.divider()

    players = sorted(
        bootstrap["batter"].dropna().unique()
    )

    selected_player = st.selectbox(
        "Select a Batter",
        players
    )

    player = bootstrap[
        bootstrap["batter"] == selected_player
    ].iloc[0]

    st.subheader("Player Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "First 10 Balls Strike Rate",
        f"{player['first_10_strike_rate']:.2f}"
    )

    col2.metric(
        "After 20 Balls Strike Rate",
        f"{player['after_20_strike_rate']:.2f}"
    )

    col3.metric(
        "Eye-In Improvement",
        f"{player['improvement']:+.2f}"
    )

    st.divider()

    # STRIKE RATE COMPARISON

    st.subheader("📈 Strike Rate Comparison")

    comparison = pd.DataFrame({
        "Period": [
            "First 10 Balls",
            "After 20 Balls"
        ],
        "Strike Rate": [
            player["first_10_strike_rate"],
            player["after_20_strike_rate"]
        ]
    })

    fig = px.bar(
        comparison,
        x="Period",
        y="Strike Rate",
        color="Period",
        text_auto=".2f",
        color_discrete_sequence=[
            "#3B82F6",
            "#2DD4BF"
        ],
        title=f"{selected_player} - Strike Rate Comparison"
    )

    fig.update_layout(showlegend=False)

    style_chart(fig, 380)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # CONFIDENCE INTERVAL

    st.subheader("📊 95% Bootstrap Confidence Interval")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[
                player["ci_lower"],
                player["ci_upper"]
            ],
            y=[
                selected_player,
                selected_player
            ],
            mode="lines",
            line=dict(
                color="#2DD4BF",
                width=8
            ),
            name="95% Confidence Interval"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[player["improvement"]],
            y=[selected_player],
            mode="markers",
            marker=dict(
                color="#F59E0B",
                size=15
            ),
            name="Estimated Improvement"
        )
    )

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="#EF4444"
    )

    fig.update_layout(
        xaxis_title="Eye-In Improvement (SR points)",
        yaxis_title="",
        height=330
    )

    style_chart(fig, 330)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        f"{selected_player}'s estimated Eye-In Improvement "
        f"is {player['improvement']:.2f} strike-rate points. "
        f"The 95% bootstrap confidence interval ranges from "
        f"{player['ci_lower']:.2f} to "
        f"{player['ci_upper']:.2f}."
    )

    st.caption(
        "The early and later contributing innings were "
        "independently resampled in the bootstrap implementation."
    )

    st.divider()

    st.subheader("Data Used")

    col1, col2 = st.columns(2)

    col1.metric(
        "First-Period Innings",
        int(player["first_period_innings"])
    )

    col2.metric(
        "Later-Period Innings",
        int(player["later_period_innings"])
    )


# =========================================================
# 10. PLAYER COMPARISON PAGE
# =========================================================

elif page == "Player Comparison":

    st.header("⚔️ Batter vs Batter Comparison")

    st.write(
        "Compare two batters based on early scoring rate, "
        "later scoring rate and Eye-In Improvement."
    )

    st.divider()

    players = sorted(
        bootstrap["batter"].dropna().unique()
    )

    if len(players) < 2:

        st.warning(
            "At least two batters are needed for comparison."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            player1_name = st.selectbox(
                "Select First Batter",
                players,
                key="comparison_player1"
            )

        other_players = [
            p for p in players if p != player1_name
        ]

        with col2:

            player2_name = st.selectbox(
                "Select Second Batter",
                other_players,
                key="comparison_player2"
            )

        player1 = bootstrap[
            bootstrap["batter"] == player1_name
        ].iloc[0]

        player2 = bootstrap[
            bootstrap["batter"] == player2_name
        ].iloc[0]

        st.divider()

        # PERFORMANCE METRICS

        st.subheader("Performance Comparison")

        comparison_metrics = [
            ("First 10 Balls SR", "first_10_strike_rate"),
            ("After 20 Balls SR", "after_20_strike_rate"),
            ("Eye-In Improvement", "improvement")
        ]

        for label, column in comparison_metrics:

            st.markdown(f"### {label}")

            c1, c2 = st.columns(2)

            c1.metric(
                player1_name,
                f"{player1[column]:.2f}"
            )

            c2.metric(
                player2_name,
                f"{player2[column]:.2f}",
                delta=f"{player2[column] - player1[column]:+.2f}"
            )

        st.divider()

        # STRIKE RATE COMPARISON

        st.subheader("Strike Rate Comparison")

        chart_data = pd.DataFrame({
            "Batter": [
                player1_name,
                player1_name,
                player2_name,
                player2_name
            ],
            "Period": [
                "First 10 Balls",
                "After 20 Balls",
                "First 10 Balls",
                "After 20 Balls"
            ],
            "Strike Rate": [
                player1["first_10_strike_rate"],
                player1["after_20_strike_rate"],
                player2["first_10_strike_rate"],
                player2["after_20_strike_rate"]
            ]
        })

        fig = px.bar(
            chart_data,
            x="Period",
            y="Strike Rate",
            color="Batter",
            barmode="group",
            text_auto=".2f",
            title="Early vs Later Strike Rate"
        )

        style_chart(fig, 420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # EYE-IN IMPROVEMENT COMPARISON

        st.subheader("Eye-In Improvement")

        improvement_data = pd.DataFrame({
            "Batter": [
                player1_name,
                player2_name
            ],
            "Improvement": [
                player1["improvement"],
                player2["improvement"]
            ]
        })

        fig = px.bar(
            improvement_data,
            x="Batter",
            y="Improvement",
            color="Batter",
            text_auto=".2f",
            title="Comparison of Eye-In Improvement"
        )

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="red"
        )

        style_chart(fig, 350)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # CONFIDENCE INTERVAL COMPARISON

        st.subheader("95% Bootstrap Confidence Intervals")

        fig = go.Figure()

        for name, player, color in [
            (player1_name, player1, "#2DD4BF"),
            (player2_name, player2, "#F59E0B")
        ]:

            fig.add_trace(
                go.Scatter(
                    x=[
                        player["ci_lower"],
                        player["ci_upper"]
                    ],
                    y=[name, name],
                    mode="lines",
                    line=dict(
                        color=color,
                        width=8
                    ),
                    name=f"{name} CI"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=[player["improvement"]],
                    y=[name],
                    mode="markers",
                    marker=dict(
                        color=color,
                        size=14
                    ),
                    name=f"{name} Estimate"
                )
            )

        fig.add_vline(
            x=0,
            line_dash="dash",
            line_color="red"
        )

        fig.update_layout(
            xaxis_title="Eye-In Improvement (SR points)",
            yaxis_title="Batter",
            height=400
        )

        style_chart(fig, 400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info(
            "A higher Eye-In Improvement indicates a larger "
            "increase in scoring rate between the first 10 balls "
            "and ball 21 onwards. It does not automatically mean "
            "that the batter is better overall."
        )


# =========================================================
# 11. DISMISSAL ANALYSIS PAGE
# =========================================================

elif page == "Dismissal Analysis":

    st.header("⚡ Dismissal Frequency Analysis")

    st.write(
        "Explore how dismissal frequency changes "
        "as batters face more deliveries."
    )

    ball_view = ball[
        ball["enough_data"]
    ]

    max_ball = int(
        ball_view["ball_faced_number"].max()
    )

    selected_ball = st.slider(
        "Maximum Ball Position",
        min_value=5,
        max_value=max_ball,
        value=min(30, max_ball)
    )

    filtered_ball = ball_view[
        ball_view["ball_faced_number"] <= selected_ball
    ]

    fig = px.line(
        filtered_ball,
        x="ball_faced_number",
        y="dismissal_rate_pct",
        markers=True,
        title="Dismissal Frequency by Ball Faced",
        labels={
            "ball_faced_number": "Ball Faced",
            "dismissal_rate_pct": "Dismissal Frequency (%)"
        }
    )

    fig.update_traces(
        line_color="#F59E0B",
        marker_color="#F59E0B",
        line_width=3
    )

    style_chart(fig, 470)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "This represents aggregated historical dismissal frequency, "
        "not an individual batter's predicted probability of dismissal. "
        "Later ball positions have fewer observations."
    )

    st.subheader("Ball Position Statistics")

    display_data = filtered_ball[
        [
            "ball_faced_number",
            "batter_innings",
            "dismissals",
            "dismissal_rate_pct"
        ]
    ].copy()

    display_data.columns = [
        "Ball Faced",
        "Innings Reaching This Ball",
        "Dismissals",
        "Dismissal Frequency (%)"
    ]

    st.dataframe(
        display_data.round(2),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# 12. PHASE ANALYSIS PAGE
# =========================================================

elif page == "Phase Analysis":

    st.header("📊 Batting Phase Analysis")

    st.write(
        "Compare batting performance across Powerplay, "
        "Middle and Death overs."
    )

    phases = [
        "Powerplay",
        "Middle",
        "Death"
    ]

    available_phases = phase["phase"].dropna().unique().tolist()

    selected_phases = st.multiselect(
        "Select Innings Phases",
        phases,
        default=[p for p in phases if p in available_phases]
    )

    phase_view = phase[
        (phase["phase"].isin(selected_phases))
        & (phase["enough_data"])
    ]

    left, right = st.columns(2)

    # STRIKE RATE BY PHASE

    with left:

        st.subheader("Strike Rate by Phase")

        fig = px.line(
            phase_view,
            x="ball_faced_number",
            y="strike_rate",
            color="phase",
            markers=True,
            title="Strike Rate Comparison"
        )

        fig.update_layout(
            xaxis_title="Ball Faced",
            yaxis_title="Strike Rate"
        )

        style_chart(fig, 450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # DISMISSAL FREQUENCY BY PHASE

    with right:

        st.subheader("Dismissal Frequency by Phase")

        fig = px.line(
            phase_view,
            x="ball_faced_number",
            y="dismissal_rate_pct",
            color="phase",
            markers=True,
            title="Dismissal Frequency Comparison"
        )

        fig.update_layout(
            xaxis_title="Ball Faced",
            yaxis_title="Dismissal Frequency (%)"
        )

        style_chart(fig, 450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# 13. FOOTER
# =========================================================

st.divider()

st.markdown(
    "<h4 style='color:#2DD4BF; text-align:center;'>"
    "🏏 IPL EYE-IN"
    "</h4>",
    unsafe_allow_html=True
)

st.caption(
    "Cricket Analytics Project | Historical IPL Ball-by-Ball Data"
)

st.caption(
    "Exploring batting patterns through data analytics."
)
