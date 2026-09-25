"""الدرس 2.2 — نظرية كمية النقود M·V=P·Y وحياد النقود عند الكلاسيكيين."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.rtl import COLORS, inject_rtl
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="نظرية كمية النقود", page_icon="2️⃣", layout="wide")
inject_rtl()
mark_visited("2_2")

lesson_header(
    "2️⃣",
    "نظرية كمية النقود",
    "معادلة التبادل M·V = P·Y؛ عند الكلاسيكيين V وY ثابتان في المدى القصير، "
    "فارتفاع عرض النقود M يُترجم ارتفاعًا نسبيًا في الأسعار P فقط — حياد "
    "النقود.",
)

st.latex(r"M \cdot V = P \cdot Y \ \ \ \Longrightarrow\ \ \ P = \frac{M \cdot V}{Y}")

with st.container(border=True):
    st.markdown("#### 🎚️ المعطيات")
    c1, c2, c3 = st.columns(3)
    M = c1.slider("عرض النقود M", 100, 400, 200, 10)
    V = c2.slider("سرعة دوران النقود V", 1.0, 10.0, 5.0, 0.5)
    Y = c3.slider("الناتج الحقيقي Y", 100, 400, 200, 10)

    P = M * V / Y

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("عرض النقود M", f"{M}")
    m2.metric("السرعة V", f"{V:.1f}")
    m3.metric("الناتج Y", f"{Y}")
    m4.metric("مستوى الأسعار P", f"{P:.2f}")

    st.markdown("#### 📈 مسار الأسعار عند تدرّج M نحو الضعف (V وY ثابتان)")
    m_path = np.linspace(M, 2 * M, 50)
    p_path = m_path * V / Y
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=m_path, y=p_path, mode="lines",
                             line=dict(color=COLORS["lm_curve"], width=3),
                             name="P كدالة في M"))
    fig.add_trace(go.Scatter(x=[M, 2 * M], y=[P, 2 * P], mode="markers+text",
                             text=["الحالية", "مضاعفة M"],
                             textposition="top center",
                             marker=dict(color=COLORS["accent"], size=12,
                                         line=dict(color="#fff", width=1))))
    fig.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Segoe UI, Tahoma, sans-serif"),
                      margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(title_text="عرض النقود M", gridcolor=COLORS["grid"])
    fig.update_yaxes(title_text="مستوى الأسعار P", gridcolor=COLORS["grid"])
    st.plotly_chart(fig, use_container_width=True)

    doubling = (2 * P / P - 1) * 100
    with st.container(border=True):
        st.success(f"عند مضاعفة M من {M} إلى {2*M}، يرتفع P من {P:.2f} إلى "
                   f"{2*P:.2f} (نسبة {doubling:.0f}% مطابقة لنسبة الزيادة في M) "
                   "بينما يبقى Y وV ثابتَين — هذه هي رؤية الكلاسيكيين لحياد النقود.")
    st.caption("استنتاج كينزي لاحق: في وجود جمود الأجور، جزء من الزيادة يذهب إلى "
               "الناتج Y وليس كله إلى الأسعار — وهو ما تدرسه الوحدة الثالثة.")

quiz("2_2")