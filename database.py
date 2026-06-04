import sqlite3

DB_PATH = "bixxu_platform.db"

def init_db():
    """Initializes the structural core database and sets up application schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. USER CAMPAIGN MASTER REGISTRY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            is_premium INTEGER DEFAULT 0,
            connected_accounts INTEGER DEFAULT 0,
            interval_delay INTEGER DEFAULT 600,
            engine_status TEXT DEFAULT 'IDLE / PAUSED ⏸️',
            ad_message TEXT DEFAULT 'NOT CONFIGURED 🔴'
        )
    """)
    
    # 2. SYSTEM CONTROL VARIABLE REGISTRY (For Owner Configurations)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            config_id INTEGER PRIMARY KEY AUTOINCREMENT,
            upi_id TEXT DEFAULT 'bixxu@upi',
            total_broadcasts INTEGER DEFAULT 0
        )
    """)
    
    # Seed default system configurations if table is empty
    cursor.execute("SELECT COUNT(*) FROM system_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO system_config (upi_id, total_broadcasts) VALUES ('bixxu@upi', 0)")
        
    conn.commit()
    conn.close()
    print("[DATABASE ENGINE LOG] Schema synchronization complete. Storage operational.")

# ==========================================
# 👤 CLIENT LEVEL QUERIES & COMMAND PIPELINES
# ==========================================

def get_user(chat_id, default_name="User"):
    """Fetches full transactional profile state of an individual user node."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, name, is_premium, connected_accounts, interval_delay, engine_status, ad_message FROM users WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    
    if not row:
        # Auto-register missing terminal entities
        cursor.execute("INSERT INTO users (chat_id, name) VALUES (?, ?)", (chat_id, default_name))
        conn.commit()
        cursor.execute("SELECT chat_id, name, is_premium, connected_accounts, interval_delay, engine_status, ad_message FROM users WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()
        
    conn.close()
    return {
        "chat_id": row[0], "name": row[1], "is_premium": bool(row[2]),
        "connected_accounts": row[3], "interval": row[4], "status": row[5], "ad_msg": row[6]
    }

def update_user_config(chat_id, column, value):
    """Dynamically updates unique configuration constraints inside a client profile."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Direct formatting safe due to parameterized query routing
    cursor.execute(f"UPDATE users SET {column} = ? WHERE chat_id = ?", (value, chat_id))
    conn.commit()
    conn.close()

def fetch_total_users_count():
    """Returns analytics data mapping absolute metrics of registered entities."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(is_premium) FROM users")
    metrics = cursor.fetchone()
    conn.close()
    return {"total_users": metrics[0], "premium_users": metrics[1] if metrics[1] else 0}

def fetch_all_user_ids():
    """Extracts every registered unique identity token for global broadcasting networks."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ids

# ==========================================
# 👑 ROOT ADMIN PRIVILEGED OVERRIDE COMMANDS
# ==========================================

def get_system_upi():
    """Pulls current structural payment gateway profile target."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT upi_id FROM system_config WHERE config_id = 1")
    upi = cursor.fetchone()[0]
    conn.close()
    return upi

def set_system_upi(new_upi):
    """Mutates global infrastructure properties mapping target transaction endpoints."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE system_config SET upi_id = ? WHERE config_id = 1", (new_upi,))
    conn.commit()
    conn.close()

def clear_volatile_cache():
    """Purges user data frameworks, resetting backend instances to ground evaluation rules."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

# Auto-execute schema mapping verification sequence upon initialization
init_db()
  
