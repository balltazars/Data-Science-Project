import streamlit as st
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
import plotly.graph_objects as go
import os

@st.cache_resource
def load_assets():
    """Memuat semua model dan scaler sesuai export notebook."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    def get_path(filename):
        # Cek di root atau di folder models
        p1 = os.path.join(base_dir, filename)
        p2 = os.path.join(base_dir, 'models', filename)
        return p1 if os.path.exists(p1) else p2

    try:
        scaler = joblib.load(get_path('scaler.joblib'))
        # Kita butuh feature_names untuk tahu urutan kolom numerik yang di-scale
        features = joblib.load(get_path('feature_names.joblib')) 
        kat_cols = joblib.load(get_path('kat_cols.joblib'))
        xgb_vol = joblib.load(get_path('xgb_vol.joblib'))
        xgb_mape = joblib.load(get_path('xgb_mape.joblib'))
        feature_extractor = tf.keras.models.load_model(get_path('feature_extractor.h5'))
        
        return scaler, xgb_vol, xgb_mape, feature_extractor, features, kat_cols
    except Exception as e:
        st.error(f"Gagal memuat assets: {e}")
        return None

def run_prediction_logic(kat, df, assets):
    """Logika Rekursif 30 Hari - CLONE dari Notebook."""
    if assets is None: return [0] * 30
    scaler, xgb_vol, xgb_mape, feature_extractor, features, kat_cols = assets
    
    # 1. Setup Data Awal
    col_name = 'Kategori Produk' if 'Kategori Produk' in df.columns else 'Kategori'
    # Ambil 30 hari terakhir sesuai time_steps
    curr_df = df[df[col_name] == kat].sort_values('Waktu Pesanan Dibuat').tail(30)
    
    if len(curr_df) < 30: return [0] * 30

    # curr_win berisi data yang SUDAH di-scale (dari full_df di app utama)
    curr_win = curr_df[features].values.tolist()
    last_date = df['Waktu Pesanan Dibuat'].max()
    
    daily_forecasts = []
    
    # List nama fitur numerik (sesuai urutan di Notebook)
    num_features = ['day_sin', 'day_cos', 'lag_1', 'lag_7', 'lag_28', 'ma_7']
    
    for i in range(1, 31):
        # A. Prediksi (Input harus 3D: 1, 30, features)
        X_in = np.array([curr_win[-30:]], dtype=float)
        
        # Ekstrak fitur latent (32 dim)
        lat = feature_extractor.predict(X_in, verbose=0)
        
        # Predict Volume & MAPE (Inverse Log)
        pv_f = np.expm1(xgb_vol.predict(lat))[0]
        pm_f = np.expm1(xgb_mape.predict(lat))[0]
        
        # B. Ensemble Logic (Sama Persis Notebook)
        if kat in ['Kitchen', 'Home']:
            d_p = np.ceil((0.8 * pv_f) + (0.2 * pm_f))
        else:
            d_p = (0.3 * pv_f) + (0.7 * pm_f)
            d_p = 0 if d_p < 0.25 else np.ceil(d_p)
        
        d_p = max(0, d_p)
        daily_forecasts.append(d_p)
        
        # C. UPDATE WINDOW (Bagian Paling Krusial)
        nxt_d = last_date + pd.Timedelta(days=i)
        
        # Fitur numerik mentah sebelum di-scale
        raw_num = [
            np.sin(2 * np.pi * nxt_d.day / 31),
            np.cos(2 * np.pi * nxt_d.day / 31),
            np.log1p(d_p),                               # lag_1 hari esok
            curr_win[-7][2] if len(curr_win)>=7 else 0,    # lag_7 (ambil index 2: lag_1 saat ini)
            curr_win[-28][2] if len(curr_win)>=28 else 0,  # lag_28
            np.mean([r[2] for r in curr_win[-7:]])         # ma_7
        ]
        
        # SCALING: Fitur numerik harus di-scale dulu pake StandardScaler
        # Kita buat DF sementara agar scaler.transform tidak protes soal nama kolom
        tmp_df = pd.DataFrame([raw_num], columns=num_features)
        scaled_num = scaler.transform(tmp_df)[0]
        
        # Gabungkan Scaled Num + Kategori Encoding (Kategori gak di-scale)
        new_row = list(scaled_num)
        # Ambil kolom kategori (index 6 ke atas) dari baris pertama data asli
        new_row.extend(curr_df[kat_cols].iloc[0].tolist())
        
        curr_win.append(new_row)
        
    return daily_forecasts

def plot_forecast_plotly(kategori_name, full_df, forecast_vals):
    """Visualisasi gabungan Historis & Forecast."""
    col_name = 'Kategori Produk' if 'Kategori Produk' in full_df.columns else 'Kategori'
    target_col = 'Net_Sales' if 'Net_Sales' in full_df.columns else 'Jumlah Terjual Bersih'
    
    hist_data = full_df[full_df[col_name] == kategori_name].sort_values('Waktu Pesanan Dibuat').tail(30)
    hist_vals = hist_data[target_col].values
    hist_dates = pd.to_datetime(hist_data['Waktu Pesanan Dibuat'])
    
    start_date = hist_dates.max()
    forecast_dates = [start_date + pd.Timedelta(days=i) for i in range(1, 31)]
    
    fig = go.Figure()
    
    # Historis (Biru)
    fig.add_trace(go.Scatter(x=hist_dates, y=hist_vals, name='Historis', line=dict(color='#1f77b4', width=3)))
    
    # Forecast (Oranye Putus-putus)
    conn_dates = [hist_dates.iloc[-1]] + forecast_dates
    conn_vals = [hist_vals[-1]] + forecast_vals
    fig.add_trace(go.Scatter(x=conn_dates, y=conn_vals, name='Forecast', line=dict(color='#ff7f0e', width=3, dash='dash')))
    
    fig.update_layout(
        title=f"Trend & Forecast: {kategori_name}",
        xaxis_title="Tanggal", yaxis_title="Unit Terjual",
        template="plotly_white", hovermode="x unified"
    )
    return fig