"""الدرس 7.2 — النمو الداخلي: رومر، لوكاس، وأكيلانو-هاويت."""
from __future__ import annotations

import numpy as np
import streamlit as st

from utils.plotting import growth_curves
from utils.rtl import inject_rtl
from utils.solvers import endogenous_growth
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="نماذج النمو الداخلي", page_icon="🧬", layout="wide")
inject_rtl()
mark_visited("7_2")

lesson_header(
    "🧬",
    "نماذج النمو الداخلي",
    "بخلاف سولو الذي يرى التقارب الحتمي، تؤكد النظرية الداخلية أن المعرفة "
    "(رومر)، ورأس المال البشري (لوكاس)، والبحث والابتكار (أكيلانو-هاويت) "
    "تحمل عوائد تصاعدية — فالنمو لا يتوقف بل يتجدد من داخل الاقتصاد نفسه.",
)

math_frame(
    "دوال الإنتاج الثلاث",
    r"\text{رومر: } Y = A\,K^{\alpha}L^{1-\alpha},\qquad"
    r"\text{لوكاس: } Y = A\,K^{\alpha}(L\,H)^{\beta},\qquad"
    r"\text{أكيلانو-هاويت: } Y = A\,K^{\alpha}L^{1-\alpha}",
    "الفرق الجوهري أن التكنولوجيا A والرأسمال البشري H محقّقان داخليًا "
    "بالاستثمار في البحث والتعليم.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات عوامل الإنتاج")
    c1, c2, c3, c4 = st.columns(4)
    A = c1.number_input("التكنولوجيا A", 0.5, 10.0, 2.0, 0.1)
    K = c2.number_input("رأس المال K", 10.0, 500.0, 100.0, 5.0)
    L = c3.number_input("العمل L", 10.0, 500.0, 50.0, 5.0)
    H = c4.number_input("رأس المال البشري H", 0.5, 5.0, 1.5, 0.1)

    c5, c6, c7 = st.columns(3)
    alpha = c5.slider("مرونة رأس المال α", 0.20, 0.80, 0.50, 0.01)
    beta = c6.slider("مرونة العمل البشري β (لوكاس)", 0.30, 0.90, 0.70, 0.01)
    model = c7.radio("النموذج", ["رومر", "لوكاس", "أكيلانو-هاويت"])

    base = endogenous_growth(model, A, K, L, H, alpha, beta)
    el = base["elasticities"]

    st.markdown(f"#### 📏 المثال في النموذج **{model}**")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("الإنتاج Y", f"{base['Y']:,.2f}")
    m2.metric("مرونة K", f"{el['K']:.2f}")
    m3.metric("مرونة العامل الأكبر", f"{el.get('L', el.get('L*H', 0.0)):.2f}")
    m4.metric("مرونة A (التكنولوجيا)", f"{el['A']:.2f}")

    st.markdown("#### 📈 حساسية Y لكل عامل (من 0.5× إلى 1.5× قاعدته)")
    scales = np.linspace(0.5, 1.5, 9)
    model_plot: dict[str, list[float]] = {"K": [], "work": [], "A": []}
    for scale in scales:
        r = endogenous_growth(model, A * scale, K, L, H, alpha, beta)
        model_plot["K"].append(r["Y"])
        r2 = endogenous_growth(model, A, K * scale, L * scale, H * scale, alpha, beta)
        model_plot["work"].append(r2["Y"])
        r3 = endogenous_growth(model, A, K, L, H * scale, alpha, beta)
        model_plot["A"].append(r3["Y"])

    labels = {"K": "رأس المال K", "work": "قوى العمل L (ورأس المال البشري H)",
              "A": "التكنولوجيا A"}
    st.plotly_chart(growth_curves(model_plot, labels), use_container_width=True)
    st.caption(
        "انحدار كل منحنى يعكس مرونة ذلك العامل في النموذج المختار — تلاحظ أن "
        "التكنولوجيا A (خط ثابت الانحدار الأعلى) هي «المحرك» الذي يجعل النمو "
        "ممكنًا بلا حدود."
    )

quiz("7_2")