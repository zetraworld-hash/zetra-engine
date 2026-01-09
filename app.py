import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="ZETRA | Kuwait Customs Engine", layout="wide")
st.title("🇰🇼 ZETRA: 2026 Manifest Engine")
st.subheader("Professional Bulk Clearance for J&T Express")

# 2. File Upload
uploaded_file = st.file_file_uploader("Upload J&T China Manifest (Excel/CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    # Read the data
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    
    st.write("### Original Data (From China)")
    st.dataframe(df.head()) # Show first 5 rows

    # 3. The "Cleaning" Logic
    # We create a button to start the AI cleaning
    if st.button("🚀 Clean & Fix for Kuwait Bayan"):
        
        # LOGIC 1: Fix HS Codes to 12 Digits
        # If code is 851713, it becomes 8517.13.00.00.00
        def fix_code(code):
            code_str = str(code).replace('.', '')
            if len(code_str) < 12:
                # Add zeros to make it 12 digits
                code_str = code_str.ljust(12, '0')
            # Format with dots: XXXX.XX.XX.XX.XX
            return f"{code_str[:4]}.{code_str[4:6]}.{code_str[6:8]}.{code_str[8:10]}.{code_str[10:12]}"

        df['12_Digit_HS_Code'] = df['HS_Code'].apply(fix_code)

        # LOGIC 2: Duty Calculation
        df['Duty_5_Percent'] = df['Value'] * 0.05

        # (Note: In the full version, we connect the AI here for Arabic Translation)
        # For now, we show the processed result
        st.success("Clean-up Complete!")
        st.write("### Cleaned Data (2026 Ready)")
        st.dataframe(df)

        # 4. The Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Perfect Manifest for Bayan",
            data=csv,
            file_name='ZETRA_Ready_Manifest.csv',
            mime='text/csv',
        )
