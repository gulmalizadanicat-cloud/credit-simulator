import streamlit as st
import pandas as pd

st.header("🧑‍💼 Kreditor Paneli")

df = pd.read_csv("data/history.csv")

st.write("CSV sütunları:", list(df.columns))
st.dataframe(df)
st.stop()
import streamlit as st
import pandas as pd

st.header("🧑‍💼 Kreditor Paneli")

df = pd.read_csv("data/history.csv")

if df.empty:
    st.info("Hələ müraciət yoxdur.")
else:
    st.subheader("📋 Gələn müraciətlər")
    st.dataframe(df[[
        "date","product","price","down_payment","term","decision"
    ]])

    st.divider()

    st.subheader("🔍 Müraciət detalları")
    idx = st.selectbox(
        "Baxmaq istədiyiniz müraciəti seçin",
        df.index,
        format_func=lambda x: f"{df.loc[x,'date']} – {df.loc[x,'product']}"
    )

    record = df.loc[idx]

    st.markdown("### 🧾 Müraciət Məlumatları")
    st.json({
        "Məhsul": record["product"],
        "Qiymət": record["price"],
        "İlkin ödəniş": record["down_payment"],
        "Müddət": record["term"],
        "Qərar": record["decision"]
    })

    st.markdown("### 🧠 AKB / Risk Məlumatları")
    st.json({
        "Yaş": record["age"],
        "Ünvan": record["address"],
        "Zaminlik": record["guarantor"],
        "Gecikmə sayı": record["late_count"],
        "Gecikmə günləri": record["late_days"],
        "Müraciət sayı": record["applications"],
        "Maks faiz": record["max_rate"]
    })

    st.markdown("### ❗ Qərar Səbəbləri")
    st.warning(record["reason"])
