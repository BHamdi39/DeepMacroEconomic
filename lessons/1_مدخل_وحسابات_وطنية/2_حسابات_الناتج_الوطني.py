"""الدرس 1.2 — حسابات الناتج الوطني: طرق القياس الثلاث (الإنتاج/الإنفاق/الدخل)."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.rtl import inject_rtl
from utils.ui import chip, lesson_header, mark_visited, quiz

st.set_page_config(page_title="حسابات الناتج الوطني", page_icon="2️⃣", layout="wide")
inject_rtl()
mark_visited("1_2")

lesson_header(
    "2️⃣",
    "حسابات الناتج الوطني",
    "الناتج المحلي الإجمالي يُقاس بثلاث طرق متكافئة: الإنتاج (القيمة المضافة)، "
    "الإنفاق (C+I+G+X−M)، والدخل (أجور+أرباح+ريع+فوائد) — ويجب أن تعطي "
    "النتيجة نفسها.",
)

st.latex(r"Y = \sum \text{القيم المضافة} = C + I + G + (X - M) = \text{أجور} + \text{أرباح} + \text{ريع} + \text{فوائد}")

with st.container(border=True):
    st.markdown("#### 👆 عدّل الجدول — راقب التطابق")
    c1, c2, c3 = st.columns(3)

    prod_df = pd.DataFrame({
        "القطاع": ["الفلاحة", "الصناعة", "الخدمات"],
        "القيمة المضافة": [180.0, 220.0, 150.0],
    })
    exp_df = pd.DataFrame({
        "البند": ["الاستهلاك C", "الاستثمار I", "الإنفاق الحكومي G",
                  "الصادرات X", "الواردات M"],
        "القيمة": [340.0, 110.0, 70.0, 60.0, 30.0],
    })
    inc_df = pd.DataFrame({
        "البند": ["الأجور", "الأرباح", "الريع", "الفوائد"],
        "القيمة": [300.0, 150.0, 60.0, 40.0],
    })

    with c1:
        st.markdown("**طريقة الإنتاج** (القيمة المضافة)")
        prod = st.data_editor(
            prod_df, key="prod", hide_index=True, num_rows="fixed",
            column_config={"القطاع": st.column_config.TextColumn(disabled=True),
                           "القيمة المضافة": st.column_config.NumberColumn()})
    with c2:
        st.markdown("**طريقة الإنفاق** (C+I+G+X−M)")
        exp = st.data_editor(
            exp_df, key="exp", hide_index=True, num_rows="fixed",
            column_config={"البند": st.column_config.TextColumn(disabled=True),
                           "القيمة": st.column_config.NumberColumn()})
    with c3:
        st.markdown("**طريقة الدخل** (أجور+أرباح+ريع+فوائد)")
        inc = st.data_editor(
            inc_df, key="inc", hide_index=True, num_rows="fixed",
            column_config={"البند": st.column_config.TextColumn(disabled=True),
                           "القيمة": st.column_config.NumberColumn()})

    prod_total = float(prod["القيمة المضافة"].sum())
    exp_total = float(exp.loc[exp["البند"] == "الاستهلاك C", "القيمة"].iloc[0]
                      + exp.loc[exp["البند"] == "الاستثمار I", "القيمة"].iloc[0]
                      + exp.loc[exp["البند"] == "الإنفاق الحكومي G", "القيمة"].iloc[0]
                      + exp.loc[exp["البند"] == "الصادرات X", "القيمة"].iloc[0]
                      - exp.loc[exp["البند"] == "الواردات M", "القيمة"].iloc[0])
    inc_total = float(inc["القيمة"].sum())

    m1, m2, m3 = st.columns(3)
    m1.metric("Y بالإنتاج", f"{prod_total:,.2f}")
    m2.metric("Y بالإنفاق", f"{exp_total:,.2f}")
    m3.metric("Y بالدخل", f"{inc_total:,.2f}")

    status_col = st.container(border=True)
    tol = 1e-6
    if abs(prod_total - exp_total) < tol and abs(exp_total - inc_total) < tol:
        status_col.markdown(
            "**✓ التطابق محقّق** — الطرق الثلاث أعطت الناتج نفسه، كما تقتضي "
            "الهوية المحاسبية الوطنية.")
        chip("متطابقة ✓", "#1e8e5a")
    else:
        status_col.markdown(
            "**⚠️ اختلال في التوازن** — الأدخلات غير منسجمة مع الهوية "
            "المحاسبية. راجع: هل مجموع القيم المضافة = الإنفاق الكلي الصافي؟ "
            "هل الدخل المحلي وُزّع بحيث يساوي الناتج؟")
        chip("غير متطابقة", "#c0392b")
        st.caption(f"الفرق الأكبر: ±{max(abs(prod_total-exp_total), abs(inc_total-exp_total)):,.2f}")

st.caption("تنبيه: الفرق بين Y بالإنفاق و Y بالإنتاج أكبر من الصفر يدل على أن "
           "البيانات المدخلة ليست ورقة محاسبية واحدة متناسقة (مثلا الواردات "
           "لا تظهر كقيمة مضافة سالبة في طريقة الإنتاج).")

quiz("1_2")