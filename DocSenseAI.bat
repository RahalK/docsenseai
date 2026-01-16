@echo off
cd /d "%~dp0"
call conda activate docsenseai
streamlit run app.py
