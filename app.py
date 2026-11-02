"""
Main application entrypoint for Streamlit Cloud deployment.
Loads and executes streamlit_app.py seamlessly.
"""
import runpy
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(current_dir, "streamlit_app.py")
runpy.run_path(app_path, run_name="__main__")
