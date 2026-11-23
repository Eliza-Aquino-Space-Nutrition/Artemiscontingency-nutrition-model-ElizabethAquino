import pandas as pd
import numpy as np

# ==============================================================================
# Deterministic Mass and Volume Trade-Off Model for Artemis Contingency Rations
# Author: Elizabeth Aquino Cabrera
# Affiliation: Universidad Europea de Madrid
# ==============================================================================

# 1. Mission Baseline Parameters
crew_size = 4
emergency_days = [14, 30]
daily_energy_kcal = 2800  # NASA exploration baseline (JSC-67378)

# 2. NASA Legacy Contingency Baseline (Carbohydrate-dominant)
energy_density_base = 4.10  # kcal/g
specific_vol_base = 1.35    # cm3/g

daily_mass_base = daily_energy_kcal / energy_density_base
daily_vol_base = daily_mass_base * specific_vol_base

# 3. Proposed Decoupled Anhydrous System (MCT + Dehydrated Protein + Supplements)
mass_mct_g = 210.0   # 9.0 kcal/g, density 0.92 g/cm3
mass_prot_g = 210.0  # 4.3 kcal/g, density 0.85 g/cm3
mass_supp_g = 18.0   # micronutrients & electrolytes, density 0.70 g/cm3

daily_mass_prop = mass_mct_g + mass_prot_g + mass_supp_g
daily_vol_prop = (mass_mct_g / 0.92) + (mass_prot_g / 0.85) + (mass_supp_g / 0.70)

# 4. Compute Crew-Level Mass and Volume Savings
results = []
for days in emergency_days:
    m_base_kg = (daily_mass_base * crew_size * days) / 1000.0
    m_prop_kg = (daily_mass_prop * crew_size * days) / 1000.0
    mass_savings_pct = ((m_base_kg - m_prop_kg) / m_base_kg) * 100.0

    v_base_l = (daily_vol_base * crew_size * days) / 1000.0
    v_prop_l = (daily_vol_prop * crew_size * days) / 1000.0
    vol_savings_pct = ((v_base_l - v_prop_l) / v_base_l) * 100.0

    results.append({
        "Emergency_Days": days,
        "NASA_Mass_kg": round(m_base_kg, 2),
        "Proposed_Mass_kg": round(m_prop_kg, 2),
        "Mass_Savings_pct": round(mass_savings_pct, 1),
        "NASA_Volume_L": round(v_base_l, 2),
        "Proposed_Volume_L": round(v_prop_l, 2),
        "Volume_Savings_pct": round(vol_savings_pct, 1)
    })

df_results = pd.DataFrame(results)
print(df_results.to_string(index=False))
