"""الدرس 3.5 — المضاعفات: كل صيغ المضاعفات السبع وأثر الصدمات مقارنةً."""
from __future__ import annotations

import streamlit as st

from utils.plotting import bar_multipliers, bar_policy_impact
from utils.rtl import inject_rtl
from utils.solvers import keynesian_multipliers, policy_shock_effect
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="المضاعفات", page_icon="5️⃣", layout="wide")
inject_rtl()
mark_visited("3_5")

lesson_header(
    "5️⃣",
    "المضاعفات",
    "كل أداة إنفاق مستقل لها مضاعف يقيس أثر صدمتها على الدخل. المضاعف العام "
    "1/(1−b+bt+m)، ومضاعف الضرائب سالب وأصغر قدرًا من مضاعف الإنفاق لأن "
    "الضريبة تُغيّر الدخل المتاح فقط بمعامل b.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ المعطيات المشتركة لكل المضاعفات")
    c1, c2, c3 = st.columns(3)
    b = c1.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
    t = c2.slider("معدل ضريبة الدخل t", 0.0, 0.40, 0.0, 0.01)
    m = c3.slider("الميل الحدي للاستيراد m", 0.0, 0.40, 0.0, 0.01)

    mult = keynesian_multipliers(b, t=t, m=m)
    rows = {
        "الإنفاق المستقل (a, I₀)": mult["Ke_A"],
        "الإنفاق الحكومي (G₀)": mult["Ke_G"],
        "الصادرات (X₀)": mult["Ke_X"],
        "الضرائب (T₀)": mult["Ke_T"],
        "التحويلات (R₀)": mult["Ke_R"],
        "الواردات (M₀)": mult["Ke_M"],
    }

    st.markdown("#### 📋 جدول المضاعفات السبعة")
    st.markdown(f"**المقام العام = 1 − b + bt + m = {mult['denom']:.4f}**")
    st.dataframe(
        {"الأداة": list(rows.keys()), "المضاعف": [f"{v:.3f}" for v in rows.values()]},
        hide_index=True, use_container_width=True,
    )

    st.markdown("#### ⚡ صدمة على أداة واحدة")
    c4, c5 = st.columns([1, 1])
    instr = c4.selectbox("الأداة المتأثرة بالصدمة", list(rows.keys()))
    delta = c5.slider("حجم الصدمة Δ (بالوحدات النقدية)", -100, 100, 20, 1)
    short = {"الإنفاق المستقل (a, I₀)": "I", "الإنفاق الحكومي (G₀)": "G",
             "الصادرات (X₀)": "X", "الضرائب (T₀)": "T",
             "التحويلات (R₀)": "R", "الواردات (M₀)": "M"}[instr]
    dY = policy_shock_effect(b, t, m, short, float(delta))
    st.success(f"ΔY = المضاعف × Δ = **{rows[instr]:.3f} × ({delta:+.0f}) = "
               f"{dY:+,.2f}**")

    st.markdown("#### 📊 مقارنة أثر صدمة بنفس المقدار عبر كل الأدوات")
    labels = list(rows.keys())
    effects = [rows[k] * float(delta) for k in labels]
    st.plotly_chart(bar_policy_impact(labels, effects,
                                      "أثر صدمة " + (f"{delta:+.0f}" ) + " على Y عبر الأدوات"),
                    use_container_width=True)
    st.plotly_chart(bar_multipliers(labels, list(rows.values()),
                                    "قيمة كل مضاعف بذاته"),
                    use_container_width=True)
    st.caption("لاحظ: مضاعف الضرائب/التحويلات أدنى من مضاعف الإنفاق المباشر — "
               "فصدمة الإنفاق (G) تُغيّر الطلب الكلي مباشرة، بينما تغيّر الضريبة "
               "الدخل المتاح فيتسرب جزء بالادخار.")

quiz("3_5")