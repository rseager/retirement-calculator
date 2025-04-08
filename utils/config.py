"""
Configuration settings for the retirement calculator.
Contains default values for inflation rates, return rates, age ranges, etc.
"""

# Default inflation and return rates
DEFAULT_INFLATION_RATE = 0.03  # 3%
DEFAULT_ROI = 0.05  # 5%
DEFAULT_SS_GROWTH_RATE = 0.02  # 2%

# Default age ranges
DEFAULT_PHASE1_START_AGE = 55
DEFAULT_PHASE2_START_AGE = 62
DEFAULT_PHASE3_START_AGE = 71
DEFAULT_PHASE4_START_AGE = 80

# Default phase durations
DEFAULT_PHASE1_YEARS = 7  # 55-61
DEFAULT_PHASE2_YEARS = 9  # 62-70
DEFAULT_PHASE3_YEARS = 9  # 71-80
DEFAULT_PHASE4_YEARS = 15  # 80+

# Default spending amounts
DEFAULT_PHASE1_SPENDING = 60000
DEFAULT_PHASE2_SPENDING = 60000
DEFAULT_PHASE3_SPENDING = 60000
DEFAULT_PHASE4_SPENDING = 50000

# Default Social Security amounts
DEFAULT_PHASE2_SS_AMOUNT = 30000
DEFAULT_PHASE3_SS_AMOUNT = 35000
DEFAULT_PHASE4_SS_AMOUNT = 40000

# Default spending change rates
DEFAULT_PHASE1_INFLATION_RATE = 0.03  # 3% increase
DEFAULT_PHASE2_INFLATION_RATE = 0.03  # 3% increase
DEFAULT_PHASE3_DECLINE_RATE = 0.03  # 3% decrease
DEFAULT_PHASE4_DECLINE_RATE = 0.04  # 4% decrease

# Default discount age (typically the retirement start age)
DEFAULT_DISCOUNT_AGE = 55

# Tab labels
PHASE1_TAB_LABEL = "Phase 1: Early Retirement (up to 62)"
PHASE2_TAB_LABEL = "Phase 2: Go-go (62–70)"
PHASE3_TAB_LABEL = "Phase 3: Slo-go (71–80)"
PHASE4_TAB_LABEL = "Phase 4: No-go (80+)"