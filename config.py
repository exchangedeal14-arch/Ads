import os

# ==========================================
# BIXXU CLOUD SYSTEM - ENVIRONMENT OVERRIDES
# ==========================================

# Railway automatically injects these strings from the environment panel
BOT_TOKEN = os.getenv("BOT_TOKEN", "8791670002:AAHU8ZuKlzPorH9qLe7PqbWhc2sHu_IUu0k")
OWNER_ID = int(os.getenv("OWNER_ID", 8864002775))

# Parsing comma-separated channel lists dynamically from system environments
RAW_CHANNELS = os.getenv("REQUIRED_CHANNELS", "@bixxu,@bixxuchats")
REQUIRED_CHANNELS = [ch.strip() for ch in RAW_CHANNELS.split(",")]
