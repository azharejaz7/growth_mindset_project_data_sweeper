# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO 
import openpyxl

# Set up Streamlit app
st.set_page_config(page_title="📀 Data Sweeper", layout="wide")
st.title("📀 Data Sweeper")
st.write("Transform your files between CSV and Excel Format with built-in data and visualization")

# File uploader
uploaded_files = st.file_uploader("Upload Your File (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:  # Ensures at least one file is uploaded
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file into a DataFrame
        if file_ext == ".csv":
            df = pd.read_csv(file, encoding="cp1252")
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        # sotre dataframe in session to presist updated data
        if "df" not in st.session_state:
            st.session_state.df =df
            
        # Display file details
        st.write(f"*File Name:* {file.name}")
        st.write(f"*File Size:* {file.size / 1024:.2f} KB")

        # Show file preview
        st.write("Current Preview of the DataFrame:")
        st.dataframe(df.head(20))

        # Data Cleaning Options
        st.subheader(f"Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates From {file.name}"):
                    st.session_state.df.drop_duplicates(inplace=True)
                    st.write("Removed Duplicates")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns
                    st.session_state.df[numeric_cols] = st.session_state.df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled")
                    
            st.write("Updated Preview of the DataFrame:")        
            st.write(st.session_state.df)           
        # Choose Specific Columns to convert or Keep
        st.header("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #create come visualization

        st.header("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


        # Convert the file -> CSV to Excel 
        st.header("🔄 Conversion Options")
        conversion_type =st.radio(f"Convert {file.name} to:",["CSV","Excel"],key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer  = BytesIO()
            if conversion_type == "CSV":
                st.session_state.df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"
            
            
            elif conversion_type == "Excel":
                st.session_state.df.to_excel(buffer , index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type ="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name = file_name,
                mime=mime_type
            )
            
            st.success("🎉 Files Proceeds!")