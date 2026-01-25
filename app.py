import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. SAYFA AYARLARI VE CSS (MODERN UI)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Eyeball Scout",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ÖZEL CSS: UI Düzeltmeleri
st.markdown("""
    <style>
        /* 1. Üstteki standart Streamlit çubuğunu gizle (Sorunu çıkaran dikdörtgen) */
        header {visibility: hidden;}
        
        /* 2. Ana içerik bloğunu aşağı it (Sekmelerin görünmesi için) */
        .block-container {
            padding-top: 2rem; /* 1rem az geliyordu, 2rem yaptık */
            padding-bottom: 1rem;
        }
        
        /* Ana font ayarları */
        h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
        
        /* Kart Görünümü */
        div[data-testid="stMetric"] {
            background-color: #262730;
            border: 1px solid #464b5f;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        
        /* Tablo Başlıklarını Gizle (Daha temiz görünüm için) */
        thead tr th:first-child { display:none }
        tbody th { display:none }
        
        /* Tablo Yazı Tipi */
        td { font-size: 1.1em !important; }
    </style>
""", unsafe_allow_html=True)

# 2. VERİ YÜKLEME
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("eyeball_streamlit_final.csv")
    df['Display_Name'] = df['Player'] + " (" + df['Season'].astype(str) + ") - " + df['Squad']
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("HATA: CSV dosyası bulunamadı.")
    st.stop()

# RENK HARİTASI
role_color_map = {
    "Inverted Winger / Dribbler": "#FF0000",       
    "Elite Speedster / Direct Winger": "#FF00FF",  
    "Poacher / Penalty Box Striker": "#FFA500",    
    "Versatile Forward / Second Striker": "#FFFF00", 
    "Target Man / Aerial Threat": "#FF69B4",       
    "Pressing Forward": "#00FF00",                 
    "Technical Hub / Deep Playmaker": "#00FFFF",   
    "Progressive Passer / Controller": "#1E90FF",  
    "Physical Ball Carrier": "#9932CC",            
    "Defensive Midfielder / Anchor": "#8B4513",    
    "Wide Midfielder / Defensive Winger": "#7FFF00", 
    "Utility Player / Workhorse": "#A9A9A9",       
    "Deep Distributor / Ball Playing CB": "#008080", 
    "Stopper / No-Nonsense Defender": "#800000",   
    "Central Defender (Standard)": "#000080",      
    "Commanding Center Back": "#FFFFFF"            
}

# 3. YAN PANEL (SIDEBAR)
# ---------------------------------------------------------
st.sidebar.title("Scouting Tab")
st.sidebar.markdown("---")

# A. Sezon
all_seasons = sorted(df['Season'].unique(), reverse=True)
selected_seasons = st.sidebar.multiselect("Season", all_seasons, default=all_seasons[:1])

if selected_seasons:
    df_filtered_season = df[df['Season'].isin(selected_seasons)]
else:
    df_filtered_season = df.copy()

# B. Takım
teams = sorted(df_filtered_season['Squad'].unique())
selected_teams = st.sidebar.multiselect("Squad", teams)

# C. Mevki (Bölge yerine)
positions = sorted(df_filtered_season['General_Position'].unique())
selected_pos = st.sidebar.multiselect("Position", positions)

# D. Rol (Yapay Zeka Rolü yerine)
if selected_pos:
    roles = sorted(df_filtered_season[df_filtered_season['General_Position'].isin(selected_pos)]['Role_Name'].unique())
else:
    roles = sorted(df_filtered_season['Role_Name'].unique())
selected_roles = st.sidebar.multiselect("Role", roles)

# Filtreleme
final_df = df_filtered_season.copy()
if selected_teams: final_df = final_df[final_df['Squad'].isin(selected_teams)]
if selected_pos: final_df = final_df[final_df['General_Position'].isin(selected_pos)]
if selected_roles: final_df = final_df[final_df['Role_Name'].isin(selected_roles)]


# 4. ANA EKRAN
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["🌍 3D Exploration", "⚖️ Player Comparison"])

# --- TAB 1: 3D KEŞİF ---
with tab1:
    col_search, col_space = st.columns([1, 3])
    with col_search:
        search_list = ["Select..."] + sorted(final_df['Display_Name'].unique().tolist())
        selected_player_search = st.selectbox("Zoom to the Player:", search_list)

    if not final_df.empty:
        fig = px.scatter_3d(
            final_df, x='x', y='y', z='z',
            color='Role_Name', color_discrete_map=role_color_map,
            hover_name='Display_Name',
            hover_data=['Age', 'Goals', 'Assists', 'Minutes'],
            opacity=0.8, size_max=12, template='plotly_dark',
            title=f"Player Pool: {len(final_df)}"
        )
        fig.update_layout(
            scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, b=0, t=30), height=600,
            legend=dict(x=0, y=1, font=dict(size=10))
        )
        if selected_player_search != "Select...":
            p_data = df[df['Display_Name'] == selected_player_search]
            if not p_data.empty:
                fig.add_trace(go.Scatter3d(
                    x=p_data['x'], y=p_data['y'], z=p_data['z'],
                    mode='markers', marker=dict(size=25, color='white', symbol='diamond', line=dict(width=2, color='black')),
                    name='SELECTED', hoverinfo='text', hovertext=selected_player_search
                ))
        st.plotly_chart(fig, use_container_width=True)
        
        # CSV İndirme Butonu (İsteğe Bağlı)
        with st.expander("📥 Download CSV"):
            st.download_button(
                label="Download Filtered Data as CSV",
                data=final_df.to_csv(index=False).encode('utf-8'),
                file_name='filtered_data.csv',
                mime='text/csv'
            )

# --- TAB 2: KARŞILAŞTIRMA (GELİŞMİŞ) ---
with tab2:
    st.markdown("### ⚔️ Player Comparison")
    
    all_players_list = sorted(df['Display_Name'].unique().tolist())
    c1, c2 = st.columns(2)
    with c1:
        p1_name = st.selectbox("1st Player", all_players_list, index=0)
    with c2:
        p2_name = st.selectbox("2nd Player", all_players_list, index=min(10, len(all_players_list)-1))

    if p1_name and p2_name:
        p1 = df[df['Display_Name'] == p1_name].iloc[0]
        p2 = df[df['Display_Name'] == p2_name].iloc[0]

        # 1. KARTLAR
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🔵 {p1['Player']}")
            st.caption(f"{p1['Squad']} | {p1['Season']}")
            st.metric("Role", p1['Role_Name'])
        with col2:
            st.error(f"🔴 {p2['Player']}")
            st.caption(f"{p2['Squad']} | {p2['Season']}")
            st.metric("Role", p2['Role_Name'])
        
        st.markdown("---")

        # 2. RADAR GRAFİĞİ (NORMALİZE EDİLMİŞ)
        # Sorunu çözen kısım burası: Verileri 0-1 arasına sıkıştırıyoruz.
        radar_metrics = ['Goals', 'Assists', 'Shots', 'SoT', 'Dribbles_Succ', 'Prg_Pass_Dist', 'Tackles', 'Interceptions', 'Blocks']
        
        # Verileri çek
        vals1 = [p1.get(m, 0) for m in radar_metrics]
        vals2 = [p2.get(m, 0) for m in radar_metrics]
        
        # Normalizasyon (Ölçekleme)
        # İki oyuncunun maksimum değerine göre oranlıyoruz.
        # Böylece 5 Gol de, 500 Pas da grafikte düzgün görünür.
        normalized_vals1 = []
        normalized_vals2 = []
        
        for v1, v2 in zip(vals1, vals2):
            max_val = max(v1, v2)
            if max_val == 0: max_val = 1 # Sıfıra bölünme hatasını önle
            normalized_vals1.append(v1 / max_val)
            normalized_vals2.append(v2 / max_val)

        fig_radar = go.Figure()
        
        # Oyuncu 1
        fig_radar.add_trace(go.Scatterpolar(
            r=normalized_vals1, # Çizim için normalize değer
            theta=radar_metrics,
            fill='toself',
            name=p1['Player'],
            text=vals1, # Üzerine gelince GERÇEK değer yazsın
            hoverinfo="text+theta+name",
            line_color='#00CC96' # Yeşilimsi
        ))
        
        # Oyuncu 2
        fig_radar.add_trace(go.Scatterpolar(
            r=normalized_vals2,
            theta=radar_metrics,
            fill='toself',
            name=p2['Player'],
            text=vals2,
            hoverinfo="text+theta+name",
            line_color='#EF553B' # Kırmızımsı
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=False)), # Eksen sayılarını gizle (kafa karıştırmasın)
            showlegend=True,
            title="Statistics Radar",
            height=450,
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # 3. GELİŞMİŞ TABLO (Kazananı Vurgulama)
        st.subheader("Statistics Comparison")
        
        compare_metrics = {
            'Attacking': ['Goals', 'Assists', 'Shots', 'SoT', 'npxG_p90', 'xA_p90'],
            'Playmaking': ['Prg_Pass_Dist', 'Prg_Carry_Dist', 'GCA', 'SCA', 'Pass_Cmp_Pct'],
            'Defencing': ['Tackles', 'Interceptions', 'Blocks'],
            'General': ['Minutes', 'Age', 'Role_Probability']
        }
        
        # Pandas Styler kullanarak tabloyu boyuyoruz
        rows = []
        for category, metrics in compare_metrics.items():
            for m in metrics:
                val1 = p1.get(m, 0)
                val2 = p2.get(m, 0)
                
                # Kazananı belirle
                diff = val1 - val2
                
                rows.append({
                    "Category": category,
                    "Metric": m,
                    f"{p1['Player']}": val1,
                    f"{p2['Player']}": val2,
                })
        
        comp_df = pd.DataFrame(rows)

        def smart_format(x):
            try:
                if isinstance(x, (int, float)):
                    if x % 1 == 0:
                        return f"{x:.0f}"
                    else:
                        return f"{x:.2f}"
                return x
            except:
                return x
        
# RENKLENDİRME FONKSİYONU (Girinti hatası olmaması için buraya aldık)
        def highlight_winner(row):
            col1_name, col2_name = row.index[2], row.index[3]
            v1, v2 = row[col1_name], row[col2_name]
            styles = ['' for _ in row]
            
            winner_style = 'color: #00FF7F; font-weight: 900; text-shadow: 0 0 5px rgba(0,255,127,0.5); font-size: 1.1em;'
            loser_style = 'color: #666; font-weight: normal; opacity: 0.5;'
            draw_style = 'color: white;'

            try:
                val1, val2 = float(v1), float(v2)
                if val1 > val2:
                    styles[2], styles[3] = winner_style, loser_style
                elif val2 > val1:
                    styles[2], styles[3] = loser_style, winner_style
                else:
                    styles[2], styles[3] = draw_style, draw_style
            except: pass
            return styles

        st.dataframe(
            comp_df.style
            .apply(highlight_winner, axis=1)
            .format(smart_format, subset=comp_df.columns[2:]),
            use_container_width=True, height=600, hide_index=True
        )

# ALTLIK
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: grey;">
    Eyeball Scout | 
    <span style="color: #4ade80;">Position & Role Analysis</span> | 
    UMAP & CA
</div>
""", unsafe_allow_html=True)


