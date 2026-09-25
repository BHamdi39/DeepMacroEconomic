"""فحص سلامة مستودع الأسئلة: كل درس 15 سؤالًا، 4 خيارات، فهرس صحيح وتعليل حاضر."""
from __future__ import annotations

import sys

from utils.questions import QUIZ_BANK


def main() -> int:
    errors: list[str] = []
    total = 0
    keys = sorted(QUIZ_BANK)
    if not keys:
        errors.append("المستودع فارغ!")
    for key in keys:
        items = QUIZ_BANK[key]
        total += len(items)
        if len(items) != 15:
            errors.append(f"{key}: عدد الأسئلة {len(items)} (المطلوب 15)")
        for i, item in enumerate(items):
            label = f"{key}#{i + 1}"
            if not isinstance(item, (tuple, list)) or len(item) != 4:
                errors.append(f"{label}: الصيغة غير صالحة")
                continue
            q, options, answer, why = item
            if not q.strip():
                errors.append(f"{label}: نص سؤال فارغ")
            if not isinstance(options, (tuple, list)) or len(options) != 4:
                errors.append(f"{label}: يجب أن يكون 4 خيارات")
            elif any(not str(o).strip() for o in options):
                errors.append(f"{label}: يوجد خيار فارغ")
            if not isinstance(answer, int) or not (0 <= answer < 4):
                errors.append(f"{label}: فهرس الإجابة {answer!r} خارج 0..3")
            if not str(why).strip():
                errors.append(f"{label}: تعليل فارغ")
            if len(str(q)) < 10:
                errors.append(f"{label}: سؤال قصير جدًا")
    report = [
        f"إجمالي الأسئلة: {total} (يجب أن يبلغ 375)",
        f"عدد الدروس في المستودع: {len(keys)} (يجب 25)",
    ]
    if errors:
        report.append(f"أخطاء: {len(errors)}")
        report.extend(errors[:80])
    else:
        report.append("✓ لا أخطاء — جميع الدروس 15/15 صالحة")
    print("\n".join(report))
    return 1 if errors or total != 375 else 0


if __name__ == "__main__":
    sys.exit(main())