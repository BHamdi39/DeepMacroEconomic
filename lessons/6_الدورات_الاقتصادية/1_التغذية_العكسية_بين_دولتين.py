"""الدرس 6.1 — التغذية العكسية بين دولتين: كل واردات A هي صادرات B والعكس."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_two_country
from utils.rtl import inject_rtl
from utils.solvers import two_country_feedback
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="التغذية العكسية بين دولتين", page_icon="🔁", layout="wide")
inject_rtl()
mark_visited("6_1")

lesson_header(
    "🔁",
    "التغذية العكسية وآثار الصفقات التجارية بين دولتين",
"صدمة إنفاق في الدولة A ترفع وارداتها من B، فترتفع صادرات B ودخلها، فتزيد "
    "واردات B من A، وهكذا دواليك حتى التقارب. هذه التغذية العكسية تجعل المضاعف "
    "الفعلي لـ A أصغر من مضاعف الاقتصاد المغلق لأن جزءًا من كل صدمة يتسرب "
    "عبرها إلى الخارج.",
)

math_frame(
    "نظام الدولتين (كلاهما اقتصاد مفتوح)",
    r"\Delta Y_A = m_A\!\cdot\!\Delta Y_B + \Delta A_0,\qquad "
    r"\Delta Y_B = m_B\!\cdot\!\Delta Y_A",
    "تتقاطع الاستجابات تكرارًا (A→B→A→...) حتى التقارب، والمضاعف المحقَّق "
    "يبلغ 1/(1−cA+mA·mB) تقريبًا.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات الدولتين")
    c1, c2, c3, c4 = st.columns(4)
    cA = c1.slider("الميل الحدي للاستهلاك في A (cA)", 0.40, 0.95, 0.80, 0.01)
    cB = c2.slider("الميل الحدي للاستهلاك في B (cB)", 0.40, 0.95, 0.80, 0.01)
    mA = c3.slider("الميل الحدي للاستيراد في A (mA)", 0.05, 0.50, 0.20, 0.01)
    mB = c4.slider("الميل الحدي للاستيراد في B (mB)", 0.05, 0.50, 0.15, 0.01)
    delta_A = st.slider("صدمة الإنفاق المستقل في A (ΔA₀)", 50.0, 500.0, 100.0, 10.0)

    out = two_country_feedback(mA, mB, cA, cB, delta_A)
    st.plotly_chart(plot_two_country(out["pathA"], out["pathB"]),
                    use_container_width=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("الدخل النهائي في A (ΔY_A)", f"{out['final_A']:,.2f}")
    k2.metric("مضاعف الاقتصاد المغلق لـ A", f"{out['closed_A']:,.2f}")
    k3.metric("التسرب عبر التغذية العكسية", f"{out['leakage']:,.2f}",
              delta=f"{100 * out['leakage'] / out['closed_A']:.1f}% من الأثر")
    k4.metric("عدد الجولات حتى التقارب", f"{out['rounds_run']}")

    st.info(
        f"لو كانت A اقتصادًا مغلقًا لكانت الصدمة تؤدي إلى **ΔY = "
        f"{out['closed_A']:,.1f}**. لكن لأن الواردات تتسرب (mA = {mA:.2f}) ثم "
        f"يعود جزء عبر واردات B (mB = {mB:.2f})، فإن الصافي النهائي "
        f"**{out['final_A']:,.1f}** أقل — هذا هو جوهر التسرب عبر التغذية العكسية."
    )

quiz("6_1")