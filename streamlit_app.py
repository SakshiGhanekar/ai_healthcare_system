"""
Streamlit Cloud Entry Point
===========================
This file acts as the primary entry point for Streamlit Community Cloud. 
It imports and runs the main application from the frontend package.
"""
import sys
import os

# Add the current directory to the path so we can find the 'frontend' package
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the main runner from your frontend
from frontend.main import main

if __name__ == "__main__":
    main()
