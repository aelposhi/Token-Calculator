import streamlit as st
import pandas as pd

# Define token cost per service type (Updated from latest document)
services = {
    "Personal Photos": 7,
    "Contracts": 7,
    "Stamp, Signature, and QR": 5,
    "Passports": 7,
    "ID": 5,
    "Invoices": 7,
    "Entry Permit File": 4,
    "Residency File": 4,
    "Immigration File": 4
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

# Define term-based discount rates
def calculate_discount(subscription_term, payment_option):
    term_discount = 1.0  # No discount by default
    if subscription_term == 2:
        term_discount = 0.90  # 10% savings for two-year term
    elif subscription_term == 3:
        term_discount = 0.80  # 20% savings for three-year term
    
    upfront_discount = 1.0  # No discount by default
    if payment_option == "Upfront Payment":
        upfront_discount = 0.90  # Additional 10% discount for upfront payment
    
    return term_discount * upfront_discount


def calculate_needed_tokens(user_inputs):
    return sum(services[service] * user_inputs[service] for service in user_inputs if service in services)

def recommend_plan(total_tokens):
    for plan, details in plans.items():
        if total_tokens <= details["Tokens Included"]:
            return plan, details
    return "Titan", plans["Titan"]  # Default to highest plan if usage is very high

st.title("Khwarizm Token Calculator")

# User inputs for service usage
st.subheader("Enter the number of Pages and Photos required per Service/Month:")
user_inputs = {service: st.number_input(f"{service}", min_value=0, step=1) for service in services.keys()}

# User input for payment preference
payment_option = st.radio("Select Payment Option:", ["Monthly Billing", "Upfront Payment"])

# User input for subscription term
subscription_term = st.selectbox("Select Subscription Term:", [1, 2, 3])

# Calculate required tokens
if st.button("Recommend Best Plan"):
    total_tokens = calculate_needed_tokens(user_inputs)
    recommended_plan, plan_details = recommend_plan(total_tokens)
    
    overage_tokens = max(0, total_tokens - plan_details["Tokens Included"])
    overage_cost = overage_tokens * plan_details["Overage Rate"]
    monthly_total = plan_details["Price"] + overage_cost
    annual_total_monthly = monthly_total * 12
    
    # Apply correct discount calculation
    total_discount = calculate_discount(subscription_term, payment_option)
    annual_total_upfront = annual_total_monthly * total_discount
    
    st.subheader("Recommended Plan and Cost Breakdown")
    st.write(f"**Recommended Plan:** {recommended_plan}")
    st.write(f"**Tokens Needed Monthly:** {total_tokens}")
    st.write(f"**Tokens Included Monthly:** {plan_details['Tokens Included']}")
    st.write(f"**Overage Tokens Monthly:** {overage_tokens}")
    st.write(f"**Overage Rate per Token:** ${plan_details['Overage Rate']:.4f}")
    st.write(f"**Overage Monthly Cost:** ${overage_cost:.2f}")
    st.write(f"**Total Monthly Cost:** ${monthly_total:.2f}")
    st.write(f"**Annual Cost (Monthly Billing):** ${annual_total_monthly:.2f}")
    if payment_option == "Upfront Payment":
        discount_percentage = 100 - (total_discount * 100)
        st.write(f"**Annual Cost (Upfront Payment - {discount_percentage:.0f}% Discount for {subscription_term} Year(s)):** ${annual_total_upfront:.2f}")
