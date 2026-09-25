"""الدرس 2.1 — فرضيات المدرستين والعرض الكلي (كلاسيكي عمودي / كينزي أفقي)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.rtl import COLORS, inject_rtl
from utils.ui import chip, lesson_header, mark_visited, quiz

st.set_page_config(page_title="فرضيات المدرستين والعرض الكلي", page_icon="1️⃣", layout="wide")
inject_rtl()
mark_visited("2_1")

lesson_header(
    "1️⃣",
    "فرضيات المدرستين والعرض الكلي",
    "الكلاسيكيون: أسعار وأجور مرنة ← عرض كلي عمودي عند التشغيل الكامل (السياسة "
    "تحرّك السعر فقط). الكينزيون: أجور جامدة نحو الأسفل وطلب فعّال ← عرض كلي "
    "أفقي قبل التشغيل الكامل (السياسة تحرّك الناتج فقط).",
)

st.markdown("### ‏مقارنة الفرضيات")
with st.container(border=True):
    c1, c2 = st.columns(2)
    c1.markdown("**الكلاسيكيون:** مرونة كاملة للأجور والأسعار، قانون ساي "
                "(العرض يخلق طلبه)، ثبات سرعة دوران النقود.")
    c2.markdown("**الكينزيون:** جمود الأجور نحو الأسفل، الطلب الفعّال محدد، "
                "عدم استقرار الاستثمار الخاص.")

school = st.radio("اختر المدرسة الفكرية:", ["كلاسيكي", "كينزي"], horizontal=True)

with st.container(border=True):
    st.markdown("#### 🎚️ إزاحة الطلب الكلي AD")
    y_full = st.slider("مستوى التشغيل الكامل Yf", 60, 180, 120, 2)
    demand = st.slider("مستوى الطلب الكلي D (إزاحة AD)", 60, 140, 100, 1)

    P_FIXED = 2.0
    slope_ad = 1.2
    y = np.linspace(0, 220, 400)
    p_ad = demand * 1.5 - slope_ad * y           # منحنى AD متناقص

    if school == "كلاسيكي":
        y_eq = y_full
        p_eq = demand * 1.5 - slope_ad * y_full
        as_xs = [y_full, y_full]
        as_ys = [0, P_FIXED + 10]
    else:
        # كينزي: أفقي حتى Yf ثم عمودي
        y_at_pfixed = (demand * 1.5 - P_FIXED) / slope_ad
        y_eq = min(y_at_pfixed, y_full)
        if y_at_pfixed >= y_full:
            y_eq = y_full
            p_eq = demand * 1.5 - slope_ad * y_full
        else:
            p_eq = P_FIXED
        as_xs = [0, y_full, y_full]
        as_ys = [P_FIXED, P_FIXED, P_FIXED + 10]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y, y=np.clip(p_ad, 0, None), mode="lines",
                             name="AD", line=dict(color=COLORS["is_curve"], width=3)))
    fig.add_trace(go.Scatter(x=as_xs, y=as_ys, mode="lines",
                             name="AS", line=dict(color=COLORS["danger"], width=3)))
    fig.add_trace(go.Scatter(x=[y_eq], y=[p_eq], mode="markers+text",
                             name="التوازن", text=[f"E (Y={y_eq:.1f}, P={p_eq:.2f})"],
                             textposition="top center",
                             marker=dict(color=COLORS["accent"], size=14)))
    fig.add_vline(x=y_full, line_color=COLORS["muted"], line_dash="dot")
    fig.add_annotation(x=y_full + 6, y=10, text="Yf",
                       showarrow=False, font=dict(color=COLORS["muted"]))
    fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Segoe UI, Tahoma, sans-serif"),
                      margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=1.02))
    fig.update_xaxes(title_text="الناتج Y", gridcolor=COLORS["grid"], range=[0, 220])
    fig.update_yaxes(title_text="مستوى الأسعار P", gridcolor=COLORS["grid"])
    st.plotly_chart(fig, use_container_width=True)

    m1, m2 = st.columns(2)
    m1.metric("الناتج التوازني", f"{y_eq:.1f}")
    m2.metric("مستوى السعر", f"{p_eq:.2f}")

    with st.container(border=True):
        if school == "كلاسيكي":
            st.success(f"في المدرسة الكلاسيكية، إزاحة AD من {demand} غيّرت "
                       "**السعر فقط** إلى {:.2f} بينما بقي الناتج عند التشغيل "
                       "الكامل {:.0f} — تجسيد لحياد السياسة النقدية.".format(p_eq, y_full))
        elif y_eq < y_full:
            st.success(f"في الحالة الكينزية قبل بلوغ التشغيل الكامل، إزاحة AD غيّرت "
                       f"**الكمية فقط** إلى {y_eq:.1f} بحيث يتغيّر الناتج ويبقى السعر "
                       f"ثابتًا عند {P_FIXED}.")
        else:
            st.success("بلغ الاقتصاد التشغيل الكامل: أي إزاحة إضافية لـ AD لن ترفع "
                       "الناتج وسترفع السعر فقط (النطاق العمودي من AS).")

    chip(school + (" — عرض عمودي" if school == "كلاسيكي" else " — عرض أفقي/منكسر"))

quiz("2_1")