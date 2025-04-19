import streamlit as st
import pandas as pd

# === Load part data ===
try:
    parts_df = pd.read_csv("parts.csv")
    parts_df['PartNumber'] = parts_df['PartNumber'].str.upper()
    parts_df['Price'] = parts_df['Price'].astype(float)
    part_dict = dict(zip(parts_df['PartNumber'], parts_df['Price']))
except Exception as e:
    st.error(f"Error loading parts.csv: {e}")
    part_dict = {}

# === Rates ===
LABOR_RATE = 100
OT_LABOR_RATE = 150
TRAVEL_RATE = 90
OT_TRAVEL_RATE = 135
MILEAGE_RATE = 0.95

# === UI ===
st.title("Guardian Calc")
st.write("Enter the details below to calculate the total cost for a service job.")

# Input Fields
labor_hours = st.number_input("Regular Labor Hours", min_value=0.0, step=0.5)
ot_labor_hours = st.number_input("Overtime Labor Hours", min_value=0.0, step=0.5)
travel_hours = st.number_input("Regular Travel Hours", min_value=0.0, step=0.5)
ot_travel_hours = st.number_input("Overtime Travel Hours", min_value=0.0, step=0.5)
miles = st.number_input("Travel Mileage", min_value=0.0, step=1.0)

# Part Section 1: Known part numbers
st.subheader("Parts From Inventory")

part_entries = []
num_parts = st.number_input("How many known parts were used?", min_value=0, step=1)

for i in range(int(num_parts)):
    cols = st.columns([3, 2])
    part_number = cols[0].text_input(f"Part #{i+1} Number", key=f"pn_{i}").upper()
    quantity = cols[1].number_input(f"Qty #{i+1}", min_value=0, step=1, key=f"qty_{i}")
    unit_price = part_dict.get(part_number, 0)
    part_entries.append((part_number, quantity, unit_price, "from inventory"))

# Part Section 2: Manual entry
st.subheader("Unknown Part Numbers (Manual Entry)")

manual_part_entries = []
num_manual_parts = st.number_input("How many manual parts to enter?", min_value=0, step=1)

for i in range(int(num_manual_parts)):
    cols = st.columns([2, 2])
    manual_price = cols[0].number_input(f"Manual Part #{i+1} Price", min_value=0.0, step=0.01, key=f"manual_price_{i}")
    quantity = cols[1].number_input(f"Manual Qty #{i+1}", min_value=0, step=1, key=f"manual_qty_{i}")
    manual_part_entries.append((f"Manual-{i+1}", quantity, manual_price, "manual entry"))

# Calculate Button
if st.button("Calculate"):
    part_cost_total = 0
    part_breakdown = []

    # Process known parts
    for part_number, quantity, unit_price, source in part_entries:
        total = unit_price * quantity
        part_cost_total += total
        part_breakdown.append((part_number, quantity, unit_price, total, source))

    # Process manual parts
    for label, quantity, unit_price, source in manual_part_entries:
        total = unit_price * quantity
        part_cost_total += total
        part_breakdown.append((label, quantity, unit_price, total, source))

    labor_cost = labor_hours * LABOR_RATE
    ot_labor_cost = ot_labor_hours * OT_LABOR_RATE
    travel_cost = travel_hours * TRAVEL_RATE
    ot_travel_cost = ot_travel_hours * OT_TRAVEL_RATE
    mileage_cost = miles * MILEAGE_RATE

    total_cost = labor_cost + ot_labor_cost + travel_cost + ot_travel_cost + mileage_cost + part_cost_total

    st.subheader("Cost Breakdown")
    st.write(f"**Labor Cost:** ${labor_cost:,.2f}")
    st.write(f"**Overtime Labor Cost:** ${ot_labor_cost:,.2f}")
    st.write(f"**Travel Time Cost:** ${travel_cost:,.2f}")
    st.write(f"**Overtime Travel Cost:** ${ot_travel_cost:,.2f}")
    st.write(f"**Mileage Cost:** ${mileage_cost:,.2f}")
    st.write(f"**Total Parts Cost:** ${part_cost_total:,.2f}")

    st.subheader("Parts Used")
    for part_number, quantity, price, total, source in part_breakdown:
        st.write(f"{quantity} × {part_number} ({source}) @ ${price:.2f} = ${total:.2f}")

    st.success(f"**Total Cost: ${total_cost:,.2f}**")
