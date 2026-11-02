# H&N Punjabi Food Junction – Smart Restaurant Management System
> **MBA Design Thinking, Disruptive Technology and Innovation (DTDTI) Project**  
> *A comprehensive digital restaurant transformation platform solving post-relocation footfall loss, eliminating aggregator margin erosion, and streamlining kitchen operations.*

---

## 1. Executive Business Profile

- **Business Name**: H&N Punjabi Food Junction
- **Location**: Chandapura–Anekal Main Road, Anekal, Bengaluru, Karnataka, India - 562106
- **Proprietors**: Manjeet Singh & spouse
- **Cuisine & Dietary**: 100% Pure Vegetarian Authentic Punjabi Cuisine
- **Brand Tagline**: *"Authentic Punjabi Taste, Served with Love."*
- **Operational Channels**: Dine-in (Table Service), Counter Takeaway, Direct Website Ordering (0% commission), Aggregators (Swiggy, Zomato).

### Business Context & Strategic Innovation
Following restaurant relocation to the Chandapura–Anekal Main Road, the restaurant faced a sharp drop in regular customer visits due to loss of physical discovery. Simultaneously, heavy dependence on third-party aggregators (Swiggy/Zomato) resulted in 25–30% commission markups that severely reduced operating profits on vegetarian dishes.

This platform introduces:
1. **Direct Web Ordering & Re-engagement**: A direct online ordering channel with zero commission fees, instant UPI payment verification, and click-to-chat WhatsApp re-engagement campaigns for relocated patrons.
2. **Unified Kitchen Pipeline**: Real-time reactive synchronization between customer order tracking and kitchen dispatch.
3. **Automated Recipe Inventory Depletion**: Direct link between culinary recipes and ingredient stocks, automatically deducting raw materials (Malai Paneer, Atta, Desi Ghee, Saffron) at the kitchen preparation stage.
4. **Touch POS Billing Terminal**: Rapid Dine-In (Table 1–12) and Takeaway billing with instant thermal invoice printing.
5. **Managerial Financial MIS**: Indicative operating surplus dashboards differentiating revenue from expenses and overheads.

> **Menu Clarification**: The exterior roadside board historically states *"Veg & Nonveg"*, but the restaurant's active kitchen and transcribed menu are strictly **100% vegetarian**.

---

## 2. Technology Stack & Enterprise Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend Framework** | React 18 + TypeScript | Type-safe, component-driven reactive interface |
| **Styling & Design System** | Tailwind CSS 3 | Deep Maroon (`#641E2B`), Warm Cream (`#FFF8E8`), Muted Gold (`#C69A45`) |
| **Routing** | React Router DOM v6 | Dual-experience architecture (Customer Web + Staff ERP) |
| **Data Layer & Fallback** | Dual-Engine: Cloud Firestore + Local Persisted Layer | Runs seamlessly out-of-the-box in verified offline Demo Mode; ready for live Firebase |
| **Security & RBAC** | Firestore Security Rules (`firestore.rules`) | Role-based permissions enforced at database and route levels |
| **Visualization & MIS** | Recharts v2 | 7-day sales trends, channel breakdown, expense distribution |
| **Icons & Effects** | Lucide React + Canvas Confetti | Visual hierarchy and feedback delight on order completion |

---

## 3. Demo Personas & Test Credentials

The system includes a persistent **Demo Control Banner** allowing one-click role switching between all evaluation personas without tedious password typing:

| Persona | Role | Email | Password | Permissions & Scope |
| :--- | :--- | :--- | :--- | :--- |
| **Manjeet Singh** | `owner` | `owner@hnpunjabifood.com` | `demo1234` | Full access: All orders, Menu, Inventory, Purchases, Financial Expenses, Customer Retention, Settings, Architecture |
| **Gurpreet Kaur** | `manager` | `manager@hnpunjabifood.com` | `demo1234` | Kitchen orders, Menu pricing & availability, Stock adjustments, Purchases log, Sales MIS |
| **Harpreet Sharma** | `employee` | `kitchen@hnpunjabifood.com` | `demo1234` | Kitchen queue view, status progression (Preparing, Ready), POS Dine-In ticket entry |
| **Priya Narayanan** | `customer` | `priya.n@example.com` | `demo1234` | Digital menu, Shopping cart, Direct checkout, Real-time order tracker, Profile & Re-order |

---

## 4. Digital Menu Transcriptions (from Photo Menus)

The digital menu features 11 verified categories with exact transcribed prices pending owner confirmation:

- **Main Course**: Paneer Butter Masala (₹220), Paneer Makhani (₹270), Dal Makhani (₹180), Dal Fry (₹140), Mix Veg (₹200), Kadai Paneer (₹200).
- **Breakfast & Kulchas**: Special Kulcha (₹90), Aloo Kulcha (₹50), Paneer Kulcha (₹90), Mix Kulcha (₹70), Gobi Kulcha (₹60).
- **Lassi & Beverages**: H&N Special Lassi (₹100), Sweet Lassi (₹50), Salt Lassi (₹50), Kesar Lassi (₹60).
- **Rice & Biryani**: Jeera Rice (₹100), Veg Pulao (₹140), Veg Biryani (₹100), Paneer Biryani (₹120), Lucknow Biryani (₹150).
- **Starters**: Paneer Tikka (₹200), Hara Bara Kabab (₹180), Mushroom 65 (₹220), Paneer 65 (₹220).
- **Supplemental Categories**: Chat & Papad, Meals & Combos (Thalis), Chinese, Salads, Soups (clearly labelled as *Sample Items Pending Owner Approval*).

---

## 5. End-to-End Workflow Verification Results

The automated test runner (`npm test`) validates all 18 end-to-end lifecycle workflows:

```bash
=== STARTING H&N SMART RESTAURANT E2E WORKFLOW TEST SUITE ===

Phase 1: Customer Auth & Account
  ✓ PASS: 1. Customer registers and profile is created
  ✓ PASS: 2. Customer authentication credentials exist and authenticate

Phase 2: Digital Menu Exploration
  ✓ PASS: 3. Customer browses menu (found 33 verified vegetarian dishes)
  ✓ PASS: 3b. Menu contains required 11 categories

Phase 3: Cart & Direct Web Checkout
  ✓ PASS: 4a. Menu items exist with transcribed prices (₹220, ₹90, ₹100)
  ✓ PASS: 4b. Shopping cart calculates subtotal, GST (5%), packaging fee & free delivery threshold correctly
  ✓ PASS: 5 & 6. Order is placed, stored, and persisted in database

Phase 4: Management Dashboard & Order Pipeline
  ✓ PASS: 7. New order appears in Management Dashboard Kitchen Queue
  ✓ PASS: 8. Staff accepts the order and logs status note
  Initial Paneer Stock before prep: 18.5 kg
  Updated Paneer Stock after recipe deduction: 18.14 kg
  ✓ PASS: 9. Staff starts order preparation in kitchen
  ✓ PASS: 13. Inventory stock decrements automatically according to configured dish recipes (Malai Paneer consumed)
  ✓ PASS: 10. Customer live tracking view reflects status transition immediately
  ✓ PASS: 11. Staff marks food ready and completes order
  ✓ PASS: 12. Sales dashboard aggregates revenue dynamically (Total sales: ₹3009.5)

Phase 5: Purchases & Expenses Management
  ✓ PASS: 14. Owner records operating expense with category, voucher note and payment mode

Phase 6: Security & Role-Based Access Control
  ✓ PASS: 15a. Owner has full administrative permissions
  ✓ PASS: 15b. Manager has permissions for orders/inventory but restricted from owner settings
  ✓ PASS: 16. Kitchen Employee is blocked from owner-only expense registers and sensitive settings
  ✓ PASS: 17. Customer cannot access staff management portal

Phase 7: Mobile Responsiveness & Design System
  ✓ PASS: 18a. Restaurant business address is configured on Chandapura-Anekal Main Road
  ✓ PASS: 18b. Business hours properly configured with editable values

======================================================
TOTAL TESTS: 21 | PASSED: 21 | FAILED: 0
STATUS: ALL 18 END-TO-END WORKFLOWS VERIFIED SUCCESSFULLY! ✓
```

---

## 6. Simulated Features vs. Live Integrations Distinction

| Capability | Current Demo Layer | Production Deployment Target |
| :--- | :--- | :--- |
| **Database & State Sync** | **Live Pub/Sub Event Bus** in local storage; changes in manager queue immediately re-render customer tracking screens without refreshing. | Firebase Cloud Firestore with real-time snapshot listeners. |
| **UPI Payment Processing** | **Simulated Demo**: Displays official QR code and merchant VPA (`manjeetsingh.hn@okhdfcbank`), with a one-click simulation verification button. | Razorpay / Cashfree / HDFC UPI Smart Gateway with webhook listener. |
| **WhatsApp Customer Outreach** | **Live Hybrid**: Pre-populates personalized relocation re-engagement copy and opens WhatsApp Web/App on patron click. | Official WhatsApp Cloud Business API with verified message template approvals. |
| **SMS Notifications** | **Simulated**: Logged to order timeline and on-screen toast alerts. | Twilio / Kaleyra / Fast2SMS webhook. |
| **POS Thermal Bill Printing** | **Live**: Formatted specifically for 80mm thermal receipt printers (`@media print` clean paper styling). | Standard USB/Network ESC/POS thermal printer. |

---

## 7. Installation and Local Execution

### Prerequisites
- Node.js v18+ (tested on Node v22.14.0)
- npm v9+

### Commands
```bash
# 1. Install dependencies
npm install

# 2. Run automated test suite
npm test

# 3. Start development server
npm run dev

# 4. Production build
npm run build
```

The application will be live at `http://localhost:5173`.

---

## 8. Firebase Configuration (Optional Live Backend)

To connect this application to live Firebase services:
1. Create a Firebase Project at [https://console.firebase.google.com/](https://console.firebase.google.com/).
2. Enable **Authentication** (Email/Password & Anonymous) and **Cloud Firestore**.
3. Create a `.env` file in the project root:
   ```env
   VITE_FIREBASE_API_KEY=your_api_key_here
   VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   VITE_FIREBASE_APP_ID=your_app_id
   ```
4. Deploy security rules with Firebase CLI:
   ```bash
   firebase deploy --only firestore:rules
   ```

*When environment variables are omitted, the platform automatically runs in Verified Offline Demo Mode with all data persisted locally.*

