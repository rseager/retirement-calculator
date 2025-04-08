import streamlit as st
from utils.calculations import compute_pv_phase_2
from utils.config import (
    DEFAULT_PHASE2_SPENDING,
    DEFAULT_INFLATION_RATE,
    DEFAULT_PHASE2_SS_AMOUNT,
    DEFAULT_SS_GROWTH_RATE,
    DEFAULT_ROI,
    DEFAULT_PHASE2_YEARS,
    DEFAULT_PHASE2_START_AGE,
    DEFAULT_DISCOUNT_AGE
)

def run_phase2(starting_spending=None):
    """
    Renders the Phase 2 (Go-go) tab and returns the discounted PV to age 55
    along with the final spending amount.
    
    Parameters:
    starting_spending (float, optional): Starting spending amount carried forward from Phase 1.
                                        If None, uses the default value.
    
    Returns:
    tuple: (float: Present value discounted to the specified age (typically 55),
            float: Final spending amount after inflation growth)
    """
    st.subheader("Phase 2: Go-go (62–70)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # If starting_spending is provided, display it as non-editable and use it
        # Otherwise, use the default value
        if starting_spending is not None:
            st.markdown(f"**Starting Spending: ${starting_spending:,.2f}** (carried forward from previous phase)")
            p2_annual_spending = starting_spending
        else:
            p2_annual_spending = st.number_input(
                "Annual Spending ($)",
                min_value=0,
                value=DEFAULT_PHASE2_SPENDING,
                step=1000,
                key="p2_spending"
            )
        p2_spending_inflation_rate = st.number_input(
            "Spending Inflation Rate (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=DEFAULT_INFLATION_RATE * 100, 
            step=0.1, 
            key="p2_spending_inflation"
        ) / 100
        p2_ss_starting = st.number_input(
            "Social Security Starting Amount ($)", 
            min_value=0, 
            value=DEFAULT_PHASE2_SS_AMOUNT, 
            step=1000, 
            key="p2_ss"
        )
        p2_ss_growth_rate = st.number_input(
            "Social Security Growth Rate (%)", 
            min_value=0.0, 
            max_value=10.0, 
            value=DEFAULT_SS_GROWTH_RATE * 100, 
            step=0.1, 
            key="p2_ss_growth"
        ) / 100
    
    with col2:
        p2_roi = st.number_input(
            "Return on Investment (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=DEFAULT_ROI * 100, 
            step=0.1, 
            key="p2_roi"
        ) / 100
        p2_years = st.number_input(
            "Number of Years", 
            min_value=1, 
            max_value=20, 
            value=DEFAULT_PHASE2_YEARS, 
            step=1, 
            key="p2_years"
        )
        p2_start_age = st.number_input(
            "Phase Start Age", 
            min_value=30, 
            max_value=90, 
            value=DEFAULT_PHASE2_START_AGE, 
            step=1, 
            key="p2_start_age"
        )
        p2_discount_age = st.number_input(
            "Discount to Age", 
            min_value=30, 
            max_value=90, 
            value=DEFAULT_DISCOUNT_AGE, 
            step=1, 
            key="p2_discount_age"
        )
    
    # Calculate Phase 2 results
    p2_pv_at_start, p2_pv_discounted, p2_yearly_data, p2_final_spending = compute_pv_phase_2(
        p2_annual_spending,
        p2_spending_inflation_rate,
        p2_ss_starting,
        p2_ss_growth_rate,
        p2_roi,
        p2_years,
        p2_start_age,
        p2_discount_age
    )
    
    # Display Phase 2 results
    st.subheader("Phase 2 Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Present Value at Phase Start", f"${p2_pv_at_start:,.2f}")
    
    with col2:
        st.metric(f"Present Value Discounted to Age {p2_discount_age}", f"${p2_pv_discounted:,.2f}")
    
    # Display yearly breakdown
    st.subheader("Yearly Breakdown")
    st.dataframe(
        p2_yearly_data.style.format({
            "Social Security": "${:,.2f}",
            "Spending": "${:,.2f}",
            "Net Withdrawal": "${:,.2f}",
            "PV to Phase Start": "${:,.2f}"
        }),
        hide_index=True
    )
    
    # Return the discounted PV and final spending amount
    return p2_pv_discounted, p2_final_spending