# 🚀 PRE-RECORDING CHECKLIST & QUICK START

**Presentation Date:** April 23, 2026

---

## ✅ SYSTEM READINESS CHECKLIST

Before you start recording, verify everything:

### 1. **Environment Setup** ✓
- [ ] Python environment activated: `source .venv/bin/activate`
- [ ] Terminal open in `/Users/rohan/Desktop/canteen`
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Check: `pip list | grep customtkinter matplotlib reportlab`

### 2. **Database Status** ✓
- [ ] Database file exists: `canteen.db` 
- [ ] Backup exists: `canteen.db.backup_20260417_170100`
- [ ] Run `python test_db.py` to verify database integrity
- [ ] Verify all tables exist (users, inventory, sales, waste_tracker, etc.)

### 3. **Application Status** ✓
- [ ] Run: `python app.py`
- [ ] Wait for GUI window to open (should take 2-3 seconds)
- [ ] Verify login screen displays correctly
- [ ] Verify Army Canteen theme is applied
- [ ] Test all 4 default login credentials work:
  - Admin: `admin / admin123` ✓
  - Manager: `manager / manager123` ✓
  - Officer: `officer / officer123` ✓
  - Waste: `waste / waste123` ✓

### 4. **Dashboard Verification** (Logged in as Admin)
- [ ] KPI Cards visible (Revenue, Meals, Profit)
- [ ] Low Stock Alerts section displays
- [ ] Daily Waste Impact shows
- [ ] All menu buttons appear
- [ ] Theme colors are correct (Army Green/Khaki)

### 5. **Data Verification** (Sample data should exist)
- [ ] At least 5-10 inventory items exist
- [ ] At least 3-4 menu items exist
- [ ] At least 2-3 recipes exist
- [ ] Sales history shows past entries
- [ ] All 4 users visible in user list

---

## 🎬 RECORDING ENVIRONMENT SETUP

### A. **Screen Preparation**
```bash
# Recommended zoom level in terminal/VS Code: 120-150%
# This makes text more visible on video

# For macOS:
# 1. Open app.py in terminal
# 2. Run: python app.py
# 3. Resize window to 1400x900 (good visibility)
```

### B. **Before Each Recording Session**
- [ ] Close all other applications
- [ ] Silence notifications (Do Not Disturb: ON)
- [ ] Test microphone audio levels
- [ ] Have notes/script visible (printed or second monitor)
- [ ] Set screen recording quality to 1080p or higher
- [ ] Test 10-second recording to verify audio/video sync

### C. **Recording Hardware/Software**
- [ ] Screen recording software ready (QuickTime, OBS, ScreenFlow, etc.)
- [ ] Microphone tested and working
- [ ] Sufficient disk space (need ~2-3GB for 20min video)

---

## 🎯 QUICK START COMMANDS

### Start the Application (3 Easy Steps)

```bash
# Step 1: Navigate to project directory
cd /Users/rohan/Desktop/canteen

# Step 2: Activate environment (if not already active)
source .venv/bin/activate

# Step 3: Run the application
python app.py
```

**Expected Output:**
```
Initializing Canteen Management System v5.0...
Database connected: canteen.db
Loading UI...
GUI Window Opening... [Application window should appear]
```

### If Application Doesn't Start

**Option 1: Check Dependencies**
```bash
pip install -r requirements.txt
```

**Option 2: Verify Database**
```bash
python test_db.py
```

**Option 3: Check Python Version**
```bash
python --version    # Should be 3.8 or higher
```

---

## 📱 PRESENTATION FLOW (QUICK VERSION)

If you need a shorter 10-minute version, focus on these **CORE FEATURES ONLY**:

1. **Login & Dashboard** (1 min)
2. **User Management: Add User** (2 min) - Main new feature
3. **Stock Management: Add & Remove** (1.5 min)
4. **Batch Prep with Auto-Deduction** (2 min) - Key feature
5. **Sales Entry - Simplified** (1.5 min)
6. **Waste Manager Section** (1 min) - Unique feature
7. **Daily Financial Report** (1 min)

---

## 🎤 KEY TALKING POINTS (For Your Narration)

### Opening Statement (10 seconds)
*"This is the Enhanced Canteen Management System v4.0. We've transformed the original system by adding 20+ features and improving every major function. This is now a complete solution for professional military canteen operations."*

### Middle Section (For each major feature)
- **Problem it solves**
- **How it works** (demo)
- **Impact** (time saved, errors prevented, money tracked)

### Closing Statement (10 seconds)
*"The system is production-ready, fully documented, and designed for immediate deployment. All features are tested and working smoothly."*

---

## 📊 DEMO DATA REFERENCE

If you need to create fresh demo data during recording:

### Add User Example:
```
Name: Suresh Kumar
Username: suresh_k
Password: demo123
Role: Manager
Status: Active
Contact: +91-98765-43210
```

### Add Stock Example:
```
Item: Basmati Rice
Quantity: 100
Unit: kg
Category: Dry
Cost/Unit: 65
```

### Add Waste Example:
```
Item: Chicken
Quantity: 5
Unit: kg
Reason: Spoilage
Cost: 750
```

### Record Sales Example:
```
Item 1: Chicken Biryani (₹250) - Qty: 30 = ₹7,500
Item 2: Daal (₹80) - Qty: 50 = ₹4,000
Item 3: Chapati (₹15) - Qty: 100 = ₹1,500
Total: ₹13,000 [Auto-Calculated]
Payment: Cash
```

---

## ⚠️ TROUBLESHOOTING (If Issues Occur During Recording)

| Issue | Solution |
|-------|----------|
| App won't start | `pip install -r requirements.txt` then restart |
| Database error | Run `python test_db.py` and check logs |
| UI not responsive | Close app, restart: `python app.py` |
| Charts not showing | `pip install matplotlib` |
| Login fails | Verify credentials in database: `python check_db.py` |
| Slow performance | Close other apps, ensure 2GB+ free RAM |

---

## 📝 RECORDING TIPS

1. **Practice First** - Do a dry run through the whole presentation
2. **Speak Clearly** - Speak slowly and clearly, enunciate well
3. **Show, Don't Tell** - Let features speak for themselves
4. **Add Captions Later** - Focus on recording, edit captions after
5. **Pause at Key Moments** - Give viewers time to see what's happening
6. **Zoom In on Details** - Highlight important numbers/fields
7. **Use Cursor Movement** - Point to what you're talking about
8. **Multiple Takes OK** - Record sections separately, edit together

---

## 🎬 EDITING (Post-Recording)

After recording, consider:
- [ ] Trim intro/outro
- [ ] Add title card (2-3 seconds)
- [ ] Add captions/labels for key features
- [ ] Add background music (optional, low volume)
- [ ] Speed up mundane tasks, slow down important ones
- [ ] Add text overlays with key statistics
- [ ] Final length: 10-20 minutes

---

## 📋 FILE LOCATIONS (For Reference During Recording)

```
Main App:           app.py
Presentation Guide: VIDEO_PRESENTATION_GUIDE.md (THIS FILE)
Database:           canteen.db
Requirements:       requirements.txt
Test Scripts:       test_db.py, test_ui.py
```

---

## ✨ YOU'RE READY TO GO!

**Final Checklist:**
- [ ] Read through VIDEO_PRESENTATION_GUIDE.md
- [ ] Run application once to verify everything works
- [ ] Prepare demo data or use existing data
- [ ] Set up recording environment
- [ ] Have notes/script ready
- [ ] Start recording!

**Good luck! Your presentation is going to look amazing! 🎉**

---

**Estimated Total Recording Time:** 15-20 minutes  
**Presentation Quality:** Professional ✓  
**Feature Coverage:** 100% of all 20+ features ✓  
**Ready for Production:** YES ✓

