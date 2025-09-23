# Synthetic Data Generation for Manganese Processing Plant Optimization

## 1. Introduction

The purpose of this project is to generate realistic, **synthetic datasets** for a manganese processing plant to support machine learning (ML) model development and process optimization. Due to limitations in accessing real industrial plant data, synthetic datasets allow safe experimentation while reflecting typical process behavior observed in manganese ore processing.

The datasets cover:

- Ore feed characteristics
- Crushing circuit performance
- Separation circuit performance
- Equipment health monitoring
- Energy consumption patterns
- Ore blending simulation

This report documents the **methodology, formulas, assumptions, and references** used to generate each dataset.

---

## 2. Ore Feed Data Generation

### 2.1 Parameters

Ore characteristics were modeled based on published ranges from mineralogical studies:

| Parameter                 | Typical Range/Mean |
| ------------------------- | ------------------ |
| Manganese (Mn) grade      | 44.13–77.1%        |
| Iron (Fe) content         | 16–22%             |
| Silica (SiO₂)             | 2–8%               |
| Alumina (Al₂O₃)           | 5–8%               |
| Phosphorus (P)            | 0.05–0.3%          |
| Moisture                  | 5–10%              |
| Particle size (P80)       | 5–50 mm            |
| Ore hardness (Work Index) | 8–22 kWh/t         |
| Specific gravity          | 3.2–4.3            |

### 2.2 Formulas

1. **Mn Grade**: Modeled using a **log-normal distribution** to represent the skewness of high-grade ores:

   $$
   \text{mn\_grade} = \text{clip}(\text{lognormal}(\mu = \log(\text{Mn\_mean}), \sigma = 0.3), 15, 52)
   $$

2. **Correlated Element Contents**: Elements inversely correlated to Mn grade:

   $$
   \text{Fe\_content} = \text{uniform}(16,22) \times (1 - \frac{\text{mn\_grade}}{60})
   $$

   $$
   \text{SiO₂\_content} = \text{uniform}(2,8) \times (1 - \frac{\text{mn\_grade}}{60})
   $$

3. **Ore Hardness (Work Index)**:

   $$
   WI = 12 + 0.3 \times \text{mn\_grade} + N(0,1.5)
   $$

4. **Specific Gravity**:

   $$
   SG = 3.2 + 0.02 \times \text{mn\_grade} + N(0,0.1)
   $$

---

## 3. Ore Blending Simulation

### 3.1 Purpose

Blending simulates mixing high-grade and low-grade ores to produce a **final plant product**, which affects recovery, energy consumption, and potential revenue.

### 3.2 Methodology

- Identify high-grade ore (e.g., Mn > 60%) and low-grade ore.
- Mix according to a **blend ratio** to simulate plant feed.
- Use blended feed for downstream simulations (crushing, separation, energy).

### 3.3 Example Formula

If `blend_ratio` is the fraction of high-grade ore in the final mix:

$$
\text{Blended Mn} = \text{blend\_ratio} \times \text{Mn}_{\text{high}} + (1 - \text{blend\_ratio}) \times \text{Mn}_{\text{low}}
$$

### 3.4 Implementation Concept

```python
def blend_ores(ore_data, high_grade_cutoff=60, blend_ratio=0.3):
    high_grade = ore_data[ore_data['mn_grade_pct'] >= high_grade_cutoff]
    low_grade = ore_data[ore_data['mn_grade_pct'] < high_grade_cutoff]
    n_low = len(low_grade)
    n_high = int(n_low * blend_ratio / (1 - blend_ratio))
    high_sample = high_grade.sample(n=min(n_high, len(high_grade)), replace=True)
    blended_feed = pd.concat([low_grade, high_sample]).sample(frac=1).reset_index(drop=True)
    return blended_feed
```

- Blended ore can then be **fed into crushing and separation simulations** for more realistic plant modeling.

---

## 4. Crushing Circuit Data

### 4.1 Parameters

- Crusher capacity: 150 tph
- Crusher gap: 12–25 mm
- Feed rate: 80–140 tph

### 4.2 Formulas

1. **Energy Consumption (Bond’s Law approximation)**:

   $$
   E = WI \times \left( \frac{1}{\sqrt{g}} - \frac{1}{\sqrt{P80}} \right) \times \frac{\text{feed rate}}{100}
   $$

2. **Power Draw (kW)**:

   $$
   P = E \times \text{feed rate} + N(0,50)
   $$

3. **Product P80**: Adjusted for crusher gap and ore hardness:

   $$
   P80_{\text{product}} = g \times (0.8 + 0.4 \cdot R) \times \left(1 + 0.1 \frac{WI - 15}{10} \right)
   $$

4. **Liner Wear & Vibration**: Modeled as cumulative effects of operating hours with noise.

---

## 5. Separation Circuit Data

### 5.1 Parameters

- Spiral speed: 180–220 rpm
- Wash water rate: 0.8–1.5 m³/h per spiral
- Feed density: 15–25% solids
- Magnetic intensity: 0.8–1.5 Tesla
- Belt speed: 0.8–1.2 m/s

### 5.2 Formulas

1. **Spiral Separation Efficiency**:

   $$
   \eta_{\text{spiral}} = \text{base\_efficiency} + 0.003 \times \text{mn\_grade} - 0.0001 \times (speed-200)^2 + N(0,0.05)
   $$

2. **Concentrate Grade**:

   $$
   \text{conc\_grade} = \text{mn\_grade} / (1 - \eta_{\text{spiral}}) \times 1.3
   $$

3. **Recovery**:

   $$
   R = \eta_{\text{spiral}} \times (\text{conc\_grade}/\text{mn\_grade}) \times 0.85
   $$

4. **Magnetic Separation Adjustment**: Efficiency adjusted for ore type and intensity.

---

## 6. Equipment Health Data

- Health score decreases with cumulative operating hours.

- Vibration, temperature, and power factor are functions of health score.

- Remaining Useful Life (RUL) is proportional to health score:

  $$
  RUL = \text{health\_score}/100 \times 1825 + N(0,100)
  $$

- Failure probability:

  $$
  P_{\text{failure}} = 1 - (\text{health\_score}/100)^2
  $$

---

## 7. Energy Consumption Data

- Total plant power is the sum of crushing, separation, conveyor, pump, and base load power.
- Operational factors account for night shifts (reduced load).
- Random maintenance shutdowns applied with 5% probability.

---

## 8. Assumptions

1. Synthetic values are generated based on **statistical distributions** aligned with published ore characteristics.
2. Physical relationships (e.g., Bond’s law, spiral recovery formulas) are used to maintain realistic process behavior.
3. Equipment health and energy consumption are approximated based on typical industrial patterns.
4. Ore blending is modeled to reflect **mixing high- and low-grade ore** as in real plant operations.

---

## 9. References

1. Bhavan, I. (2022). *Indian Minerals Yearbook 2020 (Part-III: MINERAL REVIEWS) 59th Edition MANGANESE ORE (ADVANCE RELEASE)*. Government of India, Ministry of Mines, Indian Bureau of Mines. [Link](https://ibm.gov.in/writereaddata/files/04272022163406Manganese_2020.pdf)
2. Cannon, W. F., Kimball, B. E., & Corathers, L. A. (2017). *Manganese. Professional Paper*. [DOI: 10.3133/pp1802]\([https://doi.org/10.3133](https://doi.org/10.3133)
3. Africa, M. R. (2024, August 28). *Marula Mining confirms high-grade Manganese in Kenya*. Miningreview\.com. [https://www.miningreview.com/manganese/marula-mining-confirms-high-grade-manganese-in-kenya/  ](https://www.miningreview.com/manganese/marula-mining-confirms-high-grade-manganese-in-kenya/  )
4. *MANGANESE (Data in thousand metric tons, gross weight, unless otherwise specified)*. (2019). [https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-manganese.pdf](https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-manganese.pdf)? 

