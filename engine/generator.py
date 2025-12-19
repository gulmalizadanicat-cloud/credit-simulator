import random

def generate_customer():
    return {
        "late_count": random.choices([0,1,2,3,4,5,6],[0.6,0.1,0.1,0.08,0.06,0.04,0.02])[0],
        "late_days_total": random.randint(0, 60),
        "applications": random.randint(0, 15),
        "guarantor": random.choice(["Var","Yox"]),
        "age": random.randint(18, 70),
        "address": random.choice(["Bakı","Sumqayıt","Abşeron","Digər"]),
        "max_rate": round(random.uniform(10, 45), 2)
    }
