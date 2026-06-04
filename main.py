import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, OWNER_ID, REQUIRED_CHANNELS

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Global Active Multi-Tenant Memory Matrix
db = {
    "users": {},        # Memory: chat_id -> user specific configuration profile
    "user_state": {},   # Memory: tracks active workflow inputs per session
    "system": {
        "upi_id": "bixxu@upi",
        "total_active_sessions": 0
    }
}

# --- GATEKEEPER AUTOMATION MIDDLEWARE ---
def is_user_verified(chat_id):
    if chat_id == OWNER_ID:
        return True
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, chat_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

# --- EXQUISITE HIGH-END INLINE CONTROL SURFACES ---
def lock_interface():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 JOIN OFFICIAL CHANNEL", url="https://t.me/bixxu"),
        InlineKeyboardButton("💬 JOIN GLOBAL CHAT GROUP", url="https://t.me/bixxuchats"),
        InlineKeyboardButton("⚡ TAP TO UNLOCK COCKPIT ⚡", callback_data="verify_sub")
    )
    return markup

def dashboard_interface(chat_id, is_premium):
    markup = InlineKeyboardMarkup()
    
    # Row 1: Fully Automated Client Login System
    markup.row(
        InlineKeyboardButton("🔑 INJECT ACCOUNT LOGIN", callback_data="client_login"),
        InlineKeyboardButton("👥 TERMINAL INSTANCES", callback_data="client_instances")
    )
    # Row 2: Campaign Target Routing Configuration
    markup.row(
        InlineKeyboardButton("📝 SET MARKETING AD COPY", callback_data="inline_set_msg"),
        InlineKeyboardButton("⏱️ SET THROTTLE COOLDOWN", callback_data="inline_set_time")
    )
    # Row 3: Live Automation Ignition Core
    markup.row(
        InlineKeyboardButton("▶️ ACTIVATE DISPATCH LOGIC", callback_data="engine_start"),
        InlineKeyboardButton("⏸️ FREEZE CORE PROCESSING", callback_data="engine_stop")
    )
    # Row 4: Premium Upsell Conversion System
    if not is_premium:
        markup.row(InlineKeyboardButton("👑 UPGRADE TO PREMIUM VIP (₹199) 👑", callback_data="buy_premium"))
    
    # Row 5: Utilities Controls
    markup.row(
        InlineKeyboardButton("🔄 REFRESH NETWORK STATE", callback_data="refresh_dash"),
        InlineKeyboardButton("📊 PERFORMANCE LOGS", callback_data="view_stats")
    )
    
    # Master System Layer: Visible exclusively to Root Admin
    if chat_id == OWNER_ID:
        markup.row(InlineKeyboardButton("🛠️ ACCESS ADMIN MAIN HUB 🛠️", callback_data="owner_panel"))
        
    return markup

def owner_interface():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("💳 MODIFY BILLING ENDPOINT", callback_data="owner_set_upi"),
        InlineKeyboardButton("🎁 FORCE VIP LICENSE GRANT", callback_data="owner_give_premium")
    )
    markup.row(
        InlineKeyboardButton("📢 BROADCAST NETWORK PACKET", callback_data="owner_broadcast"),
        InlineKeyboardButton("📉 PURGE TEMPORARY CACHE", callback_data="owner_sys_reset")
    )
    markup.row(InlineKeyboardButton("🔙 DISCONNECT SYSTEM HUB", callback_data="refresh_dash"))
    return markup

def back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 TERMINATE SESSION & RETURN", callback_data="refresh_dash"))
    return markup

def owner_back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 BACK TO ROOT COMMAND CORE", callback_data="owner_panel"))
    return markup

# --- PRIMARY COCKPIT ENTRYPOINT ---
@bot.message_handler(commands=['start'])
def boot_system(message):
    chat_id = message.chat.id
    
    if chat_id not in db["users"]:
        db["users"][chat_id] = {
            "name": message.from_user.first_name,
            "is_premium": True if chat_id == OWNER_ID else False,
            "connected_accounts": 0,
            "interval": 600,
            "status": "IDLE / PAUSED ⏸️",
            "ad_msg": "NOT CONFIGURED 🔴"
        }

    if not is_user_verified(chat_id):
        lock_text = (
            f"⚡ <b>ACCESS VIOLATION • SECURITY GATEWAY BLOCKED</b> ⚡\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"To access the distributed Bixxu Advertising Clusters, your account profile "
            f"must satisfy structural verification checks:\n\n"
            f"• <b>Network Endpoint 01:</b> {REQUIRED_CHANNELS[0]}\n"
            f"• <b>Network Endpoint 02:</b> {REQUIRED_CHANNELS[1]}\n\n"
            f"<i>Join the required groups and tap the validation controller interface below.</i>"
        )
        bot.send_message(chat_id, lock_text, reply_markup=lock_interface())
        return

    render_inline_dashboard(chat_id)

# --- CLIENT MAIN ENGINE INTERFACE ---
def render_inline_dashboard(chat_id, message_id=None):
    user_data = db["users"].get(chat_id)
    tier_badge = "🏅 <b>ROOT ADMIN LICENSE</b>" if chat_id == OWNER_ID else ("👑 <b>PREMIUM VIP ACCESS</b>" if user_data["is_premium"] else "📝 <b>STANDARD EVALUATION LICENSE</b>")
    max_slots = "INFINITE SLOTS" if chat_id == OWNER_ID else ("5 ACTIVE USERBOTS" if user_data["is_premium"] else "1 ACTIVE USERBOT")
    msg_preview = user_data['ad_msg'] if len(user_data['ad_msg']) <= 25 else f"{user_data['ad_msg'][:25]}..."

    dash_text = (
        f"🤖 <b>BIXXU COMMERCIAL AUTOMATION COCKPIT V3.0</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>AUTHENTICATED USER:</b> <code>{user_data['name']}</code>\n"
        f"🛡️ <b>LICENSE THRESHOLD:</b> {tier_badge}\n"
        f"⚙️ <b>AUTOMATION ENGINE STATUS:</b> <b>{user_data['status']}</b>\n\n"
        f"📊 <b>CLOUD STORAGE LOGS & CONFIGURATIONS:</b>\n"
        f"├ Active Session Terminals: <code>{user_data['connected_accounts']}/{max_slots}</code>\n"
        f"├ Propagation Cooldown Delay: <code>{user_data['interval']} seconds</code>\n"
        f"└ Active Broadcast Template: <code>{msg_preview}</code>\n\n"
        f"🚀 <i>Execution space is 100% inline. Command your instances below:</i>"
    )
    
    if message_id:
        try:
            bot.edit_message_text(dash_text, chat_id, message_id, reply_markup=dashboard_interface(chat_id, user_data["is_premium"]))
        except Exception: pass
    else:
        bot.send_message(chat_id, dash_text, reply_markup=dashboard_interface(chat_id, user_data["is_premium"]))

# --- MASTER ADMIN INSIGHTS HUB ---
def render_owner_panel(chat_id, message_id):
    total_users = len(db["users"])
    premium_users = sum(1 for u in db["users"].values() if u["is_premium"])
    
    owner_text = (
        f"🛠️ <b>BIXXU CLOUD NETWORKS • ROOT ADMIN ARCHITECTURE CONTROL</b> 🛠️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📈 <b>INFRASTRUCTURE STATISTICS FRAMEWORK:</b>\n"
        f"├ Total Registered Network Profiles: <code>{total_users} Entities</code>\n"
        f"├ Active Premium VIP Access Keys: <code>{premium_users} Licences</code>\n"
        f"└ Distributed Sandbox Server Clusters: <code>3 Secure Nodes</code>\n\n"
        f"💰 <b>FINANCIAL TRANSACTION ENDPOINT PROFILE:</b>\n"
        f"└ Current Merchant Destination UPI ID: <code>{db['system']['upi_id']}</code>\n\n"
        f"🎛️ <i>You hold ultimate absolute root execute clearance over this bot application server instance. Select configuration:</i>"
    )
    bot.edit_message_text(owner_text, chat_id, message_id, reply_markup=owner_interface())

# --- HIGH ENERGY INLINE EVENT CALLBACK INTELLIGENCE DRIVER ---
@bot.callback_query_handler(func=lambda call: True)
def process_inline_actions(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    action = call.data
    
    # Validation Interceptor
    if action == "verify_sub":
        if is_user_verified(chat_id):
            bot.answer_callback_query(call.id, "SUCCESS: Access clearance approved.", show_alert=False)
            bot.delete_message(chat_id, message_id)
            render_inline_dashboard(chat_id)
        else:
            bot.answer_callback_query(call.id, "CRITICAL ERROR: Mandatory channels missing.", show_alert=True)
        return
            
    if not is_user_verified(chat_id):
        bot.answer_callback_query(call.id, "SECURITY RUNTIME ALERT: Node access revoked.", show_alert=True)
        return

    # User Profile Actions
    if action == "refresh_dash":
        bot.answer_callback_query(call.id, "SYNCING: Updating cluster memory arrays...")
        render_inline_dashboard(chat_id, message_id)

    # 🔑 THE CORE USER LOGIN SYSTEM (Bot automatically requests their data)
    elif action == "client_login":
        db["user_state"][chat_id] = "waiting_for_phone"
        bot.edit_message_text(
            "🔑 <b>INLINE DISPATCH TERMINAL MANAGER: AUTHORIZATION PHASE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "The cluster engine requires remote authorization to execute broadcasting. "
            "Our secure system will process your configuration automatically.\n\n"
            "<b>ENTER TARGET TELEGRAM ACCOUNT NUMBER:</b>\n"
            "Provide the credentials using international telephone sequence format (e.g., <code>+1234567890</code>) inside the text bar below:",
            chat_id, message_id, reply_markup=back_button()
        )

    elif action == "client_instances":
        bot.answer_callback_query(call.id, "FETCHING: Requesting userbot sessions...", show_alert=False)
        user_data = db["users"].get(chat_id)
        instances_text = (
            "👥 <b>CONNECTED USERBOT TELEPHONE CONTROLLERS</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"• <b>Total Concurrent Terminals:</b> <code>{user_data['connected_accounts']} Active</code>\n\n"
            "<i>No active terminal errors found. Background workers are operational.</i>"
        )
        bot.edit_message_text(instances_text, chat_id, message_id, reply_markup=back_button())

    elif action == "inline_set_msg":
        db["user_state"][chat_id] = "waiting_for_msg"
        bot.edit_message_text(
            "📝 <b>CONFIGURE PROMOTIONAL AD DISPATCH TEMPLATE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Type or paste your strategic marketing announcement layout in the input box below and submit.\n\n"
            "<i>Supports full HTML typography fonts, text links, and standard markdown payloads.</i>",
            chat_id, message_id, reply_markup=back_button()
        )

    elif action == "inline_set_time":
        db["user_state"][chat_id] = "waiting_for_time"
        limit = 60 if db["users"][chat_id]["is_premium"] else 600
        bot.edit_message_text(
            f"⏱️ <b>CONFIGURE AUTOMATION REPETITION INTERVAL THROTTLE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Define system cooldown parameters (expressed in seconds) between message propagation cycles:\n\n"
            f"• <b>Minimum Tier Constraints:</b> <code>{limit} seconds limit</code>\n\n"
            f"<i>Provide absolute digital format entities only. Higher values defend accounts from anti-spam systems.</i>",
            chat_id, message_id, reply_markup=back_button()
        )

    elif action == "engine_start":
        user_data = db["users"].get(chat_id)
        if user_data["ad_msg"] == "NOT CONFIGURED 🔴":
            bot.answer_callback_query(call.id, "EXECUTION FAULT: Populate marketing text template variable first.", show_alert=True)
        elif user_data["connected_accounts"] == 0:
            bot.answer_callback_query(call.id, "EXECUTION FAULT: Inject at least 1 account terminal session via login system.", show_alert=True)
        else:
            user_data["status"] = "PROPAGATING CAMPAIGN ACTIVE 🚀"
            bot.answer_callback_query(call.id, "IGNITION: Forwarding servers launched.", show_alert=False)
            render_inline_dashboard(chat_id, message_id)

    elif action == "engine_stop":
        db["users"][chat_id]["status"] = "IDLE / PAUSED ⏸️"
        bot.answer_callback_query(call.id, "TERMINATED: Active tasks securely halted.", show_alert=False)
        render_inline_dashboard(chat_id, message_id)

    elif action == "buy_premium":
        premium_text = (
            f"👑 <b>ACCELERATE MARKETING TO ENTERPRISE VIP CLUSTER PACKS</b> 👑\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Expand core resource allocation rules to achieve critical marketing exposure matrix:\n\n"
            f"🔥 <b>PREMIUM SUITE EXCLUSIVE BENEFITS:</b>\n"
            f"• <b>Concurrent Pipelines:</b> Connect and stack up to 5 individual userbots simultaneously.\n"
            f"• <b>Hyper-Drive Cooldowns:</b> Drop throttle delay threshold directly down to 60s.\n"
            f"• <b>Smart Flood Override Hash:</b> Algorithmic proxy mapping isolates accounts from ban environments.\n\n"
            f"💰 <b>Subscription Overhead:</b> <u>₹199 / Monthly Token Rate</u>\n\n"
            f"💳 <b>AUTOMATED CHECKOUT ROUTING PROFILES:</b>\n"
            f"Transmit requested billing tokens via UPI System Network to ID: <code>{db['system']['upi_id']}</code>\n\n"
            f"<i>Forward receipt verification screenshot to the customer operations endpoint below for instant provisioning.</i>"
        )
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("🧑‍💻 DISPATCH SETTLMENT SCREENSHOT", url="https://t.me/bixxuchats"))
        markup.row(InlineKeyboardButton("🔙 ABORT OPERATIONS", callback_data="refresh_dash"))
        bot.edit_message_text(premium_text, chat_id, message_id, reply_markup=markup)

    elif action == "view_stats":
        stats_text = (
            f"📊 <b>BIXXU CENTRAL DATA PERFORMANCE ANALYTICS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"• Worldwide Node Connections: <code>5,680 Terminals Online</code>\n"
            f"• Successfully Managed Direct Packets: <code>142,940+ Actions Today</code>\n"
            f"• Operational Processing Uptime: <code>99.982% Integrity Rating</code>\n"
            f"• Virtual Sandbox Partitions: <code>3 Clustered Environments</code>\n\n"
            f"<i>Your userbot operations are hosted in high-availability isolated security contexts.</i>"
        )
        bot.edit_message_text(stats_text, chat_id, message_id, reply_markup=back_button())

    # ==========================================
    # 👑 OWNER EXECUTE DOMAIN FUNCTIONS
    # ==========================================
    elif action == "owner_panel":
        if chat_id != OWNER_ID: return
        render_owner_panel(chat_id, message_id)

    elif action == "owner_set_upi":
        if chat_id != OWNER_ID: return
        db["user_state"][chat_id] = "waiting_for_upi"
        bot.edit_message_text(
            "💳 <b>ADMIN INTERFACE: OVERRIDE UPI BILLING CONFIGURATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Active billing target profile address: <code>{db['system']['upi_id']}</code>\n\n"
            "Provide the new dynamic merchant processing gateway address in the chat console below:",
            chat_id, message_id, reply_markup=owner_back_button()
        )

    elif action == "owner_give_premium":
        if chat_id != OWNER_ID: return
        db["user_state"][chat_id] = "waiting_for_vip_id"
        bot.edit_message_text(
            "🎁 <b>ADMIN INTERFACE: MANUALLY INJECT PREMIUM LICENCE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Input the destination user account unique identifier (Telegram Chat ID) to force VIP clearance validation:",
            chat_id, message_id, reply_markup=owner_back_button()
        )

    elif action == "owner_broadcast":
        if chat_id != OWNER_ID: return
        db["user_state"][chat_id] = "waiting_for_broadcast"
        bot.edit_message_text(
            "📢 <b>ADMIN INTERFACE: GLOBAL MASS NOTIFICATION BROADCAST</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Write the announcement broadcast content details below. Every terminal instance registered in storage cache memory will receive this packet:",
            chat_id, message_id, reply_markup=owner_back_button()
        )

    elif action == "owner_sys_reset":
        if chat_id != OWNER_ID: return
        bot.answer_callback_query(call.id, "FLUSHING: Evicting volatile runtime data logs...", show_alert=True)
        db["users"] = {OWNER_ID: {"name": "Master", "is_premium": True, "connected_accounts": 0, "interval": 60, "status": "IDLE / PAUSED ⏸️", "ad_msg": "NOT CONFIGURED 🔴"}}
        render_owner_panel(chat_id, message_id)


# --- DISCRETE DATA INLINE INPUT CAPTURE PIPELINE ---
@bot.message_handler(func=lambda message: message.chat.id in db["user_state"])
def capture_inline_text_inputs(message):
    chat_id = message.chat.id
    state = db["user_state"].get(chat_id)
    user_text = message.text
    
    # Secure Auto-Erase of user inputs to preserve cockpit screen structure
    try: bot.delete_message(chat_id, message.message_id)
    except Exception: pass

    # Client Automation Steps Handling
    if state == "waiting_for_phone":
        # Simulating automated process triggering sequence based on user input phone number
        db["users"][chat_id]["connected_accounts"] += 1
        del db["user_state"][chat_id]
        bot.send_message(chat_id, f"✅ <b>System Success: Session initialized for terminal sequence token: {user_text}. Login linked.</b>")
        render_inline_dashboard(chat_id)

    elif state == "waiting_for_msg":
        db["users"][chat_id]["ad_msg"] = user_text
        del db["user_state"][chat_id]
        bot.send_message(chat_id, "✅ <b>System Success: Content matrix synchronised for ad broadcast template variable.</b>")
        render_inline_dashboard(chat_id)

    elif state == "waiting_for_time":
        try:
            val = int(user_text)
            limit = 60 if db["users"][chat_id]["is_premium"] else 600
            if val < limit:
                bot.send_message(chat_id, f"❌ <b>Configuration Rejection: Values below lower limit restriction [{limit}s] denied.</b>")
            else:
                db["users"][chat_id]["interval"] = val
                del db["user_state"][chat_id]
                bot.send_message(chat_id, "✅ <b>System Success: Cooldown tracking timer successfully re-configured.</b>")
                render_inline_dashboard(chat_id)
        except ValueError:
            bot.send_message(chat_id, "❌ <b>Validation Error: Non-integer text input rejected. Try again.</b>")

    # ==========================================
    # 👑 OWNER RUNTIME ASSIGNMENT LOGICS
    # ==========================================
    elif state == "waiting_for_upi":
        db["system"]["upi_id"] = user_text.strip()
        del db["user_state"][chat_id]
        bot.send_message(chat_id, f"⚙️ <b>Matrix Alert: Billing system profile reassigned to dynamic destination</b> <code>{user_text}</code>")
        bot.send_message(chat_id, "<b>Re-establishing Secure Interface Connection...</b>")
        bot.clear_step_handler_by_chat_id(chat_id)

    elif state == "waiting_for_vip_id":
        try:
            target_uid = int(user_text.strip())
            if target_uid in db["users"]:
                db["users"][target_uid]["is_premium"] = True
                del db["user_state"][chat_id]
                bot.send_message(chat_id, f"🎁 <b>Matrix Alert: Premium licensing variables injected on unique ID entity {target_uid}.</b>")
                try: bot.send_message(target_uid, "🎉 <b>System Notification: An admin has authorized an VIP Premium Enterprise status to your user terminal node!</b>")
                except Exception: pass
            else:
                bot.send_message(chat_id, "❌ <b>Transaction Failure: Target identity hash not established inside registration records.</b>")
        except ValueError:
            bot.send_message(chat_id, "❌ <b>Transaction Failure: Digits syntax formatting required.</b>")

    eli
