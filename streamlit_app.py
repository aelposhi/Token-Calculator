import streamlit as st
import pandas as pd

# Define token cost per service type (Updated from latest document)
services = {
    "Personal Photos": 7,  # Cost per photo
    "Contracts": 7,  # Cost per page
    "Stamp, Signature, and QR": 5,  # Cost per verification
    "Passports": 7,  # Cost per page
    "ID": 5,  # Cost per photo
    "Invoices": 7,  # Cost per page
    "Entry Permit File": 4,  # Cost per page
    "Residency File": 4,  # Cost per page
    "Immigration File": 4  # Cost per page
}

# Define subscription plans (Updated from latest document)
plans = {
    "Starter": {"Price": 99, "Tokens Included": 2000, "Overage Rate": 0.0590},
    "Builder": {"Price": 399, "Tokens Included": 9000, "Overage Rate": 0.0528},
    "Professional": {"Price": 999, "Tokens Included": 25000, "Overage Rate": 0.0476},
    "Advanced": {"Price": 2499, "Tokens Included": 70000, "Overage Rate": 0.0426},
    "Enterprise": {"Price": 5499, "Tokens Included": 180000, "Overage Rate": 0.0364},
    "Ultimate": {"Price": 9999, "Tokens Included": 400000, "Overage Rate": 0.0298},
    "Titan": {"Price": 14999, "Tokens Included": 750000, "Overage Rate": 0.0238}
}

# Define term-based and upfront discounts (Updated to match Subscription Scenarios)
def calculate_discount(subscription_term, payment_option):
    term_discount = 0
    upfront_discount = 0
    
    if subscription_term == "Two-Year":
        term_discount = 10  # 10% savings for two-year term
    elif subscription_term == "Three-Year":
        term_discount = 20  # 20% savings for three-year term
    
    if payment_option == "Upfront Payment":
        upfront_discount = 10  # Additional 10% savings for upfront payment
    
    total_discount = term_discount + upfront_discount
    return total_discount, term_discount, upfront_discount


def calculate_needed_tokens(user_inputs, input_type):
    factor = 1 if input_type == "Monthly" else 12  # Convert annual inputs to monthly
    return int(-(-sum(services[service] * (user_inputs[service] / factor) for service in user_inputs if service in services) // 1))  # Round up to nearest integer

def recommend_best_plan(total_tokens, strategy):
    best_plan = None
    best_cost = float("inf")
    selected_plan = None
    
    plan_names = list(plans.keys())
    for i, (plan, details) in enumerate(plans.items()):
        tokens_included = details["Tokens Included"]
        base_price = details["Price"]
        overage_rate = details["Overage Rate"]
        
        if strategy == "Nearest Plan":
            if total_tokens <= tokens_included:
                return plan, details  # Select the smallest plan that fully covers the tokens
        
        if total_tokens <= tokens_included:
            cost = base_price  # No overage cost
        else:
            overage_tokens = total_tokens - tokens_included
            overage_cost = overage_tokens * overage_rate
            cost = base_price + overage_cost
        
        if strategy == "Cost Optimization" and i < len(plan_names) - 1:
            next_plan = plan_names[i + 1]
            next_plan_cost = plans[next_plan]["Price"]
            if next_plan_cost < cost:
                best_plan, best_cost = next_plan, next_plan_cost
                continue
        
        if cost < best_cost:
            best_plan, best_cost = plan, cost
    
    return best_plan, plans[best_plan]

st.title("Khwarizm Token Calculator")

# User input for monthly or annual service usage
st.subheader("Enter the number of pages and photos needed for each service:")
input_type = st.radio(
    "How would you like to enter your service usage?",
    ["Monthly", "Annually"],
    help="Select whether to enter the number of services processed per month or per year."
)

# User inputs for service usage with detailed hints
user_inputs = {
    service: st.number_input(
        f"{service} ({input_type})", min_value=0, step=1, format="%d",
        help=f"Enter the expected number of {service} to be processed {input_type.capitalize()}.")
    for service in services.keys()
}

# User input for payment preference
payment_option = st.radio(
    "Select Payment Option:",
    ["Monthly Billing", "Upfront Payment"],
    help="Choose whether you want to pay monthly or upfront for additional savings."
)

# User input for subscription term
subscription_term = st.selectbox(
    "Select Subscription Term:",
    ["One-Year", "Two-Year", "Three-Year"],
    help="Select the duration of your subscription. Longer terms provide additional discounts."
)

# User input for subscription strategy
strategy = st.radio(
    "Select Subscription Recommendation Strategy:",
    ["Nearest Plan", "Cost Optimization"],
    help="Choose whether to select the nearest plan that fully covers the tokens or optimize for the lowest total cost."
)

# Calculate required tokens
if st.button("Recommend Best Plan"):
    total_tokens = calculate_needed_tokens(user_inputs, input_type)
    recommended_plan, plan_details = recommend_best_plan(total_tokens, strategy)
    
    overage_tokens = max(0, total_tokens - plan_details["Tokens Included"])
    overage_cost = overage_tokens * plan_details["Overage Rate"]
    standard_monthly_subscription_cost = plan_details["Price"]
    monthly_total = standard_monthly_subscription_cost + overage_cost
    term_length = 1 if subscription_term == "One-Year" else (2 if subscription_term == "Two-Year" else 3)
    total_term_cost = monthly_total * 12 * term_length
    
    # Apply correct discount calculation based on Subscription Scenarios
    total_discount, term_discount, upfront_discount = calculate_discount(subscription_term, payment_option)
    total_cost_after_discount = total_term_cost * (1 - total_discount / 100)
    
    st.subheader("Token Calculation")
    st.write(f"**Monthly Tokens Needed:** {total_tokens:,}")

    st.subheader("Subscription Plan Details")
    st.write(f"**Recommended Plan:** {recommended_plan}")
    st.write(f"**Subscription Term:** {subscription_term}")
    st.write(f"**Monthly Subscription Cost:** ${standard_monthly_subscription_cost:,.2f}")
    st.write(f"**Tokens Included Monthly:** {plan_details['Tokens Included']:,}")
    st.write(f"**Overage Tokens Monthly:** {overage_tokens:,}")
    st.write(f"**Overage Rate per Token:** ${plan_details['Overage Rate']:,.4f}")

    
    st.subheader("Cost Calculation")
    st.write(f"**Monthly Subscription Cost:** ${standard_monthly_subscription_cost:,.2f}")
    st.write(f"**Overage Monthly Cost:** ${overage_cost:,.2f}")
    st.write(f"**Monthly Subscription Cost (Including Overage):** ${monthly_total:,.2f}")
    st.write(f"**Total Cost for {subscription_term}:** ${total_term_cost:,.2f}")
    st.write(f"**Final Cost After Discounts:** ${total_cost_after_discount:,.2f}")
    
    st.subheader("Discount Breakdown")
    st.write(f"**Term Discount:** {term_discount}%")
    st.write(f"**Upfront Payment Discount:** {upfront_discount}%")
    st.write(f"**Total Discount Applied:** {total_discount}%")

    if subscription_term in ["Two-Year", "Three-Year"]:
        st.subheader("Annual Breakdown")
        for year in range(1, term_length + 1):
            year_discounted_cost = (monthly_total * 12) * (1 - (total_discount / 100))
            st.write(f"**Year {year} Cost After Discount:** ${year_discounted_cost:,.2f}")
