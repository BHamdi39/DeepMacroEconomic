"""الدرس 3.4 — التوازن في اقتصاد أربع قطاعات (قطاع العالم الخارجي)."""
from __future__ import annotations

import numpy as np
import streamlit as st

from utils.plotting import plot_dual_income, plot_nx
from utils.rtl import inject_rtl
from utils.solvers import four_sector_equilibrium
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="التوازن في أربع قطاعات", page_icon="4️⃣", layout="wide")
inject_rtl()
mark_visited("3_4")

lesson_header(
    "4️⃣",
    "التوازن في اقتصاد أربع قطاعات (اقتصاد مفتوح)",
    "إضافة قطاع العالم الخارجي: صادرات مستقلة X0 وواردات M0+mY. الميل الحدي "
    "للاستيراد m تسريب إضافي يُضعف المضاعف: Ke=1/(1−b+bt+m).",
)

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
    c7, c8, c9 = st.columns(3)
    X0 = c7.slider("الصادرات المستقلة X₀", 0, 200, 90, 5)
    M0 = c8.slider("الواردات المستقلة M₀", 0, 200, 50, 5)
    m = c9.slider("الميل الحدي للاستيراد m", 0.05, 0.40, 0.20, 0.01)

    eq = four_sector_equilibrium(a, b, I0, G0, T0, R0, X0, M0, t=0.0, m=m)
    st.session_state["y_star_4sector"] = eq["Y"]  # يقرأه درس 3.8
    st.session_state["params_4sector"] = {"X0": X0, "M0": M0, "m": m}

    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("مضاعف الاقتصاد المغلق", f"{eq['Ke_closed']:.2f}")
    m2.metric("مضاعف الاقتصاد المفتوح Ke", f"{eq['Ke_open']:.2f}")
    m3.metric("الدخل التوازني Y*", f"{eq['Y']:,.2f}")
    nx0 = X0 - M0 - m * eq["Y"]
    m4.metric("الميزان التجاري NX عند Y*", f"{nx0:,.2f}")

    st.markdown("#### 📊 الرسم المزدوج + الميزان التجاري")
    cA, cB = st.columns([2, 1])
    with cA:
        fig = plot_dual_income(
            ad_slope=b, ad_intercept=a + I0 + G0 - b * T0 + b * R0 + X0 - M0,
            y_star=eq["Y"],
            leak_intercept=-a + b * T0 + (1 - b) * R0 + M0,
            leak_slope=1 - b + m,
            inj_intercept=I0 + G0 + R0 + X0,
        )
        st.plotly_chart(fig, use_container_width=True)
    with cB:
        yp = np.linspace(0, eq["Y"] * 2, 300)
        nxp = X0 - M0 - m * yp
        fig2 = plot_nx(yp, nxp, eq["Y"])
        st.plotly_chart(fig2, use_container_width=True)

    st.info(f"مضاعف الاقتصاد المفتوح {eq['Ke_open']:.2f} أصغر من المغلق "
            f"{eq['Ke_closed']:.2f} بفضل تسريب m={m:.2f}.")

st.latex(r"Y^* = \frac{1}{1-b+bt+m}\,[a+I_0+G_0-bT_0+bR_0+X_0-M_0] \ \ \ \ NX = X_0-M_0-mY")

quiz("3_4")