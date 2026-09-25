"""الدرس 4.1 — اشتقاق منحنى IS: كل سعر فائدة يعطي دخل توازن؛ أثر النقاط (Y,i)."""
from __future__ import annotations

import numpy as np
import streamlit as st

from utils.plotting import plot_is_derivation
from utils.rtl import inject_rtl
from utils.solvers import is_curve
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="اشتقاق منحنى IS", page_icon="📉", layout="wide")
inject_rtl()
mark_visited("4_1")

lesson_header(
    "📉",
    "اشتقاق منحنى IS",
    "الاستثمار يتناقص مع سعر الفائدة (I = I₀ − µi). لكل سعر فائدة يوجد دخل توازن "
    "وحيد، ولما كان كل ٱ (Y,i) تحقق توازن سوق السلع تكون منحنى IS: Y = Kₑ[A − µi].",
)

math_frame(
    "معادلة منحنى IS",
    r"Y^* = K_e\,[\,A - \mu\,i\,],\qquad "
    r"K_e = \frac{1}{1 - b + bt + m},\qquad "
    r"A = a + I_0 + G_0 - bT_0 + bR_0 + X_0 - M_0",
    "A مجموع الإنفاق المستقل، و Kₑ المضاعف العام، و µ حساسية الاستثمار للفائدة.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات سوق السلع")
    c1, c2, c3, c4 = st.columns(4)
    a = c1.number_input("الاستهلاك الذاتي a", 0.0, 500.0, 100.0, 10.0)
    b = c2.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
    I0 = c3.number_input("الاستثمار المستقل I₀", 0.0, 500.0, 150.0, 10.0)
    mu = c4.slider("حساسية الاستثمار للفائدة µ", 1.0, 30.0, 10.0, 0.5)

    c5, c6, c7, c8 = st.columns(4)
    G0 = c5.number_input("الإنفاق الحكومي G₀", 0.0, 500.0, 200.0, 10.0)
    T0 = c6.number_input("الضرائب T₀", 0.0, 500.0, 0.0, 10.0)
    R0 = c7.number_input("التحويلات R₀", 0.0, 500.0, 0.0, 10.0)
    c8.markdown("")

    c9, c10 = st.columns(2)
    X0 = c9.number_input("الصادرات X₀", 0.0, 500.0, 0.0, 10.0)
    M0 = c10.number_input("الواردات M₀", 0.0, 500.0, 0.0, 10.0)

    c11, c12 = st.columns(2)
    t = c11.slider("معدل ضريبة الدخل t", 0.0, 0.40, 0.0, 0.01)
    m = c12.slider("الميل الحدي للاستيراد m", 0.0, 0.40, 0.0, 0.01)

    p = is_curve(a, b, I0, mu, G0, T0, R0, X0, M0, t=t, m=m)
    st.success(
        f"A = {p['A']:.2f}  |  Kₑ = 1/(1−b+bt+m) = **{p['Ke']:.4f}**  ⇒  "
        f"**IS: Y = {p['Ke']:.3f} × ({p['A']:.2f} − {mu:.1f}·i)**"
    )
    st.caption("⁄ ∵ كل انخفاض في i يرفع الاستثمار، فيزداد الدخل: منحنى IS ينحدر يمينًا-أسفل.")

    i_range = np.linspace(0.0, 12.0, 40)
    fig = plot_is_derivation(p, i_range)
    st.plotly_chart(fig, use_container_width=True)

    y0 = p["Ke"] * p["A"]
    y10 = p["Ke"] * (p["A"] - mu * 10)
    m1, m2, m3 = st.columns(3)
    m1.metric("الدخل عند i = 0%", f"{y0:,.1f}")
    m2.metric("الدخل عند i = 10%", f"{y10:,.1f}")
    m3.metric("الفارق لكل 1% زيادة في i", f"{p['Ke'] * mu:,.1f}")
    st.caption("الرسم العلوي: خط AD ينزاح مع تغيّر i فيقطع °45 عند توازن جديد؛ "
               "الرسم السفلي: منحنى IS يربط نقاط التوازن (Y, i) — اشتقاق نقطة بنقطة.")

quiz("4_1")