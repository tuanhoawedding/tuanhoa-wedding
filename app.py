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
    "Admin":       ["🏠 Tổng quan", "📋 Hợp đồng", "🗓️ Lịch hẹn", "💄 Makeup",
                    "🎨 Hậu kỳ", "📅 Lịch làm việc",
                    "👗 Kho váy cưới", "🥻 Kho áo dài", "👔 Kho Suit", "📦 Giao nhận đồ",
                    "💰 Thu Chi", "💵 Tính Lương", "📊 Thuế & Báo cáo",
                    "⚙️ Quản lý nhân sự"],
    "Lễ tân":      ["🏠 Tổng quan", "📋 Hợp đồng", "🗓️ Lịch hẹn", "📦 Giao nhận đồ"],
    "Quản lý kho": ["🏠 Tổng quan", "👗 Kho váy cưới", "🥻 Kho áo dài", "👔 Kho Suit", "📦 Giao nhận đồ"],
    "Makeup":      ["🏠 Tổng quan", "💄 Makeup", "🗓️ Lịch hẹn"],
    "Nhiếp ảnh":   ["🏠 Tổng quan", "📅 Lịch làm việc", "🗓️ Lịch hẹn"],
    "Design":      ["🏠 Tổng quan", "🎨 Hậu kỳ", "📅 Lịch làm việc"],
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

    # ── Thu Chi ──────────────────────────────────────────
    if "df_thu_chi" not in st.session_state:
        st.session_state.df_thu_chi = pd.DataFrame([
            {"Mã":"TC001","Ngày":"2025-08-01","Loại":"Thu","Danh mục":"Dịch vụ chụp ảnh","Mô tả":"Khách Lê Thị Hồng - Gói Luxury","Số tiền":15000000,"Ghi chú":""},
            {"Mã":"TC002","Ngày":"2025-08-03","Loại":"Chi","Danh mục":"Lương nhân viên","Mô tả":"Lương tháng 8","Số tiền":25000000,"Ghi chú":""},
            {"Mã":"TC003","Ngày":"2025-08-05","Loại":"Thu","Danh mục":"Cho thuê trang phục","Mô tả":"Khách Nguyễn Thị Mai - Váy VIP","Số tiền":3500000,"Ghi chú":""},
            {"Mã":"TC004","Ngày":"2025-08-07","Loại":"Chi","Danh mục":"Vật tư - Makeup","Mô tả":"Mua son phấn Fenty, MAC","Số tiền":4200000,"Ghi chú":""},
            {"Mã":"TC005","Ngày":"2025-08-08","Loại":"Thu","Danh mục":"Dịch vụ makeup","Mô tả":"Khách Trần Văn Hùng - Gói Basic","Số tiền":5000000,"Ghi chú":""},
            {"Mã":"TC006","Ngày":"2025-08-10","Loại":"Chi","Danh mục":"Tiền điện nước","Mô tả":"Hóa đơn tháng 8","Số tiền":1800000,"Ghi chú":""},
            {"Mã":"TC007","Ngày":"2025-08-12","Loại":"Chi","Danh mục":"Giặt là trang phục","Mô tả":"Giặt hấy 12 bộ váy","Số tiền":600000,"Ghi chú":""},
            {"Mã":"TC008","Ngày":"2025-08-15","Loại":"Thu","Danh mục":"Dịch vụ design","Mô tả":"Album ảnh cưới Phạm Minh Tuấn","Số tiền":4000000,"Ghi chú":""},
        ])

    # ── Nhân sự & Lương ───────────────────────────────────
    if "df_nhansu" not in st.session_state:
        st.session_state.df_nhansu = pd.DataFrame([
            {"Mã NV":"NV001","Họ tên":"Phạm Thị Hoa",    "Chức vụ":"Makeup Artist","Phòng ban":"Makeup",    "Lương cơ bản":8000000, "Hệ số":1.2,"Số ngày công":26,"Thưởng":500000, "Khấu trừ":0},
            {"Mã NV":"NV002","Họ tên":"Đỗ Văn Ảnh",      "Chức vụ":"Nhiếp ảnh gia","Phòng ban":"Nhiếp ảnh","Lương cơ bản":10000000,"Hệ số":1.3,"Số ngày công":24,"Thưởng":1000000,"Khấu trừ":0},
            {"Mã NV":"NV003","Họ tên":"Nguyễn Thiết Kế",  "Chức vụ":"Designer",     "Phòng ban":"Design",   "Lương cơ bản":9000000, "Hệ số":1.2,"Số ngày công":26,"Thưởng":0,      "Khấu trừ":0},
            {"Mã NV":"NV004","Họ tên":"Trần Thị Lan",     "Chức vụ":"Lễ tân",       "Phòng ban":"Lễ tân",   "Lương cơ bản":6000000, "Hệ số":1.0,"Số ngày công":26,"Thưởng":200000, "Khấu trừ":0},
            {"Mã NV":"NV005","Họ tên":"Lê Văn Kho",       "Chức vụ":"Quản lý kho",  "Phòng ban":"Kho",      "Lương cơ bản":7000000, "Hệ số":1.1,"Số ngày công":25,"Thưởng":300000, "Khấu trừ":0},
        ])


    # ── Hợp đồng ─────────────────────────────────────────
    if "df_hopdong" not in st.session_state:
        st.session_state.df_hopdong = pd.DataFrame([
            {"Mã HĐ":"HD001","Khách hàng":"Nguyễn Văn A - Trần Thị B","SĐT":"0901234567",
             "Gói chụp":"Gói Studio I","Ngày chụp":"2025-08-10","Ngày cưới":"2025-08-15",
             "Ngày ăn hỏi":"2025-08-14","Ngày trả ảnh":"2025-09-10",
             "Thợ chụp":"Đỗ Văn Ảnh","Thợ makeup":"Phạm Thị Hoa","Lễ tân":"Trần Thị Lan",
             "Tổng tiền":9800000,"Đã TT":7800000,"Còn lại":2000000,
             "Trạng thái":"Đang thực hiện","Ghi chú":""},
            {"Mã HĐ":"HD002","Khách hàng":"Lê Văn C - Hoàng Thị D","SĐT":"0912345678",
             "Gói chụp":"Gói Ảnh Phòng","Ngày chụp":"2025-08-12","Ngày cưới":"2025-08-20",
             "Ngày ăn hỏi":"2025-08-18","Ngày trả ảnh":"2025-09-15",
             "Thợ chụp":"Đỗ Văn Ảnh","Thợ makeup":"Phạm Thị Hoa","Lễ tân":"Trần Thị Lan",
             "Tổng tiền":6100000,"Đã TT":5100000,"Còn lại":1000000,
             "Trạng thái":"Đang thực hiện","Ghi chú":""},
            {"Mã HĐ":"HD003","Khách hàng":"Phạm Minh E - Vũ Thị F","SĐT":"0923456789",
             "Gói chụp":"Gói Studio III","Ngày chụp":"2025-09-02","Ngày cưới":"2025-09-10",
             "Ngày ăn hỏi":"2025-09-08","Ngày trả ảnh":"2025-10-02",
             "Thợ chụp":"","Thợ makeup":"","Lễ tân":"",
             "Tổng tiền":14500000,"Đã TT":5000000,"Còn lại":9500000,
             "Trạng thái":"Đặt lịch","Ghi chú":"Yêu cầu chụp ngoại cảnh"},
        ])

    # ── Lịch hẹn ─────────────────────────────────────────
    if "df_lichhens" not in st.session_state:
        today = date.today()
        st.session_state.df_lichhens = pd.DataFrame([
            {"Mã LH":"LH001","Khách hàng":"Nguyễn Văn A - Trần Thị B","Loại":"Chụp ảnh",
             "Ngày":str(today),"Giờ":"08:00","Nhân viên":"Đỗ Văn Ảnh","Trạng thái":"Chờ"},
            {"Mã LH":"LH002","Khách hàng":"Nguyễn Văn A - Trần Thị B","Loại":"Trả ảnh",
             "Ngày":str(today + timedelta(days=30)),"Giờ":"09:00","Nhân viên":"Trần Thị Lan","Trạng thái":"Chờ"},
            {"Mã LH":"LH003","Khách hàng":"Lê Văn C - Hoàng Thị D","Loại":"Ăn hỏi",
             "Ngày":str(today + timedelta(days=5)),"Giờ":"06:00","Nhân viên":"Đỗ Văn Ảnh","Trạng thái":"Chờ"},
            {"Mã LH":"LH004","Khách hàng":"Lê Văn C - Hoàng Thị D","Loại":"Đám cưới",
             "Ngày":str(today + timedelta(days=7)),"Giờ":"05:30","Nhân viên":"Đỗ Văn Ảnh","Trạng thái":"Chờ"},
            {"Mã LH":"LH005","Khách hàng":"Phạm Minh E - Vũ Thị F","Loại":"Chụp ảnh",
             "Ngày":str(today + timedelta(days=15)),"Giờ":"07:30","Nhân viên":"","Trạng thái":"Chờ"},
        ])

    # ── Makeup ───────────────────────────────────────────
    if "df_makeup" not in st.session_state:
        today = date.today()
        st.session_state.df_makeup = pd.DataFrame([
            {"Mã MU":"MU001","Khách hàng":"Nguyễn Văn A - Trần Thị B","Loại makeup":"Makeup chụp",
             "Ngày":str(today),"Giờ":"05:30","Thợ makeup":"Phạm Thị Hoa","Trạng thái":"Chờ xác nhận","Ghi chú":""},
            {"Mã MU":"MU002","Khách hàng":"Lê Văn C - Hoàng Thị D","Loại makeup":"Makeup ăn hỏi",
             "Ngày":str(today + timedelta(days=5)),"Giờ":"04:30","Thợ makeup":"Phạm Thị Hoa","Trạng thái":"Chờ xác nhận","Ghi chú":""},
            {"Mã MU":"MU003","Khách hàng":"Lê Văn C - Hoàng Thị D","Loại makeup":"Makeup cưới",
             "Ngày":str(today + timedelta(days=7)),"Giờ":"03:00","Thợ makeup":"","Trạng thái":"Chưa giao","Ghi chú":""},
            {"Mã MU":"MU004","Khách hàng":"Phạm Minh E - Vũ Thị F","Loại makeup":"Makeup chụp",
             "Ngày":str(today + timedelta(days=15)),"Giờ":"05:00","Thợ makeup":"","Trạng thái":"Chưa giao","Ghi chú":""},
        ])

    # ── Hậu kỳ ───────────────────────────────────────────
    if "df_hauky" not in st.session_state:
        today = date.today()
        st.session_state.df_hauky = pd.DataFrame([
            {"Mã HK":"HK001","Khách hàng":"Nguyễn Văn A - Trần Thị B","Mã HĐ":"HD001",
             "Loại":"Chỉnh sửa album","Nhân viên HK":"Nguyễn Thiết Kế",
             "Ngày giao":"2025-08-10","Ngày hẹn trả":str(today + timedelta(days=30)),
             "Trạng thái HK":"Đang làm","Ghi chú":"100 ảnh chỉnh màu"},
            {"Mã HK":"HK002","Khách hàng":"Lê Văn C - Hoàng Thị D","Mã HĐ":"HD002",
             "Loại":"Video slide","Nhân viên HK":"Nguyễn Thiết Kế",
             "Ngày giao":"2025-08-12","Ngày hẹn trả":str(today + timedelta(days=10)),
             "Trạng thái HK":"Chờ xử lý","Ghi chú":""},
            {"Mã HK":"HK003","Khách hàng":"Phạm Minh E - Vũ Thị F","Mã HĐ":"HD003",
             "Loại":"Chỉnh sửa album","Nhân viên HK":"",
             "Ngày giao":"","Ngày hẹn trả":str(today + timedelta(days=45)),
             "Trạng thái HK":"Chưa giao","Ghi chú":""},
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

    # nav_override: set by dashboard card buttons
    if "nav_override" not in st.session_state:
        st.session_state.nav_override = None

    default_idx = 0
    if st.session_state.nav_override and st.session_state.nav_override in menus:
        default_idx = menus.index(st.session_state.nav_override)

    selected = st.sidebar.radio("Menu", menus, index=default_idx, label_visibility="collapsed")

    # Clear override after use
    if st.session_state.nav_override:
        st.session_state.nav_override = None

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
    user = st.session_state.user

    # ── Chào mừng ────────────────────────────────────────
    today_vn = date.today().strftime("%A, %d/%m/%Y")
    st.markdown(f'''
    <div style="margin-bottom:20px;">
        <div style="font-size:1.6rem;font-weight:800;color:#FAF6EE;">
            Xin chào, {user["name"]} 👋
        </div>
        <div style="font-size:0.82rem;color:#FAF6EE66;margin-top:2px;">
            Tổng quan hoạt động kinh doanh — {today_vn}
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ── Lấy dữ liệu ──────────────────────────────────────
    df_hd   = st.session_state.df_hopdong
    df_lh   = st.session_state.df_lichhens
    df_mu   = st.session_state.df_makeup
    df_hk   = st.session_state.df_hauky
    df_vay  = st.session_state.df_vay
    df_ao   = st.session_state.df_aodai
    df_suit = st.session_state.df_suit
    df_bn   = st.session_state.df_borrow
    df_tc   = st.session_state.df_thu_chi
    today_s = str(date.today())

    # Tính nhanh
    tong_hd       = len(df_hd)
    hd_dang_th    = len(df_hd[df_hd["Trạng thái"]=="Đang thực hiện"])
    hd_con_no     = df_hd["Còn lại"].sum()
    hd_doanh_thu  = df_hd["Tổng tiền"].sum()
    lh_hom_nay    = len(df_lh[df_lh["Ngày"]==today_s])
    mu_chua_giao  = len(df_mu[df_mu["Thợ makeup"]==""])
    hk_qua_han    = len(df_hk[(df_hk["Trạng thái HK"]!="Hoàn thành")&(df_hk["Ngày hẹn trả"]<today_s)&(df_hk["Ngày hẹn trả"]!="")])
    hk_chua_giao  = len(df_hk[df_hk["Trạng thái HK"]=="Chưa giao"])
    vay_san_sang  = len(df_vay[df_vay["Trạng thái"]=="Sẵn sàng"])
    do_cho_tra    = len(df_bn[df_bn["Trạng thái"]=="Đã giao"])
    tong_thu_tc   = df_tc[df_tc["Loại"]=="Thu"]["Số tiền"].sum()
    tong_chi_tc   = df_tc[df_tc["Loại"]=="Chi"]["Số tiền"].sum()

    # ── Cảnh báo nhanh ───────────────────────────────────
    warnings = []
    if mu_chua_giao:  warnings.append(f"💄 {mu_chua_giao} lịch Makeup chưa giao")
    if hk_qua_han:    warnings.append(f"🎨 {hk_qua_han} Hậu kỳ quá hạn")
    if hk_chua_giao:  warnings.append(f"📋 {hk_chua_giao} Hậu kỳ chưa giao việc")
    if do_cho_tra:    warnings.append(f"📦 {do_cho_tra} đồ chưa hoàn trả")
    if warnings:
        warn_html = " &nbsp;·&nbsp; ".join([f'<span style="color:#e67e22;font-weight:600;">{w}</span>' for w in warnings])
        st.markdown(f'''
        <div style="background:#e67e2210;border:1px solid #e67e2244;border-radius:8px;
                    padding:10px 16px;margin-bottom:18px;font-size:0.8rem;">
            ⚠️ &nbsp; {warn_html}
        </div>''', unsafe_allow_html=True)

    # ── Định nghĩa tất cả modules ─────────────────────────
    MODULES = [
        # (menu_key, icon, title, subtitle, color, badge_val, badge_label, row_group)
        ("📋 Hợp đồng",    "📋", "Hợp đồng",         f"{tong_hd} hợp đồng · {hd_dang_th} đang thực hiện",   "#C9A84C", f"{hd_doanh_thu/1_000_000:.0f}M", "Doanh thu",    0),
        ("🗓️ Lịch hẹn",    "🗓️", "Lịch hẹn",          f"{lh_hom_nay} lịch hôm nay",                          "#3498db", str(lh_hom_nay),                  "Hôm nay",      0),
        ("💄 Makeup",       "💄", "Makeup",             f"{len(df_mu)} lịch · {mu_chua_giao} chưa giao",        "#e91e8c", str(mu_chua_giao) if mu_chua_giao else "✓","Chưa giao",0),
        ("🎨 Hậu kỳ",      "🎨", "Hậu kỳ",             f"{len(df_hk)} công việc · {hk_qua_han} quá hạn",       "#9b59b6", str(hk_qua_han) if hk_qua_han else "✓","Quá hạn",  0),
        ("👥 Khách hàng & Tiến độ","👥","Khách hàng",  f"Tiến độ & trạng thái khách",                          "#27ae60", str(len(st.session_state.df_customers)), "Khách hàng",1),
        ("📅 Lịch làm việc","📅", "Lịch làm việc",     f"Giao việc Makeup · Photo · Design",                   "#e67e22", str(len(st.session_state.df_schedule)),  "Lịch",      1),
        ("👗 Kho váy cưới", "👗", "Kho váy cưới",      f"{vay_san_sang} váy sẵn sàng",                         "#e74c3c", str(vay_san_sang),                 "Sẵn sàng",    1),
        ("🥻 Kho áo dài",   "🥻", "Kho áo dài",        f"{len(df_ao)} áo dài",                                 "#f39c12", str(len(df_ao)),                   "Tổng",        1),
        ("👔 Kho Suit",     "👔", "Kho Suit",           f"{len(df_suit)} suit",                                  "#1abc9c", str(len(df_suit)),                 "Tổng",        1),
        ("📦 Giao nhận đồ", "📦", "Giao nhận đồ",      f"{do_cho_tra} đồ chưa hoàn trả",                       "#e67e22", str(do_cho_tra) if do_cho_tra else "✓","Chưa trả", 1),
        ("💰 Thu Chi",      "💰", "Thu Chi",            f"Thu: {tong_thu_tc/1_000_000:.1f}M · Chi: {tong_chi_tc/1_000_000:.1f}M","#27ae60",f"{(tong_thu_tc-tong_chi_tc)/1_000_000:.1f}M","Lợi nhuận",2),
        ("💵 Tính Lương",   "💵", "Tính Lương",         f"{len(st.session_state.df_nhansu)} nhân viên",          "#E8D08A", str(len(st.session_state.df_nhansu)),"NV",          2),
        ("📊 Thuế & Báo cáo","📊","Thuế & Báo cáo",    "Kê khai thuế · Sổ kế toán",                            "#e74c3c", "7%","GTGT",                                         2),
        ("⚙️ Quản lý nhân sự","⚙️","Nhân sự",          f"Phân quyền & tài khoản",                              "#888",    str(len(USERS)),"Tài khoản",                          2),
    ]

    menus_allowed = ROLE_MENUS.get(user["role"], [])

    # ── Group 0: Nghiệp vụ chính ─────────────────────────
    group0 = [m for m in MODULES if m[7]==0 and m[0] in menus_allowed]
    group1 = [m for m in MODULES if m[7]==1 and m[0] in menus_allowed]
    group2 = [m for m in MODULES if m[7]==2 and m[0] in menus_allowed]

    def render_module_cards(modules, ncols=4):
        rows = [modules[i:i+ncols] for i in range(0, len(modules), ncols)]
        for row in rows:
            cols = st.columns(len(row))
            for ci, (menu_key, icon, title, subtitle, color, badge_val, badge_label, _) in enumerate(row):
                with cols[ci]:
                    st.markdown(f'''
                    <div style="background:linear-gradient(135deg,#2A2618 60%,{color}18 100%);
                                border:1px solid {color}44;border-radius:12px;
                                padding:18px 16px;margin-bottom:4px;
                                box-shadow:0 4px 16px rgba(0,0,0,0.25);
                                position:relative;overflow:hidden;">
                        <div style="position:absolute;top:-10px;right:-10px;font-size:3.5rem;opacity:0.06;">{icon}</div>
                        <div style="font-size:1.8rem;margin-bottom:8px;">{icon}</div>
                        <div style="font-size:0.95rem;font-weight:800;color:#FAF6EE;margin-bottom:4px;">{title}</div>
                        <div style="font-size:0.72rem;color:#FAF6EE66;margin-bottom:12px;line-height:1.4;">{subtitle}</div>
                        <div style="display:flex;align-items:center;justify-content:space-between;">
                            <span style="color:{color};font-weight:800;font-size:1.4rem;">{badge_val}</span>
                            <span style="background:{color}22;color:{color};font-size:0.65rem;
                                         font-weight:700;padding:2px 8px;border-radius:8px;">{badge_label}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    if st.button(f"Vào {title}", key=f"dash_btn_{menu_key}", use_container_width=True):
                        st.session_state.nav_override = menu_key
                        st.rerun()

    # Render 3 nhóm
    if group0:
        st.markdown('<div style="color:#C9A84C;font-weight:700;font-size:0.78rem;letter-spacing:0.1em;margin-bottom:10px;">NGHIỆP VỤ CHÍNH</div>', unsafe_allow_html=True)
        render_module_cards(group0, ncols=4)
        st.markdown("<br>", unsafe_allow_html=True)

    if group1:
        st.markdown('<div style="color:#C9A84C;font-weight:700;font-size:0.78rem;letter-spacing:0.1em;margin-bottom:10px;">KHO & VẬN HÀNH</div>', unsafe_allow_html=True)
        render_module_cards(group1, ncols=min(len(group1), 5))
        st.markdown("<br>", unsafe_allow_html=True)

    if group2:
        st.markdown('<div style="color:#C9A84C;font-weight:700;font-size:0.78rem;letter-spacing:0.1em;margin-bottom:10px;">TÀI CHÍNH & QUẢN TRỊ</div>', unsafe_allow_html=True)
        render_module_cards(group2, ncols=4)

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
# TRANG: THU CHI
# ============================================================
def page_thu_chi():
    st.markdown('<div class="section-header">💰 Quản lý Thu Chi Doanh Nghiệp</div>', unsafe_allow_html=True)
    df = st.session_state.df_thu_chi

    # ── KPI tổng quan ─────────────────────────────────────
    tong_thu = df[df["Loại"]=="Thu"]["Số tiền"].sum()
    tong_chi = df[df["Loại"]=="Chi"]["Số tiền"].sum()
    loi_nhuan = tong_thu - tong_chi
    tab1, tab2, tab3 = st.tabs(["📊 Tổng hợp", "📋 Chi tiết giao dịch", "➕ Thêm giao dịch"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**💚 Thu theo danh mục**")
            thu_cat = df[df["Loại"]=="Thu"].groupby("Danh mục")["Số tiền"].sum().reset_index()
            thu_cat.columns = ["Danh mục","Số tiền"]
            thu_cat["Tỷ lệ"] = (thu_cat["Số tiền"]/tong_thu*100).round(1).astype(str) + "%"
            thu_cat["Số tiền (đ)"] = thu_cat["Số tiền"].apply(lambda x: f"{int(x):,}".replace(",","."))
            st.dataframe(thu_cat[["Danh mục","Số tiền (đ)","Tỷ lệ"]], use_container_width=True, hide_index=True)
        with c2:
            st.markdown("**❤️ Chi theo danh mục**")
            chi_cat = df[df["Loại"]=="Chi"].groupby("Danh mục")["Số tiền"].sum().reset_index()
            chi_cat.columns = ["Danh mục","Số tiền"]
            chi_cat["Tỷ lệ"] = (chi_cat["Số tiền"]/tong_chi*100).round(1).astype(str) + "%"
            chi_cat["Số tiền (đ)"] = chi_cat["Số tiền"].apply(lambda x: f"{int(x):,}".replace(",","."))
            st.dataframe(chi_cat[["Danh mục","Số tiền (đ)","Tỷ lệ"]], use_container_width=True, hide_index=True)

        # Biểu đồ bar
        st.markdown("**📊 Biểu đồ Thu vs Chi theo danh mục**")
        import json
        thu_data = df[df["Loại"]=="Thu"].groupby("Danh mục")["Số tiền"].sum()
        chi_data = df[df["Loại"]=="Chi"].groupby("Danh mục")["Số tiền"].sum()
        all_cats  = sorted(set(list(thu_data.index) + list(chi_data.index)))
        thu_vals  = [thu_data.get(c,0)/1_000_000 for c in all_cats]
        chi_vals  = [chi_data.get(c,0)/1_000_000 for c in all_cats]
        chart_html = f"""
        <div style="background:#2A2618;border:1px solid #C9A84C33;border-radius:10px;padding:16px;margin-top:8px;">
            <div style="display:flex;gap:16px;margin-bottom:12px;">
                <span style="color:#27ae60;font-size:0.8rem;">■ Thu (triệu đ)</span>
                <span style="color:#e74c3c;font-size:0.8rem;">■ Chi (triệu đ)</span>
            </div>
            {"".join([f'''
            <div style="margin-bottom:10px;">
                <div style="font-size:0.72rem;color:#C9A84C;margin-bottom:3px;">{c}</div>
                <div style="display:flex;gap:4px;align-items:center;">
                    <div style="height:16px;width:{min(tv/max(max(thu_vals),max(chi_vals),0.1)*260,260):.0f}px;
                                background:linear-gradient(90deg,#27ae60,#2ecc71);border-radius:3px;min-width:3px;"></div>
                    <span style="font-size:0.7rem;color:#27ae60;">{tv:.1f}M</span>
                </div>
                <div style="display:flex;gap:4px;align-items:center;margin-top:2px;">
                    <div style="height:16px;width:{min(cv/max(max(thu_vals),max(chi_vals),0.1)*260,260):.0f}px;
                                background:linear-gradient(90deg,#e74c3c,#c0392b);border-radius:3px;min-width:3px;"></div>
                    <span style="font-size:0.7rem;color:#e74c3c;">{cv:.1f}M</span>
                </div>
            </div>
            ''' for c,tv,cv in zip(all_cats,thu_vals,chi_vals)])}
        </div>"""
        st.markdown(chart_html, unsafe_allow_html=True)

    with tab2:
        loai_f = st.selectbox("Lọc loại", ["Tất cả","Thu","Chi"])
        df_show = df if loai_f=="Tất cả" else df[df["Loại"]==loai_f]
        df_disp = df_show.copy()
        df_disp["Số tiền"] = df_disp["Số tiền"].apply(lambda x: f"{int(x):,}".replace(",",".") + "đ")
        st.dataframe(df_disp, use_container_width=True, hide_index=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**➕ Thêm giao dịch mới**")
            with st.form("form_add_tc"):
                ma_tc   = f"TC{len(df)+1:03d}"
                ngay_tc = st.date_input("📅 Ngày", value=date.today())
                loai_tc = st.selectbox("Loại", ["Thu","Chi"])
                dm_thu  = ["Dịch vụ chụp ảnh","Dịch vụ makeup","Cho thuê trang phục","Dịch vụ design","Khác"]
                dm_chi  = ["Lương nhân viên","Vật tư - Makeup","Tiền điện nước","Giặt là trang phục","Marketing","Thuê mặt bằng","Khác"]
                dm_tc   = st.selectbox("Danh mục", dm_thu if loai_tc=="Thu" else dm_chi)
                mo_ta   = st.text_input("Mô tả")
                so_tien = st.number_input("Số tiền (đồng)", min_value=0, step=100000, value=1000000)
                ghi_chu = st.text_input("Ghi chú")
                if st.form_submit_button("✅ Thêm giao dịch", use_container_width=True):
                    new_row = {"Mã":ma_tc,"Ngày":str(ngay_tc),"Loại":loai_tc,
                               "Danh mục":dm_tc,"Mô tả":mo_ta,"Số tiền":so_tien,"Ghi chú":ghi_chu}
                    st.session_state.df_thu_chi = pd.concat(
                        [st.session_state.df_thu_chi, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"✅ Đã thêm giao dịch {loai_tc}: {so_tien:,}đ".replace(",",".")); st.rerun()


# ============================================================
# TRANG: TÍNH LƯƠNG
# ============================================================
def page_luong():
    st.markdown('<div class="section-header">💵 Tính Lương Nhân Sự</div>', unsafe_allow_html=True)
    df = st.session_state.df_nhansu.copy()

    # Hằng số BHXH, BHYT, BHTN (2024)
    BHXH_NLD  = 0.08   # 8% BHXH người lao động
    BHYT_NLD  = 0.015  # 1.5% BHYT
    BHTN_NLD  = 0.01   # 1% BHTN
    TONG_BH   = BHXH_NLD + BHYT_NLD + BHTN_NLD  # 10.5%
    GIAM_TRU_BT = 11_000_000  # Giảm trừ bản thân 11 triệu

    BHXH_DN  = 0.175   # 17.5% BHXH doanh nghiệp
    BHYT_DN  = 0.03    # 3% BHYT
    BHTN_DN  = 0.01    # 1% BHTN
    TONG_BH_DN = BHXH_DN + BHYT_DN + BHTN_DN  # 21.5%

    def tinh_thue_tncn(thu_nhap_chiu_thue):
        """Thuế TNCN lũy tiến 7 bậc 2024"""
        bac = [
            (5_000_000,   0.05),
            (5_000_000,   0.10),
            (8_000_000,   0.15),
            (14_000_000,  0.20),
            (20_000_000,  0.25),
            (28_000_000,  0.30),
            (float("inf"),0.35),
        ]
        thue, con_lai = 0, max(thu_nhap_chiu_thue, 0)
        for muc, ts in bac:
            if con_lai <= 0: break
            chiu = min(con_lai, muc)
            thue += chiu * ts
            con_lai -= chiu
        return thue

    # Tính toán lương
    rows_calc = []
    for _, r in df.iterrows():
        luong_cb   = r["Lương cơ bản"]
        he_so      = r["Hệ số"]
        ngay_cong  = r["Số ngày công"]
        thuong     = r["Thưởng"]
        khau_tru   = r["Khấu trừ"]

        luong_thuc = luong_cb * he_so * (ngay_cong / 26)
        tong_thu_nhap = luong_thuc + thuong

        bh_nld     = luong_cb * TONG_BH
        thu_nhap_chiu_thue = tong_thu_nhap - bh_nld - GIAM_TRU_BT
        thue_tncn  = tinh_thue_tncn(thu_nhap_chiu_thue)
        tong_khau  = bh_nld + thue_tncn + khau_tru
        luong_net  = tong_thu_nhap - tong_khau

        bh_dn      = luong_cb * TONG_BH_DN
        cp_dn      = luong_thuc + thuong + bh_dn

        rows_calc.append({
            "Mã NV":      r["Mã NV"],
            "Họ tên":     r["Họ tên"],
            "Chức vụ":    r["Chức vụ"],
            "Ngày công":  ngay_cong,
            "Lương thực": int(luong_thuc),
            "Thưởng":     int(thuong),
            "BH người LD":int(bh_nld),
            "Thuế TNCN":  int(thue_tncn),
            "Lương NET":  int(luong_net),
            "CP doanh nghiệp": int(cp_dn),
        })
    df_calc = pd.DataFrame(rows_calc)

    # ── KPI ────────────────────────────────────────────────
    tong_net = df_calc["Lương NET"].sum()
    tong_cp  = df_calc["CP doanh nghiệp"].sum()
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(f'''<div class="metric-card"><h2>{len(df_calc)}</h2><p>Số nhân viên</p></div>''', unsafe_allow_html=True)
    with c2: st.markdown(f'''<div class="metric-card"><h2 style="color:#E8D08A;">{tong_net/1_000_000:.1f}M</h2><p>💵 Tổng lương NET</p></div>''', unsafe_allow_html=True)
    with c3: st.markdown(f'''<div class="metric-card"><h2 style="color:#e74c3c;">{tong_cp/1_000_000:.1f}M</h2><p>🏢 Chi phí DN thực tế</p></div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Bảng lương tháng", "👤 Chi tiết từng nhân viên", "✏️ Cập nhật dữ liệu"])

    with tab1:
        st.markdown("**📋 Bảng lương chi tiết tháng**")
        df_disp = df_calc.copy()
        for col in ["Lương thực","Thưởng","BH người LD","Thuế TNCN","Lương NET","CP doanh nghiệp"]:
            df_disp[col] = df_disp[col].apply(lambda x: f"{int(x):,}".replace(",",".") + "đ")
        st.dataframe(df_disp, use_container_width=True, hide_index=True)

        st.markdown("""
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:8px;padding:12px;margin-top:12px;font-size:0.78rem;">
            <div style="color:#C9A84C;font-weight:700;margin-bottom:6px;">📌 Ghi chú các khoản khấu trừ (theo luật 2024)</div>
            <div style="color:#FAF6EE88;line-height:1.8;">
                • BHXH người lao động: <b style="color:#FAF6EE;">8%</b> lương cơ bản<br>
                • BHYT người lao động: <b style="color:#FAF6EE;">1.5%</b> lương cơ bản<br>
                • BHTN người lao động: <b style="color:#FAF6EE;">1%</b> lương cơ bản<br>
                • Giảm trừ gia cảnh bản thân: <b style="color:#FAF6EE;">11,000,000đ/tháng</b><br>
                • Thuế TNCN: Lũy tiến 7 bậc từ 5% → 35%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        chon_nv = st.selectbox("Chọn nhân viên", df_calc["Họ tên"].tolist())
        row_nv  = df_calc[df_calc["Họ tên"]==chon_nv].iloc[0]
        row_ns  = st.session_state.df_nhansu[st.session_state.df_nhansu["Họ tên"]==chon_nv].iloc[0]

        c1,c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:16px;">
                <div style="color:#C9A84C;font-weight:800;font-size:1rem;margin-bottom:12px;">
                    👤 {row_nv["Họ tên"]} — {row_nv["Chức vụ"]}
                </div>
                <div style="line-height:2;font-size:0.85rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">Lương cơ bản</span>
                        <span style="color:#FAF6EE;">{int(row_ns["Lương cơ bản"]):,}đ</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">Hệ số lương</span>
                        <span style="color:#FAF6EE;">× {row_ns["Hệ số"]}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">Ngày công</span>
                        <span style="color:#FAF6EE;">{row_nv["Ngày công"]}/26 ngày</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">Lương thực tế</span>
                        <span style="color:#E8D08A;font-weight:700;">{int(row_nv["Lương thực"]):,}đ</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">Thưởng</span>
                        <span style="color:#27ae60;">+{int(row_nv["Thưởng"]):,}đ</span>
                    </div>
                </div>
            </div>
            """.replace(",","."), unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:16px;">
                <div style="color:#e74c3c;font-weight:800;font-size:0.9rem;margin-bottom:12px;">
                    📉 Các khoản khấu trừ
                </div>
                <div style="line-height:2;font-size:0.85rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">BHXH+BHYT+BHTN (10.5%)</span>
                        <span style="color:#e74c3c;">-{int(row_nv["BH người LD"]):,}đ</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">Thuế TNCN</span>
                        <span style="color:#e74c3c;">-{int(row_nv["Thuế TNCN"]):,}đ</span>
                    </div>
                    <div style="height:1px;background:#C9A84C33;margin:8px 0;"></div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE;font-weight:700;">💵 Lương NET thực lĩnh</span>
                        <span style="color:#27ae60;font-weight:800;font-size:1rem;">{int(row_nv["Lương NET"]):,}đ</span>
                    </div>
                    <div style="height:1px;background:#C9A84C33;margin:8px 0;"></div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#FAF6EE88;">Chi phí thực tế doanh nghiệp</span>
                        <span style="color:#e67e22;font-weight:700;">{int(row_nv["CP doanh nghiệp"]):,}đ</span>
                    </div>
                </div>
            </div>
            """.replace(",","."), unsafe_allow_html=True)

    with tab3:
        st.markdown("**✏️ Cập nhật thông tin lương nhân viên**")
        with st.form("form_update_luong"):
            chon_nv2  = st.selectbox("Chọn nhân viên", st.session_state.df_nhansu["Họ tên"].tolist())
            row_edit  = st.session_state.df_nhansu[st.session_state.df_nhansu["Họ tên"]==chon_nv2].iloc[0]
            c1, c2   = st.columns(2)
            with c1:
                new_cb   = st.number_input("Lương cơ bản", value=int(row_edit["Lương cơ bản"]), step=500000)
                new_hs   = st.number_input("Hệ số", value=float(row_edit["Hệ số"]), step=0.1, format="%.1f")
            with c2:
                new_nc   = st.number_input("Số ngày công", value=int(row_edit["Số ngày công"]), min_value=0, max_value=31)
                new_th   = st.number_input("Thưởng", value=int(row_edit["Thưởng"]), step=100000)
            new_kt = st.number_input("Khấu trừ khác", value=int(row_edit["Khấu trừ"]), step=100000)
            if st.form_submit_button("💾 Cập nhật lương", use_container_width=True):
                mask = st.session_state.df_nhansu["Họ tên"] == chon_nv2
                st.session_state.df_nhansu.loc[mask,"Lương cơ bản"]  = new_cb
                st.session_state.df_nhansu.loc[mask,"Hệ số"]         = new_hs
                st.session_state.df_nhansu.loc[mask,"Số ngày công"]  = new_nc
                st.session_state.df_nhansu.loc[mask,"Thưởng"]        = new_th
                st.session_state.df_nhansu.loc[mask,"Khấu trừ"]      = new_kt
                st.success(f"✅ Đã cập nhật lương cho {chon_nv2}!"); st.rerun()


# ============================================================
# TRANG: THUẾ & BÁO CÁO
# ============================================================
def page_thue():
    st.markdown('<div class="section-header">📊 Thuế & Báo cáo Tài chính</div>', unsafe_allow_html=True)

    # Hằng số thuế ngành dịch vụ ảnh cưới (2024)
    THUE_GTGT    = 0.10   # VAT 10% dịch vụ nhiếp ảnh / makeup
    THUE_TNDN    = 0.20   # 20% TNDN (doanh nghiệp vừa và nhỏ)
    MUC_MIEN_TNDN= 200_000_000  # Được giảm 30% nếu DT < 200M/năm (SME)
    BHXH_DN      = 0.175
    BHYT_DN      = 0.03
    BHTN_DN      = 0.01

    df_tc  = st.session_state.df_thu_chi
    df_ns  = st.session_state.df_nhansu

    tong_thu = df_tc[df_tc["Loại"]=="Thu"]["Số tiền"].sum()
    tong_chi = df_tc[df_tc["Loại"]=="Chi"]["Số tiền"].sum()

    # ── GTGT ─────────────────────────────────────────────
    thue_gtgt_phai_nop = tong_thu * THUE_GTGT
    thue_gtgt_dau_vao  = tong_chi * THUE_GTGT * 0.5  # Ước tính 50% chi phí có hóa đơn
    gtgt_net           = max(thue_gtgt_phai_nop - thue_gtgt_dau_vao, 0)

    # ── TNDN ─────────────────────────────────────────────
    luong_cp   = sum(r["Lương cơ bản"] * r["Hệ số"] * (r["Số ngày công"]/26)
                     + r["Thưởng"]
                     + r["Lương cơ bản"] * (BHXH_DN + BHYT_DN + BHTN_DN)
                     for _, r in df_ns.iterrows())
    loi_nhuan_tt = tong_thu - tong_chi - luong_cp
    thue_tndn    = max(loi_nhuan_tt, 0) * THUE_TNDN
    if tong_thu * 12 < MUC_MIEN_TNDN:
        thue_tndn = thue_tndn * 0.70  # Giảm 30% cho SME

    tong_thue = gtgt_net + thue_tndn

    # ── KPI ─────────────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'''<div class="metric-card"><h2 style="color:#e67e22;">{gtgt_net/1_000_000:.1f}M</h2><p>🧾 Thuế GTGT nộp</p></div>''', unsafe_allow_html=True)
    with c2: st.markdown(f'''<div class="metric-card"><h2 style="color:#e74c3c;">{thue_tndn/1_000_000:.1f}M</h2><p>🏢 Thuế TNDN</p></div>''', unsafe_allow_html=True)
    with c3: st.markdown(f'''<div class="metric-card"><h2 style="color:#C9A84C;">{tong_thue/1_000_000:.1f}M</h2><p>📊 Tổng thuế ước tính</p></div>''', unsafe_allow_html=True)
    with c4: st.markdown(f'''<div class="metric-card"><h2 style="color:#27ae60;">{max(loi_nhuan_tt-thue_tndn,0)/1_000_000:.1f}M</h2><p>💰 Lợi nhuận sau thuế</p></div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📋 Báo cáo chi tiết", "📌 Hướng dẫn kê khai"])

    with tab1:
        st.markdown("**🧾 1. Thuế Giá trị gia tăng (GTGT) — VAT 10%**")
        st.markdown(f"""
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:16px;margin-bottom:16px;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:0.85rem;">
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Doanh thu chịu thuế GTGT (10%)</div>
                    <div style="color:#27ae60;font-weight:700;font-size:1rem;">{int(tong_thu):,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Thuế GTGT đầu ra phải nộp</div>
                    <div style="color:#e67e22;font-weight:700;font-size:1rem;">{int(thue_gtgt_phai_nop):,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Thuế GTGT đầu vào được khấu trừ (ước)</div>
                    <div style="color:#3498db;font-weight:700;font-size:1rem;">{int(thue_gtgt_dau_vao):,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">💳 Số thuế GTGT phải nộp</div>
                    <div style="color:#e74c3c;font-weight:800;font-size:1.1rem;">{int(gtgt_net):,}đ</div>
                </div>
            </div>
        </div>
        """.replace(",","."), unsafe_allow_html=True)

        st.markdown("**🏢 2. Thuế Thu nhập doanh nghiệp (TNDN) — 20%**")
        st.markdown(f"""
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:16px;margin-bottom:16px;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:0.85rem;">
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Tổng doanh thu</div>
                    <div style="color:#27ae60;font-weight:700;">{int(tong_thu):,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Chi phí vận hành</div>
                    <div style="color:#e74c3c;font-weight:700;">-{int(tong_chi):,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Chi phí lương (tổng)</div>
                    <div style="color:#e74c3c;font-weight:700;">-{int(luong_cp):,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Lợi nhuận trước thuế</div>
                    <div style="color:#E8D08A;font-weight:700;">{int(loi_nhuan_tt):,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">Thuế suất TNDN</div>
                    <div style="color:#FAF6EE;font-weight:700;">20% {"(giảm 30% SME)" if tong_thu*12<MUC_MIEN_TNDN else ""}</div>
                </div>
                <div>
                    <div style="color:#FAF6EE88;margin-bottom:4px;">💳 Số thuế TNDN phải nộp</div>
                    <div style="color:#e74c3c;font-weight:800;font-size:1.1rem;">{int(thue_tndn):,}đ</div>
                </div>
            </div>
        </div>
        """.replace(",","."), unsafe_allow_html=True)

        st.markdown("**👥 3. BHXH doanh nghiệp đóng**")
        tong_bh_dn = sum(r["Lương cơ bản"] * (BHXH_DN+BHYT_DN+BHTN_DN) for _,r in df_ns.iterrows())
        st.markdown(f"""
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:16px;">
            <div style="font-size:0.85rem;line-height:2;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE88;">BHXH doanh nghiệp đóng (17.5%)</span>
                    <span style="color:#e74c3c;">{int(sum(r["Lương cơ bản"]*BHXH_DN for _,r in df_ns.iterrows())):,}đ</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE88;">BHYT doanh nghiệp đóng (3%)</span>
                    <span style="color:#e74c3c;">{int(sum(r["Lương cơ bản"]*BHYT_DN for _,r in df_ns.iterrows())):,}đ</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE88;">BHTN doanh nghiệp đóng (1%)</span>
                    <span style="color:#e74c3c;">{int(sum(r["Lương cơ bản"]*BHTN_DN for _,r in df_ns.iterrows())):,}đ</span>
                </div>
                <div style="height:1px;background:#C9A84C33;margin:6px 0;"></div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE;font-weight:700;">Tổng BHXH doanh nghiệp phải đóng</span>
                    <span style="color:#e74c3c;font-weight:800;">{int(tong_bh_dn):,}đ</span>
                </div>
            </div>
        </div>
        """.replace(",","."), unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:20px;">
            <div style="color:#C9A84C;font-weight:800;font-size:1rem;margin-bottom:14px;">
                📌 Hướng dẫn kê khai thuế — Ngành Nhiếp ảnh & Dịch vụ cưới hỏi
            </div>
            <div style="color:#FAF6EE;font-size:0.85rem;line-height:2.2;">

                <div style="color:#E8D08A;font-weight:700;margin-top:8px;">🧾 Thuế GTGT (kê khai hàng tháng/quý)</div>
                <div style="color:#FAF6EE88;">• Mã ngành: 7420 — Hoạt động nhiếp ảnh</div>
                <div style="color:#FAF6EE88;">• Thuế suất: <b style="color:#FAF6EE;">10%</b> cho dịch vụ chụp ảnh, makeup, cho thuê trang phục</div>
                <div style="color:#FAF6EE88;">• Nộp tờ khai mẫu <b style="color:#FAF6EE;">01/GTGT</b> trước ngày 20 tháng sau</div>
                <div style="color:#FAF6EE88;">• Xuất hóa đơn điện tử cho từng dịch vụ</div>

                <div style="color:#E8D08A;font-weight:700;margin-top:12px;">🏢 Thuế TNDN (kê khai tạm nộp theo quý)</div>
                <div style="color:#FAF6EE88;">• Thuế suất phổ thông: <b style="color:#FAF6EE;">20%</b></div>
                <div style="color:#FAF6EE88;">• SME (doanh thu &lt; 200M/năm): được giảm 30% → còn <b style="color:#FAF6EE;">14%</b></div>
                <div style="color:#FAF6EE88;">• Nộp tạm nộp quý trước ngày <b style="color:#FAF6EE;">30</b> tháng đầu quý tiếp theo</div>
                <div style="color:#FAF6EE88;">• Quyết toán năm: mẫu <b style="color:#FAF6EE;">03/TNDN</b> trước 31/03 năm sau</div>

                <div style="color:#E8D08A;font-weight:700;margin-top:12px;">👤 Thuế TNCN nhân viên</div>
                <div style="color:#FAF6EE88;">• Khấu trừ tại nguồn hàng tháng</div>
                <div style="color:#FAF6EE88;">• Nộp mẫu <b style="color:#FAF6EE;">05/KK-TNCN</b> hàng tháng trước ngày 20</div>
                <div style="color:#FAF6EE88;">• Quyết toán năm: mẫu <b style="color:#FAF6EE;">05/QTT-TNCN</b> trước 31/03 năm sau</div>

                <div style="color:#E8D08A;font-weight:700;margin-top:12px;">📋 BHXH nộp hàng tháng</div>
                <div style="color:#FAF6EE88;">• Nộp trước ngày <b style="color:#FAF6EE;">15</b> hàng tháng qua cổng BHXH điện tử</div>
                <div style="color:#FAF6EE88;">• Tổng tỷ lệ doanh nghiệp + người lao động: <b style="color:#FAF6EE;">31.5%</b> lương cơ bản</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
# TRANG: HỢP ĐỒNG
# ============================================================
def page_hopdong():
    st.markdown('<div class="section-header">📋 Quản lý Hợp đồng</div>', unsafe_allow_html=True)
    df = st.session_state.df_hopdong

    # Init selected contract state
    if "selected_hd" not in st.session_state:
        st.session_state.selected_hd = None

    # ── Nếu đang xem chi tiết ─────────────────────────────
    if st.session_state.selected_hd:
        _show_hopdong_detail(st.session_state.selected_hd)
        return

    # ── Tìm kiếm & lọc ────────────────────────────────────
    c1, c2 = st.columns([3,1])
    with c1: search = st.text_input("🔍 Tìm theo tên, SĐT, mã HĐ...", placeholder="Nhập từ khoá...", label_visibility="collapsed")
    with c2: tt_f   = st.selectbox("Trạng thái", ["Tất cả","Đặt lịch","Đang thực hiện","Hoàn thành","Hủy"], label_visibility="collapsed")

    df_show = df.copy()
    if search:
        mask = (df_show["Khách hàng"].str.contains(search, case=False, na=False) |
                df_show["SĐT"].str.contains(search, case=False, na=False) |
                df_show["Mã HĐ"].str.contains(search, case=False, na=False))
        df_show = df_show[mask]
    if tt_f != "Tất cả":
        df_show = df_show[df_show["Trạng thái"]==tt_f]

    st.markdown(f"**{len(df_show)} hợp đồng** phù hợp", unsafe_allow_html=False)

    # ── Danh sách card — 1 chạm vào chi tiết ─────────────
    for _, row in df_show.iterrows():
        tt_color = {"Đang thực hiện":"#e67e22","Hoàn thành":"#27ae60",
                    "Đặt lịch":"#3498db","Hủy":"#e74c3c"}.get(row["Trạng thái"],"#888")
        con_lai_color = "#e74c3c" if row["Còn lại"] > 0 else "#27ae60"
        pct = int(row["Đã TT"] / row["Tổng tiền"] * 100) if row["Tổng tiền"] > 0 else 0

        # Progress bar
        progress_html = f'''
        <div style="height:3px;background:#C9A84C22;border-radius:2px;margin-top:8px;">
            <div style="height:3px;width:{pct}%;background:linear-gradient(90deg,#C9A84C,#27ae60);border-radius:2px;"></div>
        </div>
        <div style="font-size:0.65rem;color:#FAF6EE44;text-align:right;margin-top:1px;">{pct}% đã thanh toán</div>
        '''

        st.markdown(f'''
        <div style="background:#2A2618;border:1px solid #C9A84C33;border-radius:10px;
                    padding:14px 18px;margin-bottom:8px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.2);
                    transition:border 0.2s;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                        <span style="color:#C9A84C;font-weight:700;font-size:0.8rem;">{row["Mã HĐ"]}</span>
                        <span style="background:{tt_color}22;color:{tt_color};font-size:0.68rem;
                                     font-weight:700;padding:2px 8px;border-radius:10px;
                                     border:1px solid {tt_color}44;">{row["Trạng thái"]}</span>
                    </div>
                    <div style="font-size:1rem;color:#FAF6EE;font-weight:700;">{row["Khách hàng"]}</div>
                    <div style="font-size:0.75rem;color:#FAF6EE88;margin-top:3px;">
                        📞 {row["SĐT"]} &nbsp;|&nbsp; 🎁 {row["Gói chụp"]}
                    </div>
                    <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:0.72rem;color:#FAF6EE88;margin-top:6px;">
                        <span>📅 Chụp: <b style="color:#FAF6EE;">{row["Ngày chụp"]}</b></span>
                        <span>💒 Cưới: <b style="color:#FAF6EE;">{row["Ngày cưới"]}</b></span>
                        <span>📷 {row["Thợ chụp"] or "⚠️ Chưa giao"}</span>
                        <span>💄 {row["Thợ makeup"] or "⚠️ Chưa giao"}</span>
                    </div>
                </div>
                <div style="text-align:right;min-width:130px;">
                    <div style="font-size:0.72rem;color:#FAF6EE66;">Tổng HĐ</div>
                    <div style="color:#E8D08A;font-weight:800;font-size:1.05rem;">{int(row["Tổng tiền"]):,}đ</div>
                    <div style="font-size:0.72rem;color:#27ae60;">Đã TT: {int(row["Đã TT"]):,}đ</div>
                    <div style="font-size:0.72rem;color:{con_lai_color};font-weight:700;">Còn: {int(row["Còn lại"]):,}đ</div>
                </div>
            </div>
            {progress_html}
        </div>
        '''.replace(",","."), unsafe_allow_html=True)

        # Nút 1 chạm — mở chi tiết
        if st.button(f"👁️ Xem chi tiết  {row['Mã HĐ']}", key=f"btn_hd_{row['Mã HĐ']}",
                     use_container_width=True):
            st.session_state.selected_hd = row["Mã HĐ"]
            st.rerun()

    # ── Lập hợp đồng mới ──────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("➕ Lập hợp đồng mới"):
        goi_options = ["Gói Studio I","Gói Studio II","Gói Studio III",
                       "Gói Ảnh Phòng","Gói Ảnh Phòng VIP","Gói Ngoại Cảnh"]
        with st.form("form_add_hd"):
            c1,c2 = st.columns(2)
            with c1:
                ma_hd   = f"HD{len(df)+1:03d}"
                kh_name = st.text_input("👤 Tên cặp đôi (Chú - Cô) *")
                sdt     = st.text_input("📞 Số điện thoại")
                goi     = st.selectbox("🎁 Gói chụp", goi_options)
                tong_t  = st.number_input("💰 Tổng tiền (đ)", min_value=0, step=500000, value=8000000)
                dat_coc = st.number_input("✅ Đặt cọc (đ)", min_value=0, step=500000, value=2000000)
            with c2:
                ngay_chup = st.date_input("📅 Ngày chụp", min_value=date.today())
                ngay_cuoi = st.date_input("💒 Ngày cưới", min_value=date.today())
                ngay_ah   = st.date_input("💍 Ngày ăn hỏi", min_value=date.today())
                ngay_tra  = st.date_input("🖼️ Ngày hẹn trả ảnh", min_value=date.today())
            ghi_chu = st.text_area("📝 Ghi chú", height=60)
            if st.form_submit_button("✅ Lập hợp đồng", use_container_width=True):
                if kh_name:
                    new_row = {
                        "Mã HĐ":ma_hd,"Khách hàng":kh_name,"SĐT":sdt,
                        "Gói chụp":goi,"Ngày chụp":str(ngay_chup),"Ngày cưới":str(ngay_cuoi),
                        "Ngày ăn hỏi":str(ngay_ah),"Ngày trả ảnh":str(ngay_tra),
                        "Thợ chụp":"","Thợ makeup":"","Lễ tân":"",
                        "Tổng tiền":tong_t,"Đã TT":dat_coc,"Còn lại":tong_t-dat_coc,
                        "Trạng thái":"Đặt lịch","Ghi chú":ghi_chu
                    }
                    st.session_state.df_hopdong = pd.concat(
                        [st.session_state.df_hopdong, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"✅ Đã lập hợp đồng {ma_hd} cho {kh_name}!")
                    st.rerun()
                else:
                    st.error("Vui lòng nhập tên khách hàng!")


def _show_hopdong_detail(ma_hd):
    """Màn hình chi tiết hợp đồng — 1 chạm quay lại"""
    df  = st.session_state.df_hopdong
    row = df[df["Mã HĐ"]==ma_hd]
    if row.empty:
        st.error("Không tìm thấy hợp đồng!")
        st.session_state.selected_hd = None
        return
    r = row.iloc[0]

    # Header + nút quay lại
    c_back, c_title = st.columns([1,6])
    with c_back:
        if st.button("← Quay lại", use_container_width=True):
            st.session_state.selected_hd = None
            st.rerun()
    with c_title:
        tt_color = {"Đang thực hiện":"#e67e22","Hoàn thành":"#27ae60",
                    "Đặt lịch":"#3498db","Hủy":"#e74c3c"}.get(r["Trạng thái"],"#888")
        st.markdown(f'''
        <div style="display:flex;align-items:center;gap:12px;padding:6px 0;">
            <span style="color:#C9A84C;font-weight:800;font-size:1.1rem;">{r["Mã HĐ"]}</span>
            <span style="background:{tt_color}22;color:{tt_color};font-size:0.78rem;
                         font-weight:700;padding:3px 12px;border-radius:10px;
                         border:1px solid {tt_color}44;">{r["Trạng thái"]}</span>
            <span style="color:#FAF6EE88;font-size:0.78rem;">Ngày lập: {date.today().strftime("%d/%m/%Y")}</span>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Thông tin khách + Lịch hẹn ────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'''
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:12px;padding:18px;height:100%;">
            <div style="color:#C9A84C;font-weight:700;font-size:0.85rem;margin-bottom:12px;">👤 THÔNG TIN KHÁCH HÀNG</div>
            <div style="font-size:1.1rem;color:#FAF6EE;font-weight:800;margin-bottom:6px;">{r["Khách hàng"]}</div>
            <div style="font-size:0.85rem;color:#FAF6EE88;margin-bottom:4px;">📞 {r["SĐT"]}</div>
            <div style="font-size:0.85rem;color:#E8D08A;">🎁 {r["Gói chụp"]}</div>
            <div style="font-size:0.78rem;color:#FAF6EE66;margin-top:8px;">{r["Ghi chú"] or ""}</div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:12px;padding:18px;height:100%;">
            <div style="color:#C9A84C;font-weight:700;font-size:0.85rem;margin-bottom:12px;">📅 LỊCH HẸN</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:0.85rem;">
                <div>
                    <div style="color:#FAF6EE66;font-size:0.72rem;margin-bottom:2px;">Ngày ăn hỏi</div>
                    <div style="color:#FAF6EE;font-weight:700;">{r["Ngày ăn hỏi"]}</div>
                </div>
                <div>
                    <div style="color:#FAF6EE66;font-size:0.72rem;margin-bottom:2px;">Ngày cưới</div>
                    <div style="color:#FAF6EE;font-weight:700;">{r["Ngày cưới"]}</div>
                </div>
                <div>
                    <div style="color:#FAF6EE66;font-size:0.72rem;margin-bottom:2px;">Ngày chụp</div>
                    <div style="color:#FAF6EE;font-weight:700;">{r["Ngày chụp"]}</div>
                </div>
                <div>
                    <div style="color:#FAF6EE66;font-size:0.72rem;margin-bottom:2px;">Ngày hẹn trả ảnh</div>
                    <div style="color:#E8D08A;font-weight:700;">{r["Ngày trả ảnh"]}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Ekip + Thanh toán ─────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'''
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:12px;padding:18px;">
            <div style="color:#C9A84C;font-weight:700;font-size:0.85rem;margin-bottom:12px;">👥 EKIP PHỤ TRÁCH</div>
            <div style="font-size:0.88rem;line-height:2.2;">
                <div style="display:flex;justify-content:space-between;border-bottom:1px solid #C9A84C22;padding-bottom:6px;margin-bottom:6px;">
                    <span style="color:#FAF6EE88;">📷 Thợ chụp</span>
                    <span style="color:{"#FAF6EE" if r["Thợ chụp"] else "#e74c3c"};font-weight:600;">
                        {r["Thợ chụp"] or "⚠️ Chưa giao"}
                    </span>
                </div>
                <div style="display:flex;justify-content:space-between;border-bottom:1px solid #C9A84C22;padding-bottom:6px;margin-bottom:6px;">
                    <span style="color:#FAF6EE88;">💄 Thợ makeup</span>
                    <span style="color:{"#FAF6EE" if r["Thợ makeup"] else "#e74c3c"};font-weight:600;">
                        {r["Thợ makeup"] or "⚠️ Chưa giao"}
                    </span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE88;">🛎️ Lễ tân</span>
                    <span style="color:{"#FAF6EE" if r["Lễ tân"] else "#e74c3c"};font-weight:600;">
                        {r["Lễ tân"] or "⚠️ Chưa giao"}
                    </span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        pct = int(r["Đã TT"]/r["Tổng tiền"]*100) if r["Tổng tiền"] > 0 else 0
        con_lai_c = "#e74c3c" if r["Còn lại"] > 0 else "#27ae60"
        st.markdown(f'''
        <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:12px;padding:18px;">
            <div style="color:#C9A84C;font-weight:700;font-size:0.85rem;margin-bottom:12px;">💰 LỊCH THANH TOÁN</div>
            <div style="font-size:0.88rem;line-height:2.2;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE88;">Tổng hợp đồng</span>
                    <span style="color:#E8D08A;font-weight:700;">{int(r["Tổng tiền"]):,}đ</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE88;">Đã thanh toán</span>
                    <span style="color:#27ae60;font-weight:700;">+{int(r["Đã TT"]):,}đ</span>
                </div>
                <div style="height:1px;background:#C9A84C22;margin:6px 0;"></div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#FAF6EE;font-weight:700;">Còn lại</span>
                    <span style="color:{con_lai_c};font-weight:800;font-size:1rem;">{int(r["Còn lại"]):,}đ</span>
                </div>
            </div>
            <div style="margin-top:10px;">
                <div style="height:6px;background:#C9A84C22;border-radius:3px;">
                    <div style="height:6px;width:{pct}%;background:linear-gradient(90deg,#C9A84C,#27ae60);border-radius:3px;"></div>
                </div>
                <div style="font-size:0.68rem;color:#FAF6EE44;text-align:right;margin-top:2px;">{pct}% đã thanh toán</div>
            </div>
        </div>
        '''.replace(",","."), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gói dịch vụ ───────────────────────────────────────
    with st.expander("🎁 Gói dịch vụ & Chi tiết", expanded=True):
        GOI_INFO = {
            "Gói Studio I":      {"dv":["Chụp ảnh ½ ngày tại Studio","01 váy VIP, 01 váy Simple","02 vest cao cấp","Makeup & làm tóc","File gốc + 15 file chỉnh sửa nghệ thuật"],"gia_dv":5000000,"gia_sp":3500000},
            "Gói Studio II":     {"dv":["Chụp ảnh 1 ngày tại Studio","02 váy VIP","02 vest cao cấp","Makeup & làm tóc","File gốc + 25 file chỉnh sửa"],"gia_dv":7000000,"gia_sp":4500000},
            "Gói Studio III":    {"dv":["Chụp ảnh 1.5 ngày","03 váy VIP + 01 Luxury","03 vest","Makeup & làm tóc","File gốc + 40 file + Video highlight"],"gia_dv":10000000,"gia_sp":5000000},
            "Gói Ảnh Phòng":     {"dv":["Chụp ảnh phòng ½ ngày","01 váy VIP","01 vest","Makeup & làm tóc","File gốc + 10 file"],"gia_dv":3500000,"gia_sp":2500000},
            "Gói Ảnh Phòng VIP": {"dv":["Chụp ảnh phòng 1 ngày","02 váy VIP","02 vest cao cấp","Makeup & làm tóc","File gốc + 20 file"],"gia_dv":6000000,"gia_sp":4000000},
            "Gói Ngoại Cảnh":    {"dv":["Chụp ảnh ngoại cảnh 1 ngày","02 váy VIP + 01 Luxury","02 vest","Makeup & làm tóc","File gốc + 30 file chỉnh sửa"],"gia_dv":8000000,"gia_sp":6000000},
        }
        goi = GOI_INFO.get(r["Gói chụp"], {"dv":[],"gia_dv":0,"gia_sp":0})
        dv_list = "".join([f'<li style="margin:4px 0;color:#FAF6EE88;">{d}</li>' for d in goi["dv"]])
        thue_dv  = int(goi["gia_dv"] * 0.07)
        thue_sp  = int(goi["gia_sp"] * 0.015)
        st.markdown(f'''
        <div style="background:#1C1A10;border:1px solid #C9A84C33;border-radius:10px;padding:16px;">
            <div style="color:#C9A84C;font-weight:700;margin-bottom:8px;">{r["Gói chụp"]}</div>
            <div style="font-size:0.82rem;margin-bottom:12px;">
                <div style="color:#FAF6EE88;margin-bottom:4px;">Dịch vụ bao gồm:</div>
                <ul style="margin:0;padding-left:18px;">{dv_list}</ul>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:0.82rem;border-top:1px solid #C9A84C22;padding-top:12px;">
                <div>
                    <div style="color:#FAF6EE66;">Dịch vụ (thuế 7%)</div>
                    <div style="color:#FAF6EE;font-weight:700;">{int(goi["gia_dv"]):,}đ</div>
                    <div style="color:#e67e22;font-size:0.72rem;">Thuế: {thue_dv:,}đ</div>
                </div>
                <div>
                    <div style="color:#FAF6EE66;">Sản phẩm (thuế 1.5%)</div>
                    <div style="color:#FAF6EE;font-weight:700;">{int(goi["gia_sp"]):,}đ</div>
                    <div style="color:#3498db;font-size:0.72rem;">Thuế: {thue_sp:,}đ</div>
                </div>
            </div>
        </div>
        '''.replace(",","."), unsafe_allow_html=True)

    # ── Cập nhật hợp đồng ─────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("✏️ Cập nhật hợp đồng"):
        with st.form(f"form_update_hd_{ma_hd}"):
            c1,c2,c3 = st.columns(3)
            with c1:
                new_tt   = st.selectbox("Trạng thái", ["Đặt lịch","Đang thực hiện","Hoàn thành","Hủy"],
                    index=["Đặt lịch","Đang thực hiện","Hoàn thành","Hủy"].index(r["Trạng thái"]) if r["Trạng thái"] in ["Đặt lịch","Đang thực hiện","Hoàn thành","Hủy"] else 0)
                new_datt = st.number_input("Đã thanh toán (đ)", value=int(r["Đã TT"]), step=500000)
            with c2:
                new_thochup  = st.text_input("Thợ chụp", value=str(r["Thợ chụp"]))
                new_thomu    = st.text_input("Thợ makeup", value=str(r["Thợ makeup"]))
            with c3:
                new_letan = st.text_input("Lễ tân", value=str(r["Lễ tân"]))
                new_gc    = st.text_input("Ghi chú", value=str(r["Ghi chú"]))
            if st.form_submit_button("💾 Lưu thay đổi", use_container_width=True):
                mask = st.session_state.df_hopdong["Mã HĐ"]==ma_hd
                st.session_state.df_hopdong.loc[mask,"Trạng thái"] = new_tt
                st.session_state.df_hopdong.loc[mask,"Đã TT"]      = new_datt
                st.session_state.df_hopdong.loc[mask,"Còn lại"]    = int(r["Tổng tiền"]) - new_datt
                st.session_state.df_hopdong.loc[mask,"Thợ chụp"]   = new_thochup
                st.session_state.df_hopdong.loc[mask,"Thợ makeup"]  = new_thomu
                st.session_state.df_hopdong.loc[mask,"Lễ tân"]     = new_letan
                st.session_state.df_hopdong.loc[mask,"Ghi chú"]    = new_gc
                st.success("✅ Đã lưu thay đổi!"); st.rerun()

    # Hậu kỳ liên quan
    df_hk = st.session_state.df_hauky[st.session_state.df_hauky["Mã HĐ"]==ma_hd]
    if not df_hk.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"🎨 Hậu kỳ liên quan ({len(df_hk)} công việc)"):
            for _, hk in df_hk.iterrows():
                tc = {"Chưa giao":"#e74c3c","Chờ xử lý":"#e67e22","Đang làm":"#3498db","Hoàn thành":"#27ae60"}.get(hk["Trạng thái HK"],"#888")
                st.markdown(f'''
                <div style="background:#1C1A10;border-left:3px solid {tc};border-radius:0 8px 8px 0;
                            padding:10px 14px;margin-bottom:6px;font-size:0.82rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:{tc};font-weight:700;">{hk["Trạng thái HK"]}</span>
                        <span style="color:#FAF6EE88;">Hẹn trả: {hk["Ngày hẹn trả"]}</span>
                    </div>
                    <div style="color:#FAF6EE;margin-top:2px;">{hk["Loại"]} — {hk["Nhân viên HK"] or "Chưa giao"}</div>
                </div>''', unsafe_allow_html=True)

# ============================================================
# TRANG: LỊCH HẸN — Calendar view
# ============================================================
def page_lichhens():
    st.markdown('<div class="section-header">🗓️ Lịch hẹn</div>', unsafe_allow_html=True)
    df = st.session_state.df_lichhens

    LOAI_COLORS = {
        "Chụp ảnh": "#3498db",
        "Trả ảnh":  "#27ae60",
        "Ăn hỏi":   "#e74c3c",
        "Đám cưới": "#f39c12",
    }

    tab1, tab2 = st.tabs(["📅 Lịch tháng", "➕ Tạo lịch hẹn"])

    with tab1:
        # Month picker
        col1,col2,_ = st.columns([1,1,4])
        with col1:
            sel_month = st.selectbox("Tháng", list(range(1,13)), index=date.today().month-1)
        with col2:
            sel_year  = st.selectbox("Năm", [2025,2026,2027], index=1)

        # Stats
        df_month = df[df["Ngày"].str.startswith(f"{sel_year}-{sel_month:02d}")]

        # Build calendar grid
        import calendar
        cal = calendar.monthcalendar(sel_year, sel_month)
        days_header = ["CN","T2","T3","T4","T5","T6","T7"]

        # Header row
        cols = st.columns(7)
        for i,d in enumerate(days_header):
            cols[i].markdown(f'<div style="text-align:center;font-weight:700;color:#C9A84C;'
                             f'font-size:0.78rem;padding:4px 0;">{d}</div>', unsafe_allow_html=True)

        # Weeks
        for week in cal:
            cols = st.columns(7)
            for ci, day in enumerate(week):
                with cols[ci]:
                    if day == 0:
                        st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)
                        continue
                    day_str   = f"{sel_year}-{sel_month:02d}-{day:02d}"
                    day_events = df[df["Ngày"]==day_str]
                    is_today  = day_str == str(date.today())
                    border    = "2px solid #C9A84C" if is_today else "1px solid #C9A84C22"
                    bg        = "rgba(201,168,76,0.08)" if is_today else "#2A2618"

                    events_html = ""
                    for _, ev in day_events.iterrows():
                        ec = LOAI_COLORS.get(ev["Loại"],"#888")
                        events_html += (f'<div style="background:{ec}33;color:{ec};font-size:0.6rem;'
                                       f'font-weight:600;padding:1px 4px;border-radius:3px;'
                                       f'margin-top:2px;white-space:nowrap;overflow:hidden;'
                                       f'text-overflow:ellipsis;">{ev["Loại"]}</div>')

                    st.markdown(f'''
                    <div style="background:{bg};border:{border};border-radius:6px;
                                padding:4px 6px;min-height:80px;margin:1px;">
                        <div style="font-size:0.8rem;color:{"#C9A84C" if is_today else "#FAF6EE"};
                                    font-weight:{"800" if is_today else "400"};">{day}</div>
                        {events_html}
                    </div>''', unsafe_allow_html=True)

        # Legend
        st.markdown("<br>", unsafe_allow_html=True)
        legend = " &nbsp; ".join([f'<span style="color:{c};">■</span> <span style="color:#FAF6EE88;font-size:0.78rem;">{l}</span>'
                                   for l,c in LOAI_COLORS.items()])
        st.markdown(f'<div style="text-align:center;">{legend}</div>', unsafe_allow_html=True)

    with tab2:
        customers = (st.session_state.df_hopdong["Khách hàng"].tolist() +
                     st.session_state.df_customers["Tên khách"].tolist())
        with st.form("form_add_lichhens"):
            c1,c2 = st.columns(2)
            with c1:
                kh      = st.selectbox("👤 Khách hàng", customers)
                loai    = st.selectbox("📌 Loại lịch hẹn", ["Chụp ảnh","Trả ảnh","Ăn hỏi","Đám cưới"])
                nv      = st.text_input("👤 Nhân viên phụ trách")
            with c2:
                ngay_lh = st.date_input("📅 Ngày", min_value=date.today())
                gio_lh  = st.time_input("⏰ Giờ", value=datetime.strptime("08:00","%H:%M").time())
            ma_lh = f"LH{len(df)+1:03d}"
            if st.form_submit_button("✅ Tạo lịch hẹn", use_container_width=True):
                new_row = {"Mã LH":ma_lh,"Khách hàng":kh,"Loại":loai,
                           "Ngày":str(ngay_lh),"Giờ":gio_lh.strftime("%H:%M"),
                           "Nhân viên":nv,"Trạng thái":"Chờ"}
                st.session_state.df_lichhens = pd.concat(
                    [st.session_state.df_lichhens, pd.DataFrame([new_row])], ignore_index=True)
                clr = LOAI_COLORS.get(loai,"#C9A84C")
                st.success(f"✅ Đã tạo lịch **{loai}** cho **{kh}** ngày {ngay_lh}")
                st.rerun()


# ============================================================
# TRANG: MAKEUP
# ============================================================
def page_makeup():
    st.markdown('<div class="section-header">💄 Quản lý Makeup</div>', unsafe_allow_html=True)
    df   = st.session_state.df_makeup
    user = st.session_state.user

    MU_COLORS = {
        "Makeup chụp":   "#e91e8c",
        "Makeup ăn hỏi": "#9b59b6",
        "Makeup cưới":   "#f39c12",
    }


    tab1, tab2 = st.tabs(["📋 Danh sách lịch makeup", "➕ Thêm lịch makeup"])

    with tab1:
        # Filter
        c1,c2 = st.columns(2)
        with c1: lf = st.selectbox("Loại", ["Tất cả"] + list(MU_COLORS.keys()))
        with c2: tf = st.selectbox("Trạng thái", ["Tất cả","Chưa giao","Chờ xác nhận","Đang thực hiện","Hoàn thành"])
        df_show = df.copy()
        if lf != "Tất cả": df_show = df_show[df_show["Loại makeup"]==lf]
        if tf != "Tất cả": df_show = df_show[df_show["Trạng thái"]==tf]

        if df_show.empty:
            st.info("Không có lịch makeup phù hợp.")
        else:
            for _, row in df_show.iterrows():
                color  = MU_COLORS.get(row["Loại makeup"],"#888")
                tt     = row["Trạng thái"]
                tc     = {"Chưa giao":"#e74c3c","Chờ xác nhận":"#e67e22",
                          "Đang thực hiện":"#3498db","Hoàn thành":"#27ae60"}.get(tt,"#888")
                mu_nv  = row["Thợ makeup"] if row["Thợ makeup"] else "⚠️ Chưa giao"
                st.markdown(f'''
                <div style="background:#2A2618;border-left:4px solid {color};
                            border-radius:0 10px 10px 0;border:1px solid {color}33;
                            border-left:4px solid {color};padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                        <div>
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                                <span style="color:{color};font-size:0.72rem;font-weight:700;">{row["Mã MU"]}</span>
                                <span style="background:{color}22;color:{color};font-size:0.68rem;
                                             padding:1px 8px;border-radius:10px;">{row["Loại makeup"]}</span>
                                <span style="background:{tc}22;color:{tc};font-size:0.65rem;
                                             padding:1px 8px;border-radius:10px;">{tt}</span>
                            </div>
                            <div style="font-size:0.92rem;color:#FAF6EE;font-weight:700;">{row["Khách hàng"]}</div>
                            <div style="font-size:0.75rem;color:#E8D08A;margin-top:2px;">💄 {mu_nv}</div>
                        </div>
                        <div style="text-align:right;font-size:0.78rem;">
                            <div style="color:#C9A84C;font-weight:700;">📅 {row["Ngày"]}</div>
                            <div style="color:#FAF6EE88;">⏰ {row["Giờ"]}</div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

        # Giao việc makeup
        st.markdown("---")
        st.markdown("**💄 Giao việc makeup**")
        chua_giao_list = df[df["Thợ makeup"]==""]["Mã MU"].tolist()
        if chua_giao_list:
            with st.form("form_giao_makeup"):
                chon_mu = st.selectbox("Chọn lịch chưa giao", chua_giao_list)
                nv_mu   = st.text_input("Thợ makeup phụ trách")
                if st.form_submit_button("💄 Giao việc", use_container_width=True):
                    mask = st.session_state.df_makeup["Mã MU"]==chon_mu
                    st.session_state.df_makeup.loc[mask,"Thợ makeup"]  = nv_mu
                    st.session_state.df_makeup.loc[mask,"Trạng thái"]  = "Chờ xác nhận"
                    st.success(f"✅ Đã giao lịch {chon_mu} cho {nv_mu}"); st.rerun()

    with tab2:
        customers = st.session_state.df_hopdong["Khách hàng"].tolist()
        with st.form("form_add_makeup"):
            c1,c2 = st.columns(2)
            with c1:
                kh     = st.selectbox("👤 Khách hàng", customers)
                loai   = st.selectbox("💄 Loại makeup", list(MU_COLORS.keys()))
                nv_mu2 = st.text_input("Thợ makeup")
            with c2:
                ngay_mu = st.date_input("📅 Ngày", min_value=date.today())
                gio_mu  = st.time_input("⏰ Giờ", value=datetime.strptime("05:00","%H:%M").time())
                gc_mu   = st.text_input("Ghi chú")
            ma_mu = f"MU{len(df)+1:03d}"
            tt_init = "Chờ xác nhận" if nv_mu2 else "Chưa giao"
            if st.form_submit_button("✅ Thêm lịch makeup", use_container_width=True):
                new_row = {"Mã MU":ma_mu,"Khách hàng":kh,"Loại makeup":loai,
                           "Ngày":str(ngay_mu),"Giờ":gio_mu.strftime("%H:%M"),
                           "Thợ makeup":nv_mu2,"Trạng thái":tt_init,"Ghi chú":gc_mu}
                st.session_state.df_makeup = pd.concat(
                    [st.session_state.df_makeup, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ Đã thêm lịch makeup {loai} cho {kh}"); st.rerun()


# ============================================================
# TRANG: HẬU KỲ
# ============================================================
def page_hauky():
    st.markdown('<div class="section-header">🎨 Quản lý Hậu kỳ</div>', unsafe_allow_html=True)
    df   = st.session_state.df_hauky
    today_str = str(date.today())

    # Quá hạn
    qua_han = df[(df["Trạng thái HK"]!="Hoàn thành") &
                 (df["Ngày hẹn trả"] != "") &
                 (df["Ngày hẹn trả"] < today_str)]
    chua_giao= len(df[df["Trạng thái HK"]=="Chưa giao"])
    hoan_th  = len(df[df["Trạng thái HK"]=="Hoàn thành"])

    # Cảnh báo
    if len(qua_han) > 0:
        st.markdown(f'''
        <div style="background:#e74c3c18;border:1px solid #e74c3c55;border-radius:8px;
                    padding:12px 16px;margin:12px 0;">
            <span style="color:#e74c3c;font-weight:700;">⚠️ {len(qua_han)} công việc QUÁ HẠN</span>
            <span style="color:#FAF6EE88;font-size:0.82rem;"> — Cần xử lý gấp!</span>
        </div>''', unsafe_allow_html=True)
    if chua_giao > 0:
        st.markdown(f'''
        <div style="background:#e67e2218;border:1px solid #e67e2255;border-radius:8px;
                    padding:12px 16px;margin-bottom:12px;">
            <span style="color:#e67e22;font-weight:700;">📋 {chua_giao} công việc CHƯA GIAO</span>
            <span style="color:#FAF6EE88;font-size:0.82rem;"> — Cần tạo công việc hậu kỳ</span>
        </div>''', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Danh sách hậu kỳ", "➕ Giao việc mới"])

    with tab1:
        tt_f = st.selectbox("Lọc trạng thái", ["Tất cả","Chưa giao","Chờ xử lý","Đang làm","Hoàn thành"])
        df_show = df if tt_f=="Tất cả" else df[df["Trạng thái HK"]==tt_f]

        for _, row in df_show.iterrows():
            tt    = row["Trạng thái HK"]
            tc    = {"Chưa giao":"#e74c3c","Chờ xử lý":"#e67e22",
                     "Đang làm":"#3498db","Hoàn thành":"#27ae60"}.get(tt,"#888")
            # Overdue check
            is_over = (row["Ngày hẹn trả"] and row["Ngày hẹn trả"] < today_str and tt != "Hoàn thành")
            over_badge = '<span style="background:#e74c3c;color:#fff;font-size:0.65rem;font-weight:700;padding:1px 7px;border-radius:10px;margin-left:6px;">QUÁ HẠN</span>' if is_over else ""
            nv_hk = row["Nhân viên HK"] if row["Nhân viên HK"] else "⚠️ Chưa giao"

            st.markdown(f'''
            <div style="background:#2A2618;border:1px solid {tc}44;border-left:4px solid {tc};
                        border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                    <div>
                        <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                            <span style="color:#C9A84C;font-size:0.72rem;font-weight:600;">{row["Mã HK"]}</span>
                            <span style="color:#FAF6EE88;font-size:0.72rem;">({row["Mã HĐ"]})</span>
                            <span style="background:{tc}22;color:{tc};font-size:0.65rem;padding:1px 8px;border-radius:10px;">{tt}</span>
                            {over_badge}
                        </div>
                        <div style="font-size:0.92rem;color:#FAF6EE;font-weight:700;">{row["Khách hàng"]}</div>
                        <div style="font-size:0.75rem;color:#E8D08A;margin-top:2px;">🎨 {row["Loại"]} &nbsp;|&nbsp; 👤 {nv_hk}</div>
                        <div style="font-size:0.72rem;color:#FAF6EE66;margin-top:2px;">{row["Ghi chú"]}</div>
                    </div>
                    <div style="text-align:right;font-size:0.78rem;">
                        <div style="color:#FAF6EE88;">Ngày giao: <b style="color:#FAF6EE;">{row["Ngày giao"] or "—"}</b></div>
                        <div style="color:{"#e74c3c" if is_over else "#C9A84C"};font-weight:700;">Hẹn trả: {row["Ngày hẹn trả"]}</div>
                    </div>
                </div>
            </div>''', unsafe_allow_html=True)

        # Cập nhật trạng thái
        st.markdown("---")
        st.markdown("**🔄 Cập nhật tiến độ hậu kỳ**")
        ma_list = df["Mã HK"].tolist()
        with st.form("form_update_hk"):
            c1,c2,c3 = st.columns(3)
            with c1: chon_hk = st.selectbox("Mã HK", ma_list)
            with c2:
                row_hk = df[df["Mã HK"]==chon_hk].iloc[0]
                new_tt = st.selectbox("Trạng thái mới", ["Chưa giao","Chờ xử lý","Đang làm","Hoàn thành"],
                    index=["Chưa giao","Chờ xử lý","Đang làm","Hoàn thành"].index(row_hk["Trạng thái HK"]) if row_hk["Trạng thái HK"] in ["Chưa giao","Chờ xử lý","Đang làm","Hoàn thành"] else 0)
            with c3: new_nv = st.text_input("Nhân viên HK", value=str(row_hk["Nhân viên HK"]))
            if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                mask = st.session_state.df_hauky["Mã HK"]==chon_hk
                st.session_state.df_hauky.loc[mask,"Trạng thái HK"]  = new_tt
                st.session_state.df_hauky.loc[mask,"Nhân viên HK"]   = new_nv
                if not row_hk["Ngày giao"] and new_tt != "Chưa giao":
                    st.session_state.df_hauky.loc[mask,"Ngày giao"] = today_str
                st.success("✅ Đã cập nhật!"); st.rerun()

    with tab2:
        customers = st.session_state.df_hopdong["Khách hàng"].tolist()
        hd_list   = st.session_state.df_hopdong["Mã HĐ"].tolist()
        with st.form("form_add_hk"):
            c1,c2 = st.columns(2)
            with c1:
                kh_hk    = st.selectbox("👤 Khách hàng", customers)
                ma_hd_hk = st.selectbox("Mã hợp đồng", hd_list)
                loai_hk  = st.selectbox("🎨 Loại công việc", ["Chỉnh sửa album","Video slide","Album in","Video highlight","Ảnh đơn"])
                nv_hk2   = st.text_input("Nhân viên hậu kỳ")
            with c2:
                ngay_htra = st.date_input("📅 Ngày hẹn trả", min_value=date.today(), value=date.today()+timedelta(days=30))
                gc_hk     = st.text_area("📝 Ghi chú", height=80)
            ma_hk = f"HK{len(df)+1:03d}"
            tt_hk = "Chờ xử lý" if nv_hk2 else "Chưa giao"
            if st.form_submit_button("✅ Giao việc hậu kỳ", use_container_width=True):
                new_row = {"Mã HK":ma_hk,"Khách hàng":kh_hk,"Mã HĐ":ma_hd_hk,
                           "Loại":loai_hk,"Nhân viên HK":nv_hk2,
                           "Ngày giao":today_str if nv_hk2 else "",
                           "Ngày hẹn trả":str(ngay_htra),
                           "Trạng thái HK":tt_hk,"Ghi chú":gc_hk}
                st.session_state.df_hauky = pd.concat(
                    [st.session_state.df_hauky, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ Đã giao việc hậu kỳ {loai_hk} cho {kh_hk}"); st.rerun()



# ============================================================
# MAIN ROUTER
# ============================================================
if not st.session_state.logged_in:
    show_login()
else:
    selected = show_sidebar()
    page_map = {
        "🏠 Tổng quan":             page_dashboard,
        "📋 Hợp đồng":              page_hopdong,
        "🗓️ Lịch hẹn":              page_lichhens,
        "💄 Makeup":                page_makeup,
        "🎨 Hậu kỳ":               page_hauky,
        "👥 Khách hàng & Tiến độ":  page_customers,
        "📅 Lịch làm việc":         page_schedule,
        "👗 Kho váy cưới":          page_vay,
        "🥻 Kho áo dài":            page_aodai,
        "👔 Kho Suit":              page_suit,
        "📦 Giao nhận đồ":          page_borrow,
        "💰 Thu Chi":               page_thu_chi,
        "💵 Tính Lương":            page_luong,
        "📊 Thuế & Báo cáo":        page_thue,
        "⚙️ Quản lý nhân sự":       page_personnel,
    }
    fn = page_map.get(selected)
    if fn: fn()
