"""
Manganese processing Plant synthetic data generator.
This script generates realistic yet synthetic datasets for Machine Learning model development

AUTHOR: DARLENE WENDY NASIMIYU
Purpose: Create comprehensive datasets for manganese processing plant optimization

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
            'mn_grade_mean': 40.0,  # Avg manganese grade
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
        mn_grades = np.clip(mn_grades, 15, 52)

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
        """Generate equipment health monitoring data"""
        print(" Generating Equipment Health Dataset...")

        # Equipment types
        equipment_types = ['crusher', 'pump', 'spiral', 'magnetic_sep', 'conveyor']
        equipment_ids = [f"{eq_type}_{i:02d}" for eq_type in equipment_types for i in range(1, 6)]

        health_data = []

        for i in range(n_samples):
            equipment_id = np.random.choice(equipment_ids)
            equipment_type = equipment_id.split('_')[0]

            # Operating hours (affects health)
            operating_hours = np.random.uniform(0, 8760 * 5, 1)[0]  # Up to 5 years

            # Base health score (decreases with age)
            base_health = 100 * (1 - operating_hours / (8760 * 10))  # 10-year life
            base_health += np.random.normal(0, 10)
            base_health = np.clip(base_health, 20, 100)

            # Equipment-specific parameters
            if equipment_type == 'crusher':
                vibration = 2 + (100 - base_health) * 0.1 + np.random.normal(0, 0.5)
                temperature = 60 + (100 - base_health) * 0.3 + np.random.normal(0, 5)
                power_factor = 0.85 - (100 - base_health) * 0.002

            elif equipment_type == 'pump':
                vibration = 1.5 + (100 - base_health) * 0.08 + np.random.normal(0, 0.3)
                temperature = 70 + (100 - base_health) * 0.4 + np.random.normal(0, 8)
                power_factor = 0.90 - (100 - base_health) * 0.0015

            else:  # Other equipment
                vibration = 1.0 + (100 - base_health) * 0.05 + np.random.normal(0, 0.2)
                temperature = 45 + (100 - base_health) * 0.2 + np.random.normal(0, 3)
                power_factor = 0.88 - (100 - base_health) * 0.001

            vibration = np.clip(vibration, 0.5, 15)
            temperature = np.clip(temperature, 25, 120)
            power_factor = np.clip(power_factor, 0.6, 0.95)

            # Failure probability (increases with poor health)
            failure_prob = 1 - (base_health / 100) ** 2
            failure_prob = np.clip(failure_prob, 0, 0.8)

            # Remaining useful life (days)
            rul_days = (base_health / 100) * 1825 + np.random.normal(0, 100)  # Up to 5 years
            rul_days = np.clip(rul_days, 1, 1825)

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
                'failure_probability': np.round(failure_prob, 4),
                'rul_days': np.round(rul_days, 0)
            })

        equipment_health = pd.DataFrame(health_data)
        print(f" Generated {len(equipment_health)} equipment health records")
        return equipment_health

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
        crushing_data = self.generate_crushing_data(ore_data, 15000)
        separation_data = self.generate_separation_data(ore_data, 12000)
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






















