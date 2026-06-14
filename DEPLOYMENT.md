# 🎬 X-LINE PRODUCTION MANAGER BOT
## Google Sheets + Telegram + Railway

---

## 📋 Bot nima qila oladi?

✅ Google Sheets dan **REAL-TIME** ma'lumot o'qiydi:
- 📋 VAZIFALAR — bajarilmagan topshiriqlar
- 🎬 VIDEO ISHLAB CHIQARISH — jarayondagi videolar
- 📅 KONTENT KALENDAR — bugungi & yaqin kontentlar
- 👥 MIJOZLAR — aktiv clientlar
- 📊 DASHBOARD — statistika

⏰ **Avtomatik vazifalar:**
- Har kuni 09:00 da bugungi reja yuboradi
- Tugmalar orqali status update qilish
- Google Sheets ga avtomatik yozish

---

## 🚀 DEPLOYMENT — 5 QADAM

### 1️⃣ **GITHUB SETUP**

```bash
# 1. GitHub da repo yarating
# https://github.com/new

# 2. Lokal klonlang
git clone https://github.com/USERNAME/xline-bot.git
cd xline-bot

# 3. Barcha fayllarni copy qiling
# bot_optimized.py, requirements.txt, .env.example, Dockerfile, railway.json, .gitignore

# 4. Push qiling
git add .
git commit -m "Initial commit: X-line bot"
git push origin main
```

### 2️⃣ **GOOGLE API SETUP**

1. **Console ga kiring:**
   - https://console.cloud.google.com
   - Yangi project yarating: `xline-bot`

2. **APIs yoqing:**
   - Search: "Google Sheets API" → Enable
   - Search: "Google Calendar API" → Enable
   - Search: "People API" → Enable

3. **Credentials yarating:**
   - APIs & Services → Credentials
   - "+ CREATE CREDENTIALS" → OAuth 2.0 Client ID
   - Application type: **Desktop App**
   - "Download as JSON" → `credentials.json` deb saqlang

4. **Faylni klonlangan repoga qo'ying:**
   ```bash
   cp ~/Downloads/credentials.json ./xline-bot/credentials.json
   ```

### 3️⃣ **LOCAL TEST (Ixtiyoriy)**

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt

# .env yarating
cp .env.example .env

# .env ni o'zgartiring
# TELEGRAM_TOKEN=sizning_tokeningiz
# ADMIN_CHAT_ID=sizning_chat_id
# SHEET_ID=sizning_sheet_id

# Ishga tushiring
python bot_optimized.py

# Telegram botda: /start, /today, /tasks, /videos, /content, /clients, /stats
```

### 4️⃣ **RAILWAY DEPLOYMENT**

**Variant A: Railway CLI (eng oson)**

```bash
# 1. Railway o'rnatish
npm install -g @railway/cli

# 2. Kirish
railway login

# 3. Repona kiring
cd xline-bot

# 4. Project yaratish
railway init
# → "X-line Bot" ni aytib ber

# 5. Variables qo'shish
railway variables set TELEGRAM_TOKEN="8604308140:AAFfknhObPupAJ3nheL0HxOhSPnTTRZFctA"
railway variables set ADMIN_CHAT_ID="332723689"
railway variables set SHEET_ID="1fMpRJEFOdHLeVLLrhf38LrD4Kp5GGf4FEqdBs3pB1ss"

# 6. Deploy
railway up
```

**Variant B: Railway Web Dashboard**

1. https://railway.app ga kiring
2. "New Project" → "Deploy from GitHub"
3. Sizning `xline-bot` repo ni tanlang
4. Railway variables qo'shish:
   - `TELEGRAM_TOKEN`
   - `ADMIN_CHAT_ID`
   - `SHEET_ID`
5. Deploy qilish

### 5️⃣ **CREDENTIALS.JSON QANDAY QILISH**

⚠️ **MASALA:** `credentials.json` GitHub ga push qila olmaysiz (xavfli!)

**Yechim:**

```bash
# 1. .gitignore da credentials.json allaqachon bor
# (push bo'lmaydi)

# 2. Railway da:
   - File type: "credentials.json"
   - Content: credentials.json dan nusxa qiling (full JSON)
   - Railway: Settings → File Storage → Upload

# YOKI

# 3. Base64 qilish:
cat credentials.json | base64 > creds.b64
# Railway variable: CREDENTIALS_BASE64=base64_content

# bot.py ni modify:
import base64
creds_json = base64.b64decode(os.getenv("CREDENTIALS_BASE64")).decode()
with open("credentials.json", "w") as f:
    f.write(creds_json)
```

---

## 📱 BOT BUYRUQLARI

| Buyruq | Nima qiladi |
|--------|-------------|
| `/start` | Bosh menyu |
| `/today` | Bugungi 3 ta vazifa (✅ tugma bilan) |
| `/tasks` | Barcha bajarilmagan topshiriqlar |
| `/videos` | Jarayondagi videolar |
| `/content` | Bugungi & yaqin kontent |
| `/clients` | Aktiv mijozlar |
| `/stats` | Umumiy statistika |

---

## 🔄 GOOGLE SHEETS INTEGRATSIYASI

**Bot o'qiydi:**
- ✅ VAZIFALAR — Bajarildi = ❌ Yo'q
- ✅ VIDEO ISHLAB CHIQARISH — Holat = 🔄 Jarayonda
- ✅ KONTENT KALENDAR — Sana = bugun + 7 kun
- ✅ MIJOZLAR — Holat = ✅ Aktiv

**Bot yozadi:**
- ✅ VAZIFALAR — Status update (tugma bosilsa)

---

## 🛠️ TROUBLESHOOTING

### Bot ishlamayapti?

```bash
# Railway da logs ko'ring
railway logs

# Local test qiling
python bot_optimized.py

# Errors:
# - "Credentials not found" → credentials.json qo'shing
# - "TELEGRAM_TOKEN error" → .env da token to'g'ri kiritilganini tekshiring
# - "Sheet not found" → SHEET_ID to'g'rimi?
```

### Credentials.json bilan muammo?

```bash
# 1. Google Console da token refresh qiling
# 2. token.pickle faylni o'chiring (agar bor bo'lsa)
# 3. Birinchi ishga tushirish vaqtida qayta auth qiling
```

### Google Sheets update bo'lmayapti?

```bash
# 1. Sheets API yoqilganini tekshiring
# 2. Bot user ga Sheets edit access bormi?
# 3. Sheet name (tab nomi) to'g'rimi? (katta-kichik harfga e'tibor!)
```

---

## 📁 FAYL TUZILMASI

```
xline-bot/
├── bot_optimized.py         # 🤖 ASOSIY KOD
├── requirements.txt          # 📦 Kutubxonalar
├── Dockerfile               # 🐳 Container
├── railway.json             # 🚂 Railway config
├── .gitignore              # 🙈 Git ignore
├── .env.example            # 📋 Template
├── credentials.json        # 🔑 Google (gitignore da!)
├── token.pickle            # 🔐 Auto-generated
└── README.md               # 📖 Bu fayl
```

---

## 🎯 KEYINGI QADAMLAR

1. ✅ GitHub repo yarating
2. ✅ Google API credentials olish
3. ✅ Railway projektga deploy qilish
4. ✅ Bot test qilish (`/today`, `/tasks`)
5. ✅ Google Sheets dan avtomatik o'qish
6. 🚀 Production!

---

## 💡 ADVANCED

**Kengaytirish imkoniyatlari:**
- Webhook o'rniga polling (Railway unlimited)
- Database qo'shish (SQLite/PostgreSQL)
- Admin panel yaratish
- Scheduled reports
- Analytics

---

## 📞 SUPPORT

Muammo bo'lsa:
1. Railway logs ko'ring
2. GitHub issues ochish
3. Google Sheets share qilish (debug uchun)

---

**Muvaffaq bo'lishingizni tilaymiz! 🚀**
