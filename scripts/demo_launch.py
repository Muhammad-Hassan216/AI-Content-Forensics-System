"""Launch Streamlit app and open browser (single command for judges).
Runs Streamlit in a subprocess and opens the browser to the local URL.
"""
import subprocess
import webbrowser
import time
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    cmd = ["python", "-m", "streamlit", "run", "app.py", "--server.headless", "true"]
    env = os.environ.copy()
    p = subprocess.Popen(cmd, cwd=ROOT, env=env)
    print('Started Streamlit (pid=%s). Waiting for server...' % p.pid)
    # wait a bit then open browser
    time.sleep(3)
    webbrowser.open('http://localhost:8501')
    try:
        p.wait()
    except KeyboardInterrupt:
        p.terminate()

if __name__ == '__main__':
    main()
