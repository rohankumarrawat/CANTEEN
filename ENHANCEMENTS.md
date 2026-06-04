# 🇮🇳 CANTEEN MANAGEMENT SYSTEM - ENHANCED VERSION 4.0

## ✨ MAJOR ENHANCEMENTS IMPLEMENTED

### 1. **STOCK MANAGEMENT** ✓
- **Add Received Stock**: Record incoming inventory with quantity & cost/unit
- **Update Stock Level**: Manually adjust stock for corrections
- **Remove Stock Items**: Delete inventory items permanently
- **Real-time Stock Alerts**: Low-stock warnings on dashboard
- **Stock Ledger**: Track all stock transactions
- **Category Filtering**: View stock by Dry/Fresh/Dairy/Packaging

**Database Tables Used:**
- `inventory` - Main stock ledger
- `goods_received` - Receiving transaction history
- `stock_ledger` - Detailed transaction log

---

### 2. **USER MANAGEMENT** ✓
- **Add New Users**: Create staff accounts with roles
- **Set User Roles**: Assign roles (Manager, Officer, Waste Manager)
- **Reset Passwords**: Change user passwords securely
- **User Status**: Active/Inactive user tracking
- **Role-based Navigation**: Different menu items based on role
- **User Information**: Name, Rank, Contact details

**Default Users:**
```
Admin:      admin / admin123
Manager:    manager / manager123
Officer:    officer / officer123
Waste:      waste / waste123
```

**Database Table:**
- `users` - User accounts with hashing
- `user_roles` - Role assignments

---

### 3. **WASTE MANAGER SECTION** ✓
- **Dedicated Waste Page**: Full page for waste tracking
- **Record Wastage**: Log food items wasted with quantity & reason
- **Waste Reasons**: Spoilage, Prep Error, Plate Waste, Burn, Storage, Return, Expiry
- **Cost Tracking**: Record estimated cost of wastage
- **Daily Log**: View all wastage recorded today
- **Total Wastage Cost**: Summary of daily wastage
- **Recorded By**: Track who logged each waste entry

**Features:**
- Simple form to enter item, qty, reason, cost
- Auto-calculation of total waste cost
- Real-time dashboard impact (shows on KPI)
- Daily waste log with full details

**Database Table:**
- `waste_tracker` - Waste transaction history

---

### 4. **DAILY REPORT SECTION** ✓
**Comprehensive Report with:**
- **Period Selection**: 1 Week / Fortnight / Monthly / Quarterly
- **Sales Summary**: Date-wise breakdown with meals, revenue, COGS, profit
- **Financial Summary**: Revenue, COGS, Waste Cost, Net Profit
- **Payment Breakdown**: Cash/UPI/Card payment mode analysis
- **KPI Cards**: Revenue, Meals Served, Net Profit display
- **Professional Letterhead**: Official army canteen format
- **Sign-off Section**: Space for manager/officer/OIC signatures

**Report Includes:**
- Total revenue with payment breakdown
- Cost of goods sold (COGS)
- Wastage impact on profit
- Expense category breakdown
- Date-range filtering

---

### 5. **BATCH PREPARATION - 2 SECTION** ✓

**SECTION 1: Batch Preparation**
- Select menu item
- Enter quantity to prepare
- Auto-deduct stock based on recipes
- Record batch preparation with timestamp
- Link to menu recipes

**SECTION 2: Sales from Batch**
- Enter quantity sold
- Record wastage (separate field)
- Select payment mode (Cash/UPI/Card)
- Auto-deduct from prepared batch
- Calculate COGS from actual used quantity

**Workflow:**
```
Batch Prep (Qty Prepared) → Deduct Stock
                         ↓
Sales (Qty Sold) + Wastage → Record Revenue
                         ↓
Auto-calculate Profit
```

---

### 6. **SIMPLE SALES ENTRY** ✓
**One-Click Sales:**
- **Menu Selection**: Dropdown list of all active menu items
- **Qty Input**: Simple number entry
- **Auto-Calculation**: Shows total revenue per item
- **Payment Mode**: Select Cash/UPI/Card
- **Instant Deduction**: Stock automatically deducted per recipe
- **COGS Auto-Calculated**: Based on ingredient costs

**Form Layout:**
```
┌─ QUICK SALES ENTRY ─────────────────────────┐
│ Menu Item    │ Price │ Qty Sold │ Total     │
├─────────────────────────────────────────────┤
│ 🍛 Panchratna │ ₹70   │    3    │ ₹210     │
│ 🍽️  Kadhi     │ ₹50   │    2    │ ₹100     │
│ ...          │ ...   │ ...    │ ...      │
└─────────────────────────────────────────────┘
```

---

### 7. **CONNECTED STOCK DEDUCTION** ✓
**Automatic Stock Management:**
```
Sales Entry (Select Item + Qty)
        ↓
Lookup Recipe (ingredients per unit)
        ↓
Calculate Required Stock
(Qty Sold × Qty Per Unit)
        ↓
Deduct from Inventory
(UPDATE stock = stock - deduction)
        ↓
Track in Stock Ledger
        ↓
Alert if Low Stock (<min_level)
```

**Example:**
- User sells 3x Panchratna Thali
- Recipe: 0.22kg Dal Mix + 0.30kg Rice + 0.20kg Roti + ...
- System deducts: 0.66kg Dal, 0.9kg Rice, 0.6kg Roti, etc.
- Updates `inventory.stock` for each ingredient

---

### 8. **FINANCIAL RECORDS** ✓

**Money Tracking:**
- **Revenue Recording**: Automatic per sale
- **COGS Calculation**: Based on ingredient costs × quantity used
- **Profit Calculation**: Revenue - COGS - Wastage - Expenses
- **Payment Modes**: Cash/UPI/Card tracking
- **Expense Categories**: Dry/Fresh/Dairy/Packaging/Repairs/Property
- **Financial Summary**: Period-wise profit/loss analysis

**Financial Reports Show:**
```
Total Revenue           ₹20,000
- COGS                  ₹12,000
= Gross Profit          ₹8,000
- Wastage Cost          ₹500
- Expenses              ₹2,000
= NET PROFIT            ₹5,500
```

---

## 🔐 ROLE-BASED ACCESS CONTROL

### **Admin**
- ✓ Dashboard
- ✓ Sales Entry
- ✓ Batch Preparation
- ✓ Inventory Management
- ✓ Waste Manager
- ✓ Daily Reports
- ✓ Master Data
- ✓ User Management

### **Manager**
- ✓ Dashboard
- ✓ Sales Entry
- ✓ Batch Preparation
- ✓ Inventory Management
- ✓ Daily Reports
- ✗ Waste Manager (read-only via reports)
- ✗ Master Data
- ✗ User Management

### **Officer**
- ✓ Dashboard (read-only)
- ✗ Sales Entry
- ✗ Batch Preparation
- ✗ Inventory
- ✗ Waste Manager
- ✗ Daily Reports
- ✗ Master Data
- ✗ User Management

### **Waste Manager**
- ✓ Dashboard (partial)
- ✗ Sales Entry
- ✗ Batch Preparation
- ✓ Waste Manager (full access)
- ✗ Inventory
- ✗ Daily Reports
- ✗ Master Data
- ✗ User Management

---

## 📊 DATABASE SCHEMA (NEW TABLES)

```sql
-- Waste Tracking
CREATE TABLE waste_tracker (
    id INTEGER PRIMARY KEY,
    date TEXT,
    item TEXT,
    qty_wasted REAL,
    reason TEXT,
    cost_lost REAL,
    recorded_by TEXT
);

-- Stock Ledger
CREATE TABLE stock_ledger (
    id INTEGER PRIMARY KEY,
    date TEXT,
    inv_id INTEGER,
    transaction_type TEXT,
    qty_change REAL,
    notes TEXT
);

-- Enhanced Users
ALTER TABLE users ADD COLUMN contact TEXT;
ALTER TABLE users ADD COLUMN active INTEGER DEFAULT 1;

-- New Role: waste_mgr
INSERT INTO roles VALUES ('waste_mgr', 'Waste Manager');
```

---

## 🎨 UI/UX IMPROVEMENTS

### **Dashboard Enhancements:**
- Wastage Cost KPI card (tracks daily waste)
- Low stock alerts with action items
- Real-time profit calculation including waste

### **Navigation:**
```
📊 Dashboard
💰 Sales Entry          (NEW: Simplified)
🧑‍🍳 Batch Prep           (NEW: 2-section design)
📦 Inventory            (IMPROVED: Add/Update/Remove)
♻️ Waste Manager        (NEW: Dedicated section)
📋 Daily Report         (IMPROVED: Comprehensive)
🧾 Master Data          (Updated)
👥 User Management      (NEW: Full system)
```

### **Color Scheme:**
- Waste tracking: **ORANGE** (#F97316)
- Financial summary: **Multi-color by type**
- Status indicators: **Green (OK) / Red (Low/Issue)**

---

## 🚀 USAGE WORKFLOW

### **Typical Daily Operations:**

#### **1. Morning: Batch Preparation**
```
Manager: 🧑‍🍳 Batch Prep
├─ Enter qty for each menu item
├─ System deducts stock per recipe
└─ Records in batch_prep table
```

#### **2. During Day: Sales Entry**
```
Manager/Officer: 💰 Sales Entry
├─ Select menu item
├─ Enter qty sold
├─ Select payment mode
└─ System auto-deducts, calculates profit
```

#### **3. Throughout Day: Waste Logging**
```
Waste Manager: ♻️ Waste Manager
├─ Record wastage with reason
├─ Enter item, qty, cost
├─ View daily waste log
└─ System tracks cost impact
```

#### **4. Evening: Daily Report**
```
Manager: 📋 Daily Report
├─ View today's sales
├─ Check financial summary
├─ Verify waste cost impact
├─ Review payment breakdown
└─ Export or print
```

---

## 📱 KEY FEATURES CHECKLIST

```
✅ Stock Management
  ✓ Add received stock
  ✓ Update stock level
  ✓ Remove items
  ✓ Low-stock alerts
  ✓ Stock category filtering

✅ User Management
  ✓ Create users
  ✓ Assign roles
  ✓ Reset passwords
  ✓ Active/inactive status

✅ Waste Tracking
  ✓ Record wastage with reason
  ✓ Cost tracking
  ✓ Daily log
  ✓ Impact on profit

✅ Batch Preparation
  ✓ Prep quantities
  ✓ Auto stock deduction
  ✓ Sales from batch
  ✓ Wastage tracking

✅ Sales Management
  ✓ Simple quick entry
  ✓ Menu selection dropdown
  ✓ Auto COGS calculation
  ✓ Payment mode selection
  ✓ Instant stock deduction

✅ Financial Reporting
  ✓ Revenue tracking
  ✓ COGS calculation
  ✓ Profit/Loss summary
  ✓ Payment breakdown
  ✓ Period filtering
  ✓ Waste impact analysis

✅ Role-Based Access
  ✓ Admin - Full access
  ✓ Manager - Operations
  ✓ Officer - Read-only
  ✓ Waste Manager - Waste only
```

---

## 🔄 DATA FLOW

```
INVENTORY                 BATCH PREP
    ↓                         ↓
    └─────→ RECIPES ←─────────┘
                ↓
            SALES
                ↓
         ┌──────┴──────┐
         ↓             ↓
    REVENUE       WASTAGE
         ↓             ↓
         └──────┬──────┘
                ↓
           PROFIT REPORT
```

---

## 📝 IMPORTANT NOTES

1. **Stock Deduction**: Automatic based on recipe `qty_per_unit`
2. **COGS**: Calculated from ingredient costs, not fixed
3. **Waste Impact**: Included in profit calculation
4. **User Roles**: Can be easily extended in roles table
5. **Password Security**: SHA256 hashing used
6. **Data Persistence**: SQLite database persists all data

---

## 🛠️ HOW TO RUN

```bash
# Install enhanced version
cd /Users/rohan/Desktop/canteen

# Run the app
python app_enhanced.py

# Or if you want to backup old version first:
cp app.py app_v3_backup.py
mv app_enhanced.py app.py
python app.py
```

---

## 📞 DEFAULT CREDENTIALS

| Role        | Username | Password      |
|-------------|----------|---------------|
| Admin       | admin    | admin123      |
| Manager     | manager  | manager123    |
| Officer     | officer  | officer123    |
| Waste Mgr   | waste    | waste123      |

---

## 🎯 NEXT IMPROVEMENTS (Optional)

- SMS alerts for low stock
- Email daily reports
- Photo attachment for waste reasons
- Expense receipt attachment
- Multi-unit reconciliation
- Inventory audit module
- Staff performance tracking
- Menu costing analysis

---

**Version**: 4.0 Enhanced
**Last Updated**: April 2026
**Database**: SQLite (canteen.db)
**Framework**: CustomTkinter
**Status**: Production Ready ✓

जय हिन्द 🇮🇳
