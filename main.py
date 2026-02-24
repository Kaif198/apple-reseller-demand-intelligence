import os
import sys
import streamlit.web.cli as stcli

def main():
    """
    Entry point for Railpack/deployment platforms.
    Railpack looks for main.py in the root and runs `python main.py`.
    This script programmatically launches our Streamlit application.
    """
    port = os.environ.get("PORT", "8501")
    sys.argv = [
        "streamlit",
        "run",
        "app/streamlit_app.py",
        "--server.port",
        port,
        "--server.address",
        "0.0.0.0"
    ]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
