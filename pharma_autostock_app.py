
import streamlit as st
import pandas as pd

st.title('PharmaAutoStock - Automated Reorder System')

st.write("""
Upload your pharmacy inventory file (CSV or Excel). The file should have the following columns:
- Product
- Current_Stock
- Average_Daily_Sales
- Supplier_Lead_Time_Days
- Target_Coverage_Days
- Minimum_Stock_Level
""")

uploaded_file = st.file_uploader("Upload Inventory File", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df['Projected_Stock_After_Lead_Time'] = df['Current_Stock'] - (df['Average_Daily_Sales'] * df['Supplier_Lead_Time_Days'])
    df['Reorder_Quantity'] = ((df['Average_Daily_Sales'] * df['Target_Coverage_Days']) - df['Current_Stock']).clip(lower=0).round()

    reorder_df = df[df['Reorder_Quantity'] > 0]

    st.subheader("Reorder Proposal")
    st.dataframe(reorder_df)

    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    excel_data = convert_df(reorder_df)

    st.download_button(
        label="Download Reorder Proposal as Excel",
        data=excel_data,
        file_name='Reorder_Proposal.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
