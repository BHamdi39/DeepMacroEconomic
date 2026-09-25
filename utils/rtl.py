"""أدوات العرض بالعربية RTL + نظام التصميم الموحّد للمختبر.

التصميم: داكن أكاديمي منخفض الضجيج مستوحى من style.jpg — خط عربي واحد
(IBM Plex Sans Arabic) وخط لاتيني للأرقام (Inter) وخط وحيد المسافة
(JetBrains Mono)، وسلم تصويري، وألوان: خلفية داكنة، أبيض، توازيًل
واحد تُحجز للأدوات التفاعلية/التقدّم فقط.

الخطوط محزّمة محليًا في pwa/fonts (تعمل دون إنترنت عبر قشرة PWA على :8000)
مع سقوط إلى الخطوط النظامية عند التشغيل المباشر على :8508.

الوضع الحالي يُحلّ عبر: جلسة المستخدم ← معامل ?theme= في الرابط ← داكن افتراضيًا.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# لوحات الألوان (داكن افتراضيًا). الأرقام الغربية 0-9 في كل الواجهة.
# ---------------------------------------------------------------------------
THEMES: dict[str, dict[str, str]] = {
    "dark": {
        # أسطح
        "bg": "#0E1117",
        "surface": "#161B22",
        "surface_hover": "#1E242C",
        "panel": "#12181F",
        "card": "#161B22",
        "border": "#2A3038",
        # نصوص
        "text": "#F5F6F7",
        "muted": "#9CA3AF",
        # تباين
        "accent": "#5FD3C4",
        "accent_dark": "#3F9E92",
        "success": "#3FB68F",
        "danger": "#E8766A",
        "warning": "#D9A65C",
        # رسوم وعلامات
        "grid": "#1C242E",
        "zero": "#2A3038",
        "fill": "#153A3E",
        "progress_track": "#252B33",
        # منحنيات اقتصادية (منخفضة التشبّع للوضوح على الداكن)
        "is_curve": "#5FD3C4",
        "lm_curve": "#E8766A",
        "bp_curve": "#7FC9A0",
        "is_prime": "#3FA3C0",
        "lm_prime": "#C26A61",
        "ref": "#6B7D94",
        # بطل الصفحة الرئيسية
        "hero_from": "#15262E",
        "hero_to": "#0E1117",
        # شارات قبل/بعد/الفرق
        "badge_before_bg": "#1D2A3B",
        "badge_before_tx": "#B9C8DD",
        "badge_after_bg": "#2A241A",
        "badge_after_tx": "#EDB979",
        "badge_delta_bg": "#0F2E27",
        "badge_delta_tx": "#7FD9A8",
        # أسطح مبنية كنقاط متدرّجة/طبقات (تتكيف مع الوضع)
        "app_bg": "radial-gradient(circle at top, rgba(28,40,48,0.85), rgba(9,13,18,1) 45%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(16,20,26,0.96), rgba(10,14,18,0.99))",
        "shell_bg": "rgba(12,17,23,0.90)",
        "shell_gradient": "linear-gradient(180deg, rgba(16,20,27,0.94), rgba(11,15,20,0.96))",
        "hover_overlay": "rgba(255,255,255,0.045)",
        "track_bg": "rgba(255,255,255,0.07)",
    },
    "light": {
        "bg": "#F7F9FC",
        "surface": "#FFFFFF",
        "surface_hover": "#EEF2F8",
        "panel": "#F1F5FB",
        "card": "#FFFFFF",
        "border": "#D8E0EC",
        "text": "#182338",
        "muted": "#5B6B84",
        "accent": "#0D8B7A",
        "accent_dark": "#08645A",
        "success": "#1E8E5A",
        "danger": "#C0392B",
        "warning": "#B9770E",
        "grid": "#E3E9F3",
        "zero": "#CBD6E4",
        "fill": "#DFF2EE",
        "progress_track": "#E3E9F3",
        "is_curve": "#0E8C7E",
        "lm_curve": "#C0392B",
        "bp_curve": "#2E8B63",
        "is_prime": "#0A4D99",
        "lm_prime": "#8E1F1A",
        "ref": "#8FA3BF",
        "hero_from": "#DDF2ED",
        "hero_to": "#EEF4FA",
        "badge_before_bg": "#E7EFF8",
        "badge_before_tx": "#2C3E50",
        "badge_after_bg": "#FBF0E2",
        "badge_after_tx": "#B35A12",
        "badge_delta_bg": "#E3F3EA",
        "badge_delta_tx": "#14633A",
        # أسطح مبنية كنقاط متدرّجة/طبقات (تتكيف مع الوضع)
        "app_bg": "radial-gradient(circle at top, rgba(221,230,240,0.82), rgba(247,249,252,1) 45%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(252,253,255,0.99), rgba(236,242,249,1))",
        "shell_bg": "rgba(255,255,255,0.90)",
        "shell_gradient": "linear-gradient(180deg, rgba(255,255,255,0.97), rgba(236,242,249,0.99))",
        "hover_overlay": "rgba(13,27,48,0.06)",
        "track_bg": "rgba(13,27,48,0.08)",
    },
}

COLORS: dict[str, str] = dict(THEMES["dark"])


def current_theme() -> str:
    """يرجع اسم الوضع الحالي: dark افتراضيًا (dark / light)."""
    chosen = st.session_state.get("theme")
    if chosen in THEMES:
        return chosen
    qp = st.query_params.get("theme")
    if qp in THEMES:
        return qp
    return "dark"


def sync_colors() -> str:
    """يطابق ألوان COLORS مع الوضع الحالي ويرجع اسمه (يُستدعى في كل صفحة)."""
    name = current_theme()
    COLORS.clear()
    COLORS.update(THEMES[name])
    return name


def set_theme(dark: bool) -> None:
    """يحفظ اختيار المستخدم في الجلسة وفي الرابط (يعبر إعادة التحميل)."""
    st.session_state["theme"] = "dark" if dark else "light"
    st.query_params["theme"] = st.session_state["theme"]


# ---------------------------------------------------------------------------
# الخطوط (محزّمة محليًا) — سلّم تصويري بحسب متطلبات النظام (قسم 4)
# ---------------------------------------------------------------------------
FONT_AR = "'Cairo', 'Segoe UI', Tahoma, sans-serif"
FONT_LAT = "'Cairo', 'Segoe UI', Arial, sans-serif"
FONT_MONO = "'JetBrains Mono', Consolas, 'Courier New', monospace"
FONT_STACK = (
    "'Cairo', 'Segoe UI', 'Tahoma', Arial, sans-serif"
)
MONO_STACK = "'JetBrains Mono', Consolas, 'Courier New', monospace"

# سلّم الأنواع (rem، أساس 16px): عربي / لاتيني-رقمي
TYPE_SCALE = {
    "h1": ("2.25rem", "2.0rem"),
    "h2": ("1.5rem", "1.375rem"),
    "h3": ("1.125rem", "1.0rem"),
    "body": ("1.0rem", "0.9375rem"),
    "nav": ("0.9375rem", "0.875rem"),
    "cap": ("0.8125rem", "0.75rem"),
    "mono": ("0.875rem", "0.875rem"),
}

_FONT_CSS_PATH = Path(__file__).resolve().parent.parent / "pwa" / "fonts-abs.css"


def _load_font_faces() -> str:
    """يحمّل @font-face الموّلد (روابط مطلقة عبر قشرة PWA :8000)."""
    try:
        return _FONT_CSS_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""


FONT_FACE = _load_font_faces()


def _root_css(theme_name: str) -> str:
    """كتلة الجذر: متغيرات الألوان + سلّم الأنواع للوضع المطلوب."""
    p = THEMES[theme_name]
    h1, h2, h3, body, nav, cap, mono = (v[0] for v in TYPE_SCALE.values())
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');
:root {{
    --bg: {p['bg']};
    --surface: {p['surface']};
    --surface-hover: {p['surface_hover']};
    --panel: {p['panel']};
    --card: {p['card']};
    --border: {p['border']};
    --stroke: {p['border']};
    --text: {p['text']};
    --muted: {p['muted']};
    --accent: {p['accent']};
    --accent-dark: {p['accent_dark']};
    --accent-soft: {p['accent']}1F;
    --accent-line: {p['accent']}55;
    --success: {p['success']};
    --success-soft: {p['success']}1F;
    --danger: {p['danger']};
    --danger-soft: {p['danger']}1F;
    --warning: {p['warning']};
    --grid: {p['grid']};
    --zero: {p['zero']};
    --fill: {p['fill']};
    --progress-track: {p['progress_track']};
    --hero-from: {p['hero_from']};
    --hero-to: {p['hero_to']};
    --bdg-b: {p['badge_before_bg']};
    --bdg-bt: {p['badge_before_tx']};
    --bdg-a: {p['badge_after_bg']};
    --bdg-at: {p['badge_after_tx']};
    --bdg-d: {p['badge_delta_bg']};
    --bdg-dt: {p['badge_delta_tx']};
    /* سلّم الأنواع */
    --t-h1: {h1}; --t-h2: {h2}; --t-h3: {h3};
    --t-body: {body}; --t-nav: {nav}; --t-cap: {cap}; --t-mono: {mono};
    --lh-ar: 1.6; --lh-lat: 1.5;
    --font-ar: {FONT_AR};
    --font-lat: {FONT_LAT};
    --font-mono: {FONT_MONO};
    --ring: {p['accent']}55;
    --shadow: 0 10px 30px rgba(0,0,0,.25);
    --app-bg: {p['app_bg']};
    --sidebar-bg: {p['sidebar_bg']};
    --shell-bg: {p['shell_bg']};
    --shell-grad: {p['shell_gradient']};
    --hover-overlay: {p['hover_overlay']};
    --track-bg: {p['track_bg']};
}}
</style>
"""


CSS_SHARED = f"""
<style>
/* ====== أسس RTL + الخطوط ====== */
html {{ font-size: 16px; }}
html, body, .stApp, [data-testid="stAppViewContainer"] {{
    direction: rtl;
    text-align: right;
    font-family: var(--font-ar);
}}
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"] {{
    background: var(--app-bg);
    color: var(--text);
}}
[data-testid="stHeader"] {{ direction: rtl; background: transparent; }}
[data-testid="stToolbar"] {{ visibility: hidden; }}
[data-testid="stStatusWidget"] {{ visibility: hidden; }}

.stMain, [data-testid="stMainBlockContainer"] {{
    padding-top: 0.25rem;
    background: transparent;
}}
[data-testid="stMainBlockContainer"] > div:first-child {{
    padding-inline: 0.75rem;
}}

h1, h2, h3, h4, h5, p, li, label, .stMarkdown, .stCaption,
.stRadio label, .stCheckbox label, .stSelectbox label, .stSlider label {{
    direction: rtl;
    text-align: right;
    font-family: var(--font-ar);
    color: var(--text);
    line-height: var(--lh-ar);
}}

/* سلّم الأنواع (يتفوّق على استايل العناوين المبني في Streamlit) */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {{
    font-family: var(--font-ar) !important;
    color: var(--text) !important;
    text-align: right;
    direction: rtl;
    letter-spacing: 0;
}}
.stMarkdown h1 {{ font-size: var(--t-h1) !important; font-weight: 700 !important; }}
.stMarkdown h2 {{ font-size: var(--t-h2) !important; font-weight: 700 !important; }}
.stMarkdown h3 {{ font-size: var(--t-h3) !important; font-weight: 600 !important; }}
.stMarkdown h4, .stMarkdown h5 {{ font-size: var(--t-body) !important; font-weight: 600 !important; }}
.body-text, .stMarkdown p {{ font-size: var(--t-body); min-font-size: 14px; }}
.stCaption, caption, .app-caption {{ font-size: var(--t-cap); color: var(--muted); }}

/* الأرقام والصيغ تبقى LTR معزولة داخل الجملة العربية (bidi) */
code, pre, samp, kbd {{
    font-family: var(--font-mono);
    direction: ltr; unicode-bidi: isolate;
    font-size: var(--t-mono);
}}
mjx-container, .MathJax, .katex, [data-testid="stMarkdown"] mjx-container {{
    direction: ltr; unicode-bidi: isolate;
}}
/* حارس التفيض: المعادلات الطويلة تتمرّر أفقياً داخل الصندوق بدل كسر الصفحة */
[data-testid="stLatex"], .stLatex, .math-frame {{
    overflow-x: auto;
    max-width: 100%;
    overscroll-behavior-x: contain;
}}
.ltr, .num {{
    direction: ltr; unicode-bidi: isolate;
    font-family: var(--font-lat);
}}

.stMarkdown a, .stMarkdown a:visited {{
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid var(--accent-line);
}}
.stMarkdown a:hover {{ color: var(--accent-dark); }}

/* علب المحتوى ذات الإطار (الوحدة على البطاقات) */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--shell-grad);
    border: 1px solid var(--border);
    border-radius: 1rem;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
    padding: 0.05rem 0.15rem 0.15rem;
}}

.lesson-shell {{
    background: var(--shell-bg);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 1rem 1.1rem 0.7rem;
    margin-bottom: 1rem;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
}}
.lesson-topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.7rem;
}}
.lesson-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    background: rgba(95,211,196,0.10);
    border: 1px solid rgba(95,211,196,0.25);
    color: var(--accent);
    font-weight: 800;
    font-size: 1rem;
}}
.lesson-kicker {{
    color: var(--muted);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}}
.lesson-title {{
    margin: 0 0 0.8rem 0;
    font-size: clamp(2rem, 3vw, 3rem);
    line-height: 1.25;
    color: var(--text);
    letter-spacing: -0.04em;
    font-weight: 800;
}}
.idea-card {{
    border-inline-start: 4px solid var(--accent);
    background: linear-gradient(90deg, rgba(95,211,196,0.08), rgba(255,255,255,0.02));
    border-radius: 0.85rem;
    padding: 0.9rem 1rem;
    color: var(--text);
    font-size: 1rem;
    line-height: 2;
    margin: 0.2rem 0 0.6rem;
}}
.idea-card b {{ color: var(--accent); }}

/* ====== الشريط الجانبي ====== */
[data-testid="stSidebar"] {{
    direction: rtl;
    background: var(--sidebar-bg);
    border-inline-start: 1px solid var(--border);
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.02);
    width: 290px !important;
    min-width: 290px !important;
    transition: transform 300ms ease;
    z-index: 1000001 !important;
}}
/* عند الطيّ: يُخرج الشريط من تدفق التخطيط (fixed) ويُخفي كليًا حتى يملك المحتوى كامل العرض */
[data-testid="stSidebar"][aria-expanded="false"] {{
    position: fixed !important;
    top: 0 !important;
    bottom: 0 !important;
    left: 100% !important;
    right: auto !important;
    height: auto !important;
    transform: none !important;
    box-shadow: none;
    z-index: 1000001 !important;
}}
[data-testid="stSidebar"][aria-expanded="true"] {{
    transform: translateX(0) !important;
}}
/* رأس الشريط يُعلّى فوق "شريط التطبيق" (stHeader, z 999990) ليظل زرّ الطيّ قابلًا للنقر في الحالتين */
[data-testid="stSidebarHeader"] {{
    position: relative;
    z-index: 1000000;
}}
/* زرّ الطيّ وسهامه مرئي وقابل للنقر دائمًا (Streamlit يُخفيه افتراضيًا عند التمديد) */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] * {{
    visibility: visible !important;
}}
/* عند الطيّ تبقى حبة طفو صغيرة تحمل زرّ الفتح فقط، بلا شريط يغطي حافة المحتوى */
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarHeader"] {{
    position: fixed;
    top: 16px;
    right: 4px;
    left: auto;
    z-index: 1000000;
    background: var(--sidebar-bg);
    border: 1px solid var(--border);
    border-radius: 999px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    padding: 0.2rem 0.15rem;
}}
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stLogoSpacer"] {{
    display: none;
}}
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"],
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarUserContent"],
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarInfoButton"] {{
    visibility: hidden;
}}
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {{
    transform: scaleX(1);
}}
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {{
    transform: scaleX(-1);
    font-family: "Material Symbols Rounded", var(--font-ar) !important;
    font-style: normal;
}}
[data-testid="stSidebar"] *:not([data-testid="stIconMaterial"]) {{
    font-family: var(--font-ar);
}}
[data-testid="stSidebar"] [data-testid="stIconMaterial"] {{
    font-family: "Material Symbols Rounded", var(--font-ar) !important;
    font-style: normal;
}}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] a {{
    color: var(--text);
}}
[data-testid="stSidebar"] [data-testid="stSidebarNavContainer"] {{
    padding: 0.8rem 0.7rem 1rem;
}}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
    background: var(--hover-overlay);
    border-radius: 0.8rem;
}}
[data-testid="stSidebar"] a {{
    text-decoration: none;
    font-size: var(--t-nav);
    font-weight: 500;
    border-radius: 10px;
    transition: background .15s ease, color .15s ease, transform .15s ease;
    padding: 0.45rem 0.6rem !important;
    margin: 0.12rem 0;
    font-family: var(--font-ar);
    color: var(--text);
}}
[data-testid="stSidebar"] a:hover {{ background: var(--hover-overlay); color: var(--text); transform: translateX(-2px); }}
[data-testid="stSidebar"] a[aria-current="page"] {{
    position: relative;
    background: linear-gradient(90deg, rgba(95,211,196,0.12), rgba(95,211,196,0.03));
    color: var(--accent);
    font-weight: 700;
    box-shadow: inset 0 0 0 1px rgba(95,211,196,0.25);
}}
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"] {{
    color: var(--muted);
    font-size: 1rem;
    line-height: 1;
}}
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] [data-testid="stIconMaterial"] {{
    color: var(--accent);
}}

/* ====== رؤوس أقسام القائمة (الوحدات) ====== */
[data-testid="stNavSectionHeader"] {{
    margin: 0.45rem 0 0.2rem;
    padding: 0.45rem 0.6rem;
    border-radius: 0.7rem;
    cursor: pointer;
    user-select: none;
    gap: 0.45rem;
    transition: background .15s ease, border-color .15s ease;
    border: 1px solid transparent;
}}
[data-testid="stNavSectionHeader"]:hover {{ background: var(--hover-overlay); border-color: var(--hover-overlay); }}
[data-testid="stNavSectionHeader"] p {{
    margin: 0;
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--muted);
    line-height: 1.5;
    letter-spacing: 0.02em;
}}
[data-testid="stNavSectionHeader"]:hover p {{ color: var(--text); }}
[data-testid="stNavSectionHeader"] [data-testid="stIconMaterial"] {{
    color: var(--accent);
    font-size: 1.05rem;
    line-height: 1;
    transition: transform .18s ease, color .15s ease;
}}
[data-testid="stNavSectionHeader"]:first-of-type p {{ color: var(--accent); }}

/* قسم مطويّ: تدوير سهم الطيّ (القسم المطويّ يبقى بلا عناصر <li> بعده) */
[data-testid="stNavSectionHeader"]:has(+ [data-testid="stNavSectionHeader"]) [data-testid="stIconMaterial"],
[data-testid="stNavSectionHeader"]:last-child:last-of-type [data-testid="stIconMaterial"] {{
    transform: rotate(180deg);
}}

/* ====== صفوف الدروس داخل القائمة ====== */
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {{
    padding: 0.4rem 0.55rem !important;
    gap: 0.5rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    border-radius: 0.7rem;
}}
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] > div {{
    align-items: center;
}}
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span {{
    font-family: var(--font-ar);
    font-size: 0.95rem;
}}

/* أيقونات Material داخل روابط القائمة */
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"] {{
    font-size: 1.35rem;
    line-height: 1;
    color: var(--muted);
    flex: none;
}}
[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] [data-testid="stIconMaterial"] {{
    color: var(--accent) !important;
}}

/* ====== أشرطة التقدّم (داكن، تدرّج نجاح→تمييز) ====== */
[data-testid="stProgress"] > div {{
    background: var(--progress-track) !important;
    border-radius: 999px;
    overflow: hidden;
}}
[data-testid="stProgress"] [role="progressbar"] {{
    background: linear-gradient(90deg, var(--success), var(--accent)) !important;
    border-radius: 999px;
}}

/* ====== جداول البيانات ====== */
[data-testid="stDataFrame"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.6rem;
    overflow: hidden;
}}

/* بطل الصفحة الرئيسية */
.top-shell {{
    position: relative;
    border: 1px solid var(--border);
    border-radius: 1.2rem;
    background: var(--shell-grad);
    padding: 0.9rem 1.2rem 0.8rem;
    margin-bottom: 1rem;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.015), 0 14px 30px rgba(0,0,0,0.18);
}}
.topbar {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    min-height: 3.2rem;
}}
.topbar-left, .topbar-right {{
    display: flex;
    align-items: center;
}}
.topbar-left {{ justify-content: flex-start; }}
.topbar-right {{ justify-content: flex-end; }}
.topbar-center {{
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}}
.nav-pill {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.48rem 1.05rem;
    border-radius: 999px;
    background: rgba(95,211,196,0.10);
    border: 1px solid rgba(95,211,196,0.25);
    color: var(--accent);
    font-weight: 700;
    font-size: 1.05rem;
    line-height: 1.3;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03);
}}
.page-title {{
    margin: 0;
    font-size: clamp(2.5rem, 4vw, 4.2rem);
    line-height: 1.1;
    letter-spacing: -0.04em;
    color: var(--text);
    font-weight: 800;
    white-space: nowrap;
    text-shadow: 0 0 0 rgba(255,255,255,0);
}}
.theme-toggle {{
    display: inline-flex;
    align-items: center;
    gap: 0.7rem;
    color: var(--text);
    font-weight: 700;
    font-size: 1.05rem;
    direction: rtl;
}}
.toggle-label {{
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 700;
    margin-inline-start: 0.1rem;
}}
.toggle-track {{
    position: relative;
    width: 4rem;
    height: 2.05rem;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(95,211,196,0.24), rgba(95,211,196,0.12));
    border: 1px solid rgba(95,211,196,0.35);
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
    display: inline-flex;
    align-items: center;
    padding: 0.15rem;
}}
.toggle-thumb {{
    position: absolute;
    inset-inline-start: 0.25rem;
    width: 1.45rem;
    height: 1.45rem;
    border-radius: 50%;
    background: linear-gradient(180deg, #F7E7A7, #F0C85F);
    box-shadow: 0 0 12px rgba(245,215,131,0.8);
    border: 1px solid rgba(255,255,255,0.3);
}}
.toggle-icon {{
    font-size: 1.7rem;
    color: #F5D783;
    line-height: 1;
    transform: translateY(-1px);
    filter: drop-shadow(0 0 8px rgba(245,215,131,0.45));
}}
.hero-panel {{
    position: relative;
    overflow: hidden;
    background: var(--shell-bg);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 1.2rem 1rem 0.9rem;
    text-align: center;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
}}
.hero-panel::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(95,211,196,0.13), transparent 50%);
    pointer-events: none;
}}
.hero-panel .hero-sub {{
    position: relative;
    z-index: 1;
    color: var(--muted);
    margin: 0 auto;
    max-width: 60rem;
    font-size: 1.15rem;
    line-height: 2;
    font-weight: 500;
}}
.hero-panel .hero-sub b {{
    color: var(--accent);
}}
.hero-chips {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.6rem;
    margin-top: 1rem;
}}
.hero-chips .nav-pill {{
    font-size: 0.92rem;
    font-weight: 600;
    padding: 0.35rem 0.95rem;
}}
@media (max-width: 900px) {{
    .topbar {{ grid-template-columns: 1fr; text-align: center; }}
    .page-title {{ white-space: normal; }}
    .topbar-left, .topbar-right, .topbar-center {{ justify-content: center; }}
}}

/* ====== الجوال (<768px): قائمة جانبية بالنظام الأصلي (هامبورغر) + تخطيط مضغوط ====== */
@media (max-width: 767px) {{
    /* نخفي حبة الطفو فنعتمد هامبورغر Streamlit الأصلي (يخفيه إخفاء stToolbar) */
    [data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarHeader"] {{
        display: none !important;
    }}
    [data-testid="stToolbar"] [data-testid="stExpandSidebarButton"],
    [data-testid="stToolbar"] [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {{
        visibility: visible !important;
    }}
    /* درج منبثق أوسع يغطي معظم الشاشة */
    [data-testid="stSidebar"][aria-expanded="true"] {{
        width: min(88vw, 320px) !important;
        min-width: min(88vw, 320px) !important;
    }}
    /* وسادات أصغر لصناديق المحتوى */
    .top-shell {{ padding: 0.6rem 0.7rem 0.5rem; }}
    .lesson-shell {{ padding: 0.7rem 0.75rem 0.55rem; }}
    .unit-card {{ padding: 0.8rem 0.85rem 0.7rem; }}
    .math-frame {{ padding: 0.45rem 0.6rem; }}
    .idea-card {{ padding: 0.7rem 0.85rem; }}
    .hero-panel {{ padding: 0.9rem 0.7rem 0.7rem; }}
    /* صفوف رأس البطاقات تلتفّ فلا تتزاحم الشارة مع العنوان */
    .unit-card-head, .lesson-topbar {{ flex-wrap: wrap; }}
    .unit-card-head {{ gap: 0.4rem; }}
    .topbar {{ gap: 0.4rem; }}
    .badge-panel {{ gap: 0.4rem; }}
    .badge {{ min-width: 100px; }}
    /* جداول عريضة تتمرّر أفقياً */
    [data-testid="stDataFrame"] {{ overflow-x: auto; }}
}}

@media (max-width: 480px) {{
    :root {{
        --t-h1: 1.85rem; --t-h2: 1.3rem; --t-h3: 1.05rem; --t-body: 0.95rem;
    }}
    .lesson-title {{ font-size: clamp(1.7rem, 7vw, 3rem); }}
    [data-testid="stMainBlockContainer"] > div:first-child {{ padding-inline: 0.5rem; }}
    [data-testid="stSidebar"] a {{ padding-block: 0.62rem !important; }}
}}
</style>
"""


CSS_PREMIUM = f"""
<style>
/* ====== بطاقات القياس (st.metric) — حالة لا زخرفة ====== */
div[data-testid="stMetric"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 0.7rem 0.9rem;
    position: relative;
    overflow: hidden;
    transition: border-color .18s ease, transform .18s ease;
}}
div[data-testid="stMetric"]::before {{
    content: "";
    position: absolute; inset-inline-start: 0; inset-block: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent-dark));
    border-radius: 999px;
}}
div[data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    border-color: var(--accent-line);
}}
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {{ color: var(--muted); font-size: var(--t-cap); }}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: var(--text); font-weight: 700; font-size: var(--t-h3);
}}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    padding: 0.1rem 0.5rem; border-radius: 999px;
    background: var(--success-soft); color: var(--success); font-weight: 700;
}}

/* ====== أزرار متدرّجة هادئة ====== */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
    background: linear-gradient(135deg, var(--accent), var(--accent-dark));
    color: #0A0F14; border: 0; border-radius: 0.6rem; font-weight: 700;
    font-family: var(--font-ar);
    box-shadow: 0 2px 10px rgba(0,0,0,.18);
    transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {{
    transform: translateY(-1px);
    filter: brightness(1.05);
    box-shadow: 0 6px 18px rgba(0,0,0,.30);
    color: #0A0F14;
}}
.stButton > button:active {{ transform: translateY(0); }}

/* ====== بطاقة فكرة الدرس ====== */
.idea-card {{
    border-inline-start: 4px solid var(--accent);
    background: var(--panel);
    border-radius: 0.6rem;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0 1rem 0;
    color: var(--text);
    font-size: var(--t-body);
    line-height: 1.8;
}}
.idea-card b {{ color: var(--accent); }}

/* ====== الإطار الرياضي ====== */
.math-frame {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.6rem;
}}
.math-title {{
    font-size: var(--t-cap);
    color: var(--accent);
    font-weight: 700;
    margin-bottom: 0.35rem;
    font-family: var(--font-ar);
}}

/* ====== شارات قبل/بعد/الفرق Δ ====== */
.badge-panel {{ display: flex; gap: 0.6rem; flex-wrap: wrap; margin: 0.5rem 0; }}
.badge {{ flex: 1; min-width: 120px; border-radius: 0.55rem; padding: 0.45rem 0.7rem;
          font-size: var(--t-nav); font-weight: 600; text-align: center;
          font-family: var(--font-mono); direction: ltr; unicode-bidi: isolate; }}
.badge.before {{ background: var(--bdg-b); color: var(--bdg-bt); }}
.badge.after  {{ background: var(--bdg-a); color: var(--bdg-at); }}
.badge.delta  {{ background: var(--bdg-d); color: var(--bdg-dt); }}

/* ====== تسلسل الدرس (فكرة ◄ إطار ◄ محاكي ◄ اختبار) ====== */
.flow {{ display: flex; flex-wrap: wrap; align-items: center; gap: 0.45rem; margin: 0.65rem 0 1rem 0; }}
.flow-step {{
    background: var(--surface); border: 1px solid var(--border);
    color: var(--muted); border-radius: 999px; padding: 0.28rem 0.8rem;
    font-size: var(--t-cap); font-weight: 600; font-family: var(--font-ar);
    line-height: 1.5;
}}
.flow-step.current {{ background: var(--accent-soft); border-color: var(--accent-line); color: var(--accent); font-weight: 700; }}
.flow-arrow {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 1.5rem; height: 1.5rem; border-radius: 50%;
    background: rgba(95,211,196,0.08); border: 1px solid rgba(95,211,196,0.18);
    color: var(--accent); font-weight: 900; font-size: 0.9rem; line-height: 1;
    direction: ltr; unicode-bidi: isolate;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
}}
.flow-arrow-inline {{
    color: var(--accent); font-weight: 900;
    direction: ltr; unicode-bidi: isolate;
}}

/* ====== شارات/كبسولات تقدّم الوحدات ====== */
.unit-progress {{
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: var(--success-soft);
    border: 1px solid var(--accent-line);
    border-radius: 999px; padding: 0.16rem 0.7rem;
    color: var(--success); font-weight: 700;
    font-size: var(--t-cap); font-family: var(--font-mono);
    direction: rtl;
}}

.unit-card {{
    background: var(--shell-bg);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 1rem 1.2rem 0.9rem;
    margin-bottom: 1rem;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.01);
}}
.unit-card-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.4rem;
}}
.unit-card-title {{
    color: var(--text);
    font-size: clamp(1.35rem, 2.2vw, 2.1rem);
    font-weight: 700;
    line-height: 1.6;
    text-align: right;
    flex: 1;
}}
.unit-score {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 6.6rem;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    background: rgba(95,211,196,0.10);
    border: 1px solid rgba(95,211,196,0.25);
    color: var(--accent);
    font-weight: 700;
    font-size: 1.05rem;
    line-height: 1.4;
    white-space: nowrap;
    font-family: var(--font-ar);
}}
.unit-score.done {{
    background: rgba(63,182,143,0.12);
    border-color: rgba(63,182,143,0.30);
    color: var(--success);
}}
.unit-card-body {{
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.9;
    margin-bottom: 0.7rem;
    text-align: right;
}}
.unit-bar-wrap {{
    width: 100%;
    height: 0.55rem;
    background: var(--track-bg);
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid var(--border);
}}
.unit-bar {{
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--success), var(--accent));
    min-width: 0.12rem;
}}

/* ====== الشريط العلوي ====== */
.toolbar {{ display: flex; align-items: center; gap: 0.8rem; padding: 0.3rem 0.1rem; }}
.tb-brand {{ font-weight: 700; font-size: var(--t-body); color: var(--text); }}
.tb-brand bdi {{ color: var(--accent); }}
.tb-link {{
    color: var(--muted); font-size: var(--t-cap); text-decoration: none;
    border: 1px solid var(--border); border-radius: 999px; padding: 0.15rem 0.7rem;
    transition: color .15s ease, border-color .15s ease, background .15s ease;
}}
.tb-link:hover {{ color: var(--accent); border-color: var(--accent-line); background: var(--accent-soft); }}

/* ====== تلميحات صغيرة ====== */
.app-caption {{ color: var(--muted); font-size: var(--t-cap); direction: rtl; text-align: right; line-height: 1.6; }}

/* ====== تذييل الموقع (أسفل كل صفحة) ====== */
.site-footer {{
    text-align: center;
    color: var(--muted);
    font-size: 0.82rem;
    font-weight: 600;
    font-family: var(--font-ar);
    letter-spacing: 0.02em;
    line-height: 1.6;
    padding: 1.1rem 0 0.6rem;
    margin-top: 2.2rem;
    border-top: 1px solid var(--border);
}}
.site-footer .ft-accent {{ color: var(--accent); font-weight: 700; }}

/* ====== خيارات اختيار من متعدّد (دقيقة وهادئة) ====== */
div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {{
    font-size: var(--t-body);
}}
div[data-testid="stRadio"] label:hover, div[data-testid="stCheckbox"] label:hover {{
    color: var(--accent);
}}

/* ====== مبدّل الوضع ====== */
div[data-testid="stSidebar"] div[data-testid="stCheckbox"]:has(input[role="switch"]) {{
    margin: 0.35rem 0.7rem 0.15rem !important;
    padding-bottom: 0.55rem;
    border-bottom: 1px solid var(--border);
}}
div[data-testid="stCheckbox"]:has(input[role="switch"]) label {{
    color: var(--text);
    font-family: var(--font-ar);
    font-size: var(--t-nav);
    font-weight: 500;
    gap: 6px;
}}
div[data-testid="stCheckbox"]:has(input[role="switch"]) label > div:not([data-testid]) {{
    background: var(--border) !important;
}}
div[data-testid="stCheckbox"]:has(input[role="switch"]) label > div:not([data-testid]) > div {{
    background: var(--text) !important;
}}
div[data-testid="stCheckbox"]:has(input[role="switch"]) label:has(input:checked) > div:not([data-testid]) {{
    background: var(--accent) !important;
}}
div[data-testid="stCheckbox"]:has(input[role="switch"]) label:has(input:checked) > div:not([data-testid]) > div {{
    background: var(--bg) !important;
}}
</style>
"""


def _toolbar() -> None:
    """يرسم الشريط العلوي للوحة (علامة المختبر فقط)."""
    st.markdown(
        '<div class="toolbar">'
        '<span class="tb-brand">🏛️ <bdi>مختبر الاقتصاد الكلي المعمّق</bdi></span>'
        "</div>",
        unsafe_allow_html=True,
    )


def render_toolbar() -> None:
    """يرسم الشريط العلوي ومبدّل الوضع في الشريط الجانبي.

    يُستدعى مرة واحدة فقط في app.py قبل st.navigation حتى لا يتكرر العنصر.
    يقع المبدّل في أعلى الشريط الجانبي (مكان طبيعي في واجهة RTL بعيدًا
    عن ركن الشاشة العلوي).
    """
    name = sync_colors()
    dark = name == "dark"
    _toolbar()
    label = "🌙 الوضع الداكن" if dark else "☀️ الوضع الفاتح"
    new_dark = st.sidebar.toggle(
        label,
        value=dark,
        key="__theme_toggle_core",
        help="التبديل بين الوضع الداكن والفاتح",
    )
    if new_dark != dark:
        set_theme(new_dark)
        st.rerun()


def render_footer() -> None:
    """يرسم تذييل المنصة أسفل كل صفحة (يُستدعى بعد nav.run في app.py)."""
    st.markdown(
        '<div class="site-footer">'
        'Deep Macro-economic Learning Platform — Created by '
        '<span class="ft-accent">HAMDI Boulanouar</span>'
        "</div>",
        unsafe_allow_html=True,
    )


def inject_rtl() -> None:
    """يحقن RTL + ألوان الوضع + الخطوط في الصفحة الجارية.

    يجب استدعاؤه بعد st.set_page_config مباشرة في بداية كل صفحة.
    يُحقن في كل مستند صفّحة لأنه يُعاد تحميله عند التنقل بين الصفحات،
    لذا لا يجوز منع الحقن عبر حالة الجلسة (تتخطى حدود المستندات).
    """
    name = sync_colors()
    st.markdown(
        "<style>\n" + FONT_FACE + "\n</style>"
        + _root_css(name) + CSS_SHARED + CSS_PREMIUM,
        unsafe_allow_html=True,
    )