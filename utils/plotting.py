"""دوال الرسم الموحّدة (plotly) لمختبر الاقتصاد الكلي المعمّق.

نفس نمط الألوان والهوامش في كل صفحات المختبر. كل الدوال تُرجع كائنات
go.Figure جاهزة st.plotly_chart.
"""
from __future__ import annotations

from typing import Any

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.rtl import COLORS, FONT_STACK


# ---------------------------------------------------------------------------
# أدوات مساعدة عامة
# ---------------------------------------------------------------------------


def _apply_layout(fig: go.Figure, height: int = 420, showlegend: bool = True) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_STACK, color=COLORS["text"]),
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=showlegend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def _axis_style(fig: go.Figure, x_title: str, y_title: str) -> go.Figure:
    fig.update_xaxes(
        title_text=x_title, gridcolor=COLORS["grid"], zeroline=True,
        zerolinecolor=COLORS["zero"], title_font=dict(size=13),
    )
    fig.update_yaxes(
        title_text=y_title, gridcolor=COLORS["grid"], zeroline=True,
        zerolinecolor=COLORS["zero"], title_font=dict(size=13),
    )
    return fig


def add_line(
    fig: go.Figure, xs: Any, ys: Any, name: str, color: str,
    dash: str = "solid", width: int = 3, row: int | None = None, col: int | None = None,
) -> go.Figure:
    fig.add_trace(
        go.Scatter(x=xs, y=ys, mode="lines", name=name, line=dict(
            color=color, width=width, dash=dash)),
        row=row, col=col,
    )
    return fig


def add_marker(
    fig: go.Figure, x: float, y: float, name: str, color: str | None = None,
    symbol: str = "circle", size: int = 13, row: int | None = None, col: int | None = None,
) -> go.Figure:
    color = color or COLORS["accent"]
    fig.add_trace(
        go.Scatter(x=[x], y=[y], mode="markers+text", name=name,
                   text=[name], textposition="top center",
                   marker=dict(color=color, size=size, symbol=symbol,
                               line=dict(color=COLORS["card"], width=1.5))),
        row=row, col=col,
    )
    return fig


def add_hline(fig: go.Figure, y: float, color: str | None = None,
              dash: str = "dot", row: int | None = None, col: int | None = None) -> go.Figure:
    fig.add_hline(y=y, line_color=color or COLORS["muted"], line_dash=dash, row=row, col=col)
    return fig


def add_vline(fig: go.Figure, x: float, color: str | None = None,
              dash: str = "dot", row: int | None = None, col: int | None = None) -> go.Figure:
    fig.add_vline(x=x, line_color=color or COLORS["muted"], line_dash=dash, row=row, col=col)
    return fig


# ---------------------------------------------------------------------------
# خط °45 وتوازن الدخل-الإنفاق (الوحدة 3)
# ---------------------------------------------------------------------------


def plot_45_degree(
    ad_slope: float, ad_intercept: float, y_star: float,
    x_title: str = "الدخل Y", labels: dict[str, str] | None = None,
    height: int = 420,
) -> go.Figure:
    """يرسم خط °45 مع AD = ad_intercept + ad_slope*Y ونقطة التوازن E."""
    labels = labels or {"ad": "الإنفاق الكلي AD", "45": "خط °45"}
    y_max = max(y_star * 1.45, ad_intercept * 1.4, 100)
    y = np.linspace(0, y_max, 300)
    ad = ad_intercept + ad_slope * y
    fig = go.Figure()
    add_line(fig, y, y, labels["45"], COLORS["ref"], dash="dot", width=2)
    add_line(fig, y, np.clip(ad, 0, None), labels["ad"], COLORS["is_curve"])
    add_marker(fig, y_star, y_star, "E")
    add_vline(fig, y_star, COLORS["muted"])
    _apply_layout(fig, height)
    _axis_style(fig, x_title, "الإنفاق المخطّط AD")
    return fig


def plot_dual_income(
    ad_slope: float, ad_intercept: float, y_star: float,
    leak_intercept: float, leak_slope: float,
    inj_intercept: float, inj_slope: float = 0.0,
    height: int = 520,
) -> go.Figure:
    """رسم مزدوج: (أعلى) AD مقابل °45، و(أسفل) التسريبات مقابل الحقنات."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.09,
                        row_heights=[0.55, 0.45])
    y_max = max(y_star * 1.45, ad_intercept * 1.4, 80)
    y = np.linspace(0, y_max, 300)

    ad = ad_intercept + ad_slope * y
    add_line(fig, y, y, "خط °45", COLORS["ref"], dash="dot", width=2, row=1, col=1)
    add_line(fig, y, np.clip(ad, 0, None), "AD = الإنفاق الكلي", COLORS["is_curve"], row=1, col=1)
    add_marker(fig, y_star, y_star, "E", row=1, col=1)
    add_vline(fig, y_star, COLORS["muted"], row=1, col=1)

    # المخطط السفلي: التسريبات مقابل الحقنات
    leak = leak_intercept + leak_slope * y
    inj = inj_intercept + inj_slope * y
    add_line(fig, y, np.clip(leak, None, y_max), "التسريبات (S+T+M)", COLORS["danger"], row=2, col=1)
    add_line(fig, y, inj, "الحقنات (I+G+X+R)", COLORS["success"], row=2, col=1)
    add_vline(fig, y_star, COLORS["muted"], row=2, col=1)

    fig.update_yaxes(title_text="AD", row=1, col=1, gridcolor=COLORS["grid"],
                     zeroline=True, zerolinecolor=COLORS["zero"])
    fig.update_xaxes(title_text="الدخل Y", row=2, col=1, gridcolor=COLORS["grid"],
                     zeroline=True, zerolinecolor=COLORS["zero"])
    fig.update_yaxes(title_text="الإجمالي", row=2, col=1, gridcolor=COLORS["grid"])
    _apply_layout(fig, height)
    return fig


# ---------------------------------------------------------------------------
# منحنيات IS / LM / BP (الوحدة 4 و 5)
# ---------------------------------------------------------------------------


def _is_y(is_params: dict[str, float], i: np.ndarray) -> np.ndarray:
    return is_params["Ke"] * (is_params["A"] - is_params["mu"] * i)


def _lm_y(lm_params: dict[str, float], i: np.ndarray) -> np.ndarray:
    return (lm_params["Ms"] - lm_params["Q"] + lm_params["g"] * i) / lm_params["alpha"]


def plot_is_lm(
    is_params: dict[str, float],
    lm_params: dict[str, float],
    eq: dict[str, float] | None = None,
    bp_params: dict[str, float] | None = None,
    is2_params: dict[str, float] | None = None,
    lm2_params: dict[str, float] | None = None,
    is3_params: dict[str, float] | None = None,
    lm3_params: dict[str, float] | None = None,
    height: int = 440,
) -> go.Figure:
    """يرسم IS و LM (وBP اختياريًا) في مستوي (Y, i) مع نقطة التوازن."""
    mu = is_params["mu"] if is_params["mu"] else 1e-9
    i_hi = max(is_params["A"] / mu, 30) * 1.15
    if eq:
        i_hi = max(i_hi, eq["i"] * 1.35 + 2)
    y_hi = max(is_params["Ke"] * is_params["A"], 50) * 1.25
    if eq:
        y_hi = max(y_hi, eq["Y"] * 1.35)
    i = np.linspace(-2, i_hi, 220)

    fig = go.Figure()
    add_line(fig, _is_y(is_params, i), i, "IS", COLORS["is_curve"])
    if is2_params is not None:
        add_line(fig, _is_y(is2_params, i), i, "IS′", COLORS["is_prime"], dash="dash")
    if is3_params is not None:
        add_line(fig, _is_y(is3_params, i), i, "IS₀ أولي", COLORS["muted"],
                 dash="dot", width=2)
    lm_y = _lm_y(lm_params, i)
    mask = lm_y > 0
    add_line(fig, np.where(mask, lm_y, np.nan), i, "LM", COLORS["lm_curve"])
    if lm2_params is not None:
        lm2_y = _lm_y(lm2_params, i)
        add_line(fig, np.where(lm2_y > 0, lm2_y, np.nan), i, "LM′", COLORS["lm_prime"], dash="dash")
    if lm3_params is not None:
        lm3_y = _lm_y(lm3_params, i)
        add_line(fig, np.where(lm3_y > 0, lm3_y, np.nan), i, "LM₀ أولي",
                 COLORS["muted"], dash="dot", width=2)

    if bp_params is not None:
        bp_y = (i - bp_params["intercept"]) / bp_params["slope"] if bp_params["slope"] else np.nan
        mask_bp = bp_y > 0
        add_line(fig, np.where(mask_bp if isinstance(mask_bp, np.ndarray) else mask_bp, bp_y, np.nan),
                 i, "BP", COLORS["bp_curve"], dash="longdash")

    if eq is not None:
        add_marker(fig, eq["Y"], eq["i"], f"E (Y={eq['Y']:.0f}, i={eq['i']:.2f})",
                   COLORS["accent"], size=14)

    _apply_layout(fig, height)
    _axis_style(fig, "الدخل Y", "سعر الفائدة i%")
    fig.update_yaxes(range=[-2, i_hi], gridcolor=COLORS["grid"])
    fig.update_xaxes(range=[0, y_hi], gridcolor=COLORS["grid"])
    return fig


def plot_is_derivation(is_params: dict[str, float], i_range: np.ndarray, height: int = 560) -> go.Figure:
    """رسم مزدوج يوضح اشتقاق IS نقطة بنقطة عبر تغيير i.

    العلوي: مخطط °45 — خط AD(i) يتحرك مع كل سعر فائدة ويتقاطع مع خط °45.
    السفلي: منحنى IS = أثر هذه التقاطعات (Y, i).
    """
    Ke, mu, A = is_params["Ke"], is_params["mu"], is_params["A"]
    c = 1 - 1 / Ke
    demo_i = np.linspace(i_range.min(), i_range.max(), 5)
    y_top_max = max(Ke * A * 1.15, 100)
    yy = np.linspace(0, y_top_max, 250)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.12,
                        row_heights=[0.45, 0.55])
    add_line(fig, yy, yy, "°45", COLORS["ref"], dash="dot", width=2, row=1, col=1)
    for i in demo_i:
        a0 = A - mu * i
        add_line(fig, yy, a0 + c * yy, f"AD (i={i:.1f}%)", COLORS["muted"],
                 width=1.5, row=1, col=1)
    for i in demo_i:
        y0 = Ke * (A - mu * i)
        add_marker(fig, y0, y0, "", COLORS["is_curve"], size=9, row=1, col=1)

    ys = Ke * (A - mu * i_range)
    add_line(fig, ys, i_range, "IS", COLORS["is_curve"], width=3, row=2, col=1)
    for i in demo_i:
        y0 = Ke * (A - mu * i)
        add_marker(fig, y0, i, f" ({y0:.0f},{i:.1f})", COLORS["is_curve"], size=9, row=2, col=1)

    _apply_layout(fig, height)
    fig.update_yaxes(title_text="AD", row=1, col=1, gridcolor=COLORS["grid"])
    fig.update_xaxes(title_text="الدخل Y", row=1, col=1, gridcolor=COLORS["grid"])
    fig.update_yaxes(title_text="i%", row=2, col=1, gridcolor=COLORS["grid"])
    fig.update_xaxes(title_text="الدخل Y", row=2, col=1, gridcolor=COLORS["grid"])
    return fig


def plot_money_derivation(lm_params: dict[str, float], i_range: np.ndarray, height: int = 560) -> go.Figure:
    """رسم مزدوج يوضح اشتقاق LM نقطة بنقطة عبر تغيير الدخل Y.

    العلوي: سوق النقود — طلب النقود MD(i) ينزاح مع كل Y وعرض Ms شاقولي.
    السفلي: منحنى LM = أثر تقاطعات سوق النقود (Y, i).
    """
    Q, alpha, g, Ms = lm_params["Q"], lm_params["alpha"], lm_params["g"], lm_params["Ms"]
    demo_i = np.linspace(i_range.min(), i_range.max(), 5)
    demo_i = demo_i[demo_i >= 0]
    m_top = np.linspace(0, max(Ms * 1.5, 200), 250)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.12,
                        row_heights=[0.45, 0.55])
    add_vline(fig, Ms, COLORS["lm_curve"], dash="dot", row=1, col=1)
    for i in demo_i:
        y_i = (Ms - Q + g * i) / alpha
        i_md = (Q + alpha * y_i - m_top) / g
        add_line(fig, m_top, i_md, f"MD (Y={y_i:.0f})", COLORS["muted"], width=1.5, row=1, col=1)
    for i in demo_i:
        y_i = (Ms - Q + g * i) / alpha
        add_marker(fig, Ms, i, "", COLORS["lm_curve"], size=9, row=1, col=1)

    lm_y = _lm_y(lm_params, i_range)
    mask = lm_y > 0
    add_line(fig, np.where(mask, lm_y, np.nan), i_range, "LM", COLORS["lm_curve"], width=3, row=2, col=1)
    for i in demo_i:
        y_i = (Ms - Q + g * i) / alpha
        if y_i > 0:
            add_marker(fig, y_i, i, f" ({y_i:.0f},{i:.1f})", COLORS["lm_curve"], size=9, row=2, col=1)

    _apply_layout(fig, height)
    fig.update_yaxes(title_text="i%", row=1, col=1, gridcolor=COLORS["grid"])
    fig.update_xaxes(title_text="النقود M", row=1, col=1, gridcolor=COLORS["grid"])
    fig.update_yaxes(title_text="i%", row=2, col=1, gridcolor=COLORS["grid"])
    fig.update_xaxes(title_text="الدخل Y", row=2, col=1, gridcolor=COLORS["grid"])
    return fig


# ---------------------------------------------------------------------------
# رسوم مساعدة: المضاعفات، الميزان التجاري، سولو، التغذية العكسية
# ---------------------------------------------------------------------------


def bar_multipliers(labels: list[str], values: list[float], title: str = "") -> go.Figure:
    """مخطط شريطي يبرز أن مضاعف الضرائب/التحويلات أصغر من مضاعف الإنفاق."""
    colors = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in values]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors,
                           text=[f"{v:.2f}" for v in values], textposition="outside"))
    _apply_layout(fig, height=380)
    _axis_style(fig, "الأداة", "المضاعف")
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=15)))
    return fig


def bar_policy_impact(labels: list[str], values: list[float], title: str = "") -> go.Figure:
    """أثر صدمة بنفس المقدار عبر الأدوات المختلفة على ΔY."""
    colors = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in values]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors,
                           text=[f"{v:+.1f}" for v in values], textposition="outside"))
    _apply_layout(fig, height=380)
    _axis_style(fig, "الأداة", "ΔY")
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=15)))
    return fig


def plot_nx(y_points: np.ndarray, nx_values: np.ndarray, eq_y: float, height: int = 380) -> go.Figure:
    """ميزان التجاري NX مقابل Y مع مناطقي الفائض والعجز."""
    fig = go.Figure()
    add_line(fig, y_points, nx_values, "NX = X − M", COLORS["bp_curve"], width=3)
    add_hline(fig, 0, COLORS["muted"])
    add_vline(fig, eq_y, COLORS["accent"], dash="dot")
    add_marker(fig, eq_y, float(np.interp(eq_y, y_points, nx_values)), "التوازن")
    fig.add_annotation(x=eq_y * 0.4, y=nx_values.max() * 0.8, text="فائض",
                       showarrow=False, font=dict(color=COLORS["success"]))
    fig.add_annotation(x=eq_y * 1.55, y=nx_values.min() * 0.8, text="عجز",
                       showarrow=False, font=dict(color=COLORS["danger"]))
    _apply_layout(fig, height)
    _axis_style(fig, "الدخل Y", "NX")
    return fig


def plot_solow(s: float, delta: float, n: float, alpha: float, k_star: float,
               k_path: list[float] | None = None, height: int = 440) -> go.Figure:
    """رسم سولو: sy و (δ+n)k وتقاطع حالة الاستقرار."""
    k = np.linspace(0, min(k_star * 1.8, 60), 300)
    sy = s * k ** alpha
    dk = (delta + n) * k
    fig = go.Figure()
    add_line(fig, k, sy, "s·f(k) = s·k^α", COLORS["is_curve"])
    add_line(fig, k, dk, "(δ+n)·k", COLORS["danger"])
    add_marker(fig, k_star, s * k_star ** alpha, f"k* = {k_star:.2f}", COLORS["accent"], size=14)
    if k_path:
        add_line(fig, list(range(len(k_path))), k_path, "المسار الزمني k_t",
                 COLORS["warning"], dash="dash", width=2)
    add_hline(fig, 0, COLORS["muted"])
    _apply_layout(fig, height)
    _axis_style(fig, "رأس المال للعامل k", "للفرد الواحد")
    return fig


def plot_two_country(pathA: list[float], pathB: list[float], height: int = 400) -> go.Figure:
    """تقارب دخل الدولتين عبر الجولات (A→B→A...)."""
    fig = go.Figure()
    add_line(fig, list(range(len(pathA))), pathA, "دخل الدولة A (ΔY_A)", COLORS["is_curve"])
    add_line(fig, list(range(len(pathB))), pathB, "دخل الدولة B (ΔY_B)", COLORS["success"])
    _apply_layout(fig, height)
    _axis_style(fig, "الجولة", "الزيادة في الدخل ΔY")
    return fig


def growth_curves(model_y: dict[str, list[float]], labels: dict[str, str],
                  height: int = 300) -> go.Figure:
    """ثلاثة منحنيات أثر كل عامل على Y في النموذج المختار (رومر/لوكاس/عتاق)."""
    fig = go.Figure()
    palette = [COLORS["is_curve"], COLORS["bp_curve"], COLORS["lm_curve"]]
    for (name, ys), color in zip(model_y.items(), palette):
        xs = np.arange(len(ys))
        add_line(fig, xs, ys, labels.get(name, name), color)
    _apply_layout(fig, height)
    _axis_style(fig, "مستوى العامل (× 0.5 إلى 1.5)", "Y")
    return fig


def plot_bop_components(nx: float, cf: float, height: int = 320) -> go.Figure:
    """شريط مكوّن: الحساب الجاري + حساب رأس المال = ميزان المدفوعات."""
    balance = nx + cf
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["الحساب الجاري NX", "حساب رأس المال CF", "ميزان المدفوعات"],
        y=[nx, cf, balance],
        marker_color=[COLORS["success"] if nx >= 0 else COLORS["danger"],
                      COLORS["lm_prime"] if cf >= 0 else COLORS["lm_curve"],
                      COLORS["accent"]],
        text=[f"{nx:+,.1f}", f"{cf:+,.1f}", f"{balance:+,.1f}"],
        textposition="outside"))
    _apply_layout(fig, height)
    _axis_style(fig, "", "المبلغ النقدي")
    return fig