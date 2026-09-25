"""الدرس 3.3 — التوازن في اقتصاد ثلاث قطاعات: أضف الحكومة (G0, T0/t, R0)."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_dual_income
from utils.rtl import inject_rtl
from utils.solvers import three_sector_equilibrium
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="التوازن في ثلاث قطاعات", page_icon="3️⃣", layout="wide")
inject_rtl()
mark_visited("3_3")

lesson_header(
    "3️⃣",
    "التوازن في اقتصاد ثلاث قطاعات (دخول الحكومة)",
    "يُضاف الإنفاق الحكومي G0 والتحويلات R0 والضرائب T (مستقلة T0 أو مرتبطة "
    "بالدخل t·Y). الضرائب المرتبطة بالدخل تخفض الميل الفعلي للإنفاق الكلي "
    "فتُضعف المضاعف وتغيّر نقطة التوازن.",
)

tax_mode = st.radio("نوع الضريبة:", ["ضرائب مستقلة T0", "ضرائب مرتبطة بالدخل T0 + t·Y"],
                    horizontal=True)
linked = "مرتبطة" in tax_mode

with st.container(border=True):
    st.markdown("#### 🎚️ المعطيات")
    c1, c2, c3 = st.columns(3)
    a = c1.slider("الاستهلاك الذاتي a", 0, 200, 100, 5)
    b = c2.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
    I0 = c3.slider("الاستثمار المستقل I₀", 0, 300, 120, 5)
    c4, c5, c6 = st.columns(3)
    G0 = c4.slider("الإنفاق الحكومي G₀", 0, 300, 100, 5)
    T0 = c5.slider("الضريبة المستقلة T₀", 0, 200, 80, 5)
    R0 = c6.slider("التحويلات R₀", 0, 200, 40, 5)
    t = 0.0
    if linked:
        t = st.slider("معدل الضريبة على الدخل t", 0.05, 0.40, 0.20, 0.01)

    st.divider()
    st.markdown("**مقارنة الحالتين جنبًا إلى جنب (E₁ مستقل / E₂ مرتبط)**")
    col1, col2 = st.columns(2)
    results = {}
    for label, mode_t, use_linked in [("ضريبة مستقلة (المنحنى الأزرق)", 0.0, False),
                                      ("ضريبة مرتبطة (المنحنى البرتقالي)", t, True)]:
        eq = three_sector_equilibrium(a, b, I0, G0, T0, R0, t=mode_t)
        results[label] = eq
        with col1 if not use_linked else col2:
            st.markdown(f"##### {label}")
            st.markdown(f"المضاعف: **{eq['Ke']:.2f}**")
            st.markdown(f"**Y* = {eq['Y']:,.2f}**")
    st.markdown("")

    m1, m2 = st.columns(2)
    m1.metric("Y* بضريبة مستقلة (E₁)", f"{results['ضريبة مستقلة (المنحنى الأزرق)']['Y']:,.2f}")
    m2.metric("Y* بضريبة مرتبطة (E₂)", f"{results['ضريبة مرتبطة (المنحنى البرتقالي)']['Y']:,.2f}")
    diff = results['ضريبة مستقلة (المنحنى الأزرق)']['Y'] - results['ضريبة مرتبطة (المنحنى البرتقالي)']['Y']
    st.caption(f"الفرق ΔY = {diff:,.2f} — الضريبة المرتبطة بالدخل تخفض التوازن لأنها "
               "تسرّب جزءًا من كل زيادة في الدخل.")

    st.markdown("#### 📊 الرسم المزدوج (الرسم الموحّد للحالتين)")
    sel = "ضريبة مرتبطة (المنحنى البرتقالي)" if linked else "ضريبة مستقلة (المنحنى الأزرق)"
    eq = results[sel]
    ad_slope = b * (1 - t) if linked else b
    ad_intercept = a + I0 + G0 - b * T0 + b * R0
    leak_intercept = (b * T0 - a + (1 - b) * R0) if linked else (-a + b * T0 + (1 - b) * R0)
    leak_slope = (1 - b + b * t) if linked else (1 - b)
    fig = plot_dual_income(
        ad_slope=ad_slope, ad_intercept=ad_intercept, y_star=eq["Y"],
        leak_intercept=leak_intercept, leak_slope=leak_slope,
        inj_intercept=I0 + G0 + R0, inj_slope=0.0,
    )
    st.plotly_chart(fig, use_container_width=True)

st.latex(r"\text{مستقلة: } Y^* = \frac{1}{1-b}(a+I_0+G_0-bT_0+bR_0) \quad\mid\quad \text{مرتبطة: } Y^* = \frac{1}{1-b+bt}(a+I_0+G_0-bT_0+bR_0)")

quiz("3_3")