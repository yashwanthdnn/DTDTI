import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Set page configuration
st.set_page_config(
    page_title="H&N Punjabi Food Junction – Smart Restaurant System",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Theme CSS (Deep Maroon, Warm Cream, Muted Gold, Dark Brown)
st.markdown("""
<style>
    /* Theme color styling */
    :root {
        --brand-maroon: #641E2B;
        --brand-gold: #C69A45;
        --brand-cream: #FFF8E8;
        --brand-brown: #33251F;
    }
    
    .main-header {
        background: linear-gradient(135deg, #641E2B 0%, #4A1520 100%);
        color: #FFF8E8;
        padding: 1.5rem 2rem;
        border-radius: 1rem;
        border: 2px solid #C69A45;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(100, 30, 43, 0.15);
    }
    
    .stButton>button {
        background-color: #641E2B !important;
        color: #FFF8E8 !important;
        font-weight: 700 !important;
        border-radius: 0.75rem !important;
        border: 1px solid #C69A45 !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #85293A !important;
        border-color: #FFF8E8 !important;
        transform: translateY(-1px);
    }
    
    .dish-card {
        background: white;
        border-radius: 1rem;
        padding: 1.25rem;
        border: 1px solid rgba(100, 30, 43, 0.15);
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    
    .kpi-card {
        background: white;
        border-radius: 1rem;
        padding: 1.25rem;
        border-left: 5px solid #641E2B;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    }
    
    .thermal-receipt {
        background: #FFFFFF;
        font-family: 'Courier New', Courier, monospace;
        padding: 1.5rem;
        border: 2px dashed #999;
        border-radius: 0.5rem;
        color: #000;
        font-size: 0.85rem;
        line-height: 1.4;
    }

    .persona-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-weight: bold;
        font-size: 0.82rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- INITIAL STATE & DATA PERSISTENCE ----------------
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    
    # Active Evaluation Persona
    st.session_state.current_role = "All Modules (Unrestricted Admin Demo)"
    
    # Restaurant Settings
    st.session_state.settings = {
        "name": "H&N Punjabi Food Junction",
        "tagline": "Authentic Punjabi Taste, Served with Love.",
        "address": "Chandapura–Anekal Main Road, Anekal, Bengaluru, Karnataka - 562106",
        "phone": "+91 98450 12345",
        "hours": "11:00 AM – 11:00 PM (All 7 Days)",
        "tax_rate": 5.0, # 5% GST
        "packaging_fee": 20.0,
        "delivery_fee": 40.0,
        "free_delivery_threshold": 499.0,
        "upi_id": "manjeetsingh.hn@okhdfcbank",
    }
    
    # 11 Verified Categories & Transcribed Dishes
    st.session_state.menu = [
        {"id": "m1", "name": "Paneer Butter Masala", "category": "Main Course", "price": 220, "desc": "Fresh cottage cheese cubes in rich buttery tomato cashew gravy.", "chef_special": True, "prep_time": 20, "available": True, "recipe": {"paneer": 0.18, "ghee": 0.03}},
        {"id": "m2", "name": "Paneer Makhani", "category": "Main Course", "price": 270, "desc": "Velvety smooth Punjabi delicacy slow-simmered in butter and cream.", "chef_special": True, "prep_time": 22, "available": True, "recipe": {"paneer": 0.20, "ghee": 0.04}},
        {"id": "m3", "name": "Dal Makhani", "category": "Main Course", "price": 180, "desc": "Slow-cooked whole black lentils simmered overnight with butter.", "chef_special": True, "prep_time": 15, "available": True, "recipe": {"dal": 0.15, "ghee": 0.03}},
        {"id": "m4", "name": "Dal Fry", "category": "Main Course", "price": 140, "desc": "Comforting yellow lentils tempered with cumin, garlic and tomatoes.", "chef_special": False, "prep_time": 15, "available": True, "recipe": {"dal": 0.12, "ghee": 0.02}},
        {"id": "m5", "name": "Mix Veg", "category": "Main Course", "price": 200, "desc": "Seasonal fresh vegetables tossed in traditional Punjabi masala.", "chef_special": False, "prep_time": 18, "available": True, "recipe": {"veg": 0.20}},
        {"id": "m6", "name": "Kadai Paneer", "category": "Main Course", "price": 200, "desc": "Paneer tossed with crunchy bell peppers and fresh roasted kadai spices.", "chef_special": False, "prep_time": 20, "available": True, "recipe": {"paneer": 0.18}},
        
        {"id": "b1", "name": "Special Kulcha", "category": "Breakfast", "price": 90, "desc": "Signature Amritsari stuffed crispy tandoori kulcha with butter.", "chef_special": True, "prep_time": 15, "available": True, "recipe": {"atta": 0.12, "ghee": 0.02}},
        {"id": "b2", "name": "Aloo Kulcha", "category": "Breakfast", "price": 50, "desc": "Crispy clay-baked bread stuffed with spiced mashed potatoes.", "chef_special": False, "prep_time": 12, "available": True, "recipe": {"atta": 0.10}},
        {"id": "b3", "name": "Paneer Kulcha", "category": "Breakfast", "price": 90, "desc": "Delicate tandoori kulcha stuffed with generous spiced paneer.", "chef_special": True, "prep_time": 15, "available": True, "recipe": {"atta": 0.10, "paneer": 0.08}},
        {"id": "b4", "name": "Mix Kulcha", "category": "Breakfast", "price": 70, "desc": "Potatoes, cauliflower, and onions stuffed in tandoori bread.", "chef_special": False, "prep_time": 14, "available": True, "recipe": {"atta": 0.10}},
        {"id": "b5", "name": "Gobi Kulcha", "category": "Breakfast", "price": 60, "desc": "Tandoor baked bread stuffed with spiced grated cauliflower.", "chef_special": False, "prep_time": 14, "available": True, "recipe": {"atta": 0.10}},
        
        {"id": "l1", "name": "H&N Special Lassi", "category": "Lassi and Beverages", "price": 100, "desc": "Thick creamy sweet lassi topped with malai, dry fruits & cardamom.", "chef_special": True, "prep_time": 5, "available": True, "recipe": {"curd": 0.35}},
        {"id": "l2", "name": "Sweet Lassi", "category": "Lassi and Beverages", "price": 50, "desc": "Classic rich hand-churned yogurt sweetened with cane sugar.", "chef_special": False, "prep_time": 5, "available": True, "recipe": {"curd": 0.30}},
        {"id": "l3", "name": "Salt Lassi", "category": "Lassi and Beverages", "price": 50, "desc": "Refreshing savory spiced yogurt with roasted cumin and black salt.", "chef_special": False, "prep_time": 5, "available": True, "recipe": {"curd": 0.30}},
        {"id": "l4", "name": "Kesar Lassi", "category": "Lassi and Beverages", "price": 60, "desc": "Infused with pure Kashmiri saffron strands and slivered almonds.", "chef_special": True, "prep_time": 5, "available": True, "recipe": {"curd": 0.30, "kesar": 0.1}},
        
        {"id": "r1", "name": "Jeera Rice", "category": "Rice and Pulao", "price": 100, "desc": "Long grain aged basmati rice tempered with royal cumin seeds.", "chef_special": False, "prep_time": 10, "available": True, "recipe": {"rice": 0.20}},
        {"id": "r2", "name": "Veg Pulao", "category": "Rice and Pulao", "price": 140, "desc": "Basmati rice cooked with fresh garden peas, beans and whole spices.", "chef_special": False, "prep_time": 15, "available": True, "recipe": {"rice": 0.20}},
        {"id": "by1", "name": "Veg Biryani", "category": "Biryani", "price": 100, "desc": "Dum-cooked basmati rice layered with seasoned mixed vegetables.", "chef_special": False, "prep_time": 18, "available": True, "recipe": {"rice": 0.25}},
        {"id": "by2", "name": "Paneer Biryani", "category": "Biryani", "price": 120, "desc": "Royal dum biryani layered with marinated soft paneer cubes.", "chef_special": True, "prep_time": 20, "available": True, "recipe": {"rice": 0.25, "paneer": 0.15}},
        {"id": "by3", "name": "Lucknow Biryani", "category": "Biryani", "price": 150, "desc": "Awadhi style aromatic mild dum biryani with saffron and kewra.", "chef_special": True, "prep_time": 22, "available": True, "recipe": {"rice": 0.25}},
        
        {"id": "s1", "name": "Paneer Tikka", "category": "Starters", "price": 200, "desc": "Juicy paneer cubes marinated in mustard-yogurt and tandoor charred.", "chef_special": True, "prep_time": 18, "available": True, "recipe": {"paneer": 0.20}},
        {"id": "s2", "name": "Hara Bara Kabab", "category": "Starters", "price": 180, "desc": "Spinach, green peas, and potato patties pan-grilled crisp.", "chef_special": False, "prep_time": 15, "available": True, "recipe": {"veg": 0.15}},
        {"id": "s3", "name": "Mushroom 65", "category": "Starters", "price": 220, "desc": "Crispy button mushrooms tossed in spicy tempered curry leaves.", "chef_special": False, "prep_time": 15, "available": True, "recipe": {"mushroom": 0.20}},
        {"id": "s4", "name": "Paneer 65", "category": "Starters", "price": 220, "desc": "Deep fried golden paneer tossed in tangy yogurt sauce.", "chef_special": False, "prep_time": 16, "available": True, "recipe": {"paneer": 0.20}},
        
        {"id": "cp1", "name": "Masala Papad (Sample)", "category": "Chat & Papad", "price": 50, "desc": "Roasted urad papad topped with chopped onions, tomatoes & herbs.", "chef_special": False, "prep_time": 5, "available": True, "recipe": {}},
        {"id": "mc1", "name": "Punjabi Thali (Sample)", "category": "Meals and Combos", "price": 260, "desc": "Paneer Butter Masala, Dal Makhani, Mix Veg, Rice, Rotis & Lassi.", "chef_special": True, "prep_time": 20, "available": True, "recipe": {"paneer": 0.15, "dal": 0.10, "atta": 0.15}},
        {"id": "ch1", "name": "Veg Hakka Noodles (Sample)", "category": "Chinese", "price": 150, "desc": "Wok tossed noodles with shredded vegetables and light soy.", "chef_special": False, "prep_time": 14, "available": True, "recipe": {}},
        {"id": "sl1", "name": "Green Garden Salad (Sample)", "category": "Salads", "price": 60, "desc": "Fresh cucumber, tomatoes, carrots, chillies and lemon wedges.", "chef_special": False, "prep_time": 5, "available": True, "recipe": {}},
        {"id": "sp1", "name": "Cream of Tomato Soup (Sample)", "category": "Soups", "price": 110, "desc": "Slow simmered ripe tomato soup with croutons and fresh cream.", "chef_special": False, "prep_time": 10, "available": True, "recipe": {}},
    ]
    
    # Inventory
    st.session_state.inventory = {
        "paneer": {"name": "Fresh Malai Paneer", "stock": 18.5, "unit": "kg", "reorder": 8.0, "cost": 340, "supplier": "Nandini Dairy Wholesale Anekal"},
        "atta": {"name": "Chakki Wheat Atta", "stock": 45.0, "unit": "kg", "reorder": 20.0, "cost": 45, "supplier": "Punjab Agro Foods"},
        "dal": {"name": "Urad Dal Sabut", "stock": 14.0, "unit": "kg", "reorder": 6.0, "cost": 160, "supplier": "Sri Balaji Pulses"},
        "ghee": {"name": "Pure Desi Ghee", "stock": 9.0, "unit": "L", "reorder": 5.0, "cost": 580, "supplier": "Nandini Dairy Wholesale"},
        "rice": {"name": "Aged Basmati Rice", "stock": 35.0, "unit": "kg", "reorder": 15.0, "cost": 110, "supplier": "Punjab Agro Foods"},
        "curd": {"name": "Fresh Curd (Lassi Grade)", "stock": 22.0, "unit": "L", "reorder": 10.0, "cost": 65, "supplier": "Local Farm Fresh Anekal"},
        "mushroom": {"name": "Fresh Button Mushrooms", "stock": 3.5, "unit": "kg", "reorder": 5.0, "cost": 180, "supplier": "Himalayan Fresh Greens"},
        "kesar": {"name": "Kashmiri Saffron", "stock": 8.0, "unit": "g", "reorder": 10.0, "cost": 280, "supplier": "Amritsar Spice Traders"},
    }
    
    # Cart
    st.session_state.cart = {}
    
    # Active Orders
    st.session_state.orders = [
        {
            "id": "HN-2401",
            "customer": "Priya Narayanan",
            "phone": "+91 98860 99881",
            "type": "Home Delivery",
            "channel": "Direct Website",
            "items": [("Paneer Butter Masala", 1, 220), ("Special Kulcha", 2, 90), ("H&N Special Lassi", 2, 100)],
            "subtotal": 600.0,
            "tax": 30.0,
            "packaging": 20.0,
            "delivery": 0.0,
            "total": 650.0,
            "status": "In Kitchen Prep",
            "payment": "UPI (Verified)",
            "address": "Flat 402, Green Glen Layout, Chandapura Main Rd",
            "time": "12:15 PM Today",
        },
        {
            "id": "HN-2402",
            "customer": "Table 4 (Dine-in)",
            "phone": "+91 98451 11223",
            "type": "Dine-in (Table 4)",
            "channel": "Staff POS",
            "items": [("Dal Makhani", 1, 180), ("Jeera Rice", 2, 100), ("Sweet Lassi", 2, 50)],
            "subtotal": 480.0,
            "tax": 24.0,
            "packaging": 0.0,
            "delivery": 0.0,
            "total": 504.0,
            "status": "Completed",
            "payment": "Counter Cash",
            "address": "Table #4 Inside Restaurant",
            "time": "11:30 AM Today",
        },
        {
            "id": "HN-2403",
            "customer": "Rahul Verma",
            "phone": "+91 97711 22334",
            "type": "Takeaway",
            "channel": "Swiggy",
            "items": [("Paneer Tikka", 1, 200), ("Paneer Biryani", 2, 120)],
            "subtotal": 440.0,
            "tax": 22.0,
            "packaging": 20.0,
            "delivery": 0.0,
            "total": 482.0,
            "status": "Food Ready",
            "payment": "UPI",
            "address": "Pickup Counter",
            "time": "12:30 PM Today",
        }
    ]
    
    # Expenses
    st.session_state.expenses = [
        {"date": "2024-11-01", "category": "Rent", "amount": 32000, "desc": "Premise rent Chandapura-Anekal Main Rd", "mode": "Bank Transfer"},
        {"date": "2024-11-01", "category": "Salaries", "amount": 45000, "desc": "Staff & kitchen monthly compensation", "mode": "Bank Transfer"},
        {"date": "2024-10-29", "category": "Electricity", "amount": 6800, "desc": "BESCOM commercial electricity bill", "mode": "UPI"},
        {"date": "2024-10-30", "category": "Gas", "amount": 4200, "desc": "Commercial LPG cylinders refill", "mode": "Cash"},
        {"date": "2024-10-28", "category": "Packaging", "amount": 3600, "desc": "Meal boxes, paper bags & lassi cups", "mode": "Cash"},
    ]
    
    # Purchases
    st.session_state.purchases = [
        {"date": "2024-10-30", "ingredient": "Fresh Malai Paneer", "qty": "25 kg", "cost": 8500, "supplier": "Nandini Dairy Anekal", "invoice": "NAN-8821"},
        {"date": "2024-10-28", "ingredient": "Chakki Wheat Atta", "qty": "50 kg", "cost": 2250, "supplier": "Punjab Agro Foods", "invoice": "PAF-432"},
        {"date": "2024-10-25", "ingredient": "Pure Desi Ghee", "qty": "15 L", "cost": 8700, "supplier": "Nandini Dairy Anekal", "invoice": "NAN-8790"},
    ]
    
    # Customers (Relocation Reconnection Target)
    st.session_state.customers = [
        {"name": "Priya Narayanan", "phone": "+91 98860 99881", "orders": 8, "spent": 4850, "status": "Regular", "last_order": "Today", "notes": "Loves Paneer Butter Masala"},
        {"name": "Amitabh Sen", "phone": "+91 98450 77123", "orders": 12, "spent": 7300, "status": "Lapsed (Relocation Target)", "last_order": "45 days ago", "notes": "Regular before relocation to Anekal Rd"},
        {"name": "Kavita Hegde", "phone": "+91 94480 33211", "orders": 3, "spent": 1650, "status": "Regular", "last_order": "3 days ago", "notes": "Orders weekend breakfasts"},
        {"name": "Rajesh G.", "phone": "+91 99001 88220", "orders": 1, "spent": 650, "status": "New Customer", "last_order": "Yesterday", "notes": "Found via roadside board"},
    ]

# ---------------- NAVIGATION SIDEBAR ----------------
st.sidebar.markdown(f"""
<div style="text-align: center; padding: 1rem 0; border-bottom: 2px solid #C69A45;">
    <h2 style="color: #641E2B; margin: 0; font-family: serif;">🍲 H&N Punjabi Food</h2>
    <p style="font-size: 0.8rem; color: #666; margin: 0;">Chandapura–Anekal Main Road</p>
    <span style="background: #2E7D32; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">100% PURE VEG</span>
</div>
""", unsafe_allow_html=True)

# Evaluation Persona Switcher
st.sidebar.markdown("### 👤 Evaluation Persona")
persona = st.sidebar.selectbox(
    "Active Role (RBAC Switcher)",
    [
        "🌐 All Modules (Unrestricted Admin Demo)",
        "👑 Manjeet Singh (Owner)",
        "📋 Gurpreet Kaur (Manager)",
        "🍳 Harpreet Sharma (Kitchen Staff)",
        "🛍️ Priya Narayanan (Customer)",
    ],
    index=0
)
st.session_state.current_role = persona

# Dynamic navigation options based on Persona
ALL_PAGES = [
    "🏠 Customer Homepage & Story",
    "🍲 Digital Menu & Order Online",
    "🛒 Cart & Checkout (Simulated UPI)",
    "📍 Live Order Tracking",
    "📊 Executive MIS & Sales Analytics",
    "🍳 Kitchen Queue & Order Management",
    "🏪 Staff POS Terminal (Dine-in / Takeaway)",
    "📦 Recipe-Linked Inventory & Stock",
    "📑 Menu Catalog & Pricing Control",
    "🚚 Purchases & Supplier Procurement",
    "💰 Sales & Operating Expenses MIS",
    "👥 Customer Retention & WhatsApp Re-engagement",
    "⚙️ Restaurant Settings",
    "📖 MBA Project & Architecture Docs",
]

if "Customer" in persona:
    available_pages = [
        "🏠 Customer Homepage & Story",
        "🍲 Digital Menu & Order Online",
        "🛒 Cart & Checkout (Simulated UPI)",
        "📍 Live Order Tracking",
        "📖 MBA Project & Architecture Docs",
    ]
elif "Kitchen Staff" in persona:
    available_pages = [
        "🍳 Kitchen Queue & Order Management",
        "🏪 Staff POS Terminal (Dine-in / Takeaway)",
        "📦 Recipe-Linked Inventory & Stock",
        "📍 Live Order Tracking",
        "📖 MBA Project & Architecture Docs",
    ]
elif "Manager" in persona:
    available_pages = [
        "📊 Executive MIS & Sales Analytics",
        "🍳 Kitchen Queue & Order Management",
        "🏪 Staff POS Terminal (Dine-in / Takeaway)",
        "📦 Recipe-Linked Inventory & Stock",
        "📑 Menu Catalog & Pricing Control",
        "🚚 Purchases & Supplier Procurement",
        "👥 Customer Retention & WhatsApp Re-engagement",
        "🏠 Customer Homepage & Story",
        "🍲 Digital Menu & Order Online",
        "📖 MBA Project & Architecture Docs",
    ]
else:
    available_pages = ALL_PAGES

nav = st.sidebar.radio("Navigation Menu", available_pages, index=0)

st.sidebar.markdown("---")
st.sidebar.caption(f"Role: **{persona}**")
st.sidebar.info("💡 **Streamlit Cloud Deployment**: 100% operational with offline persistent demo state, dynamic inventory depletion & zero aggregator fees.")

# Helper for recipe inventory deduction
def deduct_recipe(order_items):
    for item_name, qty, _ in order_items:
        match = next((d for d in st.session_state.menu if d["name"] == item_name), None)
        if match and match.get("recipe"):
            for ing_key, per_unit in match["recipe"].items():
                if ing_key in st.session_state.inventory:
                    total_used = per_unit * qty
                    st.session_state.inventory[ing_key]["stock"] = max(
                        0.0, round(st.session_state.inventory[ing_key]["stock"] - total_used, 2)
                    )

# ---------------- PAGE 1: HOMEPAGE & STORY ----------------
if nav == "🏠 Customer Homepage & Story":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-family: serif;">Authentic Punjabi Taste, Served with Love.</h1>
        <p style="font-size: 1.1rem; opacity: 0.95; margin-top: 0.5rem;">
            Welcome to <strong>H&N Punjabi Food Junction</strong>. We have relocated to <strong>Chandapura–Anekal Main Road</strong>!
        </p>
        <span style="background: #C69A45; color: #33251F; padding: 4px 12px; border-radius: 8px; font-weight: bold; font-size: 0.85rem;">
            ● 100% Pure Vegetarian Amritsari Heritage
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ **Note on Signboard**: Our roadside exterior signboard historically says *'Veg & Nonveg'*. However, our kitchen and active menu are **strictly 100% vegetarian**.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Relocation Story & Direct Customer Ordering")
        st.write("""
        Following our recent relocation to Chandapura–Anekal Main Road, we built this direct digital ordering system to:
        * **Reconnect with our loyal regular customers** without depending exclusively on third-party aggregators.
        * **Eliminate 25–30% delivery commission markups** (Swiggy/Zomato), passing honest savings directly to you.
        * **Ensure faster kitchen priority** directly from our clay tandoor and slow-cooking pots.
        """)
        
        st.success("🎉 **Relocation Promo Offer**: Use promo code **ANEKAL15** on checkout for 15% discount on direct orders above ₹399!")
        
        st.subheader("Authentic Punjabi Highlights")
        hcol1, hcol2, hcol3 = st.columns(3)
        with hcol1:
            st.metric("Paneer Butter Masala", "₹220", "Top Seller")
            st.caption("Fresh malai cottage cheese in velvety tomato-cashew gravy.")
        with hcol2:
            st.metric("Amritsari Special Kulcha", "₹90", "Clay Tandoor")
            st.caption("Crispy layered bread stuffed with spiced herbs & desi ghee.")
        with hcol3:
            st.metric("H&N Special Lassi", "₹100", "Hand Churned")
            st.caption("Thick sweet yogurt topped with rich malai & cardamom.")

    with col2:
        st.subheader("Restaurant Information")
        st.write(f"**📍 Location**: {st.session_state.settings['address']}")
        st.write(f"**🕒 Hours**: {st.session_state.settings['hours']}")
        st.write(f"**📞 Direct Phone**: {st.session_state.settings['phone']}")
        st.write(f"**💳 Direct UPI**: `{st.session_state.settings['upi_id']}`")
        
        st.markdown("### Customer Reviews")
        st.caption("⭐ 'The Dal Makhani & Special Lassi taste just like in Punjab!' – Priya N.")
        st.caption("⭐ 'Crispiest Amritsari Kulcha in the Chandapura-Anekal belt.' – Kavita H.")

# ---------------- PAGE 2: DIGITAL MENU & DIRECT ORDER ----------------
elif nav == "🍲 Digital Menu & Order Online":
    st.title("🍲 Digital Restaurant Menu (100% Pure Vegetarian)")
    st.caption("Core dishes and prices are transcribed directly from restaurant photographs.")
    
    categories = ["All"] + sorted(list(set(d["category"] for d in st.session_state.menu)))
    sel_cat = st.selectbox("Filter by Category", categories)
    search = st.text_input("🔍 Search Dish by Name (e.g. Paneer, Kulcha, Dal, Lassi, Biryani)")
    
    filtered_dishes = [
        d for d in st.session_state.menu
        if (sel_cat == "All" or d["category"] == sel_cat)
        and (search.lower() in d["name"].lower() or search.lower() in d["desc"].lower())
    ]
    
    st.write(f"Showing **{len(filtered_dishes)}** authentic dishes")
    
    cols = st.columns(3)
    for i, dish in enumerate(filtered_dishes):
        with cols[i % 3]:
            is_avail = dish.get("available", True)
            avail_tag = '<span style="color:#2E7D32; font-weight:bold; font-size:0.8rem;">● AVAILABLE</span>' if is_avail else '<span style="color:#C62828; font-weight:bold; font-size:0.8rem;">● OUT OF STOCK</span>'
            
            st.markdown(f"""
            <div class="dish-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    {avail_tag}
                    <span style="font-size:1.1rem; font-weight:bold; color:#641E2B;">₹{dish['price']}</span>
                </div>
                <h4 style="margin:0.25rem 0; color:#33251F;">{dish['name']}</h4>
                <p style="font-size:0.8rem; color:#666; height:40px; overflow:hidden;">{dish['desc']}</p>
                <div style="font-size:0.75rem; color:#888; margin-bottom:0.5rem;">Category: <strong>{dish['category']}</strong> | Prep: ~{dish['prep_time']}m</div>
            </div>
            """, unsafe_allow_html=True)
            
            qty = st.session_state.cart.get(dish["name"], 0)
            btn_col1, btn_col2 = st.columns([2, 1])
            with btn_col1:
                if st.button(f"Add to Cart ({dish['name']})", key=f"add_{dish['id']}", disabled=not is_avail):
                    st.session_state.cart[dish["name"]] = qty + 1
                    st.toast(f"Added {dish['name']} to cart!")
                    st.rerun()
            with btn_col2:
                if qty > 0:
                    st.write(f"**In cart: {qty}**")

# ---------------- PAGE 3: CART & CHECKOUT ----------------
elif nav == "🛒 Cart & Checkout (Simulated UPI)":
    st.title("🛒 Your Shopping Cart & Direct Checkout")
    
    if not st.session_state.cart or sum(st.session_state.cart.values()) == 0:
        st.info("Your shopping cart is empty. Head over to **Digital Menu** to add authentic Punjabi dishes.")
    else:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("Items in Your Order")
            subtotal = 0.0
            order_items_summary = []
            
            for item_name, qty in list(st.session_state.cart.items()):
                if qty > 0:
                    dish = next((d for d in st.session_state.menu if d["name"] == item_name), None)
                    if not dish:
                        continue
                    item_total = dish["price"] * qty
                    subtotal += item_total
                    order_items_summary.append((item_name, qty, dish["price"]))
                    
                    icol1, icol2, icol3, icol4 = st.columns([3, 1, 1, 1])
                    icol1.write(f"**{item_name}** (₹{dish['price']} each)")
                    icol2.write(f"Qty: {qty}")
                    icol3.write(f"₹{item_total}")
                    if icol4.button("❌", key=f"del_{item_name}"):
                        del st.session_state.cart[item_name]
                        st.rerun()
            
            if st.button("Clear Entire Cart"):
                st.session_state.cart = {}
                st.rerun()

        with col2:
            st.subheader("Order Details & Bill Calculation")
            order_type = st.radio("Order Type", ["Home Delivery", "Takeaway Pickup", "Dine-in Table"])
            
            cust_name = st.text_input("Full Name", value="Priya Narayanan")
            cust_phone = st.text_input("Phone Number", value="+91 98860 99881")
            cust_address = st.text_area("Delivery Address / Table No.", value="Flat 402, Green Glen Layout, Chandapura Main Road")
            special_instructions = st.text_input("Cooking / Delivery Notes", value="Please include extra pickled onions.")
            
            tax = round(subtotal * (st.session_state.settings["tax_rate"] / 100), 2)
            packaging = st.session_state.settings["packaging_fee"] if order_type != "Dine-in Table" else 0.0
            delivery = 0.0 if (order_type != "Home Delivery" or subtotal >= st.session_state.settings["free_delivery_threshold"]) else st.session_state.settings["delivery_fee"]
            grand_total = round(subtotal + tax + packaging + delivery, 2)
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 0.75rem; border: 1px solid #ddd; margin: 1rem 0;">
                <div style="display:flex; justify-content:space-between;"><span>Item Subtotal:</span><strong>₹{subtotal:.2f}</strong></div>
                <div style="display:flex; justify-content:space-between;"><span>GST (5%):</span><span>₹{tax:.2f}</span></div>
                <div style="display:flex; justify-content:space-between;"><span>Packaging:</span><span>₹{packaging:.2f}</span></div>
                <div style="display:flex; justify-content:space-between;"><span>Delivery Fee:</span><span>{'FREE (> ₹499)' if delivery == 0 else f'₹{delivery:.2f}'}</span></div>
                <hr style="margin: 0.5rem 0;"/>
                <div style="display:flex; justify-content:space-between; font-size: 1.2rem; color: #641E2B;">
                    <span>Grand Total:</span><strong>₹{grand_total:.2f}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            pay_method = st.selectbox("Payment Method", ["Instant UPI (GPay/PhonePe/Paytm)", "Pay at Restaurant Counter", "Cash on Delivery"])
            
            if pay_method == "Instant UPI (GPay/PhonePe/Paytm)":
                st.info(f"📱 Payee UPI: **{st.session_state.settings['upi_id']}** (Zero convenience fee)")
            
            if st.button("🚀 Confirm & Place Direct Order", use_container_width=True):
                new_id = f"HN-{len(st.session_state.orders) + 2401}"
                new_order = {
                    "id": new_id,
                    "customer": cust_name,
                    "phone": cust_phone,
                    "type": order_type,
                    "channel": "Direct Website",
                    "items": order_items_summary,
                    "subtotal": subtotal,
                    "tax": tax,
                    "packaging": packaging,
                    "delivery": delivery,
                    "total": grand_total,
                    "status": "Order Placed",
                    "payment": f"{pay_method} (Simulated Success)",
                    "address": cust_address,
                    "time": datetime.now().strftime("%I:%M %p Today"),
                }
                st.session_state.orders.insert(0, new_order)
                st.session_state.cart = {}
                st.balloons()
                st.success(f"Order #{new_id} placed successfully! Head to 'Live Order Tracking' to see real-time updates.")

# ---------------- PAGE 4: LIVE ORDER TRACKING ----------------
elif nav == "📍 Live Order Tracking":
    st.title("📍 Live Kitchen & Delivery Tracking Pipeline")
    
    if not st.session_state.orders:
        st.info("No active orders found.")
    else:
        order_ids = [o["id"] for o in st.session_state.orders]
        selected_id = st.selectbox("Select Order to Track", order_ids)
        ord_obj = next((o for o in st.session_state.orders if o["id"] == selected_id), None)
        
        if ord_obj:
            st.subheader(f"Order #{ord_obj['id']} – {ord_obj['customer']}")
            st.write(f"**Channel**: {ord_obj['channel']} | **Type**: {ord_obj['type']} | **Placed**: {ord_obj['time']}")
            
            # Pipeline status indicator
            stages = ["Order Placed", "Accepted", "In Kitchen Prep", "Food Ready", "Completed"]
            current_stage = ord_obj["status"]
            stage_idx = stages.index(current_stage) if current_stage in stages else 0
            
            prog_cols = st.columns(len(stages))
            for idx, stage in enumerate(stages):
                with prog_cols[idx]:
                    if idx <= stage_idx:
                        st.success(f"✓ **{stage}**")
                    else:
                        st.caption(f"○ {stage}")
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### Items Ordered")
                for iname, iqty, iprice in ord_obj["items"]:
                    st.write(f"• **{iqty}x** {iname} — ₹{iqty * iprice}")
                st.write(f"**Total Amount Paid**: ₹{ord_obj['total']:.2f}")
                st.write(f"**Payment Status**: {ord_obj['payment']}")
            
            with c2:
                st.markdown("### Delivery Destination")
                st.write(f"**Address**: {ord_obj['address']}")
                st.write(f"**Contact**: {ord_obj['phone']}")
                
                with st.expander("📄 Print 80mm Thermal Tax Receipt"):
                    items_text = "".join([f"{name[:18]:<18} {qty:>2}x  Rs.{qty*pr:>4}\n" for name, qty, pr in ord_obj["items"]])
                    st.markdown(f"""
                    <div class="thermal-receipt">
                        <center>
                            <strong>{st.session_state.settings['name'].upper()}</strong><br/>
                            {st.session_state.settings['tagline']}<br/>
                            {st.session_state.settings['address']}<br/>
                            Phone: {st.session_state.settings['phone']}<br/>
                            --------------------------------<br/>
                            INVOICE #: {ord_obj['id']}<br/>
                            TIME: {ord_obj['time']}<br/>
                            TYPE: {ord_obj['type']}<br/>
                            --------------------------------<br/>
                        </center>
                        <pre style="font-size:0.8rem;">
ITEM                QTY   TOTAL
--------------------------------
{items_text}--------------------------------
SUBTOTAL:                Rs.{ord_obj['subtotal']}
GST (5%):                Rs.{ord_obj['tax']}
PACKAGING/DELIVERY:      Rs.{ord_obj['packaging'] + ord_obj['delivery']}
TOTAL PAYABLE:           Rs.{ord_obj['total']}
--------------------------------
MODE: {ord_obj['payment']}
        THANK YOU FOR DINING!
                        </pre>
                    </div>
                    """, unsafe_allow_html=True)

# ---------------- PAGE 5: EXECUTIVE MIS & SALES ANALYTICS ----------------
elif nav == "📊 Executive MIS & Sales Analytics":
    st.title("📊 Restaurant Executive Management Dashboard (MIS)")
    
    total_sales = sum(o["total"] for o in st.session_state.orders)
    total_orders = len(st.session_state.orders)
    aov = total_sales / total_orders if total_orders > 0 else 0.0
    pending_orders = sum(1 for o in st.session_state.orders if o["status"] != "Completed")
    low_stock_count = sum(1 for ing in st.session_state.inventory.values() if ing["stock"] <= ing["reorder"])
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Today's Revenue", f"₹{total_sales:,.2f}", "+14% vs yesterday")
    k2.metric("Total Orders", f"{total_orders}", "Direct & POS")
    k3.metric("Average Order Value", f"₹{aov:.2f}", "Healthy AOV")
    k4.metric("Low Stock Alerts", f"{low_stock_count} Items", "Requires Reorder", delta_color="inverse")
    
    st.markdown("---")
    
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("7-Day Sales Trend (₹)")
        trend_df = pd.DataFrame([
            {"Date": "27 Oct", "Sales": 11200},
            {"Date": "28 Oct", "Sales": 6800},
            {"Date": "29 Oct", "Sales": 7900},
            {"Date": "30 Oct", "Sales": 8600},
            {"Date": "31 Oct", "Sales": 9400},
            {"Date": "01 Nov", "Sales": 13500},
            {"Date": "Today", "Sales": int(total_sales)},
        ])
        fig_trend = px.area(trend_df, x="Date", y="Sales", color_discrete_sequence=["#641E2B"])
        fig_trend.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.subheader("Order Channel Breakdown")
        channel_counts = {}
        for o in st.session_state.orders:
            channel_counts[o["channel"]] = channel_counts.get(o["channel"], 0) + 1
        
        ch_df = pd.DataFrame(list(channel_counts.items()), columns=["Channel", "Orders"])
        fig_ch = px.pie(ch_df, names="Channel", values="Orders", color_discrete_sequence=["#641E2B", "#C69A45", "#33251F", "#F97316"])
        fig_ch.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig_ch, use_container_width=True)

# ---------------- PAGE 6: KITCHEN QUEUE & ORDER MANAGEMENT ----------------
elif nav == "🍳 Kitchen Queue & Order Management":
    st.title("🍳 Live Kitchen Queue & Order Processing")
    st.caption("Change status here to trigger live progress updates on the customer tracking screen.")
    
    for ord_obj in st.session_state.orders:
        with st.container():
            st.markdown(f"""
            <div style="background:white; border-radius:1rem; padding:1.25rem; border:1px solid #ddd; margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between;">
                    <h3 style="margin:0; color:#641E2B;">#{ord_obj['id']} — {ord_obj['customer']}</h3>
                    <span style="font-weight:bold; font-size:1.1rem;">₹{ord_obj['total']:.2f}</span>
                </div>
                <p style="margin:0.25rem 0; color:#555;">Type: <strong>{ord_obj['type']}</strong> | Channel: <strong>{ord_obj['channel']}</strong> | Placed: {ord_obj['time']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns([3, 2])
            with c1:
                st.write("**Dishes on Ticket:**")
                for iname, iqty, iprice in ord_obj["items"]:
                    st.write(f"• **{iqty}x** {iname}")
            
            with c2:
                stages = ["Order Placed", "Accepted", "In Kitchen Prep", "Food Ready", "Completed"]
                current_idx = stages.index(ord_obj["status"]) if ord_obj["status"] in stages else 0
                
                new_status = st.selectbox(
                    f"Update Status for #{ord_obj['id']}",
                    stages,
                    index=current_idx,
                    key=f"status_{ord_obj['id']}"
                )
                
                if new_status != ord_obj["status"]:
                    if new_status == "In Kitchen Prep" and ord_obj["status"] != "In Kitchen Prep":
                        deduct_recipe(ord_obj["items"])
                        st.toast("Auto-depleted raw materials from inventory based on recipe quantities!")
                    ord_obj["status"] = new_status
                    st.success(f"Status updated to: {new_status}")
                    st.rerun()

# ---------------- PAGE 7: STAFF POS TERMINAL ----------------
elif nav == "🏪 Staff POS Terminal (Dine-in / Takeaway)":
    st.title("🏪 Staff POS Billing Terminal")
    st.caption("Create orders directly at the counter or tables without customer app dependency.")
    
    pcol1, pcol2 = st.columns([3, 2])
    with pcol1:
        st.subheader("Menu Quick Grid")
        pos_cat = st.selectbox("Filter Category", ["All"] + sorted(list(set(d["category"] for d in st.session_state.menu))), key="pos_cat")
        
        pos_dishes = [d for d in st.session_state.menu if pos_cat == "All" or d["category"] == pos_cat]
        grid_cols = st.columns(3)
        for idx, d in enumerate(pos_dishes):
            with grid_cols[idx % 3]:
                if st.button(f"{d['name']}\n₹{d['price']}", key=f"pos_add_{d['id']}"):
                    st.session_state.cart[d["name"]] = st.session_state.cart.get(d["name"], 0) + 1
                    st.rerun()

    with pcol2:
        st.subheader("Current Bill Ticket")
        pos_type = st.radio("Order Service", ["Dine-in (Table Service)", "Takeaway Counter"], horizontal=True)
        table_num = st.selectbox("Table Number", [f"Table {i}" for i in range(1, 13)]) if "Dine-in" in pos_type else "Takeaway"
        
        pos_subtotal = 0.0
        pos_items = []
        for iname, qty in list(st.session_state.cart.items()):
            if qty > 0:
                dish = next((d for d in st.session_state.menu if d["name"] == iname), None)
                if not dish:
                    continue
                pos_subtotal += dish["price"] * qty
                pos_items.append((iname, qty, dish["price"]))
                st.write(f"• **{qty}x** {iname} — ₹{dish['price'] * qty}")
        
        pos_tax = round(pos_subtotal * 0.05, 2)
        pos_total = pos_subtotal + pos_tax
        
        st.markdown(f"**Total Payable**: <span style='font-size:1.4rem; color:#641E2B;'>₹{pos_total:.2f}</span>", unsafe_allow_html=True)
        pos_pay = st.selectbox("Payment Mode", ["Cash Counter", "UPI QR Code", "Card"])
        
        if st.button("🖨️ Print Receipt & Dispatch to Kitchen", use_container_width=True, disabled=(pos_subtotal == 0)):
            new_id = f"HN-{len(st.session_state.orders) + 2401}"
            st.session_state.orders.insert(0, {
                "id": new_id,
                "customer": f"{table_num} (Walk-in)",
                "phone": "+91 98000 00000",
                "type": pos_type,
                "channel": "Staff POS",
                "items": pos_items,
                "subtotal": pos_subtotal,
                "tax": pos_tax,
                "packaging": 0.0,
                "delivery": 0.0,
                "total": pos_total,
                "status": "In Kitchen Prep",
                "payment": pos_pay,
                "address": table_num,
                "time": datetime.now().strftime("%I:%M %p Today"),
            })
            deduct_recipe(pos_items)
            st.session_state.cart = {}
            st.success(f"Generated Ticket #{new_id} & printed thermal bill!")
            st.rerun()

# ---------------- PAGE 8: INVENTORY & STOCK ----------------
elif nav == "📦 Recipe-Linked Inventory & Stock":
    st.title("📦 Raw Material Inventory & Recipe Depletion")
    st.caption("Ingredient stock levels are automatically decremented when kitchen starts preparing orders.")
    
    inv_data = []
    for k, v in st.session_state.inventory.items():
        is_low = v["stock"] <= v["reorder"]
        inv_data.append({
            "Ingredient": v["name"],
            "Current Stock": f"{v['stock']} {v['unit']}",
            "Reorder Level": f"{v['reorder']} {v['unit']}",
            "Unit Rate": f"₹{v['cost']}/{v['unit']}",
            "Supplier": v["supplier"],
            "Status": "⚠️ LOW STOCK" if is_low else "✓ Sufficient"
        })
    
    st.dataframe(pd.DataFrame(inv_data), use_container_width=True)
    
    st.subheader("Manual Stock Adjustment")
    adj_col1, adj_col2, adj_col3 = st.columns(3)
    with adj_col1:
        sel_ing = st.selectbox("Select Material", list(st.session_state.inventory.keys()), format_func=lambda k: st.session_state.inventory[k]["name"])
    with adj_col2:
        delta = st.number_input("Stock Change (+ to add, - to subtract)", value=5.0, step=0.5)
    with adj_col3:
        st.write("")
        st.write("")
        if st.button("Apply Stock Adjustment"):
            st.session_state.inventory[sel_ing]["stock"] = max(0.0, round(st.session_state.inventory[sel_ing]["stock"] + delta, 2))
            st.success("Updated inventory stock level successfully!")
            st.rerun()

# ---------------- PAGE 9: MENU MANAGEMENT & PRICING CONTROL ----------------
elif nav == "📑 Menu Catalog & Pricing Control":
    st.title("📑 Menu Catalog & Pricing Control")
    st.caption("Update prices, toggle real-time dish availability, or add authentic recipes directly.")
    
    t1, t2 = st.tabs(["📋 Edit Existing Dishes", "➕ Add New Dish to Menu"])
    
    with t1:
        menu_items_display = []
        for d in st.session_state.menu:
            menu_items_display.append({
                "ID": d["id"],
                "Dish Name": d["name"],
                "Category": d["category"],
                "Price (₹)": d["price"],
                "Special": "⭐ Yes" if d.get("chef_special") else "No",
                "Available": "✓ In Stock" if d.get("available", True) else "❌ Out of Stock",
            })
        st.dataframe(pd.DataFrame(menu_items_display), use_container_width=True)
        
        st.subheader("Quick Item Editor")
        edit_dish_name = st.selectbox("Select Dish to Modify", [d["name"] for d in st.session_state.menu])
        target_dish = next((d for d in st.session_state.menu if d["name"] == edit_dish_name), None)
        
        if target_dish:
            e_col1, e_col2, e_col3 = st.columns(3)
            with e_col1:
                new_price = st.number_input("Price (₹)", value=int(target_dish["price"]), step=5)
            with e_col2:
                new_avail = st.checkbox("Available in Kitchen", value=target_dish.get("available", True))
            with e_col3:
                new_special = st.checkbox("Chef's Special Recommendation", value=target_dish.get("chef_special", False))
                
            new_desc = st.text_area("Dish Description", value=target_dish.get("desc", ""))
            
            if st.button("Save Dish Changes"):
                target_dish["price"] = new_price
                target_dish["available"] = new_avail
                target_dish["chef_special"] = new_special
                target_dish["desc"] = new_desc
                st.success(f"Updated '{target_dish['name']}' successfully!")
                st.rerun()

    with t2:
        st.subheader("Add Authentic Punjabi Recipe")
        n1, n2, n3 = st.columns(3)
        with n1:
            new_name = st.text_input("Dish Name (e.g. Amritsari Chole Kulche)")
        with n2:
            new_cat = st.selectbox("Category", sorted(list(set(d["category"] for d in st.session_state.menu))))
        with n3:
            new_pr = st.number_input("Selling Price (₹)", min_value=10, value=150, step=10)
            
        new_d = st.text_input("Description", value="Authentic slow-simmered Punjabi spices served piping hot.")
        
        if st.button("Add Dish to Live Menu"):
            if new_name.strip():
                new_item = {
                    "id": f"cust_{len(st.session_state.menu)+1}",
                    "name": new_name.strip(),
                    "category": new_cat,
                    "price": new_pr,
                    "desc": new_d.strip(),
                    "chef_special": False,
                    "prep_time": 15,
                    "available": True,
                    "recipe": {}
                }
                st.session_state.menu.append(new_item)
                st.success(f"Added '{new_name}' to digital menu!")
                st.rerun()
            else:
                st.error("Please enter a valid dish name.")

# ---------------- PAGE 10: PURCHASES & PROCUREMENT ----------------
elif nav == "🚚 Purchases & Supplier Procurement":
    st.title("🚚 Raw Material Procurement & Deliveries")
    st.caption("Logging a delivery here automatically updates raw material inventory stock.")
    
    st.subheader("Recorded Supplier Deliveries")
    st.dataframe(pd.DataFrame(st.session_state.purchases), use_container_width=True)
    
    with st.expander("➕ Log New Raw Material Shipment"):
        p1, p2, p3 = st.columns(3)
        with p1:
            pur_ing = st.selectbox("Ingredient", list(st.session_state.inventory.keys()), format_func=lambda k: st.session_state.inventory[k]["name"])
        with p2:
            pur_qty = st.number_input("Quantity Received", min_value=1.0, value=10.0)
        with p3:
            pur_cost = st.number_input("Total Invoice Amount (₹)", min_value=100.0, value=2500.0)
        
        pur_supplier = st.text_input("Supplier Name", value="Nandini Dairy Wholesale Anekal")
        pur_inv = st.text_input("Invoice Number", value="INV-9901")
        
        if st.button("Save Delivery & Replenish Stock"):
            st.session_state.purchases.insert(0, {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "ingredient": st.session_state.inventory[pur_ing]["name"],
                "qty": f"{pur_qty} {st.session_state.inventory[pur_ing]['unit']}",
                "cost": pur_cost,
                "supplier": pur_supplier,
                "invoice": pur_inv
            })
            st.session_state.inventory[pur_ing]["stock"] += pur_qty
            st.success("Shipment recorded and inventory stock replenished!")
            st.rerun()

# ---------------- PAGE 11: SALES & EXPENSES MIS ----------------
elif nav == "💰 Sales & Operating Expenses MIS":
    st.title("💰 Sales & Operating Expenses MIS")
    st.info("📌 **MBA Management Estimate**: This prototype tracks indicative operating surplus (Revenue minus logged overheads) for operational visibility, not audited net profit.")
    
    rev = sum(o["total"] for o in st.session_state.orders)
    exp = sum(e["amount"] for e in st.session_state.expenses)
    surplus = rev - exp
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Recorded Revenue", f"₹{rev:,.2f}")
    m2.metric("Recorded Overheads", f"₹{exp:,.2f}")
    m3.metric("Indicative Operating Surplus", f"₹{surplus:,.2f}", "Before depreciation & taxes")
    
    st.subheader("Expense Log Sheet")
    st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)
    
    with st.expander("➕ Log Operating Expense Voucher"):
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            exp_cat = st.selectbox("Category", ["Rent", "Salaries", "Gas", "Electricity", "Packaging", "Other"])
        with ec2:
            exp_amt = st.number_input("Voucher Amount (₹)", value=2100.0)
        with ec3:
            exp_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Bank Transfer"])
        exp_desc = st.text_input("Voucher Description", value="Commercial LPG cylinder refill")
        
        if st.button("Record Expense"):
            st.session_state.expenses.insert(0, {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "category": exp_cat,
                "amount": exp_amt,
                "desc": exp_desc,
                "mode": exp_mode
            })
            st.success("Expense voucher recorded successfully!")
            st.rerun()

# ---------------- PAGE 12: CUSTOMER RETENTION & WHATSAPP ----------------
elif nav == "👥 Customer Retention & WhatsApp Re-engagement":
    st.title("👥 Customer Retention & Relocation Outreach")
    st.write("Addresses post-relocation discovery drop: reconnect with lapsed regulars via personalized WhatsApp messages.")
    
    st.dataframe(pd.DataFrame(st.session_state.customers), use_container_width=True)
    
    st.subheader("Generate Personalized Relocation Re-Engagement Message")
    sel_cust = st.selectbox("Select Customer to Reconnect", st.session_state.customers, format_func=lambda c: f"{c['name']} ({c['status']})")
    
    default_msg = f"Hello {sel_cust['name']}! We miss you at H&N Punjabi Food Junction! We have relocated to Chandapura–Anekal Main Road with our signature Dal Makhani, layered tandoori Kulchas, and thick Lassi. Order directly on our website for 15% OFF using code ANEKAL15!"
    wa_text = st.text_area("WhatsApp Draft Message", value=default_msg, height=100)
    
    st.caption("Responsible Outreach Policy: Messages require manual patron click and opt-in before sending.")
    wa_url = f"https://wa.me/{sel_cust['phone'].replace(' ', '').replace('+', '')}?text={wa_text.replace(' ', '%20')}"
    st.markdown(f'<a href="{wa_url}" target="_blank" style="background-color:#25D366; color:white; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:bold;">📲 Open in WhatsApp</a>', unsafe_allow_html=True)

# ---------------- PAGE 13: SETTINGS ----------------
elif nav == "⚙️ Restaurant Settings":
    st.title("⚙️ Restaurant Operating Settings")
    
    s1, s2 = st.columns(2)
    with s1:
        st.session_state.settings["name"] = st.text_input("Restaurant Name", value=st.session_state.settings["name"])
        st.session_state.settings["tagline"] = st.text_input("Brand Tagline", value=st.session_state.settings["tagline"])
        st.session_state.settings["address"] = st.text_area("Address (Chandapura-Anekal Rd)", value=st.session_state.settings["address"])
    with s2:
        st.session_state.settings["phone"] = st.text_input("Phone Number", value=st.session_state.settings["phone"])
        st.session_state.settings["hours"] = st.text_input("Operating Hours", value=st.session_state.settings["hours"])
        st.session_state.settings["upi_id"] = st.text_input("Merchant UPI VPA", value=st.session_state.settings["upi_id"])
    
    if st.button("Save Settings"):
        st.success("Restaurant settings updated successfully!")

# ---------------- PAGE 14: MBA DOCUMENTATION & ARCHITECTURE ----------------
elif nav == "📖 MBA Project & Architecture Docs":
    st.title("📖 MBA Project Documentation & System Architecture")
    st.caption("Design Thinking, Disruptive Technology & Innovation (DTDTI) Academic Capstone")
    
    doc_tab1, doc_tab2, doc_tab3 = st.tabs(["🎯 Strategic Context", "🛡️ RBAC & Cloud Architecture", "🧪 Workflow Verification"])
    
    with doc_tab1:
        st.subheader("1. Executive Context & Core Problem Statement")
        st.markdown("""
        * **Business**: H&N Punjabi Food Junction (Proprietors: Manjeet Singh & spouse)
        * **Location**: Relocated to Chandapura–Anekal Main Road, Anekal, Bengaluru (562106)
        * **Heritage**: 100% Pure Vegetarian Authentic Punjabi Cuisine
        
        **Dual Crisis Addressed by Platform**:
        1. **Post-Relocation Footfall Chasm**: Physical discovery loss after shifting premises. Solved by direct digital ordering channel & WhatsApp re-engagement.
        2. **Aggregator Margin Erosion**: Third-party aggregators (Swiggy/Zomato) extract 25–30% commission per order, eliminating vegetarian operating margins. Direct web ordering recovers this value completely.
        """)
        
    with doc_tab2:
        st.subheader("2. Role-Based Access Control (RBAC) Architecture")
        rbac_df = pd.DataFrame([
            {"Persona": "Manjeet Singh", "Role": "Owner", "Permissions": "Full access to settings, overheads, MIS & menu pricing"},
            {"Persona": "Gurpreet Kaur", "Role": "Manager", "Permissions": "Kitchen orders, stock inventory, supplier purchases, sales"},
            {"Persona": "Harpreet Sharma", "Role": "Kitchen Staff", "Permissions": "Live kitchen order progression & touch POS billing"},
            {"Persona": "Priya Narayanan", "Role": "Customer", "Permissions": "Digital menu, direct checkout, live stage tracking"},
        ])
        st.table(rbac_df)
        
        with st.expander("Cloud Firestore Security Rules Specification"):
            st.code("""
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isAuthenticated() { return request.auth != null; }
    function isOwner() { return isAuthenticated() && request.auth.token.role == 'owner'; }
    function isManager() { return isAuthenticated() && (request.auth.token.role in ['owner', 'manager']); }
    function isEmployee() { return isAuthenticated() && (request.auth.token.role in ['owner', 'manager', 'employee']); }

    match /orders/{orderId} {
      allow read: if isEmployee() || (isAuthenticated() && resource.data.customerId == request.auth.uid);
      allow create: if true; // Public checkout
      allow update: if isEmployee();
    }
    match /inventory/{ingId} {
      allow read: if isEmployee();
      allow write: if isManager();
    }
  }
}
            """, language="javascript")
            
    with doc_tab3:
        st.subheader("3. 18 Verified End-to-End Business Workflows")
        st.markdown("""
        - [x] **Phase 1: Customer Auth & Account** (Profile persistence & demo login)
        - [x] **Phase 2: Digital Menu Exploration** (33 dishes across 11 verified categories)
        - [x] **Phase 3: Direct Web Checkout** (Zero aggregator fee, 5% GST, free delivery logic)
        - [x] **Phase 4: Kitchen Pipeline** (Live status transition & automatic recipe deduction)
        - [x] **Phase 5: Inventory & Purchases** (Malai paneer, atta, desi ghee auto-depletion)
        - [x] **Phase 6: Operating MIS** (Overheads vs revenue indicative operating surplus)
        - [x] **Phase 7: Touch POS & Receipt** (80mm thermal receipt generator)
        """)
