import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ROL RENK HARİTASI (YÜKSEK KONTRAST - 16 FARKLI RENK)
role_color_map = {
    # --- HÜCUMCULAR (Sıcak ve Parlak Renkler) ---
    "Inverted Winger / Dribbler": "#FF0000",       # Saf Kırmızı (Çok Dikkat Çekici)
    "Elite Speedster / Direct Winger": "#FF00FF",  # Magenta / Parlak Pembe
    "Poacher / Penalty Box Striker": "#FFA500",    # Turuncu
    "Versatile Forward / Second Striker": "#FFFF00", # Saf Sarı
    "Target Man / Aerial Threat": "#FF69B4",       # Hot Pink (Şeker Pembesi)
    "Pressing Forward": "#00FF00",                 # Neon Yeşil (Enerji Vurgusu)

    # --- ORTA SAHALAR (Teknik ve Ara Renkler) ---
    "Technical Hub / Deep Playmaker": "#00FFFF",   # Cyan / Turkuaz (Parlak)
    "Progressive Passer / Controller": "#1E90FF",  # Dodger Blue (Parlak Mavi)
    "Physical Ball Carrier": "#9932CC",            # Dark Orchid (Mor)
    "Defensive Midfielder / Anchor": "#8B4513",    # Saddle Brown (Kahverengi - Toprak Rengi)
    "Wide Midfielder / Defensive Winger": "#7FFF00", # Chartreuse (Sarı-Yeşil Karışımı)
    "Utility Player / Workhorse": "#A9A9A9",       # Dark Gray (Gümüş/Gri - Nötr)

    # --- DEFANSLAR (Koyu ve Soğuk Renkler) ---
    "Deep Distributor / Ball Playing CB": "#008080", # Teal (Ördek Başı Yeşili)
    "Stopper / No-Nonsense Defender": "#800000",   # Maroon (Bordo)
    "Central Defender (Standard)": "#000080",      # Navy (Lacivert - En Koyu Mavi)
    "Commanding Center Back": "#FFFFFF"            # Beyaz (Koyu tema üzerinde Lider gibi parlasın)
}

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Eyeball Scout", page_icon="⚽", layout="wide")

# 2. VERİ YÜKLEME
@st.cache_data
def load_data():
    df = pd.read_csv("eyeball_streamlit_final.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("CSV dosyası bulunamadı! Lütfen dosyayı GitHub'a yüklediğinizden emin olun.")
    st.stop()

# 3. YAN PANEL (FİLTRELER)
st.sidebar.title("🔍 Filtreler")
st.sidebar.markdown("---")

# Takım Seçimi
teams = sorted(df['Squad'].unique())
selected_teams = st.sidebar.multiselect("Takım", teams)

# Mevki Seçimi
positions = sorted(df['General_Position'].unique())
selected_pos = st.sidebar.multiselect("Mevki", positions)

# Rol Seçimi
if selected_pos:
    roles = sorted(df[df['General_Position'].isin(selected_pos)]['Role_Name'].unique())
else:
    roles = sorted(df['Role_Name'].unique())
selected_roles = st.sidebar.multiselect("Rol", roles)

# Oyuncu Arama
st.sidebar.markdown("---")
player_list = sorted(df['Player'].unique())
selected_player = st.sidebar.selectbox("Oyuncu Ara", ["Seçiniz..."] + player_list)

# 4. VERİYİ FİLTRELE
filtered_df = df.copy()
if selected_teams:
    filtered_df = filtered_df[filtered_df['Squad'].isin(selected_teams)]
if selected_pos:
    filtered_df = filtered_df[filtered_df['General_Position'].isin(selected_pos)]
if selected_roles:
    filtered_df = filtered_df[filtered_df['Role_Name'].isin(selected_roles)]

# 5. ANA EKRAN (3D KÜRE)
st.title("⚽ Eyeball: 3D Futbolcu Evreni")
col1, col2 = st.columns([3, 1])

with col1:
    if not filtered_df.empty:
        fig = px.scatter_3d(
            filtered_df, x='x', y='y', z='z',
            color='Role_Name',
            color_discrete_map=role_color_map,
            hover_name='Player',
            hover_data=['Squad', 'Age', 'Goals', 'Assists'],
            opacity=0.7, size_max=10, template='plotly_dark',
            title=f"Görüntülenen Oyuncu: {len(filtered_df)}"
        )
        fig.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)), margin=dict(t=30, b=0, l=0, r=0))
        
        # Seçili Oyuncuyu Vurgula
        if selected_player != "Seçiniz...":
            p_data = df[df['Player'] == selected_player]
            fig.add_trace(go.Scatter3d(
                x=p_data['x'], y=p_data['y'], z=p_data['z'],
                mode='markers', marker=dict(size=15, color='red', symbol='diamond'),
                name=selected_player, hoverinfo='text', hovertext=selected_player
            ))
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Bu kriterlere uygun oyuncu bulunamadı.")

# 6. SAĞ PANEL (OYUNCU KARTI)
with col2:
    if selected_player != "Seçiniz...":
        player = df[df['Player'] == selected_player].iloc[0]
        st.header(player['Player'])
        st.caption(f"{player['Squad']} | {player['Age']} Yaş")
        st.info(f"🎯 Rol: {player['Role_Name']}")
        
        # İstatistikler
        c1, c2 = st.columns(2)
        c1.metric("Gol", int(player['Goals']))
        c2.metric("Asist", int(player['Assists']))
        c1.metric("Dakika", int(player['Minutes']))
        c2.metric("Güven %", int(player['Role_Probability']*100))
        
        # Benzer Oyuncular
        st.markdown("### 🧬 Benzerleri")
        dist = np.sqrt((df['x']-player['x'])**2 + (df['y']-player['y'])**2 + (df['z']-player['z'])**2)
        df['Dist'] = dist
        similars = df[df['Player'] != selected_player].sort_values('Dist').head(5)
        for _, s in similars.iterrows():
            st.write(f"- **{s['Player']}** ({s['Squad']})")
    else:

        st.info("👈 Detaylar için soldan filtreleyin veya oyuncu seçin.")



