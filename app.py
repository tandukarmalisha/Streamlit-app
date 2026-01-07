import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import extras
import os
from dotenv import load_dotenv
# Ensure logic.py is in the same folder
from logic import format_name, clean_mobile, split_email_data 

load_dotenv()

st.set_page_config(page_title="Data Pro Importer", page_icon="📥")
st.title("🚀 Professional Batch Importer")

# --- DATABASE CONNECTION HELPER ---
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT", "5432") # Default to 5432 if port is missing
    )

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # --- ADD THIS LINE ---
    df.columns = df.columns.str.strip().str.lower()
    
    # --- DEBUG SECTION: SEE ACTUAL COLUMN NAMES ---
    st.info(f"📂 File contains {len(df)} rows.")
    st.write("### 🔍 Detected Columns in Excel:")
    st.code(list(df.columns)) # This helps you see if 'name' is actually 'Name'
    
    st.write("### 📄 Data Preview")
    st.dataframe(df.head(3))

    batch_size = st.select_slider("Select Batch Size", options=[100, 500, 1000, 2000], value=1000)

    if st.button("⚡ Start Migration"):
        user_error_report = []
        batch_data = []
        total_inserted = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        error_log_container = st.container() # For showing live errors
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            for index, row in df.iterrows():
                try:
                    # APPLY YOUR CLEANING LOGIC 
                    # Note: .get('column_name') is case-sensitive!
                    raw_name = row.get('name') or row.get('Name')
                    raw_mob = row.get('mobile number') or row.get('Mobile Number') or row.get('Phone')
                    raw_email = row.get('email') or row.get('Email')
                    raw_addr = row.get('address') or row.get('Address', '')

                    # Run cleaning functions from logic.py
                    name = format_name(raw_name)
                    mob = clean_mobile(raw_mob)
                    user, domain = split_email_data(raw_email)
                    addr = str(raw_addr).strip().upper()

                    batch_data.append((name, addr, mob, f"{user}@{domain}", domain))

                    # BATCH INSERT LOGIC
                    if len(batch_data) >= batch_size:
                        extras.execute_values(
                            cur, 
                            "INSERT INTO streamlit_import (name, address, mobile_number, email, domain) VALUES %s", 
                            batch_data
                        )
                        conn.commit()
                        total_inserted += len(batch_data)
                        
                        # UI Updates
                        progress = (index + 1) / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f"Moving batch... {total_inserted} rows saved.")
                        batch_data = []

                except Exception as row_err:
                    # DISPLAY ERROR IMMEDIATELY IN THE UI
                    err_msg = f"Row {index+2}: {str(row_err)}"
                    user_error_report.append(err_msg)
                    with error_log_container:
                        st.warning(err_msg)

            # --- FINAL CLEANUP (For the last few rows) ---
            if batch_data:
                extras.execute_values(
                    cur, 
                    "INSERT INTO streamlit_import (name, address, mobile_number, email, domain) VALUES %s", 
                    batch_data
                )
                conn.commit()
                total_inserted += len(batch_data)

            st.success(f"🎊 Finished! Successfully imported {total_inserted} rows.")
            progress_bar.progress(1.0)

        except Exception as db_err:
            st.error("### 🛑 Critical Database Error")
            st.exception(db_err) # Shows the full traceback in the UI
        finally:
            if 'conn' in locals():
                cur.close()
                conn.close()

        # Final Summary Report
        if user_error_report:
            with st.expander("📝 Full Error Summary Report"):
                for error in user_error_report:
                    st.write(error)
