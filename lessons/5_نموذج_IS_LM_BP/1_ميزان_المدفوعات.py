"""الدرس 5.1 — ميزان المدفوعات: الحساب الجاري (NX) وحساب رأس المال (CF)."""
from __future__ import annotations

import streamlit as st

from utils.plotting import bar_policy_impact
from utils.rtl import inject_rtl
from utils.solvers import marshall_lerner_check
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="ميزان المدفوعات", page_icon="💱", layout="wide")
inject_rtl()
mark_visited("5_1")

lesson_header(
    "💱",
    "ميزان المدفوعات",
    "يسجّل ميزان المدفوعات كل معاملات الدولة مع الخارج: فالحساب الجاري (NX = X − M) "
    "يتراجع مع ارتفاع الدخل، وحساب رأس المال يتفاعل مع فارق الفائدة. توازن الميزان "
    "يتطلب معً ا أن يغطي أحدهما الآخر قبالة العالم.",
)

math_frame(
    "مكوّنا ميزان المدفوعات",
    r"NX = X - M = X_0 - M_0 - m\,Y,\qquad BP = NX + CF",
    "X الصادرات (مستقلة أوليًا)، M الواردات (تزداد مع Y)، و CF حساب رأس المال.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات التجارة مع الخارج")
    c1, c2, c3 = st.columns(3)
    X0 = c1.number_input("الصادرات المستقلة X₀", 0.0, 300.0, 150.0, 5.0)
    M0 = c2.number_input("الواردات المستقلة M₀", 0.0, 300.0, 100.0, 5.0)
    m = c3.slider("الميل الحدي للاستيراد m", 0.0, 0.50, 0.20, 0.01)

    c4, c5 = st.columns(2)
    Y = c4.slider("مستوى الدخل Y", 100.0, 2000.0, 800.0, 10.0)
    i = c5.slider("سعر الفائدة i%", 0.0, 20.0, 6.0, 0.5)

    dY = 100.0
    NX = X0 - M0 - m * Y
    NX2 = X0 - M0 - m * (Y + dY)
    st.success(f"**NX = {X0:.0f} − {M0:.0f} − {m:.2f}×{Y:.0f} = {NX:+,.2f}**")
    st.info(f"عند رفع الدخل بـ {dY:.0f} ينخفض الميزان بـ −m·ΔY = "
            f"**{NX2 - NX:+.2f}** (من {NX:+,.2f} إلى {NX2:+,.2f}) — التسرب عبر الاستيراد.")
    st.plotly_chart(bar_policy_impact(["NX الحالي", "NX بعد +ΔY"], [NX, NX2],
                                      "أثر ارتفاع الدخل على الميزان التجاري"),
                    use_container_width=True)

st.markdown("#### 🌐 الحساب الجاري وحساب رأس المال")
with st.container(border=True):
    c6, c7 = st.columns(2)
    i_world = c6.slider("سعر الفائدة العالمي i*%", 0.0, 20.0, 4.0, 0.5)
    kappa = c7.slider("حساسية حركة رأس المال للفارق κ", 0.0, 50.0, 15.0, 1.0)

    NX_ = X0 - M0 - m * Y
    CF = kappa * (i - i_world)
    BP = NX_ + CF
    j1, j2, j3 = st.columns(3)
    j1.metric("الميزان التجاري NX", f"{NX_:+,.2f}")
    j2.metric("حساب رأس المال CF", f"{CF:+,.2f}", delta=f"κ(i−i*)={kappa:.0f}×({i:.0f}−{i_world:.0f})")
    j3.metric("ميزان المدفوعات BP", f"{BP:+,.2f}",
              delta="فائض" if BP > 0.001 else ("عجز" if BP < -0.001 else "متوازن"))
    st.caption("فارق فائدة موجب يجذب رؤوس أموال فأفقرة CF>0 — تمامًا كآلية "
               "موندل-فليمنغ عند تحليل فاعلية السياسات.")

quiz("5_1")

st.divider()
st.markdown("#### 🧠 ربط بالدرس القادم")
st.markdown("منحنى BP في الدرس 5.2 هو أثر نقاط (Y, i) التي تجعل BP = 0 — "
            "أي ميله = m/κ: كلما زادت حركة رأس المال صار أكثر أفقية عند i*.")