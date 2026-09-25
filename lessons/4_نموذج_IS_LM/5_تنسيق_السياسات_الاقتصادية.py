"""الدرس 4.5 — تنسيق السياسات المالية والنقدية: حالة E2/E3/E4 بتطبيق أداتين معًا."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_is_lm
from utils.rtl import inject_rtl
from utils.solvers import is_lm_equilibrium, lm_curve
from utils.ui import bad_after_delta, lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="تنسيق السياسات الاقتصادية", page_icon="🤝", layout="wide")
inject_rtl()
mark_visited("4_5")

lesson_header(
    "🤝",
    "تنسيق السياسات الاقتصادية",
    "لتحقيق هدفين معًا (تشغيل كامل + مستوى فائدة محدد) تطبَّق مالية ونقدية في آن "
    "واحد. بمقارنة أثر الأداة المالية على الفائدة (α/g)ΘΔA بالأثر النقدي "
    "(1/Kₑg)ΘΔMₛ نصنّف النتيجة: مالية أقوى (E2)، نقدية أقوى (E4)، أو تعادل وثبات i (E3).",
)

math_frame(
    "صنف الحالة بمقارنة أثرين على i",
    r"i_{\text{مالية}} = \frac{\alpha}{g}\,\Theta\,\Delta A,\qquad "
    r"i_{\text{نقدية}} = \frac{1}{K_e g}\,\Theta\,\Delta M_s",
    "فإن كانت |i المالية| > |i النقدية| فالسياسة المالية أقوى (E2)، والعلاقة " 
    "الأخرى تعني النقدية أقوى (E4)، والتساوي يعني تعادل الأثرين (E3).",
)

c1, c2, c3, c4 = st.columns(4)
b = c1.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
A0 = c2.number_input("الإنفاق المستقل A", 100.0, 1500.0, 600.0, 10.0)
mu = c3.slider("حساسية الاستثمار للفائدة µ", 1.0, 30.0, 10.0, 0.5)
Ms = c4.number_input("عرض النقود Mₛ", 50.0, 1000.0, 400.0, 10.0)

c5, c6 = st.columns(2)
Q = c5.number_input("الطلب الذاتي Q", 0.0, 500.0, 100.0, 10.0)
alpha = c6.slider("حساسية الطلب للدخل α", 0.1, 1.2, 0.60, 0.05)
g = c6.slider("حساسية الطلب المضاربي g", 1.0, 300.0, 30.0, 1.0)

c7, c8, c9 = st.columns(3)
dG = c7.slider("ΔG₀ (سياسة مالية)", -150.0, 150.0, 100.0, 5.0)
dM = c8.slider("ΔMₛ (سياسة نقدية)", -150.0, 150.0, 50.0, 5.0)
c9.markdown("<div style='padding-top:2.2rem'></div>", unsafe_allow_html=True)

Ke = 1 / (1 - b)
is0 = {"Ke": Ke, "A": A0, "mu": mu}
lm0 = lm_curve(Q, alpha, g, Ms)
eq0 = is_lm_equilibrium(is0, lm0)

is1 = {"Ke": Ke, "A": A0 + dG, "mu": mu}
lm1 = lm_curve(Q, alpha, g, Ms + dM)
eq1 = is_lm_equilibrium(is1, lm1)

i_fisc = (alpha / g) * eq0["Theta"] * dG
i_mon = (1 / (Ke * g)) * eq0["Theta"] * dM
if abs(i_fisc) > abs(i_mon):
    state, desc = "E2 — السياسة المالية أقوى", (
        f"الأثر المالي |{i_fisc:+.3f}| أكبر من النقدي |{i_mon:+.3f}| ⇒ "
        f"الفائدة ترتفع صافيًا ({i_fisc + i_mon:+.3f}%) والاقتصاد يُدار مالياً.")
elif abs(i_fisc) < abs(i_mon):
    state, desc = "E4 — السياسة النقدية أقوى", (
        f"الأثر النقدي |{i_mon:+.3f}| أكبر من المالي |{i_fisc:+.3f}| ⇒ "
        f"الفائدة تنخفض صافيًا ({i_fisc + i_mon:+.3f}%) والاقتصاد يُدار نقدياً.")
else:
    state, desc = "E3 — تعادل الأثرين وثبات i", (
        f"الأثران متساويان تقريبًا ({i_fisc:+.3f} ≈ {i_mon:+.3f}) ⇒ "
        f"الفائدة شبه ثابتة مع نموّ الدخل: تشغيل كامل دون تغيّر i.")

with st.container(border=True):
    bad_after_delta(("قبل (Y*)", "بعد التنسيق (Y*)", "ΔY"), eq0["Y"], eq1["Y"], "{:,.1f}")
    bad_after_delta(("قبل (i*)", "بعد التنسيق (i*)", "Δi"), eq0["i"], eq1["i"], "{:.3f}")
    st.success(f"**{state}** — {desc}")
    st.plotly_chart(plot_is_lm(is0, lm0, eq0, is2_params=is1, lm2_params=lm1),
                    use_container_width=True)
    st.markdown(f"$Y^*$: {eq0['Y']:,.1f} → {eq1['Y']:,.1f}  |  "
                f"$i^*$: {eq0['i']:.3f}% → {eq1['i']:.3f}%")

quiz("4_5")