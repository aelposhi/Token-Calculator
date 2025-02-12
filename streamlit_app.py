import streamlit as st
import pandas as pd

# Define token cost per service type (Updated from latest document)
services = {
    "Personal Photos": 7,  # Cost per photo
    "Contracts": 7,  # Cost per page
    "Stamp, Signature, and QR": 5,  # Cost per page
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


def calculate_needed_tokens(user_inputs):
    return sum(services[service] * user_inputs[service] for service in user_inputs if service in services)

def recommend_best_plan(total_tokens):
    best_plan = None
    best_cost = float("inf")
    selected_plan = None
    
    plan_names = list(plans.keys())
    for i, (plan, details) in enumerate(plans.items()):
        tokens_included = details["Tokens Included"]
        base_price = details["Price"]
        overage_rate = details["Overage Rate"]
        
        if total_tokens <= tokens_included:
            cost = base_price  # No overage cost
        else:
            overage_tokens = total_tokens - tokens_included
            overage_cost = overage_tokens * overage_rate
            cost = base_price + overage_cost
        
        # Check if upgrading to the next plan is cheaper
        if i < len(plan_names) - 1:
            next_plan = plan_names[i + 1]
            next_plan_cost = plans[next_plan]["Price"]
            if next_plan_cost < cost:
                best_plan, best_cost = next_plan, next_plan_cost
                continue
        
        if cost < best_cost:
            best_plan, best_cost = plan, cost
    
    return best_plan, plans[best_plan]

st.title("Khwarizm Token Calculator")

# User inputs for service usage
st.subheader("Enter the monthly number of pages or photos required:")
user_inputs = {
    "Personal Photos": st.number_input("Personal Photos", min_value=0, step=1, help="Number of personal photos to be processed per month."),
    "Contracts": st.number_input("Contracts", min_value=0, step=1, help="Number of contract pages to be processed per month."),
    "Stamp, Signature, and QR": st.number_input("Stamp, Signature, and QR", min_value=0, step=1, help="Number of pages containing stamp, signature, or QR to be processed per month."),
    "Passports": st.number_input("Passports", min_value=0, step=1, help="Number of passport pages to be processed per month."),
    "ID": st.number_input("ID", min_value=0, step=1, help="Number of ID photos to be processed per month. Note: Id front and back are counted as two photos"),
    "Invoices": st.number_input("Invoices", min_value=0, step=1, help="Number of invoice pages to be processed per month."),
    "Entry Permit File": st.number_input("Entry Permit File", min_value=0, step=1, help="Number of entry permit file pages to be processed per month."),
    "Residency File": st.number_input("Residency File", min_value=0, step=1, help="Number of residency file pages to be processed per month."),
    "Immigration File": st.number_input("Immigration File", min_value=0, step=1, help="Number of immigration file pages to be processed per month.")
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

# Calculate required tokens
if st.button("Recommend Best Plan"):
    total_tokens = calculate_needed_tokens(user_inputs)
    recommended_plan, plan_details = recommend_best_plan(total_tokens)
    
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
    st.write(f"**Tokens Included Monthly:** {plan_details['Tokens Included']:,}")
    st.write(f"**Overage Rate per Token:** ${plan_details['Overage Rate']:,.4f}")
    st.write(f"**Overage Tokens Monthly:** {overage_tokens:,}")
    
    st.write(f"**Standard Monthly Subscription Cost:** ${standard_monthly_subscription_cost:,.2f}")
    st.write(f"**Monthly Subscription Cost (Including Overage):** ${monthly_total:,.2f}")
    
    st.subheader("Cost Calculation")
    st.write(f"**Overage Monthly Cost:** ${overage_cost:,.2f}")
    st.write(f"**Total Cost for {subscription_term}:** ${total_term_cost:,.2f}")
    st.write(f"**Term Discount:** {term_discount}%")
    st.write(f"**Upfront Payment Discount:** {upfront_discount}%")
    st.write(f"**Total Discount Applied:** {total_discount}%")
    st.write(f"**Final Cost After Discounts:** ${total_cost_after_discount:,.2f}")
    
    if subscription_term in ["Two-Year", "Three-Year"]:
        st.subheader("Annual Breakdown")
        for year in range(1, term_length + 1):
            year_discounted_cost = (monthly_total * 12) * (1 - (total_discount / 100))
            st.write(f"**Year {year} Cost After Discount:** ${year_discounted_cost:,.2f}")
