"""مكوّنات واجهة موحّدة لكل صفحة درس: فكرة → إطار رياضي → محاكي → اختبر فهمك.

تشمل أيضًا تتبّع تقدّم المستخدم (الزيارات) وتخزين نتائج الاختبارات في
st.session_state (يملأ PRD §7 و §9 ويحقق البند 11 من سلسلة البرومبتات).
"""
from __future__ import annotations

import random

import streamlit as st

from utils.rtl import COLORS


def _shuffle_options(page_key: str, idx: int, options: list[str],
                     answer_id: int) -> tuple[list[str], int]:
    """خلط توليدي مستقر لخيارات السؤال حتى لا تكون الإجابة الصحيحة دائمًا الأولى.

    تُشتق البذرة من مفتاح الدرس ورقم السؤال، فيبقى الترتيب ثابتًا عبر
    إعادة التشغيل دون الحاجة إلى تغيير بيانات البنك.
    """
    rng = random.Random(f"{page_key}:{idx}")
    order = list(range(len(options)))
    rng.shuffle(order)
    shuffled = [options[p] for p in order]
    return shuffled, order.index(answer_id)


def mark_visited(page_key: str) -> None:
    """يسجّل زيارة المستخدم للصفحة الحالية لتتبّع التقدّم."""
    visited = st.session_state.setdefault("visited_pages", set())
    if isinstance(visited, set):
        visited.add(page_key)
        st.session_state["visited_pages"] = visited


def visited_count() -> int:
    return len(st.session_state.get("visited_pages", set()))


ALL_PAGES: dict[str, str] = {}


def lesson_header(emoji: str, title: str, idea: str) -> None:
    """رأس الدرس: عنوان + بطاقة فكرة مختصرة."""
    st.markdown(
        f"""
        <div class="lesson-shell">
          <div class="lesson-topbar">
            <span class="lesson-badge">{emoji}</span>
            <span class="lesson-kicker">محتوى الدرس</span>
          </div>
          <h2 class="lesson-title">{title}</h2>
          <div class="idea-card">
            <b>الفكرة في سطرين:</b> {idea}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def flow(steps: list[str]) -> None:
    """شريط تسلسل الدرس بأسهم RTL نحو اليسار (فكرة ◄ إطار ◄ محاكي ◄ اختبار)."""
    parts: list[str] = []
    for i, step in enumerate(steps):
        if i:
            parts.append('<span class="flow-arrow">◄</span>')
        parts.append(f'<span class="flow-step">{step}</span>')
    st.markdown(f'<div class="flow">{"".join(parts)}</div>', unsafe_allow_html=True)


def math_frame(title: str, latex: str, note: str | None = None) -> None:
    """إطار رياضي بخلفية بيضاء يضم الصيغة الرئيسية للدرس."""
    with st.container(border=True):
        st.markdown(f'<div class="math-title">{title}</div>', unsafe_allow_html=True)
        st.latex(latex)
        if note:
            st.caption(note)


def bad_after_delta(labels: tuple[str, str, str], before: float, after: float,
                    fmt: str = "{:,.2f}") -> None:
    """لوحة "قبل / بعد / الفرق Δ" الثابتة أعلى رسوم صفحات السياسات (قسم 7 PRD)."""
    b, a, d = labels
    st.markdown(
        f"""
        <div class="badge-panel">
          <div class="badge before">{b}<br>{fmt.format(before)}</div>
          <div class="badge after">{a}<br>{fmt.format(after)}</div>
          <div class="badge delta">{d}<br>{fmt.format(after - before)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def quiz(page_key: str, questions: list | None = None) -> None:
    """أختبر فهمك: أسئلة اختيار من متعدد لكل درس.

    يقرأ الأسئلة من مستودع الأسئلة المركزي (QUIZ_BANK) ما لم تُمرَّر قائمة
    مضمنة (صيغة قديمة من 3 عناصر). مع كل إجابة يُكشف التصحيح والتعليل،
    وتُحفظ النتيجة في st.session_state.
    """
    if questions is None:
        from utils.questions import QUIZ_BANK
        questions = QUIZ_BANK.get(page_key, [])
    scores = st.session_state.setdefault("quiz_scores", {})
    st.divider()
    with st.container(border=True):
        st.markdown("#### ‏🧠 اختبر فهمك")
        correct = 0
        answered = 0
        for idx, item in enumerate(questions):
            if len(item) == 4:
                q, options, answer_id, why = item
            else:
                q, options, answer_id = item
                why = None
            options, answer_id = _shuffle_options(page_key, idx, options, answer_id)
            key = f"quiz_{page_key}_{idx}"
            choice = st.radio(q, options, key=key, index=None)
            if choice is not None:
                answered += 1
                if options.index(choice) == answer_id:
                    correct += 1
                    suffix = f" — {why}" if why else ""
                    st.success(f"✓ إجابة صحيحة.{suffix}")
                else:
                    st.error(f"✗ إجابة غير صحيحة — الإجابة الصحيحة: "
                             f"**{options[answer_id]}**")
                    if why:
                        st.info(f"لماذا: {why}")
        scores[page_key] = {"answered": answered, "correct": correct,
                            "total": len(questions)}
        st.session_state["quiz_scores"] = scores
        if answered == len(questions):
            st.write(f"النتيجة: **{correct} / {len(questions)}**")


def progress_block() -> None:
    """شريط تقدّم عام في الصفحة الرئيسية (نسبة الدروس التي تمت زيارتها)."""
    visited = st.session_state.get("visited_pages", set())
    total_lessons = 25
    pct = len(visited) / total_lessons
    st.markdown(
        f"""
        <div class="unit-progress">
        تمّت زيارتك <b>{len(visited)}</b> من {total_lessons} درسًا
        ({pct * 100:.0f}% من المقرر).
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(pct, text="التقدّم في المقرر")


def chip(text: str, color: str | None = None) -> None:
    """وسم لوني صغير لعرض حالة/قيمة."""
    color = color or COLORS["accent"]
    st.markdown(
        f'<span style="display:inline-block;background:{color}22;color:{color};'
        f'border:1px solid {color}55;border-radius:999px;padding:2px 12px;'
        f'font-weight:600;font-size:0.85rem;">{text}</span>',
        unsafe_allow_html=True,
    )