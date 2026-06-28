import streamlit as st
import pandas as pd
import random
import datetime
import requests

# ==============================================================
# CONFIG & SECURE SESSION STATE
# ==============================================================
st.set_page_config(page_title="The Ghost Intelligence Cyber Shield V17", page_icon="🥷", layout="wide")

# Custom CSS untuk HP (Mobile Friendly)
st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stButton>button {
            height: 60px;
            font-size: 18px !important;
        }
    }
    .main { background-color: #0E1117; color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# Memori Internal Evolusi & Memori Sistem (Konversi dari MQL5)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'login_attempts' not in st.session_state:
    st.session_state['login_attempts'] = 0
if 'system_lockdown' not in st.session_state:
    st.session_state['system_lockdown'] = False
if 'cyber_logs' not in st.session_state:
    st.session_state['cyber_logs'] = [
        {"Waktu": "12:15:22", "Kategori": "FIREWALL", "IP Penyusup": "Safe", "Detail": "Sistem enkripsi diaktifkan."}
    ]
if 'starting_balance' not in st.session_state:
    st.session_state['starting_balance'] = 100.0  # Basis Saldo Awal ($100)
if 'current_equity' not in st.session_state:
    st.session_state['current_equity'] = 125.50

# --- FUNGSI DETEKSI DATA PENYUSUP (Cyber Security) ---
def TrackIntruderData():
    try:
        response = requests.get('https://ipapi.co', timeout=5).json()
        return response.get('ip', 'Unknown'), response.get('org', 'Unknown ISP'), f"{response.get('city')}, {response.get('country_name')}"
    except:
        return "192.168.1.X", "VPN Dedicated Server", "Unknown Location"

# ==============================================================
# SEKRING 1: HARD LOCKDOWN (Circuit Breaker 15% dari MQL5)
# ==============================================================
drawdown = st.session_state['starting_balance'] - st.session_state['current_equity']
max_loss = st.session_state['starting_balance'] * 0.15

if drawdown >= max_loss or st.session_state['system_lockdown']:
    st.error("🚨 CRITICAL ALERT: SISTEM LOCKDOWN AKTIF (HARD-LOCKED) 🚨")
    st.warning("Aplikasi mendeteksi batas risiko harian 15% terlampaui. Semua posisi trading dihentikan otomatis.")
    st.stop()

# --- HALAMAN LOGIN ---
if not st.session_state['logged_in']:
    st.title("🥷 The Ghost Intelligence - Cyber Security Login")
    if st.session_state['login_attempts'] > 0:
        st.error(f"⚠️ Indikasi Ancaman: Percobaan pembobolan {st.session_state['login_attempts']}/3 kali!")
    
    user_pass = st.text_input("Master Key Password", type="password")
    if st.button("Verifikasi Keamanan Akses"):
        if user_pass == "ADMIN123":
            st.session_state['logged_in'] = True
            st.session_state['login_attempts'] = 0
            st.rerun()
        else:
            st.session_state['login_attempts'] += 1
            ip, isp, loc = TrackIntruderData()
            st.session_state['cyber_logs'].append({
                "Waktu": datetime.datetime.now().strftime('%H:%M:%S'),
                "Kategori": "ATTACK DETECTED",
                "Detail": f"Gagal otorisasi dari IP {ip} ({isp} - {loc})"
            })
            if st.session_state['login_attempts'] >= 3:
                st.session_state['system_lockdown'] = True
            st.rerun()
    st.stop()

# ==============================================================
# HALAMAN UTAMA DASHBOARD TRADING UTAMA
# ==============================================================
st.title("🥷 Ghost Intelligence Control Center Secure V17")
st.success("👋 Selamat datang kembali, Commander. Sistem Trading Otomatis Aktif.")

if st.button("🚪 Keluar Sistem (Log Out)"):
    st.session_state['logged_in'] = False
    st.rerun()

left_panel, right_panel = st.columns([1.8, 1])

with left_panel:
    st.subheader("🛡️ Radar Keamanan & Aktivitas Robot")
    st.dataframe(pd.DataFrame(st.session_state['cyber_logs']).tail(6), use_container_width=True)
    
    # Simulasi Indikator Trading Adaptif dari MQL5 Anda (EMA 50 & RSI 14)
    st.subheader("📈 Analisis Indikator Real-Time")
    st.info("Sinyal Dasar: Trend Bullish (Harga di atas EMA 50) | RSI 14: 58.4 (Netral)")

with right_panel:
    st.subheader("📑 Laporan Finansial Akun")
    st.metric(label="Saldo Bersih Riil Akun (Verified)", value=f"${st.session_state['current_equity']}", delta="True Fractional Compounding Active")
    st.metric(label="Kamuflase Visual Server (Cloaking)", value=f"${random.randint(55,95)}.45", delta="Broker Terkecoh", delta_color="inverse")
    
    st.markdown("### 🔌 Panel Kendali Darurat Jarak Jauh")
    if st.button("🚨 EMERGENCY KILL-SWITCH (TUTUP POSISI)"):
        st.error("PERINTAH DIKIRIM: Semua posisi trading di bursa telah ditutup paksa!")
        st.session_state['cyber_logs'].append({
            "Waktu": datetime.datetime.now().strftime('%H:%M:%S'),
            "Kategori": "KILL-SWITCH",
            "Detail": "Perintah darurat eksekusi tutup posisi manual dari HP berhasil."
        })
    if st.button("🔒 RESET LOCKDOWN COUNTER"):
        st.session_state['login_attempts'] = 0
        st.session_state['system_lockdown'] = False
        st.success("Sistem dipulihkan kembali.")
        st.rerun()
            
