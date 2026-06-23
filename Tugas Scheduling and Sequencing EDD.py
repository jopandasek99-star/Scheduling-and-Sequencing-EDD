import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from io import BytesIO

# ==========================================
# 1. PAGE CONFIGURATION & AGGRESSIVE PREMIUM SKIN
# ==========================================
st.set_page_config(page_title="EDD Scheduling System", layout="wide")

# Jalur paksa kustomisasi warna (Palet: Dark Sienna, Rosewood & Off-White)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        /* Force Global Background & Text */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #fdfcf9 !important;
            color: #250902 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Force Right Sidebar Panel Background to Dark Sienna */
        section[data-testid="stSidebar"] {
            background-color: #38040e !important;
            border-left: 1px solid #250902 !important;
        }
        
        /* Force Sidebar Text & Labels to Off-White */
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label {
            color: #fdfcf9 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Clean Data Editor & Inputs */
        div[data-baseweb="input"], div[data-baseweb="data-editor"], [data-testid="stDataEditor"] {
            background-color: #ffffff !important; 
            border: 1px solid #e2dcd5 !important;
            border-radius: 8px !important;
        }
        
        input {
            color: #38040e !important; 
            font-weight: 600 !important;
        }
        
        /* Headings Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #38040e !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }
        
        /* Dividers color mapping */
        hr {
            border-top: 1px solid #e2dcd5 !important;
        }
        
        /* Professional Buttons (Rosewood to Crimson Red Hover) */
        .stButton>button {
            background-color: #640d14 !important;
            color: #fdfcf9 !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.6rem 2.5rem !important;
        }
        .stButton>button:hover {
            background-color: #800e13 !important;
            box-shadow: 0 4px 15px rgba(100,13,20,0.2) !important;
        }
        
        /* Custom Info Cards style */
        .metric-card {
            background-color: #ffffff !important; 
            padding: 18px !important; 
            border-radius: 8px !important; 
            border: 1px solid #e2dcd5 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Master Header Platform Branding - CLEAN LOOK
st.title("Tugas Sistem Produksi Scheduling & Sequencing Earliest Due Date")
st.markdown("---")

# ==========================================
# 2. SIDEBAR (KANAN) - CLEAN & DIRECT INFO
# ==========================================
st.sidebar.markdown("### Hello")
st.sidebar.markdown("Earliest due date is a sequencing rule that sorts jobs based on their deadlines to minimize maximum tardiness.")
st.sidebar.markdown("---")
st.sidebar.markdown("Please input the scheduling start time below:")
scheduling_start = st.sidebar.number_input("Scheduling Start Time (T=0)", min_value=0, value=0, step=1)

# ==========================================
# 3. DATA INPUT MANAGEMENT
# ==========================================
st.subheader("⚙️ Job Data Input Management")

input_method = st.radio(
    "Select Data Input Method:", 
    ["Manual Interface Input", "Use Template Dataset"]
)

df_working = None

if input_method == "Manual Interface Input":
    num_jobs = st.number_input("Number of Jobs in Queue:", min_value=1, max_value=20, value=5, step=1)
    
    init_data = {
        'Job ID': [f"Job {chr(65+i)}" for i in range(num_jobs)],
        'Processing Time (Days)': [0] * num_jobs,
        'Due Date (Day Count)': [0] * num_jobs
    }
    df_empty = pd.DataFrame(init_data)
    st.markdown("##### Edit Job Parameters directly in the grid below:")
    df_working = st.data_editor(df_empty, use_container_width=True, hide_index=True)

else:
    default_data = {
        'Job ID': ['Job A', 'Job B', 'Job C', 'Job D', 'Job E'],
        'Processing Time (Days)': [5, 3, 8, 2, 6],
        'Due Date (Day Count)': [10, 6, 20, 8, 15]
    }
    df_working = pd.DataFrame(default_data)
    st.markdown("##### Template Dataset Loaded Preview:")
    df_working = st.data_editor(df_working, use_container_width=True, hide_index=True)

# ==========================================
# 4. SEQUENCING & SCHEDULING ENGINE (EDD)
# ==========================================
if df_working is not None and not df_working.empty:
    
    df_working['Processing Time (Days)'] = pd.to_numeric(df_working['Processing Time (Days)']).fillna(0).astype(int)
    df_working['Due Date (Day Count)'] = pd.to_numeric(df_working['Due Date (Day Count)']).fillna(0).astype(int)
    
    st.markdown("---")
    st.header("📊 Sequence Planning & Analytics Framework")
    
    t_edd = st.tabs(["Earliest Due Date (EDD) Scheduling Optimization"])
    
    with t_edd[0]:
        st.markdown(f"The EDD rule sequences jobs in ascending order of their Due Dates. (Current Timeline Start: **Day {scheduling_start}**)")
        
        df_edd = df_working.sort_values(by=['Due Date (Day Count)', 'Processing Time (Days)']).copy()
        
        completion_times = []
        current_time = scheduling_start
        
        for index, row in df_edd.iterrows():
            current_time += row['Processing Time (Days)']
            completion_times.append(current_time)
            
        df_edd['Completion Time (Waktu Selesai)'] = completion_times
        df_edd['Flow Time (Waktu Alir)'] = df_edd['Completion Time (Waktu Selesai)'] - scheduling_start
        
        tardiness_list = []
        for index, row in df_edd.iterrows():
            tardiness_val = max(0, row['Completion Time (Waktu Selesai)'] - row['Due Date (Day Count)'])
            tardiness_list.append(tardiness_val)
            
        df_edd['Tardiness (Keterlambatan)'] = tardiness_list
        
        st.dataframe(df_edd, use_container_width=True, hide_index=True)
        
        total_flow_time = df_edd['Flow Time (Waktu Alir)'].sum()
        total_tardiness = df_edd['Tardiness (Keterlambatan)'].sum()
        max_tardiness = df_edd['Tardiness (Keterlambatan)'].max()
        job_count = len(df_edd)
        
        avg_flow_time = total_flow_time / job_count if job_count > 0 else 0
        avg_tardiness = total_tardiness / job_count if job_count > 0 else 0
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Sequencing Performance Metrics Summary")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='metric-card' style='border-left: 4px solid #640d14 !important;'>
                            <div style='color: #640d14; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;'>Average Flow Time</div>
                            <div style='font-size: 22px; font-weight: 700; color: #250902; margin-top: 4px;'>{avg_flow_time:.2f} Days</div>
                            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='metric-card' style='border-left: 4px solid #800e13 !important;'>
                            <div style='color: #800e13; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;'>Average Tardiness</div>
                            <div style='font-size: 22px; font-weight: 700; color: #250902; margin-top: 4px;'>{avg_tardiness:.2f} Days</div>
                            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='metric-card' style='border-left: 4px solid #ad2831 !important;'>
                            <div style='color: #ad2831; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;'>Maximum Tardiness</div>
                            <div style='font-size: 22px; font-weight: 700; color: #250902; margin-top: 4px;'>{max_tardiness} Days</div>
                            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='metric-card' style='border-left: 4px solid #250902 !important; background-color: #fffaf5 !important;'>
                            <div style='color: #250902; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;'>Jobs in System (Avg)</div>
                            <div style='font-size: 22px; font-weight: 700; color: #38040e; margin-top: 4px;'>{(total_flow_time / df_edd['Processing Time (Days)'].sum()):.2f} Jobs</div>
                            </div>""", unsafe_allow_html=True)

    # ==========================================
    # 5. VISUALIZATION - PETA PENJADWALAN (GANTT CHART)
    # ==========================================
    st.markdown("---")
    st.header("🗺️ Peta Penjadwalan & Linimasa Operasional (EDD Gantt Chart)")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#fdfcf9')
    ax.set_facecolor('#ffffff')
    
    y_labels = []
    # Dinamisasi Palet Warna Baru: Kombinasi Eksklusif Red-Sienna Palette
    colors_pool = ['#640d14', '#38040e', '#800e13', '#ad2831', '#250902']
    
    start_times_dict = {}
    accumulator = scheduling_start
    for index, row in df_edd.iterrows():
        start_times_dict[row['Job ID']] = accumulator
        accumulator += row['Processing Time (Days)']

    df_edd_reversed = df_edd.iloc[::-1].reset_index(drop=True)

    for idx, row in enumerate(df_edd_reversed.itertuples()):
        job_id = row._1
        proc_time = row._2
        due_date = row._3
        comp_time = row._4
        job_start = start_times_dict[job_id]
        
        original_idx = df_edd[df_edd['Job ID'] == job_id].index[0]
        bar_color = colors_pool[original_idx % len(colors_pool)]
        
        y_bottom = idx * 10 + 2
        y_height = 6
        y_top_edge = y_bottom + y_height
        
        if comp_time > due_date:
            if job_start < due_date:
                ontime_duration = due_date - job_start
                tardy_duration = comp_time - due_date
                
                ax.broken_barh([(job_start, ontime_duration)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#250902', linewidth=1, alpha=0.95)
                ax.broken_barh([(due_date, tardy_duration)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#250902', linewidth=1, hatch='//', alpha=0.7)
            else:
                ax.broken_barh([(job_start, proc_time)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#250902', linewidth=1, hatch='//', alpha=0.7)
        else:
            ax.broken_barh([(job_start, proc_time)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#250902', linewidth=1, alpha=0.95)
            
        ax.text(job_start + proc_time/2, y_bottom + y_height/2, f"{job_id}\n({proc_time} Hari)", 
                ha='center', va='center', color='#fdfcf9', fontweight='bold', fontsize=9)
        
        ax.axvline(x=due_date, color='#ad2831', linestyle='--', linewidth=1.5, alpha=0.8)
        ax.text(due_date + 0.2, y_top_edge + 0.4, f"DL: {due_date}", 
                color='#ad2831', fontsize=11, fontweight='bold', ha='left', va='bottom')
        
        y_labels.append(job_id)
        
    max_horizon = max(accumulator + 2, df_edd['Due Date (Day Count)'].max() + 5)
    ax.set_xlabel('Horizon Waktu Produksi (Hari)', fontsize=10, fontweight='bold', color='#250902')
    ax.set_ylabel('Daftar Antrean Kerja (Job ID)', fontsize=10, fontweight='bold', color='#250902')
    
    ax.set_xticks(np.arange(0, max_horizon, 1))
    ax.set_xticklabels(np.arange(0, max_horizon, 1).astype(int), fontsize=8, color='#250902')
    
    ax.set_yticks([i*10 + 5 for i in range(len(df_edd_reversed))])
    ax.set_yticklabels(y_labels, fontsize=9, fontweight='bold', color='#250902')
    ax.set_xlim(0, max_horizon)
    ax.set_ylim(0, len(df_edd_reversed)*10 + 9)
    ax.grid(True, linestyle=':', alpha=0.4, axis='x', color='#250902')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e2dcd5')
    ax.spines['bottom'].set_color('#e2dcd5')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Analisis Peta
    st.markdown("### 🔍 Analisis Peta Operasional")
    c_info, c_desc = st.columns([1, 2])
    with c_info:
        st.info(f"**Urutan Eksekusi Mesin Tunggal:** \n**{' ➔ '.join(df_edd['Job ID'].tolist())}**")
    with c_desc:
        st.markdown(f"""
        * **Waktu Selesai Total (Makespan):** Seluruh rangkaian pengerjaan akan rampung pada hari ke-**{df_edd['Completion Time (Waktu Selesai)'].max()}**.
        * **Keterlambatan Maksimal:** Batas keterlambatan terlama berhasil ditekan hingga maksimal **{max_tardiness} hari**.
        * **Legenda Visual Grafik:** * Blok warna **Solid (Polos)** = Durasi pengerjaan aman (sebelum batas deadline).
          * Blok warna **Berarsir miring (`//`)** = Durasi pengerjaan yang terlambat (*Tardiness*) karena melewati batas garis merah putus-putus (`DL`).
        """)

    # ==========================================
    # 5B. CARA PEMAKAIAN SISTEM (NUMERIC POINTS)
    # ==========================================
    st.markdown("---")
    st.subheader("📋 Panduan Cara Pemakaian Sistem")
    st.markdown("""
    1. **Pilih Metode Input Data:** Pilih opsi **Manual Interface Input** untuk memasukkan data Anda sendiri atau klik **Use Template Dataset** untuk memuat data simulasi secara instan.
    2. **Tentukan Jumlah Job:** Jika memilih input manual, masukkan jumlah antrean pekerjaan (*job*) yang ingin dihitung melalui kolom input angka yang disediakan.
    3. **Isi Parameter Job:** Masukkan nilai durasi waktu kerja pada kolom **Processing Time (Days)** dan batas tenggat waktu pada kolom **Due Date (Day Count)** di tabel editor yang interaktif.
    4. **Evaluasi Hasil Kalkulasi:** Periksa tabel optimasi EDD yang otomatis mengurutkan baris berdasarkan tenggat waktu terdekat dan perhatikan kartu indikator KPI rata-rata performa.
    5. **Analisis Gantt Chart:** Lihat grafik visualisasi di bagian bawah untuk mendeteksi bagian kerja yang aman (warna solid) dan bagian yang terlambat (warna berarsir miring `//`).
    6. **Unduh Laporan Resmi:** Klik tombol **Download Production Schedule Report (Excel)** untuk mengekstrak lembar kerja hasil optimasi ke format Excel.
    """)

    # ==========================================
    # 6. EXPORT MANAGEMENT REPORTING DATA
    # ==========================================
    st.markdown("---")
    st.subheader("💾 Management Reporting Layer")
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_edd.to_excel(writer, sheet_name="EDD Production Schedule", index=False)
        
        df_meta_summary = pd.DataFrame({
            'Performance Matrix Target': ['Average Flow Time', 'Average Tardiness', 'Maximum Tardiness'],
            'Values Calculated (Days Profile)': [avg_flow_time, avg_tardiness, max_tardiness]
        })
        df_meta_summary.to_excel(writer, sheet_name="Performance Summary Logs", index=False)
        
    buffer.seek(0)
        
    st.download_button(
        label="Download Production Schedule Report (Excel)", 
        data=buffer, 
        file_name="Production_Scheduling_EDD_Report.xlsx", 
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("💡 Establish baseline job transaction vectors above to trigger automated queue metric calculations.")
