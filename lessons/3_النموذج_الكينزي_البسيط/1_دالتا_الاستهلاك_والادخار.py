"""الدرس 3.1 — دالتا الاستهلاك والادخار: C=a+bYd و S=-a+(1-b)Yd."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.rtl import COLORS, inject_rtl
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="دالتا الاستهلاك والادخار", page_icon="1️⃣", layout="wide")
inject_rtl()
mark_visited("3_1")

lesson_header(
    "1️⃣",
    "دالتا الاستهلاك والادخار",
    "الدخل المتاح يقسم إلى استهلاك وادخار: الميل الحدي للاستهلاك b وميله "
    "للادخار s=1−b؛ والميل المتوسط للاستهلاك = a/Y + b وينخفض مع ارتفاع الدخل.",
)

st.latex(r"C = a + b\cdot Y_d \ \ \ \ \ S = -a + (1-b)\cdot Y_d \ \ \ \ \ MPC = b, \; MPS = 1-b,\; APC = \frac{C}{Y},\; APS = \frac{S}{Y}")

with st.container(border=True):
    st.markdown("#### 🎚️ المعطيات")
    c1, c2 = st.columns(2)
    a = c1.slider("الاستهلاك الذاتي a", 0, 200, 100, 5)
    b = c2.slider("الميل الحدي للاستهلاك b (MPC)", 0.40, 0.95, 0.80, 0.01)
    y_sel = st.slider("مؤشر الدخل Y (لحساب القيم المتوسطة)", 0, 1000, 400, 10)

    s = 1 - b
    y = np.linspace(0, 1000, 400)
    C = a + b * y
    S = -a + s * y

    c_sel = a + b * y_sel
    s_sel = -a + s * y_sel

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y, y=C, mode="lines", name="C = a + b·Y",
                             line=dict(color=COLORS["is_curve"], width=3)))
    fig.add_trace(go.Scatter(x=y, y=S, mode="lines", name="S = −a + (1−b)·Y",
                             line=dict(color=COLORS["success"], width=3)))
    fig.add_vline(x=y_sel, line_color=COLORS["muted"], line_dash="dot")
    fig.add_trace(go.Scatter(x=[y_sel], y=[c_sel], mode="markers",
                             marker=dict(color=COLORS["accent"], size=12)))
    fig.add_trace(go.Scatter(x=[y_sel], y=[s_sel], mode="markers",
                             marker=dict(color=COLORS["warning"], size=12)))
    fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Segoe UI, Tahoma, sans-serif"),
                      margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(title_text="الدخل المتاح Yd", gridcolor=COLORS["grid"], range=[0, 1000])
    fig.update_yaxes(title_text="C و S", gridcolor=COLORS["grid"])
    st.plotly_chart(fig, use_container_width=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("MPC = b", f"{b:.2f}")
    m2.metric("MPS = 1−b", f"{s:.2f}")
    m3.metric(f"الدخل Y={y_sel}", "—")
    m4.metric("APC = C/Y", f"{c_sel / y_sel:.3f}" if y_sel else "—")
    m5.metric("APS = S/Y", f"{s_sel / y_sel:.3f}" if y_sel else "—")

    with st.container(border=True):
        st.markdown("#### 📈 ملاحظة جوهرية")
        st.info(f"عند Y = {y_sel}: APC = {c_sel/y_sel:.3f} بينما MPC = {b:.2f} — "
                "الميل المتوسط للاستهلاك أكبر من الحدي ويكون مقاربًا له مع تزايد "
                "الدخل (لأن العنصر الذاتي a يتناقص وزنه النسبي).")
        st.caption("نقطة التعادل (C=Y تُعطي S=0): عند Y = a/(1−b) = "
                   f"{a / s:.1f}.")

quiz("3_1")