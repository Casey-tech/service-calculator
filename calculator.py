import pandas as pd
import os
print("Looking for parts.csv in:", os.getcwd())


# === RATES ===
LABOR_RATE = 100
OT_LABOR_RATE = 150
TRAVEL_RATE = 90
OT_TRAVEL_RATE = 135
MILEAGE_RATE = 0.95

# === LOAD PART DATA FROM CSV ===
try:
    parts_df = pd.read_csv("parts.csv")
    part_dict = dict(zip(parts_df['PartNumber'].str.upper(), parts_df['Price'].astype(float)))
except Exception as e:
    print("Error reading parts.csv:", e)
    part_dict = {}

# === INPUT FUNCTIONS ===
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_part_number():
    part = input("Enter part number (e.g. ABC123): ").upper()
    if part not in part_dict:
        print("Part not found in spreadsheet. Using $0.00 as price.")
    return part

# === COLLECT INPUT ===
print("\n=== Service Job Calculator (Spreadsheet Version) ===\n")

labor_hours = get_float("Enter regular labor hours: ")
ot_labor_hours = get_float("Enter overtime labor hours: ")
travel_hours = get_float("Enter regular travel hours: ")
ot_travel_hours = get_float("Enter overtime travel hours: ")
miles = get_float("Enter travel mileage: ")

part_number = get_part_number()
part_quantity = get_float("Enter quantity of that part used: ")

# === COST CALCULATIONS ===
labor_cost = labor_hours * LABOR_RATE
ot_labor_cost = ot_labor_hours * OT_LABOR_RATE
travel_cost = travel_hours * TRAVEL_RATE
ot_travel_cost = ot_travel_hours * OT_TRAVEL_RATE
mileage_cost = miles * MILEAGE_RATE
part_cost = part_dict.get(part_number, 0) * part_quantity

total_cost = labor_cost + ot_labor_cost + travel_cost + ot_travel_cost + mileage_cost + part_cost

# === OUTPUT ===
print("\n=== Invoice Breakdown ===")
print(f"Labor Cost:               ${labor_cost:,.2f}")
print(f"Overtime Labor Cost:      ${ot_labor_cost:,.2f}")
print(f"Travel Time Cost:         ${travel_cost:,.2f}")
print(f"Overtime Travel Cost:     ${ot_travel_cost:,.2f}")
print(f"Mileage Cost:             ${mileage_cost:,.2f}")
print(f"Part Cost ({part_number}):         ${part_cost:,.2f}")
print(f"\nTOTAL COST:               ${total_cost:,.2f}")

input("\nPress Enter to exit...")
