import pandas as pd
import random
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

print("🚀 Generating Complete 3-Table Dataset (with City & Address data)...")

# --- SETTINGS ---
NUM_VENDORS = 260
NUM_ORDERS = 5000
IMAGES_PER_VENDOR = 3

SHARED_BANK_RING = "0098765432_Zenith"
SHARED_PHONE_RING = "+234 701 999 0000"
SHARED_ADDRESS_RING = "Block B, Industrial Estate, Ogba, Lagos" # Restored Fraud Ring Address

SHADOW_BANK = "0055443322_GTB"
SHADOW_PHONE = "+234 802 111 2222"

vendors = []
images = []
orders = []

order_pool = [] 

# ==========================================
# 1. GENERATE VENDORS
# ==========================================
for i in range(1, NUM_VENDORS + 1):
    v_id = i
    
    is_ring = v_id in [1, 2, 3, 4, 5]
    is_shadow_duo = v_id in [100, 101]
    is_medium_risk = 200 <= v_id <= 230
    is_solo_fraud = v_id > 245
    
    name_base = f"{fake.color_name()} {random.choice(['Suya', 'Jollof', 'Yam', 'Egusi', 'Boli'])} {random.choice(['Hub', 'Kitchen', 'Chow', 'Express'])}"
    restaurant_name = name_base 
    
    # --- RESTORED LOCATION & DATE DATA ---
    raw_date = fake.date_between(start_date='-150d', end_date='-30d')
    signup_date = raw_date.strftime('%Y-%m-%d') if i % 7 != 0 else raw_date.strftime('%d/%m/%Y')
    city = random.choice(["LAGOS", "lagos", "Abuja", "ABUJA", "Ibadan", "P.H."])
    
    if is_ring:
        phone, bank, address = SHARED_PHONE_RING, SHARED_BANK_RING, SHARED_ADDRESS_RING
        acc_type, cac_v, tin_v = "Personal", False, False
        f_label = "Fraud Ring"
        tickets = 3 
    elif is_shadow_duo:
        phone, bank, address = SHADOW_PHONE, SHADOW_BANK, fake.address().replace("\n", ", ")
        acc_type, cac_v, tin_v = "Corporate", True, True
        f_label = "Legit (Shared Info)"
        tickets = 25 
    elif is_medium_risk:
        phone, bank, address = fake.phone_number(), fake.iban(), fake.address().replace("\n", ", ")
        acc_type, cac_v, tin_v = "Personal", True, True
        f_label = "Medium Risk"
        tickets = 10 
    elif is_solo_fraud:
        phone, bank, address = fake.phone_number(), fake.iban(), fake.address().replace("\n", ", ")
        acc_type, cac_v, tin_v = "Personal", False, False
        f_label = "Individual Fraud"
        tickets = 2 
    else:
        phone, bank, address = fake.phone_number(), fake.iban(), fake.address().replace("\n", ", ")
        acc_type, cac_v, tin_v = "Corporate", True, True
        f_label = "Legit"
        tickets = 30 

    order_pool.extend([v_id] * tickets)

    if is_ring or is_solo_fraud:
        dup_score = random.randint(75, 100)
        ref_rate = round(random.uniform(0.20, 0.50), 2)
        fail_rate = round(random.uniform(0.15, 0.40), 2)
    elif is_medium_risk:
        dup_score = random.randint(40, 70)
        ref_rate = round(random.uniform(0.08, 0.15), 2)
        fail_rate = round(random.uniform(0.05, 0.12), 2)
    else:
        dup_score = random.randint(0, 20)
        ref_rate = round(random.uniform(0.01, 0.05), 2)
        fail_rate = round(random.uniform(0.01, 0.04), 2)

    score = 0
    if not tin_v: score += 25
    if dup_score > 70: score += 20
    if acc_type == "Personal": score += 15
    if ref_rate > 0.15: score += 20
    if fail_rate > 0.10: score += 10
    
    category = "Critical" if score >= 60 else "High" if score >= 40 else "Medium" if score >= 20 else "Low"

    # Columns added back into the dictionary export
    vendors.append({
        "vendor_id": v_id, 
        "restaurant_name": restaurant_name, 
        "signup_date": signup_date,
        "city": city,
        "address": address,
        "phone_number": phone, 
        "bank_account": bank, 
        "cac_verified": cac_v, 
        "tin_verified": tin_v, 
        "account_type": acc_type, 
        "duplicate_image_score": dup_score, 
        "refund_rate": ref_rate, 
        "delivery_failure_rate": fail_rate, 
        "risk_score": score, 
        "risk_category": category, 
        "fraud_label": f_label
    })

    # ==========================================
    # 2. GENERATE IMAGES
    # ==========================================
    for img_num in range(1, IMAGES_PER_VENDOR + 1):
        img_dup_score = min(100, max(0, dup_score + random.randint(-10, 10)))
        img_source = "Social Media" if img_dup_score > 50 else "Original Upload"
        
        images.append({
            "image_id": (v_id * 10) + img_num, 
            "vendor_id": v_id,
            "duplicate_score": img_dup_score,
            "image_source": img_source
        })

# ==========================================
# 3. GENERATE ORDERS
# ==========================================
for o_id in range(1, NUM_ORDERS + 1):
    v_id = random.choice(order_pool)
    v_info = next(item for item in vendors if item["vendor_id"] == v_id)
    
    amt = round(random.uniform(4000.0, 22000.0), 2)
    time = fake.date_time_between(start_date='-30d', end_date='now')
    
    if v_info["fraud_label"] in ["Fraud Ring", "Individual Fraud"]:
        status = random.choice(["Delivered", "Failed", "Cancelled"])
        refund = random.choice([True, True, False])
        rating = round(random.uniform(1.0, 2.5), 1) if status == "Delivered" else None
    elif v_info["fraud_label"] == "Medium Risk":
        status = random.choice(["Delivered", "Delivered", "Failed"])
        refund = random.choice([True, False, False])
        rating = round(random.uniform(2.5, 4.0), 1) if status == "Delivered" else None
    else:
        status = random.choice(["Delivered", "Delivered", "Delivered", "Failed"])
        refund = random.choice([False, False, False, True])
        rating = round(random.uniform(3.8, 5.0), 1) if status == "Delivered" else None

    # Added datetime stripping so it writes cleanly to Excel
    orders.append({
        "order_id": o_id, "vendor_id": v_id, "order_amount": amt, 
        "order_time": time.replace(tzinfo=None),
        "delivery_status": status, "customer_rating": rating, "refund_requested": refund
    })

# ==========================================
# 4. EXPORT TO A SINGLE EXCEL WORKBOOK
# ==========================================
file_name = "Marketplace_Fraud_Dataset.xlsx"

with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
    pd.DataFrame(vendors).to_excel(writer, sheet_name="Vendors", index=False)
    pd.DataFrame(images).to_excel(writer, sheet_name="Images", index=False)
    pd.DataFrame(orders).to_excel(writer, sheet_name="Orders", index=False)

print("==========================================")
print(f"✅ SUCCESS! Data Generation Complete.")
print(f"📂 Saved to: {file_name}")
print(f"📊 Sheet 1: {len(vendors)} Vendors (Now including City & Address)")
print(f"🖼️ Sheet 2: {len(images)} Images")
print(f"📦 Sheet 3: {len(orders)} Orders")
print("==========================================")
