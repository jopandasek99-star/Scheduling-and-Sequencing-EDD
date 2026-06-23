import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from io import BytesIO

# ==========================================
# 1. PAGE CONFIGURATION & PREMIUM SKIN
# ==========================================
st.set_page_config(page_title="Production Scheduling System", layout="wide")

# Custom architectural skin injection (Premium Editorial Looks)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background-color: #faf8f2;
        }
        
        section[data-testid="stSidebar"] {
            background-color: #f4efdc !important;
            border-left: 1px solid #e5dfcb;
            border-right: none !important;
        }
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #6a0708 !important;
            font-weight: 700;
        }
        
        div[data-baseweb="input"] {
            background-color: #ffffff !important; 
            border: 1px solid #e5dfcb !important;
            border-radius: 6px !important;
        }
        
        input {
            color: #6a0708 !important; 
            font-weight: 600 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #6a0708 !important;
            font-weight: 700 !important;
        }
        
        hr {
            border-top: 1px solid #e5dfcb !important;
            margin-top: 2rem !important;
            margin-bottom: 2rem !important;
        }
        
        .stButton>button {
            background-color: #6a0708 !important;
            color: #f4efdc !important;
            border-radius: 6px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.5rem 2rem !important;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #a01a1e !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(106,7,8,0.15);
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
st.subheader("Job Data Input Management")

input_method = st.radio(
    "Select Data Input Method:", 
    ["Manual Interface Input", "Use Template Dataset"]
)

df_working = None

if input_method == "Manual Interface Input":
    num_jobs = st.number_input("Number of Jobs in Queue:", min_value=1, max_value=20, value=5, step=1)
    
    # Generate interactive empty shell for data editing
    init_data = {
        'Job ID': [f"Job {chr(65+i)}" for i in range(num_jobs)],
        'Processing Time (Days)': [0] * num_jobs,
        'Due Date (Day Count)': [0] * num_jobs
    }
    df_empty = pd.DataFrame(init_data)
    st.markdown("##### Edit Job Parameters directly in the grid below:")
    df_working = st.data_editor(df_empty, use_container_width=True, hide_index=True)

else:
    # High-fidelity testing scenario template dataset
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
    
    # Sanitize input datatypes
    df_working['Processing Time (Days)'] = pd.to_numeric(df_working['Processing Time (Days)']).fillna(0).astype(int)
    df_working['Due Date (Day Count)'] = pd.to_numeric(df_working['Due Date (Day Count)']).fillna(0).astype(int)
    
    # --------------------------------------
    # ANALYSIS LAYER — TAB SEQUENCING
    # --------------------------------------
    st.markdown("---")
    st.header("Sequence Planning & Analytics Framework")
    
    t_edd = st.tabs(["📊 Earliest Due Date (EDD) Scheduling Optimization"])
    
    with t_edd[0]:
        st.subheader("EDD Priority Rule Sequence Calculations")
        st.markdown(f"The EDD rule sequences jobs in ascending order of their Due Dates. (Current Timeline Start: **Day {scheduling_start}**)")
        
        # Core Algorithmic Logic Rule Execution
        df_edd = df_working.sort_values(by=['Due Date (Day Count)', 'Processing Time (Days)']).copy()
        
        # Calculate timeline metrics sequence array
        completion_times = []
        current_time = scheduling_start
        
        for index, row in df_edd.iterrows():
            current_time += row['Processing Time (Days)']
            completion_times.append(current_time)
            
        df_edd['Completion Time (Waktu Selesai)'] = completion_times
        df_edd['Flow Time (Waktu Alir)'] = df_edd['Completion Time (Waktu Selesai)'] - scheduling_start
        
        # Calculate Tardiness: Max(0, Completion Time - Due Date)
        tardiness_list = []
        for index, row in df_edd.iterrows():
            tardiness_val = max(0, row['Completion Time (Waktu Selesai)'] - row['Due Date (Day Count)'])
            tardiness_list.append(tardiness_val)
            
        df_edd['Tardiness (Keterlambatan)'] = tardiness_list
        
        # Display Scheduled Dataset Results
        st.dataframe(df_edd, use_container_width=True, hide_index=True)
        
        # Calculate Evaluation Metrics Summary Data Points
        total_flow_time = df_edd['Flow Time (Waktu Alir)'].sum()
        total_tardiness = df_edd['Tardiness (Keterlambatan)'].sum()
        max_tardiness = df_edd['Tardiness (Keterlambatan)'].max()
        job_count = len(df_edd)
        
        avg_flow_time = total_flow_time / job_count if job_count > 0 else 0
        avg_tardiness = total_tardiness / job_count if job_count > 0 else 0
        
        # Display Metric KPI Block Summary Cards
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Sequencing Performance Metrics Summary")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div style='background-color: #ffffff; padding: 14px; border-radius: 6px; border: 1px solid #e5dfcb; border-left: 4px solid #415a77;'>
                            <div style='color: #666666; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Average Flow Time</div>
                            <div style='font-size: 20px; font-weight: 700; color: #415a77; margin-top: 2px;'>{avg_flow_time:.2f} Days</div>
                            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div style='background-color: #ffffff; padding: 14px; border-radius: 6px; border: 1px solid #e5dfcb; border-left: 4px solid #2a9d8f;'>
                            <div style='color: #666666; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Average Tardiness</div>
                            <div style='font-size: 20px; font-weight: 700; color: #2a9d8f; margin-top: 2px;'>{avg_tardiness:.2f} Days</div>
                            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div style='background-color: #ffffff; padding: 14px; border-radius: 6px; border: 1px solid #e5dfcb; border-left: 4px solid #e9c46a;'>
                            <div style='color: #666666; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Maximum Tardiness</div>
                            <div style='font-size: 20px; font-weight: 700; color: #e9c46a; margin-top: 2px;'>{max_tardiness} Days</div>
                            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div style='background-color: #f4efdc; padding: 14px; border-radius: 6px; border: 1px solid #e5dfcb; border-left: 4px solid #6a0708;'>
                            <div style='color: #4a4a4a; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Jobs in System (Avg)</div>
                            <div style='font-size: 20px; font-weight: 700; color: #6a0708; margin-top: 2px;'>{(total_flow_time / df_edd['Processing Time (Days)'].sum()):.2f} Jobs</div>
                            </div>""", unsafe_allow_html=True)

    # ==========================================
    # 5. VISUALIZATION - PETA PENJADWALAN (GANTT CHART)
    # ==========================================
    st.markdown("---")
    st.header("Peta Penjadwalan & Linimasa Operasional (EDD Gantt Chart)")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#faf8f2')
    ax.set_facecolor('#faf8f2')
    
    y_labels = []
    colors_pool = ['#6a0708', '#415a77', '#2a9d8f', '#e9c46a', '#e76f51', '#264653', '#9b5de5', '#f15bb5', '#00bbf9', '#00f5d4']
    
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
                
                ax.broken_barh([(job_start, ontime_duration)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#333333', linewidth=1, alpha=0.95)
                ax.broken_barh([(due_date, tardy_duration)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#333333', linewidth=1, hatch='//', alpha=0.9)
            else:
                ax.broken_barh([(job_start, proc_time)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#333333', linewidth=1, hatch='//', alpha=0.9)
        else:
            ax.broken_barh([(job_start, proc_time)], (y_bottom, y_height), facecolors=bar_color, edgecolor='#333333', linewidth=1, alpha=0.95)
            
        ax.text(job_start + proc_time/2, y_bottom + y_height/2, f"{job_id}\n({proc_time} Hari)", 
                ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        
        ax.axvline(x=due_date, color='#b91c1c', linestyle='--', linewidth=1.2, alpha=0.7)
        ax.text(due_date + 0.2, y_top_edge + 0.4, f"DL: {due_date}", 
                color='#b91c1c', fontsize=11, fontweight='bold', ha='left', va='bottom')
        
        y_labels.append(job_id)
        
    max_horizon = max(accumulator + 2, df_edd['Due Date (Day Count)'].max() + 5)
    ax.set_xlabel('Horizon Waktu Produksi (Hari)', fontsize=10, fontweight='bold', color='#6a0708')
    ax.set_ylabel('Daftar Antrean Kerja (Job ID)', fontsize=10, fontweight='bold', color='#6a0708')
    
    ax.set_xticks(np.arange(0, max_horizon, 1))
    ax.set_xticklabels(np.arange(0, max_horizon, 1).astype(int), fontsize=8)
    
    ax.set_yticks([i*10 + 5 for i in range(len(df_edd_reversed))])
    ax.set_yticklabels(y_labels, fontsize=9, fontweight='bold')
    ax.set_xlim(0, max_horizon)
    ax.set_ylim(0, len(df_edd_reversed)*10 + 9)
    ax.grid(True, linestyle=':', alpha=0.6, axis='x')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Analisis berada tepat di bawah peta penjadwalan
    st.markdown("### Analisis Peta Operasional")
    c_info, c_desc = st.columns([1, 2])
    with c_info:
        st.info(f"💡 **Urutan Eksekusi Mesin Tunggal:** \n**{' ➔ '.join(df_edd['Job ID'].tolist())}**")
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
    st.subheader("Management Reporting Layer")
    
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
