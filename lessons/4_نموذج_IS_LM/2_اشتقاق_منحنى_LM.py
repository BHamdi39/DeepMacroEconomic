"""الدرس 4.2 — اشتقاق منحنى LM: الطلب على النقود MD = Q + αY − gi يساوي العرض Ms."""
from __future__ import annotations

import numpy as np
import streamlit as st

from utils.plotting import plot_money_derivation, plot_is_lm
from utils.rtl import inject_rtl
from utils.solvers import lm_curve
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="اشتقاق منحنى LM", page_icon="💵", layout="wide")
inject_rtl()
mark_visited("4_2")

lesson_header(
    "💵",
    "اشتقاق منحنى LM",
    "الطلب على النقود لثلاثة دوافع: المعاملات والاحتياط (αY) والمضاربة (−gi). "
    "توازن سوق النقود MD = Ms يعطي، مقابل كل دخل، سعر فائدة يتوازن عنده "
    "السوق — وهذه النقاط تشكّل منحنى LM الصاعد.",
)

math_frame(
    "معادلة منحنى LM",
    r"MD = Q + \alpha\,Y - g\,i = M_s \;\Longrightarrow\; "
    r"Y = \frac{1}{\alpha}\,\big(M_s - Q + g\,i\big)",
    "α حساسية الطلب للدخل، و g حساسية الطلب المضاربي للفائدة، و Q الطلب الذاتي.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات سوق النقود")
    c1, c2, c3, c4 = st.columns(4)
    Q = c1.number_input("الطلب الذاتي على النقود Q", 0.0, 500.0, 100.0, 10.0)
    alpha = c2.slider("حساسية الطلب للدخل α", 0.1, 1.2, 0.60, 0.05)
    g = c3.slider("حساسية الطلب المضاربي للفائدة g", 1.0, 300.0, 30.0, 1.0)
    Ms = c4.number_input("عرض النقود Mₛ", 50.0, 1000.0, 400.0, 10.0)

    p = lm_curve(Q, alpha, g, Ms)
    st.success(f"وضع التوازن: Y = (1/{alpha:.2f}) × ({Ms:.0f} − {Q:.0f} + "
               f"{g:.0f}·i) = **{Ms - Q + g * 0:.1f} + {g / alpha:.2f}·i**")

    i_range = np.linspace(0.0, 18.0, 40)
    fig = plot_money_derivation(p, i_range)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📈 أثر زيادة الدخل على سوق النقود")
    y_demo = (Ms - Q + g * 15) / alpha
    demo = lm_curve(Q, alpha, g, Ms)
    fig2 = plot_is_lm({"Ke": 9.0, "A": 900.0, "mu": 40.0}, demo)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("الرسم العلوي يوضح كيف ينزاح طلب النقود يمينًا مع كل دخل Y أعلى، "
               "فيرتفع سعر التوازن i؛ الرسم السفلي يقلب العلاقة ليعطي LM في المستوى "
               "(Y, i). لاحظ أن نموذج الدخل في المثال أسفله دلالي فقط للتوضيح.")

quiz("4_2")