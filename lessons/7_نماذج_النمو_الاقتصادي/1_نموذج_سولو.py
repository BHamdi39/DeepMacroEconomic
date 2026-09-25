"""الدرس 7.1 — نموذج سولو: حالة الاستقرار والمسار الزمني لرأس المال."""
from __future__ import annotations

import streamlit as st

from utils.plotting import plot_solow
from utils.rtl import inject_rtl
from utils.solvers import solow_path, solow_steady_state
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="نموذج سولو", page_icon="🛠️", layout="wide")
inject_rtl()
mark_visited("7_1")

lesson_header(
    "🛠️",
    "نموذج سولو للنمو",
    "التراكم الرأسمالي (sf(k)) يصطدم بالاستنزاف (δ+n)k. نقطة التلاقي هي حالة "
    "الاستقرار k* حيث يتوقف k عن التغير — وكل ما يرفع معدل الادخار s أو يخفض "
    "النمو السكاني n يرفع k* ومعه الإنتاج قرب العامل.",
)

math_frame(
    "معادلة التراكم وحالة الاستقرار",
    r"\Delta k = s\,f(k) - (\delta + n)\,k,\qquad "
    r"k^{*} = \left(\frac{s}{\delta + n}\right)^{1/(1-\alpha)}",
    "k يدور نحو k* لأن sf(k) تتقاطع مع خط الاستنزاف أسفلها قرب الصفر وفوقه عند الكبر.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات النموذج")
    c1, c2, c3, c4, c5 = st.columns(5)
    s = c1.slider("معدل الادخار s", 0.05, 0.60, 0.30, 0.01)
    delta = c2.slider("معدل الاستهلاك رأس المال δ", 0.0, 0.20, 0.05, 0.005)
    n = c3.slider("نمو السكان n", 0.0, 0.15, 0.02, 0.005)
    alpha = c4.slider("مرونة رأس المال α", 0.10, 0.60, 1/3, 0.01)
    k0 = c5.slider("رأس المال الابتدائي k₀", 0.5, 40.0, 2.0, 0.5)

    k_star = solow_steady_state(s, delta, n, alpha)
    ks, ys = solow_path(k0, s, delta, n, alpha)

    st.plotly_chart(plot_solow(s, delta, n, alpha, k_star, ks), use_container_width=True)

    y_star = k_star ** alpha
    c_star = (1 - s) * y_star
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("رأس المال حالة الاستقرار k*", f"{k_star:.3f}")
    m2.metric("الإنتاج للعامل y*", f"{y_star:.3f}")
    m3.metric("الاستهلاك للعامل c*", f"{c_star:.3f}",
              delta="(1−s)·y*")
    m4.metric("رأس المال الحالي k₀", f"{k0:.1f}")

    st.caption(
        "إن كان k₀ < k* فالاقتصاد يتراكم ويقِترب من k* صاعدًا؛ وإن كان k₀ > k* "
        "فالنمو سالب يعود إلى الاستقرار. في حالة الاستقرار تكون sf(k) = (δ+n)k "
        "مساوية تمامًا."
    )

quiz("7_1")