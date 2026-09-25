"""الدرس 3.7 — الميزانية العامة ومضاعف الميزانية المتوازنة."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.rtl import COLORS, inject_rtl
from utils.solvers import balanced_budget_analysis, three_sector_equilibrium
from utils.ui import lesson_header, mark_visited, quiz

st.set_page_config(page_title="الميزانية ومضاعفها المتوازن", page_icon="7️⃣", layout="wide")
inject_rtl()
mark_visited("3_7")

lesson_header(
    "7️⃣",
    "الميزانية العامة ومضاعف الميزانية المتوازنة",
    "رصيد الميزانية BS = T − G − R (فائض/عجز/توازن). إذا رُفعت الضريبة مع "
    "الإنفاق بنفس المقدار بحيث تبقى الميزانية متوازنة، فإن ΔY = ΔG = ΔT بالضبط "
    "(المضاعف الموحّد = 1) عند ضرائب مستقلة.",
)

with st.container(border=True):
    st.markdown("#### 🎚️ معطيات الميزانية والنموذج")
    c1, c2, c3 = st.columns(3)
    G0 = c1.slider("الإنفاق الحكومي G₀", 0, 300, 120, 5)
    T0 = c2.slider("الضريبة المستقلة T₀", 0, 300, 140, 5)
    R0 = c3.slider("التحويلات R₀", 0, 150, 30, 5)
    c4, c5, c6 = st.columns(3)
    b = c4.slider("الميل الحدي للاستهلاك b", 0.40, 0.95, 0.80, 0.01)
    t = c5.slider("معدل ضريبة الدخل t (اختياري)", 0.0, 0.40, 0.0, 0.01)
    a = c6.slider("الاستهلاك الذاتي a", 0, 200, 100, 5)
    I0 = st.slider("الاستثمار I₀", 0, 300, 120, 5)

    eq = three_sector_equilibrium(a, b, I0, G0, T0, R0, t=t)
    Y_star = eq["Y"]

    st.divider()
    st.markdown("#### 📉 رصيد الميزانية مقابل الدخل")
    y = np.linspace(0, max(Y_star * 1.6, 500), 300)
    bs = T0 + t * y - G0 - R0
    bs_star = T0 + t * Y_star - G0 - R0
    y_bs = (G0 + R0 - T0) / t if t > 1e-9 and (G0 + R0 - T0) / t > 0 else None

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y, y=bs, mode="lines", name="BS = T − G − R",
                             line=dict(color=COLORS["is_curve"], width=3)))
    fig.add_hline(y=0, line_color=COLORS["muted"], line_dash="dot")
    fig.add_vline(x=Y_star, line_color=COLORS["accent"], line_dash="dot")
    fig.add_trace(go.Scatter(x=[Y_star], y=[bs_star], mode="markers+text",
                             text=["التوازن"], textposition="top center",
                             marker=dict(color=COLORS["accent"], size=13)))
    if y_bs:
        fig.add_annotation(x=y_bs, y=0, text=f"Y التوازن الميزاني ≈ {y_bs:.0f}",
                           showarrow=False, font=dict(color=COLORS["success"]))
    fig.update_layout(height=360, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Segoe UI, Tahoma, sans-serif"),
                      margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(title_text="الدخل Y", gridcolor=COLORS["grid"])
    fig.update_yaxes(title_text="رصيد الميزانية", gridcolor=COLORS["grid"])
    st.plotly_chart(fig, use_container_width=True)

    if bs_star > 1e-9:
        state = "فائض (+)"
    elif bs_star < -1e-9:
        state = "عجز (−)"
    else:
        state = "متوازنة (= 0)"
    st.metric(f"رصيد الميزانية عند Y* = {Y_star:,.0f}", f"{bs_star:+,.2f}", state)

    st.divider()
    st.markdown("#### ⚖️ مضاعف الميزانية المتوازنة (رفع ΔG مع إبقاء BS ثابتة)")
    col1, col2 = st.columns(2)
    dG = col1.slider("زيادة الإنفاق ΔG₀", 0, 150, 40, 1)
    attached = col2.radio("نمط الضريبة", ["ضريبة مستقلة", "مرتبطة بالدخل"], horizontal=True)
    t_used = 0.0 if "مستقلة" in attached else t

    result = balanced_budget_analysis(G0, T0, t_used, b, float(dG))

    m1, m2, m3 = st.columns(3)
    m1.metric("ΔG₀ المطبَّقة", f"{dG:,.2f}")
    m2.metric("ΔT₀ اللازمة (المطلوبة)", f"{result['dT']:,.2f}")
    m3.metric("ΔY الناتج", f"{result['dY']:,.2f}")

    with st.container(border=True):
        if "مستقلة" in attached:
            ok = abs(result["dY"] - dG) < 0.5 and abs(result["dT"] - dG) < 0.5
            st.success(f"بضريبة مستقلة: ΔT = ΔG = **{dG}** (إلزام التوازن BS "
                       f"ثابتة اكتمل) و ΔY = **{result['dY']:.2f} = ΔG** ✓ — "
                       "المضاعف الموحّد للميزانية المتوازنة يساوي 1.")
        else:
            st.markdown(f"بضريبة مرتبطة: القيد ΔBS = −ΔG + ΔT + t·ΔY = 0 أعطى "
                        f"ΔT₀ = **{result['dT']:,.2f}** وΔY = **{result['dY']:,.2f}**.")
            st.markdown(f"رصيد الميزانية قبل: {result['BS0']:,.2f} ← بعد: "
                        f"{result['BS1']:,.2f}")
            st.caption("رغم تغيّر t، تبقى النتيجة مقاربة لـ ΔY=ΔG لأن مضاعف "
                       "الميزانية المتوازنة يساوي 1 في هذا الإطار.")

quiz("3_7")