import streamlit as st
from engine.products import PRODUCTS
from engine.generator import generate_customer
from engine.rules import decision_engine

from datetime import datetime
import csv
import os

st.header("🧾 Müştəri Kredit Müraciəti")

# Məhsul seçimi
product = st.selectbox("Məhsulu seçin", list(PRODUCTS.keys()))
price = PRODUCTS[product]
st.write(f"💰 Qiymət: **{price} AZN**")

# İlkin ödəniş
down_payment = st.slider(
    "İlkin ödəniş məbləği",
    0, price, int(price * 0.1)
)

# Müddət
term = st.selectbox("Müddət (ay)", [6, 12, 18, 24, 36])

# AKB icazəsi
akb = st.checkbox("AKB məlumatlarının yoxlanmasına icazə verirəm")

# CSV fayl yolu
CSV_PATH = os.path.join("data", "history.csv")

# Müraciət düyməsi
if st.button("📨 Müraciət et"):
    if not akb:
        st.error("Müraciət üçün AKB icazəsi vacibdir.")
    else:
        # 1) Arxa planda random müştəri dataları
        customer = generate_customer()

        # 2) Tətbiq məlumatları
        application = {
            "product": product,
            "price": price,
            "down_payment": down_payment,
            "term": term,
            "min_amount": price - down_payment
        }

        # 3) Admin qaydaları (yoxdursa default)
        rules = st.session_state.get("rules")
        if not rules:
            rules = {
                "max_late_count": 5,
                "max_late_days": 30,
                "min_amount_low": 20,
                "min_amount_high": 100,
                "max_applications": 11,
                "age_min": 18,
                "age_max": 70,
                "max_rate_decline": 30,
                "approve_applications": 3,
                "approve_age_min": 24,
                "approve_age_max": 60,
                "max_rate_approve": 24,
                "min_down_payment_ratio": 0.20
            }

        # 4) Qərar + səbəblər
        decision, reasons = decision_engine(customer, application, rules)

        # 5) CSV-yə yaz (fayl yoxdursa başlıqla yarat)
        file_exists = os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0
        os.makedirs("data", exist_ok=True)

        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "date","product","price","down_payment","term",
                    "decision","reason",
                    "age","address","guarantor",
                    "late_count","late_days","applications","max_rate"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                product,
                price,
                down_payment,
                term,
                decision,
                "; ".join(reasons),
                customer["age"],
                customer["address"],
                customer["guarantor"],
                customer["late_count"],
                customer["late_days_total"],
                customer["applications"],
                customer["max_rate"]
            ])

        # 6) Ekranda göstər
        st.divider()
        st.subheader("📌 Qərar")

        d = decision.lower()
        if "təsdiq" in d or "tesdiq" in d:
            st.success(decision)
        elif "imtina" in d:
            st.error(decision)
        elif "təklif" in d or "teklif" in d or "ilkin ödəniş" in d or "ilkin odenis" in d:
            st.warning(decision)
        else:
            st.info(decision)

        st.caption("Qərar səbəbləri: " + ", ".join(reasons))

        with st.expander("🔍 AKB / Texniki məlumatlar (demo üçün)"):
            st.json({
                "application": application,
                "customer": customer,
                "rules": rules
            })
