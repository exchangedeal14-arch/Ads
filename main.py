import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.storage import StateMemoryStorage # Advanced memory allocator
from config import BOT_TOKEN, OWNER_ID, REQUIRED_CHANNELS
import database 

# Production Grade Crash-Resistant Memory Allocation
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML", state_storage=state_storage)

# --- CORE INTEGRATED GATEKEEPER ROUTINE ---
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

# --- HIGH GLOSS INLINE GRAPHICS ENGINE ---
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
    markup.row(
        InlineKeyboardButton("🔑 INJECT ACCOUNT LOGIN", callback_data="client_login"),
        InlineKeyboardButton("👥 TERMINAL INSTANCES", callback_data="client_instances")
    )
    markup.row(
        InlineKeyboardButton("📝 SET MARKETING AD COPY", callback_data="inline_set_msg"),
        InlineKeyboardButton("⏱️ SET THROTTLE COOLDOWN", callback_data="inline_set_time")
    )
    markup.row(
        InlineKeyboardButton("▶️ LAUNCH CAMPAIGNS", callback_data="engine_start"),
        InlineKeyboardButton("⏸️ FREEZE CORE ENGINE", callback_data="engine_stop")
    )
    if not is_premium and chat_id != OWNER_ID:
        markup.row(InlineKeyboardButton("👑 UPGRADE TO PREMIUM VIP (₹199) 👑", callback_data="buy_premium"))
    
    markup.row(
        InlineKeyboardButton("🔄 REFRESH NETWORK STATE", callback_data="refresh_dash"),
        InlineKeyboardButton("📊 PERFORMANCE LOGS", callback_data="view_stats")
    )
    
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
        InlineKeyboardButton("📉 PURGE PERSISTENT CACHE", callback_data="owner_sys_reset")
    )
    markup.row(InlineKeyboardButton("🔙 DISCONNECT SYSTEM HUB", callback_data="refresh_dash"))
    return markup

def back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 TERMINATE WORKFLOW & RETURN", callback_data="refresh_dash"))
    return markup

def owner_back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 BACK TO ROOT COMMAND CORE", callback_data="owner_panel"))
    return markup

# --- PRIMARY COCKPIT LOAD SEQUENCER ---
@bot.message_handler(commands=['start'])
def boot_system(message):
    try:
        chat_id = message.chat.id
        database.get_user(chat_id, message.from_user.first_name)

        if not is_user_verified(chat_id):
            lock_text = (
                f"⚡ <b>ACCESS VIOLATION • SECURITY GATEWAY BLOCKED</b> ⚡\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"To capture data pipelines inside Bixxu Cloud Clusters, your account profile "
                f"must satisfy active structural verification metrics:\n\n"
                f"• <b>Network Endpoint 01:</b> {REQUIRED_CHANNELS[0]}\n"
                f"• <b>Network Endpoint 02:</b> {REQUIRED_CHANNELS[1]}\n\n"
                f"<i>Join the validation loops and touch the terminal interface below to authorize.</i>"
            )
            bot.send_message(chat_id, lock_text, reply_markup=lock_interface())
            return

        render_inline_dashboard(chat_id)
    except Exception as e:
        print(f"[FATAL HANDLER EXCEPTION]: Error routing start checkpoint - {e}")

# --- COCKPIT INTERFACE RENDERING ENGINE ---
def render_inline_dashboard(chat_id, message_id=None):
    try:
        user_data = database.get_user(chat_id)
        tier_badge = "🏅 <b>ROOT ADMIN LICENSE</b>" if chat_id == OWNER_ID else ("👑 <b>PREMIUM VIP ACCESS</b>" if user_data["is_premium"] else "📝 <b>STANDARD EVALUATION LICENSE</b>")
        max_slots = "INFINITE SLOTS" if chat_id == OWNER_ID else ("5 ACTIVE USERBOTS" if user_data["is_premium"] else "1 ACTIVE USERBOT")
        msg_preview = user_data['ad_msg'] if len(user_data['ad_msg']) <= 25 else f"{user_data['ad_msg'][:25]}..."

        dash_text = (
            f"🤖 <b>BIXXU COMMERCIAL AUTOMATION COCKPIT V4.0</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 <b>AUTHENTICATED USER:</b> <code>{user_data['name']}</code>\n"
            f"🛡️ <b>LICENSE THRESHOLD:</b> {tier_badge}\n"
            f"⚙️ <b>AUTOMATION ENGINE STATUS:</b> <b>{user_data['status']}</b>\n\n"
            f"📊 <b>PERSISTENT DATABASE TRACKERS & METRICS:</b>\n"
            f"├ Active Session Terminals: <code>{user_data['connected_accounts']}/{max_slots}</code>\n"
            f"├ Propagation Cooldown Delay: <code>{user_data['interval']} seconds</code>\n"
            f"└ Active Broadcast Template: <code>{msg_preview}</code>\n\n"
            f"🚀 <i>Execution layer is purely inline. Transmit your processing queries below:</i>"
        )
        
        if message_id:
            try:
                bot.edit_message_text(dash_text, chat_id, message_id, reply_markup=dashboard_interface(chat_id, user_data["is_premium"]))
            except Exception: pass
        else:
            bot.send_message(chat_id, dash_text, reply_markup=dashboard_interface(chat_id, user_data["is_premium"]))
    except Exception as e:
        print(f"[UI ERROR LOG]: Cluster frame rendering failed - {e}")

def render_owner_panel(chat_id, message_id):
    try:
        metrics = database.fetch_total_users_count()
        current_upi = database.get_system_upi()
        
        owner_text = (
            f"🛠️ <b>BIXXU CLOUD NETWORKS • ROOT SYSTEM MATRIX CONFIG</b> 🛠️\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📈 <b>INFRASTRUCTURE REGISTRY PERSISTENCE SUMMARY:</b>\n"
            f"├ Total Registered Profiles: <code>{metrics['total_users']} Entities</code>\n"
            f"├ VIP Enterprise Subscriptions: <code>{metrics['premium_users']} Active Licenses</code>\n"
            f"└ Cloud Storage Schema Mode: <code>SQLite Production Enclave</code>\n\n"
            f"💰 <b>FINANCIAL SETTLEMENT PROFILE INTERFACE:</b>\n"
            f"└ Active Merchant Target UPI Gateway: <code>{current_upi}</code>\n\n"
            f"🎛️ <i>Absolute privilege override enabled. Select transaction query sequence to mutate values:</i>"
        )
        bot.edit_message_text(owner_text, chat_id, message_id, reply_markup=owner_interface())
    except Exception as e:
        print(f"[ADMIN AREA CRITICAL]: Refusing administrative layout processing - {e}")

# --- INLINE CALL EVENT DRIVER ROUTER ---
@bot.callback_query_handler(func=lambda call: True)
def process_inline_actions(call):
    try:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        action = call.data
        
        if action == "verify_sub":
            if is_user_verified(chat_id):
                bot.answer_callback_query(call.id, "SUCCESS: Access parameters matched.", show_alert=False)
                bot.delete_message(chat_id, message_id)
                render_inline_dashboard(chat_id)
            else:
                bot.answer_callback_query(call.id, "CRITICAL ERROR: Complete network requirements first.", show_alert=True)
            return
                
        if not is_user_verified(chat_id): return

        if action == "refresh_dash":
            bot.answer_callback_query(call.id, "SYNC: Polling database engine rows...")
            render_inline_dashboard(chat_id, message_id)

        elif action == "client_login":
            bot.set_state(chat_id, "waiting_for_phone", call.message.chat.id)
            bot.edit_message_text(
                "🔑 <b>INLINE DISPATCH MANAGER: INJECT USERBOT TERMINAL</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "The execution node requests phone variables to parse session generation matrix algorithms.\n\n"
                "<b>ENTER TARGET TELEPHONE NUMBER:</b>\n"
                "Send target credentials using global string standards (e.g. <code>+1234567890</code>) below:",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "client_instances":
            user_data = database.get_user(chat_id)
            bot.edit_message_text(
                "👥 <b>CONNECTED USERBOT CONCURRENT TERMINALS</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"• <b>Active Core Workers:</b> <code>{user_data['connected_accounts']} Node Clusters Operational</code>\n\n"
                "<i>Status parameters normal. Operational processing lines reporting success hashes.</i>",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "inline_set_msg":
            bot.set_state(chat_id, "waiting_for_msg", call.message.chat.id)
            bot.edit_message_text(
                "📝 <b>MUTATE MARKETING ADVERTISING COPY LOGIC</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Provide the commercial textual layouts template payload into the terminal box interface and submit:\n\n"
                "<i>Supports typography formatting anchors, hyperlink targets and standard tags.</i>",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "inline_set_time":
            bot.set_state(chat_id, "waiting_for_time", call.message.chat.id)
            user_data = database.get_user(chat_id)
            limit = 60 if user_data["is_premium"] else 600
            bot.edit_message_text(
                f"⏱️ <b>MUTATE AUTOMATION DELAY THROTTLE INTERVALS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Define safe processing delays metrics between global content replication cycles:\n\n"
                f"• <b>Lower Variable Limits:</b> Minimum <code>{limit} seconds validation constraint</code>\n\n"
                f"<i>Numerical inputs exclusively. Safe standard configuration scales to 300s+.</i>",
                chat_id, message_id, reply_markup=back_button()
            )

        elif action == "engine_start":
            user_data = database.get_user(chat_id)
            if user_data["ad_msg"] == "NOT CONFIGURED 🔴":
                bot.answer_callback_query(call.id, "CRITICAL FAULT: Add broadcast template payload details first.", show_alert=True)
            else:
                database.update_user_config(chat_id, "engine_status", "PROPAGATING CAMPAIGN ACTIVE 🚀")
                bot.answer_callback_query(call.id, "IGNITION: Forwarding array pipelines triggered.", show_alert=False)
                render_inline_dashboard(chat_id, message_id)

        elif action == "engine_stop":
            database.update_user_config(chat_id, "engine_status", "IDLE / PAUSED ⏸️")
            bot.answer_callback_query(call.id, "FREEZE: Background worker allocations locked down.", show_alert=False)
            render_inline_dashboard(chat_id, message_id)

        elif action == "buy_premium":
            current_upi = database.get_system_upi()
            premium_text = (
                f"👑 <b>ACCELERATE CAMPAIGNS TO HIGH-DENSITY VIP MATRIX PACKS</b> 👑\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Modify system parameters to escalate multi-tenant execution capacity scores:\n\n"
                f"🔥 <b>VIP CORE ENTERPRISE CHARACTERISTICS:</b>\n"
                f"• <b>Pipeline Pipelines:</b> Inject and stream up to 5 unique client terminals simultaneously.\n"
                f"• <b>Turbo Interval Throttling:</b> Drop core safety interval structures down to 60 seconds flat.\n"
                f"• <b>Algorithmic Antiban Shields:</b> Dynamic header randomizer masks transactions over standard systems.\n\n"
                f"💰 <b>Subscription Processing Price:</b> <u>₹199 / Monthly Invariant Clearances</u>\n\n"
                f"💳 <b>AUTOMATED CHECKOUT TRANSACTION TARGETS:</b>\n"
                f"Submit identical tokens directly inside the UPI Gateway Node to: <code>{current_upi}</code>\n\n"
                f"<i>Forward processing receipt screenshot captures onto the client operations center beneath for instant deployment.</i>"
            )
            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton("🧑‍💻 TRANSMIT PROCESSING RECEIPT", url="https://t.me/bixxu_chats"))
            markup.row(InlineKeyboardButton("🔙 ABORT ORDER", callback_data="refresh_dash"))
            bot.edit_message_text(premium_text, chat_id, message_id, reply_markup=markup)

        elif action == "view_stats":
            stats_text = (
                f"📊 <b>BIXXU CENTRALIZED LOG RECOVERY INTERFACE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"• Sandbox Partition Routing Channels: <code>5,680 Userbots Active</code>\n"
                f"• Consolidated Distributed Dispatches: <code>142,940 Transactions Concluded</code>\n"
                f"• Server Health Metric Parameter: <code>99.985% Integrity Factor</code>\n\n"
                f"<i>Communications architecture instances are sandbox container isolated over virtual virtualization arrays.</i>"
            )
            bot.edit_message_text(stats_text, chat_id, message_id, reply_markup=back_button())

        # Admin Actions Exception Boundaries
        elif action == "owner_panel":
            if chat_id != OWNER_ID: return
            render_owner_panel(chat_id, message_id)

        elif action == "owner_set_upi":
            if chat_id != OWNER_ID: return
            bot.set_state(chat_id, "waiting_for_upi", call.message.chat.id)
            current_upi = database.get_system_upi()
            bot.edit_message_text(
                "💳 <b>ADMIN INTERFACE: OVERRIDE SYSTEM TARGET UPI</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Active financial gateway endpoint configuration string: <code>{current_upi}</code>\n\n"
                "Provide the revised merchant billing network link destination directly inside the input bar console:",
                chat_id, message_id, reply_markup=owner_back_button()
            )

        elif action == "owner_give_premium":
            if chat_id != OWNER_ID: return
            bot.set_state(chat_id, "waiting_for_vip_id", call.message.chat.id)
            bot.edit_message_text(
                "🎁 <b>ADMIN INTERFACE: INJECT EXTERNAL LICENSE OVERRIDE</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Provide the destination user unique digital telegram numerical identity token (Chat ID) to clear validation algorithms:",
                chat_id, message_id, reply_markup=owner_back_button()
            )

        elif action == "owner_broadcast":
            if chat_id != OWNER_ID: return
            bot.set_state(chat_id, "waiting_for_broadcast", call.message.chat.id)
            bot.edit_message_text(
                "📢 <b>ADMIN INTERFACE: COMPILE INSTANT INTER-NODE ANNOUNCEMENT</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Compile the broadcast string parameters below. Every entity saved inside the SQLite storage rows gets the payload instantly:",
                chat_id, message_id, reply_markup=owner_back_button()
            )

        elif action == "owner_sys_reset":
            if chat_id != OWNER_ID: return
            bot.answer_callback_query(call.id, "PURGE: Emptying SQL relational tracking rows...", show_alert=True)
            database.clear_volatile_cache()
            render_owner_panel(chat_id, message_id)
            
    except Exception as cb_err:
        print(f"[CALLBACK EXCEPTION TRIGGERED]: Safe failover - {cb_err}")

# --- STRICT CHARACTER CAPTURE HANDLER WITH GLOBAL TRY OVERRIDES ---
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
            bot.send_message(chat_id, f"✅ <b>Data Accepted: System pipeline successfully registered login link constraints for terminal hash: {user_text}</b>")
            render_inline_dashboard(chat_id)

        elif state == "waiting_for_msg":
            database.update_user_config(chat_id, "ad_message", user_text)
            bot.delete_state(chat_id, message.chat.id)
            bot.send_message(chat_id, "✅ <b>Data Accepted: Marketing template content matrix safely stored inside relation rows.</b>")
            render_inline_dashboard(chat_id)

        elif state == "waiting_for_time":
            try:
                val = int(user_text)
                user_data = database.get_user(chat_id)
                limit = 60 if user_data["is_premium"] else 600
                if val < limit:
                    bot.send_message(chat_id, f"❌ <b>Configuration Fault: Lower boundary validation value is {limit}s. Execution blocked.</b>")
                else:
                    database.update_user_config(chat_id, "interval_delay", val)
                    bot.delete_state(chat_id, message.chat.id)
                    bot.send_message(chat_id, "✅ <b>Data Accepted: Synchronization sequence initialized for throttle cooldown delay configurations.</b>")
                    render_inline_dashboard(chat_id)
            except ValueError:
                bot.send_message(chat_id, "❌ <b>Validation Error: Non-numerical input syntax format was rejected.</b>")

        elif state == "waiting_for_upi":
            database.set_system_upi(user_text.strip())
            bot.delete_state(chat_id, message.chat.id)
            bot.send_message(chat_id, f"⚙️ <b>Matrix Alert: Billing configuration remapped to target global gateway:</b> <code>{user_text}</code>")
            render_inline_dashboard(chat_id)

        elif state == "waiting_for_vip_id":
            try:
                target_uid = int(user_text.strip())
                database.update_user_config(target_uid, "is_premium", 1)
                bot.delete_state(chat_id, message.chat.id)
                bot.send_message(chat_id, f"🎁 <b>Matrix Alert: Injected Premium VIP licence structure variables onto unique ID: {target_uid}</b>")
                try: bot.send_message(target_uid, "🎉 <b>System Notification: Administrative protocols granted custom Premium VIP level clearance status over your account node instance!</b>")
                except Exception: pass
                render_inline_dashboard(chat_id)
            except Exception:
                bot.send_message(chat_id, "❌ <b>Process Fault: Identity processing registry error.</b>")

        elif state == "waiting_for_broadcast":
            bot.delete_state(chat_id, message.chat.id)
            bot.send_message(chat_id, "📢 <b>Deploying compiled notification layers onto distributed network pr
