import streamlit as st
import pandas as pd
from datetime import datetime
import io
import chardet
 
st.title("数据规范处理平台")

# User inputs for file name
user_name = st.text_input("Enter your name")
date_input = st.text_input("Enter date (yyyymmdd)", datetime.now().strftime("%Y%m%d"))
material = st.text_input("Enter positive electrode material")
remark = st.text_input("Enter remarks")
batterynumber = st.text_input("Enter battery number")
file_base_name = f"{user_name}_{date_input}_{material}_{remark}_TestData{batterynumber}"

# Desired column order
desired_order = ["Cycle number", "Test time", "Step time", "Step number",
                 "Battery state", "Current/A", "Voltage/V", "System time", "Capacity/Ah"]

# File type selection
file_type_selection = st.radio("Select file type", ("蓝电高精度通道", "蓝电普通精度通道"))
format_choice = st.radio("选择下载格式", ('CSV', 'TXT'))
# Function to reorder columns

def keep_and_reorder_columns(dataframe, column_order):
    # Keep only columns that are in both the dataframe and the desired column order
    columns_to_keep = [col for col in column_order if col in dataframe.columns]
    # Reorder and return the dataframe with only the desired columns
    return dataframe[columns_to_keep]


if file_type_selection == "蓝电高精度通道":
    uploaded_files = st.file_uploader("Choose an Excel or txt file", type=['xlsx','txt'], accept_multiple_files=True)
    if uploaded_files:
        for i, uploaded_file in enumerate(uploaded_files):
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                keywords_to_replace = {
                "静置": "R",
                "恒流充电": "CCC",
                "恒压充电": "CVC",
                "恒流放电": "CCD",
                "恒压放电": "CVD",
                }
                df.replace(keywords_to_replace, inplace=True)
                column_name_mapping = {
                "循环序号": "Cycle number",
                "工步序号": "Step number",
                "工作模式": "Battery state",
                "步骤时间": "Step time",
                "测试时间": "Test time",
                "电压/V": "Voltage/V",
                "电流/A": "Current/A",
                "容量/Ah": "Capacity/Ah",
                "系统时间": "System time"
                }
                df.rename(columns=column_name_mapping, inplace=True)
                df = keep_and_reorder_columns(df, desired_order)

                #df.to_csv(f'processed_{2}.txt', index=False, sep='\t')

            elif uploaded_file.name.endswith('.txt'):
                df = pd.read_csv(uploaded_file, sep='\t', encoding='ANSI')
                keywords_to_replace = {
                "静置": "R",
                "恒流充电": "CCC",
                "恒压充电": "CVC",
                "恒流放电": "CCD",
                "恒压放电": "CVD",
                }
                df.replace(keywords_to_replace, inplace=True)
                column_name_mapping = {
                "循环序号": "Cycle number",
                "工步序号": "Step number",
                "工作模式": "Battery state",
                "步骤时间": "Step time",
                "测试时间": "Test time",
                "电压/V": "Voltage/V",
                "电流/A": "Current/A",
                "容量/Ah": "Capacity/Ah",
                "系统时间": "System time"
                }
                df.rename(columns=column_name_mapping, inplace=True)
                df = keep_and_reorder_columns(df, desired_order)

            download_button_key = f"download_button_{i}_{file_base_name}"    
            if format_choice == 'CSV':
                        #df.to_csv(f'{file_base_name}.csv', index=False)
                        to_download = df.to_csv(index=False).encode('utf-8')
                        new_file_name = f'{file_base_name}.csv'
                        mime_type = 'text/csv'
            elif format_choice == 'TXT':
                       # df.to_csv(f'{file_base_name}.txt', index=False, sep='\t')
                        to_download = df.to_csv(index=False, sep='\t') .encode('utf-8')
                        new_file_name = f'{file_base_name}.txt'
                        mime_type = 'text/plain'
            st.download_button(label=f"Download modified_{uploaded_file.name}", data=to_download, file_name=new_file_name, mime=mime_type,
                               key=download_button_key)

    
            

elif file_type_selection == "蓝电普通精度通道":  
    uploaded_files = st.file_uploader("Choose an Excel or txt file", type=['xlsx','txt'],accept_multiple_files=True)
    if uploaded_files:
        for i,uploaded_file in enumerate(uploaded_files):
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                column_name_mapping = {
                "循环序号": "Cycle number",
                "工步序号": "Step number",
                "工步状态": "Battery state",
                "步骤时间": "Step time",
                "测试时间": "Test time",
                "电压/V": "Voltage/V",
                "电流/A": "Current/A",
                "容量/Ah": "Capacity/Ah",
                "系统时间": "System time"
                }
                df.rename(columns=column_name_mapping, inplace=True)
                df = keep_and_reorder_columns(df, desired_order)
                #df.to_csv(f'processed_{1}', index=False)

            elif uploaded_file.name.endswith('.txt'):
                df = pd.read_csv(uploaded_file, sep='\t', encoding='ANSI')
                column_name_mapping = {
                "循环序号": "Cycle number",
                "工步序号": "Step number",
                "工步状态": "Battery state",
                "步骤时间": "Step time",
                "测试时间": "Test time",
                "电压/V": "Voltage/V",
                "电流/A": "Current/A",
                "容量/Ah": "Capacity/Ah",
                "系统时间": "System time"
                }
                df.rename(columns=column_name_mapping, inplace=True)
                df = keep_and_reorder_columns(df, desired_order)
                #df.to_csv(f'processed_{1}.txt', index=False, sep='\t')

            download_button_key = f"download_button_{i}_{file_base_name}" 
            if format_choice == 'CSV':
                        #df.to_csv(f'{file_base_name}.csv', index=False)
                        to_download = df.to_csv(index=False).encode('utf-8')
                        new_file_name = f'{file_base_name}.csv'
                        mime_type = 'text/csv'
            elif format_choice == 'TXT':
                       # df.to_csv(f'{file_base_name}.txt', index=False, sep='\t')
                        to_download = df.to_csv(index=False, sep='\t') .encode('utf-8')
                        new_file_name = f'{file_base_name}.txt'
                        mime_type = 'text/plain'
            st.download_button(label=f"Download modified_{uploaded_file.name}", data=to_download, file_name=new_file_name, mime=mime_type,
                               key=download_button_key)


# def prepare_download_button(df, file_base_name):
#     format_choice = st.radio("Choose format for download", ('CSV', 'TXT'))

#     if format_choice == 'CSV':
#         to_download = df.to_csv(index=False).encode('utf-8')
#         file_name = f'{file_base_name}.csv'
#         mime_type = 'text/csv'
#     elif format_choice == 'TXT':
#         # 对于TXT格式，这里可以根据需要调整，例如使用df.to_string()等
#         # to_download = df_object.to_csv('xgboost.txt', sep='\t', index=False)
#         # file_name = f'{file_base_name}.txt'
#         # mime_type = 'text/plain'
#         to_download = df.to_csv(index=False, sep='\t').encode('utf-8')
#         file_name = f'{file_base_name}.txt'
#         mime_type = 'text/plain'

#     st.download_button(label="Download File", data=to_download, file_name=file_name, mime=mime_type)


#检查是否有DataFrame可供下载
# if st.button("Prepare Download"):
#     if 'df' in locals():
#         file_base_name = f"{user_name}_{date_input}_{material}_{remark}_TestData{batterynumber}"
#         prepare_download_button(df, file_base_name)
#     else:
#         st.error("Please upload a file to process.")

##streamlit run naming_standard.py

