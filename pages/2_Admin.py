import streamlit as st

st.header("🛠️ Admin Panel – Qaydalar")

# Default rules
if "rules" not in st.session_state:
    st.session_state.rules = {
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

rules = st.session_state.rules

st.subheader("❌ İmtina Qaydaları")
rules["max_late_count"] = st.slider("Maks gecikmə sayı", 0, 10, rules["max_late_count"])
rules["max_late_days"] = st.slider("Maks gecikmə günləri cəmi", 0, 120, rules["max_late_days"])
rules["max_applications"] = st.slider("Maks müraciət sayı (imtina)", 1, 20, rules["max_applications"])
rules["age_min"] = st.slider("Minimum yaş", 18, 30, rules["age_min"])
rules["age_max"] = st.slider("Maksimum yaş", 60, 75, rules["age_max"])
rules["max_rate_decline"] = st.slider("Faiz limiti (imtina)", 20, 50, rules["max_rate_decline"])

st.subheader("✅ Təsdiq Qaydaları")
rules["approve_applications"] = st.slider("Maks müraciət sayı (təsdiq)", 0, 10, rules["approve_applications"])
rules["approve_age_min"] = st.slider("Təsdiq min yaş", 18, 40, rules["approve_age_min"])
rules["approve_age_max"] = st.slider("Təsdiq max yaş", 50, 70, rules["approve_age_max"])
rules["max_rate_approve"] = st.slider("Faiz limiti (təsdiq)", 10, 30, rules["max_rate_approve"])

st.subheader("💰 İlkin ödəniş qaydası")
rules["min_down_payment_ratio"] = st.slider(
    "Minimum ilkin ödəniş faizi",
    0.05, 0.50, rules["min_down_payment_ratio"]
)

st.success("Qaydalar yadda saxlanıldı və dərhal tətbiq olunur ✅")

with st.expander("🔍 Cari qaydalar (JSON)"):
    st.json(rules)
