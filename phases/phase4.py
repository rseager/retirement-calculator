import streamlit as st
from utils.calculations import compute_pv_phase_4
from utils.config import (
    DEFAULT_PHASE4_SPENDING,
    DEFAULT_PHASE4_DECLINE_RATE,
    DEFAULT_PHASE4_SS_AMOUNT,
    DEFAULT_SS_GROWTH_RATE,
    DEFAULT_ROI,
    DEFAULT_PHASE4_YEARS,
    DEFAULT_PHASE4_START_AGE,
    DEFAULT_DISCOUNT_AGE
)

def run_phase4(starting_spending=None):
    """
    Renders the Phase 4 (No-go) tab and returns the discounted PV to age 55
    along with the final spending amount.
    
    Parameters:
    starting_spending (float, optional): Starting spending amount carried forward from Phase 3.
                                        If None, uses the default value.
    
    Returns:
    tuple: (float: Present value discounted to the specified age (typically 55),
            float: Final spending amount after decline)
    """
    st.subheader("Phase 4: No-go (80+)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # If starting_spending is provided, display it as non-editable and use it
        # Otherwise, use the default value
        if starting_spending is not None:
            st.markdown(f"**Starting Spending: ${starting_spending:,.2f}** (carried forward from previous phase)")
            p4_annual_spending = starting_spending
        else:
            p4_annual_spending = st.number_input(
                "Annual Spending ($)",
                min_value=0,
                value=DEFAULT_PHASE4_SPENDING,
                step=1000,
                key="p4_spending"
            )
        p4_spending_decline_rate = st.number_input(
            "Spending Decline Rate (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=DEFAULT_PHASE4_DECLINE_RATE * 100, 
            step=0.1, 
            key="p4_spending_decline"
        ) / 100
        p4_ss_starting = st.number_input(
            "Social Security Starting Amount ($)", 
            min_value=0, 
            value=DEFAULT_PHASE4_SS_AMOUNT, 
            step=1000, 
            key="p4_ss"
        )
        p4_ss_growth_rate = st.number_input(
            "SS Growth Rate (%)", 
            min_value=0.0, 
            max_value=10.0, 
            value=DEFAULT_SS_GROWTH_RATE * 100, 
            step=0.1, 
            key="p4_ss_growth"
        ) / 100
    
    with col2:
        p4_roi = st.number_input(
            "Return on Investment (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=DEFAULT_ROI * 100, 
            step=0.1, 
            key="p4_roi"
        ) / 100
        p4_years = st.number_input(
            "Number of Years", 
            min_value=1, 
            max_value=30, 
            value=DEFAULT_PHASE4_YEARS, 
            step=1, 
            key="p4_years"
        )
        p4_start_age = st.number_input(
            "Phase Start Age", 
            min_value=30, 
            max_value=100, 
            value=DEFAULT_PHASE4_START_AGE, 
            step=1, 
            key="p4_start_age"
        )
        p4_discount_age = st.number_input(
            "Discount to Age", 
            min_value=30, 
            max_value=90, 
            value=DEFAULT_DISCOUNT_AGE, 
            step=1, 
            key="p4_discount_age"
        )
    
    # Calculate Phase 4 results
    p4_pv_at_start, p4_pv_discounted, p4_yearly_data, p4_final_spending = compute_pv_phase_4(
        p4_annual_spending,
        p4_spending_decline_rate,
        p4_ss_starting,
        p4_ss_growth_rate,
        p4_roi,
        p4_years,
        p4_start_age,
        p4_discount_age
    )
    
    # Display Phase 4 results
    st.subheader("Phase 4 Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Present Value at Phase Start", f"${p4_pv_at_start:,.2f}")
    
    with col2:
        st.metric(f"Present Value Discounted to Age {p4_discount_age}", f"${p4_pv_discounted:,.2f}")
    
    # Display yearly breakdown
    st.subheader("Yearly Breakdown")
    st.dataframe(
        p4_yearly_data.style.format({
            "Social Security": "${:,.2f}",
            "Spending": "${:,.2f}",
            "Net Withdrawal": "${:,.2f}",
            "PV to Phase Start": "${:,.2f}"
        }),
        hide_index=True
    )
    
    # Return the discounted PV and final spending amount
    return p4_pv_discounted, p4_final_spending