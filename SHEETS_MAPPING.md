# X-LINE BOT — GOOGLE SHEETS MAPPING

## 📊 SHEETS STRUCTURE

### VAZIFALAR (Tasks)
```
Columns:
- A: ID (T-01, T-02...)
- B: Vazifa (Task title)
- C: Javobgar (Responsible person)
- D: Vazifa beruvchi (Assigned by)
- E: Deadline (DD/MM/YYYY)
- F: Bajarildi (Status: ✅ Ha / ❌ Yo'q)
- G: Muhimligi (Priority: 🔴 Yuqor / 🟡 O'rta / 🟢 Past)
- H: Izoh (Notes)

Bot o'qiydi:
- Bajarildi = ❌ Yo'q (pending tasks)
- Sort by: Deadline (nearest first)
- Limit: 20 tasks

Bot yozadi:
- Column F: Bajarildi (when button clicked)
```

### VIDEO ISHLAB CHIQARISH (Video Production)
```
Columns:
- A: ID (V-01, V-02...)
- B: Mavzu (Subject)
- C: Loyiha (Project)
- D: Ssenariy (Scenario status)
- E: Suratga olish (Filming status)
- F: Montaj (Editing status)
- G: Post qoyishga masul (Responsible for posting)
- H: Deadline
- I: Holat (Status: ✅ Tayyor / 🔄 Jarayonda / ⏳ Kutilmoqda)

Bot o'qiydi:
- Filter: Holat like "🔄" OR "⏳"
- Shows: Current progress
```

### KONTENT KALENDAR (Content Calendar)
```
Columns:
- A: ID
- B: Sana (Date: MM/DD/YYYY)
- C: Vaqt (Time: HH:MM)
- D: Loyiha (Project)
- E: Platforma (Instagram, TG, YouTube)
- F: Turi (Type: Reels, Story, Post, Image)
- G: Mavzu (Topic)
- H: Mas'ul (Responsible)
- I: Chiqadigan sana (Publishing date)
- J: Holat (Status: 🔄 Tayyor / ✅ Chiqdi / ❌ Bekor)

Bot o'qiydi:
- Filter: Today ≤ Sana ≤ Today + 7 days
- Sort by: Sana ascending
```

### MIJOZLAR (Clients)
```
Columns:
- A: Mijoz ID (M-1, M-2...)
- B: Mijoz (Client name)
- C: Brend (Brand)
- D: Tel (Phone)
- E: Platforma (Social media platforms)
- F: Mas'ul (Responsible manager)
- G: Yordamchi (Assistant)
- H: Holat (Status: ✅ Aktiv / ⏸️ Pauza / ❌ Tugagan)
- I: Izoh (Notes)

Bot o'qiydi:
- Filter: Holat = ✅ Aktiv
- Shows: All active clients with contact info
```

### DASHBOARD (Statistics)
```
Key metrics:
- B2: Bugun (Today)
- B4: Bugun chiqadigan kontent (Content today)
- B5: Bugun suratga olish (Shooting today)
- B6: Bugun meeting (Meetings today)
- F2: Aktiv mijozlar
- F3: Aktiv ko'tarilgan mavzular
- F4: Bu oy daromad
```

### MOLIYA (Finance)
```
Columns:
- A: ID
- B: Oy (Month)
- C: Loyiha (Project)
- D: Daromad (Income)
- E: Xarajat turi (Expense type)
- F: Xarajat (Expense amount)
- G: To'lov sanasi (Payment date)
- H: To'landi (Status: ✅ To'landi / ❌ To'lanmadi / ⏳ Kutilmoqda)
```

### HODIMLAR (Team)
```
Columns:
- A: Ism (Name)
- B: TG ID (Telegram ID)
- C: Rol (Role: Manager, Videograph, etc.)
- D: Status
- E: ID_Fayl
- F: Tel
- G: Email
- H: Maosh (Salary)
- I: Ishga kirgan sana (Start date)
- J: Holat (Status: ✅ Aktiv / 🆕 Yangi)
```

### UCHRASHUVLAR (Meetings)
```
Columns:
- A: ID
- B: Sana (Date)
- C: Vaqt (Time)
- D: Turi (Type: Mijoz, Yangi mijoz, Jamoa)
- E: Kim bilan (With whom)
- F: Maqsad (Purpose)
- G: Qatnashuvchilar (Participants)
- H: Holat (Status: ✅ Bo'ldi / ⏳ Kutilmoqda)
```

---

## 🔄 BOT DATA FLOW

### READ (Bot → Sheet)
```
/today → VAZIFALAR (Bajarildi=❌) → 3 ta
/tasks → VAZIFALAR (Bajarildi=❌) → All
/videos → VIDEO ISHLAB CHIQARISH (Holat=🔄,⏳)
/content → KONTENT KALENDAR (Date range)
/clients → MIJOZLAR (Holat=✅)
/stats → DASHBOARD metrics
```

### WRITE (Button → Sheet)
```
Button click: ✅ {Task}
→ Update VAZIFALAR[F] = ✅ Ha
→ Confirmation to user
```

### AUTO (Scheduler)
```
09:00 daily → /today report (first 3 tasks)
10:00 daily → Client reminders (every 3 days)
```

---

## 🔑 CRITICAL COLUMN NAMES (CASE-SENSITIVE)

**Bot foydalaniladigan EXACT column names:**

1. **VAZIFALAR**
   - `ID`, `Vazifa`, `Javobgar`, `Deadline`, `Bajarildi`, `Muhimligi`

2. **VIDEO ISHLAB CHIQARISH**
   - `ID`, `Mavzu`, `Loyiha`, `Holat`, `Deadline`

3. **KONTENT KALENDAR**
   - `Sana`, `Vaqt`, `Loyiha`, `Platforma`, `Turi`, `Mavzu`, `Holat`

4. **MIJOZLAR**
   - `Mijoz`, `Tel`, `Platforma`, `Mas'ul`, `Holat`

⚠️ **AGAR COLUMN NOMI BOSHQACHA BO'LSA:**
- Bot "KeyError" xatosini beradi
- `bot.py` dagi column nomlarini o'zgartiring

---

## 🛠️ CUSTOMIZE

### Status symbollarini o'zgartirish

`bot_optimized.py` da:
```python
# FILTER EXAMPLES:

# Vazifa status
if t.get("Bajarildi", "") == "❌ Yo'q":  # ← o'zgartiring

# Video status
if "🔄" in v.get("Holat", ""):  # ← o'zgartiring

# Kontent status
if today <= item_date <= today + timedelta(days=7):  # ← kunlarni o'zgartiring

# Client status
if m.get("Holat", "") == "✅ Aktiv":  # ← o'zgartiring
```

### Sheet selection

```python
# Boshqa sheet o'qish uchun:
sheet = gc.open_by_key(SHEET_ID).worksheet("SHEET_NAME")
# "SHEET_NAME" ni o'zgartiring
```

---

## 📊 MISOL: Yangi column qo'shish

Agar VAZIFALAR sheetga "Javobgar TG ID" column qo'shsangiz:

```python
def get_vazifalar(limit: int = 10) -> List[Dict]:
    # ...existing code...
    for task in pending:
        task_id = task.get("ID", "")
        title = task.get("Vazifa", "")
        javobgar_tg = task.get("Javobgar TG ID", "")  # ← yangi
        # ...
```

---

## ✅ READY TO DEPLOY!

Agar column nomlar to'g'rimi, bot avtomatik ishlaydi! 🚀
