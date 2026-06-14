# ⚡ X-LINE BOT — TEZKOR BOSHLASH

## 🎯 30 DAQIQADA DEPLOY QILISH

### 1️⃣ GitHub Repo (2 daqiqa)
```bash
# 1. https://github.com/new
# 2. "xline-bot" repo yarating
# 3. Clone qiling va fayllarni copy qiling
git clone https://github.com/YOUR_USERNAME/xline-bot.git
cd xline-bot
# (barcha .py, .txt, .json, .yml fayllarni copy qiling)
git push origin main
```

### 2️⃣ Google Credentials (5 daqiqa)
```
1. https://console.cloud.google.com → New Project
2. APIs: Google Sheets API + Calendar API + People API (Enable)
3. Credentials → OAuth 2.0 Desktop App
4. credentials.json yuklab oling
5. Bot.py bilan bir joyga qo'ying
```

### 3️⃣ Telegram Token (1 daqiqa)
```
1. Telegramda @BotFather ga yozing: /newbot
2. Botga nom bering: XlineManagerBot
3. Token nusxa oling
```

### 4️⃣ Railway Deploy (10 daqiqa)
```
1. https://railway.app → Sign Up (GitHub bilan)
2. "New Project" → "Deploy from GitHub"
3. xline-bot repo tanlang
4. Environment variables qo'shish:
   TELEGRAM_TOKEN = 8604308140:AAF...
   ADMIN_CHAT_ID = 332723689
   SHEET_ID = 1fMpRJEFOdHLeVLLrhf38LrD4Kp5GGf4FEqdBs3pB1ss
5. "Deploy" tugmasi — DONE! 🚀
```

### 5️⃣ Test Qilish (1 daqiqa)
```
Telegramda botga /start yozing
→ Menyu chiqadi
→ /today, /tasks, /videos, /content, /clients, /stats
```

---

## 📝 SHEETDA KERAKLI COLUMN NOMLAR

**VAZIFALAR sheet:**
- ID, Vazifa, Javobgar, Deadline, Bajarildi, Muhimligi

**VIDEO ISHLAB CHIQARISH sheet:**
- ID, Mavzu, Loyiha, Holat, Deadline

**KONTENT KALENDAR sheet:**
- Sana, Vaqt, Loyiha, Platforma, Turi, Mavzu, Holat

**MIJOZLAR sheet:**
- Mijoz, Tel, Platforma, Mas'ul, Holat

---

## ✅ MISOL: Sheetdan data o'qish

Bot avtomatik:
- Har kuni 09:00 da `/today` natijasini yuboradi
- Tugmaga bosilsa, Google Sheets da status update qiladi
- Har 7 kunda kontent oladi

---

## 🐛 XATO YUZASA

| Xato | Yechim |
|------|--------|
| "Credentials not found" | credentials.json ni qo'shish |
| "TELEGRAM_TOKEN error" | Railway variables ni tekshirish |
| "Sheet not found" | Sheet names to'g'rimi? (Case-sensitive) |
| Bot ishlamayapti | Railway logs ko'ring: `railway logs` |

---

## 🚀 DONE!

Endi botingiz **24/7** ishlaydi! 🎉

Har kuni bugungi rejani Telegramga yuboradi, tugmalar bilan status update qila olasiz, barcha ma'lumot Google Sheetsdan olinadi.

**Agar muammo bo'lsa:** Railway/GitHub logs ko'ring, credentials.json va environment variables to'g'rimi?

---

**JIgar, tayyor bo'ldingmi? GitHub linkni bersang, barchasini setup qilib beraman!** 💪
