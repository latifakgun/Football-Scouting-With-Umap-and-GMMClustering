import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Eyeball Scout | Pro Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ULTRA PREMIUM CSS
# ---------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        * { font-family: 'Inter', sans-serif !important; }
        .stApp { background-color: #050505; color: #ffffff; }

        /* GRADIENT TEXT */
        h1, h2, h3 {
            font-weight: 800 !important;
            background: -webkit-linear-gradient(45deg, #4ADE80, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        /* INPUT FIELDS */
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #111111 !important;
            border: 1px solid #333333 !important;
            border-radius: 12px !important;
            color: white !important;
        }
        ul[data-baseweb="menu"] { background-color: #000 !important; border: 1px solid #333 !important; }

        /* METRIC CARDS */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 15px;
            text-align: center;
        }
        div[data-testid="stMetricValue"] { color: #00FFA3 !important; font-weight: 800; font-size: 24px !important; }
        div[data-testid="stMetricLabel"] { color: #888; font-size: 13px; }

        /* TABS */
        .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: transparent; border-bottom: 1px solid #333; margin-bottom: 20px; }
        .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; border: none; color: #666; font-size: 16px; font-weight: 600; }
        .stTabs [aria-selected="true"] { background-color: transparent; color: #00FFA3 !important; border-bottom: 3px solid #00FFA3; }

        /* SIDEBAR */
        [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #222; }
        
        header {visibility: hidden;}
        .block-container { padding-top: 2rem; }
        td { font-size: 14px !important; color: #ddd !important; border-bottom: 1px solid #222 !important; }

    </style>
""", unsafe_allow_html=True)

# 3. MAPPING & DATA LOADING
# ---------------------------------------------------------

# CLUSTER ID -> ROLE NAME MAPPING
# Modelden çıkan sayısal ID'leri gerçek futbol rollerine çevirir.
CLUSTER_NAME_MAP = {
    # DEFENDERS (0-4)
    0: "Ball Playing Defender",
    1: "Stopper / No-Nonsense CB",
    2: "Conservative Defender",
    3: "Progressive Defender",
    4: "Commanding Center Back",
    
    # MIDFIELDERS (10-15)
    10: "Deep-Lying Playmaker",
    11: "Ball Winning Midfielder",
    12: "Advanced Playmaker",
    13: "Box-to-Box Midfielder",
    14: "Wide Midfielder",
    15: "Dynamic Midfielder / Mezzala",
    
    # ATTACKERS (20-25)
    20: "Target Man / Aerial Threat",
    21: "Creative Winger",
    22: "Complete Forward",
    23: "Direct Winger / Dribbler",
    24: "Pressing Forward",
    25: "Poacher / Penalty Box Striker"
}

@st.cache_data
def load_data():
    # Yeni oluşturduğumuz İSİMLİ dosyayı oku
    df = pd.read_csv("Eyeball_Streamlit_Final_Named.csv")
    
    # Display Name oluştur
    df['Display_Name'] = df['Player'] + " (" + df['Season'].astype(str) + ") - " + df['Squad']
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("ERROR: CSV file not found.")
    st.stop()

# COLOR MAP (YENİ ROLLERE GÖRE GÜNCELLENDİ)
role_color_map = {
    # Defans (Mavi/Mor Tonları)
    "Ball Playing Defender": "#00BFFF",      # Deep Sky Blue
    "Stopper / No-Nonsense CB": "#8B0000",   # Dark Red
    "Conservative Defender": "#483D8B",      # Dark Slate Blue
    "Progressive Defender": "#1E90FF",       # Dodger Blue
    "Commanding Center Back": "#000080",     # Navy
    
    # Orta Saha (Yeşil/Turkuaz Tonları)
    "Deep-Lying Playmaker": "#2E8B57",       # Sea Green
    "Ball Winning Midfielder": "#556B2F",    # Dark Olive Green
    "Advanced Playmaker": "#00FF7F",         # Spring Green
    "Box-to-Box Midfielder": "#32CD32",      # Lime Green
    "Wide Midfielder": "#20B2AA",            # Light Sea Green
    "Dynamic Midfielder / Mezzala": "#00FFFF", # Cyan

    # Hücum (Kırmızı/Turuncu/Pembe Tonları)
    "Target Man / Aerial Threat": "#FF4500", # Orange Red
    "Creative Winger": "#FF1493",            # Deep Pink
    "Complete Forward": "#FFD700",           # Gold
    "Direct Winger / Dribbler": "#FF00FF",   # Magenta
    "Pressing Forward": "#CD5C5C",           # Indian Red
    "Poacher / Penalty Box Striker": "#FF0000" # Red
}

# 4. SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0;'>EYEBALL<span style='color:#00FFA3'>.</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 0.9rem; margin-top: -10px;'>AI SCOUTING ANALYTICS</p>", unsafe_allow_html=True)

# 5. MAIN LAYOUT
# ---------------------------------------------------------
st.markdown('<h1 style="font-size: 3rem; margin-bottom: 0;">SCOUTING INTELLIGENCE</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#888; margin-bottom: 30px; font-size: 1.1rem;">Next-generation 3D clustering & performance analysis suite.</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 3D EXPLORATION", 
    "⚔️ PLAYER COMPARISON", 
    "🏆 ROLE LEADERBOARD", 
    "🧬 SIMILARITY SEARCH"
])

# =============================================================================
# TAB 1: 3D EXPLORATION
# =============================================================================
with tab1:
    st.markdown("### 🎛️ DATA CONTROLS")
    c1, c2, c3, c4 = st.columns(4)
    
    all_seasons = sorted(df['Season'].unique(), reverse=True)
    selected_seasons = c1.multiselect("📅 SEASON", all_seasons, default=all_seasons[:1])
    
    if selected_seasons: df_season = df[df['Season'].isin(selected_seasons)]
    else: df_season = df.copy()
        
    teams = sorted(df_season['Squad'].unique())
    selected_teams = c2.multiselect("🛡️ SQUAD", teams)
    
    positions = sorted(df_season['General_Position'].unique())
    selected_pos = c3.multiselect("📍 POSITION", positions)
    
    if selected_pos: roles = sorted(df_season[df_season['General_Position'].isin(selected_pos)]['Role_Name'].unique())
    else: roles = sorted(df_season['Role_Name'].unique())
    selected_roles = c4.multiselect("🧠 ROLE", roles)

    final_df = df_season.copy()
    if selected_teams: final_df = final_df[final_df['Squad'].isin(selected_teams)]
    if selected_pos: final_df = final_df[final_df['General_Position'].isin(selected_pos)]
    if selected_roles: final_df = final_df[final_df['Role_Name'].isin(selected_roles)]

    st.markdown("---")

    col_search, col_stats = st.columns([1, 4])
    with col_search:
        search_list = ["Select..."] + sorted(final_df['Display_Name'].unique().tolist())
        selected_player_search = st.selectbox("ZOOM TO PLAYER", search_list)
        
        st.markdown(f"""
        <div style="background-color: #111; padding: 15px; border-radius: 12px; border: 1px solid #333; margin-top: 20px;">
            <span style="color: #888; font-size: 0.8rem;">ACTIVE PLAYERS</span><br>
            <b style="color: #00FFA3; font-size: 1.8rem;">{len(final_df)}</b>
        </div>
        """, unsafe_allow_html=True)

    with col_stats:
        if not final_df.empty:
            fig = px.scatter_3d(
                final_df, x='x', y='y', z='z',
                color='Role_Name', color_discrete_map=role_color_map,
                hover_name='Display_Name', hover_data=['Age', 'Goals', 'Assists'],
                opacity=0.9, size_max=15, title=""
            )
            fig.update_layout(
                scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, b=0, t=0), height=600,
                legend=dict(x=0, y=1, font=dict(color="#aaa", size=10), bgcolor="rgba(0,0,0,0.5)")
            )
            if selected_player_search != "Select...":
                p_data = df[df['Display_Name'] == selected_player_search]
                if not p_data.empty:
                    fig.add_trace(go.Scatter3d(
                        x=p_data['x'], y=p_data['y'], z=p_data['z'],
                        mode='markers', marker=dict(size=35, color='#00FFA3', symbol='diamond', line=dict(width=3, color='white')),
                        name='SELECTED', hoverinfo='text', hovertext=selected_player_search
                    ))
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("No players match.")

# =============================================================================
# TAB 2: PLAYER COMPARISON
# =============================================================================
with tab2:
    col_sel1, col_sel2 = st.columns(2)
    all_players = sorted(df['Display_Name'].unique().tolist())
    
    with col_sel1: p1_name = st.selectbox("PLAYER 1", all_players, index=0)
    with col_sel2: p2_name = st.selectbox("PLAYER 2", all_players, index=min(10, len(all_players)-1))

    if p1_name and p2_name:
        p1 = df[df['Display_Name'] == p1_name].iloc[0]
        p2 = df[df['Display_Name'] == p2_name].iloc[0]
        
        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("PLAYER 1", p1['Player'], f"{p1['Role_Name']}")
        c2.metric("TEAM", p1['Squad'], p1['Season'])
        c3.metric("PLAYER 2", p2['Player'], f"{p2['Role_Name']}")
        c4.metric("TEAM", p2['Squad'], p2['Season'])

        st.markdown("<br>", unsafe_allow_html=True)
        col_3d, col_radar = st.columns([1, 1])
        
        with col_3d:
            st.markdown("##### 📏 3D PROXIMITY")
            ignore_others = st.checkbox("Ignore Others (Focus Mode)", value=False)
            dist = np.linalg.norm(np.array([p1['x'], p1['y'], p1['z']]) - np.array([p2['x'], p2['y'], p2['z']]))
            sim_score = max(0, 100 - (dist * 5))
            st.caption(f"Spatial Distance: {dist:.2f} | Similarity: %{sim_score:.1f}")

            fig_comp = go.Figure()
            if not ignore_others:
                fig_comp.add_trace(go.Scatter3d(x=df['x'], y=df['y'], z=df['z'], mode='markers', marker=dict(size=3, color='#333', opacity=0.3), hoverinfo='skip', name='Others'))
            fig_comp.add_trace(go.Scatter3d(x=[p1['x']], y=[p1['y']], z=[p1['z']], mode='markers+text', marker=dict(size=20, color='#00FFA3'), name=p1['Player'], text=[p1['Player']], textposition="top center"))
            fig_comp.add_trace(go.Scatter3d(x=[p2['x']], y=[p2['y']], z=[p2['z']], mode='markers+text', marker=dict(size=20, color='#00D2FF'), name=p2['Player'], text=[p2['Player']], textposition="top center"))
            fig_comp.add_trace(go.Scatter3d(x=[p1['x'], p2['x']], y=[p1['y'], p2['y']], z=[p1['z'], p2['z']], mode='lines', line=dict(color='white', width=2, dash='dash'), name='Distance'))
            fig_comp.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0), height=400, showlegend=False)
            st.plotly_chart(fig_comp, use_container_width=True)

        with col_radar:
            st.markdown("##### ⚡ SKILL OVERLAP")
            radar_metrics = ['Goals', 'Assists', 'Shots', 'SoT', 'Dribbles_Succ', 'Prg_Pass_Dist', 'Tackles', 'Interceptions', 'Blocks']
            v1_raw = [p1.get(m, 0) for m in radar_metrics]
            v2_raw = [p2.get(m, 0) for m in radar_metrics]
            v1_norm, v2_norm = [], []
            for val1, val2 in zip(v1_raw, v2_raw):
                mx = max(val1, val2)
                if mx == 0: mx = 1
                v1_norm.append(val1/mx)
                v2_norm.append(val2/mx)
                
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=v1_norm, theta=radar_metrics, fill='toself', name=p1['Player'], text=v1_raw, hoverinfo="text+theta+name", line=dict(color='#00FFA3', width=3), fillcolor='rgba(0, 255, 163, 0.1)'))
            fig_radar.add_trace(go.Scatterpolar(r=v2_norm, theta=radar_metrics, fill='toself', name=p2['Player'], text=v2_raw, hoverinfo="text+theta+name", line=dict(color='#00D2FF', width=3), fillcolor='rgba(0, 210, 255, 0.1)'))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False), bgcolor='#111'), paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=30, l=30, r=30), height=400, showlegend=True, legend=dict(font=dict(color="white"), orientation="h"))
            st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown("##### 📋 DETAILED STATS")
        compare_metrics = {
            'ATTACK': ['Goals', 'Assists', 'Shots', 'SoT', 'npxG_p90', 'xA_p90'],
            'PLAYMAKING': ['Prg_Pass_Dist', 'Prg_Carry_Dist', 'GCA', 'SCA', 'Pass_Cmp_Pct'],
            'DEFENSE': ['Tackles', 'Interceptions', 'Blocks'],
            'INFO': ['Minutes', 'Age', 'Role_Probability']
        }
        rows = []
        for cat, metrics in compare_metrics.items():
            for m in metrics:
                rows.append({"Category": cat, "Metric": m, f"{p1['Player']}": p1.get(m, 0), f"{p2['Player']}": p2.get(m, 0)})
        comp_df = pd.DataFrame(rows)
        
        def smart_format(x):
            try: return f"{x:.0f}" if isinstance(x, (int, float)) and x % 1 == 0 else f"{x:.2f}"
            except: return x

        def highlight(row):
            c1, c2 = row.index[2], row.index[3]
            v1, v2 = row[c1], row[c2]
            styles = ['' for _ in row]
            win_css = 'color: #00FFA3; font-weight: 700; background-color: rgba(0, 255, 163, 0.05); border-radius: 4px;'
            lose_css = 'color: #555; font-weight: 400; opacity: 0.5;'
            try:
                val1, val2 = float(v1), float(v2)
                if val1 > val2: styles[2], styles[3] = win_css, lose_css
                elif val2 > val1: styles[2], styles[3] = lose_css, win_css
            except: pass
            return styles

        st.dataframe(comp_df.style.apply(highlight, axis=1).format(smart_format, subset=comp_df.columns[2:]), use_container_width=True, height=500, hide_index=True)

# =============================================================================
# TAB 3: ROLE LEADERBOARD (SMART RANKING)
# =============================================================================
with tab3:
    st.markdown("### 🏆 ROLE LEADERBOARD (Archetype Ranking)")
    st.info("Ranking Logic: Players are sorted by AI Confidence first. If confidence is 100%, they are ranked by their proximity to the role's geometric center (Purest Style).")

    c1, c2 = st.columns([2, 1])
    
    with c1:
        target_role = st.selectbox("Select Role to Rank", sorted(df['Role_Name'].unique()))
    with c2:
        top_n = st.slider("Top N Players", 5, 200, 50)
    
    # 1. ROLDEKİ OYUNCULARI AL
    role_df = df[df['Role_Name'] == target_role].copy()
    
    # 2. MERKEZİ (CENTROID) HESAPLA
    centroid = role_df[['x', 'y', 'z']].mean()
    
    # 3. MERKEZE UZAKLIĞI HESAPLA
    role_df['Dist_to_Center'] = np.sqrt(
        (role_df['x'] - centroid['x'])**2 +
        (role_df['y'] - centroid['y'])**2 +
        (role_df['z'] - centroid['z'])**2
    )
    
    # 4. SIRALAMA: Önce Olasılık (Yüksekten Düşüğe), Sonra Mesafe (Düşükten Yükseğe)
    role_df = role_df.sort_values(by=['Role_Probability', 'Dist_to_Center'], ascending=[False, True]).head(top_n)
    
    # Gösterilecek Sütunlar
    display_cols = ['Player', 'Squad', 'Season', 'Age', 'Role_Probability', 'Dist_to_Center', 'Goals', 'Assists', 'Minutes']
    
    st.dataframe(
        role_df[display_cols],
        use_container_width=True,
        height=600,
        column_config={
            "Role_Probability": st.column_config.ProgressColumn(
                "AI Confidence",
                help="Probability of belonging to this role",
                format="%.4f", # 4 hane göster ki fark belli olsun
                min_value=0,
                max_value=1,
            ),
            "Dist_to_Center": st.column_config.NumberColumn(
                "Archetype Dist.",
                help="Distance to the geometric center of this role. Lower is better (Purer style).",
                format="%.2f"
            )
        },
        hide_index=True
    )

# =============================================================================
# TAB 4: SIMILARITY SEARCH
# =============================================================================
with tab4:
    st.markdown("### 🧬 NEAREST NEIGHBORS")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        target_player_name = st.selectbox("Select Base Player", sorted(df['Display_Name'].unique()), key="sim_search")
    with c2:
        neighbor_count = st.slider("Number of Neighbors", 5, 20, 10)
    
    if target_player_name:
        target_player = df[df['Display_Name'] == target_player_name].iloc[0]
        distances = np.sqrt((df['x'] - target_player['x'])**2 + (df['y'] - target_player['y'])**2 + (df['z'] - target_player['z'])**2)
        df['Distance'] = distances
        neighbors = df[df['Display_Name'] != target_player_name].sort_values('Distance').head(neighbor_count)
        
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Scatter3d(x=[target_player['x']], y=[target_player['y']], z=[target_player['z']], mode='markers+text', marker=dict(size=25, color='#FFD700', symbol='diamond'), name='TARGET', text=[target_player['Player']], textposition="top center"))
        fig_sim.add_trace(go.Scatter3d(x=neighbors['x'], y=neighbors['y'], z=neighbors['z'], mode='markers', marker=dict(size=10, color='#00FFFF', opacity=0.8), name='Similar', hovertext=neighbors['Display_Name']))
        fig_sim.add_trace(go.Scatter3d(x=df['x'], y=df['y'], z=df['z'], mode='markers', marker=dict(size=2, color='#333', opacity=0.1), hoverinfo='skip', name='Others'))
        fig_sim.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0), height=500, showlegend=True)
        st.plotly_chart(fig_sim, use_container_width=True)
        
        st.dataframe(neighbors[['Player', 'Squad', 'Role_Name', 'Distance', 'Goals', 'Assists']], use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("""<div style="text-align: center; color: #444; font-size: 0.8rem;">EYEBALL INTELLIGENCE © 2026</div>""", unsafe_allow_html=True)

