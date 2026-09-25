"""الدرس 5.2 — منحنى BP والتوازن الثلاثي: تصنيف فائض/عجز ميزان المدفوعات."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_is_lm
from utils.rtl import inject_rtl
from utils.solvers import bp_curve, is_lm_bp_equilibrium, lm_curve, x0_neutral_bp
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="التوازن الداخلي والخارجي", page_icon="🔺", layout="wide")
inject_rtl()
mark_visited("5_2")

lesson_header(
    "🔺",
    "التوازن الداخلي والخارجي (منحنى BP)",
    "منحنى BP يجمع توافيق (Y, i) التي يوازن عندها ميزان المدفوعات NX + CF = 0. "
    "ميله = m/κ: حركة رأس مال قوية تجعله شبه أفقي عند i*، وحركة منعدمة تجعله "
    "شبه عمودي. التوازن الثلاثي عند تقاطع IS و LM و BP جميعًا.",
)

math_frame(
    "معادلة منحنى BP",
    r"i = i^* + \frac{m}{\kappa}\,Y - \frac{X_0 - M_0}{\kappa}",
    "استخلصت من NX + CF = 0 مع CF = κ(i−i*). الميل m/κ يعكس مرتبتين: مرونة "
    "الاستيراد مقابل حركة رأس المال.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات IS-LM-BP")
    c1, c2, c3, c4 = st.columns(4)
    b = c1.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
    A0 = c2.number_input("الإنفاق المستقل الكلي A", 100.0, 1500.0, 600.0, 10.0)
    mu = c3.slider("حساسية الاستثمار للفائدة µ", 1.0, 30.0, 10.0, 0.5)
    Ms = c4.number_input("عرض النقود Mₛ", 50.0, 1000.0, 400.0, 10.0)

    c5, c6, c7 = st.columns(3)
    Q = c5.number_input("الطلب الذاتي Q", 0.0, 500.0, 100.0, 10.0)
    alpha = c6.slider("حساسية الطلب للدخل α", 0.1, 1.2, 0.60, 0.05)
    g = c6.slider("حساسية الطلب المضاربي g", 1.0, 300.0, 30.0, 1.0)

    c8, c9, c10, c11 = st.columns(4)
    X0 = c8.number_input("الصادرات المستقلة X₀", 0.0, 300.0, 150.0, 5.0)
    M0 = c9.number_input("الواردات المستقلة M₀", 0.0, 300.0, 100.0, 5.0)
    m = c10.slider("الميل الحدي للاستيراد m", 0.05, 0.50, 0.15, 0.01)
    kappa = c11.slider("درجة حركة رأس المال κ", 0.5, 50.0, 15.0, 0.5)

    i_world = st.slider("سعر الفائدة العالمي i*%", 0.0, 20.0, 4.0, 0.1)

    Ke = 1 / (1 - b)
    is_params = {"Ke": Ke, "A": A0, "mu": mu}
    lm_params = lm_curve(Q, alpha, g, Ms)
    bp_params = bp_curve(X0, M0, m, kappa, i_world)
    out = is_lm_bp_equilibrium(is_params, lm_params, X0, M0, m, kappa, i_world)

    tilt = "شبه أفقي (حركة رأس مال قوية)" if bp_params["slope"] < 0.02 else \
           ("شبه عمودي (حركة رأس مال شبه منعدمة)" if bp_params["slope"] > 0.5 else "بميل معتدل")
    st.progress(max(0.0, min(1.0, bp_params["slope"] / 0.6)),
                text=f"ميل منحنى BP = m/κ = {bp_params['slope']:.4f} — {tilt}")

    st.plotly_chart(plot_is_lm(is_params, lm_params, {"Y": out["Y"], "i": out["i"]},
                               bp_params=bp_params), use_container_width=True)

    if out["i"] - out["i_bp"] > 1e-9:
        st.warning(f"النقطة ({out['Y']:,.1f}, {out['i']:.2f}%) تقع **فوق** BP ⇒ "
                   f"فائض (i أعلى من المطلوب لجذب رؤوس أموال تغطي العجز التجاري).")
    elif out["i"] - out["i_bp"] < -1e-9:
        st.warning(f"النقطة ({out['Y']:,.1f}, {out['i']:.2f}%) تقع **تحت** BP ⇒ "
                   f"عجز في ميزان المدفوعات.")
    else:
        st.success("التوازن الثلاثي محقق بالضبط.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("الدخل Y*", f"{out['Y']:,.1f}")
    m2.metric("سعر الفائدة i*", f"{out['i']:.3f}%")
    m3.metric("عند هذا Y المطلوب i_BP", f"{out['i_bp']:.3f}%")
    m4.metric("رصيد BP", f"{out['balance']:+,.2f}")

    x_neutral = x0_neutral_bp(is_params, lm_params, M0, m, kappa, i_world)
    st.caption(f"لتحقيق التوازن الثلاثي بالضبط عند هذه النقطة يلزم X₀ = "
               f"**{x_neutral:,.1f}** (الصادرات المحايدة BP).")

quiz("5_2")