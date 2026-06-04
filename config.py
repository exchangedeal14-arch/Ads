import os

# ==========================================
# BIXXU CLOUD SYSTEM - PRODUCTION REGISTRY
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8791670002:AAHU8ZuKlzPorH9qLe7PqbWhc2sHu_IUu0k")
OWNER_ID = int(os.getenv("OWNER_ID", 8864002775))

RAW_CHANNELS = os.getenv("REQUIRED_CHANNELS", "@bixxu,@bixxuchats")
REQUIRED_CHANNELS = [ch.strip() for ch in RAW_CHANNELS.split(",")]
