"""الدرس 5.3 — السياسات تحت أنظمة الصرف: أربع تركيبات (مالية/نقدية × صرف ثابت/مرن)."""
from __future__ import annotations

import numpy as np
import streamlit as st

from utils.plotting import plot_is_lm
from utils.rtl import inject_rtl
from utils.solvers import bp_curve, is_lm_equilibrium, lm_curve
from utils.ui import bad_after_delta, lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="السياسات تحت أنظمة الصرف", page_icon="🧭", layout="wide")
inject_rtl()
mark_visited("5_3")

lesson_header(
    "🧭",
    "السياسات تحت أنظمة الصرف (موندل-فليمنغ)",
    "نظام الصرف يقرّر مصير السياسات: تحت الصرف الثابت تتدخل البنك المركزي فيداعب "
    "LM، فتكون النقدية عاجزة والمالية فعّالة؛ وتحت الصرف المرن تتحمّل حركة سعر "
    "الصرف تعديل IS (عبر NX)، فتنعكس الفاعلية: النقدية فعّالة والمالية تتراجع.",
)

math_frame(
    "قاعدة الميـز التنبئية",
    r"\text{طلبات ثابتة: البنك المركزي يحرّك LM} \;\Rightarrow\; "
    r"\underbrace{\Delta G\text{ فعّال},\ \Delta M\text{ عاجز}}"
    r"_{\text{صرف ثابت}}",
    r"\text{صرف مرن: سعر الصرف يحرّك IS (NX)} \;\Rightarrow\; "
    r"\underbrace{\Delta M\text{ فعّال},\ \Delta G\text{ يتسرب}}"
    r"_{\text{صرف مرن}}",
)

c1, c2, c3, c4 = st.columns(4)
b = c1.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
A0 = c2.number_input("الإنفاق المستقل الكلي A", 100.0, 1500.0, 600.0, 10.0)
mu = c3.slider("حساسية الاستثمار للفائدة µ", 1.0, 30.0, 10.0, 0.5)
Ms = c4.number_input("عرض النقود Mₛ", 50.0, 1000.0, 400.0, 10.0)

c5, c6, c7 = st.columns(3)
Q = c5.number_input("الطلب الذاتي Q", 0.0, 500.0, 100.0, 10.0)
alpha = c6.slider("حساسية الطلب للدخل α", 0.1, 1.2, 0.60, 0.05)
g = c6.slider("حساسية الطلب المضاربي g", 1.0, 300.0, 30.0, 1.0)

c8, c9, c10 = st.columns(3)
X0 = c8.number_input("الصادرات المستقلة X₀", 0.0, 300.0, 150.0, 5.0)
M0 = c9.number_input("الواردات المستقلة M₀", 0.0, 300.0, 100.0, 5.0)
m = c10.slider("الميل الحدي للاستيراد m", 0.05, 0.50, 0.15, 0.01)
kappa = c10.slider("درجة حركة رأس المال κ", 0.5, 50.0, 15.0, 0.5)
i_world = c10.slider("سعر الفائدة العالمي i*%", 0.0, 20.0, 4.0, 0.1)

c11, c12, c13 = st.columns(3)
policy = c11.radio("أداة السياسة التوسعية", ["مالية (ΔG₀)", "نقدية (ΔMₛ)"])
regime = c12.radio("نظام سعر الصرف", ["ثابت", "مرن"])
delta = c13.slider("حجم الصدمة", 0.0, 200.0, 100.0, 5.0)

Ke = 1 / (1 - b)
is0 = {"Ke": Ke, "A": A0, "mu": mu}
lm0 = lm_curve(Q, alpha, g, Ms)
bp_params = bp_curve(X0, M0, m, kappa, i_world)
c0, s0 = bp_params["intercept"], bp_params["slope"]
eq0 = is_lm_equilibrium(is0, lm0)

fiscal = policy.startswith("مالية")
is_shock = {"Ke": Ke, "A": A0 + delta, "mu": mu}
lm_shock = lm_curve(Q, alpha, g, Ms + delta)


def is_bp(Ke_, A_, mu_, c, s):
    y = Ke_ * (A_ - mu_ * c) / (1 + Ke_ * mu_ * s)
    i = c + s * y
    return float(y), float(i)


def lm_bp(lm_, c, s):
    denom = lm_["alpha"] - g * s
    if denom <= 0:
        return None
    y = (lm_["Ms"] - lm_["Q"] + g * c) / denom
    i = c + s * y
    if y <= 0:
        return None
    return float(y), float(i)


# --- منطق مونديل-فليمنغ: التوازن النهائي يعود إلى منحنى BP ---
if regime == "ثابت":
    if fiscal:
        y_f, i_f = is_bp(Ke, A0 + delta, mu, c0, s0)     # LM يتدخل البنك حتى يمرّ بـ BP
        is_f, lm_f = is_shock, {"Ke": Ke, "A": A0 + delta, "mu": mu}
        ms_final = Q + alpha * y_f - g * i_f
        lm_f = lm_curve(Q, alpha, g, ms_final)
        msg = ("السياسة المالية تحرك IS يمينًا فترتفع i فوق i_BP ويحدث فائض؛ "
               "فيشتري البنك المركزي العملة الأجنبية (LM يتسع) حتى بلوغ التوازن "
               "الجديد على BP — فإذن المالية **فعّالة** تحت الصرف الثابت.")
    else:
        y_f, i_f = eq0["Y"], eq0["i"]                    # التدخل يقضي على أثر الصدمة النقدية
        is_f, lm_f = is0, lm0
        msg = ("السياسة النقدية توسّع LM يمينًا فتهبط i تحت i_BP فيحصل عجز تدفقات؛ "
               "لكن البنك المركزي يضطر للتدخل لبيع العملة الأجنبية فينكمش عرض "
               "النقود ويعود LM أين كان — فإذن النقدية **عاجزة تمامًا** تحت الصرف الثابت.")
else:  # مرن
    if fiscal:
        y_f, i_f = lm_bp(lm0, c0, s0)                    # LM ثابت، الصرف يحرّك IS عائدًا إلى BP
        is_f = {"Ke": Ke, "A": y_f / Ke + mu * i_f, "mu": mu}
        lm_f = lm0
        msg = ("السياسة المالية تحرك IS يمينًا فترتفع i فوق i_BP فيدخل رأس مال "
               "ويشتد عجز تجاري، فتنخفض الصادرات الصافية (تقدير العملة) فيتراجع IS "
               "ذاتيًا حتى عودته إلى BP — فإذن المالية **أقل فاعلية** تحت الصرف المرن "
               "(مزاحمة عبر NX بدل الفائدة).")
    else:
        y_f, i_f = lm_bp(lm_shock, c0, s0)               # LM يتسع، الصرف يحرّك IS نحو BP
        is_f = {"Ke": Ke, "A": y_f / Ke + mu * i_f, "mu": mu}
        lm_f = lm_shock
        msg = ("السياسة النقدية توسّع LM يمينًا فتهبط i تحت i_BP فيخرج رأس المال "
               "وينخفض سعر الصرف (تراجع العملة) فيشتد دعم NX ويرتفع IS ذاتيًا نحو "
               "BP — فإذن النقدية **فعّالة بقوة** تحت الصرف المرن.")

eq_f = {"Y": y_f, "i": i_f}
closed_Y = (eq0["Theta"] if fiscal else eq0["sigma"]) * delta

with st.container(border=True):
    st.markdown(f"#### 🎬 السيناريو: {policy} × صرف {regime}")
    st.info(msg)
    bad_after_delta(("قبل (Y*)", "النهاية بعد التعديل (Y*)", "ΔY نهائي"),
                    eq0["Y"], y_f, "{:,.1f}")
    bad_after_delta(("قبل (i*)", "بعد (i*)", "Δi"), eq0["i"], i_f, "{:.3f}")
    st.plotly_chart(
        plot_is_lm(is_f, lm_f, eq_f, bp_params=bp_params,
                   is2_params=is_shock if fiscal and not (regime == "ثابت") else None,
                   is3_params=is0 if fiscal else None,
                   lm2_params=lm_shock if (not fiscal and regime == "ثابت") else None,
                   lm3_params=lm0 if not fiscal else None),
        use_container_width=True)
    st.markdown(
        f"| | قبل | بعد التعديل | الاقتصاد المغلق (بدون BP) |\n"
        f"|---|---|---|---|\n"
        f"| Y | {eq0['Y']:,.1f} | **{y_f:,.1f}** | {eq0['Y'] + closed_Y:,.1f} |\n"
        f"| ΔY | — | {y_f - eq0['Y']:+,.1f} | {closed_Y:+,.1f} |",
        unsafe_allow_html=True,
    )

quiz("5_3")