"""
Manganese processing Plant synthetic data generator.
This script generates realistic yet synthetic datasets for Machine Learning model development

AUTHOR: DARLENE WENDY NASIMIYU
Purpose: Create comprehensive datasets for manganese processing plant optimization

"""


"""
The simulation begins with the ore dataset, which establishes the foundation by characterizing manganese
feed in terms of grade percentage, size distribution, hardness, and ore type (oxide or carbonate), 
providing the variability that drives downstream performance.
This ore data is then used to generate the crushing dataset, where equipment throughput, product size,
and power draw are modeled as functions of ore hardness and crusher type, incorporating wear, operational efficiency,
 and energy demand. Building on this, the separation dataset reflects gravity (spiral concentrators) and magnetic 
 separation stages, where parameters such as spiral speed, wash water, feed density, and magnetic field intensity are 
 used to predict concentrate grade, tailings quality, and recovery efficiency, while adjusting performance according 
 to ore type. Finally, the energy dataset integrates all process stages with plant-wide loads by combining crushing and
separation power requirements with auxiliary demands from pumps and conveyors, while also embedding seasonal 
variability, daily shifts, maintenance downtime, and dynamic electricity tariffs. 
Collectively, these interconnected datasets capture the theoretical performance of a typical manganese processing plant, 
creating a digital twin that reflects both operational complexity and economic implications.

"""

import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings('ignore')

class ManganeseDataGenerator:
    def __init__(self, random_state=42):
        np.random.seed(random_state)

        # Manganese processing plant parameters
        self.plant_capacity = 2000  #Tonnes per day
        self.operating_hours = 20  # Hours in a day

        # Ore characteristics ranges (based on typical manganese ores
        self.ore_params = {
            'mn_grade_mean': 62.0,  # Avg manganese grade
            'mn_grade_std':8.0, # Standard Deviation
            'fe_content_range':(16,22),  # Fe content %
            'siO2_range': (2,8), # Silica content %
            'al2O3_range':(5,8), # Alumina content %
            'p_range':(0.05,0.3), # Phosphorus content %
            'moisture_range': (5,10),   # Moisture content %

        }

        self.equipment_params = {
            'crusher_capacity': 150, #tph
            'spiral_efficiency_base': (0.75),
            'magnetic_sep_efficiency': (0.80),
            'screen_efficiency_base': (0.90),
        }

    def generate_ore_feed_data(self, n_samples = 10000):
        print("Generating ORE feed data......")

        #Generate primary Mn grade (log-normal distribution)
        mn_grades = np.random.lognormal(
            mean=np.log(self.ore_params['mn_grade_mean']),
            sigma=0.3,
            size=n_samples
        )
        mn_grades = np.clip(mn_grades, 44.13, 77.71)

        # Generate correlated elements (inverse correlation with Mn)
        fe_content = np.random.uniform(*self.ore_params['fe_content_range'], n_samples)
        fe_content = fe_content * (1 - mn_grades/60)


        siO2_content = np.random.uniform(*self.ore_params['siO2_range'], n_samples)
        siO2_content = siO2_content * (1 - mn_grades / 60)  # Higher Mn == Lower Fe

        al2O3_content = np.random.uniform(*self.ore_params['al2O3_range'], n_samples)
        p_content = np.random.uniform(*self.ore_params['p_range'], n_samples)
        moisture = np.random.uniform(*self.ore_params['moisture_range'], n_samples)

        # Particle size distribution
        p80 = np.random.lognormal(mean=np.log(15), sigma=0.4, size=n_samples)
        p80 = np.clip(p80, 5, 50)  # mm

        # Ore hardness (Work Index -kWh/t)
        work_index = 12 + 0.3 * mn_grades + np.random.normal(0, 1.5, n_samples)
        work_index = np.clip(work_index, 8, 22)

        # Specific gravity
        specific_gravity = 3.2 + 0.02 * mn_grades + np.random.normal(0, 0.1, n_samples)

        # Time stamp
        start_date = datetime.datetime(2020, 1, 1)
        timestamps = [start_date + datetime.timedelta(hours=i * 6) for i in range(n_samples)]

        ore_data = pd.DataFrame({
            'timestamp': timestamps,
            'mn_grade_pct': np.round(mn_grades, 2),
            'fe_content_pct': np.round(fe_content, 2),
            'siO2_content_pct': np.round(siO2_content, 2),
            'al2O3_content_pct': np.round(al2O3_content, 2),
            'p_content_pct': np.round(p_content, 3),
            'moisture_pct': np.round(moisture, 1),
            'p80_mm': np.round(p80, 1),
            'work_index_kwh_t': np.round(work_index, 1),
            'specific_gravity': np.round(specific_gravity, 2),
            'ore_type': np.random.choice(['oxide', 'carbonate', 'silicate'], n_samples, p=[0.6, 0.3, 0.1])
        })

        print(f"Generated {len(ore_data)} ore feed records")
        return ore_data

    def blend_ores(self, ore_data, high_grade_cutoff=60, blend_ratio=0.3):
        """
        Simulate blending high-grade and low-grade ore.
        """
        high_grade = ore_data[ore_data['mn_grade_pct'] >= high_grade_cutoff]
        low_grade = ore_data[ore_data['mn_grade_pct'] < high_grade_cutoff]

        n_low = len(low_grade)
        n_high = int(n_low * blend_ratio / (1 - blend_ratio))
        high_sample = high_grade.sample(n=min(n_high, len(high_grade)), replace=True)

        blended_feed = pd.concat([low_grade, high_sample]).sample(frac=1).reset_index(drop=True)
        print(f"Blended {len(blended_feed)} ore feed records")
        return blended_feed


    def generate_crushing_data(self, ore_data, n_samples=15000):
        """Generate crushing circuit performance data"""
        print("Generating Crushing Circuit Dataset...")

        # Sample from ore data for crushing operations
        ore_sample_idx = np.random.choice(len(ore_data), n_samples, replace=True)
        base_ore = ore_data.iloc[ore_sample_idx].reset_index(drop=True)

        # Generate crusher operating parameters
        feed_rate = np.random.uniform(80, 140, n_samples)  # tph
        crusher_gap = np.random.uniform(12, 25, n_samples)  # mm

        # Calculate crusher performance (physics-based relationships)
        # Bond's law for energy consumption
        energy_consumption = (base_ore['work_index_kwh_t'] *
                              (1 / np.sqrt(crusher_gap) - 1 / np.sqrt(base_ore['p80_mm'])) *
                              feed_rate / 100)

        # Power draw (kW)
        power_draw = energy_consumption * feed_rate + np.random.normal(0, 50, n_samples)
        power_draw = np.clip(power_draw, 200, 800)

        # Product size (influenced by gap setting and ore hardness)
        product_p80 = crusher_gap * (0.8 + 0.4 * np.random.random(n_samples))
        product_p80 *= (1 + 0.1 * (base_ore['work_index_kwh_t'] - 15) / 10)

        # Crusher liner wear (increases with runtime)
        operating_hours = np.cumsum(np.random.exponential(1, n_samples)) % (30 * 24)
        liner_wear = 100 * (1 - operating_hours / (30 * 24)) + np.random.normal(0, 5, n_samples)
        liner_wear = np.clip(liner_wear, 20, 100)

        # Vibration levels (increase with wear)
        vibration_rms = 2 + (100 - liner_wear) * 0.05 + np.random.normal(0, 0.3, n_samples)

        # Create timestamps (hourly data)
        start_date = datetime.datetime(2020, 1, 1)
        timestamps = [start_date + datetime.timedelta(hours=i) for i in range(n_samples)]

        crushing_data = pd.DataFrame({
            'timestamp': timestamps,
            'feed_rate_tph': np.round(feed_rate, 1),
            'crusher_gap_mm': np.round(crusher_gap, 1),
            'power_draw_kw': np.round(power_draw, 0),
            'product_p80_mm': np.round(product_p80, 1),
            'liner_wear_pct': np.round(liner_wear, 1),
            'vibration_rms_mm_s': np.round(vibration_rms, 2),
            'ore_hardness_wi': base_ore['work_index_kwh_t'],
            'feed_moisture_pct': base_ore['moisture_pct']
        })

        print(f"Generated {len(crushing_data)} crushing records")
        return crushing_data

    def generate_separation_data(self, ore_data, n_samples=12000):
        """Generate gravity and magnetic separation data"""
        print("Generating Separation Circuit Dataset...")

        ore_sample_idx = np.random.choice(len(ore_data), n_samples, replace=True)
        base_ore = ore_data.iloc[ore_sample_idx].reset_index(drop=True)

        # Spiral separator parameters
        spiral_speed = np.random.uniform(180, 220, n_samples)  # rpm
        wash_water_rate = np.random.uniform(0.8, 1.5, n_samples)  # m3/h per spiral
        feed_density = np.random.uniform(15, 25, n_samples)  # % solids

        # Calculate spiral separation efficiency
        # Higher Mn grade and optimal speed increase efficiency
        spiral_efficiency = (self.equipment_params['spiral_efficiency_base'] +
                             0.003 * base_ore['mn_grade_pct'] -
                             0.0001 * (spiral_speed - 200) ** 2)
        spiral_efficiency += np.random.normal(0, 0.05, n_samples)
        spiral_efficiency = np.clip(spiral_efficiency, 0.5, 0.95)

        # Concentrate and tailings grades
        concentrate_grade = base_ore['mn_grade_pct'] / (1 - spiral_efficiency) * 1.3
        concentrate_grade = np.clip(concentrate_grade, base_ore['mn_grade_pct'], 48)

        tailings_grade = base_ore['mn_grade_pct'] * (1 - spiral_efficiency) * 0.4

        # Recovery calculation
        recovery = spiral_efficiency * (concentrate_grade / base_ore['mn_grade_pct']) * 0.85
        recovery = np.clip(recovery, 0.4, 0.9)

        # Magnetic separation parameters
        magnetic_intensity = np.random.uniform(0.8, 1.5, n_samples)  # Tesla
        belt_speed = np.random.uniform(0.8, 1.2, n_samples)  # m/s

        # Magnetic separation efficiency (depends on ore type and intensity)
        mag_efficiency = self.equipment_params['magnetic_sep_efficiency']
        oxide_mask = base_ore['ore_type'] == 'oxide'
        mag_efficiency_adj = np.where(oxide_mask,
                                      mag_efficiency * 0.9,  # Lower for oxides
                                      mag_efficiency)

        mag_efficiency_adj *= (0.9 + 0.2 * (magnetic_intensity - 0.8) / 0.7)
        mag_efficiency_adj = np.clip(mag_efficiency_adj, 0.6, 0.95)

        # Final concentrate grade after magnetic separation
        final_concentrate_grade = concentrate_grade * mag_efficiency_adj * 1.1
        final_concentrate_grade = np.clip(final_concentrate_grade, concentrate_grade, 50)

        # Overall recovery
        overall_recovery = recovery * mag_efficiency_adj

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 2)
                      for i in range(n_samples)]

        separation_data = pd.DataFrame({
            'timestamp': timestamps,
            'feed_grade_pct': np.round(base_ore['mn_grade_pct'], 2),
            'spiral_speed_rpm': np.round(spiral_speed, 0),
            'wash_water_m3h': np.round(wash_water_rate, 2),
            'feed_density_pct_solids': np.round(feed_density, 1),
            'spiral_concentrate_grade_pct': np.round(concentrate_grade, 2),
            'spiral_tailings_grade_pct': np.round(tailings_grade, 2),
            'spiral_recovery': np.round(recovery, 3),
            'magnetic_intensity_t': np.round(magnetic_intensity, 2),
            'belt_speed_ms': np.round(belt_speed, 2),
            'final_concentrate_grade_pct': np.round(final_concentrate_grade, 2),
            'overall_recovery': np.round(overall_recovery, 3),
            'ore_type': base_ore['ore_type']
        })

        print(f"Generated {len(separation_data)} separation records")
        return separation_data

    def generate_equipment_health_data(self, n_samples=8000):
        """Generate comprehensive equipment health monitoring data for complete manganese processing plant"""
        print("Generating Equipment Health Dataset...")

        # Complete equipment types for manganese processing plant
        equipment_types = [
            'primary_crusher', 'secondary_crusher', 'tertiary_crusher',
            'vibrating_screen', 'trommel_screen', 'dewatering_screen',
            'spiral_concentrator', 'jig', 'shaking_table',
            'magnetic_separator_lims', 'magnetic_separator_hims',
            'flotation_cell_rougher', 'flotation_cell_cleaner', 'flotation_cell_scavenger',
            'dms_cyclone', 'hydrocyclone',
            'thickener', 'vacuum_filter', 'filter_press',
            'slurry_pump', 'sump_pump', 'transfer_pump',
            'conveyor_belt', 'apron_feeder', 'vibrating_feeder',
            'agitator', 'air_blower', 'reagent_dosing_pump'
        ]

        # Generate equipment IDs (2-5 units per equipment type depending on criticality)
        equipment_ids = []
        equipment_counts = {
            'primary_crusher': 2, 'secondary_crusher': 3, 'tertiary_crusher': 2,
            'vibrating_screen': 5, 'trommel_screen': 2, 'dewatering_screen': 3,
            'spiral_concentrator': 8, 'jig': 4, 'shaking_table': 3,
            'magnetic_separator_lims': 4, 'magnetic_separator_hims': 3,
            'flotation_cell_rougher': 6, 'flotation_cell_cleaner': 4, 'flotation_cell_scavenger': 3,
            'dms_cyclone': 3, 'hydrocyclone': 5,
            'thickener': 2, 'vacuum_filter': 3, 'filter_press': 2,
            'slurry_pump': 12, 'sump_pump': 6, 'transfer_pump': 8,
            'conveyor_belt': 15, 'apron_feeder': 4, 'vibrating_feeder': 3,
            'agitator': 5, 'air_blower': 4, 'reagent_dosing_pump': 6
        }

        for eq_type, count in equipment_counts.items():
            equipment_ids.extend([f"{eq_type}_{i:02d}" for i in range(1, count + 1)])

        health_data = []

        for i in range(n_samples):
            equipment_id = np.random.choice(equipment_ids)
            equipment_type = '_'.join(equipment_id.split('_')[:-1])  # Handle multi-word equipment types

            # Operating hours (affects health) - varies by equipment type
            if 'crusher' in equipment_type or 'pump' in equipment_type:
                max_hours = 8760 * 5  # 5 years for high-wear equipment
            elif 'conveyor' in equipment_type or 'screen' in equipment_type:
                max_hours = 8760 * 7  # 7 years
            else:
                max_hours = 8760 * 8  # 8 years for other equipment

            operating_hours = np.random.uniform(0, max_hours, 1)[0]

            # Base health score (decreases with age)
            expected_life = max_hours * 2  # Total design life
            base_health = 100 * (1 - operating_hours / expected_life)
            base_health += np.random.normal(0, 10)
            base_health = np.clip(base_health, 20, 100)

            # Equipment-specific parameters based on equipment type
            if 'crusher' in equipment_type:
                vibration = 2.5 + (100 - base_health) * 0.12 + np.random.normal(0, 0.6)
                temperature = 65 + (100 - base_health) * 0.35 + np.random.normal(0, 6)
                power_factor = 0.85 - (100 - base_health) * 0.002
                wear_rate = (100 - base_health) * 0.8  # Liner wear

            elif 'pump' in equipment_type:
                vibration = 1.8 + (100 - base_health) * 0.09 + np.random.normal(0, 0.4)
                temperature = 75 + (100 - base_health) * 0.45 + np.random.normal(0, 9)
                power_factor = 0.90 - (100 - base_health) * 0.0015
                wear_rate = (100 - base_health) * 0.6  # Impeller wear

            elif 'screen' in equipment_type:
                vibration = 3.5 + (100 - base_health) * 0.15 + np.random.normal(0, 0.7)
                temperature = 50 + (100 - base_health) * 0.25 + np.random.normal(0, 4)
                power_factor = 0.87 - (100 - base_health) * 0.0018
                wear_rate = (100 - base_health) * 0.9  # Screen deck wear

            elif 'flotation' in equipment_type:
                vibration = 1.2 + (100 - base_health) * 0.06 + np.random.normal(0, 0.25)
                temperature = 40 + (100 - base_health) * 0.15 + np.random.normal(0, 3)
                power_factor = 0.89 - (100 - base_health) * 0.001
                wear_rate = (100 - base_health) * 0.4  # Impeller/stator wear

            elif 'magnetic' in equipment_type:
                vibration = 1.5 + (100 - base_health) * 0.07 + np.random.normal(0, 0.3)
                temperature = 55 + (100 - base_health) * 0.28 + np.random.normal(0, 5)
                power_factor = 0.88 - (100 - base_health) * 0.0012
                wear_rate = (100 - base_health) * 0.5  # Belt/drum wear

            elif 'spiral' in equipment_type or 'jig' in equipment_type:
                vibration = 1.0 + (100 - base_health) * 0.05 + np.random.normal(0, 0.2)
                temperature = 35 + (100 - base_health) * 0.12 + np.random.normal(0, 2)
                power_factor = 0.86 - (100 - base_health) * 0.0008
                wear_rate = (100 - base_health) * 0.7  # Surface wear

            elif 'conveyor' in equipment_type:
                vibration = 2.0 + (100 - base_health) * 0.10 + np.random.normal(0, 0.45)
                temperature = 48 + (100 - base_health) * 0.22 + np.random.normal(0, 4)
                power_factor = 0.84 - (100 - base_health) * 0.0016
                wear_rate = (100 - base_health) * 0.85  # Belt wear

            elif 'thickener' in equipment_type or 'filter' in equipment_type:
                vibration = 0.8 + (100 - base_health) * 0.04 + np.random.normal(0, 0.15)
                temperature = 38 + (100 - base_health) * 0.10 + np.random.normal(0, 2)
                power_factor = 0.91 - (100 - base_health) * 0.0009
                wear_rate = (100 - base_health) * 0.3  # Media/cloth wear

            elif 'cyclone' in equipment_type:
                vibration = 1.3 + (100 - base_health) * 0.06 + np.random.normal(0, 0.25)
                temperature = 42 + (100 - base_health) * 0.18 + np.random.normal(0, 3)
                power_factor = 0.87 - (100 - base_health) * 0.0010
                wear_rate = (100 - base_health) * 0.65  # Liner wear

            else:  # Feeders, agitators, blowers, etc.
                vibration = 1.4 + (100 - base_health) * 0.07 + np.random.normal(0, 0.3)
                temperature = 52 + (100 - base_health) * 0.24 + np.random.normal(0, 4)
                power_factor = 0.88 - (100 - base_health) * 0.0011
                wear_rate = (100 - base_health) * 0.55

            # Clip values to realistic ranges
            vibration = np.clip(vibration, 0.3, 20)
            temperature = np.clip(temperature, 25, 135)
            power_factor = np.clip(power_factor, 0.55, 0.98)
            wear_rate = np.clip(wear_rate, 0, 100)

            # Failure probability (increases with poor health and wear)
            failure_prob = (1 - (base_health / 100) ** 2) * (1 + wear_rate / 200)
            failure_prob = np.clip(failure_prob, 0, 0.85)

            # Remaining useful life (days)
            rul_days = (base_health / 100) * 1825 * (1 - wear_rate / 200)
            rul_days += np.random.normal(0, 100)
            rul_days = np.clip(rul_days, 1, 2500)

            # Maintenance priority (1=critical, 5=low)
            if failure_prob > 0.5:
                maintenance_priority = 1
            elif failure_prob > 0.3:
                maintenance_priority = 2
            elif failure_prob > 0.15:
                maintenance_priority = 3
            elif failure_prob > 0.05:
                maintenance_priority = 4
            else:
                maintenance_priority = 5

            timestamp = (datetime.datetime(2020, 1, 1) +
                         datetime.timedelta(hours=np.random.randint(0, n_samples * 2)))

            health_data.append({
                'timestamp': timestamp,
                'equipment_id': equipment_id,
                'equipment_type': equipment_type,
                'operating_hours': np.round(operating_hours, 0),
                'health_score': np.round(base_health, 1),
                'vibration_rms': np.round(vibration, 2),
                'temperature_c': np.round(temperature, 1),
                'power_factor': np.round(power_factor, 3),
                'wear_rate_pct': np.round(wear_rate, 1),
                'failure_probability': np.round(failure_prob, 4),
                'rul_days': np.round(rul_days, 0),
                'maintenance_priority': maintenance_priority
            })

        equipment_health = pd.DataFrame(health_data)

        # Summary statistics
        unique_equipment = equipment_health['equipment_type'].nunique()
        total_units = equipment_health['equipment_id'].nunique()

        print(f"Generated {len(equipment_health)} equipment health records")
        print(f"Equipment types: {unique_equipment}")
        print(f"Total equipment units: {total_units}")

        return equipment_health

    """
    The synthetic dataset generated by the function, while comprehensive, incorporates several simplifications that 
    limit its realism. The operating hours are treated as continuous over arbitrary maximums of 5–8 years, 
    assuming near-constant operation, whereas actual manganese plants have variable duty cycles, scheduled downtime, 
    and unplanned stoppages, which significantly affect equipment wear. Health scores are modeled as a linear function 
    of operating hours with added random noise, yet in reality, degradation is non-linear and subject to abrupt failures, 
    cumulative fatigue, and operational shocks, making the dataset less representative of sudden or irregular wear events. 
    Equipment-specific parameters such as vibration, temperature, and power factor are based on simple linear scaling 
    with health, which can exaggerate extreme values; for example, vibration RMS values can reach high levels that are 
    uncommon for extended periods without maintenance. Wear rates are modeled purely as a function of health, ignoring 
    critical factors like ore abrasiveness, feed size, and operational conditions. 
    Remaining Useful Life (RUL) is estimated from health and wear in a simplified formula, 
    whereas real-world RUL predictions rely on historical failure data, vibration trends, lubricant analysis, and 
    history. Finally, timestamps are randomly assigned, producing independent data points rather than time-correlated 
    trends, which reduces the dataset’s fidelity for predictive maintenance or time-series modeling, as it fails to 
    capture gradual degradation over time.
    """


    def generate_energy_data(self, crushing_data, separation_data, n_samples=10000):
        """Generate energy consumption dataset"""
        print("Generating Energy Consumption Dataset...")

        # Base energy consumption patterns
        timestamps = pd.date_range('2020-01-01', periods=n_samples, freq='H')

        # Daily and seasonal patterns
        hour_of_day = timestamps.hour
        day_of_year = timestamps.dayofyear

        # Base load (always present)
        base_load = 200 + 50 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation

        # Crushing energy (sample from crushing data)
        crushing_sample_idx = np.random.choice(len(crushing_data), n_samples, replace=True)
        crushing_power = crushing_data.iloc[crushing_sample_idx]['power_draw_kw'].values

        # Processing energy (from separation circuits)
        sep_sample_idx = np.random.choice(len(separation_data), n_samples, replace=True)

        # Spiral energy (proportional to speed and throughput)
        spiral_power = 15 * separation_data.iloc[sep_sample_idx]['spiral_speed_rpm'].values / 200

        # Magnetic separator energy
        mag_power = 25 * separation_data.iloc[sep_sample_idx]['magnetic_intensity_t'].values

        # Pumping energy (varies with throughput)
        pump_power = np.random.uniform(80, 150, n_samples)

        # Conveyor energy
        conveyor_power = np.random.uniform(25, 45, n_samples)

        # Total plant power
        total_power = (base_load + crushing_power + spiral_power +
                       mag_power + pump_power + conveyor_power)

        # Add operational variations (night shifts, maintenance)
        operational_factor = np.where((hour_of_day >= 6) & (hour_of_day <= 18),
                                      1.0, 0.7)  # Reduced night operation
        total_power *= operational_factor

        # Add random maintenance shutdowns (5% probability)
        maintenance_mask = np.random.random(n_samples) < 0.05
        total_power = np.where(maintenance_mask, total_power * 0.1, total_power)

        # Energy costs (varies by time of day)
        energy_cost_per_kwh = 0.08 + 0.02 * np.sin(2 * np.pi * hour_of_day / 24)

        energy_data = pd.DataFrame({
            'timestamp': timestamps,
            'total_power_kw': np.round(total_power, 0),
            'crushing_power_kw': np.round(crushing_power, 0),
            'separation_power_kw': np.round(spiral_power + mag_power, 0),
            'auxiliary_power_kw': np.round(pump_power + conveyor_power, 0),
            'base_load_kw': np.round(base_load, 0),
            'energy_cost_kwh': np.round(energy_cost_per_kwh, 4),
            'operational_factor': np.round(operational_factor, 2),
            'maintenance_mode': maintenance_mask
        })

        print(f"Generated {len(energy_data)} energy consumption records")
        return energy_data

    def generate_complete_dataset(self):
        """Generate complete integrated dataset for manganese processing plant"""
        print(" MANGANESE PROCESSING PLANT DATA GENERATION")
        print("=" * 60)

        # Generate individual datasets
        ore_data = self.generate_ore_feed_data(10000)
        blended_ore = self.blend_ores(ore_data, high_grade_cutoff=60, blend_ratio=0.3)
        crushing_data = self.generate_crushing_data(blended_ore, 15000)
        separation_data = self.generate_separation_data(blended_ore, 12000)
        equipment_health = self.generate_equipment_health_data(8000)
        energy_data = self.generate_energy_data(crushing_data, separation_data, 10000)

        # Create summary statistics
        print("\n DATASET SUMMARY")
        print("=" * 40)
        print(f"Ore Feed Records: {len(ore_data):,}")
        print(f"Crushing Records: {len(crushing_data):,}")
        print(f"Separation Records: {len(separation_data):,}")
        print(f"Equipment Health Records: {len(equipment_health):,}")
        print(f"Energy Records: {len(energy_data):,}")
        print(
            f"Total Records: {sum([len(df) for df in [ore_data, crushing_data, separation_data, equipment_health, energy_data]]):,}")

        return {
            'ore_feed': ore_data,
            'blended_ore_feed': blended_ore,
            'crushing_circuit': crushing_data,
            'separation_circuit': separation_data,
            'equipment_health': equipment_health,
            'energy_consumption': energy_data
        }

    def save_datasets(self, datasets, output_dir='./synthetic/'):
        """Save all datasets to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n Saving datasets to {output_dir}")

        for name, df in datasets.items():
            filename = f"{output_dir}manganese_{name}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {filename} ({len(df):,} records)")

        print("\nAll datasets generated and saved successfully!")
        return True

# Example usage and testing
if __name__ == "__main__":
    print(" Starting Manganese Processing Data Generation...")

    # Initialize generator
    generator = ManganeseDataGenerator(random_state=42)

    # Generate all datasets
    datasets = generator.generate_complete_dataset()

    # Save datasets
    generator.save_datasets(datasets)

    # Display sample data
    print("\n SAMPLE DATA PREVIEW")
    print("=" * 40)

    for name, df in datasets.items():
        print(f"\n{name.upper()} Dataset (first 3 rows):")
        print(df.head(3))
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

    print("\n Data generation complete! Ready for ML development.")






















