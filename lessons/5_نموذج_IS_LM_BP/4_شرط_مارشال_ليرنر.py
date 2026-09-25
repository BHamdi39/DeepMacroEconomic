"""الدرس 5.4 — شرط مارشال-ليرنر: متى يُحسّن تخفيض العملة الميزان التجاري؟"""
from __future__ import annotations

import streamlit as st

from utils.plotting import bar_policy_impact
from utils.rtl import inject_rtl
from utils.solvers import marshall_lerner_check
from utils.ui import lesson_header, mark_visited, math_frame, quiz

st.set_page_config(page_title="شرط مارشال-ليرنر", page_icon="⚓", layout="wide")
inject_rtl()
mark_visited("5_4")

lesson_header(
    "⚓",
    "شرط مارشال-ليرنر",
    "تخفيض العملة يجعل الصادرات أرخص للأجانب (فيبدو كمها أعظم a) والواردات أغلى "
    "على المحليين (فينخفض كمها، مرونته b). الميزان التجاري لا يتحسن إلا إذا كان "
    "مجموع المرونتين أكبر من 1: a + b > 1.",
)

math_frame(
    "شرط مارشال-ليرنر",
    r"\underbrace{a}_{\text{مرونة الطلب الخارجي على الصادرات}} \;+\; "
    r"\underbrace{b}_{\text{مرونة الطلب المحلي على الواردات}} \;>\; 1",
    "قيمة الصادرات ترتفع بـ (a×نسبة التخفيض)، وفاتورة الواردات ترتفع فقط بـ "
    "(1−b)×نسبة التخفيض — فافتراض الشرط فائدة صافية.",
)

c1, c2 = st.columns(2)
a = c1.slider("مرونة الطلب الخارجي على الصادرات a", 0.0, 3.0, 1.1, 0.05)
b = c2.slider("مرونة الطلب المحلي على الواردات b", 0.0, 3.0, 0.7, 0.05)

ok, msg = marshall_lerner_check(a, b)
with st.container(border=True):
    st.markdown(f"#### 📐 a + b = **{a + b:.3f}**")
    if ok:
        st.success(f"✅ {msg}")
    else:
        st.error(f"❌ {msg}")

    pct = 20.0
    gain = a * pct
    loss = (1 - b) * pct
    dn = gain - loss
    st.plotly_chart(bar_policy_impact(
        ["قيمة الصادرات (ترتفع)", "فاتورة الواردات (ترتفع أقل)", "صافي الأثر على NX"],
        [gain, -loss, dn],
        f"تخفيض العملة بنسبة {pct:.0f}% بصادرات وواردات ابتدائية 100"),
        use_container_width=True)
    st.markdown(
        f"- **قيمة الصادرات** بعد التخفيض: +{gain:.2f} (a×{pct:.0f}%)\n"
        f"- **فاتورة الواردات**: تأثير السعر +{pct:.0f}% يعوّضه انكماش الكمية "
        f"(b×{pct:.0f}%) ⇒ صافي +{loss:.2f}\n"
        f"- **صافي أثر الميزان التجاري:** {gain:+.2f} − {loss:+.2f} = "
        f"**{dn:+.2f}** ({'تحسّن' if dn > 0 else 'تفاقم'})"
    )
    st.caption("المساواة الأخيرة هي أصل الشرط: التحسن يقتضي gain > loss ⇔ "
               "a·pct > (1−b)·pct ⇔ a + b > 1.")

quiz("5_4")