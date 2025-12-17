import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(
    page_title="Aplikasi Anomali Magnetik",
    layout="wide"
)

st.title("Aplikasi Streamlit – Studi Kasus Data Magnetik")

# ==============================
# CONTOH DATA (GANTI DENGAN DATA ASLI JIKA ADA)
# ==============================
np.random.seed(10)

nx, ny = 50, 50
x = np.linspace(0, 1000, nx)
y = np.linspace(0, 1000, ny)
X, Y = np.meshgrid(x, y)

Tobs = (
    50
    + 10 * np.sin(X / 200) * np.cos(Y / 300)
    + np.random.normal(0, 1, (ny, nx))
)

Calculated_Regional = 50 + 5 * np.sin(X / 400)
Calculated_Residual = Tobs - Calculated_Regional

# ==============================
# SIDEBAR – KONTROL USER
# ==============================
st.sidebar.header("Pengaturan Visualisasi")

# Colormap
cmap_list = [
    "viridis", "plasma", "inferno",
    "magma", "jet", "seismic", "coolwarm"
]
cmap_choice = st.sidebar.selectbox("Pilih Colormap", cmap_list)

# Mode skala
scale_mode = st.sidebar.radio("Mode Skala", ["Auto", "Manual"])

vmin, vmax = None, None
if scale_mode == "Manual":
    global_min = float(np.min(Tobs))
    global_max = float(np.max(Tobs))

    vmin = st.sidebar.slider(
        "vmin", global_min, global_max, global_min
    )
    vmax = st.sidebar.slider(
        "vmax", global_min, global_max, global_max
    )

# ==============================
# FUNGSI PLOT
# ==============================
def plot_map(data, title):
    fig, ax = plt.subplots(figsize=(6, 5))
    c = ax.contourf(
        X, Y, data,
        levels=50,
        cmap=cmap_choice,
        vmin=vmin,
        vmax=vmax
    )
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.colorbar(c, ax=ax)
    return fig

# ==============================
# LAYOUT 3 KOLOM
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Anomali Observasi")
    fig_obs = plot_map(Tobs, "Anomali Magnetik Observasi")
    st.pyplot(fig_obs)

with col2:
    st.subheader("Anomali Regional")
    fig_reg = plot_map(Calculated_Regional, "Anomali Magnetik Regional")
    st.pyplot(fig_reg)

with col3:
    st.subheader("Anomali Residual")
    fig_res = plot_map(Calculated_Residual, "Anomali Magnetik Residual")
    st.pyplot(fig_res)

# ==============================
# DOWNLOAD PLOT
# ==============================
st.markdown("---")
st.subheader("Simpan Hasil Plot")

fig_all, axs = plt.subplots(1, 3, figsize=(18, 5))

data_list = [
    Tobs,
    Calculated_Regional,
    Calculated_Residual
]
titles = ["Observasi", "Regional", "Residual"]

for ax, data, title in zip(axs, data_list, titles):
    c = ax.contourf(
        X, Y, data,
        levels=50,
        cmap=cmap_choice,
        vmin=vmin,
        vmax=vmax
    )
    ax.set_title(title)
    plt.colorbar(c, ax=ax)

buf = io.BytesIO()
fig_all.savefig(buf, format="png", dpi=300)
buf.seek(0)

st.download_button(
    label="Download Plot (PNG)",
    data=buf,
    file_name="anomali_magnetik.png",
    mime="image/png"
)

st.success(
    "Aplikasi siap digunakan. "
    "Ganti bagian data dengan data magnetik asli jika diperlukan."
)
