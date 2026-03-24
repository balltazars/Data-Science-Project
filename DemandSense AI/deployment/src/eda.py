import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import io

@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data_from_DE.csv")
    
    if not os.path.exists(data_path):
        return None

    df = pd.read_csv(data_path)
    df['Weekend'] = df['Weekend'].replace({0:'No', 1:'Yes'})
    df['Waktu Pesanan Dibuat'] = pd.to_datetime(df['Waktu Pesanan Dibuat'])
    
    cols = [
        'Total Diskon',
        'Ongkos Kirim Dibayar oleh Pembeli',
        'Estimasi Potongan Biaya Pengiriman',
        'Perkiraan Ongkos Kirim'
    ]
    df[cols] = df[cols].astype('int64')
    df['Provinsi'] = df['Provinsi'].str.replace(r'\(.*\)', '', regex=True).str.strip()
    return df

def run_eda():
    st.title("📊 Market Demand and Sales Analysis")

    st.markdown("""
Analisis ini bertujuan untuk memahami pola permintaan penjualan pada e-commerce sales dataset melalui eksplorasi tren penjualan, distribusi produk, perilaku pembelian konsumen, serta faktor operasional yang mempengaruhi transaksi.

Insight yang dihasilkan dari analisis ini digunakan sebagai dasar untuk memahami dinamika permintaan sebelum dilakukan proses demand forecasting.
""")

    with st.spinner("Loading dataset..."):
        df = load_data()

    if df is None:
        st.error("❌ File 'data_from_DE.csv' tidak ditemukan di folder src!")
        return

    # ==============================
    # PRODUCT DISTRIBUTION
    # ==============================
    st.header("Inspecting product distribution")
    
    product_count = df['Kategori Produk'].value_counts().reset_index()
    product_count.columns = ['Kategori Produk', 'Count']

    fig_pie = px.pie(product_count, values='Count', names='Kategori Produk', 
                     title="Proporsi Kategori Produk",
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
- **Kitchen & Dining (36.5%)** dan **Home Organization & Living (33.1%)** mendominasi penjualan dan menyumbang hampir **70% dari total transaksi**.
- Hal ini menunjukkan bahwa permintaan terutama berasal dari **produk kebutuhan rumah tangga dan peralatan dapur**.
- **Tools & Accessories (~16%)** menjadi kategori pendukung dengan kontribusi menengah.
""")

    # ==============================
    # MONTHLY SALES DISTRIBUTION
    # ==============================
    st.header("1. Monthly Sales Distribution")
    df['year_month'] = df['Waktu Pesanan Dibuat'].dt.to_period('M').astype(str)

    monthly_category = df.groupby(['year_month', 'Kategori Produk'])['Jumlah Terjual Bersih'].sum().reset_index()

    fig_area = px.area(monthly_category, x='year_month', y='Jumlah Terjual Bersih', 
                       color='Kategori Produk', title='Monthly Sales Distribution by Product',
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_area, use_container_width=True)

    st.markdown("""
- Penjualan bulanan secara konsisten didominasi oleh **Kitchen & Dining**.
- **Kitchen & Dining memiliki variabilitas permintaan tertinggi**, menunjukkan perubahan demand yang cukup besar antar bulan.
""")

    # ==============================
    # MONTHLY SALES TREND
    # ==============================
    st.header("2. Monthly Sales Trend and Growth")
    monthly_total = df.groupby('year_month')['Jumlah Terjual Bersih'].sum().reset_index()

    fig_line = px.line(monthly_total, x='year_month', y='Jumlah Terjual Bersih', 
                       markers=True, title="Monthly Sales Trend Over Time")
    st.plotly_chart(fig_line, use_container_width=True)

    # MoM Growth
    monthly_total['MoM_growth_pct'] = monthly_total['Jumlah Terjual Bersih'].pct_change() * 100
    fig_growth = px.bar(monthly_total, x='year_month', y='MoM_growth_pct', 
                        title="Month-over-Month Growth (%)",
                        color='MoM_growth_pct', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_growth, use_container_width=True)

    st.markdown("""
- Tren penjualan bulanan menunjukkan **fluktuasi yang cukup tajam**.
- Analisis **Month-over-Month (MoM) Growth** menunjukkan bahwa pertumbuhan penjualan bersifat **sangat volatil**.
""")

    # ==============================
    # REVENUE
    # ==============================
    st.header("3. Gross and Net Revenue")
    df['Total Harga'] = df[['Total Pembayaran','Total Diskon','Ongkos Kirim Dibayar oleh Pembeli']].sum(axis=1)

    revenue_summary = df.groupby('Kategori Produk').agg(
        Gross_Revenue=('Total Harga','sum'),
        Net_Revenue=('Total Pembayaran','sum')
    ).reset_index()
    revenue_summary['Cost_Revenue'] = revenue_summary['Gross_Revenue'] - revenue_summary['Net_Revenue']

    rev_melted = revenue_summary.melt(id_vars='Kategori Produk', 
                                      value_vars=['Gross_Revenue', 'Net_Revenue', 'Cost_Revenue'],
                                      var_name='Revenue Type', value_name='Amount')

    fig_rev = px.bar(rev_melted, x='Kategori Produk', y='Amount', color='Revenue Type',
                     barmode='group', title="Financial Overview per Category",
                     text_auto='.2s')
    st.plotly_chart(fig_rev, use_container_width=True)

    # ==============================
    # WEEKDAY VS WEEKEND
    # ==============================
    st.header("4. Weekday vs Weekend Sales")
    weekend_sales = df.groupby(['Weekend','Kategori Produk'])['Jumlah Terjual Bersih'].sum().reset_index()

    fig_week = px.bar(weekend_sales, x='Kategori Produk', y='Jumlah Terjual Bersih', 
                      color='Weekend', barmode='group', title="Sales Comparison: Weekday vs Weekend")
    st.plotly_chart(fig_week, use_container_width=True)

    # ==============================
    # PROVINCE SALES
    # ==============================
    st.header("5. Sales by Provinces")
    province_sales = df.groupby('Provinsi')['Jumlah'].sum().sort_values(ascending=False).head(10).reset_index()

    fig_prov = px.bar(province_sales, x='Jumlah', y='Provinsi', orientation='h',
                      title="Top 10 Sales by Province", color='Jumlah',
                      color_continuous_scale='Blues')
    fig_prov.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_prov, use_container_width=True)

    # ==============================
    # PAYMENT METHODS
    # ==============================
    st.header("6. Payment Methods")
    pay_summary = df.groupby('Metode Pembayaran').agg(
        Total_Quantity=('Jumlah','sum'),
        Total_Revenue=('Total Pembayaran','sum')
    ).reset_index().sort_values('Total_Quantity', ascending=False)

    fig_pay = px.bar(pay_summary, x='Metode Pembayaran', y=['Total_Quantity', 'Total_Revenue'],
                     title="Payment Methods Impact", barmode='group')
    st.plotly_chart(fig_pay, use_container_width=True)

    # ==============================
    # EXECUTIVE SUMMARY
    # ==============================
    st.divider()
    st.header("Executive Summary")
    st.write("""
    Analisis ini bertujuan untuk memahami pola permintaan, faktor pendorong penjualan, serta beberapa aspek operasional yang mempengaruhi performa penjualan dalam dataset.
    """)

    st.subheader("Key Findings")
    st.markdown("""
1. **Dominasi Produk**: Kitchen & Dining dan Home Organization mendominasi hampir 70% transaksi.
2. **Volatilitas**: Pertumbuhan bulanan sangat tidak stabil, dipicu oleh event-driven demand.
3. **Metode Pembayaran**: COD masih menjadi raja transaksi baik dari volume maupun revenue.
4. **Geografis**: Penjualan terpusat di Pulau Jawa (Jabar, Jakarta, Banten).
5. **Logistik**: Ongkir ke Indonesia Timur (Papua/Maluku) sangat tinggi, menjadi penghambat ekspansi.
    """)

    st.header("Business Recommendations")
    
    with st.expander("1. Strategi Produk & Stok"):
        st.write("""
        Fokus pada Kitchen & Dining. Pastikan ketersediaan stok maksimal sebelum kampanye besar marketplace karena kategori ini memiliki variabilitas tertinggi.
        """)

    with st.expander("2. Strategi Logistik & Wilayah"):
        st.write("""
        Berikan subsidi ongkir atau promo 'Flat Ongkir' untuk wilayah luar Jawa untuk menstimulasi demand di daerah dengan biaya logistik tinggi.
        """)

    with st.expander("3. Strategi Pembayaran"):
        st.write("""
        Tawarkan promo cashback khusus pembayaran digital (ShopeePay/Online Payment) untuk perlahan mengurangi ketergantungan pada COD yang memiliki risiko operasional lebih tinggi.
        """)