"""الدرس 3.2 — التوازن في اقتصاد قطاعين: Y = C + I = a + bY + I0."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_dual_income
from utils.rtl import inject_rtl
from utils.solvers import keynesian_multipliers
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="التوازن في اقتصاد قطاعين", page_icon="2️⃣", layout="wide")
inject_rtl()
mark_visited("3_2")

lesson_header(
    "2️⃣",
    "التوازن في اقتصاد قطاعين (الأسر والشركات)",
    "التوازن حيث الإنفاق الكلي يساوي الناتج: Y=C+I، وأيضًا حيث الادخار يساوي "
    "الاستثمار S=I. حرّك السلايدرات وشاهد تغيّر نقطة التوازن إزاء الصيغة المغلقة.",
)

st.latex(r"Y^* = \frac{1}{1-b}(a + I_0) \ \ \ \ \text{حيث التوازن: } S = I \iff Y^* - C = I_0")

with st.container(border=True):
    st.markdown("#### 🎚️ المعطيات")
    c1, c2, c3 = st.columns(3)
    a = c1.slider("الاستهلاك الذاتي a", 0, 200, 100, 5)
    b = c2.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
    I0 = c3.slider("الاستثمار المستقل I₀", 0, 300, 50, 5)

    ke = keynesian_multipliers(b)["Ke_A"]
    Y_star = ke * (a + I0)

    m1, m2, m3 = st.columns(3)
    m1.metric("المضاعف Ke = 1/(1−b)", f"{ke:.2f}")
    m2.metric("الدخل التوازني Y*", f"{Y_star:,.2f}")
    m3.metric("الادخار عند التوازن S = I", f"{I0:,.2f}")

    st.markdown("#### 📊 الرسم المزدوج")
    fig = plot_dual_income(
        ad_slope=b, ad_intercept=a + I0, y_star=Y_star,
        leak_intercept=-a, leak_slope=1 - b,
        inj_intercept=I0, inj_slope=0.0,
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.success(f"Y* = 1/(1−{b}) × ({a} + {I0}) = **{Y_star:,.2f}**. "
                   f"عند هذا المستوى: C = {a + b*Y_star:,.2f} و S = {I0:,.2f} = I₀ ✓")
    st.caption("مثال مرجعي متحقّق: a=100, b=0.8, I0=50 → Y* = 750 بالضبط.")

quiz("3_2")