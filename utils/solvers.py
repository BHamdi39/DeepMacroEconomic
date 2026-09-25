"""المحرّك الرياضي لمختبر الاقتصاد الكلي المعمّق.

كل المعادلات مطابقة لمراجع المقياس (سلسلة الأستاذ عقبة عبداللاوي) كما هي
موثّقة في PRD_تطبيق_الاقتصاد_الكلي_المعمق.md القسم 6.

الرموز المستعملة:
    a    : الاستهلاك الذاتي
    b    : الميل الحدي للاستهلاك MPC
    t    : معدل الضريبة المرتبطة بالدخل
    m    : الميل الحدي للاستيراد
    mu   : حساسية الاستثمار لسعر الفائدة
    I0   : الاستثمار المستقل
    G0   : الإنفاق الحكومي المستقل
    T0   : الضريبة المستقلة
    R0   : التحويلات
    X0   : الصادرات المستقلة
    M0   : الواردات المستقلة
    Q    : الطلب الذاتي على النقود (Q1+Q2)
    alpha: حساسية الطلب على النقود للدخل
    g    : حساسية الطلب المضاربي على النقود لسعر الفائدة
    Ms   : عرض النقود الاسمي
"""
from __future__ import annotations

from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# الحلول العامة للأنظمة الخطية
# ---------------------------------------------------------------------------


def solve_linear_system(coefficients: np.ndarray, constants: np.ndarray) -> dict[str, float]:
    """يحل نظامًا خطيًا عامًا (معادلتين أو ثلاثة) عبر numpy.linalg.solve.

    المعاملات: مصفوفة A حيث A @ x = b، والمتغيرات بترتيب (Y, i, e).
    """
    coeff = np.asarray(coefficients, dtype=float)
    const = np.asarray(constants, dtype=float)
    x = np.linalg.solve(coeff, const)
    names = ["Y", "i", "e"][: len(x)]
    return dict(zip(names, x.tolist()))


# ---------------------------------------------------------------------------
# المضاعفات الكينزية (القسم 3.5)
# ---------------------------------------------------------------------------


def keynesian_multipliers(b: float, t: float = 0.0, m: float = 0.0) -> dict[str, float]:
    """يُعيد كل المضاعفات السبعة بصيغها المعدّلة حسب وجود t و m.

    المقام العام للاقتصاد المفتوح مع ضريبة دخل: 1 - b + b*t + m.
    """
    denom = 1 - b + b * t + m
    if denom <= 0:
        raise ValueError("المقام سالب أو معدوم: تأكد من قيم b, t, m (يجب 1-b+bt+m>0)")
    ke = 1.0 / denom
    return {
        "Ke_A": ke,       # مضاعف الإنفاق المستقل (استهلاك/استثمار)
        "Ke_G": ke,       # مضاعف الإنفاق الحكومي
        "Ke_X": ke,       # مضاعف الصادرات
        "Ke_T": -b * ke,  # مضاعف الضرائب (سلبي)
        "Ke_R": b * ke,   # مضاعف التحويلات
        "Ke_M": -ke,      # مضاعف الواردات المستقلة (سلبي)
        "Ke_0": 1.0 / (1 - b) if b < 1 else float("inf"),  # مضاعف الاقتصاد المغلق (مقارنة)
        "denom": denom,
    }


# ---------------------------------------------------------------------------
# منحني IS و LM (القسم 4.1 و 4.2)
# ---------------------------------------------------------------------------


def is_curve(
    a: float, b: float, I0: float, mu: float, G0: float,
    T0: float, R0: float, X0: float, M0: float, t: float = 0.0, m: float = 0.0,
) -> dict[str, float]:
    """معاملات معادلة IS بصيغة Y = Ke[A - mu*i].

    A = مجموع الإنفاق المستقل = a + I0 + G0 - b*T0 + b*R0 + X0 - M0
    Ke = 1 / (1 - b + b*t + m)
    """
    denom = 1 - b + b * t + m
    ke = 1.0 / denom if denom > 0 else float("nan")
    A = a + I0 + G0 - b * T0 + b * R0 + X0 - M0
    return {"Ke": ke, "A": A, "mu": mu, "denom": denom}


def lm_curve(Q: float, alpha: float, g: float, Ms: float) -> dict[str, float]:
    """معاملات معادلة LM بصيغة Y = (1/alpha)*(Ms - Q + g*i)."""
    return {"Q": Q, "alpha": alpha, "g": g, "Ms": Ms}


# ---------------------------------------------------------------------------
# توازن IS-LM (القسم 4.3)
# ---------------------------------------------------------------------------


def is_lm_equilibrium(is_params: dict[str, float], lm_params: dict[str, float]) -> dict[str, float]:
    """يحل نظام IS=LM ويعيد (Y*, i*, Theta, sigma) مطابقة للصيغ المغلقة.

    الصيغ المغلقة (كما في المرجع):
        Theta = Ke*g / (g + Ke*mu*alpha)   المضاعف المالي
        sigma = Ke*mu / (g + Ke*mu*alpha)  المضاعف النقدي
        Y*    = Theta*A + sigma*(Ms - Q)
        i*    = (alpha/g)*Theta*A - Theta*(Ms - Q)/(Ke*g)
    """
    Ke, A, mu = is_params["Ke"], is_params["A"], is_params["mu"]
    alpha, g, Ms, Q = lm_params["alpha"], lm_params["g"], lm_params["Ms"], lm_params["Q"]
    denom = g + Ke * mu * alpha
    Theta = Ke * g / denom
    sigma = Ke * mu / denom
    Mbar = Ms - Q
    Y_star = Theta * A + sigma * Mbar
    i_star = (alpha / g) * Theta * A - Theta * Mbar / (Ke * g)
    return {"Y": Y_star, "i": i_star, "Theta": Theta, "sigma": sigma}


def is_lm_regions_preset() -> dict[str, dict[str, float]]:
    """إعدادات g الثلاثة لمنحنى LM (كينزي أفقي / وسيط / كلاسيكي شبه عمودي)."""
    return {
        "كينزي (أفقي)": {"g": 300.0, "desc": "فخ السيولة: الطلب المضاربي شديد الحساسية للفائدة."},
        "وسيط": {"g": 30.0, "desc": "منحنى LM بميل معتدل."},
        "كلاسيكي (عمودي)": {"g": 3.0, "desc": "الطلب المضاربي منعدم المرونة: LM شبه عمودي."},
    }


# ---------------------------------------------------------------------------
# نموذج IS-LM-BP (موندل-فليمنغ، القسم 5)
# ---------------------------------------------------------------------------


def bp_curve(
    X0: float, M0: float, m: float, kappa: float, i_world: float = 0.0,
) -> dict[str, float]:
    """معاملات منحنى BP: i = i_world + (m/كابا)*Y - (X0-M0)/كابا.

    kappa = درجة حركة رأس المال (حساسية تدفق رؤوس الأموال لفارق الفائدة).
    كابا كبيرة → BP شبه أفقي عند i_world؛ كابا صغيرة → BP شبه عمودي.
    """
    if kappa <= 0:
        kappa = 1e-9
    return {"X0": X0, "M0": M0, "m": m, "kappa": kappa, "i_world": i_world,
            "slope": m / kappa, "intercept": i_world - (X0 - M0) / kappa}


def bp_balance(
    is_params: dict[str, float],
    lm_params: dict[str, float],
    X0: float, M0: float, m: float, kappa: float, i_world: float = 0.0,
) -> dict[str, float]:
    """يحسب وضع ميزان المدفوعات عند توازن IS-LM (فائض/عجز)."""
    eq = is_lm_equilibrium(is_params, lm_params)
    Y, i = eq["Y"], eq["i"]
    NX = X0 - M0 - m * Y                     # الميزان التجاري
    CF = kappa * (i - i_world)               # حساب رأس المال
    balance = NX + CF                        # ميزان المدفوعات
    return {"Y": Y, "i": i, "NX": NX, "CF": CF, "balance": balance}


def is_lm_bp_equilibrium(
    is_params: dict[str, float],
    lm_params: dict[str, float],
    X0: float, M0: float, m: float, kappa: float, i_world: float = 0.0,
) -> dict[str, float]:
    """حل نظام IS=LM=BP الثلاثي إذا كان منسجمًا، مع تصنيف الوضع.

    الـ IS-LM يعطي (Y*, i*)؛ نقاط BP عند ذلك الدخل: i_bp(Y*)؛ الفرق يحدد
    فائضًا/عجزًا. إذا تساوى i* مع i_bp فالتوازن الثلاثي محقق بالضبط.
    """
    eq = is_lm_equilibrium(is_params, lm_params)
    Y, i = eq["Y"], eq["i"]
    bp = bp_curve(X0, M0, m, kappa, i_world)
    i_bp_at_Y = bp["intercept"] + bp["slope"] * Y
    diff = i - i_bp_at_Y
    NX = X0 - M0 - m * Y
    CF = kappa * (i - i_world)
    balance = NX + CF
    if abs(diff) < 1e-9:
        status = "توازن ثلاثي محقق"
    elif diff > 0 and balance > 0 or diff > 0:
        status = "فائض في ميزان المدفوعات (النقطة فوق BP)"
    elif diff < 0:
        status = "عجز في ميزان المدفوعات (النقطة تحت BP)"
    else:
        status = "ميزان المدفوعات متوازن"
    return {"Y": Y, "i": i, "i_bp": i_bp_at_Y, "NX": NX, "CF": CF,
            "balance": balance, "status": status}


def x0_neutral_bp(
    is_params: dict[str, float],
    lm_params: dict[str, float],
    M0: float, m: float, kappa: float, i_world: float = 0.0,
) -> float:
    """قيمة الصادرات X0 التي تجعل منحنى BP يمر بنقطة توازن IS-LM بالضبط."""
    eq = is_lm_equilibrium(is_params, lm_params)
    Y, i = eq["Y"], eq["i"]
    # mise-BP: i = i_world + (m Y - X0 + M0)/kappa  =>  X0 = m*Y + M0 - kappa*(i - i_world)
    return m * Y + M0 - kappa * (i - i_world)


# ---------------------------------------------------------------------------
# شرط مارشال-ليرنر (القسم 5.4)
# ---------------------------------------------------------------------------


def marshall_lerner_check(a: float, b: float) -> tuple[bool, str]:
    """شرط نجاح تخفيض العملة في تحسين الميزان التجاري: a + b > 1."""
    ok = a + b > 1.0
    if ok:
        msg = f"الشرط محقّق (a+b = {a + b:.3f} > 1): تخفيض العملة يحسّن الميزان التجاري."
    else:
        msg = f"الشرط غير محقّق (a+b = {a + b:.3f} ≤ 1): التخفيض قد يزيد العجز التجاري."
    return ok, msg


# ---------------------------------------------------------------------------
# النموذج الكينزي البسيط (الوحدة 3)
# ---------------------------------------------------------------------------


def three_sector_equilibrium(
    a: float, b: float, I0: float, G0: float, T0: float, R0: float,
    t: float = 0.0,
) -> dict[str, float]:
    """توازن ثلاث قطاعات — Y* = Ke[a + I0 + G0 - b*T0 + b*R0]."""
    ke = keynesian_multipliers(b, t=t, m=0.0)["Ke_A"]
    Y = ke * (a + I0 + G0 - b * T0 + b * R0)
    return {"Y": Y, "Ke": ke}


def four_sector_equilibrium(
    a: float, b: float, I0: float, G0: float, T0: float, R0: float,
    X0: float, M0: float, t: float = 0.0, m: float = 0.0,
) -> dict[str, float]:
    """توازن أربع قطاعات — Y* = Ke[a + I0 + G0 - b*T0 + b*R0 + X0 - M0]."""
    mult = keynesian_multipliers(b, t=t, m=m)
    ke = mult["Ke_A"]
    Y = ke * (a + I0 + G0 - b * T0 + b * R0 + X0 - M0)
    return {"Y": Y, "Ke": ke, "Ke_open": ke, "Ke_closed": mult["Ke_0"]}


def policy_shock_effect(
    b: float, t: float, m: float, instrument: str, delta: float,
) -> float:
    """أثر صدمة على أداة واحدة على الدخل: ΔY = مضاعفُ_الأداة × Δ."""
    mult = keynesian_multipliers(b, t=t, m=m)
    mapping = {
        "G0": mult["Ke_G"], "G": mult["Ke_G"],
        "T0": mult["Ke_T"], "T": mult["Ke_T"],
        "R0": mult["Ke_R"], "R": mult["Ke_R"],
        "I0": mult["Ke_A"], "I": mult["Ke_A"], "a": mult["Ke_A"],
        "X0": mult["Ke_X"], "X": mult["Ke_X"],
        "M0": mult["Ke_M"], "M": mult["Ke_M"],
    }
    return mapping[instrument] * delta


def gap_analysis(
    Y_star: float, Y_full: float, b: float, t: float = 0.0, m: float = 0.0,
) -> dict[str, Any]:
    """الفجوة الانكماشية/التضخمية: نوعها ومقدار الإنفاق المستقل اللازم لسدّها."""
    dy = Y_full - Y_star
    ke = keynesian_multipliers(b, t=t, m=m)["Ke_A"]
    if abs(dy) < 1e-9:
        kind = "لا فجوة — الاقتصاد عند التشغيل الكامل"
    elif dy > 0:
        kind = "فجوة انكماشية (Y* < Yf)"
    else:
        kind = "فجوة تضخمية (Y* > Yf)"
    return {"dy": dy, "ke": ke, "autonomous_gap": dy / ke, "kind": kind,
            "Y_star": Y_star, "Y_full": Y_full}


def balanced_budget_analysis(
    G0: float, T0: float, t: float, b: float, dG: float,
) -> dict[str, float]:
    """يحافظ على رصيد الميزانية BS = T - G - R ثابتًا عند رفع G.

    معضرات سعر: مع t=0 يعطي بالضبط dY=dG=dT (العنصر المقبول في PRD 3.7).
    """
    R0 = 0.0
    ke = keynesian_multipliers(b, t=t, m=0.0)["Ke_A"]
    # النظام:  dY + Ke*b*dT = Ke*dG      (من معادلة التوازن)
    #          -t*dY + dT  = dG          (من قيد dBS=0)
    coeff = np.array([[1.0, ke * b], [-t, 1.0]])
    const = np.array([ke * dG, dG])
    dY, dT = np.linalg.solve(coeff, const)
    Y0 = three_sector_equilibrium(0.0, b, 0.0, G0, T0, R0, t=t)["Y"]
    return {"dY": dY, "dT": dT, "Y0": Y0, "Y1": Y0 + dY,
            "BS0": T0 + t * Y0 - G0 - R0, "BS1": T0 + t * (Y0 + dY) + dT - (G0 + dG) - R0}


def trade_balance_point(X0: float, M0: float, m: float) -> dict[str, float]:
    """نقطة تعادل الميزان التجاري (NX=0): Y_tb = (X0-M0)/m."""
    if m <= 0:
        return {"Y_tb": float("inf") if X0 > M0 else float("-inf")}
    return {"Y_tb": (X0 - M0) / m}


# ---------------------------------------------------------------------------
# الناتج الاسمي والحقيقي ومعامل الانكماش (القسم 1.3)
# ---------------------------------------------------------------------------


def real_nominal_gdp(quantities: dict[str, float], prices_base: dict[str, float],
                     prices_year: dict[str, float]) -> dict[str, float]:
    """الناتج الاسمي والحقيقي ومعامل الانكماش الضمني."""
    nominal = sum(quantities[k] * prices_year.get(k, 0.0) for k in quantities)
    real = sum(quantities[k] * prices_base.get(k, 0.0) for k in quantities)
    deflator = nominal / real * 100.0 if real else float("nan")
    return {"nominal": nominal, "real": real, "deflator": deflator}


# ---------------------------------------------------------------------------
# التغذية العكسية بين دولتين (القسم 6.1)
# ---------------------------------------------------------------------------


def two_country_feedback(
    mA: float, mB: float, cA: float, cB: float, delta_A: float, rounds: int = 20,
) -> dict[str, Any]:
    """يحاكي جولات التأثير المتبادل A→B→A→... حتى التقارب.

    يُعيد سلسلة دخل كل دولة عبر الجولات، ومقارنة بالمضاعف المغلق.
    """
    # مضاعف كل دولة مع تسريب الواردات الذاتي
    multA = 1.0 / (1.0 - cA + mA)
    multB = 1.0 / (1.0 - cB + mB)
    dYA = multA * delta_A      # استجابة A الوحيدة للصدمة (مع تسريبها الذاتي)
    dYB = 0.0
    pathA, pathB = [dYA], [dYB]
    for _ in range(rounds):
        # جولة جديدة: B يستقبل واردات A، ثم A يستقبل واردات B (نقطتان ثابتتان)
        dYB_new = multB * (mA * dYA)
        dYA_new = multA * (delta_A + mB * dYB)
        if abs(dYA_new - dYA) < 1e-12 and abs(dYB_new - dYB) < 1e-12:
            dYA, dYB = dYA_new, dYB_new
            pathA.append(dYA)
            pathB.append(dYB)
            break
        dYA, dYB = dYA_new, dYB_new
        pathA.append(dYA)
        pathB.append(dYB)
    closed = delta_A / (1.0 - cA)  # مضاعف الاقتصاد المغلق
    return {"pathA": pathA, "pathB": pathB,
            "final_A": dYA, "closed_A": closed,
            "leakage": closed - dYA, "rounds_run": len(pathA)}


# ---------------------------------------------------------------------------
# نماذج النمو (الوحدة 7)
# ---------------------------------------------------------------------------


def solow_steady_state(s: float, delta: float, n: float, alpha: float) -> float:
    """حالة الاستقرار: s*k^alpha = (delta+n)*k — يعيد k* (رأس المال للعامل)."""
    b = delta + n
    if s <= 0 or b <= 0:
        return float("nan")
    return (s / b) ** (1.0 / (1.0 - alpha))


def solow_path(k0: float, s: float, delta: float, n: float, alpha: float,
               periods: int = 80) -> tuple[list[float], list[float]]:
    """المسار الزمني k_{t+1} = k_t + s*k^alpha - (delta+n)*k_t."""
    k = k0
    ks, ys = [k], [k ** alpha]
    for _ in range(periods):
        k = k + s * (k ** alpha) - (delta + n) * k
        if k < 0:
            k = 0.0
        ks.append(k)
        ys.append(k ** alpha)
    return ks, ys


def endogenous_growth(
    model: str, A: float, K: float, L: float, H: float = 1.0,
    alpha: float = 0.5, beta: float = 0.7,
) -> dict[str, float]:
    """نماذج النمو الداخلي الثلاثة وإعادة قيمة Y وفق النموذج."""
    if model in ("رومر", "أكيلانو-هاويت"):
        Y = A * (K ** alpha) * (L ** (1.0 - alpha))
        factors = {"A": A, "K": K, "L": L}
    else:  # لوكاس
        Y = A * (K ** alpha) * ((L * H) ** beta)
        factors = {"A": A, "K": K, "L * H": L * H}
    # مرونات جزئية دالة لإبراز "المحرّك" الجوهري في كل نموذج
    if model in ("رومر", "أكيلانو-هاويت"):
        elasticities = {"K": alpha, "L": 1.0 - alpha, "A": 1.0}
    else:
        elasticities = {"K": alpha, "L*H": beta, "A": 1.0}
    return {"Y": Y, "elasticities": elasticities, "factors": factors}


# ---------------------------------------------------------------------------
# اختبار سريع للمثال المقبول في PRD (3.2: a=100, b=0.8, I0=50 => Y*=750)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # مثال 3.2
    ke = keynesian_multipliers(0.8, 0, 0)
    Y = ke["Ke_A"] * (100 + 50)
    print("3.2 two-sector default :", Y, "(مطلوب 750)")

    # مثال IS-LM
    is_p = is_curve(a=100, b=0.8, I0=200, mu=40, G0=150, T0=100, R0=0,
                    X0=0, M0=0, t=0, m=0)
    lm_p = lm_curve(Q=50, alpha=0.6, g=30, Ms=200)
    eq = is_lm_equilibrium(is_p, lm_p)
    print("4.3 IS-LM   :", eq)

    # تحقق يدوي:
    # IS: Ke=1/0.2=5, A=100+200+150-80=370 → Y=5(370-40i)
    # LM: Y=(1/0.6)(200-50+30i)=250+50i
    # 5(370-40i)=250+50i → 1850-200i=250+50i → 1600=250i → i=6.4 → Y=570
    print("   manual   : i=6.4, Y=570")

    # ميزانية متوازنة
    bb = balanced_budget_analysis(G0=100, T0=100, t=0.0, b=0.8, dG=50)
    print("3.7 balanced budget :", bb["dY"], bb["dT"], "(مطلوب 50/50)")

    # مارشال-ليرنر
    ok, msg = marshall_lerner_check(0.9, 0.6)
    print("5.4 M-L:", ok, msg)

    # تغذية عكسية
    fb = two_country_feedback(mA=0.2, mB=0.15, cA=0.8, cB=0.8, delta_A=100)
    print("6.1 feedback final A:", round(fb["final_A"], 2),
          "closed:", round(fb["closed_A"], 2), "leak:", round(fb["leakage"], 2))

    # سولو
    print("7.1 solow k*:", solow_steady_state(0.3, 0.05, 0.02, 1/3))

    # نمو داخلي
    print("7.2 romer:", endogenous_growth("رومر", 2, 100, 50, alpha=0.5))