"""Backward-compatible Streamlit entry point.

New deployments should use ``streamlit_demo/app.py``. This wrapper preserves older
bookmarks and local commands while sharing the hardened dashboard implementation.
"""

from streamlit_app import main


if __name__ == "__main__":
    main()
