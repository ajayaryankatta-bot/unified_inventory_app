"""
Unified Inventory Management System - Professional Enterprise Dashboard (UIMS v2.8)
Polished High-Performance UI/UX Dark-Mode Theme with Shining Navigation Boxes
"""
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Unified Inventory Management System (UIMS)",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Dark Theme CSS Styling with Shining Boxes & Custom Nav Cards
st.markdown("""
    <style>
        /* Global Theme */
        .stApp { background-color: #0b0f19; color: #f0f6fc; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        
        /* Sidebar Polish */
        [data-testid="stSidebar"] { 
            background-color: #0d1322; 
            border-right: 1px solid #1e293b; 
        }
        
        /* Executive Metric & Nav Cards */
        .metric-card {
            background: linear-gradient(135deg, #131b2e 0%, #172138 100%);
            border: 1px solid #1e293b;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            margin-bottom: 12px;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            border-color: #388bfd;
            box-shadow: 0 8px 28px rgba(56, 139, 253, 0.15);
            transform: translateY(-2px);
        }

        /* ✨ Shining / Glowing Animation (No Blinking) */
        @keyframes shine {
            0% { box-shadow: 0 0 5px rgba(56, 139, 253, 0.15); border-color: #1e293b; }
            50% { box-shadow: 0 0 22px rgba(56, 139, 253, 0.5), inset 0 0 10px rgba(56, 139, 253, 0.15); border-color: #3b82f6; }
            100% { box-shadow: 0 0 5px rgba(56, 139, 253, 0.15); border-color: #1e293b; }
        }
        .shine-card { animation: shine 3.5s infinite ease-in-out; }

        /* Subtle indicator blink for live status ONLY */
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        .blink-element { animation: blink 1.5s infinite ease-in-out; }

        /* Typography & Headers */
        h1, h2, h3, h4 { color: #f8fafc !important; font-weight: 600; letter-spacing: -0.01em; }
        
        /* Dataframes & Tables */
        [data-testid="stDataFrame"] { 
            border: 1px solid #1e293b; 
            border-radius: 10px; 
            background-color: #111827; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* Sidebar Live Status Badge */
        .sidebar-status {
            position: fixed;
            bottom: 20px;
            left: 20px;
            font-size: 13px;
            color: #94a3b8;
            background-color: #0f172a;
            padding: 10px 14px;
            border-radius: 8px;
            border: 1px solid #1e293b;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }

        /* Buttons Polish */
        .stButton button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            padding: 8px 16px;
            transition: background-color 0.2s ease;
        }
        .stButton button:hover { background-color: #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# App Header Bar
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.title("📦 Unified Inventory Management System")
    st.caption("Enterprise Multi-Channel Stock Orchestration Engine | Seed: 20261022")
with top_col2:
    st.markdown("👤 **Deployed Eng** `FD`")

st.markdown("---")

# ==========================================
# NAVIGATION SIDEBAR (SHINING BOXES / CARDS)
# ==========================================
st.sidebar.markdown("### 🧭 NAVIGATION VIEWS")

views_dict = {
    "1. Inventory Balances & Stock Levels": "📦",
    "2. 1M Movement Ledger Explorer": "📈",
    "3. Ground Truth Anomalies Feed": "⚠️",
    "4. In-Transit Shipments": "🚚",
    "5. Multi-Channel Orders & Allocation": "🛒"
}

# Initialize Session State for active view if not present
if "selected_nav_view" not in st.session_state:
    st.session_state.selected_nav_view = list(views_dict.keys())[0]

# Render shining/interactive box buttons in sidebar
for view_name, icon in views_dict.items():
    is_active = (st.session_state.selected_nav_view == view_name)
    btn_style = "border: 2px solid #3b82f6; background-color: #172138;" if is_active else "border: 1px solid #1e293b; background-color: #111827;"
    
    if st.sidebar.button(f"{icon} {view_name}", key=f"nav_btn_{view_name}", use_container_width=True):
        st.session_state.selected_nav_view = view_name
        st.rerun()

selected_view = st.session_state.selected_nav_view

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div class="sidebar-status">
        <span class="blink-element" style="color: #22c55e; font-size: 16px;">●</span> <b>System Live</b><br>
        Last Sync: Just now
    </div>
""", unsafe_allow_html=True)

# Helper function to load data from data/ directory
def load_csv_data(file_name):
    path = os.path.join("data", file_name)
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# Helper function for sparkline chart
def create_sparkline(values, color="#3b82f6"):
    fig = go.Figure(go.Scatter(
        y=values,
        mode='lines',
        line=dict(color=color, width=2.5),
        hoverinfo='none'
    ))
    fig.update_layout(
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        margin=dict(t=0, b=0, l=0, r=0),
        height=32,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# ==========================================
# 1. INVENTORY BALANCES & STOCK LEVELS TABLE
# ==========================================
if selected_view == "1. Inventory Balances & Stock Levels":
    st.subheader("1. Live Inventory Balances & Stock Levels (Primary View)")
    st.markdown("Real-time valuation and Available-to-Promise (ATP) calculations across enterprise nodes.")
    
    df = load_csv_data("inventory_balances.csv")
    
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card shine-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">TOTAL CATALOG SKUS ✨</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #f8fafc;">{df['SKU Code'].nunique():,}</h3>
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(create_sparkline([2010, 2030, 2050, 2040, 2080, 2100, df['SKU Code'].nunique()], "#3b82f6"), use_container_width=True, config={'displayModeBar': False})
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">PHYSICAL ON-HAND UNITS</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #f8fafc;">{df['On-Hand Stock'].sum():,}</h3>
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(create_sparkline([22000, 23100, 22800, 24000, 23900, 24200, df['On-Hand Stock'].sum() % 25000], "#3b82f6"), use_container_width=True, config={'displayModeBar': False})
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">COMMITTED RESERVED</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #f8fafc;">{df['Reserved Stock'].sum():,}</h3>
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(create_sparkline([800, 850, 820, 890, 910, 940, df['Reserved Stock'].sum()], "#3b82f6"), use_container_width=True, config={'displayModeBar': False})
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">NET AVAILABLE (ATP)</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #22c55e;">{df['ATP'].sum():,}</h3>
                </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(create_sparkline([1500, 1550, 1600, 1580, 1620, 1650, df['ATP'].sum() % 2000], "#22c55e"), use_container_width=True, config={'displayModeBar': False})

        st.markdown("---")
        
        search_col, filter_col = st.columns([2, 1])
        with search_col:
            search_q = st.text_input("🔍 Search by SKU Code", "").strip().upper()
        with filter_col:
            loc_type = st.selectbox("Location Type Filter", ["All"] + list(df["Location Type"].unique()))
            
        filtered_df = df.copy()
        if search_q:
            filtered_df = filtered_df[filtered_df["SKU Code"].str.contains(search_q)]
        if loc_type != "All":
            filtered_df = filtered_df[filtered_df["Location Type"] == loc_type]

        st.dataframe(filtered_df, use_container_width=True, height=350, hide_index=True)
        
        st.markdown("### 📊 Stock Balance Distribution by Location")
        chart_data = filtered_df.groupby("Location Name")[["On-Hand Stock", "ATP", "Reserved Stock"]].sum()
        st.bar_chart(chart_data)
        
        st.download_button("📥 Download Balances CSV", filtered_df.to_csv(index=False), "inventory_balances.csv", "text/csv")
    else:
        st.warning("Data file `data/inventory_balances.csv` not found. Please run `python generate_csv_data.py` first.")

# ==========================================
# 2. 1M MOVEMENT LEDGER TABLE
# ==========================================
elif selected_view == "2. 1M Movement Ledger Explorer":
    st.subheader("2. Immutable Movement Ledger Explorer (Audit Log View)")
    st.markdown("Auditable inventory transaction log tracking 1,000,000 ledger movements across 6 transaction types.")
    
    df = load_csv_data("movement_ledger.csv")
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="metric-card shine-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">TOTAL LEDGER MOVEMENTS ✨</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #f8fafc;">1,000,000</h3>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">NET POSITIVE INBOUND DELTA</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #22c55e;">+{df[df['Quantity Delta'] > 0]['Quantity Delta'].sum():,}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">NET OUTBOUND SALES DELTA</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #ef4444;">{df[df['Quantity Delta'] < 0]['Quantity Delta'].sum():,}</h3>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        m_type_filter = st.selectbox("Filter by Movement Type", ["All"] + list(df["Movement Type"].unique()))
        filtered_df = df if m_type_filter == "All" else df[df["Movement Type"] == m_type_filter]
        
        st.dataframe(filtered_df, use_container_width=True, height=350, hide_index=True)
        
        st.markdown("### 📊 Ledger Movement Volume by Transaction Type")
        m_counts = filtered_df["Movement Type"].value_counts()
        st.bar_chart(m_counts)
        
        st.download_button("📥 Download Ledger CSV", filtered_df.to_csv(index=False), "movement_ledger.csv", "text/csv")
    else:
        st.warning("Data file `data/movement_ledger.csv` not found. Please run `python generate_csv_data.py` first.")

# ==========================================
# 3. GROUND TRUTH ANOMALIES TABLE
# ==========================================
elif selected_view == "3. Ground Truth Anomalies Feed":
    st.subheader("3. Ground Truth Anomaly Tracking Feed")
    st.markdown("Isolated edge-case anomalies (oversells, expired reservations, dual-counting flags) loaded from audit reports.")
    
    df = load_csv_data("ground_truth_anomalies.csv")
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">TOTAL DETECTED ANOMALIES</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #f8fafc;">{len(df)}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card" style="border-color: #ef4444;">
                    <span style="font-size: 12px; color: #ef4444; font-weight: 700; letter-spacing: 0.05em;">⚠️ HIGH SEVERITY ISSUES</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #ef4444;">{len(df[df['Severity'] == 'HIGH'])}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">UNRESOLVED ALERTS</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #eab308;">{len(df[df['Status'] == 'UNRESOLVED'])}</h3>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        st.dataframe(df, use_container_width=True, height=350, hide_index=True)
        
        st.markdown("### 📊 Anomaly Types Distribution by Severity")
        st.bar_chart(df.groupby(["Anomaly Type", "Severity"]).size().unstack(fill_value=0))
        
        st.download_button("📥 Download Anomalies CSV", df.to_csv(index=False), "ground_truth_anomalies.csv", "text/csv")
    else:
        st.warning("Data file `data/ground_truth_anomalies.csv` not found. Please run `python generate_csv_data.py` first.")

# ==========================================
# 4. IN-TRANSIT SHIPMENTS TABLE
# ==========================================
elif selected_view == "4. In-Transit Shipments":
    st.subheader("4. Inter-Facility In-Transit Shipments Table")
    st.markdown("Live dispatch monitoring for inventory movements between warehouses and fulfillment hubs.")
    
    df = load_csv_data("in_transit_shipments.csv")
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">ACTIVE SHIPMENTS</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #f8fafc;">{len(df)}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card shine-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">TOTAL IN-TRANSIT UNITS ✨</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #f8fafc;">{df['Transfer Quantity'].sum():,}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">IN-TRANSIT STATUS</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 24px; color: #22c55e;">{len(df[df['Status'] == 'IN_TRANSIT'])}</h3>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        st.dataframe(df, use_container_width=True, height=350, hide_index=True)
        
        st.markdown("### 📊 Shipment Status Breakdown")
        st.bar_chart(df["Status"].value_counts())
        
        st.download_button("📥 Download Shipments CSV", df.to_csv(index=False), "in_transit_shipments.csv", "text/csv")
    else:
        st.warning("Data file `data/in_transit_shipments.csv` not found. Please run `python generate_csv_data.py` first.")

# ==========================================
# 5. MULTI-CHANNEL ORDERS TABLE
# ==========================================
elif selected_view == "5. Multi-Channel Orders & Allocation":
    st.subheader("5. Multi-Channel Orders & Stock Allocation Table")
    st.markdown("Omnichannel customer orders synchronized across Web, Mobile, B2B, and Marketplace platforms.")
    
    df = load_csv_data("multi_channel_orders.csv")
    
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">TOTAL EVALUATED ORDERS</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 22px; color: #f8fafc;">{len(df):,}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">ALLOCATED & RESERVED</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 22px; color: #22c55e;">{len(df[df['Order Status'] == 'ALLOCATED'])}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">BACKORDERED (ATP=0)</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 22px; color: #ef4444;">{len(df[df['Order Status'] == 'BACKORDERED'])}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="metric-card shine-card">
                    <span style="font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 0.05em;">FULFILLED & SHIPPED ✨</span>
                    <h3 style="margin: 6px 0 6px 0; font-size: 22px; color: #3b82f6;">{len(df[df['Order Status'] == 'SHIPPED'])}</h3>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        st.dataframe(df, use_container_width=True, height=350, hide_index=True)
        
        st.markdown("### 📊 Order Volume by Sales Channel")
        st.bar_chart(df.groupby(["Channel", "Order Status"]).size().unstack(fill_value=0))
        
        st.download_button("📥 Download Orders CSV", df.to_csv(index=False), "multi_channel_orders.csv", "text/csv")
    else:
        st.warning("Data file `data/multi_channel_orders.csv` not found. Please run `python generate_csv_data.py` first.")