# 🎬 CANTEEN MANAGEMENT SYSTEM - VIDEO PRESENTATION GUIDE

**Presentation Date:** April 23, 2026  
**Recording Focus:** All 20+ Features Complete Walkthrough  
**Total Duration:** ~15-20 minutes recommended

---

## 📋 QUICK FEATURE CHECKLIST

- [ ] Login & Dashboard
- [ ] User Management (Add/Remove/Reset Password)
- [ ] Stock Management (Add/Update/Remove)
- [ ] Inventory & Categories
- [ ] Recipes & Linking
- [ ] Batch Preparation (2-section design)
- [ ] Sales Entry (Simplified 3-step)
- [ ] Waste Management (Complete section)
- [ ] Daily Reports (Financial)
- [ ] Master Data
- [ ] UI Theme & Responsiveness

---

## 🎥 PART 1: LOGIN & DASHBOARD (1:00 - 1:30 min)

### What to Show:
1. **Application Launch**
   - Show app.py running
   - Display clean login interface
   - Highlight professional UI theme

2. **Default Credentials** (Demo with these accounts)
   ```
   ✓ Admin:      admin / admin123
   ✓ Manager:    manager / manager123
   ✓ Officer:    officer / officer123
   ✓ Waste Mgr:  waste / waste123
   ```

3. **Dashboard Overview** (Login as Admin)
   - KPI Cards: Revenue, Meals Served, Net Profit
   - Low Stock Alerts section
   - Daily Waste Impact display
   - Quick access buttons

**Script:** "Welcome to the Canteen Management System v4.0. This enhanced system provides comprehensive management for military canteens with 20+ new features. Let's start with a secure login interface."

---

## 🎥 PART 2: USER MANAGEMENT (1:30 - 3:00 min)

### What to Show:

**A. View Existing Users** (Admin role only)
1. Click on "User Management" → "View Users"
2. Display table with all users:
   - Name, Role, Status, Contact info
   - Show 4 default users (Admin, Manager, Officer, Waste Manager)

**B. Add New User** (NEW Feature - Core Enhancement)
1. Click "User Management" → "Add User"
2. Fill form with sample data:
   ```
   Name: Raj Kumar
   Username: rajkumar
   Password: test123
   Confirm: test123
   Role: Officer
   Status: Active
   Contact: 98765-43210
   ```
3. Click "Add User" button
4. Show success message
5. Go back to View Users and show the new user in the list

**C. Reset Password** (NEW Feature)
1. Click "User Management" → "Reset Password"
2. Select a user (e.g., the newly created one)
3. Enter new password: "newpassword123"
4. Confirm and save
5. Show success notification

**D. Update User Status** (NEW Feature)
1. Click "User Management" → "View Users"
2. Click on a user to edit
3. Toggle status from Active to Inactive (or vice versa)
4. Save changes
5. Show updated status

**E. Test Login with New User**
1. Logout (top right corner)
2. Login with newly created credentials:
   ```
   Username: rajkumar
   Password: newpassword123
   ```
3. Show user-specific dashboard based on Officer role

**Script:** "The system now supports unlimited user creation. Unlike the original version with only 3 default users, you can now add staff members dynamically, assign specific roles, manage passwords securely, and control user access. This provides complete user lifecycle management."

---

## 🎥 PART 3: STOCK MANAGEMENT (3:00 - 4:30 min)

### What to Show:

**A. View Current Stock** 
1. Click "Stock" → "View Inventory"
2. Show inventory table with items:
   - Item name, Quantity, Unit, Category
   - Categories: Dry, Fresh, Dairy, Packaging
3. Highlight category dropdown filter

**B. Add Received Stock** (IMPROVED Feature)
1. Click "Stock" → "Add Received Stock"
2. Fill form:
   ```
   Item: Flour
   Quantity: 50
   Unit: kg
   Cost/Unit: 45
   Category: Dry
   Remarks: Weekly supply
   ```
3. Click "Add Stock"
4. Show success notification
5. Go back to View Inventory and verify new entry

**C. Update Stock Level** (IMPROVED Feature)
1. Click "Stock" → "Update Stock Level"
2. Select an item from dropdown (e.g., Rice)
3. Enter new quantity: 120
4. Click "Update"
5. Show success message
6. View inventory to confirm update

**D. Remove Stock Item** (NEW Feature)
1. Click "Stock" → "Remove Stock Item"
2. Select an item to remove
3. Show confirmation dialog
4. Confirm removal
5. Show success and verify item is gone from inventory

**E. View Stock Ledger** (NEW Feature)
1. Click "Stock" → "View Stock Ledger"
2. Show transaction history:
   - Date, Item, Quantity, Type (Add/Update/Remove)
   - Remarks column
3. Demonstrate that all changes are tracked

**Script:** "Stock management has been significantly enhanced. You can now receive stock with precise cost tracking, manually adjust inventory for corrections, and permanently remove obsolete items. All transactions are logged in the stock ledger for complete audit trail."

---

## 🎥 PART 4: RECIPES & BATCH PREPARATION (4:30 - 6:00 min)

### What to Show:

**A. View Recipes**
1. Click "Masters" → "Recipes"
2. Show recipe list with:
   - Recipe name, Ingredients used, Prep instructions
3. Show a sample recipe details

**B. Batch Preparation - Section 1: PREP** (2-Section Design)
1. Click "Batch Prep" → "Prepare Batch"
2. Fill Section 1 (Batch Preparation):
   ```
   Recipe: Chicken Biryani
   Quantity to Prepare: 10 (units)
   Date: Today
   Prepared By: Admin
   ```
3. Show automatic ingredient deduction table
4. Display deducted items (e.g., Rice: -5kg, Chicken: -10 units)
5. Click "Save Batch Prep"
6. Show inventory updated automatically

**C. Batch Preparation - Section 2: SALES FROM BATCH** (Connected Workflow)
1. In same form, fill Section 2 (Sales from Batch):
   ```
   Recipe: Chicken Biryani
   Units Sold: 8
   Price/Unit: 250
   Payment Mode: Cash
   ```
2. Show automatic COGS calculation
3. Click "Record Sales"
4. Show success message

**D. View Batch History**
1. Click "Batch Prep" → "View Batch History"
2. Show all recorded batches with:
   - Date, Recipe, Quantity, Prep By, Sales info
3. Demonstrate the connected workflow

**Script:** "Batch preparation has been redesigned with a 2-section workflow. Section 1 handles batch prep with automatic inventory deduction based on recipes. Section 2 immediately records sales from that batch with payment details. This creates a seamless prep-to-sales workflow with automatic COGS calculation."

---

## 🎥 PART 5: SALES ENTRY - SIMPLIFIED (6:00 - 7:00 min)

### What to Show:

**A. Simplified Sales Entry Interface** (Reduced from 8 steps to 3)
1. Click "Sales" → "Record Sales"
2. Show simplified 3-section form:
   - **Section 1: Menu Selection** (Dropdown)
   - **Section 2: Quantity Input** (Quick entry)
   - **Section 3: Payment Mode** (Radio buttons)

**B. Record Multiple Sales Items**
1. Select Item 1: Chapati (quantity: 50)
2. Real-time total updates: 50 × 15 = ₹750
3. Click "Add Item" to add more
4. Select Item 2: Daal (quantity: 30)
5. Total updates: 750 + (30 × 80) = ₹2,550
6. Continue adding 2-3 more items

**C. Select Payment Mode**
1. Show three payment options:
   - Cash
   - UPI
   - Card
2. Select "Cash"

**D. Calculate & Verify**
1. Show real-time calculations:
   - Total Quantity (meals)
   - Revenue
   - COGS (auto-calculated)
   - Profit margin display

**E. Save Sales**
1. Click "Save Sales"
2. Show success notification
3. Display receipt/confirmation

**F. View Sales History** (NEW Feature)
1. Click "Sales" → "View Sales"
2. Show today's sales list with:
   - Time, Items sold, Total revenue, Payment mode
3. Search/filter functionality

**Script:** "Sales entry has been completely simplified. Instead of complex 8-step forms, you now have a quick 3-step interface. Menu dropdown, quantity input, payment mode selection - that's it! Real-time calculations show you the revenue and profit instantly. Stock is automatically deducted for each item sold."

---

## 🎥 PART 6: WASTE MANAGEMENT - DEDICATED SECTION (7:00 - 8:30 min)

### What to Show:

**A. Navigate to Waste Management** (Waste Manager Role Feature)
1. Logout and login as Waste Manager:
   ```
   Username: waste
   Password: waste123
   ```
2. Show "Waste Manager" specific dashboard
3. Highlight menu item: "Waste Management"

**B. Record Wastage** (8 Reason Types)
1. Click "Waste Management" → "Record Waste"
2. Fill form with sample data:
   ```
   Item: Chicken (spoiled)
   Quantity: 5
   Unit: kg
   Reason: Spoilage ▼
   ```
3. Show dropdown with 8 reasons:
   - Spoilage
   - Prep Error
   - Plate Waste
   - Burn
   - Storage Issue
   - Customer Return
   - Expiry
   - Other

4. Continue filling form:
   ```
   Reason: Spoilage
   Estimated Cost: 500
   Remarks: Found mold in storage
   ```
5. Click "Record Waste"
6. Show success notification

**C. Record Additional Waste Items** (Multiple entries)
1. Record another waste item:
   ```
   Item: Rice
   Quantity: 2
   Reason: Burn (during prep)
   Cost: 150
   ```
2. Show total waste cost updating

**D. View Daily Waste Log** (NEW Feature)
1. Click "Waste Management" → "Daily Waste Log"
2. Show today's waste entries:
   - Item, Quantity, Reason, Cost
   - Recorded by, Timestamp
3. Display total waste count and total cost
4. Show waste impact on today's profit (in dashboard)

**E. Waste Impact on Dashboard** (Integrated KPI)
1. Go back to Dashboard
2. Show KPI card: "Daily Waste Cost: ₹650"
3. Show profit calculation includes waste reduction:
   - Revenue: ₹10,000
   - COGS: ₹6,000
   - Waste: ₹650
   - Net Profit: ₹3,350

**Script:** "Waste management has been transformed from a small checkbox into a complete dedicated system. Only Waste Managers can access this section. You can log different types of waste with 8 specific reason categories, track estimated costs, and see real-time impact on profitability. The dashboard instantly shows waste impact on your net profit."

---

## 🎥 PART 7: FINANCIAL REPORTS (8:30 - 10:30 min)

### What to Show:

**A. Daily Report** (Professional Format)
1. Click "Reports" → "Daily Report"
2. Show automatic date selection (today)
3. Display comprehensive report with:
   - **KPI Cards**: Revenue, Meals Served, Net Profit
   - **Sales Summary**: Date-wise breakdown

**B. Period Filtering** (Multiple Options)
1. Show period selector with options:
   - Last 1 Week
   - Last Fortnight (15 days)
   - Last Month
   - Last Quarter

2. Select "Last Week"
3. Show data updates for 7-day period

**C. Financial Summary Section**
1. Show "Financial Summary" table:
   ```
   Total Revenue:        ₹45,000
   Total COGS:          ₹28,000
   Total Waste Cost:    ₹2,100
   Total Expenses:      ₹3,500
   Net Profit:          ₹11,400
   Profit Margin:       25.3%
   ```

**D. Payment Breakdown** (NEW Enhanced Feature)
1. Show "Payment Mode Breakdown":
   - Cash: ₹22,500 (50%)
   - UPI: ₹15,750 (35%)
   - Card: ₹6,750 (15%)
2. Show pie chart visualization

**E. Expense Breakdown**
1. Show "Expense Category Breakdown":
   - Food Cost: ₹28,000
   - Waste: ₹2,100
   - Operational: ₹3,500

**F. Professional Report Format** (Letterhead)
1. Scroll down to show official format:
   - Army Canteen letterhead
   - Date range
   - All financial details
   - Signature lines for:
     - Manager
     - Officer
     - OIC (Officer In Charge)

**G. Export Report** (if feature exists)
1. Click "Generate PDF" / "Export" button
2. Show report downloads/displays
3. Display professional PDF with all details

**Script:** "The reporting system provides comprehensive financial insights. Choose any period - last week, fortnight, month, or quarter - and get detailed breakdowns. See revenue by payment mode, track costs by category, understand waste impact, and calculate exact profit margins. The professional letterhead format is ready for official submission."

---

## 🎥 PART 8: MASTER DATA MANAGEMENT (10:30 - 11:30 min)

### What to Show:

**A. Inventory Master**
1. Click "Masters" → "Inventory Master"
2. Show all inventory items:
   - Item name, Category, Unit, Current stock
3. Demonstrate search/filter functionality

**B. Menu Master** (Items for Sale)
1. Click "Masters" → "Menu Master"
2. Show menu items:
   - Item name, Price, Category, Status
3. Show add new menu item dialog
4. Add sample item:
   ```
   Name: Tandoori Chicken
   Price: 180
   Category: Non-Veg
   Description: Grilled chicken tandoori style
   ```
5. Click "Add" and show in menu list

**C. Recipe Master**
1. Click "Masters" → "Recipe Master"
2. Show recipes with ingredient details
3. Click on a recipe to show:
   - Ingredients and quantities
   - Cooking instructions
   - Prep time

**D. User Master** (NEW Feature)
1. Click "Masters" → "User Master"
2. Show all users with:
   - Name, Role, Status, Contact
   - Create/Edit/Delete options
3. Show this is the centralized user management hub

**E. Linking Between Masters** (Show Relationships)
1. Show recipe "Chicken Biryani" using inventory items
2. Show menu item "Chicken Biryani" linked to recipe
3. Demonstrate how batch prep uses recipe → deducts from inventory

**Script:** "Master data management is centralized and interconnected. Inventory items feed into recipes, recipes are linked to menu items, and batch preparation orchestrates the entire flow. The new User Master provides centralized user management with all lifecycle controls."

---

## 🎥 PART 9: UI/UX & THEME ENHANCEMENTS (11:30 - 12:30 min)

### What to Show:

**A. Professional Theme** (Army Canteen Color Scheme)
1. Show application color scheme:
   - Primary: Army Green/Khaki
   - Secondary: Professional Gray
   - Accent colors for alerts/warnings
2. Point out professional typography
3. Highlight consistent design language

**B. Responsive UI**
1. Show desktop layout
2. If possible, resize window to show responsive behavior
3. Highlight clean button layouts, readable tables

**C. Navigation Structure** (Role-based)
1. Show menu structure changes based on logged-in user
2. Admin sees: All options + User Management
3. Manager sees: Stock, Sales, Reports (no waste/user mgmt)
4. Officer sees: Sales, Batch Prep, Inventory
5. Waste Manager sees: Waste management focused menu

**D. Visual Enhancements**
1. Show KPI cards with icons
2. Display color-coded alerts
3. Show professional report letterhead

**Script:** "The UI has been completely redesigned with a professional army canteen theme. The color scheme is consistent throughout the application. Navigation is role-based - users see only what's relevant to their job. The responsive design works smoothly on different screen sizes."

---

## 🎥 PART 10: DEMO SCENARIO - COMPLETE WORKFLOW (12:30 - 15:00 min)

### What to Show (Complete Day Simulation):

**A. Morning: Stock Received**
1. Login as Admin
2. Add received stock: 100kg Flour, cost ₹4,500
3. Show inventory updated

**B. Mid-Morning: Batch Preparation**
1. Click "Batch Prep"
2. Prepare 50 units of Chicken Biryani
3. Show automatic ingredient deduction
4. Record 40 units sold (payment: cash)
5. Show inventory auto-updated

**C. Afternoon: Direct Sales**
1. Record multiple items sold:
   - 80 Chapati
   - 60 Dal
   - 40 Vegetables
2. Show sales calculated in real-time

**D. Waste Recording** (Login as Waste Manager)
1. Record waste:
   - 2kg Chicken (Spoilage): ₹400
   - 3kg Rice (Burn): ₹150
2. Show total waste: ₹550

**E. Generate Daily Report**
1. Go to Reports → Daily Report
2. Show complete financial picture:
   ```
   Revenue: ₹X,XXX
   COGS: ₹X,XXX
   Waste: ₹550
   Net Profit: ₹X,XXX
   ```
3. Show payment breakdown
4. Display with professional letterhead

**F. End of Day: User Management Check**
1. Review all users logged in during day
2. Show audit trail capability
3. Export report

**Script:** "Let me walk you through a typical operating day. We start with stock receipt, prepare batches with automatic inventory deduction, record direct sales, log waste with reasons, and end with a comprehensive financial report showing every transaction's impact on profitability. Everything is connected - stock flows to batches, batches to sales, waste impacts profit, and the report shows the complete picture."

---

## 📝 BACKUP TALKING POINTS

When presenting, emphasize:

1. **Improvement Over Original (3x better)**
   - Original: Limited 3 default users only
   - Now: Unlimited dynamic users with role management

2. **Complete User Lifecycle**
   - Create, modify, disable, reset passwords
   - All users secure with SHA256 hashing

3. **Waste Management Impact**
   - 8 waste reason types
   - Cost tracking for every wastage
   - Real-time dashboard impact

4. **Simplified Sales Entry**
   - Reduced complexity from 8 steps to 3
   - Faster data entry
   - Fewer errors

5. **Batch Prep Innovation**
   - 2-section connected workflow
   - Automatic inventory deduction
   - COGS auto-calculation

6. **Professional Reporting**
   - Multiple time periods
   - Payment mode analysis
   - Waste impact visibility
   - Official letterhead format

7. **Security & Audit Trail**
   - All transactions logged
   - User tracking
   - Stock ledger
   - Password hashing

---

## ✅ RECORDING CHECKLIST

- [ ] Test all database operations before recording
- [ ] Prepare sample data for demo
- [ ] Ensure internet/connectivity stable
- [ ] Set appropriate screen zoom (120-150% for visibility)
- [ ] Clear desktop background
- [ ] Close unnecessary applications
- [ ] Test audio recording
- [ ] Have notes visible during recording
- [ ] Record each section separately (easier to edit)
- [ ] Do practice run first

---

## 🎬 RECOMMENDED RECORDING SETTINGS

**Video Quality:** 1080p or higher  
**Frame Rate:** 30 FPS minimum  
**Audio:** Clear narration, background noise minimal  
**Pacing:** Slow enough to see clearly, fast enough to hold attention  
**Length:** 15-20 minutes total  

---

**Good luck with your presentation! 🎉**
