"""الدرس 4.3 — توازن IS-LM الآني: مفتاح Θ و σ، وثلاث حالات منحنى LM."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_is_lm
from utils.rtl import inject_rtl
from utils.solvers import is_lm_equilibrium, is_lm_regions_preset, lm_curve
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="التوازن الآني وحالات منحنى LM", page_icon="⚖️", layout="wide")
inject_rtl()
mark_visited("4_3")

lesson_header(
    "⚖️",
    "التوازن الآني وحالات منحنى LM",
    "تقاطع IS و LM يحدد simultaneously الدخل (Y*) والفائدة (i*) عبر مفتاحين: "
    "Θ (المضاعف المالي) الذي يضاعف الإنفاق المستقل، و σ (المضاعف النقدي) الذي "
    "يضاعف عرض النقود. وطبيعة LM نفسها تختلف بين الكينزي الأفقي والكلاسيكي "
    "العمودي والوسيط بينهما.",
)

math_frame(
    "الصيغتان المغلقتان للتوازن",
    r"Y^* = \Theta\,A + \sigma\,\bar M_s,\qquad "
    r"i^* = \frac{\alpha}{g}\,\Theta\,A - \frac{1}{K_e\,g}\,\Theta\,\bar M_s",
    "Θ = Kₑg/(g+Kₑµα) المضاعف المالي، σ = Kₑµ/(g+Kₑµα) المضاعف النقدي، "
    "و M̄ₛ = Mₛ − Q.",
)

c1, c2, c3, c4 = st.columns(4)
b = c1.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
A0 = c2.number_input("الإنفاق المستقل الكلي A", 100.0, 1500.0, 600.0, 10.0)
mu = c3.slider("حساسية الاستثمار للفائدة µ", 1.0, 30.0, 10.0, 0.5)
Ms = c4.number_input("عرض النقود Mₛ", 50.0, 1000.0, 400.0, 10.0)

c5, c6, c7, c8 = st.columns(4)
Q = c5.number_input("الطلب الذاتي Q", 0.0, 500.0, 100.0, 10.0)
alpha = c6.slider("حساسية الطلب للدخل α", 0.1, 1.2, 0.60, 0.05)
region = c7.radio("حالة منحنى LM (قيمة g)", list(is_lm_regions_preset().keys()))
region_desc = is_lm_regions_preset()[region]
g = region_desc["g"]

Ke = 1 / (1 - b)
is_params = {"Ke": Ke, "A": A0, "mu": mu}
lm_params = lm_curve(Q, alpha, g, Ms)
eq = is_lm_equilibrium(is_params, lm_params)

with st.container(border=True):
    st.markdown(f"#### 🏷️ المنطقة المختارة: {region}")
    st.info(region_desc["desc"])
    st.markdown(
        r"**IS:** $Y = K_e[A - \mu i] = " + f"{Ke:.3f} \\times ({A0:.0f} - "
        f"{mu:.0f}\\,i)" + r"$،  "
        r"**LM:** $Y = \\frac{1}{\\alpha}(M_s - Q + g\\,i) = "
        f"({Ms:.0f} - {Q:.0f} + {g:.0f}\\,i)/{alpha:.2f}" + r"$"
    )
    st.plotly_chart(plot_is_lm(is_params, lm_params, eq), use_container_width=True)

    st.markdown("#### 🔑 القراءات العددية")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("مضاعف المالي Θ", f"{eq['Theta']:.4f}")
    m2.metric("المضاعف النقدي σ", f"{eq['sigma']:.4f}")
    m3.metric("الدخل التوازني Y*", f"{eq['Y']:,.1f}")
    m4.metric("سعر الفائدة i*", f"{eq['i']:.3f}%")
    st.markdown(
        f"$Y^* = \\Theta\\,A + \\sigma\\bar M_s = "
        f"{eq['Theta']:.3f}\\times{A0:.0f} + {eq['sigma']:.3f}\\times"
        f"({Ms - Q:.0f}) = {eq['Y']:,.1f}$"
    )

quiz("4_3")