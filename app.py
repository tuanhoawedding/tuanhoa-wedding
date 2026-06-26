import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="TUANHOA WEDDING - Hệ Thống Quản Lý",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# LOAD LOGO — Cache để không đọc file mỗi lần re-run
# ============================================================
# LOGO SVG — Monogram TH vàng ánh kim (không cần file ngoài)
# ============================================================
LOGO_HTML = """
<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#E8D08A"/>
      <stop offset="40%"  stop-color="#C9A84C"/>
      <stop offset="100%" stop-color="#9A6F20"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <circle cx="40" cy="40" r="36" fill="none" stroke="url(#gold)" stroke-width="1.5" opacity="0.6"/>
  <circle cx="40" cy="40" r="30" fill="none" stroke="url(#gold)" stroke-width="0.5" opacity="0.35"/>
  <text x="21" y="53" font-family="Georgia,serif" font-size="34" font-weight="700"
        fill="url(#gold)" filter="url(#glow)">T</text>
  <text x="40" y="53" font-family="Georgia,serif" font-size="34" font-weight="700"
        fill="url(#gold)" filter="url(#glow)">H</text>
  <path d="M34,13 Q40,9 46,13" fill="none" stroke="url(#gold)" stroke-width="1.2" opacity="0.7"/>
  <path d="M34,67 Q40,71 46,67" fill="none" stroke="url(#gold)" stroke-width="1.2" opacity="0.7"/>
</svg>
"""

# ============================================================
# CSS TUANHOA WEDDING — Gold Luxury (cached)
# ============================================================
@st.cache_data
def get_css():
    return """
<style>
    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1C1A10 0%, #2A2618 55%, #3A3426 100%);
        border-right: 1px solid #C9A84C44;
    }
    [data-testid="stSidebar"] * { color: #FAF6EE !important; }

    /* ── Radio menu items ── */
    [data-testid="stSidebar"] .stRadio > div { gap: 2px; }
    [data-testid="stSidebar"] .stRadio label {
        background: transparent;
        border-radius: 8px;
        padding: 8px 12px !important;
        font-size: 0.88rem !important;
        transition: background 0.2s;
        color: #FAF6EE !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(201,168,76,0.15); }
    [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + div { border-color: #C9A84C !important; }

    /* ── Logout button ── */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #C9A84C, #E8D08A) !important;
        color: #1C1A10 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #E8D08A, #C9A84C) !important;
    }

    /* ── Main background ── */
    .stApp { background: #1C1A10; }
    .main .block-container { padding-top: 1.5rem; }

    /* ── Metric cards ── */
    .metric-card {
        background: linear-gradient(135deg, #2A2618 0%, #3A3426 100%);
        border: 1px solid #C9A84C55;
        padding: 22px 16px; border-radius: 12px; color: #FAF6EE;
        text-align: center; margin: 5px 0;
        box-shadow: 0 4px 16px rgba(201,168,76,0.12);
    }
    .metric-card h2 { font-size: 2.4rem; margin: 0; color: #C9A84C; font-weight: 800; }
    .metric-card p  { margin: 4px 0 0; opacity: 0.8; font-size: 0.88rem; color: #FAF6EE; }

    /* ── Section header ── */
    .section-header {
        background: linear-gradient(90deg, #C9A84C, #E8D08A, #C9A84C);
        color: #1C1A10; padding: 12px 22px; border-radius: 8px;
        margin-bottom: 20px; font-size: 1.05rem; font-weight: 700;
        letter-spacing: 0.03em;
    }

    /* ── DataFrames ── */
    .stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid #C9A84C33 !important; }

    /* ── Forms ── */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input,
    .stTextArea > div > textarea {
        background: #2A2618 !important;
        color: #FAF6EE !important;
        border: 1px solid #C9A84C55 !important;
        border-radius: 6px !important;
    }
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #C9A84C, #E8D08A) !important;
        color: #1C1A10 !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab"] {
        color: #C9A84C !important;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #C9A84C !important;
        color: #E8D08A !important;
    }

    /* ── General text ── */
    h1,h2,h3,h4,h5,h6,p,label,span,div { color: #FAF6EE; }
    .stMarkdown { color: #FAF6EE; }

    /* ── Login box ── */
    .login-box {
        background: linear-gradient(160deg, #2A2618, #1C1A10);
        border: 1px solid #C9A84C66;
        border-radius: 18px;
        padding: 36px 32px;
        box-shadow: 0 12px 48px rgba(201,168,76,0.18);
        text-align: center;
    }
    .gold-text { color: #C9A84C !important; }
    .gold-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #C9A84C, transparent);
        margin: 16px 0;
    }
</style>
"""
st.markdown(get_css(), unsafe_allow_html=True)

# ============================================================
# DỮ LIỆU NGƯỜI DÙNG & QUYỀN
# Tên đăng nhập chung: 0965758883 | Mật khẩu chung: Tun883@
# Phân biệt vai trò qua dropdown khi đăng nhập
# ============================================================
# ============================================================
# HỆ THỐNG TÀI KHOẢN — Mỗi phòng ban có user/pass riêng
# ============================================================
USERS = {
    # ── Ban Giám Đốc ──
    "0965758883": {
        "password": "Tun883@",
        "role":     "Admin",
        "name":     "Giám Đốc",
        "phong":    "Ban Giám Đốc",
    },
    # ── Lễ Tân ──
    "letan":  {
        "password": "letan123",
        "role":     "Lễ tân",
        "name":     "Nhân viên Lễ tân",
        "phong":    "Phòng Lễ tân",
    },
    # ── Kho ──
    "kho": {
        "password": "kho123",
        "role":     "Quản lý kho",
        "name":     "Nhân viên Kho",
        "phong":    "Phòng Kho",
    },
    # ── Makeup ──
    "makeup": {
        "password": "makeup123",
        "role":     "Makeup",
        "name":     "Chuyên viên Makeup",
        "phong":    "Phòng Makeup",
    },
    # ── Nhiếp Ảnh ──
    "photo": {
        "password": "photo123",
        "role":     "Nhiếp ảnh",
        "name":     "Nhiếp ảnh gia",
        "phong":    "Phòng Chụp ảnh",
    },
    # ── Design ──
    "design": {
        "password": "design123",
        "role":     "Design",
        "name":     "Chuyên viên Design",
        "phong":    "Phòng Design",
    },
}

ROLE_MENUS = {
    "Admin":       ["🏠 Tổng quan", "👥 Khách hàng & Tiến độ", "📅 Lịch làm việc", "👗 Kho váy cưới", "🥻 Kho áo dài", "👔 Kho Suit", "📦 Giao nhận đồ", "⚙️ Quản lý nhân sự"],
    "Lễ tân":      ["🏠 Tổng quan", "👥 Khách hàng & Tiến độ", "📅 Lịch làm việc", "📦 Giao nhận đồ"],
    "Quản lý kho": ["🏠 Tổng quan", "👗 Kho váy cưới", "🥻 Kho áo dài", "👔 Kho Suit", "📦 Giao nhận đồ"],
    "Makeup":      ["🏠 Tổng quan", "📅 Lịch làm việc"],
    "Nhiếp ảnh":   ["🏠 Tổng quan", "📅 Lịch làm việc"],
    "Design":      ["🏠 Tổng quan", "📅 Lịch làm việc"],
}

# Config hiển thị cho từng loại công việc
LOAI_CONFIG = {
    "Makeup": {
        "icon":    "💄",
        "color":   "#e91e8c",
        "bg":      "rgba(233,30,140,0.10)",
        "border":  "rgba(233,30,140,0.35)",
        "label":   "MAKE UP",
        "img":     "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=400&q=80",
    },
    "Chụp ảnh": {
        "icon":    "📷",
        "color":   "#3498db",
        "bg":      "rgba(52,152,219,0.10)",
        "border":  "rgba(52,152,219,0.35)",
        "label":   "PHOTO",
        "img":     "https://images.unsplash.com/photo-1554048612-b6a482bc67e5?w=400&q=80",
    },
    "Design": {
        "icon":    "🎨",
        "color":   "#9b59b6",
        "bg":      "rgba(155,89,182,0.10)",
        "border":  "rgba(155,89,182,0.35)",
        "label":   "DESIGN",
        "img":     "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400&q=80",
    },
}

ROLE_ICONS = {"Admin":"👑","Lễ tân":"🛎️","Quản lý kho":"📦","Makeup":"💄","Nhiếp ảnh":"📷","Design":"🎨"}

# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================
def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if "df_customers" not in st.session_state:
        st.session_state.df_customers = pd.DataFrame([
            {"Mã KH":"KH001","Tên khách":"Nguyễn Thị Mai","SĐT":"0901234567","Ngày chụp":"2025-08-10","Gói dịch vụ":"VIP",   "Trạng thái":"Chốt lịch",    "Ghi chú":""},
            {"Mã KH":"KH002","Tên khách":"Trần Văn Hùng", "SĐT":"0912345678","Ngày chụp":"2025-08-12","Gói dịch vụ":"Basic", "Trạng thái":"Đặt lịch",     "Ghi chú":"Yêu cầu 2 váy"},
            {"Mã KH":"KH003","Tên khách":"Lê Thị Hồng",   "SĐT":"0923456789","Ngày chụp":"2025-08-05","Gói dịch vụ":"Luxury","Trạng thái":"Đang thực hiện","Ghi chú":""},
            {"Mã KH":"KH004","Tên khách":"Phạm Minh Tuấn","SĐT":"0934567890","Ngày chụp":"2025-07-28","Gói dịch vụ":"VIP",   "Trạng thái":"Hoàn thành",   "Ghi chú":""},
        ])

    if "df_schedule" not in st.session_state:
        st.session_state.df_schedule = pd.DataFrame([
            {"Mã lịch":"LV001","Tên khách":"Lê Thị Hồng",   "Loại":"Makeup",   "Nhân viên":"Phạm Thị Hoa","Ngày":"2025-08-05","Giờ":"06:00","Trạng thái":"Hoàn thành","Ghi chú":""},
            {"Mã lịch":"LV002","Tên khách":"Lê Thị Hồng",   "Loại":"Chụp ảnh", "Nhân viên":"Đỗ Văn Ảnh", "Ngày":"2025-08-05","Giờ":"08:00","Trạng thái":"Hoàn thành","Ghi chú":""},
            {"Mã lịch":"LV003","Tên khách":"Nguyễn Thị Mai","Loại":"Makeup",   "Nhân viên":"Phạm Thị Hoa","Ngày":"2025-08-10","Giờ":"05:30","Trạng thái":"Chờ",       "Ghi chú":""},
            {"Mã lịch":"LV004","Tên khách":"Nguyễn Thị Mai","Loại":"Chụp ảnh", "Nhân viên":"Đỗ Văn Ảnh", "Ngày":"2025-08-10","Giờ":"07:30","Trạng thái":"Chờ",       "Ghi chú":""},
            {"Mã lịch":"LV005","Tên khách":"Trần Văn Hùng", "Loại":"Design",   "Nhân viên":"Nguyễn Thiết Kế","Ngày":"2025-08-12","Giờ":"09:00","Trạng thái":"Chờ",   "Ghi chú":"Album ảnh"},
        ])

    if "df_vay" not in st.session_state:
        st.session_state.df_vay = pd.DataFrame([
            {"Mã váy":"V001","Tên váy":"Váy trắng đuôi cá", "Phân loại":"VIP",   "Size":"S","Màu sắc":"Trắng","Đơn giá":3500000,"Trạng thái":"Sẵn sàng",     "Ghi chú":"","Ảnh URL":"https://images.unsplash.com/photo-1594552072238-b8a33785b6cd?w=400&q=80"},
            {"Mã váy":"V002","Tên váy":"Váy bồng công chúa","Phân loại":"Luxury","Size":"M","Màu sắc":"Trắng","Đơn giá":6000000,"Trạng thái":"Đang cho mượn","Ghi chú":"KH003","Ảnh URL":"https://images.unsplash.com/photo-1537633552985-df8429e8048b?w=400&q=80"},
            {"Mã váy":"V003","Tên váy":"Váy suông tối giản","Phân loại":"Basic", "Size":"L","Màu sắc":"Kem",  "Đơn giá":1800000,"Trạng thái":"Sẵn sàng",     "Ghi chú":"","Ảnh URL":"https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=400&q=80"},
            {"Mã váy":"V004","Tên váy":"Váy ren hoa nổi",   "Phân loại":"VIP",   "Size":"S","Màu sắc":"Trắng","Đơn giá":4200000,"Trạng thái":"Đang giặt là", "Ghi chú":"","Ảnh URL":"https://images.unsplash.com/photo-1519741497674-611481863552?w=400&q=80"},
            {"Mã váy":"V005","Tên váy":"Váy cúp ngực đơn",  "Phân loại":"Basic", "Size":"M","Màu sắc":"Trắng","Đơn giá":2000000,"Trạng thái":"Sẵn sàng",     "Ghi chú":"","Ảnh URL":"https://images.unsplash.com/photo-1591130222377-40c4df20f6fa?w=400&q=80"},
        ])

    if "df_aodai" not in st.session_state:
        st.session_state.df_aodai = pd.DataFrame([
            {"Mã áo":"AD001","Tên áo":"Áo dài đỏ cặp đôi",   "Loại":"Áo dài cặp dâu rể","Cấp độ":"VIP",   "Size":"S/M","Đơn giá":2500000,"Trạng thái":"Sẵn sàng",     "Ảnh URL":"https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=400&q=80"},
            {"Mã áo":"AD002","Tên áo":"Áo dài vàng bê lễ",   "Loại":"Áo dài bê lễ",     "Cấp độ":"Basic", "Size":"M",  "Đơn giá":800000, "Trạng thái":"Đang cho mượn","Ảnh URL":"https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=400&q=80"},
            {"Mã áo":"AD003","Tên áo":"Áo dài hồng bê lễ",   "Loại":"Áo dài bê lễ",     "Cấp độ":"Basic", "Size":"S",  "Đơn giá":800000, "Trạng thái":"Sẵn sàng",     "Ảnh URL":"https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=400&q=80"},
            {"Mã áo":"AD004","Tên áo":"Áo dài luxury cặp đôi","Loại":"Áo dài cặp dâu rể","Cấp độ":"Luxury","Size":"S/L","Đơn giá":4500000,"Trạng thái":"Sẵn sàng",     "Ảnh URL":"https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=400&q=80"},
        ])

    if "df_suit" not in st.session_state:
        st.session_state.df_suit = pd.DataFrame([
            {"Mã suit":"S001","Tên suit":"Suit đen classic", "Cấp độ":"VIP",   "Size":"M","Phụ kiện":"Nơ, Đồ cài",        "Đơn giá":2800000,"Trạng thái":"Sẵn sàng",     "Ảnh URL":"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"Mã suit":"S002","Tên suit":"Suit xanh navy",   "Cấp độ":"Basic", "Size":"L","Phụ kiện":"Caravat",            "Đơn giá":1500000,"Trạng thái":"Đang cho mượn","Ảnh URL":"https://images.unsplash.com/photo-1593032465175-481ac7f401a0?w=400&q=80"},
            {"Mã suit":"S003","Tên suit":"Suit trắng luxury","Cấp độ":"Luxury","Size":"M","Phụ kiện":"Nơ, Caravat, Đồ cài","Đơn giá":5000000,"Trạng thái":"Sẵn sàng",     "Ảnh URL":"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"Mã suit":"S004","Tên suit":"Suit xám basic",   "Cấp độ":"Basic", "Size":"S","Phụ kiện":"Nơ",                 "Đơn giá":1200000,"Trạng thái":"Đang giặt là", "Ảnh URL":"https://images.unsplash.com/photo-1593032465175-481ac7f401a0?w=400&q=80"},
        ])

    if "df_borrow" not in st.session_state:
        st.session_state.df_borrow = pd.DataFrame([
            {"Mã GN":"GN001","Tên khách":"Lê Thị Hồng",   "Mã trang phục":"V002", "Loại":"Váy cưới","Ngày mượn":"2025-08-05","Ngày hẹn trả":"2025-08-07","Trạng thái":"Đã giao"},
            {"Mã GN":"GN002","Tên khách":"Phạm Minh Tuấn","Mã trang phục":"S002", "Loại":"Suit",    "Ngày mượn":"2025-07-28","Ngày hẹn trả":"2025-07-30","Trạng thái":"Đã trả"},
            {"Mã GN":"GN003","Tên khách":"Lê Thị Hồng",   "Mã trang phục":"AD002","Loại":"Áo dài",  "Ngày mượn":"2025-08-05","Ngày hẹn trả":"2025-08-07","Trạng thái":"Đã giao"},
        ])

init_session()

# ============================================================
# TRANG ĐĂNG NHẬP
# ============================================================
def show_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        # Box viền
        st.markdown('''<div class="login-box">''', unsafe_allow_html=True)
        # Logo SVG
        st.markdown('''<div style="display:flex;justify-content:center;margin-bottom:12px;">''' + LOGO_HTML + '''</div>''', unsafe_allow_html=True)
        # Tên thương hiệu
        st.markdown('''
        <div class="gold-divider"></div>
        <h2 style="color:#C9A84C;margin:8px 0 2px;font-size:1.4rem;letter-spacing:0.08em;font-weight:800;text-align:center;">
            TUANHOA WEDDING
        </h2>
        <p style="color:#E8D08A;font-size:0.78rem;letter-spacing:0.15em;margin:0 0 4px;text-align:center;">
            PHOTO · MAKE UP · BRIDAL · ACADEMY
        </p>
        <div class="gold-divider"></div>
        <p style="color:#FAF6EE99;font-size:0.82rem;margin:10px 0 0;text-align:center;">Hệ thống quản lý nội bộ</p>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("login_form"):
            username  = st.text_input("👤 Tên đăng nhập", placeholder="Nhập username...")
            password  = st.text_input("🔑 Mật khẩu", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("✨ Đăng nhập", use_container_width=True)
            if submitted:
                if username in USERS and USERS[username]["password"] == password:
                    u = USERS[username]
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "username": username,
                        "role":     u["role"],
                        "name":     u["name"],
                        "phong":    u["phong"],
                    }
                    st.rerun()
                else:
                    st.error("❌ Sai tên đăng nhập hoặc mật khẩu!")

        st.markdown("""
        <div style="background:#2A2618;border:1px solid #C9A84C33;border-radius:8px;
                    padding:12px 16px;margin-top:10px;font-size:0.77rem;color:#FAF6EE99;">
            <div style="color:#C9A84C;font-weight:700;margin-bottom:6px;text-align:center;">
                📋 Tài khoản các phòng ban
            </div>
            <table style="width:100%;border-collapse:collapse;">
              <tr style="color:#E8D08A;font-size:0.72rem;">
                <td style="padding:2px 6px;">Username</td>
                <td style="padding:2px 6px;">Phòng ban</td>
                <td style="padding:2px 6px;">Quyền truy cập</td>
              </tr>
              <tr><td style="padding:2px 6px;color:#FAF6EE;">0965758883</td>
                  <td style="padding:2px 6px;color:#C9A84C;">Ban Giám Đốc</td>
                  <td style="padding:2px 6px;color:#FAF6EE88;">Toàn bộ hệ thống</td></tr>
              <tr><td style="padding:2px 6px;color:#FAF6EE;">letan</td>
                  <td style="padding:2px 6px;color:#C9A84C;">Phòng Lễ tân</td>
                  <td style="padding:2px 6px;color:#FAF6EE88;">Khách hàng, Lịch, Giao nhận</td></tr>
              <tr><td style="padding:2px 6px;color:#FAF6EE;">kho</td>
                  <td style="padding:2px 6px;color:#C9A84C;">Phòng Kho</td>
                  <td style="padding:2px 6px;color:#FAF6EE88;">3 kho + Giao nhận</td></tr>
              <tr><td style="padding:2px 6px;color:#FAF6EE;">makeup</td>
                  <td style="padding:2px 6px;color:#C9A84C;">Phòng Makeup</td>
                  <td style="padding:2px 6px;color:#FAF6EE88;">Lịch của mình</td></tr>
              <tr><td style="padding:2px 6px;color:#FAF6EE;">photo</td>
                  <td style="padding:2px 6px;color:#C9A84C;">Phòng Chụp ảnh</td>
                  <td style="padding:2px 6px;color:#FAF6EE88;">Lịch của mình</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
def show_sidebar():
    user = st.session_state.user
    icon = ROLE_ICONS.get(user["role"], "👤")

    # Logo + brand name — render SVG terpisah tránh lỗi f-string
    st.sidebar.markdown(
        '<div style="text-align:center;padding:18px 0 4px;">' +
        '<div style="display:flex;justify-content:center;margin-bottom:6px;">' +
        LOGO_HTML +
        '</div>' +
        '<div style="height:1px;background:linear-gradient(90deg,transparent,#C9A84C,transparent);margin:4px 0 6px;"></div>' +
        '<div style="font-size:0.95rem;font-weight:800;color:#C9A84C;letter-spacing:0.1em;">TUANHOA WEDDING</div>' +
        '<div style="font-size:0.62rem;color:#E8D08A;letter-spacing:0.12em;margin-top:2px;">PHOTO · MAKE UP · BRIDAL · ACADEMY</div>' +
        '</div>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        f'''<div style="background:rgba(201,168,76,0.1);border:1px solid #C9A84C44;border-radius:10px;
                padding:10px;margin:8px 0 14px;text-align:center;">
            <div style="font-size:1.3rem;">{icon}</div>
            <div style="font-weight:700;font-size:0.88rem;color:#FAF6EE;">{user["name"]}</div>
            <div style="font-size:0.72rem;color:#C9A84C;margin-top:2px;">{user["phong"]}</div>
        </div>''',
        unsafe_allow_html=True
    )
    menus = ROLE_MENUS.get(user["role"], [])
    selected = st.sidebar.radio("Menu", menus, label_visibility="collapsed")

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.sidebar.markdown(f"""
    <div style="text-align:center;margin-top:20px;padding-top:12px;
                border-top:1px solid #C9A84C33;font-size:0.68rem;color:#C9A84C88;">
        0963 758 883 · 0965 758 883<br>
        <span style="color:#FAF6EE55;">Phố Cát – Vân Du – Thanh Hoá</span>
    </div>
    """, unsafe_allow_html=True)

    return selected

# ============================================================
# TRANG: TỔNG QUAN
# ============================================================
def page_dashboard():
    st.markdown('<div class="section-header">🏠 Tổng quan hệ thống — TUANHOA WEDDING</div>', unsafe_allow_html=True)
    df_c = st.session_state.df_customers
    df_b = st.session_state.df_borrow

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><h2>{len(df_c)}</h2><p>Tổng khách hàng</p></div>', unsafe_allow_html=True)
    with c2:
        dang_lam = len(df_c[df_c["Trạng thái"]=="Đang thực hiện"])
        st.markdown(f'<div class="metric-card"><h2>{dang_lam}</h2><p>Đang thực hiện</p></div>', unsafe_allow_html=True)
    with c3:
        cho_tra = len(df_b[df_b["Trạng thái"]=="Đã giao"])
        st.markdown(f'<div class="metric-card"><h2>{cho_tra}</h2><p>Đồ chưa hoàn trả</p></div>', unsafe_allow_html=True)
    with c4:
        vay_san = len(st.session_state.df_vay[st.session_state.df_vay["Trạng thái"]=="Sẵn sàng"])
        st.markdown(f'<div class="metric-card"><h2>{vay_san}</h2><p>Váy cưới sẵn sàng</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("**📊 Trạng thái khách hàng**")
        sc = df_c["Trạng thái"].value_counts().reset_index()
        sc.columns = ["Trạng thái","Số lượng"]
        st.dataframe(sc, use_container_width=True, hide_index=True)
    with col_r:
        st.markdown("**📦 Tình trạng trang phục**")
        all_items = pd.concat([
            st.session_state.df_vay[["Trạng thái"]],
            st.session_state.df_aodai[["Trạng thái"]],
            st.session_state.df_suit[["Trạng thái"]],
        ])
        ic = all_items["Trạng thái"].value_counts().reset_index()
        ic.columns = ["Trạng thái","Số lượng"]
        st.dataframe(ic, use_container_width=True, hide_index=True)

# ============================================================
# TRANG: KHÁCH HÀNG
# ============================================================
def page_customers():
    st.markdown('<div class="section-header">👥 Quản lý Khách hàng & Tiến độ</div>', unsafe_allow_html=True)
    df = st.session_state.df_customers
    tab1, tab2 = st.tabs(["📋 Danh sách", "➕ Thêm / Cập nhật"])

    with tab1:
        sf = st.selectbox("Lọc trạng thái", ["Tất cả","Đặt lịch","Chốt lịch","Đang thực hiện","Hoàn thành"])
        df_show = df if sf=="Tất cả" else df[df["Trạng thái"]==sf]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**➕ Thêm khách hàng mới**")
            with st.form("form_add_customer"):
                ma_kh  = st.text_input("Mã KH", value=f"KH{len(df)+1:03d}")
                ten_kh = st.text_input("Tên khách *")
                sdt    = st.text_input("Số điện thoại")
                ngay   = st.date_input("Ngày chụp", min_value=date.today())
                goi    = st.selectbox("Gói dịch vụ", ["Basic","VIP","Luxury"])
                tt     = st.selectbox("Trạng thái", ["Đặt lịch","Chốt lịch"])
                gc     = st.text_area("Ghi chú", height=70)
                if st.form_submit_button("✅ Thêm khách", use_container_width=True):
                    if ten_kh:
                        new_row = {"Mã KH":ma_kh,"Tên khách":ten_kh,"SĐT":sdt,
                                   "Ngày chụp":str(ngay),"Gói dịch vụ":goi,"Trạng thái":tt,"Ghi chú":gc}
                        st.session_state.df_customers = pd.concat(
                            [st.session_state.df_customers, pd.DataFrame([new_row])], ignore_index=True)
                        st.success(f"✅ Đã thêm khách {ten_kh}"); st.rerun()
                    else:
                        st.error("Vui lòng nhập tên khách!")
        with c2:
            st.markdown("**🔄 Cập nhật trạng thái**")
            with st.form("form_update_customer"):
                ma_list = st.session_state.df_customers["Mã KH"].tolist()
                chon    = st.selectbox("Chọn Mã KH", ma_list)
                row     = st.session_state.df_customers[st.session_state.df_customers["Mã KH"]==chon].iloc[0]
                st.info(f"**{row['Tên khách']}** | Hiện: {row['Trạng thái']}")
                new_tt  = st.selectbox("Trạng thái mới",
                    ["Đặt lịch","Chốt lịch","Đang thực hiện","Hoàn thành"],
                    index=["Đặt lịch","Chốt lịch","Đang thực hiện","Hoàn thành"].index(row["Trạng thái"]))
                new_gc  = st.text_area("Ghi chú", value=row["Ghi chú"], height=70)
                if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                    mask = st.session_state.df_customers["Mã KH"]==chon
                    st.session_state.df_customers.loc[mask,"Trạng thái"] = new_tt
                    st.session_state.df_customers.loc[mask,"Ghi chú"]    = new_gc
                    st.success("✅ Đã cập nhật!"); st.rerun()

# ============================================================
# TRANG: LỊCH LÀM VIỆC
# ============================================================
def page_schedule():
    st.markdown('<div class="section-header">📅 Lịch làm việc & Giao việc</div>', unsafe_allow_html=True)
    df   = st.session_state.df_schedule
    user = st.session_state.user

    tab1, tab2 = st.tabs(["🗓️ Lịch theo phòng ban", "➕ Giao việc mới"])

    with tab1:
        # ── Thống kê nhanh ────────────────────────────────────
        tong_lich  = len(df)
        cho_lam    = len(df[df["Trạng thái"] == "Chờ"])
        hoan_thanh = len(df[df["Trạng thái"] == "Hoàn thành"])
        c1,c2,c3   = st.columns(3)
        with c1: st.markdown(f'''<div class="metric-card"><h2>{tong_lich}</h2><p>Tổng lịch</p></div>''', unsafe_allow_html=True)
        with c2: st.markdown(f'''<div class="metric-card"><h2 style="color:#e67e22;">{cho_lam}</h2><p>Đang chờ thực hiện</p></div>''', unsafe_allow_html=True)
        with c3: st.markdown(f'''<div class="metric-card"><h2 style="color:#27ae60;">{hoan_thanh}</h2><p>Hoàn thành</p></div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Lọc theo role ─────────────────────────────────────
        if user["role"] == "Makeup":
            df_filter = df[df["Loại"] == "Makeup"].copy()
            st.info("💄 Hiển thị lịch Makeup của bạn")
        elif user["role"] == "Nhiếp ảnh":
            df_filter = df[df["Loại"] == "Chụp ảnh"].copy()
            st.info("📷 Hiển thị lịch Chụp ảnh của bạn")
        elif user["role"] == "Design":
            df_filter = df[df["Loại"] == "Design"].copy()
            st.info("🎨 Hiển thị lịch Design của bạn")
        else:
            c1, c2, c3 = st.columns(3)
            with c1: lf = st.selectbox("Loại", ["Tất cả","Makeup","Chụp ảnh","Design"])
            with c2: tf = st.selectbox("Trạng thái", ["Tất cả","Chờ","Hoàn thành","Hủy"])
            with c3: ngay_f = st.date_input("Lọc ngày (bỏ qua nếu không cần)", value=None)
            df_filter = df.copy()
            if lf != "Tất cả": df_filter = df_filter[df_filter["Loại"] == lf]
            if tf != "Tất cả": df_filter = df_filter[df_filter["Trạng thái"] == tf]
            if ngay_f:
                df_filter = df_filter[df_filter["Ngày"] == str(ngay_f)]

        # ── Render theo nhóm phòng ban ─────────────────────────
        for loai_name, cfg in LOAI_CONFIG.items():
            df_loai = df_filter[df_filter["Loại"] == loai_name]
            if df_loai.empty:
                continue

            # Header nhóm
            st.markdown(f'''
            <div style="display:flex;align-items:center;gap:10px;margin:20px 0 12px;
                        padding:10px 16px;background:{cfg["bg"]};
                        border-left:4px solid {cfg["color"]};border-radius:0 8px 8px 0;">
                <span style="font-size:1.4rem;">{cfg["icon"]}</span>
                <div>
                    <div style="color:{cfg["color"]};font-weight:800;font-size:0.95rem;letter-spacing:0.08em;">{cfg["label"]}</div>
                    <div style="color:#FAF6EE88;font-size:0.75rem;">{len(df_loai)} lịch</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            items  = df_loai.to_dict("records")
            n_cols = 3
            rows   = [items[i:i+n_cols] for i in range(0, len(items), n_cols)]

            for row in rows:
                cols = st.columns(n_cols)
                for ci, item in enumerate(row):
                    with cols[ci]:
                        tt       = item.get("Trạng thái","")
                        ma_lv    = item.get("Mã lịch","")
                        ten_kh   = item.get("Tên khách","")
                        nhan_vien= item.get("Nhân viên","")
                        ngay     = item.get("Ngày","")
                        gio      = item.get("Giờ","")
                        ghi_chu  = item.get("Ghi chú","")

                        # Màu trạng thái
                        if tt == "Hoàn thành":
                            tc, tb = "#27ae60", "rgba(39,174,96,0.12)"
                            ticon  = "✅"
                        elif tt == "Hủy":
                            tc, tb = "#e74c3c", "rgba(231,76,60,0.12)"
                            ticon  = "❌"
                        else:
                            tc, tb = "#e67e22", "rgba(230,126,34,0.12)"
                            ticon  = "🕐"

                        # Cảnh báo hôm nay
                        today_badge = ""
                        try:
                            from datetime import date as _d
                            if ngay == str(_d.today()) and tt == "Chờ":
                                today_badge = f'''<div style="background:{cfg["color"]}22;color:{cfg["color"]};
                                    font-size:0.65rem;font-weight:800;padding:3px 8px;
                                    text-align:center;letter-spacing:0.05em;">⚡ HÔM NAY</div>'''
                        except: pass

                        gc_html = f'''<div style="font-size:0.72rem;color:#FAF6EE66;margin-top:4px;
                                        font-style:italic;">📝 {ghi_chu}</div>''' if ghi_chu else ""

                        st.markdown(f'''
                        <div style="background:#2A2618;
                                    border:1px solid {cfg["border"]};
                                    border-top:3px solid {cfg["color"]};
                                    border-radius:10px;overflow:hidden;
                                    margin-bottom:12px;
                                    box-shadow:0 2px 12px rgba(0,0,0,0.2);">
                            <div style="position:relative;height:110px;overflow:hidden;">
                                <img src="{cfg["img"]}" style="width:100%;height:110px;object-fit:cover;opacity:0.45;"
                                     onerror="this.style.display='none'">
                                <div style="position:absolute;inset:0;padding:10px 12px;
                                            background:linear-gradient(to bottom,transparent,#2A2618 85%);">
                                    <div style="position:absolute;top:8px;right:8px;
                                                background:{tb};color:{cfg["color"]};
                                                font-size:1.6rem;width:36px;height:36px;
                                                border-radius:50%;display:flex;align-items:center;
                                                justify-content:center;border:1px solid {cfg["border"]};">
                                        {cfg["icon"]}
                                    </div>
                                    <div style="position:absolute;top:8px;left:10px;
                                                background:rgba(0,0,0,0.55);
                                                color:{cfg["color"]};font-size:0.65rem;
                                                font-weight:800;padding:2px 8px;
                                                border-radius:10px;letter-spacing:0.06em;">
                                        {cfg["label"]}
                                    </div>
                                </div>
                            </div>
                            {today_badge}
                            <div style="padding:10px 12px 12px;">
                                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                                    <span style="color:#C9A84C;font-size:0.72rem;font-weight:600;">{ma_lv}</span>
                                    <span style="background:{tb};color:{tc};font-size:0.65rem;
                                                 font-weight:700;padding:2px 8px;border-radius:10px;">
                                        {ticon} {tt}
                                    </span>
                                </div>
                                <div style="font-size:1rem;color:#FAF6EE;font-weight:700;margin-bottom:2px;">
                                    👤 {ten_kh}
                                </div>
                                <div style="font-size:0.78rem;color:#E8D08A;margin-bottom:8px;">
                                    🧑‍💼 {nhan_vien}
                                </div>
                                <div style="height:1px;background:#C9A84C22;margin:6px 0;"></div>
                                <div style="display:flex;justify-content:space-between;font-size:0.78rem;">
                                    <span style="color:#FAF6EE;">📅 {ngay}</span>
                                    <span style="color:{cfg["color"]};font-weight:700;">⏰ {gio}</span>
                                </div>
                                {gc_html}
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

    with tab2:
        if user["role"] in ["Admin", "Lễ tân"]:
            customers = st.session_state.df_customers["Tên khách"].tolist()

            # Hiển thị lịch hôm nay nhanh
            from datetime import date as _today_date
            today_str = str(_today_date.today())
            df_today  = df[df["Ngày"] == today_str]
            if not df_today.empty:
                st.markdown(f"**⚡ Hôm nay có {len(df_today)} lịch:**")
                st.dataframe(df_today[["Mã lịch","Tên khách","Loại","Nhân viên","Giờ","Trạng thái"]],
                             use_container_width=True, hide_index=True)
                st.markdown("---")

            st.markdown("**➕ Giao việc mới**")
            with st.form("form_add_schedule"):
                c1, c2 = st.columns(2)
                with c1:
                    ten_kh    = st.selectbox("👤 Tên khách", customers)
                    loai      = st.selectbox("🗂️ Loại công việc", ["Makeup","Chụp ảnh","Design"])
                    nhan_vien = st.text_input("🧑‍💼 Nhân viên thực hiện")
                with c2:
                    ngay_lv = st.date_input("📅 Ngày làm việc", min_value=date.today())
                    gio_lv  = st.time_input("⏰ Giờ bắt đầu", value=datetime.strptime("07:00","%H:%M").time())
                    ghi_chu = st.text_input("📝 Ghi chú", placeholder="Yêu cầu đặc biệt...")
                ma_lv = f"LV{len(st.session_state.df_schedule)+1:03d}"
                if st.form_submit_button("📅 Giao việc", use_container_width=True):
                    if nhan_vien and ten_kh:
                        new_row = {
                            "Mã lịch":   ma_lv,
                            "Tên khách": ten_kh,
                            "Loại":      loai,
                            "Nhân viên": nhan_vien,
                            "Ngày":      str(ngay_lv),
                            "Giờ":       gio_lv.strftime("%H:%M"),
                            "Trạng thái":"Chờ",
                            "Ghi chú":   ghi_chu,
                        }
                        st.session_state.df_schedule = pd.concat(
                            [st.session_state.df_schedule, pd.DataFrame([new_row])], ignore_index=True)
                        cfg_l = LOAI_CONFIG.get(loai,{})
                        st.success(f"{cfg_l.get('icon','📅')} Đã giao việc **{loai}** cho **{nhan_vien}** — khách **{ten_kh}** ngày {ngay_lv}")
                        st.rerun()
                    else:
                        st.error("Vui lòng điền đầy đủ tên khách và nhân viên!")

            # Cập nhật trạng thái lịch
            st.markdown("---")
            st.markdown("**🔄 Cập nhật trạng thái lịch**")
            ma_list = st.session_state.df_schedule["Mã lịch"].tolist()
            with st.form("form_update_schedule"):
                chon_ma = st.selectbox("Chọn mã lịch", ma_list)
                row_lv  = st.session_state.df_schedule[st.session_state.df_schedule["Mã lịch"]==chon_ma].iloc[0]
                st.info(f"**{row_lv['Tên khách']}** | {row_lv['Loại']} | {row_lv['Ngày']} {row_lv['Giờ']} | Nhân viên: {row_lv['Nhân viên']}")
                new_tt = st.selectbox("Trạng thái mới", ["Chờ","Hoàn thành","Hủy"],
                    index=["Chờ","Hoàn thành","Hủy"].index(row_lv["Trạng thái"]) if row_lv["Trạng thái"] in ["Chờ","Hoàn thành","Hủy"] else 0)
                if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                    st.session_state.df_schedule.loc[
                        st.session_state.df_schedule["Mã lịch"]==chon_ma, "Trạng thái"] = new_tt
                    st.success("✅ Đã cập nhật!"); st.rerun()
        else:
            st.info("⚠️ Chức năng giao việc chỉ dành cho Admin hoặc Lễ tân.")

# ============================================================
# TRANG: KHO VÁY CƯỚI
# ============================================================
def page_vay():
    st.markdown('<div class="section-header">👗 Kho Váy Cưới</div>', unsafe_allow_html=True)
    df = st.session_state.df_vay

    tab1, tab2, tab3 = st.tabs(["🖼️ Dạng thẻ card", "📋 Danh sách bảng", "➕ Thêm / Cập nhật"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1: pl  = st.selectbox("Phân loại", ["Tất cả","Basic","VIP","Luxury"], key="vay_pl_card")
        with c2: ttf = st.selectbox("Trạng thái", ["Tất cả","Sẵn sàng","Đang cho mượn","Đang giặt là"], key="vay_tt_card")
        df_show = df.copy()
        if pl  != "Tất cả": df_show = df_show[df_show["Phân loại"] == pl]
        if ttf != "Tất cả": df_show = df_show[df_show["Trạng thái"] == ttf]
        st.markdown(f"**{len(df_show)} váy** phù hợp bộ lọc")
        render_cards(df_show, "Mã váy", "Tên váy", "Phân loại")

    with tab2:
        c1, c2 = st.columns(2)
        with c1: pl2  = st.selectbox("Phân loại", ["Tất cả","Basic","VIP","Luxury"], key="vay_pl_tbl")
        with c2: ttf2 = st.selectbox("Trạng thái", ["Tất cả","Sẵn sàng","Đang cho mượn","Đang giặt là"], key="vay_tt_tbl")
        df_show2 = df.copy()
        if pl2  != "Tất cả": df_show2 = df_show2[df_show2["Phân loại"] == pl2]
        if ttf2 != "Tất cả": df_show2 = df_show2[df_show2["Trạng thái"] == ttf2]
        show_cols = ["Mã váy","Tên váy","Phân loại","Size","Màu sắc","Đơn giá","Trạng thái","Ghi chú"]
        st.dataframe(df_show2[show_cols], use_container_width=True, hide_index=True)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Sẵn sàng",      len(df[df["Trạng thái"]=="Sẵn sàng"]))
        with c2: st.metric("Đang cho mượn", len(df[df["Trạng thái"]=="Đang cho mượn"]))
        with c3: st.metric("Đang giặt là",  len(df[df["Trạng thái"]=="Đang giặt là"]))

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**➕ Thêm váy mới**")
            with st.form("form_add_vay"):
                ma_vay  = st.text_input("Mã váy", value=f"V{len(df)+1:03d}")
                ten_vay = st.text_input("Tên váy *")
                pl_add  = st.selectbox("Phân loại", ["Basic","VIP","Luxury"])
                size    = st.selectbox("Size", ["XS","S","M","L","XL","XXL"])
                mau_sac = st.text_input("Màu sắc", value="Trắng")
                gia     = st.number_input("Đơn giá (đồng)", min_value=0, step=100000, value=2000000)
                anh_url = st.text_input("URL ảnh (tuỳ chọn)", placeholder="https://...")
                gc      = st.text_input("Ghi chú")
                if st.form_submit_button("✅ Thêm váy", use_container_width=True):
                    if ten_vay:
                        new_row = {"Mã váy":ma_vay,"Tên váy":ten_vay,"Phân loại":pl_add,
                                   "Size":size,"Màu sắc":mau_sac,"Đơn giá":gia,
                                   "Trạng thái":"Sẵn sàng","Ghi chú":gc,"Ảnh URL":anh_url}
                        st.session_state.df_vay = pd.concat(
                            [st.session_state.df_vay, pd.DataFrame([new_row])], ignore_index=True)
                        st.success("✅ Đã thêm váy mới!"); st.rerun()
        with c2:
            st.markdown("**🔄 Cập nhật trạng thái & giá**")
            with st.form("form_update_vay"):
                ma_list = st.session_state.df_vay["Mã váy"].tolist()
                chon    = st.selectbox("Chọn Mã váy", ma_list)
                row     = st.session_state.df_vay[st.session_state.df_vay["Mã váy"]==chon].iloc[0]
                st.info(f"**{row['Tên váy']}** | {row['Phân loại']} | Hiện: {row['Trạng thái']}")
                new_tt  = st.selectbox("Trạng thái mới", ["Sẵn sàng","Đang cho mượn","Đang giặt là"])
                new_gia = st.number_input("Đơn giá", min_value=0, step=100000, value=int(row.get("Đơn giá",0)))
                new_anh = st.text_input("URL ảnh", value=str(row.get("Ảnh URL","")))
                new_gc  = st.text_input("Ghi chú", value=str(row.get("Ghi chú","")))
                if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                    mask = st.session_state.df_vay["Mã váy"] == chon
                    st.session_state.df_vay.loc[mask, "Trạng thái"] = new_tt
                    st.session_state.df_vay.loc[mask, "Đơn giá"]    = new_gia
                    st.session_state.df_vay.loc[mask, "Ảnh URL"]    = new_anh
                    st.session_state.df_vay.loc[mask, "Ghi chú"]    = new_gc
                    st.success("✅ Đã cập nhật!"); st.rerun()

# ============================================================
# TRANG: KHO ÁO DÀI
# ============================================================
def page_aodai():
    st.markdown('<div class="section-header">🥻 Kho Áo Dài</div>', unsafe_allow_html=True)
    df = st.session_state.df_aodai

    tab1, tab2, tab3 = st.tabs(["🖼️ Dạng thẻ card", "📋 Danh sách bảng", "➕ Thêm / Cập nhật"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1: lf  = st.selectbox("Loại", ["Tất cả","Áo dài cặp dâu rể","Áo dài bê lễ"], key="ad_l_card")
        with c2: cf  = st.selectbox("Cấp độ", ["Tất cả","Basic","VIP","Luxury"], key="ad_c_card")
        df_show = df.copy()
        if lf != "Tất cả": df_show = df_show[df_show["Loại"]   == lf]
        if cf != "Tất cả": df_show = df_show[df_show["Cấp độ"] == cf]
        st.markdown(f"**{len(df_show)} áo dài** phù hợp bộ lọc")
        render_cards(df_show, "Mã áo", "Tên áo", "Cấp độ")

    with tab2:
        c1, c2 = st.columns(2)
        with c1: lf2 = st.selectbox("Loại", ["Tất cả","Áo dài cặp dâu rể","Áo dài bê lễ"], key="ad_l_tbl")
        with c2: cf2 = st.selectbox("Cấp độ", ["Tất cả","Basic","VIP","Luxury"], key="ad_c_tbl")
        df_show2 = df.copy()
        if lf2 != "Tất cả": df_show2 = df_show2[df_show2["Loại"]   == lf2]
        if cf2 != "Tất cả": df_show2 = df_show2[df_show2["Cấp độ"] == cf2]
        show_cols = ["Mã áo","Tên áo","Loại","Cấp độ","Size","Đơn giá","Trạng thái"]
        st.dataframe(df_show2[show_cols], use_container_width=True, hide_index=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**➕ Thêm áo dài mới**")
            with st.form("form_add_aodai"):
                ma_ao    = st.text_input("Mã áo", value=f"AD{len(df)+1:03d}")
                ten_ao   = st.text_input("Tên áo *")
                loai_add = st.selectbox("Loại", ["Áo dài cặp dâu rể","Áo dài bê lễ"])
                cap_do   = st.selectbox("Cấp độ", ["Basic","VIP","Luxury"])
                size     = st.text_input("Size", value="M")
                gia      = st.number_input("Đơn giá (đồng)", min_value=0, step=100000, value=1000000)
                anh_url  = st.text_input("URL ảnh (tuỳ chọn)", placeholder="https://...")
                if st.form_submit_button("✅ Thêm", use_container_width=True):
                    if ten_ao:
                        new_row = {"Mã áo":ma_ao,"Tên áo":ten_ao,"Loại":loai_add,
                                   "Cấp độ":cap_do,"Size":size,"Đơn giá":gia,
                                   "Trạng thái":"Sẵn sàng","Ảnh URL":anh_url}
                        st.session_state.df_aodai = pd.concat(
                            [st.session_state.df_aodai, pd.DataFrame([new_row])], ignore_index=True)
                        st.success("✅ Đã thêm!"); st.rerun()
        with c2:
            st.markdown("**🔄 Cập nhật trạng thái & giá**")
            with st.form("form_update_aodai"):
                ma_list = st.session_state.df_aodai["Mã áo"].tolist()
                chon    = st.selectbox("Chọn Mã áo", ma_list)
                row     = st.session_state.df_aodai[st.session_state.df_aodai["Mã áo"]==chon].iloc[0]
                st.info(f"**{row['Tên áo']}** | {row['Loại']} | Hiện: {row['Trạng thái']}")
                new_tt  = st.selectbox("Trạng thái mới", ["Sẵn sàng","Đang cho mượn","Đang giặt là"])
                new_gia = st.number_input("Đơn giá", min_value=0, step=100000, value=int(row.get("Đơn giá",0)))
                new_anh = st.text_input("URL ảnh", value=str(row.get("Ảnh URL","")))
                if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                    mask = st.session_state.df_aodai["Mã áo"] == chon
                    st.session_state.df_aodai.loc[mask, "Trạng thái"] = new_tt
                    st.session_state.df_aodai.loc[mask, "Đơn giá"]    = new_gia
                    st.session_state.df_aodai.loc[mask, "Ảnh URL"]    = new_anh
                    st.success("✅ Đã cập nhật!"); st.rerun()

# ============================================================
# TRANG: KHO SUIT
# ============================================================
def page_suit():
    st.markdown('<div class="section-header">👔 Kho Suit</div>', unsafe_allow_html=True)
    df = st.session_state.df_suit

    tab1, tab2, tab3 = st.tabs(["🖼️ Dạng thẻ card", "📋 Danh sách bảng", "➕ Thêm / Cập nhật"])

    with tab1:
        cf = st.selectbox("Cấp độ", ["Tất cả","Basic","VIP","Luxury"], key="suit_c_card")
        df_show = df if cf == "Tất cả" else df[df["Cấp độ"] == cf]
        st.markdown(f"**{len(df_show)} suit** phù hợp bộ lọc")
        render_cards(df_show, "Mã suit", "Tên suit", "Cấp độ")

    with tab2:
        cf2 = st.selectbox("Cấp độ", ["Tất cả","Basic","VIP","Luxury"], key="suit_c_tbl")
        df_show2 = df if cf2 == "Tất cả" else df[df["Cấp độ"] == cf2]
        show_cols = ["Mã suit","Tên suit","Cấp độ","Size","Phụ kiện","Đơn giá","Trạng thái"]
        st.dataframe(df_show2[show_cols], use_container_width=True, hide_index=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**➕ Thêm Suit mới**")
            with st.form("form_add_suit"):
                ma_suit  = st.text_input("Mã Suit", value=f"S{len(df)+1:03d}")
                ten_suit = st.text_input("Tên Suit *")
                cap_do   = st.selectbox("Cấp độ", ["Basic","VIP","Luxury"])
                size     = st.selectbox("Size", ["XS","S","M","L","XL"])
                phu_kien = st.multiselect("Phụ kiện", ["Nơ","Caravat","Đồ cài"])
                gia      = st.number_input("Đơn giá (đồng)", min_value=0, step=100000, value=2000000)
                anh_url  = st.text_input("URL ảnh (tuỳ chọn)", placeholder="https://...")
                if st.form_submit_button("✅ Thêm", use_container_width=True):
                    if ten_suit:
                        new_row = {"Mã suit":ma_suit,"Tên suit":ten_suit,"Cấp độ":cap_do,
                                   "Size":size,"Phụ kiện":", ".join(phu_kien),"Đơn giá":gia,
                                   "Trạng thái":"Sẵn sàng","Ảnh URL":anh_url}
                        st.session_state.df_suit = pd.concat(
                            [st.session_state.df_suit, pd.DataFrame([new_row])], ignore_index=True)
                        st.success("✅ Đã thêm!"); st.rerun()
        with c2:
            st.markdown("**🔄 Cập nhật trạng thái & giá**")
            with st.form("form_update_suit"):
                ma_list = st.session_state.df_suit["Mã suit"].tolist()
                chon    = st.selectbox("Chọn Mã Suit", ma_list)
                row     = st.session_state.df_suit[st.session_state.df_suit["Mã suit"]==chon].iloc[0]
                st.info(f"**{row['Tên suit']}** | {row['Cấp độ']} | Hiện: {row['Trạng thái']}")
                new_tt  = st.selectbox("Trạng thái mới", ["Sẵn sàng","Đang cho mượn","Đang giặt là"])
                new_gia = st.number_input("Đơn giá", min_value=0, step=100000, value=int(row.get("Đơn giá",0)))
                new_anh = st.text_input("URL ảnh", value=str(row.get("Ảnh URL","")))
                if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                    mask = st.session_state.df_suit["Mã suit"] == chon
                    st.session_state.df_suit.loc[mask, "Trạng thái"] = new_tt
                    st.session_state.df_suit.loc[mask, "Đơn giá"]    = new_gia
                    st.session_state.df_suit.loc[mask, "Ảnh URL"]    = new_anh
                    st.success("✅ Đã cập nhật!"); st.rerun()

# ============================================================
# TRANG: GIAO NHẬN ĐỒ
# ============================================================
def page_borrow():
    st.markdown('<div class="section-header">📦 Quản lý Giao nhận đồ</div>', unsafe_allow_html=True)
    df = st.session_state.df_borrow

    tab1, tab2 = st.tabs(["📋 Danh sách phiếu", "➕ Ghi nhận giao / nhận"])

    with tab1:
        # ── Thống kê nhanh ────────────────────────────────────
        tong      = len(df)
        da_giao   = len(df[df["Trạng thái"] == "Đã giao"])
        da_tra    = len(df[df["Trạng thái"] == "Đã trả"])
        c1,c2,c3  = st.columns(3)
        with c1: st.markdown(f'''<div class="metric-card"><h2>{tong}</h2><p>Tổng phiếu</p></div>''', unsafe_allow_html=True)
        with c2: st.markdown(f'''<div class="metric-card"><h2 style="color:#e67e22;">{da_giao}</h2><p>Đang cho mượn</p></div>''', unsafe_allow_html=True)
        with c3: st.markdown(f'''<div class="metric-card"><h2 style="color:#27ae60;">{da_tra}</h2><p>Đã hoàn trả</p></div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Bộ lọc ────────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1: ttf  = st.selectbox("Lọc trạng thái", ["Tất cả","Đã giao","Đã trả"])
        with c2: loai = st.selectbox("Lọc loại trang phục", ["Tất cả","Váy cưới","Áo dài","Suit"])
        df_show = df.copy()
        if ttf  != "Tất cả": df_show = df_show[df_show["Trạng thái"] == ttf]
        if loai != "Tất cả": df_show = df_show[df_show["Loại"]       == loai]

        # ── Render card phiếu ─────────────────────────────────
        if da_giao > 0 and ttf in ["Tất cả","Đã giao"]:
            st.warning(f"⚠️ Có **{da_giao}** phiếu chưa hoàn trả — cần theo dõi!")

        items = df_show.to_dict("records")
        if not items:
            st.info("Không có phiếu nào phù hợp bộ lọc.")
        else:
            n_cols = 3
            rows   = [items[i:i+n_cols] for i in range(0, len(items), n_cols)]
            for row in rows:
                cols = st.columns(n_cols)
                for ci, item in enumerate(row):
                    with cols[ci]:
                        tt       = item.get("Trạng thái","")
                        ma_gn    = item.get("Mã GN","")
                        ten_kh   = item.get("Tên khách","")
                        ma_tp    = item.get("Mã trang phục","")
                        loai_tp  = item.get("Loại","")
                        ngay_m   = item.get("Ngày mượn","")
                        ngay_t   = item.get("Ngày hẹn trả","")

                        # Màu & icon theo trạng thái
                        if tt == "Đã giao":
                            scolor = "#e67e22"
                            sicon  = "📤"
                            sbg    = "rgba(230,126,34,0.12)"
                        else:
                            scolor = "#27ae60"
                            sicon  = "✅"
                            sbg    = "rgba(39,174,96,0.12)"

                        # Tìm ảnh từ kho tương ứng
                        anh_url = ""
                        if loai_tp == "Váy cưới":
                            df_tp = st.session_state.df_vay
                            row_tp = df_tp[df_tp["Mã váy"] == ma_tp]
                            icon_tp = "👗"
                        elif loai_tp == "Áo dài":
                            df_tp = st.session_state.df_aodai
                            row_tp = df_tp[df_tp["Mã áo"] == ma_tp]
                            icon_tp = "🥻"
                        else:
                            df_tp = st.session_state.df_suit
                            row_tp = df_tp[df_tp["Mã suit"] == ma_tp]
                            icon_tp = "👔"

                        if not row_tp.empty and "Ảnh URL" in row_tp.columns:
                            anh_url = str(row_tp.iloc[0].get("Ảnh URL",""))
                        gia_str = ""
                        if not row_tp.empty and "Đơn giá" in row_tp.columns:
                            try:
                                gia_str = f"{int(row_tp.iloc[0]['Đơn giá']):,}đ".replace(",",".")
                            except: pass

                        img_html = f'''<img src="{anh_url}" style="width:100%;height:160px;object-fit:cover;border-radius:8px 8px 0 0;" onerror="this.style.display='none'">''' if anh_url else f'''<div style="width:100%;height:80px;background:#2A2618;border-radius:8px 8px 0 0;display:flex;align-items:center;justify-content:center;font-size:2.5rem;">{icon_tp}</div>'''

                        # Cảnh báo quá hạn
                        overdue_html = ""
                        try:
                            from datetime import date as _date
                            han_tra = _date.fromisoformat(ngay_t)
                            if tt == "Đã giao" and han_tra < _date.today():
                                overdue_html = '<div style="background:#e74c3c22;color:#e74c3c;font-size:0.7rem;font-weight:700;padding:4px 10px;border-radius:0;text-align:center;border-top:1px solid #e74c3c44;">⚠️ QUÁ HẠN TRẢ</div>'
                        except: pass

                        st.markdown(f'''
                        <div style="background:#2A2618;border:1px solid {scolor}44;
                                    border-radius:10px;overflow:hidden;margin-bottom:12px;
                                    box-shadow:0 2px 12px rgba(201,168,76,0.08);">
                            {img_html}
                            {overdue_html}
                            <div style="padding:10px 12px 12px;">
                                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                                    <span style="color:#C9A84C;font-weight:700;font-size:0.8rem;">{ma_gn}</span>
                                    <span style="background:{sbg};color:{scolor};font-size:0.68rem;
                                                 font-weight:700;padding:2px 8px;border-radius:10px;
                                                 border:1px solid {scolor}55;">{sicon} {tt}</span>
                                </div>
                                <div style="font-size:1rem;color:#FAF6EE;font-weight:700;margin-bottom:2px;">👤 {ten_kh}</div>
                                <div style="font-size:0.8rem;color:#E8D08A;margin-bottom:6px;">{icon_tp} {ma_tp} · {loai_tp}</div>
                                <div style="height:1px;background:#C9A84C22;margin:6px 0;"></div>
                                <div style="display:flex;justify-content:space-between;font-size:0.75rem;">
                                    <div style="color:#FAF6EE88;">
                                        📅 Mượn: <b style="color:#FAF6EE;">{ngay_m}</b>
                                    </div>
                                    <div style="color:#FAF6EE88;">
                                        🔔 Trả: <b style="color:#FAF6EE;">{ngay_t}</b>
                                    </div>
                                </div>
                                {f'<div style="margin-top:6px;text-align:right;color:#E8D08A;font-weight:800;font-size:0.88rem;">{gia_str}</div>' if gia_str else ""}
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

        # ── Xác nhận hoàn trả ─────────────────────────────────
        st.markdown("---")
        st.markdown("**🔄 Xác nhận hoàn trả**")
        chua_tra = df[df["Trạng thái"]=="Đã giao"]["Mã GN"].tolist()
        if chua_tra:
            with st.form("form_return"):
                chon_gn = st.selectbox("Chọn phiếu cần xác nhận trả", chua_tra)
                row_gn  = df[df["Mã GN"]==chon_gn].iloc[0]
                st.info(f"**{row_gn['Tên khách']}** | {row_gn['Mã trang phục']} ({row_gn['Loại']}) | Hẹn trả: **{row_gn['Ngày hẹn trả']}**")
                if st.form_submit_button("✅ Xác nhận đã hoàn trả", use_container_width=True):
                    st.session_state.df_borrow.loc[df["Mã GN"]==chon_gn, "Trạng thái"] = "Đã trả"
                    # Cập nhật lại trạng thái kho về Sẵn sàng
                    ma_tp_tra = row_gn["Mã trang phục"]
                    for ds_key, col in [("df_vay","Mã váy"),("df_aodai","Mã áo"),("df_suit","Mã suit")]:
                        mask = st.session_state[ds_key][col] == ma_tp_tra
                        if mask.any():
                            st.session_state[ds_key].loc[mask, "Trạng thái"] = "Sẵn sàng"
                    st.success(f"✅ Đã xác nhận hoàn trả — trang phục {ma_tp_tra} về kho!"); st.rerun()
        else:
            st.success("✅ Tất cả trang phục đã được hoàn trả!")

    with tab2:
        # ── Ghi nhận giao đồ mới ──────────────────────────────
        all_tp = (
            [f"{r} (Váy)" for r in st.session_state.df_vay[st.session_state.df_vay["Trạng thái"]=="Sẵn sàng"]["Mã váy"].tolist()] +
            [f"{r} (Áo dài)" for r in st.session_state.df_aodai[st.session_state.df_aodai["Trạng thái"]=="Sẵn sàng"]["Mã áo"].tolist()] +
            [f"{r} (Suit)" for r in st.session_state.df_suit[st.session_state.df_suit["Trạng thái"]=="Sẵn sàng"]["Mã suit"].tolist()]
        )
        customers = st.session_state.df_customers["Tên khách"].tolist()

        if not all_tp:
            st.warning("⚠️ Hiện không có trang phục nào sẵn sàng để giao!")
        else:
            st.markdown(f"**{len(all_tp)} trang phục đang sẵn sàng** có thể giao")
            with st.form("form_add_borrow"):
                c1, c2 = st.columns(2)
                with c1:
                    ten_kh  = st.selectbox("👤 Tên khách hàng", customers)
                    chon_tp = st.selectbox("👗 Trang phục (đang sẵn sàng)", all_tp)
                with c2:
                    ngay_muon = st.date_input("📅 Ngày mượn",    value=date.today())
                    ngay_tra  = st.date_input("🔔 Ngày hẹn trả", value=date.today()+timedelta(days=2))
                ghi_chu = st.text_input("📝 Ghi chú thêm", placeholder="Yêu cầu đặc biệt...")
                ma_gn   = f"GN{len(df)+1:03d}"

                # Tách mã và loại từ chuỗi "V001 (Váy)"
                def parse_tp(s):
                    if "(Váy)"    in s: return s.replace(" (Váy)",""),    "Váy cưới"
                    if "(Áo dài)" in s: return s.replace(" (Áo dài)",""), "Áo dài"
                    if "(Suit)"   in s: return s.replace(" (Suit)",""),   "Suit"
                    return s, "Khác"

                if st.form_submit_button("📦 Ghi nhận giao đồ", use_container_width=True):
                    ma_tp_giao, loai_tp_giao = parse_tp(chon_tp)
                    new_row = {
                        "Mã GN": ma_gn, "Tên khách": ten_kh,
                        "Mã trang phục": ma_tp_giao, "Loại": loai_tp_giao,
                        "Ngày mượn": str(ngay_muon), "Ngày hẹn trả": str(ngay_tra),
                        "Trạng thái": "Đã giao"
                    }
                    st.session_state.df_borrow = pd.concat(
                        [st.session_state.df_borrow, pd.DataFrame([new_row])], ignore_index=True)
                    # Cập nhật trạng thái kho
                    for ds_key, col in [("df_vay","Mã váy"),("df_aodai","Mã áo"),("df_suit","Mã suit")]:
                        mask = st.session_state[ds_key][col] == ma_tp_giao
                        if mask.any():
                            st.session_state[ds_key].loc[mask, "Trạng thái"] = "Đang cho mượn"
                    st.success(f"✅ Đã ghi nhận giao **{ma_tp_giao}** ({loai_tp_giao}) cho **{ten_kh}**")
                    st.rerun()

# ============================================================
# TRANG: NHÂN SỰ
# ============================================================
def page_personnel():
    st.markdown('<div class="section-header">⚙️ Quản lý Nhân sự & Phân quyền</div>', unsafe_allow_html=True)

    st.markdown("**👥 Danh sách tài khoản & phân quyền**")
    rows = []
    for uname, info in USERS.items():
        menus = ROLE_MENUS.get(info["role"], [])
        quyen = " · ".join([m.split(" ",1)[1] for m in menus if "Tổng quan" not in m])
        rows.append({
            "Username":           uname,
            "Họ tên / Chức danh": info["name"],
            "Phòng ban":          info["phong"],
            "Vai trò":            info["role"],
            "Quyền truy cập":     quyen,
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**🔐 Bảng phân quyền chi tiết**")
    role_rows = []
    icons_map = {"Admin":"👑","Lễ tân":"🛎️","Quản lý kho":"📦","Makeup":"💄","Nhiếp ảnh":"📷"}
    for role, menus in ROLE_MENUS.items():
        role_rows.append({
            "Vai trò": f"{icons_map.get(role,'')} {role}",
            "Các chức năng": " · ".join([m.split(" ",1)[1] for m in menus]),
            "Số chức năng": len(menus),
        })
    st.dataframe(pd.DataFrame(role_rows), use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:16px;margin-top:16px;">
        <div style="color:#C9A84C;font-weight:700;margin-bottom:8px;">📋 Thông tin hệ thống</div>
        <div style="color:#FAF6EE;font-size:0.88rem;line-height:1.9;">
            🏢 <b>TUANHOA WEDDING</b> — PHOTO · MAKE UP · BRIDAL · ACADEMY<br>
            📞 0963 758 883 · 0965 758 883<br>
            📍 Phố Cát – Vân Du – Thanh Hoá<br>
            📍 158 Khu 2 – Kim Tân – Thanh Hoá<br>
            📍 TMN – Khu 2 – Vân Du – Thanh Hoá
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN ROUTER
# ============================================================
if not st.session_state.logged_in:
    show_login()
else:
    selected = show_sidebar()
    page_map = {
        "🏠 Tổng quan":             page_dashboard,
        "👥 Khách hàng & Tiến độ":  page_customers,
        "📅 Lịch làm việc":         page_schedule,
        "👗 Kho váy cưới":          page_vay,
        "🥻 Kho áo dài":            page_aodai,
        "👔 Kho Suit":              page_suit,
        "📦 Giao nhận đồ":          page_borrow,
        "⚙️ Quản lý nhân sự":       page_personnel,
    }
    fn = page_map.get(selected)
    if fn: fn()
