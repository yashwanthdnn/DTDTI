@echo off
title H&N Punjabi Food Junction - Streamlit App
echo ========================================================
echo  Starting H&N Punjabi Food Junction Streamlit App...
echo ========================================================
echo.
python -m pip install -r requirements.txt
echo.
echo Launching Streamlit on http://localhost:8501 ...
python -m streamlit run streamlit_app.py
pause
