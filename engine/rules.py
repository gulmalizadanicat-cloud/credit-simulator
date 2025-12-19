def decision_engine(c, app, rules):
    reasons = []

    if c["late_count"] > rules["max_late_count"]:
        reasons.append("Gecikmə sayı yüksəkdir")

    if c["late_days_total"] > rules["max_late_days"]:
        reasons.append("Gecikmə günləri çoxdur")

    if rules["min_amount_low"] <= app["min_amount"] <= rules["min_amount_high"]:
        reasons.append("Kredit məbləği risklidir")

    if c["applications"] > rules["max_applications"]:
        reasons.append("Çox sayda kredit müraciəti")

    if c["guarantor"] == "Var":
        reasons.append("Zaminlik mövcuddur")

    if c["age"] < rules["age_min"] or c["age"] > rules["age_max"]:
        reasons.append("Yaş limiti uyğun deyil")

    if c["address"] == "Digər":
        reasons.append("Qeydiyyat ünvanı uyğun deyil")

    if c["max_rate"] > rules["max_rate_decline"]:
        reasons.append("Faiz limiti aşılır")

    # ❌ İMTİNA
    if reasons:
        return "Kreditinizə imtina olundu", reasons

    # ✅ TƏSDİQ
    if (
        c["late_count"] == 0 and
        c["applications"] <= rules["approve_applications"] and
        c["guarantor"] == "Yox" and
        rules["approve_age_min"] <= c["age"] <= rules["approve_age_max"] and
        c["address"] != "Digər" and
        c["max_rate"] <= rules["max_rate_approve"]
    ):
        return "Kreditiniz təsdiq olundu", ["Risk faktorları yoxdur"]

    # 💰 İLKİN ÖDƏNİŞ TƏKLİFİ
    min_dp = int(app["price"] * rules["min_down_payment_ratio"])
    if app["down_payment"] < min_dp:
        return f"İlkin ödəniş {min_dp} AZN olarsa mümkündür", ["İlkin ödəniş azdır"]

    return "Kredit mütəxəssisinin təhlilinə ehtiyac var", ["Manual baxış tələb olunur"]
