"""مستودع أسئلة الاختبارات المركزي — 15 سؤالًا لكل درس من الدروس الخمسة والعشرين.

كل درس يملك مفتاحًا (مثل "1_1") يقابله قائمة من 15 سؤالًا، كل سؤال بصيغة
(q, options, answer, why) حيث:
- q: نص السؤال.
- options: أربعة خيارات.
- answer: فهرس الخيار الصحيح (0..3).
- why: شرح التعليل للخيار الصحيح (يُعرض بعد الإجابة).
"""
from __future__ import annotations

from utils.questions.unit_1 import QUIZZES as _U1
from utils.questions.unit_2 import QUIZZES as _U2
from utils.questions.unit_3 import QUIZZES as _U3
from utils.questions.unit_4 import QUIZZES as _U4
from utils.questions.unit_5 import QUIZZES as _U5
from utils.questions.unit_6 import QUIZZES as _U6
from utils.questions.unit_7 import QUIZZES as _U7

QUIZ_BANK: dict[str, list[tuple[str, list[str], int, str]]] = {}
for _label, _q in (
    ("الوحدة 1", _U1),
    ("الوحدة 2", _U2),
    ("الوحدة 3", _U3),
    ("الوحدة 4", _U4),
    ("الوحدة 5", _U5),
    ("الوحدة 6", _U6),
    ("الوحدة 7", _U7),
):
    for _key, _items in _q.items():
        if _key in QUIZ_BANK:
            raise ValueError(f"مفتاح سؤال مكرر: {_key}")
        QUIZ_BANK[_key] = list(_items)