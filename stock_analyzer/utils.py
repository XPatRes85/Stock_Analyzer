"""
Core utility functions for Stock Analyzer.
Handles CAGR, trend ratings, SKIP logic and score mapping.
"""

from typing import List, Optional, Union, Callable, Any



def safe_get(data: dict, key: str, default=None):
    """
    Safely retrieve a value from a dictionary.
    Returns default if the key is missing or the value is "skip".
    """

    if not isinstance (data, dict):
        return default

    value = data.get(key, default)

    if value == "skip":
        return None

    return value



def skip_if_none(value, func: Callable, skip_label: str = "SKIP"):
    """
    If value is None return skip_label.
    Otherwise apply the given function to the value.
    """

    if value is None:
        return skip_label
    try:
        return func(value)
    except (TypeError, ValueError, ZeroDivisionError):
        return skip_label



def calculate_cagr(values: List[float]) -> Optional[float]:
    """
    Calculate Compound Annual Growth Rate (CAGR).
    values: list ordered from newest to oldest
    Example: [120, 110, 100, 90]  → newest is 120, oldest is 90
    Returns CAGR as a decimal (e.g. 0.10 for 10%), or None if calculation is not possible.
    """

    if not values or len(values) < 2:
        return None
    
    newest = values[0]
    oldest = values[-1]

    # CAGR is only mathematically valid when both endpoints are positive
    if newest <= 0 or oldest <= 0:
        return None

    years = len(values) - 1

    try:
        cagr = (newest / oldest) ** (1 / years) - 1
        return cagr
    except (ZeroDivisionError, ValueError):
        return None



def trend_rating(values: List[float]) -> str:
    """
    Rate a growth-oriented metric (Revenue, EPS, FCF, etc.).

    Returns:
        "✅" → Strong positive trend
        "!" → Mild / acceptable trend
        "❌" → Weak or negative trend
        "SKIP"→ Not enough data
    """

    if not values or len(values) < 2:
        return "SKIP"

    cagr = calculate_cagr(values)

    # Prefer CAGR when it is valid
    if cagr is not None:
        if cagr >= 0.10:    # 10% or higher
            return "✅"
        elif cagr >= 0.03:  # 3% – 10%
            return "!"
        else:
            return "❌"

    # Fallback when CAGR cannot be calculated (negatives, zeros, etc.)
    newest = values[0]
    oldest = values[-1]

    if newest > oldest:
        return "✅"
    elif newest < oldest:
        return "❌"
    else:
        return "!"



def debt_trend_rating (values: List[float]) -> str:
    """
    Rate Total Debt.
    Lower debt over time is positive
    """

    if not values or len (values) < 2:
        return "SKIP"

    newest = values[0]
    oldest = values[-1]

    if newest < oldest:
        return "✅"      # Debt decreased
    elif newest > oldest:
        return "❌"      # Debt increased
    else:
        return "!"



def net_cash_trend_rating(values: List[float]) -> str:
    """
    Rate Net Cash (Debt)
    Higher (more positive or less negative) is better.
    """

    if not values or len(values) < 2:
        return "SKIP"

    newest = values[0]
    oldest = values[-1]

    if newest > oldest:
        return "✅"
    elif newest < oldest:
        return "❌"
    else:
        return "!"



def shares_trend_rating(values: List[float]) -> str:
    """
    Rate Shares Outstanding.
    Decreasing shares = buybacks = positive.
    """

    if not values or len (values) < 2:
        return "SKIP"

    newest = values[0]
    oldest = values[-1]

    if newest < oldest:
        return "✅"      # Share count fell (buybacks)
    elif newest > oldest:
        return "❌"      # Share count rose (dilution)
    else:
        return "!"



def dividend_trend_rating(values: List[float]) -> str:
    """
    Rate Dividend Growth.
    Uses milder thresholds than regular growth metrics.
    """

    if not values or len (values) < 2:
        return "SKIP"

    cagr = calculate_cagr(values)

    if cagr is not None:
        if cagr >= 0.025:       # 2.5%+
            return "✅"
        elif cagr >= 0.005:     # 0.5% – 2.5%
            return "!"
        else:
            return "❌"

# Fallback
    newest = values[0]
    oldest = values[-1]

    if newest > oldest:
        return "✅"
    elif newest < oldest:
        return "❌"
    else:
        return "!"



def positive_check(value: float) -> str:
    """
    Simple positive / negative check.
    
    Returns:
        "✅" if value > 0
        "❌" if value <= 0
        "SKIP" if value is None
    """

    if value is None:
        return "SKIP"

    if value > 0:
        return "✅"
    else:
        return "❌"



def map_rating(symbol: str) -> Optional[float]:
    """
    Convert rating symbol to a numeric score.
    ✅ → 1.0
    !  → 0.5
    ❌ → 0.0
    SKIP or anything else → None (ignored in weighting)
    """

    if symbol == "✅":
        return 1.0
    elif symbol == "!":
        return 0.5
    elif symbol == "❌":
        return 0.0
    else:
        return None