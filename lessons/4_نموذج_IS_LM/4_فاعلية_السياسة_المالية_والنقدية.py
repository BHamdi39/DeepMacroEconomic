"""الدرس 4.4 — فاعلية السياسة المالية والنقدية عبر مناطق LM الثلاث."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_is_lm
from utils.rtl import inject_rtl
from utils.solvers import is_lm_equilibrium, is_lm_regions_preset, lm_curve
from utils.ui import bad_after_delta, lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="فاعلية السياسة المالية والنقدية", page_icon="🎯", layout="wide")
inject_rtl()
mark_visited("4_4")

lesson_header(
    "🎯",
    "فاعلية السياسة المالية والنقدية",
    "صدمة مالية (ΔG₀) تزحزح IS، وصدمة نقدية (ΔMₛ) تزحزح LM، لكن الأثر على الدخل "
    "والفائدة يتباين بشدة حسب منطقة LM: في الكينزي تكون المالية فعّالة والنقدية "
    "بلا أثر؛ وفي الكلاسيكي ينعكس الوضع مع مزاحمة كاملة.",
)

math_frame(
    "أثر أدوات السياسة",
    r"\Delta Y = \Theta\,\Delta A,\quad \Delta i = \frac{\alpha}{g}\,\Theta\,\Delta A,"
    r"\qquad\qquad"
    r"\Delta Y = \sigma\,\Delta M_s,\quad \Delta i = -\frac{1}{K_e g}\,\Theta\,\Delta M_s",
    "الأوليان للسياسة المالية (ΔA = ΔG₀)، والآخران للسياسة النقدية.",
)

c1, c2, c3, c4 = st.columns(4)
b = c1.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
A0 = c2.number_input("الإنفاق المستقل A", 100.0, 1500.0, 600.0, 10.0)
mu = c3.slider("حساسية الاستثمار للفائدة µ", 1.0, 30.0, 10.0, 0.5)
Ms = c4.number_input("عرض النقود Mₛ", 50.0, 1000.0, 400.0, 10.0)

c5, c6, c7 = st.columns(3)
Q = c5.number_input("الطلب الذاتي Q", 0.0, 500.0, 100.0, 10.0)
alpha = c6.slider("حساسية الطلب للدخل α", 0.1, 1.2, 0.60, 0.05)
region = c7.radio("منطقة منحنى LM", list(is_lm_regions_preset().keys()))
g = is_lm_regions_preset()[region]["g"]

c8, c9, c10 = st.columns(3)
tool = c8.radio("أداة السياسة", ["مالية: ΔG₀", "نقدية: ΔMₛ"])
delta = c9.slider("حجم الصدمة", 0.0, 200.0, 80.0, 5.0)
c10.markdown(f"<div style='padding-top:2.2rem'></div>", unsafe_allow_html=True)

Ke = 1 / (1 - b)
is0 = {"Ke": Ke, "A": A0, "mu": mu}
lm0 = lm_curve(Q, alpha, g, Ms)
eq0 = is_lm_equilibrium(is0, lm0)

if tool.startswith("مالية"):
    is1 = {"Ke": Ke, "A": A0 + delta, "mu": mu}
    lm1 = lm0
    effect_y = eq0["Theta"] * delta
    effect_i = (alpha / g) * eq0["Theta"] * delta
else:
    is1 = is0
    lm1 = lm_curve(Q, alpha, g, Ms + delta)
    effect_y = eq0["sigma"] * delta
    effect_i = -(1 / (Ke * g)) * eq0["Theta"] * delta

eq1 = is_lm_equilibrium(is1, lm1)
shock_name = "ΔG₀" if tool.startswith("مالية") else "ΔMₛ"

with st.container(border=True):
    bad_after_delta(("قبل (Y*)", "بعد الصدمة (Y*)", f"ΔY (صدمة {shock_name})"),
                    eq0["Y"], eq1["Y"], "{:,.1f}")
    bad_after_delta(("قبل (i*)", "بعد الصدمة (i*)", "Δi"), eq0["i"], eq1["i"], "{:.3f}")
    st.markdown(f"**المنطقة:** {region} — {is_lm_regions_preset()[region]['desc']}")
    st.markdown(f"$\\Delta Y = {effect_y:+,.2f}$,  "
                f"$\\Delta i = {effect_i:+,.3f}$%")
    st.plotly_chart(plot_is_lm(is0, lm0, eq0, is2_params=is1 if tool.startswith("مالية") else None,
                               lm2_params=lm1 if tool.startswith("نقدية") else None),
                    use_container_width=True)

with st.container(border=True):
    st.markdown("#### 📊 مقارنة الأثر عبر المناطق الثلاث")
    table = []
    for rname, rp in is_lm_regions_preset().items():
        gk = rp["g"]
        lmk = lm_curve(Q, alpha, gk, Ms)
        eqk = is_lm_equilibrium(is0, lmk)
        if tool.startswith("مالية"):
            dY = eqk["Theta"] * delta
            di = (alpha / gk) * eqk["Theta"] * delta
        else:
            dY = eqk["sigma"] * delta
            di = -(1 / (Ke * gk)) * eqk["Theta"] * delta
        table.append({"منطقة LM": rname, "ΔY": f"{dY:,.2f}", "Δi": f"{di:+.3f}%"})
    st.dataframe(table, hide_index=True, use_container_width=True)
    st.caption(
        "الكينزي: المالية ترفع Y كثيرًا دون رفع i (لا مزاحمة) والنقدية ≈ صفر. "
        "الكلاسيكي: المالية لا ترفع Y (مزاحمة كاملة) والنقدية ترفعه بأقصى أثر "
        "ΔM/α. الوسيط: حالة وسطى."
    )

quiz("4_4")