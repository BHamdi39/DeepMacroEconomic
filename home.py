"""مختبر الاقتصاد الكلي المعمّق — الصفحة الرئيسية (لوحة القيادة)."""
from __future__ import annotations

import streamlit as st

from utils.modules import MODULES, module_visited
from utils.rtl import inject_rtl
from utils.ui import flow, progress_block, visited_count, visited_set

TOTAL_LESSONS = 25

st.set_page_config(
    page_title="مختبر الاقتصاد الكلي المعمّق",
    page_icon="🏛️",
    layout="wide",
    menu_items={
        "About": "مختبر تفاعلي لتعلّم الاقتصاد الكلي المعمّق — من الحسابات الوطنية إلى IS-LM-BP ونماذج النمو.",
    },
)

inject_rtl()

# إخفاء الشريط العلوي العام في لوحة القيادة (يتكرر مع عنوان الصفحة ورابط البطاقة)
st.markdown("<style>.toolbar { display: none !important; }</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="top-shell">
      <div class="topbar">
        <div class="topbar-left"></div>
        <div class="topbar-center">
          <h1 class="page-title">مختبر الاقتصاد الكلي المعمّق</h1>
        </div>
      </div>
      <div class="hero-panel">
        <p class="hero-sub">
          قاعدة نظرية <b>+ محاكي تفاعلي</b> لكل مفهوم في المقرر، مع شرح رياضيّ واضح،
          منحنيات تفاعلية، واختبارات فورية تعزّز الفهم بدل الحفظ.
        </p>
        <div class="hero-chips">
          <span class="nav-pill">منحنيات تفاعلية</span>
          <span class="nav-pill">نماذج قابلة للمحاكاة</span>
          <span class="nav-pill">اختبارات فورية</span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

flow(["الفكرة", "الإطار الرياضي", "المحاكي التفاعلي", "اختبر فهمك"])

# ---- بطاقات القياس (حالة، لا زخرفة) ----
visited = visited_set()
c1, c2, c3, c4 = st.columns(4, gap="small")
c1.metric("الوحدات", "7", help="عدد الوحدات في المقرر")
c2.metric("الدروس", TOTAL_LESSONS, help="إجمالي الدروس التفاعلية")
c3.metric("الدروس المزارة", f"{visited_count()}", help="عدد الدروس التي فتحتها")
c4.metric(
    "نسبة الإنجاز", f"{len(visited) / TOTAL_LESSONS * 100:.0f}%",
    help="التقدّم الكلي في المقرر",
)

progress_block()

st.markdown("### الوحدات السبع للمقرر")
module_cards = []
for prefix, name, desc, total, _pages in MODULES:
    n = module_visited(prefix, total)
    completed = n == total
    pct = n / total
    score_text = "مكتملة ✓" if completed else f"{n} من {total}"
    card = f'''
    <div class="unit-card">
      <div class="unit-card-head">
        <div class="unit-card-title">{name}</div>
        <div class="unit-score {'done' if completed else ''}">{score_text}</div>
      </div>
      <div class="unit-card-body">{desc}</div>
      <div class="unit-bar-wrap">
        <div class="unit-bar" style="width:{pct * 100:.0f}%"></div>
      </div>
    </div>
    '''
    module_cards.append(card)

st.markdown("\n".join(module_cards), unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "ابدأ من <b>القائمة الجانبية</b>: اختر وحدة ثم درسًا، واتبع البنية الثابتة الموضحة أعلى الصفحة — "
    "الفكرة، الإطار الرياضي، المحاكي التفاعلي، ثم اختبار الفهم.",
    unsafe_allow_html=True,
)
st.caption("حالة الإنجاز لكل درس تُسجَّل محليًا في متصفحك مباشرةً.")

scores = st.session_state.get("quiz_scores", {})
if scores:
    total_correct = sum(v["correct"] for v in scores.values())
    total_answered = sum(v["answered"] for v in scores.values())
    success_rate = (total_correct / total_answered * 100) if total_answered else 0.0
    with st.container(border=True):
        st.markdown("### 📊 ملخص نتائج الاختبارات")
        st.markdown(
            f"أجبت على **{total_answered}** سؤالًا بنجاح {total_correct} (معدل "
            f"{success_rate:.0f}%) من أصل "
            f"{visited_count()} درسًا زرته."
        )
        st.caption("توجد الاختبارات داخل كل درس في قاع الصفحة.")