"""
Configuration loader.
Reads BOT_TOKEN from the environment (set it as a Replit Secret
or export it in your shell before running).
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on environment variables

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is not set. "
        "Add it as a Replit Secret (key: BOT_TOKEN) or in a .env file."
    )
