import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import time
import plotly.express as px
import speech_recognition as sr
import io
import re

load_dotenv()

# ===================== PRODUCT IMAGE HELPER =====================
# Comprehensive product images covering everything a girl needs
PRODUCT_IMAGES = {
    # --- Clothing ---
    "kurta":       "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=300&h=300&fit=crop",
    "kurti":       "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=300&h=300&fit=crop",
    "saree":       "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=300&h=300&fit=crop",
    "dress":       "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300&h=300&fit=crop",
    "dupatta":     "https://images.unsplash.com/photo-1617627191896-067d9b15a4f7?w=300&h=300&fit=crop",
    "lehenga":     "https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=300&h=300&fit=crop",
    "gown":        "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=300&h=300&fit=crop",
    "top":         "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=300&h=300&fit=crop",
    "t-shirt":     "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=300&fit=crop",
    "jeans":       "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=300&h=300&fit=crop",
    "leggings":    "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=300&h=300&fit=crop",
    "palazzo":     "https://images.unsplash.com/photo-1509551388413-e18d0ac5d495?w=300&h=300&fit=crop",
    "nightwear":   "https://images.unsplash.com/photo-1617475375508-25276f0c108b?w=300&h=300&fit=crop",
    "innerwear":   "https://images.unsplash.com/photo-1582533561751-ef6f6ab93a2e?w=300&h=300&fit=crop",
    # --- Seasonal ---
    "summer":      "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=300&h=300&fit=crop",
    "cotton":      "https://images.unsplash.com/photo-1558171813-4c088753af8f?w=300&h=300&fit=crop",
    "winter":      "https://images.unsplash.com/photo-1544441893-675973e31985?w=300&h=300&fit=crop",
    "shawl":       "https://images.unsplash.com/photo-1601244005535-a48d21d951ac?w=300&h=300&fit=crop",
    "jacket":      "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=300&h=300&fit=crop",
    "sweater":     "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=300&h=300&fit=crop",
    "monsoon":     "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=300&h=300&fit=crop",
    "raincoat":    "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=300&h=300&fit=crop",
    # --- Jewelry & Accessories ---
    "jewelry":     "https://images.unsplash.com/photo-1515562141589-67f0d93e3876?w=300&h=300&fit=crop",
    "jhumka":      "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=300&h=300&fit=crop",
    "earring":     "https://images.unsplash.com/photo-1630019852942-f89202989a59?w=300&h=300&fit=crop",
    "necklace":    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=300&h=300&fit=crop",
    "bangle":      "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=300&h=300&fit=crop",
    "ring":        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=300&h=300&fit=crop",
    "bracelet":    "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=300&h=300&fit=crop",
    "pendant":     "https://images.unsplash.com/photo-1599643477877-530eb83abc8e?w=300&h=300&fit=crop",
    "chain":       "https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=300&h=300&fit=crop",
    "mangalsutra": "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=300&h=300&fit=crop",
    "anklet":      "https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=300&h=300&fit=crop",
    "watch":       "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=300&h=300&fit=crop",
    # --- Cosmetics & Beauty ---
    "lipstick":    "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=300&h=300&fit=crop",
    "makeup":      "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300&h=300&fit=crop",
    "foundation":  "https://images.unsplash.com/photo-1631730486572-226d1f595b68?w=300&h=300&fit=crop",
    "mascara":     "https://images.unsplash.com/photo-1631214524020-7e18db9a8f69?w=300&h=300&fit=crop",
    "skincare":    "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=300&h=300&fit=crop",
    "moisturizer": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=300&h=300&fit=crop",
    "sunscreen":   "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop",
    "perfume":     "https://images.unsplash.com/photo-1541643600914-78b084683601?w=300&h=300&fit=crop",
    "nail polish": "https://images.unsplash.com/photo-1604654894610-df63bc536371?w=300&h=300&fit=crop",
    "blush":       "https://images.unsplash.com/photo-1599733594230-6b823276abcc?w=300&h=300&fit=crop",
    "eyeliner":    "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=300&h=300&fit=crop",
    "haircare":    "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=300&h=300&fit=crop",
    "hair oil":    "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=300&h=300&fit=crop",
    "shampoo":     "https://images.unsplash.com/photo-1585232004423-244e0e6904e3?w=300&h=300&fit=crop",
    "face wash":   "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=300&h=300&fit=crop",
    # --- Bags & Shoes ---
    "handbag":     "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop",
    "clutch":      "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=300&h=300&fit=crop",
    "purse":       "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=300&h=300&fit=crop",
    "sandal":      "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop",
    "heels":       "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop",
    "sneakers":    "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=300&h=300&fit=crop",
    "jutti":       "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop",
    # --- Occasion ---
    "wedding":     "https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=300&h=300&fit=crop",
    "festival":    "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?w=300&h=300&fit=crop",
    "party":       "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?w=300&h=300&fit=crop",
    "casual":      "https://images.unsplash.com/photo-1485231183945-fffde7cc051e?w=300&h=300&fit=crop",
    "office":      "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=300&h=300&fit=crop",
    # --- General ---
    "trending":    "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=300&h=300&fit=crop",
    "fashion":     "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=300&h=300&fit=crop",
    "beauty":      "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=300&h=300&fit=crop",
    "accessories": "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=300&h=300&fit=crop",
    "cosmetics":   "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300&h=300&fit=crop",
}

# Month-wise default product sets (what sells best each month)
MONTH_PRODUCTS = {
    1:  ["winter", "shawl", "moisturizer", "sweater"],
    2:  ["winter", "jacket", "skincare", "shawl"],
    3:  ["cotton", "kurti", "sunscreen", "sandal"],
    4:  ["summer", "cotton", "sunglasses", "sandal"],
    5:  ["summer", "kurti", "sunscreen", "cotton"],
    6:  ["summer", "dress", "sandal", "perfume"],
    7:  ["monsoon", "raincoat", "kurta", "sandal"],
    8:  ["festival", "saree", "jhumka", "bangle"],
    9:  ["festival", "lehenga", "necklace", "makeup"],
    10: ["festival", "saree", "jhumka", "lipstick"],
    11: ["wedding", "lehenga", "jewelry", "makeup"],
    12: ["wedding", "shawl", "perfume", "gown"],
}

# General fallback: everything a girl needs
GIRL_ESSENTIALS = ["kurti", "saree", "jhumka", "lipstick", "makeup", "skincare",
                    "handbag", "sandal", "bangle", "perfume", "necklace", "dress"]

def get_product_images(query: str):
    """Return matching product image URLs based on keywords in the query."""
    from datetime import datetime
    query_lower = query.lower()
    matched = []
    seen = set()

    # Keyword matching
    for keyword, url in PRODUCT_IMAGES.items():
        if keyword in query_lower and keyword not in seen:
            matched.append((keyword, url))
            seen.add(keyword)

    # If query mentions a month or season, add month-based products
    month = datetime.now().month
    month_keywords = MONTH_PRODUCTS.get(month, [])
    for kw in month_keywords:
        if kw not in seen and kw in PRODUCT_IMAGES:
            matched.append((kw, PRODUCT_IMAGES[kw]))
            seen.add(kw)

    # If still less than 6, pad with girl-essentials
    if len(matched) < 6:
        for kw in GIRL_ESSENTIALS:
            if kw not in seen and kw in PRODUCT_IMAGES:
                matched.append((kw, PRODUCT_IMAGES[kw]))
                seen.add(kw)
            if len(matched) >= 8:
                break

    return matched[:8]  # Max 8 images

def render_product_images(query: str):
    """Render a grid of product images matching the query keywords."""
    images = get_product_images(query)
    # Render in rows of 4
    for row_start in range(0, len(images), 4):
        row = images[row_start:row_start + 4]
        cols = st.columns(len(row))
        for col, (keyword, url) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div style="text-align:center; background:rgba(255,255,255,0.85); border-radius:16px;
                            padding:10px; box-shadow:0 4px 16px rgba(192,38,211,0.18);
                            border:2px solid #e879f9; margin-bottom:12px;">
                    <img src="{url}" style="width:100%; border-radius:12px; aspect-ratio:1; object-fit:cover;">
                    <p style="color:#7e22ce; font-weight:800; font-size:0.85rem; margin-top:6px;">
                        {keyword.title()}
                    </p>
                </div>
                """, unsafe_allow_html=True)

st.set_page_config(page_title="Meesho Reseller Success Coach", page_icon="👩‍💼", layout="wide")

# ===================== HACKATHON TECH STYLING =====================
st.markdown("""
<style>
    /* --- Dark cyber / tech grid background --- */
    .stApp {
        background:
            radial-gradient(ellipse 70% 50% at 15% 85%, rgba(0,212,255,0.08) 0%, transparent 60%),
            radial-gradient(ellipse 50% 60% at 85% 15%, rgba(16,185,129,0.07) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 50% 50%, rgba(59,130,246,0.05) 0%, transparent 60%),
            linear-gradient(180deg, #060a12 0%, #0a1225 30%, #081018 60%, #050810 100%);
        background-attachment: fixed;
    }

    /* --- Animated grid lines (circuit board / matrix feel) --- */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px),
            linear-gradient(rgba(16,185,129,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(16,185,129,0.03) 1px, transparent 1px);
        background-size: 60px 60px, 60px 60px, 240px 240px, 240px 240px;
        pointer-events: none;
        z-index: 0;
        animation: gridPulse 6s ease-in-out infinite;
    }
    @keyframes gridPulse {
        0%, 100% { opacity: 0.6; }
        50%      { opacity: 1; }
    }

    /* --- Floating data nodes (global network dots) --- */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            radial-gradient(3px 3px at 12% 18%, rgba(0,212,255,0.6) 0%, transparent 100%),
            radial-gradient(2px 2px at 28% 42%, rgba(16,185,129,0.5) 0%, transparent 100%),
            radial-gradient(3px 3px at 45% 12%, rgba(0,212,255,0.5) 0%, transparent 100%),
            radial-gradient(2px 2px at 62% 55%, rgba(59,130,246,0.4) 0%, transparent 100%),
            radial-gradient(3px 3px at 78% 22%, rgba(16,185,129,0.55) 0%, transparent 100%),
            radial-gradient(2px 2px at 88% 68%, rgba(0,212,255,0.45) 0%, transparent 100%),
            radial-gradient(2px 2px at 18% 72%, rgba(59,130,246,0.4) 0%, transparent 100%),
            radial-gradient(3px 3px at 35% 88%, rgba(0,212,255,0.5) 0%, transparent 100%),
            radial-gradient(2px 2px at 55% 78%, rgba(16,185,129,0.45) 0%, transparent 100%),
            radial-gradient(3px 3px at 72% 85%, rgba(59,130,246,0.5) 0%, transparent 100%),
            radial-gradient(2px 2px at 92% 38%, rgba(0,212,255,0.4) 0%, transparent 100%),
            radial-gradient(2px 2px at 5% 50%, rgba(16,185,129,0.35) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
        animation: nodePulse 4s ease-in-out infinite;
    }
    @keyframes nodePulse {
        0%, 100% { opacity: 0.5; }
        50%      { opacity: 1; }
    }

    /* --- Header --- */
    .main-header {
        font-size: 3.4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #22d3ee, #3b82f6, #10b981, #22d3ee);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        text-align: center;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 40px rgba(34,211,238,0.3);
    }
    @keyframes shimmer {
        to { background-position: 300% center; }
    }
    .sub-header {
        text-align: center;
        font-size: 1.15rem;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }

    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(10,18,40,0.7);
        color: #94a3b8 !important;
        border-radius: 12px 12px 0 0;
        padding: 10px 22px;
        font-weight: 700;
        font-size: 1rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(34,211,238,0.12);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0891b2, #3b82f6) !important;
        color: white !important;
        border: 1px solid rgba(34,211,238,0.3) !important;
        box-shadow: 0 4px 25px rgba(34,211,238,0.25);
    }

    /* --- Metric cards --- */
    div[data-testid="stMetric"] {
        background: rgba(8,14,28,0.7);
        border: 1px solid rgba(34,211,238,0.15);
        border-radius: 16px;
        padding: 16px 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        backdrop-filter: blur(15px);
    }
    div[data-testid="stMetricLabel"] { color: #94a3b8; font-weight: 700; }
    div[data-testid="stMetricValue"] { color: #22d3ee; font-weight: 900; }

    /* --- Containers & chat --- */
    .stChatMessage {
        border-radius: 16px !important;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background: rgba(8,14,28,0.7) !important;
        border-left: 3px solid #22d3ee !important;
        backdrop-filter: blur(15px);
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background: rgba(8,20,14,0.7) !important;
        border-left: 3px solid #10b981 !important;
        backdrop-filter: blur(15px);
    }
    .stChatMessage p, .stChatMessage li, .stChatMessage strong {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    .stChatMessage h1, .stChatMessage h2, .stChatMessage h3 {
        color: #22d3ee !important;
        font-weight: 900 !important;
    }

    /* --- Demo mode banner --- */
    .demo-banner {
        background: rgba(8,20,14,0.6);
        color: #4ade80 !important;
        padding: 18px 24px;
        border-radius: 14px;
        font-weight: 800 !important;
        font-size: 1rem !important;
        text-align: center;
        border: 1px solid rgba(16,185,129,0.25);
        backdrop-filter: blur(15px);
    }

    /* --- Buttons --- */
    .stButton > button {
        background: linear-gradient(135deg, #0891b2, #3b82f6);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 30px;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 4px 25px rgba(34,211,238,0.25);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #0891b2);
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(34,211,238,0.4);
    }

    /* --- File uploader --- */
    .stFileUploader {
        border: 2px dashed rgba(34,211,238,0.25);
        border-radius: 16px;
        background: rgba(8,12,20,0.5);
    }

    /* --- Feature cards --- */
    .feature-card {
        background: rgba(8,14,28,0.65);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.35);
        border: 1px solid rgba(34,211,238,0.12);
        backdrop-filter: blur(15px);
        transition: transform 0.3s, box-shadow 0.3s;
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #22d3ee, #10b981, transparent);
    }
    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 15px 50px rgba(34,211,238,0.15);
        border-color: rgba(34,211,238,0.3);
    }
    .feature-card h3 { color: #22d3ee; margin: 8px 0 4px; font-size: 1.2rem; }
    .feature-card p  { color: #94a3b8; font-size: 0.95rem; }
    .feature-card .icon-3d {
        font-size: 3rem;
        display: block;
        margin-bottom: 10px;
        filter: drop-shadow(0 4px 12px rgba(34,211,238,0.4));
    }

    .overlay {
        background: rgba(8,14,28,0.65);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(34,211,238,0.1);
    }

    /* --- General text --- */
    p, li, span, label, .stCaption { color: #e2e8f0 !important; }
    h1, h2, h3, h4, h5 { color: #f1f5f9 !important; }
    strong { color: #22d3ee !important; }
</style>
""", unsafe_allow_html=True)

# ===================== HEADER & HERO =====================
st.markdown('<h1 class="main-header">🛍️ Agentic Reseller Success Coach</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">🚀 Built for Meesho ScriptedBy{Her} 2.0 Hackathon — Your AI Business Mentor for Women Resellers in Bharat 🚀</p>', unsafe_allow_html=True)

# Hackathon hero banner — global tech / coding theme
st.markdown("""
<div style="position:relative; overflow:hidden; border-radius:20px; padding:30px 24px; margin:16px 0;
            background: linear-gradient(135deg, rgba(8,14,28,0.85), rgba(10,20,40,0.75));
            border:1px solid rgba(34,211,238,0.15); backdrop-filter: blur(15px);">
    <div style="position:absolute; top:0; left:0; right:0; height:2px;
                background: linear-gradient(90deg, transparent, #22d3ee, #3b82f6, #10b981, transparent);"></div>
    <div style="display:flex; justify-content:center; align-items:center; gap:20px; flex-wrap:wrap;">
        <div style="font-size:2.8rem; filter: drop-shadow(0 0 15px rgba(34,211,238,0.5));">🏆</div>
        <div style="text-align:center;">
            <div style="font-size:1.5rem; font-weight:900; color:#22d3ee;
                        text-shadow:0 0 20px rgba(34,211,238,0.4);">
                Meesho ScriptedBy{Her} 2.0
            </div>
            <div style="font-size:1rem; font-weight:600; color:#94a3b8; margin-top:4px;">
                🌍 Worldwide Hackathon — Empowering Women Entrepreneurs with AI
            </div>
            <div style="display:flex; justify-content:center; gap:16px; margin-top:12px;">
                <span style="background:rgba(34,211,238,0.12); color:#22d3ee; padding:4px 14px;
                             border-radius:20px; font-size:0.8rem; font-weight:700;
                             border:1px solid rgba(34,211,238,0.2);">🤖 AI Agents</span>
                <span style="background:rgba(16,185,129,0.12); color:#4ade80; padding:4px 14px;
                             border-radius:20px; font-size:0.8rem; font-weight:700;
                             border:1px solid rgba(16,185,129,0.2);">📊 Analytics</span>
                <span style="background:rgba(59,130,246,0.12); color:#60a5fa; padding:4px 14px;
                             border-radius:20px; font-size:0.8rem; font-weight:700;
                             border:1px solid rgba(59,130,246,0.2);">🎙️ Voice AI</span>
                <span style="background:rgba(168,85,247,0.12); color:#c084fc; padding:4px 14px;
                             border-radius:20px; font-size:0.8rem; font-weight:700;
                             border:1px solid rgba(168,85,247,0.2);">💡 Smart Pricing</span>
            </div>
        </div>
        <div style="font-size:2.8rem; filter: drop-shadow(0 0 15px rgba(16,185,129,0.5));">🚀</div>
    </div>
    <div style="position:absolute; bottom:0; left:0; right:0; height:2px;
                background: linear-gradient(90deg, transparent, #10b981, #3b82f6, #22d3ee, transparent);"></div>
</div>
""", unsafe_allow_html=True)

# ===================== FEATURE CARDS (3D icons, no photos) =====================
st.markdown("<br>", unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)

with fc1:
    st.markdown("""
    <div class="feature-card">
        <span class="icon-3d">💬</span>
        <h3>AI-Powered Chat</h3>
        <p>Get product ideas, marketing tips & pricing advice from your personal AI coach.</p>
    </div>
    """, unsafe_allow_html=True)

with fc2:
    st.markdown("""
    <div class="feature-card">
        <span class="icon-3d">📊</span>
        <h3>Sales Analytics</h3>
        <p>Upload your data and discover trends, top products & profit insights instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with fc3:
    st.markdown("""
    <div class="feature-card">
        <span class="icon-3d">🎙️</span>
        <h3>Voice Coaching</h3>
        <p>Speak your questions in your language — get instant AI-powered business guidance.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat with Coach", "📊 Upload Sales Data", "🎙️ Voice Mode", "📈 Dashboard"])

# ===================== TAB 1: CHAT =====================
with tab1:
    with st.container():
        st.subheader("💬 Chat with Your AI Coach")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Namaste! I'm your Agentic Reseller Success Coach 🤖\n\nHow can I help you grow your Meesho business today? 🌸"}
            ]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Type your message here... (e.g., Suggest summer products)"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("🤖 Agents are working..."):
                    try:
                        from backend import create_crew
                        crew = create_crew(prompt)
                        result = crew.kickoff()
                        response = result.raw
                    except Exception:
                        time.sleep(0.8)
                        st.markdown(
                            '<div class="demo-banner">⚠️ Backend not connected — Running in Demo Mode (Responses are pre-built examples)</div>',
                            unsafe_allow_html=True
                        )
                        response = """**🔍 Market Research Agent:** Summer Kurtas, Cotton Sarees, and Short Kurtis are trending right now.

**✍️ Content Agent:**
1. 🌸 New Summer Collection! Beautiful Short Kurtis only ₹399. Perfect for daily wear! DM to order ❤️
2. Limited Stock! Stylish Cotton Sarees at best price. Free delivery on orders above ₹1000.

**💰 Pricing Agent:** Recommended price range: ₹399–₹499 for good profit margin."""

                st.markdown(response)

                # Show relevant product images based on query
                st.markdown("#### 🛒 Trending Products for You")
                render_product_images(prompt)

            st.session_state.messages.append({"role": "assistant", "content": response})

# ===================== TAB 2: UPLOAD SALES DATA =====================
with tab2:
    st.subheader("📊 Upload Past Sales Data")
    uploaded_file = st.file_uploader("Upload your Meesho sales file (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Parse the uploaded file
        try:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

            # Strip whitespace from column names
            df.columns = df.columns.str.strip()

            st.success(f"✅ Successfully loaded {len(df)} records!")
            st.dataframe(df, use_container_width=True)

            # ---------- Sales Insights ----------
            st.markdown("### 🔍 Sales Insights")
            col1, col2, col3, col4 = st.columns(4)

            # Ensure numeric columns
            for c in ["Quantity", "Selling_Price", "Cost_Price", "Profit"]:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")

            total_revenue = df["Selling_Price"].sum() if "Selling_Price" in df.columns else 0
            total_profit = df["Profit"].sum() if "Profit" in df.columns else 0
            total_orders = len(df)
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

            col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
            col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
            col3.metric("🛒 Total Orders", f"{total_orders}")
            col4.metric("🧾 Avg Order Value", f"₹{avg_order_value:,.0f}")

            # Category breakdown
            if "Category" in df.columns and "Profit" in df.columns:
                st.markdown("### 📦 Category-wise Performance")
                cat_group = df.groupby("Category").agg(
                    Total_Revenue=("Selling_Price", "sum"),
                    Total_Profit=("Profit", "sum"),
                    Orders=("Order_ID", "count")
                ).reset_index()

                cat_fig = px.bar(
                    cat_group, x="Category", y=["Total_Revenue", "Total_Profit"],
                    barmode="group", color_discrete_sequence=["#ff0080", "#40e0d0"],
                    title="Revenue vs Profit by Category"
                )
                cat_fig.update_layout(template="plotly_white", font=dict(color="#4a0072"))
                st.plotly_chart(cat_fig, use_container_width=True)

            # Top products
            if "Product_Name" in df.columns:
                st.markdown("### 🏆 Top Selling Products")
                top_products = df.groupby("Product_Name").agg(
                    Quantity_Sold=("Quantity", "sum"),
                    Total_Profit=("Profit", "sum")
                ).sort_values("Quantity_Sold", ascending=False).head(5).reset_index()
                st.dataframe(top_products, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    else:
        st.info("👆 Upload a CSV or Excel file to see sales insights.")

# ===================== TAB 3: VOICE MODE =====================
with tab3:
    st.subheader("🎙️ Voice Mode — Talk to Your Coach")
    st.markdown("Click the button below and speak your question. Your voice will be transcribed and sent to the AI Coach.")

    if st.button("🎤 Start Listening"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🔊 Listening... Please speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
                with st.spinner("🔄 Transcribing your voice..."):
                    try:
                        transcribed_text = recognizer.recognize_google(audio)
                        st.success(f"📝 You said: **{transcribed_text}**")
                    except sr.UnknownValueError:
                        st.error("😕 Could not understand the audio. Please try again.")
                        transcribed_text = None
                    except sr.RequestError:
                        st.error("⚠️ Speech recognition service unavailable. Using demo text.")
                        transcribed_text = "Suggest trending summer products for women"
            except sr.WaitTimeoutError:
                st.warning("⏰ No speech detected. Please try again.")
                transcribed_text = None

        if transcribed_text:
            st.markdown("---")
            st.markdown("### 🤖 Coach Response")
            with st.spinner("🤖 Agents are working on your voice query..."):
                try:
                    from backend import create_crew
                    crew = create_crew(transcribed_text)
                    result = crew.kickoff()
                    voice_response = result.raw
                except Exception:
                    time.sleep(0.8)
                    voice_response = (
                        "**Market Research Agent:** Based on current trends, Cotton Kurtis and Lightweight Sarees are hot sellers this season.\n\n"
                        "**Content Agent:**\n"
                        "1. 🌞 Beat the heat in style! Premium Cotton Kurtis starting at ₹299. Limited stock — order now!\n"
                        "2. ✨ Gorgeous Lightweight Sarees perfect for summer. Best prices guaranteed! DM to book ❤️\n\n"
                        "**Pricing Agent:** Sweet spot pricing: ₹299–₹599 for maximum conversions and healthy margins."
                    )
            st.markdown(voice_response)

# ===================== TAB 4: DASHBOARD =====================
with tab4:
    st.subheader("📈 Sales Dashboard")

    # Load sales data
    try:
        dash_df = pd.read_csv("sales_data.csv")
        dash_df.columns = dash_df.columns.str.strip()
        for c in ["Quantity", "Selling_Price", "Cost_Price", "Profit"]:
            if c in dash_df.columns:
                dash_df[c] = pd.to_numeric(dash_df[c], errors="coerce")
        dash_df["Date"] = pd.to_datetime(dash_df["Date"])

        # KPI Row
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("💰 Total Revenue", f"₹{dash_df['Selling_Price'].sum():,.0f}")
        k2.metric("📈 Total Profit", f"₹{dash_df['Profit'].sum():,.0f}")
        k3.metric("🛒 Total Orders", f"{len(dash_df)}")
        k4.metric("💵 Profit Margin",
                   f"{dash_df['Profit'].sum() / dash_df['Selling_Price'].sum() * 100:.1f}%")

        st.markdown("---")

        # Row 1: Sales Trend + Profit Trend
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### 📅 Daily Sales Trend")
            daily_sales = dash_df.groupby("Date")["Selling_Price"].sum().reset_index()
            fig_sales = px.line(
                daily_sales, x="Date", y="Selling_Price",
                markers=True, color_discrete_sequence=["#ff0080"],
                title="Daily Revenue Over Time"
            )
            fig_sales.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Revenue (₹)",
                                    font=dict(color="#4a0072"), plot_bgcolor="#fff5f9")
            st.plotly_chart(fig_sales, use_container_width=True)

        with col_right:
            st.markdown("#### 📈 Daily Profit Trend")
            daily_profit = dash_df.groupby("Date")["Profit"].sum().reset_index()
            fig_profit = px.line(
                daily_profit, x="Date", y="Profit",
                markers=True, color_discrete_sequence=["#40e0d0"],
                title="Daily Profit Over Time"
            )
            fig_profit.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Profit (₹)",
                                     font=dict(color="#4a0072"), plot_bgcolor="#f0fdfa")
            st.plotly_chart(fig_profit, use_container_width=True)

        # Row 2: Category Pie + Top Products Bar
        col_left2, col_right2 = st.columns(2)

        with col_left2:
            st.markdown("#### 🥧 Revenue Share by Category")
            cat_rev = dash_df.groupby("Category")["Selling_Price"].sum().reset_index()
            fig_pie = px.pie(
                cat_rev, values="Selling_Price", names="Category",
                color_discrete_sequence=["#ff0080", "#ff8c00", "#40e0d0", "#7e22ce", "#f857a6"],
                title="Category-wise Revenue Distribution"
            )
            fig_pie.update_traces(textinfo="percent+label", textfont_size=14)
            fig_pie.update_layout(font=dict(color="#4a0072"))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_right2:
            st.markdown("#### 🏆 Top Products by Profit")
            prod_profit = dash_df.groupby("Product_Name")["Profit"].sum().sort_values(ascending=True).reset_index()
            fig_bar = px.bar(
                prod_profit, x="Profit", y="Product_Name",
                orientation="h", color="Profit",
                color_continuous_scale=["#fbc2eb", "#ff0080", "#7e22ce"],
                title="Products Ranked by Total Profit"
            )
            fig_bar.update_layout(template="plotly_white", xaxis_title="Total Profit (₹)", yaxis_title="",
                                  font=dict(color="#4a0072"))
            st.plotly_chart(fig_bar, use_container_width=True)

        # Row 3: Quantity vs Profit scatter
        st.markdown("#### 🔢 Quantity Sold vs Profit per Order")
        fig_scatter = px.scatter(
            dash_df, x="Quantity", y="Profit", size="Selling_Price",
            color="Category", hover_name="Product_Name",
            title="Order Quantity vs Profit (bubble size = selling price)"
        )
        fig_scatter.update_layout(template="plotly_white", font=dict(color="#4a0072"),
                                  colorway=["#ff0080", "#ff8c00", "#40e0d0", "#7e22ce"])
        st.plotly_chart(fig_scatter, use_container_width=True)

    except FileNotFoundError:
        st.warning("⚠️ sales_data.csv not found. Please place the file in the project directory.")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

# Elegant divider
st.markdown("""
<div style="height:2px; border-radius:1px;
     background: linear-gradient(90deg, transparent, #22d3ee, #3b82f6, #10b981, transparent);
     margin: 10px 0 20px;
     box-shadow: 0 0 10px rgba(34,211,238,0.3);"></div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:20px; border-radius:16px;
     background: rgba(8,14,28,0.65);
     border: 1px solid rgba(34,211,238,0.12); margin-top:10px;
     backdrop-filter: blur(15px);">
    <div style="font-size:1.15rem; color:#22d3ee; font-weight:800; margin-bottom:4px;">
        🚀 Built for Worldwide Hackathon — Empowering Bharat's Women Entrepreneurs
    </div>
    <div style="font-size:0.85rem; color:#64748b; font-weight:600;">
        AI Agents · Voice Tech · Sales Analytics · Smart Pricing
    </div>
</div>
""", unsafe_allow_html=True)
