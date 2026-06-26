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
MASTER_USERNAME = "0965758883"
MASTER_PASSWORD = "Tun883@"

ROLES = ["Admin", "Lễ tân", "Quản lý kho", "Makeup", "Nhiếp ảnh"]

ROLE_MENUS = {
    "Admin":       ["🏠 Tổng quan", "👥 Khách hàng & Tiến độ", "📅 Lịch làm việc", "👗 Kho váy cưới", "🥻 Kho áo dài", "👔 Kho Suit", "📦 Giao nhận đồ", "⚙️ Quản lý nhân sự"],
    "Lễ tân":      ["🏠 Tổng quan", "👥 Khách hàng & Tiến độ", "📅 Lịch làm việc", "📦 Giao nhận đồ"],
    "Quản lý kho": ["🏠 Tổng quan", "👗 Kho váy cưới", "🥻 Kho áo dài", "👔 Kho Suit", "📦 Giao nhận đồ"],
    "Makeup":      ["🏠 Tổng quan", "📅 Lịch làm việc"],
    "Nhiếp ảnh":   ["🏠 Tổng quan", "📅 Lịch làm việc"],
}

ROLE_ICONS = {"Admin":"👑","Lễ tân":"🛎️","Quản lý kho":"📦","Makeup":"💄","Nhiếp ảnh":"📷"}

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
            {"Mã lịch":"LV001","Tên khách":"Lê Thị Hồng",   "Loại":"Makeup",  "Nhân viên":"Phạm Thị Hoa","Ngày":"2025-08-05","Giờ":"06:00","Trạng thái":"Hoàn thành"},
            {"Mã lịch":"LV002","Tên khách":"Lê Thị Hồng",   "Loại":"Chụp ảnh","Nhân viên":"Đỗ Văn Ảnh", "Ngày":"2025-08-05","Giờ":"08:00","Trạng thái":"Hoàn thành"},
            {"Mã lịch":"LV003","Tên khách":"Nguyễn Thị Mai","Loại":"Makeup",  "Nhân viên":"Phạm Thị Hoa","Ngày":"2025-08-10","Giờ":"05:30","Trạng thái":"Chờ"},
            {"Mã lịch":"LV004","Tên khách":"Nguyễn Thị Mai","Loại":"Chụp ảnh","Nhân viên":"Đỗ Văn Ảnh", "Ngày":"2025-08-10","Giờ":"07:30","Trạng thái":"Chờ"},
        ])

    if "df_vay" not in st.session_state:
        st.session_state.df_vay = pd.DataFrame([
            {"Mã váy":"V001","Tên váy":"Váy trắng đuôi cá", "Phân loại":"VIP",   "Size":"S","Màu sắc":"Trắng","Trạng thái":"Sẵn sàng",     "Ghi chú":""},
            {"Mã váy":"V002","Tên váy":"Váy bồng công chúa","Phân loại":"Luxury","Size":"M","Màu sắc":"Trắng","Trạng thái":"Đang cho mượn","Ghi chú":"KH003"},
            {"Mã váy":"V003","Tên váy":"Váy suông tối giản","Phân loại":"Basic", "Size":"L","Màu sắc":"Kem",  "Trạng thái":"Sẵn sàng",     "Ghi chú":""},
            {"Mã váy":"V004","Tên váy":"Váy ren hoa nổi",   "Phân loại":"VIP",   "Size":"S","Màu sắc":"Trắng","Trạng thái":"Đang giặt là",  "Ghi chú":""},
            {"Mã váy":"V005","Tên váy":"Váy cúp ngực đơn",  "Phân loại":"Basic", "Size":"M","Màu sắc":"Trắng","Trạng thái":"Sẵn sàng",     "Ghi chú":""},
        ])

    if "df_aodai" not in st.session_state:
        st.session_state.df_aodai = pd.DataFrame([
            {"Mã áo":"AD001","Tên áo":"Áo dài đỏ cặp đôi",   "Loại":"Áo dài cặp dâu rể","Cấp độ":"VIP",   "Size":"S/M","Trạng thái":"Sẵn sàng"},
            {"Mã áo":"AD002","Tên áo":"Áo dài vàng bê lễ",   "Loại":"Áo dài bê lễ",     "Cấp độ":"Basic", "Size":"M",  "Trạng thái":"Đang cho mượn"},
            {"Mã áo":"AD003","Tên áo":"Áo dài hồng bê lễ",   "Loại":"Áo dài bê lễ",     "Cấp độ":"Basic", "Size":"S",  "Trạng thái":"Sẵn sàng"},
            {"Mã áo":"AD004","Tên áo":"Áo dài luxury cặp đôi","Loại":"Áo dài cặp dâu rể","Cấp độ":"Luxury","Size":"S/L","Trạng thái":"Sẵn sàng"},
        ])

    if "df_suit" not in st.session_state:
        st.session_state.df_suit = pd.DataFrame([
            {"Mã suit":"S001","Tên suit":"Suit đen classic", "Cấp độ":"VIP",   "Size":"M","Phụ kiện":"Nơ, Đồ cài",        "Trạng thái":"Sẵn sàng"},
            {"Mã suit":"S002","Tên suit":"Suit xanh navy",   "Cấp độ":"Basic", "Size":"L","Phụ kiện":"Caravat",            "Trạng thái":"Đang cho mượn"},
            {"Mã suit":"S003","Tên suit":"Suit trắng luxury","Cấp độ":"Luxury","Size":"M","Phụ kiện":"Nơ, Caravat, Đồ cài","Trạng thái":"Sẵn sàng"},
            {"Mã suit":"S004","Tên suit":"Suit xám basic",   "Cấp độ":"Basic", "Size":"S","Phụ kiện":"Nơ",                 "Trạng thái":"Đang giặt là"},
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
            username = st.text_input("📱 Số điện thoại / Tên đăng nhập", placeholder="0965758883")
            password = st.text_input("🔑 Mật khẩu", type="password", placeholder="••••••••")
            role     = st.selectbox("👤 Vai trò", ROLES)
            submitted = st.form_submit_button("✨ Đăng nhập", use_container_width=True)
            if submitted:
                if username == MASTER_USERNAME and password == MASTER_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.user = {"username": username, "role": role, "name": f"{role} - TuanHoa Wedding"}
                    st.rerun()
                else:
                    st.error("❌ Sai thông tin đăng nhập!")

        st.markdown(f"""
        <div style="background:#2A2618;border:1px solid #C9A84C33;border-radius:8px;
                    padding:12px 16px;margin-top:10px;font-size:0.78rem;color:#FAF6EE99;text-align:center;">
            <span style="color:#C9A84C;font-weight:600;">Thông tin đăng nhập:</span><br>
            SĐT: <b style="color:#E8D08A;">0965758883</b> &nbsp;|&nbsp; Chọn vai trò tương ứng
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
    st.sidebar.markdown(f"""
    <div style="text-align:center;padding:0;">
    <div style="background:rgba(201,168,76,0.1);border:1px solid #C9A84C44;border-radius:10px;
                padding:10px;margin:8px 0 14px;text-align:center;">
        <div style="font-size:1.4rem;">{icon}</div>
        <div style="font-weight:700;font-size:0.9rem;color:#FAF6EE;">{user["role"]}</div>
        <div style="font-size:0.72rem;color:#C9A84C;margin-top:2px;">TUANHOA WEDDING</div>
    </div>
    """, unsafe_allow_html=True)

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
    tab1, tab2 = st.tabs(["📋 Danh sách lịch", "➕ Giao việc mới"])

    with tab1:
        if user["role"] == "Makeup":
            df_show = df[df["Loại"]=="Makeup"]
            st.info("💄 Hiển thị lịch Makeup")
        elif user["role"] == "Nhiếp ảnh":
            df_show = df[df["Loại"]=="Chụp ảnh"]
            st.info("📷 Hiển thị lịch Chụp ảnh")
        else:
            c1,c2 = st.columns(2)
            with c1: lf = st.selectbox("Lọc loại",["Tất cả","Makeup","Chụp ảnh"])
            with c2: tf = st.selectbox("Lọc trạng thái",["Tất cả","Chờ","Hoàn thành","Hủy"])
            df_show = df.copy()
            if lf!="Tất cả": df_show=df_show[df_show["Loại"]==lf]
            if tf!="Tất cả": df_show=df_show[df_show["Trạng thái"]==tf]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

    with tab2:
        if user["role"] in ["Admin","Lễ tân"]:
            customers = st.session_state.df_customers["Tên khách"].tolist()
            with st.form("form_add_schedule"):
                c1,c2 = st.columns(2)
                with c1:
                    ten_kh   = st.selectbox("Tên khách", customers)
                    loai     = st.selectbox("Loại công việc",["Makeup","Chụp ảnh"])
                    nhan_vien = st.text_input("Nhân viên thực hiện")
                with c2:
                    ngay_lv = st.date_input("Ngày làm việc", min_value=date.today())
                    gio_lv  = st.time_input("Giờ bắt đầu", value=datetime.strptime("07:00","%H:%M").time())
                ma_lv = f"LV{len(st.session_state.df_schedule)+1:03d}"
                if st.form_submit_button("📅 Giao việc", use_container_width=True):
                    new_row = {"Mã lịch":ma_lv,"Tên khách":ten_kh,"Loại":loai,
                               "Nhân viên":nhan_vien,"Ngày":str(ngay_lv),
                               "Giờ":gio_lv.strftime("%H:%M"),"Trạng thái":"Chờ"}
                    st.session_state.df_schedule = pd.concat(
                        [st.session_state.df_schedule, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"✅ Đã giao việc {loai} cho {nhan_vien}"); st.rerun()
        else:
            st.info("⚠️ Chức năng giao việc chỉ dành cho Admin hoặc Lễ tân.")

# ============================================================
# TRANG: KHO VÁY CƯỚI
# ============================================================
def page_vay():
    st.markdown('<div class="section-header">👗 Kho Váy Cưới</div>', unsafe_allow_html=True)
    df   = st.session_state.df_vay
    tab1,tab2 = st.tabs(["📋 Danh sách váy","➕ Thêm / Cập nhật"])

    with tab1:
        c1,c2 = st.columns(2)
        with c1: pl = st.selectbox("Phân loại",["Tất cả","Basic","VIP","Luxury"])
        with c2: ttf= st.selectbox("Trạng thái",["Tất cả","Sẵn sàng","Đang cho mượn","Đang giặt là"])
        df_show = df.copy()
        if pl !="Tất cả": df_show=df_show[df_show["Phân loại"]==pl]
        if ttf!="Tất cả": df_show=df_show[df_show["Trạng thái"]==ttf]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Sẵn sàng",     len(df[df["Trạng thái"]=="Sẵn sàng"]))
        with c2: st.metric("Đang cho mượn",len(df[df["Trạng thái"]=="Đang cho mượn"]))
        with c3: st.metric("Đang giặt là", len(df[df["Trạng thái"]=="Đang giặt là"]))

    with tab2:
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("**➕ Thêm váy mới**")
            with st.form("form_add_vay"):
                ma_vay  = st.text_input("Mã váy", value=f"V{len(df)+1:03d}")
                ten_vay = st.text_input("Tên váy *")
                pl_add  = st.selectbox("Phân loại",["Basic","VIP","Luxury"])
                size    = st.selectbox("Size",["XS","S","M","L","XL","XXL"])
                mau_sac = st.text_input("Màu sắc", value="Trắng")
                gc      = st.text_input("Ghi chú")
                if st.form_submit_button("✅ Thêm váy", use_container_width=True):
                    if ten_vay:
                        new_row={"Mã váy":ma_vay,"Tên váy":ten_vay,"Phân loại":pl_add,
                                 "Size":size,"Màu sắc":mau_sac,"Trạng thái":"Sẵn sàng","Ghi chú":gc}
                        st.session_state.df_vay = pd.concat(
                            [st.session_state.df_vay,pd.DataFrame([new_row])],ignore_index=True)
                        st.success("✅ Đã thêm!"); st.rerun()
        with c2:
            st.markdown("**🔄 Cập nhật trạng thái**")
            with st.form("form_update_vay"):
                ma_list=st.session_state.df_vay["Mã váy"].tolist()
                chon   =st.selectbox("Chọn Mã váy",ma_list)
                row    =st.session_state.df_vay[st.session_state.df_vay["Mã váy"]==chon].iloc[0]
                st.info(f"**{row['Tên váy']}** | {row['Phân loại']} | Hiện: {row['Trạng thái']}")
                new_tt =st.selectbox("Trạng thái mới",["Sẵn sàng","Đang cho mượn","Đang giặt là"])
                new_gc =st.text_input("Ghi chú", value=row["Ghi chú"])
                if st.form_submit_button("💾 Cập nhật", use_container_width=True):
                    mask=st.session_state.df_vay["Mã váy"]==chon
                    st.session_state.df_vay.loc[mask,"Trạng thái"]=new_tt
                    st.session_state.df_vay.loc[mask,"Ghi chú"]   =new_gc
                    st.success("✅ Đã cập nhật!"); st.rerun()

# ============================================================
# TRANG: KHO ÁO DÀI
# ============================================================
def page_aodai():
    st.markdown('<div class="section-header">🥻 Kho Áo Dài</div>', unsafe_allow_html=True)
    df   = st.session_state.df_aodai
    tab1,tab2 = st.tabs(["📋 Danh sách áo dài","➕ Thêm / Cập nhật"])

    with tab1:
        c1,c2=st.columns(2)
        with c1: lf=st.selectbox("Loại",["Tất cả","Áo dài cặp dâu rể","Áo dài bê lễ"])
        with c2: cf=st.selectbox("Cấp độ",["Tất cả","Basic","VIP","Luxury"])
        df_show=df.copy()
        if lf!="Tất cả": df_show=df_show[df_show["Loại"]==lf]
        if cf!="Tất cả": df_show=df_show[df_show["Cấp độ"]==cf]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

    with tab2:
        c1,c2=st.columns(2)
        with c1:
            st.markdown("**➕ Thêm áo dài mới**")
            with st.form("form_add_aodai"):
                ma_ao   =st.text_input("Mã áo",value=f"AD{len(df)+1:03d}")
                ten_ao  =st.text_input("Tên áo *")
                loai_add=st.selectbox("Loại",["Áo dài cặp dâu rể","Áo dài bê lễ"])
                cap_do  =st.selectbox("Cấp độ",["Basic","VIP","Luxury"])
                size    =st.text_input("Size",value="M")
                if st.form_submit_button("✅ Thêm",use_container_width=True):
                    if ten_ao:
                        new_row={"Mã áo":ma_ao,"Tên áo":ten_ao,"Loại":loai_add,
                                 "Cấp độ":cap_do,"Size":size,"Trạng thái":"Sẵn sàng"}
                        st.session_state.df_aodai=pd.concat(
                            [st.session_state.df_aodai,pd.DataFrame([new_row])],ignore_index=True)
                        st.success("✅ Đã thêm!"); st.rerun()
        with c2:
            st.markdown("**🔄 Cập nhật trạng thái**")
            with st.form("form_update_aodai"):
                ma_list=st.session_state.df_aodai["Mã áo"].tolist()
                chon   =st.selectbox("Chọn Mã áo",ma_list)
                row    =st.session_state.df_aodai[st.session_state.df_aodai["Mã áo"]==chon].iloc[0]
                st.info(f"**{row['Tên áo']}** | {row['Loại']} | Hiện: {row['Trạng thái']}")
                new_tt =st.selectbox("Trạng thái mới",["Sẵn sàng","Đang cho mượn","Đang giặt là"])
                if st.form_submit_button("💾 Cập nhật",use_container_width=True):
                    st.session_state.df_aodai.loc[
                        st.session_state.df_aodai["Mã áo"]==chon,"Trạng thái"]=new_tt
                    st.success("✅ Đã cập nhật!"); st.rerun()

# ============================================================
# TRANG: KHO SUIT
# ============================================================
def page_suit():
    st.markdown('<div class="section-header">👔 Kho Suit</div>', unsafe_allow_html=True)
    df   = st.session_state.df_suit
    tab1,tab2=st.tabs(["📋 Danh sách Suit","➕ Thêm / Cập nhật"])

    with tab1:
        cf=st.selectbox("Cấp độ",["Tất cả","Basic","VIP","Luxury"])
        df_show=df if cf=="Tất cả" else df[df["Cấp độ"]==cf]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

    with tab2:
        c1,c2=st.columns(2)
        with c1:
            st.markdown("**➕ Thêm Suit mới**")
            with st.form("form_add_suit"):
                ma_suit =st.text_input("Mã Suit",value=f"S{len(df)+1:03d}")
                ten_suit=st.text_input("Tên Suit *")
                cap_do  =st.selectbox("Cấp độ",["Basic","VIP","Luxury"])
                size    =st.selectbox("Size",["XS","S","M","L","XL"])
                phu_kien=st.multiselect("Phụ kiện đi kèm",["Nơ","Caravat","Đồ cài"])
                if st.form_submit_button("✅ Thêm",use_container_width=True):
                    if ten_suit:
                        new_row={"Mã suit":ma_suit,"Tên suit":ten_suit,"Cấp độ":cap_do,
                                 "Size":size,"Phụ kiện":", ".join(phu_kien),"Trạng thái":"Sẵn sàng"}
                        st.session_state.df_suit=pd.concat(
                            [st.session_state.df_suit,pd.DataFrame([new_row])],ignore_index=True)
                        st.success("✅ Đã thêm!"); st.rerun()
        with c2:
            st.markdown("**🔄 Cập nhật trạng thái**")
            with st.form("form_update_suit"):
                ma_list=st.session_state.df_suit["Mã suit"].tolist()
                chon   =st.selectbox("Chọn Mã Suit",ma_list)
                row    =st.session_state.df_suit[st.session_state.df_suit["Mã suit"]==chon].iloc[0]
                st.info(f"**{row['Tên suit']}** | {row['Cấp độ']} | Hiện: {row['Trạng thái']}")
                new_tt =st.selectbox("Trạng thái mới",["Sẵn sàng","Đang cho mượn","Đang giặt là"])
                if st.form_submit_button("💾 Cập nhật",use_container_width=True):
                    st.session_state.df_suit.loc[
                        st.session_state.df_suit["Mã suit"]==chon,"Trạng thái"]=new_tt
                    st.success("✅ Đã cập nhật!"); st.rerun()

# ============================================================
# TRANG: GIAO NHẬN ĐỒ
# ============================================================
def page_borrow():
    st.markdown('<div class="section-header">📦 Quản lý Giao nhận đồ</div>', unsafe_allow_html=True)
    df   = st.session_state.df_borrow
    tab1,tab2=st.tabs(["📋 Danh sách","➕ Ghi nhận giao/nhận"])

    with tab1:
        ttf=st.selectbox("Lọc trạng thái",["Tất cả","Đã giao","Đã trả"])
        df_show=df if ttf=="Tất cả" else df[df["Trạng thái"]==ttf]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        if ttf=="Đã giao" and len(df_show)>0:
            st.warning(f"⚠️ Có **{len(df_show)}** mặt hàng chưa hoàn trả!")

        st.markdown("**🔄 Xác nhận hoàn trả**")
        chua_tra=df[df["Trạng thái"]=="Đã giao"]["Mã GN"].tolist()
        if chua_tra:
            with st.form("form_return"):
                chon_gn=st.selectbox("Mã giao nhận",chua_tra)
                row_gn =df[df["Mã GN"]==chon_gn].iloc[0]
                st.info(f"**{row_gn['Tên khách']}** | {row_gn['Mã trang phục']} | Hẹn trả: {row_gn['Ngày hẹn trả']}")
                if st.form_submit_button("✅ Xác nhận đã trả",use_container_width=True):
                    st.session_state.df_borrow.loc[df["Mã GN"]==chon_gn,"Trạng thái"]="Đã trả"
                    st.success("✅ Đã xác nhận!"); st.rerun()
        else:
            st.info("✅ Không có mặt hàng nào cần hoàn trả.")

    with tab2:
        all_tp=(
            st.session_state.df_vay[st.session_state.df_vay["Trạng thái"]=="Sẵn sàng"]["Mã váy"].tolist()+
            st.session_state.df_aodai[st.session_state.df_aodai["Trạng thái"]=="Sẵn sàng"]["Mã áo"].tolist()+
            st.session_state.df_suit[st.session_state.df_suit["Trạng thái"]=="Sẵn sàng"]["Mã suit"].tolist()
        )
        customers=st.session_state.df_customers["Tên khách"].tolist()
        with st.form("form_add_borrow"):
            c1,c2=st.columns(2)
            with c1:
                ten_kh =st.selectbox("Tên khách hàng",customers)
                ma_tp  =st.selectbox("Mã trang phục (sẵn sàng)",all_tp if all_tp else ["Không có"])
                loai_tp=st.selectbox("Loại",["Váy cưới","Áo dài","Suit"])
            with c2:
                ngay_muon=st.date_input("Ngày mượn",value=date.today())
                ngay_tra =st.date_input("Ngày hẹn trả",value=date.today()+timedelta(days=2))
            ma_gn=f"GN{len(df)+1:03d}"
            if st.form_submit_button("📦 Ghi nhận giao đồ",use_container_width=True):
                if all_tp:
                    new_row={"Mã GN":ma_gn,"Tên khách":ten_kh,"Mã trang phục":ma_tp,
                             "Loại":loai_tp,"Ngày mượn":str(ngay_muon),
                             "Ngày hẹn trả":str(ngay_tra),"Trạng thái":"Đã giao"}
                    st.session_state.df_borrow=pd.concat(
                        [st.session_state.df_borrow,pd.DataFrame([new_row])],ignore_index=True)
                    for ds_key,col in [("df_vay","Mã váy"),("df_aodai","Mã áo"),("df_suit","Mã suit")]:
                        mask=st.session_state[ds_key][col]==ma_tp
                        if mask.any():
                            st.session_state[ds_key].loc[mask,"Trạng thái"]="Đang cho mượn"
                    st.success(f"✅ Đã ghi nhận giao {ma_tp} cho {ten_kh}"); st.rerun()
                else:
                    st.error("Không có trang phục sẵn sàng!")

# ============================================================
# TRANG: NHÂN SỰ
# ============================================================
def page_personnel():
    st.markdown('<div class="section-header">⚙️ Quản lý Nhân sự</div>', unsafe_allow_html=True)
    st.info("💡 Hệ thống dùng 1 tài khoản chung **0965758883** — phân quyền qua lựa chọn vai trò khi đăng nhập.")
    data=[{"Vai trò":r,"Quyền truy cập":", ".join([m.split(" ",1)[1] for m in ROLE_MENUS[r]])} for r in ROLES]
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="background:#2A2618;border:1px solid #C9A84C44;border-radius:10px;padding:16px;margin-top:16px;">
        <div style="color:#C9A84C;font-weight:700;margin-bottom:8px;">📋 Thông tin hệ thống</div>
        <div style="color:#FAF6EE;font-size:0.88rem;line-height:1.8;">
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
