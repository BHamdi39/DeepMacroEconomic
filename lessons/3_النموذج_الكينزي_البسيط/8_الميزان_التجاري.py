"""الدرس 3.8 — الميزان التجاري: NX = X0 − M0 − m·Y مع الفائض والعجز."""
from __future__ import annotations

import numpy as np
import streamlit as st

from utils.plotting import plot_nx
from utils.rtl import inject_rtl
from utils.solvers import trade_balance_point
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="الميزان التجاري", page_icon="8️⃣", layout="wide")
inject_rtl()
mark_visited("3_8")

lesson_header(
    "8️⃣",
    "الميزان التجاري",
    "صافي الصادرات NX = X − M = X0 − M0 − mY: يتدهور مع ارتفاع الدخل (لأن "
    "الواردات تتبع الدخل). يتعامل الميزان عند Y_tb = (X0−M0)/m، فوقه عجز "
    "وتحته فائض.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ المعطيات")
    c1, c2, c3 = st.columns(3)
    X0 = c1.slider("الصادرات المستقلة X₀", 20, 300, 150, 5)
    M0 = c2.slider("الواردات المستقلة M₀", 20, 300, 90, 5)
    m = c3.slider("الميل الحدي للاستيراد m", 0.05, 0.40, 0.20, 0.01)

    y_max = 1200
    yp = np.linspace(0, y_max, 400)
    nxp = X0 - M0 - m * yp
    y_tb = trade_balance_point(X0, M0, m)["Y_tb"]
    y_star = st.session_state.get("y_star_4sector")
    params4 = st.session_state.get("params_4sector", {})
    use_4s = y_star and abs(params4.get("X0", 0) - X0) < 1e-9 and \
        abs(params4.get("M0", 0) - M0) < 1e-9 and abs(params4.get("m", 0) - m) < 1e-9

    fig = plot_nx(yp, nxp, y_tb if np.isfinite(y_tb) else y_max / 2)
    st.plotly_chart(fig, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("نقطة تعادل الميزان Y_tb", f"{y_tb:,.2f}" if np.isfinite(y_tb) else "∞")
    if use_4s:
        nx_star = X0 - M0 - m * y_star
        m2.metric(f"NX عند Y* الاقتصاد ({y_star:,.0f})", f"{nx_star:,.2f}")
        m3.metric("الوضع", "فائض" if nx_star > 0 else "عجز")
    else:
        m2.metric("الدخل الحالي Y (افتراضي)", f"{y_max/2:,.0f}")
        m3.metric("NX عنده", f"{X0 - M0 - m*(y_max/2):,.2f}")

    with st.container(border=True):
        if use_4s:
            if nx_star > 0:
                st.success(f"عند توازن الاقتصاد الكلي الكامل (من درس 3.4) Y* = "
                           f"{y_star:,.0f}: الميزان التجاري في **فائض** ({nx_star:+,.2f}).")
            else:
                st.warning(f"عند توازن الاقتصاد الكلي الكامل (من درس 3.4) Y* = "
                           f"{y_star:,.0f}: الميزان التجاري في **عجز** ({nx_star:+,.2f}).")
            st.caption("هذا يربط محاكي 3.4 بهذا الدرس: وضع الميزان التجاري يتحدد "
                       "بمقارنة Y* الفعلي بنقطة التعادل Y_tb.")
        else:
            st.info("اذهب إلى درس 3.4 (اقتصاد أربع قطاعات) ثم عد: سيعرض هذا "
                    "الرسم وضع الميزان التجاري عند التوازن الكلي الفعلي.")

quiz("3_8")