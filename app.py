import streamlit as st
import pandas as pd
import re
import base64
from io import BytesIO
from pathlib import Path

LOGO_DATA_URI = (
    "data:image/png;base64,"
    + base64.b64encode(Path(__file__).with_name("logo.png").read_bytes()).decode("ascii")
)

OG_IMAGE_URL = "https://raw.githubusercontent.com/realestateruby-sketch/Foreclosure_Prep/main/logo.png"
OG_SITE_URL = "https://foreclosureprep-production.up.railway.app/"
OG_TITLE = "Foreclosure Prep"
OG_DESCRIPTION = (
    "Better data, faster decisions. Built for agents, investors, and "
    "negotiators who work foreclosures."
)


def _patch_streamlit_index_for_og() -> None:
    """Inject Open Graph + Twitter Card meta tags into Streamlit's index.html.

    Streamlit serves a single static index.html for every route. We patch it
    once at container startup so link-preview bots (Telegram, iMessage, Slack,
    etc.) see proper OG tags instead of the bare default. Idempotent.
    """
    try:
        import streamlit as _st_module
        index_path = Path(_st_module.__file__).parent / "static" / "index.html"
        if not index_path.exists():
            return
        html = index_path.read_text(encoding="utf-8")
        if 'property="og:title"' in html:
            return
        og_block = (
            f'    <meta property="og:title" content="{OG_TITLE}" />\n'
            f'    <meta property="og:description" content="{OG_DESCRIPTION}" />\n'
            f'    <meta property="og:image" content="{OG_IMAGE_URL}" />\n'
            f'    <meta property="og:url" content="{OG_SITE_URL}" />\n'
            f'    <meta property="og:type" content="website" />\n'
            f'    <meta name="twitter:card" content="summary_large_image" />\n'
            f'    <meta name="twitter:title" content="{OG_TITLE}" />\n'
            f'    <meta name="twitter:description" content="{OG_DESCRIPTION}" />\n'
            f'    <meta name="twitter:image" content="{OG_IMAGE_URL}" />\n'
        )
        html = html.replace("<head>", "<head>\n" + og_block, 1)
        html = re.sub(r"<title>.*?</title>", f"<title>{OG_TITLE}</title>", html, count=1)
        index_path.write_text(html, encoding="utf-8")
    except Exception:
        pass


_patch_streamlit_index_for_og()

st.set_page_config(
    page_title="Foreclosure Prep",
    page_icon="https://em-content.zobj.net/source/twitter/408/house_1f3e0.png",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Montserrat:wght@800;900&display=swap');

    .stApp {
        background: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        max-width: 900px;
        padding: 2rem 3rem;
        margin: 0 auto;
    }

    .brand-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 20px 0 8px 0;
        position: relative;
    }

    a.brand-link,
    a.brand-link:visited,
    a.brand-link:hover,
    a.brand-link:active {
        display: flex;
        align-items: center;
        gap: 16px;
        text-decoration: none !important;
        cursor: pointer;
    }

    .nav-buttons {
        position: absolute;
        right: 0;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        gap: 12px;
        align-items: center;
    }

    a.nav-btn-login,
    a.nav-btn-login:visited,
    a.nav-btn-login:hover,
    a.nav-btn-login:active {
        font-size: 16px;
        font-weight: 700;
        color: #1A1A2E !important;
        text-decoration: none !important;
        padding: 12px 24px;
        border: none;
        background: none;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
        transition: opacity 0.2s;
    }

    a.nav-btn-login:hover {
        opacity: 0.7;
    }

    a.nav-btn-getstarted,
    a.nav-btn-getstarted:visited,
    a.nav-btn-getstarted:hover,
    a.nav-btn-getstarted:active {
        font-size: 16px;
        font-weight: 800;
        color: white !important;
        padding: 14px 36px;
        border-radius: 14px;
        background: linear-gradient(135deg, #A78BFA, #7C3AED);
        border: none;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none !important;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3);
    }

    a.nav-btn-getstarted:hover {
        background: linear-gradient(135deg, #9B7AEA, #6D28D9);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        transform: translateY(-1px);
    }

    .brand-icon {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        flex-shrink: 0;
        object-fit: cover;
    }

    .brand-name {
        font-size: 32px;
        font-weight: 900;
        font-family: 'Inter', sans-serif;
        line-height: 1.1;
    }

    .brand-name .dark {
        color: #1A1A2E;
    }

    .brand-name .purple {
        color: #7C3AED;
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
    }

    .hero-section {
        text-align: center;
        padding: 40px 0 24px 0;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #7C3AED;
        line-height: 1.15;
        margin-bottom: 16px;
        font-family: 'Montserrat', sans-serif;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #6B7280;
        line-height: 1.7;
        max-width: 640px;
        margin: 0 auto;
    }

    .features-row {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        padding: 24px 0 32px 0;
        max-width: 560px;
        margin: 0 auto;
    }

    .video-placeholder {
        max-width: 640px;
        margin: 32px auto;
        background: linear-gradient(135deg, #F5F3FF, #EDE9FE);
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        aspect-ratio: 16 / 9;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .video-placeholder::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.03), rgba(124, 58, 237, 0.08));
        border-radius: 16px;
    }

    .video-placeholder:hover {
        border-color: #7C3AED;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.12);
        transform: translateY(-2px);
    }

    .video-play-btn {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35);
        position: relative;
        z-index: 1;
    }

    .video-play-btn svg {
        width: 24px;
        height: 24px;
        fill: white;
        margin-left: 3px;
    }

    .video-label {
        font-size: 14px;
        font-weight: 600;
        color: #6B7280;
        position: relative;
        z-index: 1;
    }

    .feature-card {
        text-align: left;
        padding: 24px 20px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        transition: all 0.25s ease;
    }

    .feature-card:hover {
        border-color: #DDD6FE;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.08);
        transform: translateY(-2px);
    }

    .feature-icon {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.2);
    }

    .feature-icon svg {
        width: 22px;
        height: 22px;
        fill: none;
        stroke: white;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .feature-title {
        font-size: 15px;
        font-weight: 700;
        color: #1A1A2E;
        margin-bottom: 8px;
    }

    .feature-desc {
        font-size: 13px;
        color: #6B7280;
        line-height: 1.6;
    }

    .upload-teaser {
        position: relative;
        margin: 8px 0 24px 0;
    }

    .upload-teaser-inner {
        background: #F9FAFB;
        border: 2px dashed #D4D4D8;
        border-radius: 16px;
        padding: 40px 24px;
        text-align: center;
        opacity: 0.6;
    }

    .upload-teaser-icon {
        width: 48px;
        height: 48px;
        background: #E5E7EB;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px auto;
    }

    .upload-teaser-icon svg {
        width: 24px;
        height: 24px;
        stroke: #9CA3AF;
        fill: none;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .upload-teaser-text {
        font-size: 15px;
        font-weight: 600;
        color: #6B7280;
    }

    .upload-teaser-subtext {
        font-size: 13px;
        color: #9CA3AF;
        margin-top: 4px;
    }

    .upload-teaser-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.85) 70%, rgba(255,255,255,1) 100%);
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        padding-bottom: 24px;
    }

    a.teaser-cta-btn,
    a.teaser-cta-btn:visited,
    a.teaser-cta-btn:hover,
    a.teaser-cta-btn:active {
        display: inline-block;
        font-size: 15px;
        font-weight: 800;
        color: white !important;
        padding: 12px 32px;
        border-radius: 14px;
        background: linear-gradient(135deg, #A78BFA, #7C3AED);
        border: none;
        cursor: pointer;
        text-decoration: none !important;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3);
        transition: all 0.2s;
        margin-bottom: 8px;
    }

    a.teaser-cta-btn:hover {
        background: linear-gradient(135deg, #9B7AEA, #6D28D9);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        transform: translateY(-1px);
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #1A1A2E;
        margin-bottom: 8px;
        font-family: 'Inter', sans-serif;
    }

    .section-subtitle {
        font-size: 15px;
        color: #9CA3AF;
        margin-bottom: 20px;
    }

    .results-card {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 28px;
        margin: 20px 0;
    }

    .results-header {
        font-size: 20px;
        font-weight: 700;
        color: #1A1A2E;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .stat-row {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
        flex-wrap: wrap;
    }

    .stat-box {
        flex: 1;
        min-width: 120px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    .stat-value {
        font-size: 28px;
        font-weight: 800;
        color: #7C3AED;
    }

    .stat-label {
        font-size: 13px;
        color: #6B7280;
        margin-top: 4px;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #6D28D9, #5B21B6) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
    }

    .divider {
        height: 1px;
        background: #E5E7EB;
        margin: 32px 0;
    }

    .footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 13px;
        padding: 24px 0 16px 0;
    }
</style>
""", unsafe_allow_html=True)

CHFA_LENDER = "COLO HOUSING FIN AUTHORITY"

DELETE_HEADERS_CONTAINS = [
    "TDD DATE", "TDR", "ERECOMLS", "ATTY", "LEGAL", "REC#", "BK", "PG", "DOC",
    "RECORDING", "Y=IND N=BUS", "PUBLIC TRUSTEE", "PARCEL NO", "OWNER OCC"
]

REQUIRED_COLUMNS = ["Orig Loan Amt", "Loan Amt", "Lender", "Cnty"]

def should_delete_column(col: str) -> bool:
    col_u = str(col).strip().upper()
    if "PROPERTY ADDRESS" in col_u:
        return False
    if "SKLD" in col_u:
        return True
    return any(token in col_u for token in DELETE_HEADERS_CONTAINS)

_money_re = re.compile(r"[^0-9\.\-]")

def parse_money(val):
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = _money_re.sub("", str(val).strip())
    if s in ("", "-", ".", "-."):
        return None
    try:
        return float(s)
    except ValueError:
        return None

def split_borrower_name(df: pd.DataFrame) -> pd.DataFrame:
    borrower_col = None
    for c in df.columns:
        if str(c).strip().upper() in ("BORROWER", "BORROWERS", "BORROWER NAME"):
            borrower_col = c
            break
    if borrower_col is None:
        return df

    first_names = []
    last_names = []
    for val in df[borrower_col]:
        if pd.isna(val) or str(val).strip() == "":
            first_names.append(None)
            last_names.append(None)
            continue
        parts = str(val).strip().split()
        if len(parts) == 1:
            first_names.append(parts[0].title())
            last_names.append(None)
        else:
            first_names.append(parts[0].rstrip(",").title())
            last_names.append(" ".join(parts[1:]).title())

    insert_at = df.columns.get_loc(borrower_col)
    df.drop(columns=[borrower_col], inplace=True)
    df.insert(insert_at, "Last Name", last_names)
    df.insert(insert_at, "First Name", first_names)
    return df

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    drop_cols = [c for c in df.columns if should_delete_column(c)]
    return df.drop(columns=drop_cols, errors="ignore")

def compute_difference_hard_values(
    df: pd.DataFrame,
    orig_col="Orig Loan Amt",
    loan_col="Loan Amt",
    diff_col="Difference"
) -> pd.DataFrame:
    if orig_col not in df.columns or loan_col not in df.columns:
        raise ValueError("Missing Orig Loan Amt and/or Loan Amt columns")

    diffs = []
    for _, row in df.iterrows():
        o = parse_money(row[orig_col])
        l = parse_money(row[loan_col])
        diffs.append((o - l) if (o is not None and l is not None) else None)

    if diff_col in df.columns:
        df[diff_col] = diffs
        return df

    insert_at = df.columns.get_loc(orig_col) + 1
    df.insert(insert_at, diff_col, diffs)
    return df

def extract_chfa(df: pd.DataFrame, lender_col="Lender"):
    if lender_col not in df.columns:
        raise ValueError("Missing Lender column (needed for CHFA split)")
    chfa_df = df[df[lender_col] == CHFA_LENDER].copy()
    main_df = df[df[lender_col] != CHFA_LENDER].copy()
    return main_df, chfa_df

def make_county_tabs(df: pd.DataFrame, county_col="Cnty") -> dict:
    if county_col not in df.columns:
        raise ValueError("Missing Cnty column (needed for county tabs)")
    tabs = {}
    for cnty, grp in df.groupby(county_col, dropna=True):
        if pd.isna(cnty):
            continue
        name = str(cnty).strip()
        if not name:
            continue
        tabs[name[:31]] = grp.copy()
    return tabs

def validate_difference(
    df: pd.DataFrame,
    orig_col="Orig Loan Amt",
    loan_col="Loan Amt",
    diff_col="Difference",
    tol=0.01
) -> int:
    if df is None or df.empty:
        return 0

    bad = 0
    for _, row in df.iterrows():
        o = parse_money(row.get(orig_col))
        l = parse_money(row.get(loan_col))
        d = parse_money(row.get(diff_col))
        if o is None or l is None:
            continue
        expected = o - l
        if d is None or abs(d - expected) > tol:
            bad += 1
    return bad

def write_multi_tab_xlsx(main_df, chfa_df, county_tabs) -> bytes:
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book
        money_fmt = workbook.add_format({"num_format": "$#,##0.00"})
        neg_fmt = workbook.add_format({"num_format": "$#,##0.00", "font_color": "red", "bold": True})

        def format_sheet(sheet_name: str, df: pd.DataFrame):
            ws = writer.sheets[sheet_name]
            ws.freeze_panes(1, 0)

            for i, col in enumerate(df.columns):
                try:
                    max_len = max(df[col].astype(str).map(len).max(), len(str(col)))
                except Exception:
                    max_len = len(str(col))
                ws.set_column(i, i, min(max_len + 2, 50))

            if "Difference" in df.columns:
                idx = df.columns.get_loc("Difference")
                ws.set_column(idx, idx, 14, money_fmt)
                ws.conditional_format(
                    1, idx, len(df), idx,
                    {"type": "cell", "criteria": "<", "value": 0, "format": neg_fmt}
                )

        main_df.to_excel(writer, sheet_name="Main", index=False)
        format_sheet("Main", main_df)

        if chfa_df is not None and not chfa_df.empty:
            chfa_df.to_excel(writer, sheet_name="CHFA", index=False)
            format_sheet("CHFA", chfa_df)

        for name, tab_df in county_tabs.items():
            tab_df.to_excel(writer, sheet_name=name, index=False)
            format_sheet(name, tab_df)

    return output.getvalue()

def run_locked_pipeline(df: pd.DataFrame):
    df = clean_columns(df)
    df = split_borrower_name(df)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df = compute_difference_hard_values(df)
    main_df, chfa_df = extract_chfa(df)
    county_tabs = make_county_tabs(main_df)

    bad = 0
    bad += validate_difference(main_df)
    bad += validate_difference(chfa_df)
    bad += sum(validate_difference(t) for t in county_tabs.values())

    if bad > 0:
        raise RuntimeError(f"Validation failed: {bad} rows have incorrect Difference math.")

    xlsx_bytes = write_multi_tab_xlsx(main_df, chfa_df, county_tabs)
    return xlsx_bytes, main_df, chfa_df, county_tabs

if "page" not in st.session_state:
    st.session_state.page = "home"

params = st.query_params
if params.get("page") == "getstarted":
    st.session_state.page = "getstarted"

def render_header():
    st.markdown(f"""
    <div class="brand-header">
        <a class="brand-link" href="?page=home">
            <img class="brand-icon" src="{LOGO_DATA_URI}" alt="Foreclosure Prep" />
            <div class="brand-name">
                <span class="dark">Foreclosure </span><span class="purple">Prep</span>
            </div>
        </a>
        <div class="nav-buttons">
            <a class="nav-btn-login" href="?page=home">Log in</a>
            <a class="nav-btn-getstarted" href="?page=getstarted">Get Started</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_home():
    render_header()

    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Stop Managing Spreadsheets.<br>Start Closing Deals.</div>
        <div class="hero-subtitle">
            Upload any foreclosure list and get a clean, organized workbook back in seconds.
            Then go deeper — pull live, county-level foreclosure records directly from the public
            trustee or attorney's office for any state in the U.S. And for your best leads,
            generate a full investment analysis and seller net sheet so you walk into every
            conversation knowing exactly what the numbers say.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="video-placeholder">
        <div class="video-play-btn">
            <svg viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21" fill="white"/></svg>
        </div>
        <div class="video-label">See how it works</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="features-row">
        <div class="feature-card">
            <div class="feature-icon">
                <svg viewBox="0 0 24 24"><path d="M3 6h18"/><path d="M3 12h12"/><path d="M3 18h8"/><path d="M19 15l-3 3 3 3"/></svg>
            </div>
            <div class="feature-title">Smart Column Cleanup</div>
            <div class="feature-desc">Automatically strips out unnecessary columns and keeps only the data you actually need for analysis and outreach.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">
                <svg viewBox="0 0 24 24"><path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/><circle cx="8" cy="7" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="10" cy="17" r="2"/></svg>
            </div>
            <div class="feature-title">Loan Type Organization</div>
            <div class="feature-desc">Identifies and categorizes loans by type so each loan type is sorted and easy to work through.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">
                <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
            </div>
            <div class="feature-title">County-Level Tabs</div>
            <div class="feature-desc">Breaks your master list into individual tabs for each county, labeled and ready to go — no more manual sorting.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">
                <svg viewBox="0 0 24 24"><path d="M12 2v20"/><path d="M2 12h20"/><path d="M6 6l-4 6h8"/><path d="M18 18l4-6h-8"/></svg>
            </div>
            <div class="feature-title">Equity at a Glance</div>
            <div class="feature-desc">Compares original and current loan amounts to calculate the difference — underwater homes are flagged in red so you see them instantly.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">Upload Your NED File</div>
    <div class="section-subtitle">Drop your weekly foreclosure Excel file below to get started.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-teaser">
        <div class="upload-teaser-inner">
            <div class="upload-teaser-icon">
                <svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            </div>
            <div class="upload-teaser-text">Drag and drop file here</div>
            <div class="upload-teaser-subtext">Limit 200MB per file &bull; XLSX</div>
        </div>
        <div class="upload-teaser-overlay">
            <a class="teaser-cta-btn" href="?page=getstarted">Get Started to Upload Your File</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Foreclosure Prep &mdash; Built for real estate professionals nationwide.
    </div>
    """, unsafe_allow_html=True)

def render_getstarted():
    render_header()

    st.markdown("""
    <div style="padding: 24px 0 8px 0;">
        <div class="section-title">Upload Your NED File</div>
        <div class="section-subtitle">Drop your weekly foreclosure Excel file below to get started.</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Excel file", type=["xlsx"], label_visibility="collapsed")

    if uploaded:
        try:
            df = pd.read_excel(uploaded)

            with st.spinner("Processing your file..."):
                xlsx_bytes, main_df, chfa_df, county_tabs = run_locked_pipeline(df)

            chfa_count = 0 if chfa_df is None else len(chfa_df)
            county_count = len(county_tabs)

            st.markdown(f"""
            <div class="results-card">
                <div class="results-header">Processing Complete</div>
                <div class="stat-row">
                    <div class="stat-box">
                        <div class="stat-value">{len(main_df)}</div>
                        <div class="stat-label">Main Rows</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{chfa_count}</div>
                        <div class="stat-label">CHFA Rows</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{county_count}</div>
                        <div class="stat-label">County Tabs</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            original_name = uploaded.name.rsplit('.', 1)[0]
            download_name = f"{original_name}_cleaned.xlsx"

            st.download_button(
                label="Download Cleaned File",
                data=xlsx_bytes,
                file_name=download_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            with st.expander("Preview (first 25 rows of Main)"):
                st.dataframe(main_df.head(25), use_container_width=True)

        except Exception as e:
            st.error("Processing failed.")
            st.code(str(e))
            st.stop()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Foreclosure Prep &mdash; Built for real estate professionals nationwide.
    </div>
    """, unsafe_allow_html=True)

page = params.get("page", "home")
if page == "getstarted":
    render_getstarted()
else:
    render_home()
    