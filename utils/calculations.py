import pandas as pd

# Reusable function for growing annuity formula
def growing_annuity_pv(payment, growth_rate, discount_rate, years):
    """
    Calculate the present value of a growing annuity.
    
    Parameters:
    payment (float): Initial payment amount
    growth_rate (float): Annual growth rate (decimal)
    discount_rate (float): Annual discount rate (decimal)
    years (int): Number of years
    
    Returns:
    float: Present value of the growing annuity
    """
    if abs(growth_rate - discount_rate) < 1e-10:  # Rates are effectively equal
        return payment * years / (1 + discount_rate)
    
    factor = (1 - ((1 + growth_rate) / (1 + discount_rate)) ** years) / (discount_rate - growth_rate)
    return payment * factor

# Function to discount a value from one age to another
def discount_to_age(value, current_age, target_age, discount_rate):
    """
    Discount a value from current age to target age.
    
    Parameters:
    value (float): Value to discount
    current_age (int): Current age
    target_age (int): Target age to discount to
    discount_rate (float): Annual discount rate (decimal)
    
    Returns:
    float: Discounted value
    """
    years = current_age - target_age
    return value / ((1 + discount_rate) ** years)

# Phase 1 calculation function
def compute_pv_phase_1(annual_spending, inflation_rate, roi, years, start_age, discount_age):
    """
    Compute the present value for Phase 1 of retirement.
    
    Parameters:
    annual_spending (float): Initial annual spending
    inflation_rate (float): Annual inflation rate (decimal)
    roi (float): Return on investment (decimal)
    years (int): Number of years in Phase 1
    start_age (int): Age at the start of Phase 1
    discount_age (int): Age to discount the present value to
    
    Returns:
    tuple: (PV at phase start, PV discounted to specified age, yearly data DataFrame)
    """
    total_pv = 0
    yearly_data = []
    
    current_spending = annual_spending
    
    for year in range(years):
        current_age = start_age + year
        
        # Apply inflation to spending (only after first year)
        if year > 0:
            current_spending *= (1 + inflation_rate)
        
        # Discount to phase start
        pv_to_phase_start = current_spending / ((1 + roi) ** year)
        
        total_pv += pv_to_phase_start
        
        yearly_data.append({
            "Year": year + 1,
            "Age": current_age,
            "Spending": current_spending,
            "PV to Phase Start": pv_to_phase_start
        })
    
    # Discount total PV to specified age
    pv_discounted = discount_to_age(total_pv, start_age, discount_age, roi)
    # Return the final spending amount as well
    return total_pv, pv_discounted, pd.DataFrame(yearly_data), current_spending
    return total_pv, pv_discounted, pd.DataFrame(yearly_data)

# Phase 2 calculation function
def compute_pv_phase_2(annual_spending, spending_inflation_rate, ss_starting_amount, ss_growth_rate, roi, years, start_age, discount_age):
    """
    Compute the present value for Phase 2 of retirement (Go-go years).
    
    Parameters:
    annual_spending (float): Initial annual spending
    spending_inflation_rate (float): Annual spending inflation rate (decimal)
    ss_starting_amount (float): Social Security starting amount
    ss_growth_rate (float): Social Security growth rate (decimal)
    roi (float): Return on investment (decimal)
    years (int): Number of years in Phase 2
    start_age (int): Age at the start of Phase 2
    discount_age (int): Age to discount the present value to
    
    Returns:
    tuple: (PV at phase start, PV discounted to specified age, yearly data DataFrame)
    """
    total_pv = 0
    yearly_data = []
    
    ss_amount = ss_starting_amount
    current_spending = annual_spending
    
    for year in range(years):
        current_age = start_age + year
        
        # Apply growth to Social Security and spending inflation (only after first year)
        if year > 0:
            ss_amount *= (1 + ss_growth_rate)
            current_spending *= (1 + spending_inflation_rate)
        
        # Calculate net withdrawal (spending minus Social Security)
        net_withdrawal = max(0, current_spending - ss_amount)
        
        # Discount to phase start
        pv_to_phase_start = net_withdrawal / ((1 + roi) ** year)
        
        total_pv += pv_to_phase_start
        
        yearly_data.append({
            "Year": year + 1,
            "Age": current_age,
            "Social Security": ss_amount,
            "Spending": current_spending,
            "Net Withdrawal": net_withdrawal,
            "PV to Phase Start": pv_to_phase_start
        })
    
    # Discount total PV to specified age
    pv_discounted = discount_to_age(total_pv, start_age, discount_age, roi)
    # Return the final spending amount as well
    return total_pv, pv_discounted, pd.DataFrame(yearly_data), current_spending
    return total_pv, pv_discounted, pd.DataFrame(yearly_data)

# Phase 3 calculation function
def compute_pv_phase_3(annual_spending, spending_decline_rate, ss_starting_amount, ss_growth_rate, roi, years, start_age, discount_age):
    """
    Compute the present value for Phase 3 of retirement (Slo-go years).
    
    Parameters:
    annual_spending (float): Initial annual spending
    spending_decline_rate (float): Annual spending decline rate (decimal)
    ss_starting_amount (float): Social Security starting amount
    ss_growth_rate (float): Social Security growth rate (decimal)
    roi (float): Return on investment (decimal)
    years (int): Number of years in Phase 3
    start_age (int): Age at the start of Phase 3
    discount_age (int): Age to discount the present value to
    
    Returns:
    tuple: (PV at phase start, PV discounted to specified age, yearly data DataFrame)
    """
    total_pv = 0
    yearly_data = []
    
    ss_amount = ss_starting_amount
    current_spending = annual_spending
    
    for year in range(years):
        current_age = start_age + year
        
        # Apply growth to Social Security and decline to spending (only after first year)
        if year > 0:
            ss_amount *= (1 + ss_growth_rate)
            current_spending *= (1 - spending_decline_rate)  # Note: Declining spending
        
        # Calculate net withdrawal (spending minus Social Security)
        net_withdrawal = max(0, current_spending - ss_amount)
        
        # Discount to phase start
        pv_to_phase_start = net_withdrawal / ((1 + roi) ** year)
        
        total_pv += pv_to_phase_start
        
        yearly_data.append({
            "Year": year + 1,
            "Age": current_age,
            "Social Security": ss_amount,
            "Spending": current_spending,
            "Net Withdrawal": net_withdrawal,
            "PV to Phase Start": pv_to_phase_start
        })
    
    # Discount total PV to specified age
    pv_discounted = discount_to_age(total_pv, start_age, discount_age, roi)
    # Return the final spending amount as well
    return total_pv, pv_discounted, pd.DataFrame(yearly_data), current_spending
    return total_pv, pv_discounted, pd.DataFrame(yearly_data)

# Phase 4 calculation function
def compute_pv_phase_4(annual_spending, spending_decline_rate, ss_starting_amount, ss_growth_rate, roi, years, start_age, discount_age):
    """
    Compute the present value for Phase 4 of retirement (No-go years).
    
    Parameters:
    annual_spending (float): Initial annual spending
    spending_decline_rate (float): Annual spending decline rate (decimal)
    ss_starting_amount (float): Social Security starting amount
    ss_growth_rate (float): Social Security growth rate (decimal)
    roi (float): Return on investment (decimal)
    years (int): Number of years in Phase 4
    start_age (int): Age at the start of Phase 4
    discount_age (int): Age to discount the present value to
    
    Returns:
    tuple: (PV at phase start, PV discounted to specified age, yearly data DataFrame)
    """
    total_pv = 0
    yearly_data = []
    
    ss_amount = ss_starting_amount
    current_spending = annual_spending
    
    for year in range(years):
        current_age = start_age + year
        
        # Apply growth to Social Security and decline to spending (only after first year)
        if year > 0:
            ss_amount *= (1 + ss_growth_rate)
            current_spending *= (1 - spending_decline_rate)  # Note: Declining spending
        
        # Calculate net withdrawal (spending minus Social Security)
        net_withdrawal = max(0, current_spending - ss_amount)
        
        # Discount to phase start
        pv_to_phase_start = net_withdrawal / ((1 + roi) ** year)
        
        total_pv += pv_to_phase_start
        
        yearly_data.append({
            "Year": year + 1,
            "Age": current_age,
            "Social Security": ss_amount,
            "Spending": current_spending,
            "Net Withdrawal": net_withdrawal,
            "PV to Phase Start": pv_to_phase_start
        })
    
    # Discount total PV to specified age
    pv_discounted = discount_to_age(total_pv, start_age, discount_age, roi)
    # Return the final spending amount as well
    return total_pv, pv_discounted, pd.DataFrame(yearly_data), current_spending
    return total_pv, pv_discounted, pd.DataFrame(yearly_data)