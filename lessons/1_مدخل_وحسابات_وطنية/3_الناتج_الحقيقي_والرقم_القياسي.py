"""الدرس 1.3 — الناتج الحقيقي والرقم القياسي: الاسمي/الحقيقي/معامل الانكماش."""
from __future__ import annotations

import streamlit as st

from utils.rtl import inject_rtl
from utils.solvers import real_nominal_gdp
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="الناتج الحقيقي والرقم القياسي", page_icon="3️⃣", layout="wide")
inject_rtl()
mark_visited("1_3")

lesson_header(
    "3️⃣",
    "الناتج الحقيقي والرقم القياسي",
    "الناتج الاسمي يقاس بأسعار السنة الجارية فيخلط الكمية بالسعر؛ الناتج "
    "الحقيقي يقيس الكميات بأسعار سنة أساس فيعزل النمو الفعلي عن التضخم، "
    "ومعامل الانكماش يبيّن مقدار ارتفاع الأسعار.",
)

st.latex(r"\text{الاسمي} = \sum p_{t}\cdot q_{t} \ \ \ \ \ \text{الحقيقي} = \sum p_{0}\cdot q_{t} \ \ \ \ \ \text{الانكماش الضمني} = \frac{\text{الاسمي}}{\text{الحقيقي}} \times 100")

GOODS = ["السلعة أ", "السلعة ب", "السلعة ج"]

with st.container(border=True):
    st.markdown("#### 🎚️ حدّد الأسعار والكميات")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**سنة الأساس (0)**")
        p0 = {g: st.slider(f"سعر {g} — الأساس", 20, 100, (i + 1) * 30, key=f"p0_{g}")
              for i, g in enumerate(GOODS)}
        q0 = {g: st.slider(f"كمية {g} — الأساس", 10, 200, (i + 1) * 60, key=f"q0_{g}")
              for i, g in enumerate(GOODS)}
    with c2:
        st.markdown("**سنة المقارنة (t)**")
        p1 = {g: st.slider(f"سعر {g} — المقارنة", 20, 100, (i + 2) * 35, key=f"p1_{g}")
              for i, g in enumerate(GOODS)}
        q1 = {g: st.slider(f"كمية {g} — المقارنة", 10, 200, (i + 1) * 70, key=f"q1_{g}")
              for i, g in enumerate(GOODS)}

    base = real_nominal_gdp(q0, p0, p0)          # سنة الأساس: الاسمي = الحقيقي
    year = real_nominal_gdp(q1, p0, p1)          # سنة المقارنة
    real_growth = (year["real"] / base["real"] - 1) * 100
    nominal_growth = (year["nominal"] / base["nominal"] - 1) * 100

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("الناتج الاسمي (سنة الأساس)", f"{base['nominal']:,.0f}")
    m2.metric("الناتج الاسمي (المقارنة)", f"{year['nominal']:,.0f}",
              f"{nominal_growth:+.1f}%")
    m3.metric("الناتج الحقيقي (أسعار الأساس)", f"{year['real']:,.0f}",
              f"{real_growth:+.1f}%")
    m4.metric("معامل الانكماش الضمني", f"{year['deflator']:.1f}",
              f"{year['deflator'] - 100:+.1f} نقطة")

    with st.container(border=True):
        if real_growth >= 0:
            st.success(f"الناتج الحقيقي ارتفع بنسبة **{real_growth:.1f}%** — نمو فعلي "
                       "في الكميات المنتجة.")
        else:
            st.error(f"الناتج الحقيقي انخفض بنسبة **{real_growth:.1f}%**.")
        inflation = year["deflator"] - 100
        if inflation > 0:
            st.info(f"معامل الانكماش **{year['deflator']:.1f}** يعني ارتفاعًا في "
                    "مستوى الأسعار بنسبة **{:.1f}%** منذ سنة الأساس.".format(inflation))
        elif inflation < 0:
            st.info("الانكماش الضمني أقل من 100: الأسعار انخفضت مقارنة بسنة الأساس.")
        else:
            st.info("لا تغيّر في مستوى الأسعار بين السنتين.")
        ratio = year["nominal"] / year["real"] if year["real"] else 0
        st.caption(f"نسبة الاسمي إلى الحقيقي = {ratio:.3f} — أي أن كل وحدة ناتج "
                   f"حقيقي تُقيَّم بـ {year['deflator']:.0f}% من سعر سنة الأساس.")

quiz("1_3")