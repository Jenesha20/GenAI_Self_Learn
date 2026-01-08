# run.py
import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    # Set the working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()