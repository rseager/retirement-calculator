import streamlit as st
from utils.calculations import compute_pv_phase_1
from utils.config import (
    DEFAULT_PHASE1_SPENDING,
    DEFAULT_INFLATION_RATE,
    DEFAULT_ROI,
    DEFAULT_PHASE1_YEARS,
    DEFAULT_PHASE1_START_AGE,
    DEFAULT_DISCOUNT_AGE
)

def run_phase1():
    """
    Renders the Phase 1 (Early Retirement) tab and returns the discounted PV to age 55
    along with the final spending amount.
    
    Returns:
    tuple: (float: Present value discounted to the specified age (typically 55),
            float: Final spending amount after inflation growth)
    """
    st.subheader("Phase 1: Early Retirement (up to 62)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        p1_annual_spending = st.number_input(
            "Annual Spending ($)", 
            min_value=0, 
            value=DEFAULT_PHASE1_SPENDING, 
            step=1000, 
            key="p1_spending"
        )
        p1_inflation_rate = st.number_input(
            "Inflation Rate (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=DEFAULT_INFLATION_RATE * 100, 
            step=0.1, 
            key="p1_inflation"
        ) / 100
        p1_roi = st.number_input(
            "Return on Investment (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=DEFAULT_ROI * 100, 
            step=0.1, 
            key="p1_roi"
        ) / 100
    
    with col2:
        p1_years = st.number_input(
            "Number of Years", 
            min_value=1, 
            max_value=50, 
            value=DEFAULT_PHASE1_YEARS, 
            step=1, 
            key="p1_years"
        )
        p1_start_age = st.number_input(
            "Phase Start Age", 
            min_value=30, 
            max_value=90, 
            value=DEFAULT_PHASE1_START_AGE, 
            step=1, 
            key="p1_start_age"
        )
        p1_discount_age = st.number_input(
            "Discount to Age", 
            min_value=30, 
            max_value=90, 
            value=DEFAULT_DISCOUNT_AGE, 
            step=1, 
            key="p1_discount_age"
        )
    
    # Calculate Phase 1 results
    p1_pv_at_start, p1_pv_discounted, p1_yearly_data, p1_final_spending = compute_pv_phase_1(
        p1_annual_spending,
        p1_inflation_rate,
        p1_roi,
        p1_years,
        p1_start_age,
        p1_discount_age
    )
    
    # Display Phase 1 results
    st.subheader("Phase 1 Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Present Value at Phase Start", f"${p1_pv_at_start:,.2f}")
    
    with col2:
        st.metric(f"Present Value Discounted to Age {p1_discount_age}", f"${p1_pv_discounted:,.2f}")
    
    # Display yearly breakdown
    st.subheader("Yearly Breakdown")
    st.dataframe(
        p1_yearly_data.style.format({
            "Spending": "${:,.2f}",
            "PV to Phase Start": "${:,.2f}"
        }),
        hide_index=True
    )
    
    # Return the discounted PV and final spending amount
    return p1_pv_discounted, p1_final_spending