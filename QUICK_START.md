# QUICK START GUIDE - Canteen Management System Enhanced v4.0

## 🚀 QUICK START (5 STEPS)

### Step 1: LOGIN
```
Username: manager
Password: manager123
(or admin/admin123 for full access)
```

### Step 2: TODAY'S BATCH PREP
```
Navigate: 🧑‍🍳 Batch Prep
SECTION 1: Enter quantities to prepare
  └─ Panchratna Thali: 20
  └─ Kadhi Pakoda: 15
  └─ Rajma Thali: 12
```
✓ System auto-deducts rice, dal, vegetables from inventory

### Step 3: RECORD SALES
```
Navigate: 💰 Sales Entry (SIMPLE MODE)
Select menu item → Enter qty sold → Payment mode
  └─ Panchratna Thali: 18 sold (Cash)
  └─ Kadhi Pakoda: 14 sold (UPI)
  └─ Rajma Thali: 11 sold (Card)
```
✓ System auto-deducts remaining stock & calculates profit

### Step 4: LOG WASTAGE
```
Navigate: ♻️ Waste Manager
Item: Rice
Qty: 0.5 kg
Reason: Spoilage
Cost: ₹20
```
✓ Cost shows on dashboard & report

### Step 5: VIEW DAILY REPORT
```
Navigate: 📋 Daily Report
See:
  ✓ Total Revenue: ₹3,500
  ✓ COGS: ₹2,100
  ✓ Wastage: ₹20
  ✓ Net Profit: ₹1,380
```

---

## 📊 DASHBOARD (Main Hub)

**KPI Cards:**
- 💰 **Total Revenue** - Sum of all meals sold today
- 🍛 **Meals Served** - Total count
- 📈 **Net Profit** - Revenue - COGS - Wastage - Expenses
- ♻️ **Wastage Cost** - Total cost of items wasted
- ⚠️ **Low Stock** - Items below minimum level

**Today's Sales Table:** Shows each meal sold with payment mode

**Low Stock Alerts:** Items needing purchase (red warning)

---

## 💰 SALES ENTRY (SIMPLIFIED)

**Most Common Task - Make It 3 Clicks:**

1. Click **💰 Sales Entry**
2. Enter quantities for each menu item
3. Click **✅ Save & Auto-Deduct Stock**

**That's it!** System handles:
- ✓ Looking up recipes
- ✓ Calculating ingredient quantities
- ✓ Deducting from stock
- ✓ Recording revenue
- ✓ Calculating profit

---

## 🧑‍🍳 BATCH PREPARATION (2-Section)

### **SECTION 1: Batch Prep**
```
Menu Item               | Qty to Prepare
────────────────────────────────────────
Panchratna Dal Thali   |      20
Kadhi Pakoda Thali     |      15
Rajma Thali            |      12
```
→ Click Save → Stock deducted per recipe

### **SECTION 2: Sales from Batch**
```
Menu Item               | Qty Sold | Wastage | Payment
───────────────────────────────────────────────────────
Panchratna Dal Thali   |    18    |    2    | Cash
Kadhi Pakoda Thali     |    14    |    1    | UPI
Rajma Thali            |    11    |    1    | Card
```
→ Click Save → Revenue recorded, profit calculated

---

## ♻️ WASTE MANAGER (Dedicated Section)

**Track Every Waste Item:**

| Field | Example |
|-------|---------|
| Item Name | Rice, Vegetables, Dal |
| Quantity | 0.5 kg |
| Reason | Spoilage, Prep Error, Burn, etc. |
| Estimated Cost | ₹25 |

**Result:**
- Logged to database
- Shows on dashboard
- Included in profit calculation
- Daily log shows all entries
- Total wastage cost calculated

---

## 📦 INVENTORY MANAGEMENT

### **Add Received Stock**
```
Item: Rice
Quantity: 50 kg
Cost/Unit: ₹40/kg
→ Stock updated (50 × ₹40 = ₹2000 total)
```

### **Update Stock Level**
```
If physical count differs from system
→ Set actual stock level
```

### **Remove Item**
```
Delete item from inventory permanently
(Use carefully - cannot undo)
```

### **View by Category**
```
Filter buttons: All / Dry / Fresh / Dairy / Packaging
Shows stock status (✓ OK or ⚠ LOW)
```

---

## 👥 USER MANAGEMENT (Admin Only)

### **Add New User**
```
Username: jco_smith
Full Name: JCO Smith
Rank: JCO
Contact: 9876543210
Password: SecurePass123
Role: Manager
```

### **Reset Password**
```
Select User → Enter New Password
Changes take effect immediately
```

---

## 📋 DAILY REPORT (Comprehensive)

**Auto-Generated Report Shows:**

1. **Sales Summary by Date**
   - Meals served per day
   - Revenue per day
   - COGS per day
   - Profit per day

2. **Financial Summary**
   - Total Revenue
   - Total COGS
   - Wastage Cost
   - **Net Profit** (Bottom Line)

3. **Payment Breakdown**
   - Cash % and amount
   - UPI % and amount
   - Card % and amount

4. **Period Selection**
   - 1 Week (7 days)
   - Fortnight (15 days)
   - Monthly (30 days)
   - Quarterly (90 days)

---

## 🔐 USER ROLES & ACCESS

### **ADMIN** (Full Access)
```
Can Do Everything:
✓ Dashboard (view)
✓ Sales Entry
✓ Batch Prep
✓ Inventory (add/update/remove)
✓ Waste Manager
✓ Daily Reports
✓ Master Data
✓ User Management (create/edit)
```

### **MANAGER** (Operations)
```
Can Do:
✓ Dashboard
✓ Sales Entry (Primary task)
✓ Batch Preparation
✓ Inventory (view & update stock)
✓ Daily Reports
✗ User Management
```

### **OFFICER** (View Only)
```
Can Do:
✓ Dashboard (view)
✗ Everything else (read-only)
```

### **WASTE MANAGER** (Specialized)
```
Can Do:
✓ Waste Manager (full access)
✓ Dashboard (partial)
✗ Other functions
```

---

## 🔗 DATA CONNECTIONS

### **Stock Deduction Flow**
```
Sales Entry: 3 meals sold
        ↓
Lookup Recipe: 
  Panchratna = 0.22kg dal + 0.30kg rice + 0.20kg roti + ...
        ↓
Calculate: 3 × (0.22, 0.30, 0.20, ...) 
        ↓
Deduct from Inventory:
  dal stock = dal stock - 0.66
  rice stock = rice stock - 0.90
  roti stock = roti stock - 0.60
  ...
        ↓
Update Batch Log & Sales Record
```

### **Profit Calculation**
```
Revenue (Selling Price × Qty Sold)
  - COGS (Cost × Qty Sold)
  - Wastage Cost
  - Expenses
  = NET PROFIT
```

---

## ⚠️ IMPORTANT REMINDERS

1. **Stock Deduction is AUTOMATIC**
   - No manual deduction needed
   - Based on recipe quantities
   - Cannot be undone (but can update stock level)

2. **COGS is AUTO-CALCULATED**
   - Uses ingredient cost per unit
   - Updated based on actual ingredient qty
   - More accurate than fixed costs

3. **Wastage Impacts Profit**
   - Every waste entry reduces net profit
   - Visible in daily report
   - Helps track operational efficiency

4. **Passwords are Hashed**
   - Secure SHA256 encryption
   - Cannot see plain password
   - Use reset function to change

5. **All Data is Persistent**
   - SQLite database (canteen.db)
   - All entries saved
   - Historical tracking available

---

## 🎨 COLOR MEANINGS

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Good / OK / Saved |
| 🔴 **Red** | Warning / Low Stock / Issue |
| 🟠 **Orange** | Wastage / Important |
| 🔵 **Blue** | Information / Secondary |
| 🟡 **Saffron** | Primary / Important action |

---

## 💾 DATA BACKUP

**Where data is stored:**
```
/Users/rohan/Desktop/canteen/canteen.db
```

**Regular backup:**
```
cp canteen.db canteen_backup_$(date +%Y%m%d).db
```

---

## 🆘 COMMON ISSUES

**Q: Stock went negative?**
A: Manual correction via "Update Stock" or check recipe quantities

**Q: Can't find menu item?**
A: Ensure it's set to "active" in Master Data

**Q: Wrong revenue amount?**
A: Check selling price in menu master

**Q: Forgot password?**
A: Admin can reset via User Management

**Q: Need to undo sale?**
A: Update stock level manually for now

---

## 📞 SUPPORT

**Default Test Accounts:**
- admin / admin123
- manager / manager123
- officer / officer123
- waste / waste123

**Database location:**
- canteen.db in application folder

**Version:**
- Enhanced v4.0

---

## ✅ CHECKLIST FOR DAILY USE

```
☐ Morning: Open app, check dashboard
☐ Morning: Run batch prep for menu items
☐ During: Record sales (meals sold)
☐ Throughout: Log any wastage
☐ Evening: Review daily report
☐ Evening: Verify revenue & profit
☐ Before closing: Check low stock alerts
☐ Weekly: Review waste patterns
☐ Monthly: Generate period reports
```

---

**जय हिन्द** 🇮🇳

For questions or issues, refer to ENHANCEMENTS.md for detailed documentation.
