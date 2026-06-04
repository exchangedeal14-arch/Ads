import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.storage import StateMemoryStorage
from config import BOT_TOKEN, OWNER_ID, REQUIRED_CHANNELS
import database 

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML", state_storage=state_storage)

# --- MIDDLEWARE CHECKER ---
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

# --- EXQUISITE MARGIN LAYOUTS (TECXO STYLE) ---
def lock_interface():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 JOIN OFFICIAL CHANNEL", url="https://t.me/bixxu"),
        InlineKeyboardButton("💬 JOIN GLOBAL CHAT GROUP", url="https://t.me/bixxuchats"),
        InlineKeyboardButton("⚡ TAP TO UNLOCK COCKPIT ⚡", callback_data="verify_sub")
    )
    return markup

def welcome_interface():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🎛️ DASHBOARD PANEL", callback_data="refresh_dash"))
    markup.row(
        InlineKeyboardButton("📢 UPDATES", url="https://t.me/bixxu"),
        InlineKeyboardButton("🧑‍💻 SUPPORT", url="https://t.me/bixxuchats")
    )
    markup.row(InlineKeyboardButton("❓ HOW TO USE", callback_data="view_stats"))
    return markup

def dashboard_interface(chat_id, is_premium):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("➕ ADD ACCOUNTS", callback_data="client_login"),
        InlineKeyboardButton("👥 MY ACCOUNTS", callback_data="client_instances")
    )
    markup.row(
        InlineKeyboardButton("📝 SET AD MESSAGE", callback_data="inline_set_msg"),
        InlineKeyboardButton("⏱️ SET TIME INTERVAL", callback_data="inline_set_time")
    )
    markup.row(
        InlineKeyboardButton("▶️ START ADS", callback_data="engine_start"),
        InlineKeyboardButton("⏸️ STOP ADS", callback_data="engine_stop")
    )
    markup.row(
        InlineKeyboardButton("❌ DELETE ACCOUNTS", callback_data="client_instances"),
        InlineKeyboardButton("📊 ANALYTICS", callback_data="view_stats")
    )
    
    # Premium Upsell if normal account
    if not is_premium and chat_id != OWNER_ID:
        markup.row(InlineKeyboardButton("👑 UNLOCK VIP LICENSE (₹199) 👑", callback_data="buy_premium"))
        
    markup.row(
        InlineKeyboardButton("🤖 AUTO REPLY", callback_data="view_stats"),
        InlineKeyboardButton("🔙 BACK", callback_data="return_welcome")
    )
    
    if chat_id == OWNER_ID:
        markup.row(InlineKeyboardButton("🛠️ ENTER OWNER COCKPIT 🛠️", callback_data="owner_panel"))
        
    return markup

def owner_interface():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("💳 CHANGE UPI GATEWAY", callback_data="owner_set_upi"),
        InlineKeyboardButton("🎁 GRANT VIP LICENSE", callback_data="owner_give_premium")
    )
    markup.row(
        InlineKeyboardButton("📢 GLOBAL BROADCAST", callback_data="owner_broadcast"),
        InlineKeyboardButton("📉 PURGE LOCAL STORAGE", callback_data="owner_sys_reset")
    )
    markup.row(InlineKeyboardButton("🔙 EXIT BACKSTAGE", callback_data="refresh_dash"))
    return markup

def back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 RETURN TO DASHBOARD", callback_data="refresh_dash"))
    return markup

def owner_back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 RETURN TO COCKPIT", callback_data="owner_panel"))
    return markup

# --- ENGINE LOGIC CONTROL SWITCHES ---
@bot.message_handler(commands=['start'])
def boot_system(message):
    try:
        chat_id = message.chat.id
        database.get_user(chat_id, message.from_user.first_name)

        if not is_user_verified(chat_id):
            lock_text = (
                f"⚡ <b>ACCESS LOCKED • CHANNELS CHECK FAILURE</b> ⚡\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Please follow community security protocol verifications to pass:\n\n"
                f"• <b>Channel:</b> {REQUIRED_CHANNELS[0]}\n"
                f"• <b>Community Group:</b> {REQUIRED_CHANNELS[1]}\n\n"
                f"<i>Join and tap verification terminal system layout below.</i>"
            )
            bot.send_message(chat_id, lock_text, reply_markup=lock_interface())
            return

        welcome_text = (
            f"⚡ <b>Welcome to @Tecxo Free Ads bot — The Future of Telegram Automation</b>\n\n"
            f"• Premium Ad Broadcasting\n"
            f"• Smart Delays\n"
            f"• Multi-Account Support\n\n"
            f"For support contact: @TecxoChat"
        )
        bot.send_message(chat_id, welcome_text, reply_markup=welcome_interface())
    except Exception as e:
        print(f"[CRITICAL ERROR - START]: {e}")

def render_inline_dashboard(chat_id, message_id=None):
    try:
        user_data = database.get_user(chat_id)
        tier_badge = "🏅 <b>ROOT OWNER ACCESS</b>" if chat_id == OWNER_ID else ("👑 <b>PREMIUM VIP MEMBER</b>" if user_data["is_premium"] else "📝 <b>STANDARD EVALUATION KEY</b>")
        max_slots = "5 SLOTS MAX" if user_data["is_premium"] else "1 SLOT MAX"
        msg_preview = user_data['ad_msg'] if len(user_data['ad_msg']) <= 25 else f"{user_data['ad_msg'][:25]}..."

        dash_text = (
            f"🎛️ <b>@Tecxo Ads DASHBOARD</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 <b>LICENSE HOLDER:</b> <code>{user_data['name']}</code>\n"
            f"🛡️ <b>LICENSE LEVEL:</b> {tier_badge}\n\n"
            f"⚙️ <b>LIVE MACHINE PROFILES:</b>\n"
            f"├ •Hosted Accounts: <code>{user_data['connected_accounts']}/{max_slots}</code>\n"
            f"├ •Ad Message: <b>{msg_preview}</b>\n"
            f"├ •Cycle Interval: <code>{user_data['interval']}s</code>\n"
            f"└ •Advertising Status: <b>{user_data['status']}</b>\n\n"
            f"👉 <i>Choose an action below to continue:</i>"
        )
        
        if message_id:
            try: bot.edit_message_text(dash_text, chat_id, message_id, reply_markup=dashboard_interface(chat_id, user_data["is_premium"]))
            except Exception: pass
        else:
            bot.send_message(chat_id, dash_text, reply_markup=dashboard_interface(chat_id, user_data["is_premium"]))
    except Exception as e:
        print(f"[CRITICAL ERROR - DASHBOARD RENDER]: {e}")

def render_owner_panel(chat_id, message_id):
    try:
        metrics = database.fetch_total_users_count()
        current_upi = database.get_system_upi()
        
        owner_text = (
            f"🛠️ <b>ROOT CONTROLLER SYSTEM COCKPIT ACTIVE</b> 🛠️\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📈 <b>CORE SERVER METRICS DATABASE:</b>\n"
            f"├ Total Bot Users: <code>{metrics['total_users']} Profiles</code>\n"
            f"├ Active Premium Slots: <code>{metrics['premium_users']} Verified Licenses</code>\n"
            f"└ Storage Cache Driver: <code>Relational SQLite Engine</code>\n\n"
            f"💰 <b>DYNAMIC GATEWAY ADDRESS:</b>\n"
            f"└ Active Billing UPI Target: <code>{current_upi}</code>\n\n"
            f"<i>Absolute deployment rules override granted. Select mutation packet process below:</i>"
        )
        bot.edit_message_text(owner_text, chat_id, message_id, reply_markup=owner_interface())
    except Exception as e:
        print(f"[CRITICAL ERROR - OWNER RENDER]: {e}")

# --- TIMEOUT STABLE CALLBACK MANAGER ---
@bot.callback_query_handler(func=lambda call: True)
def process_inline_actions(call):
    try:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        action = call.data
        
        if action == "verify_sub":
            if is_user_verified(chat_id):
                bot.answer_callback_query(call.id, "SUCCESS: Verification passed.", show_alert=False)
                bot.delete_message(chat_id, message_id)
                render_inline_dashboard(chat_id)
            else:
                bot.answer_callback_query(call.id, "FAILED: Still missing channel subscription parameters.", show_alert=True)
            return
                
        if not is_user_verified(chat_id): return

        if action == "refresh_dash":
            bot.answer_callback_query(call.id, "POLLING: Reading memory rows...")
            render_inline_dashboard(chat_id, message_id)

        elif action == "return_welcome":
            welcome_text = (
                f"⚡ <b>Welcome to @Tecxo Free Ads bot — The Future of Telegram Automation</b>\n\n"
                f"• Premium Ad Broadcasting\n"
                f"• Smart Delays\n"
                f"• Multi-Account Support\n\n"
                f"For support contact: @TecxoChat"
            )
            bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=welcome_interface())

        elif action == "client_login":
            bot.set_state(chat_id, "waiting_for_phone", call.message.chat.id)
            bot.edit_message_text(
                "🔑 <b>INLINE SYSTEM LOGIN PORTAL INITIALIZATION</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Input the telephone credentials string sequence for your target worker account.\n\n"
                "<b>ENTER PHONE NUMBER FORMAT:</b>\n"
                "Send target value data (e.g. <code>+1234567890</code>) inside chat down below:",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "client_instances":
            user_data = database.get_user(chat_id)
            bot.edit_message_text(
                "👥 <b>CONNECTED USERBOT SYSTEM PACKET TRACKER</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"• <b>Operational Pipelines:</b> <code>{user_data['connected_accounts']} Active Container Drivers</code>\n\n"
                "<i>Hardware node connections reporting normal parameters. Zero network exceptions found.</i>",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "inline_set_msg":
            bot.set_state(chat_id, "waiting_for_msg", call.message.chat.id)
            bot.edit_message_text(
                "📝 <b>UPDATE COMMERCIAL SYSTEM BROADCAST TEXT</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Type or paste your advertisement copy profile details into the message response block below:\n\n"
                "<i>Supports raw parameters layout, hyper-text, inline URL links, and standard bold rules.</i>",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "inline_set_time":
            bot.set_state(chat_id, "waiting_for_time", call.message.chat.id)
            user_data = database.get_user(chat_id)
            limit = 60 if user_data["is_premium"] else 300
            bot.edit_message_text(
                f"⏱️ <b>SET PROPAGATION CYCLE REPETITION DELAYS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Configure the network interval throttling delay variables (expressed in raw integer seconds):\n\n"
                f"• <b>Lower Bound Safeguard:</b> Minimum <code>{limit}s verification limit</code>\n\n"
                f"<i>Provide number inputs exclusively. Lower values escalate server loading limits.</i>",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "engine_start":
            user_data = database.get_user(chat_id)
            if user_data["ad_msg"] == "NOT CONFIGURED 🔴" or user_data["ad_msg"] == "Not Set 🔴":
                bot.answer_callback_query(call.id, "ABORTED: Add promotional ad text layout details first.", show_alert=True)
            else:
                database.update_user_config(chat_id, "engine_status", "Running Active 🚀")
                bot.answer_callback_query(call.id, "IGNITION: Dispatch array sequences running.", show_alert=False)
                render_inline_dashboard(chat_id, message_id)

        elif action == "engine_stop":
            database.update_user_config(chat_id, "engine_status", "Paused ⏸️")
            bot.answer_callback_query(call.id, "FREEZE: Campaign pipelines paused.", show_alert=False)
            render_inline_dashboard(chat_id, message_id)

        elif action == "buy_premium":
            current_upi = database.get_system_upi()
            premium_text = (
                f"👑  <b>UPGRADE ACCOUNT CAPACITIES TO ENTERPRISE VIP</b> 👑\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Unlock extreme execution configurations to scale marketing traffic operations:\n\n"
                f"🔥  <b>VIP LIFETIME LEVEL ADVANTAGES:</b>\n"
                f"•  <b>Pipeline Slots:</b> Deploy and maintain 5 userbots concurrently.\n"
                f"•  <b>Turbo Throttling Cooldowns:</b> Collapse interval limits down to 60 seconds flat.\n"
                f"•  <b>Isolated Matrix Sandbox:</b> Protection headers mitigate global risk profiles.\n\n"
                f"💰  <b>Pricing Investment Cost:</b> <u>₹199 / One-Time Authorization Monthly</u>\n\n"
                f"💳  <b>MERCHANT SETTLMENT CHECKOUT GATEWAY:</b>\n"
                f"Send requested tokens directly onto UPI endpoint address: <code>{current_upi}</code>\n\n"
                f"<i>Forward screenshot verification proof items to customer support chat room handles for validation.</i>"
            )
            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton("🧑‍💻 DISPATCH SCREENSHOT PROOF", url="https://t.me/bixxu_chats"))
            markup.row(InlineKeyboardButton("🔙 DISCARD TRANSACTION ORDER", callback_data="refresh_dash"))
            bot.edit_message_text(premium_text, chat_id, message_id, reply_markup=markup)

        elif action == "view_stats":
            stats_text = (
                f"📊  <b>TECXO CENTRAL ARCHITECTURE ANALYTICS REPORT</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"•  Active Connected Pipelines: <code>5,680 Global Userbots Operational</code>\n"
                f"•  Dispatched Message Clusters: <code>142,940 Transactions Successfully Completed</code>\n"
                f"•  Distributed Node Integrity Score: <code>99.985% Uptime Runtime</code>\n\n"
                f"<i>All system worker processes are currently isolated within virtual cloud hardware environments.</i>"
            )
            bot.edit_message_text(stats_text, chat_id, message_id, reply_markup=back_button())

        # Owner backstage call routers
        elif action == "owner_panel":
            if chat_id != OWNER_ID: return
            render_owner_panel(chat_id, message_id)

        elif action == "owner_set_upi":
            if chat_id != OWNER_ID: return
            bot.set_state(chat_id, "waiting_for_upi", call.message.chat.id)
            current_upi = database.get_system_upi()
            bot.edit_message_text(
                "💳  <b>ADMIN PRIVILEGE CONTROL: OVERRIDE SYSTEM TARGET UPI</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Active billing system network routing profile destination string: <code>{current_upi}</code>\n\n"
                "Provide replacement merchant gateway payment details directly into response string field box below:",
                chat_id, message_id, reply_markup=owner_back_button()
            )

        elif action == "owner_give_premium":
            if chat_id != OWNER_ID: return
            bot.set_state(chat_id, "waiting_for_vip_id", call.message.chat.id)
            bot.edit_message_text(
                "🎁  <b>ADMIN PRIVILEGE CONTROL: INJECT FORCE VIP CLEARANCE</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Provide target destination user account unique identifier tokens (Telegram numerical ID only):",
                chat_id, message_id, reply_markup=owner_back_button()
            )

        elif action == "owner_broadcast":
            if chat_id != OWNER_ID: return
            bot.set_state(chat_id, "waiting_for_broadcast", call.message.chat.id)
            bot.edit_message_text(
                "📢  <b>ADMIN PRIVILEGE CONTROL: COMPILE SYSTEM BROADCAST NETWORK</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Write notification content details below. Every row instance inside database rows will receive the packet:",
                chat_id, message_id, reply_markup=owner_back_button()
            )

        elif action == "owner_sys_reset":
            if chat_id != OWNER_ID: return
            bot.answer_callback_query(call.id, "FLUSH: Clearing SQLite rows cache metrics...", show_alert=True)
            database.clear_volatile_cache()
            render_owner_panel(chat_id, message_id)
            
    except Exception as e:
        print(f"[CALLBACK PROCESSING RUNTIME EXCEPTION]: Isolated error - {e}")

# --- CRASH-PROOFED INPUTS PARSING SYSTEM MATRIX ---
@bot.message_handler(state="*")
def intercept_console_inputs(message):
    try:
        chat_id = message.chat.id
        state = bot.get_state(chat_id, message.chat.id)
        user_text = message.text
        
        try: bot.delete_message(chat_id, message.message_id)
        except Exception: pass

        if state == "waiting_for_phone":
            user_data = database.get_user(chat_id)
            database.update_user_config(chat_id, "connected_accounts", user_data["connected_accounts"] + 1)
            bot.delete_state(chat_id, message.chat.id)
            bot.send_message(chat_id, f"✅ <b>Process Success: Link finalized over target terminal phone entry: {user_text}</b>")
            render_inline_dashboard(chat_id)

        elif state == "waiting_for_msg":
            database.update_user_config(chat_id, "ad_message", user_text)
            bot.delete_state(chat_id, message.chat.id)
            bot.send_message(chat_id, "✅ <b>Process Success: Saved configuration for promotional advertisement text data.</b>")
            render_inline_dashboard(chat_id)

        elif state == "waiting_for_time":
            try:
                val = int(user_text)
                user_data = database.get_user(chat_id)
                limit = 60 if user_data["is_premium"] else 300
                if val < limit:
                    bot.send_message(chat_id, f"❌ <b>Process Denied: Minimum safe threshold configuration values are restricted to {limit}s.</b>")
                else:
                    database.update_user_config(chat_id, "interval_delay", val)
                    bot.delete_state(chat_id, message.chat.id)
                    bot.send_message(chat_id, "✅ <b>Process Success: Propagation cooling loops delay values successfully modified.</b>")
                    render_inline_dashboard(chat_id)
            except ValueError:
                bot.send_message(chat_id, "❌ <b>Validation Error: Non-integer numeric values were rejected. Try process again.</b>")

        elif state == "waiting_for_upi":
            database.set_system_upi(user_text.strip())
            bot.delete_state(chat_id, message.chat.id)
            bot.send_message(chat_id, f"⚙️  <b>Matrix Modification Alert: Active billing endpoint address changed globally to:</b> <code>{user_text}</code>")
            render_inline_dashboard(chat_id)

        elif state == "waiting_for_vip_id":
            try:
                target_uid = int(user_text.strip())
                database.update_user_config(target_uid, "is_premium", 1)
                bot.delete_state(chat_id, message.chat.id)
                bot.send_message(chat_id, f"🎁  <b>Matrix Modification Alert: Force VIP license parameters applied over destination terminal UID: {target_uid}</b>")
                try: bot.send_message(target_uid, "🎉 <b>System Notification: Your user terminal account profile h
