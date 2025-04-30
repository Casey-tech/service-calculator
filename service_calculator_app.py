import streamlit as st

# === Client rate profiles with enhanced rules ===
client_profiles = {
    "COD": {
        "labor": 100,
        "ot_labor": 150,
        "travel_type": "hourly",
        "travel_rate": 90,
        "ot_travel_rate": 135,
        "mileage_rate": 0.95
    },
    "Majors": {
        "labor": 90,
        "ot_labor": 135,
        "travel_type": "flat_per_trip",
        "trip_charge": 150,
        "ot_trip_charge": 225,
        "mileage_rate": 0.95
    },
    "Circle K": {
        "labor": 90,
        "ot_labor": 135,
        "travel_type": "hourly",
        "travel_rate": 60,
        "ot_travel_rate": 90,
        "mileage_rate": 0.90
    }
}

SALES_TAX_RATE = 0.07  # 7%

st.title("Service Calculator")
st.write("Includes 7% sales tax and client-specific pricing.")

# Client selection
client_choice = st.selectbox("Select Client", list(client_profiles.keys()))
rates = client_profiles[client_choice]

# Input Fields
labor_hours = st.number_input("Regular Labor Hours", min_value=0.0, step=0.5)
ot_labor_hours = st.number_input("Overtime Labor Hours", min_value=0.0, step=0.5)

# Travel input logic
travel_hours = 0
ot_travel_hours = 0
trip_charge = 0
ot_trip_charge = 0

if rates["travel_type"] == "hourly":
    travel_hours = st.number_input("Travel Time (hrs)", min_value=0.0, step=0.5)
    ot_travel_hours = st.number_input("Overtime Travel Time (hrs)", min_value=0.0, step=0.5)
elif rates["travel_type"] == "flat_per_trip":
    trip_count = st.number_input("Number of Standard Trips", min_value=0, step=1)
    ot_trip_count = st.number_input("Number of OT Trips", min_value=0, step=1)
    trip_charge = trip_count * rates["trip_charge"]
    ot_trip_charge = ot_trip_count * rates["ot_trip_charge"]

miles = st.number_input("Travel Mileage", min_value=0.0, step=1.0)

# Manual part entries
st.subheader("Manual Part Entry")
manual_parts = []
num_manual_parts = st.number_input("How many parts are being used?", min_value=0, step=1)

for i in range(int(num_manual_parts)):
    cols = st.columns([2, 2])
    price = cols[0].number_input(f"Part #{i+1} Price", min_value=0.0, step=0.01, key=f"manual_price_{i}")
    qty = cols[1].number_input(f"Qty #{i+1}", min_value=0, step=1, key=f"manual_qty_{i}")
    manual_parts.append((price, qty))

# Calculate
if st.button("Calculate"):
    part_total = sum(p * q for p, q in manual_parts)
    labor_cost = labor_hours * rates["labor"]
    ot_labor_cost = ot_labor_hours * rates["ot_labor"]

    if rates["travel_type"] == "hourly":
        travel_cost = travel_hours * rates["travel_rate"]
        ot_travel_cost = ot_travel_hours * rates["ot_travel_rate"]
    else:
        travel_cost = trip_charge
        ot_travel_cost = ot_trip_charge

    mileage_cost = miles * rates["mileage_rate"]
    subtotal = labor_cost + ot_labor_cost + travel_cost + ot_travel_cost + mileage_cost + part_total
    tax = subtotal * SALES_TAX_RATE
    total = subtotal + tax

    st.subheader("Cost Breakdown")
    st.write(f"**Client:** {client_choice}")
    st.write(f"**Labor Cost:** ${labor_cost:,.2f}")
    st.write(f"**Overtime Labor Cost:** ${ot_labor_cost:,.2f}")
    st.write(f"**Travel Cost:** ${travel_cost:,.2f}")
    st.write(f"**OT Travel Cost:** ${ot_travel_cost:,.2f}")
    st.write(f"**Mileage Cost:** ${mileage_cost:,.2f}")
    st.write(f"**Parts Total:** ${part_total:,.2f}")
    st.write(f"**Subtotal:** ${subtotal:,.2f}")
    st.write(f"**Sales Tax (7%):** ${tax:,.2f}")
    st.success(f"**Total Cost: ${total:,.2f}**")



