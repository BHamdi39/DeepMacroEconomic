"""الدرس 3.6 — الفجوة الانكماشية والفجوة التضخمية: المسافة AB أو DM على خط °45."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.rtl import COLORS, inject_rtl
from utils.solvers import gap_analysis, three_sector_equilibrium
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="الفجوة الانكماشية والتضخمية", page_icon="6️⃣", layout="wide")
inject_rtl()
mark_visited("3_6")

lesson_header(
    "6️⃣",
    "الفجوة الانكماشية والفجوة التضخمية",
    "إذا كان التوازن دون التشغيل الكامل كانت هناك فجوة انكماشية (بطالة)، وإذا "
    "تجاوزه فهي تضخمية. حجم الفجوة بالمصطلح النقدي الذاتي = |Yf−Y*| / Ke وهو "
    "الإنفاق المستقل الإضافي المطلوب لسدّها.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ المعطيات")
    c1, c2 = st.columns(2)
    y_full = c1.slider("مستوى التشغيل الكامل Yf", 200, 1200, 640, 10)
    model = c2.selectbox("نوع النموذج", ["ثلاث قطاعات", "أربع قطاعات"])
    c3, c4, c5 = st.columns(3)
    a = c3.slider("الاستهلاك الذاتي a", 0, 200, 100, 5)
    b = c4.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
    I0 = c5.slider("الاستثمار I₀", 0, 300, 120, 5)
    c6, c7, c8 = st.columns(3)
    G0 = c6.slider("الإنفاق الحكومي G₀", 0, 300, 100, 5)
    T0 = c7.slider("الضريبة T₀", 0, 200, 80, 5)
    R0 = c8.slider("التحويلات R₀", 0, 200, 40, 5)
    X0, M0, m = 0.0, 0.0, 0.0
    if model == "أربع قطاعات":
        c9, c10, c11 = st.columns(3)
        X0 = c9.slider("الصادرات X₀", 0, 200, 90, 5)
        M0 = c10.slider("الواردات M₀", 0, 200, 50, 5)
        m = c11.slider("الميل الحدي للاستيراد m", 0.05, 0.40, 0.20, 0.01)

    eq = three_sector_equilibrium(a, b, I0, G0, T0, R0, t=0.0) if model == "ثلاث قطاعات" \
        else three_sector_equilibrium(a, b, I0 + X0 - M0, G0, T0, R0, t=0.0)
    # (للاقتصاد المفتوح نستخدم مباشرة بروكسي باحتساب X0-M0 في الإنفاق المستقل)
    Y_star = eq["Y"]
    ke = eq["Ke"]

    if model == "أربع قطاعات":
        from utils.solvers import four_sector_equilibrium
        eq4 = four_sector_equilibrium(a, b, I0, G0, T0, R0, X0, M0, t=0.0, m=m)
        Y_star, ke = eq4["Y"], eq4["Ke"]

    gap = gap_analysis(Y_star, y_full, b, t=0.0, m=(m if model == "أربع قطاعات" else 0.0))

    m1, m2, m3 = st.columns(3)
    m1.metric("الدخل التوازني Y*", f"{Y_star:,.2f}")
    m2.metric("التشغيل الكامل Yf", f"{y_full:,.2f}")
    m3.metric("المضاعف Ke", f"{ke:.2f}")
    st.markdown(f"**نوع الفجوة:** {gap['kind']}")

    # رسم الفجوة على مخطط خط °45
    y = np.linspace(0, max(y_full * 1.5, Y_star * 1.5), 300)
    ad = (a + I0 + G0 - b * T0 + b * R0 + X0 - M0) + b * y
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y, y=y, mode="lines", name="خط °45",
                             line=dict(color=COLORS["ref"], dash="dot", width=2)))
    fig.add_trace(go.Scatter(x=y, y=np.clip(ad, 0, None), mode="lines", name="AD",
                             line=dict(color=COLORS["is_curve"], width=3)))
    fig.add_trace(go.Scatter(x=[Y_star], y=[Y_star], mode="markers+text",
                             text=["E (Y*)"], textposition="top center",
                             marker=dict(color=COLORS["accent"], size=13)))
    fig.add_vline(x=y_full, line_color=COLORS["danger"], line_dash="dot")
    fig.add_annotation(x=y_full + 15, y=max(ad) * 0.9, text="Yf",
                       showarrow=False, font=dict(color=COLORS["danger"]))
    if abs(gap["dy"]) > 1e-9:
        gap_y_top = min(gap["dy"], 0) + y_full
        fig.add_annotation(
            x=y_full, y=y_full + gap["dy"] / 2,
            text=f"الفجوة {gap['dy']:+,.0f}", showarrow=False,
            font=dict(color=COLORS["accent"], size=13))
    fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Segoe UI, Tahoma, sans-serif"),
                      margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(title_text="الدخل Y", gridcolor=COLORS["grid"])
    fig.update_yaxes(title_text="الإنفاق الكلي AD", gridcolor=COLORS["grid"])
    st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        if abs(gap["dy"]) < 1e-9:
            st.success("لا فجوة: الاقتصاد عند التشغيل الكامل.")
        else:
            st.markdown(
                f"**رياضيًا:** Gap = |Yf − Y*| / Ke = |{y_full} − {Y_star:,.1f}| / "
                f"{ke:.2f} = **{abs(gap['dy']) / ke:,.2f}** وحدة من الإنفاق المستقل."
            )
            if gap["dy"] > 0:
                st.warning("فجوة **انكماشية**: يلزم رفع الإنفاق المستقل بنحو "
                           f"{gap['dy'] / ke:,.2f} (رفع G أو خفض T) لبلوغ التشغيل "
                           "الكامل.")
            else:
                st.warning("فجوة **تضخمية**: يلزم خفض الإنفاق المستقل بنحو "
                           f"{abs(gap['dy']) / ke:,.2f} للعودة إلى التشغيل الكامل "
                           "وإخماد الضغوط التضخمية.")

quiz("3_6")