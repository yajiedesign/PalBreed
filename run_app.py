import sys

import streamlit.web.cli as stcli

if __name__ == '__main__':
    app_path = "app.py"
    sys.argv = ["streamlit", "run", app_path]

    sys.exit(stcli.main())
