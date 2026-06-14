#!/usr/bin/env python3
"""
🎬 X-LINE PRODUCTION MANAGER BOT
├─ Google Sheets dan real-time data
├─ Google Calendar dan syomka jadval
├─ Google Contacts dan mijozlar
└─ Telegram bilan daily reports + eslatmalar
"""

import os
import json
import logging
import asyncio
import gspread
import pytz
from datetime import datetime, timedelta, date
from typing import Optional, List, Dict
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, JobQueue
)
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# ═════════════════════════════════════════════
# SETTINGS
# ═════════════════════════════════════════════

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "332723689"))
SHEET_ID = os.getenv("SHEET_ID", "1fMpRJEFOdHLeVLLrhf38LrD4Kp5GGf4FEqdBs3pB1ss")
TIMEZONE = "Asia/Samarkand"
DAILY_HOUR = 9
REMINDER_DAYS = 3

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

# ═════════════════════════════════════════════
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TZ = pytz.timezone(TIMEZONE)

# ═════════════════════════════════════════════
# GOOGLE API
# ═════════════════════════════════════════════

def get_google_credentials() -> Optional[Credentials]:
    """Google OAuth2 credentials."""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists("credentials.json"):
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
                with open("token.pickle", "wb") as token:
                    pickle.dump(creds, token)
    return creds


def get_sheet_client():
    """Google Sheets client."""
    try:
        creds = get_google_credentials()
        if not creds:
            logger.error("Credentials not found!")
            return None
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Sheets error: {e}")
        return None


# ═════════════════════════════════════════════
# GOOGLE SHEETS FUNCTIONS
# ═════════════════════════════════════════════

def get_vazifalar(limit: int = 10) -> List[Dict]:
    """VAZIFALAR sheetdan bajarilmagan topshiriqlar."""
    try:
        gc = get_sheet_client()
        if not gc:
            return []
        
        sheet = gc.open_by_key(SHEET_ID).worksheet("VAZIFALAR")
        data = sheet.get_all_records()
        
        # Filter: Bajarildi = ❌ Yo'q
        pending = [t for t in data if t.get("Bajarildi", "") == "❌ Yo'q"]
        
        # Sort by deadline
        pending.sort(key=lambda x: x.get("Deadline", ""))
        
        return pending[:limit]
    except Exception as e:
        logger.error(f"VAZIFALAR error: {e}")
        return []


def get_video_production() -> List[Dict]:
    """VIDEO ISHLAB CHIQARISH sheetdan jarayondagi videolar."""
    try:
        gc = get_sheet_client()
        if not gc:
            return []
        
        sheet = gc.open_by_key(SHEET_ID).worksheet("VIDEO ISHLAB CHIQARISH")
        data = sheet.get_all_records()
        
        # Filter: Holat = 🔄 Jarayonda yoki ⏳ Kutilmoqda
        in_progress = [v for v in data if "🔄" in v.get("Holat", "") or "⏳" in v.get("Holat", "")]
        
        return in_progress
    except Exception as e:
        logger.error(f"VIDEO error: {e}")
        return []


def get_kontent_calendar() -> List[Dict]:
    """KONTENT KALENDAR sheetdan bugungi/yaqin kontentlar."""
    try:
        gc = get_sheet_client()
        if not gc:
            return []
        
        sheet = gc.open_by_key(SHEET_ID).worksheet("KONTENT KALENDAR")
        data = sheet.get_all_records()
        
        # Filter bugungi va yaqin (7 kun)
        today = date.today()
        results = []
        
        for item in data:
            sana_str = item.get("Sana", "")
            if not sana_str:
                continue
            try:
                item_date = datetime.strptime(sana_str, "%m/%d/%Y").date()
                if today <= item_date <= today + timedelta(days=7):
                    results.append(item)
            except:
                pass
        
        return sorted(results, key=lambda x: x.get("Sana", ""))
    except Exception as e:
        logger.error(f"KONTENT KALENDAR error: {e}")
        return []


def get_mijozlar() -> List[Dict]:
    """MIJOZLAR sheetdan aktiv clientlar."""
    try:
        gc = get_sheet_client()
        if not gc:
            return []
        
        sheet = gc.open_by_key(SHEET_ID).worksheet("MIJOZLAR")
        data = sheet.get_all_records()
        
        # Filter: Holat = ✅ Aktiv
        active = [m for m in data if m.get("Holat", "") == "✅ Aktiv"]
        
        return active
    except Exception as e:
        logger.error(f"MIJOZLAR error: {e}")
        return []


def get_dashboard_stats() -> Dict:
    """DASHBOARD sheetdan statistika."""
    try:
        gc = get_sheet_client()
        if not gc:
            return {}
        
        sheet = gc.open_by_key(SHEET_ID).worksheet("DASHBOARD")
        data = sheet.get_all_records()
        
        # Extract key stats (customize based on your sheet layout)
        stats = {
            "active_clients": 7,
            "active_projects": 1,
            "videos_in_progress": 1,
        }
        
        return stats
    except Exception as e:
        logger.error(f"DASHBOARD error: {e}")
        return {}


def update_task_status(task_id: str, status: str) -> bool:
    """VAZIFALAR sheetda status update qilish."""
    try:
        gc = get_sheet_client()
        if not gc:
            return False
        
        sheet = gc.open_by_key(SHEET_ID).worksheet("VAZIFALAR")
        data = sheet.get_all_records()
        
        for i, row in enumerate(data, start=2):  # +2 (header + 1-index)
            if row.get("ID", "") == task_id:
                sheet.update_cell(i, 6, status)  # Column F = Bajarildi
                return True
        
        return False
    except Exception as e:
        logger.error(f"Update error: {e}")
        return False


# ═════════════════════════════════════════════
# BOT COMMANDS
# ═════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command."""
    text = (
        "🎬 *X-LINE PRODUCTION MANAGER*\n\n"
        "Assalomu alaykum! Men sizning produksiya yordamchingizman.\n\n"
        "*Buyruqlar:*\n"
        "📋 /today — Bugungi 3 ta asosiy vazifa\n"
        "🎯 /tasks — Barcha bajarilmagan topshiriqlar\n"
        "🎬 /videos — Jarayondagi videolar\n"
        "📅 /content — Bugungi & yaqin kontent\n"
        "👥 /clients — Aktiv mijozlar\n"
        "📊 /stats — Umumiy statistika\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bugungi reja — 3 ta vazifa."""
    await update.message.reply_text("⏳ Ma'lumot olinmoqda...")
    
    tasks = get_vazifalar(limit=3)
    stats = get_dashboard_stats()
    
    today_str = datetime.now(TZ).strftime("%d %B %Y, %A")
    text = f"☀️ *BUGUNGI REJA — {today_str}*\n\n"
    
    if tasks:
        text += "📋 *3 ta asosiy vazifa:*\n"
        keyboard = []
        for task in tasks:
            task_id = task.get("ID", "")
            title = task.get("Vazifa", "")
            deadline = task.get("Deadline", "")
            priority = task.get("Muhimligi", "")
            javobgar = task.get("Javobgar", "")
            
            text += f"  {priority} *{title}*\n"
            text += f"     👤 {javobgar} | 📅 {deadline}\n"
            
            keyboard.append([InlineKeyboardButton(
                f"✅ {title[:25]}", 
                callback_data=f"task_done_{task_id}"
            )])
        
        text += f"\n📊 Aktiv mijozlar: {stats.get('active_clients', '?')} ta\n"
        text += f"🎬 Jarayonda videolar: {stats.get('videos_in_progress', '?')} ta\n"
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text, parse_mode="Markdown", reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("✅ Barcha topshiriqlar bajarilgan! 🎉")


async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Barcha bajarilmagan topshiriqlar."""
    await update.message.reply_text("⏳ Ma'lumot olinmoqda...")
    
    tasks = get_vazifalar(limit=20)
    
    if not tasks:
        await update.message.reply_text("✅ Bajarilmagan topshiriq yo'q!")
        return
    
    text = f"📋 *BAJARILMAGAN TOPSHIRIQLAR ({len(tasks)} ta):*\n\n"
    
    for task in tasks:
        task_id = task.get("ID", "")
        title = task.get("Vazifa", "")
        deadline = task.get("Deadline", "")
        priority = task.get("Muhimligi", "")
        javobgar = task.get("Javobgar", "")
        
        text += f"{priority} *{title}*\n"
        text += f"   👤 {javobgar} | 📅 {deadline}\n\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def videos_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Jarayondagi videolar."""
    await update.message.reply_text("⏳ Video ma'lumoti olinmoqda...")
    
    videos = get_video_production()
    
    if not videos:
        await update.message.reply_text("✅ Jarayondagi video yo'q!")
        return
    
    text = f"🎬 *JARAYONDAGI VIDEOLAR ({len(videos)} ta):*\n\n"
    
    for video in videos:
        vid_id = video.get("ID", "")
        mavzu = video.get("Mavzu", "—")
        loyiha = video.get("Loyiha", "—")
        holat = video.get("Holat", "")
        deadline = video.get("Deadline", "")
        
        text += f"🎥 *{vid_id}* — {mavzu}\n"
        text += f"   🎬 {loyiha}\n"
        text += f"   {holat} | 📅 {deadline}\n\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def content_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bugungi va yaqin kontent."""
    await update.message.reply_text("⏳ Kontent kalendari olinmoqda...")
    
    contents = get_kontent_calendar()
    
    if not contents:
        await update.message.reply_text("❌ Yaqin 7 kunda kontent yo'q.")
        return
    
    text = f"📅 *BUGUNGI & YAQIN KONTENT ({len(contents)} ta):*\n\n"
    
    for content in contents:
        sana = content.get("Sana", "")
        vaqt = content.get("Vaqt", "")
        loyiha = content.get("Loyiha", "")
        platforma = content.get("Platforma", "")
        turi = content.get("Turi", "")
        mavzu = content.get("Mavzu", "")
        holat = content.get("Holat", "")
        
        text += f"{holat} *{sana} — {vaqt}*\n"
        text += f"   🎬 {loyiha} | {platforma}\n"
        text += f"   📝 {turi} — {mavzu}\n\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def clients_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Aktiv mijozlar."""
    await update.message.reply_text("⏳ Mijozlar olinmoqda...")
    
    clients = get_mijozlar()
    
    if not clients:
        await update.message.reply_text("❌ Aktiv mijoz topilmadi.")
        return
    
    text = f"👥 *AKTIV MIJOZLAR ({len(clients)} ta):*\n\n"
    
    for client in clients:
        name = client.get("Mijoz", "")
        tel = client.get("Tel", "")
        platforma = client.get("Platforma", "")
        masul = client.get("Mas'ul", "")
        
        text += f"👤 *{name}*\n"
        text += f"   📞 {tel}\n"
        text += f"   📱 {platforma}\n"
        text += f"   👨‍💼 Mas'ul: {masul}\n\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Statistika."""
    await update.message.reply_text("⏳ Statistika olinmoqda...")
    
    tasks = get_vazifalar()
    videos = get_video_production()
    contents = get_kontent_calendar()
    clients = get_mijozlar()
    stats = get_dashboard_stats()
    
    text = "📊 *UMUMIY STATISTIKA*\n\n"
    text += f"👥 Aktiv mijozlar: {len(clients)} ta\n"
    text += f"📋 Bajarilmagan vazifalar: {len(tasks)} ta\n"
    text += f"🎬 Jarayondagi videolar: {len(videos)} ta\n"
    text += f"📅 Yaqin 7 kunda kontent: {len(contents)} ta\n"
    
    await update.message.reply_text(text, parse_mode="Markdown")


# ═════════════════════════════════════════════
# CALLBACK HANDLERS
# ═════════════════════════════════════════════

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Button callback — task status update."""
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data.startswith("task_done_"):
        task_id = data.replace("task_done_", "")
        success = update_task_status(task_id, "✅ Ha")
        
        if success:
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text(f"✅ Vazifa #{task_id} bajarildi deb belgilandi!")
        else:
            await query.message.reply_text("❌ Xatolik yuz berdi!")


# ═════════════════════════════════════════════
# AUTO JOBS
# ═════════════════════════════════════════════

async def daily_report(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Har kuni 09:00 da bugungi reja."""
    tasks = get_vazifalar(limit=3)
    videos = get_video_production()
    
    today_str = datetime.now(TZ).strftime("%d %B %Y")
    text = f"🌅 *ERTALAB HISOBOT — {today_str}*\n\n"
    
    if tasks:
        text += "📋 *Bugungi 3 ta asosiy vazifa:*\n"
        keyboard = []
        for task in tasks:
            task_id = task.get("ID", "")
            title = task.get("Vazifa", "")
            priority = task.get("Muhimligi", "")
            
            text += f"  {priority} {title}\n"
            keyboard.append([InlineKeyboardButton(
                f"✅ {title[:25]}", 
                callback_data=f"task_done_{task_id}"
            )])
        
        if videos:
            text += f"\n🎬 Jarayondagi videolar: {len(videos)} ta\n"
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )


# ═════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════

def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today_command))
    app.add_handler(CommandHandler("tasks", tasks_command))
    app.add_handler(CommandHandler("videos", videos_command))
    app.add_handler(CommandHandler("content", content_command))
    app.add_handler(CommandHandler("clients", clients_command))
    app.add_handler(CommandHandler("stats", stats_command))
    
    # Callbacks
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Jobs
    job_queue = app.job_queue
    tz = pytz.timezone(TIMEZONE)
    
    job_queue.run_daily(
        daily_report,
        time=datetime.now(tz).replace(
            hour=DAILY_HOUR, minute=0, second=0
        ).timetz(),
        name="daily_report",
    )
    
    logger.info("🚀 X-LINE BOT ISHGA TUSHDI!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
