import streamlit as st
import pandas as pd

# Import phase modules
from phases.phase1 import run_phase1
from phases.phase2 import run_phase2
from phases.phase3 import run_phase3
from phases.phase4 import run_phase4

# Import config for tab labels
from utils.config import (
    PHASE1_TAB_LABEL,
    PHASE2_TAB_LABEL,
    PHASE3_TAB_LABEL,
    PHASE4_TAB_LABEL,
    DEFAULT_DISCOUNT_AGE
)

# Set page config
st.set_page_config(page_title="Retirement Calculator", layout="wide")
st.title("Retirement Calculator")
st.header("Retirement Phases Calculator")

# Create tabs for different phases
tab1, tab2, tab3, tab4 = st.tabs([
    PHASE1_TAB_LABEL,
    PHASE2_TAB_LABEL,
    PHASE3_TAB_LABEL,
    PHASE4_TAB_LABEL
])

# Run each phase in its respective tab and collect the discounted PVs and final spending amounts
with tab1:
    p1_pv_discounted, p1_final_spending = run_phase1()

with tab2:
    p2_pv_discounted, p2_final_spending = run_phase2(p1_final_spending)

with tab3:
    p3_pv_discounted, p3_final_spending = run_phase3(p2_final_spending)

with tab4:
    p4_pv_discounted, p4_final_spending = run_phase4(p3_final_spending)

# Total retirement fund needed
st.header("Total Retirement Fund Needed")

# Calculate total PV discounted to the specified age (typically 55)
total_pv_discounted = p1_pv_discounted + p2_pv_discounted + p3_pv_discounted + p4_pv_discounted

st.metric(
    f"Total Present Value Discounted to Age {DEFAULT_DISCOUNT_AGE}",
    f"${total_pv_discounted:,.2f}"
)

# Add explanatory text
st.markdown("""
### How to Use This Calculator

1. **Phase 1: Early Retirement (up to 62)** - Calculate the present value needed for early retirement years.
2. **Phase 2: Go-go (62–70)** - Calculate the present value needed for the active retirement years with Social Security income.
3. **Phase 3: Slo-go (71–80)** - Calculate the present value needed for the slower, less active retirement years with declining spending.
4. **Phase 4: No-go (80+)** - Calculate the present value needed for the later retirement years with minimal activity and further declining spending.
5. **Total Retirement Fund Needed** - The sum of all phases, discounted to your target age.

### Notes
- All present values are calculated using the growing annuity formula where applicable.
- Social Security income reduces the amount needed from your retirement fund.
- When Social Security exceeds spending, the net withdrawal is set to $0 (you don't need to withdraw from your retirement fund).
- In Phases 3 and 4, spending is assumed to decline each year, reflecting reduced activity levels in later retirement.
""")
