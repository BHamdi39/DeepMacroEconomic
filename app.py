"""مختبر الاقتصاد الكلي المعمّق — الموجّه (multipage v2).

يستخدم Streamlit 1.64 API (st.navigation) لبناء قائمة جانبية مبوبة حسب
الوحدات السبع للمقرر، مع نسبة إنجاز حيّة لكل وحدة وعلامة ✓ لكل درس مُنجز،
واستضافة الدروس في مجلد lessons/ منظمًا.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.modules import MODULES, module_visited
from utils.rtl import inject_rtl, render_footer, render_toolbar

LESSONS_PREFIX = "lessons/"


def _lesson_key(path: str) -> str | None:
    """يشتق مفتاح الزيارة (مثل "3_5") من مسار الدرس {الوحدة}_{الدرس}."""
    if not path.startswith(LESSONS_PREFIX):
        return None
    parts = path.removeprefix(LESSONS_PREFIX).split("/")
    if len(parts) != 2:
        return None
    unit = parts[0].split("_", 1)[0]
    lesson = Path(parts[1]).stem.split("_", 1)[0]
    return f"{unit}_{lesson}" if unit and lesson else None


def _visited_set() -> set:
    raw = st.session_state.get("visited_pages")
    if isinstance(raw, (list, set)):
        return set(raw)
    return set()


def build_nav() -> dict:
    """يبني قائمة التنقل مع شارة الإنجاز الحيّة وعلامات ✓ لكل درس."""
    visited = _visited_set()
    groups: dict[str, list] = {
        "الرئيسية": [
            st.Page("home.py", title="لوحة القيادة", icon=":material/dashboard:", default=True),
        ]
    }
    for prefix, label, _desc, total, pages in MODULES:
        n = module_visited(prefix, total)
        done = n == total
        section = f"{label} · {n}/{total}" + (" ✓" if done else "")
        group_pages = []
        for path, title, icon in pages:
            key = _lesson_key(path)
            display = f"{title} ✓" if (key and key in visited) else title
            group_pages.append(st.Page(path, title=display, icon=icon))
        groups[section] = group_pages
    return groups


st.set_page_config(
    page_title="مختبر الاقتصاد الكلي المعمّق",
    page_icon="🏛️",
    layout="wide",
)

if "__bk0" not in st.query_params:
    st.query_params["__bk0"] = "started"

inject_rtl()
render_toolbar()

if "__bk1" not in st.query_params:
    st.query_params["__bk1"] = "toolbar"

nav = st.navigation(build_nav(), position="sidebar", expanded=True)
try:
    nav.run()
    if "__bk2" not in st.query_params:
        st.query_params["__bk2"] = "ran"
except Exception:
    import traceback

    if "__bk3" not in st.query_params:
        st.query_params["__bk3"] = "err"
    st.error("تعذّر تشغيل الصفحة — يظهر أدناه التتبّع الكامل للخطأ.")
    st.code(traceback.format_exc())

render_footer()