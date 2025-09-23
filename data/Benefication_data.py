"""
Enhanced Manganese Processing Plant - Additional Beneficiation Modules
Adds froth flotation, dense media separation, jigging, and dewatering circuits

AUTHOR: DARLENE WENDY NASIMIYU
Purpose: Complete the manganese processing circuit with industry-standard beneficiation processes
"""

import pandas as pd
import numpy as np
import datetime
import warnings

warnings.filterwarnings('ignore')


class EnhancedManganeseModules:
    """Additional beneficiation modules to complement the base generator"""

    def __init__(self, random_state=42):
        np.random.seed(random_state)

        # Flotation circuit parameters
        self.flotation_params = {
            'collector_dosage_range': (80, 200),  # g/t potassium amyl xanthate
            'frother_dosage_range': (15, 35),  # g/t MIBC
            'ph_range': (8.5, 10.5),  # pH for manganese flotation
            'pulp_density_range': (25, 35),  # % solids
            'air_flow_range': (8, 15),  # m3/min per m3 cell volume
            'residence_time_range': (8, 16),  # minutes
            'cell_number': 6  # rougher-cleaner configuration
        }

        # Dense Media Separation parameters
        self.dms_params = {
            'media_density_range': (2.8, 3.2),  # sg using ferrosilicon
            'cyclone_pressure_range': (80, 120),  # kPa
            'feed_size_range': (6, 50),  # mm (coarse fraction)
            'separation_efficiency_base': 0.88,  # base efficiency
            'media_consumption_range': (0.5, 2.0)  # kg/t ore
        }

        # Jigging parameters
        self.jigging_params = {
            'stroke_length_range': (15, 25),  # mm
            'stroke_frequency_range': (150, 250),  # strokes per minute
            'water_flow_range': (2.0, 4.0),  # m3/h per m2
            'bed_height_range': (150, 300),  # mm
            'hutch_water_range': (1.0, 2.5)  # m3/h
        }

        # Dewatering parameters
        self.dewatering_params = {
            'thickener_underflow_range': (55, 70),  # % solids
            'filter_cake_moisture_range': (8, 12),  # % moisture
            'flocculant_dosage_range': (20, 80),  # g/t
            'retention_time_range': (2, 6)  # hours in thickener
        }

    def generate_flotation_data(self, separation_data, n_samples=12000):
        """Generate froth flotation circuit data"""
        print("Generating Froth Flotation Circuit Dataset...")

        # Sample from separation data to get feed characteristics
        sep_sample_idx = np.random.choice(len(separation_data), n_samples, replace=True)
        base_feed = separation_data.iloc[sep_sample_idx].reset_index(drop=True)

        # Flotation reagent dosages
        collector_dosage = np.random.uniform(*self.flotation_params['collector_dosage_range'], n_samples)
        frother_dosage = np.random.uniform(*self.flotation_params['frother_dosage_range'], n_samples)

        # pH control (critical for manganese flotation)
        ph_value = np.random.uniform(*self.flotation_params['ph_range'], n_samples)

        # Pulp density
        pulp_density = np.random.uniform(*self.flotation_params['pulp_density_range'], n_samples)

        # Air flow rate
        air_flow = np.random.uniform(*self.flotation_params['air_flow_range'], n_samples)

        # Residence time
        residence_time = np.random.uniform(*self.flotation_params['residence_time_range'], n_samples)

        # Calculate flotation performance based on ore type and conditions
        feed_grade = base_feed['final_concentrate_grade_pct']
        ore_type = base_feed['ore_type']

        # Flotation efficiency (varies by ore type)
        base_efficiency = np.where(ore_type == 'oxide', 0.65,  # Oxides harder to float
                                   np.where(ore_type == 'carbonate', 0.78,  # Carbonates good
                                            0.85))  # Silicates excellent

        # pH optimization effect
        ph_factor = 1.0 + 0.1 * np.sin(2 * np.pi * (ph_value - 9.0) / 2.0)  # Optimal around pH 9

        # Collector dosage effect
        collector_factor = 0.7 + 0.3 * (collector_dosage - 80) / 120  # Diminishing returns
        collector_factor = np.clip(collector_factor, 0.7, 1.0)

        # Calculate flotation recovery
        flotation_recovery = base_efficiency * ph_factor * collector_factor
        flotation_recovery += np.random.normal(0, 0.05, n_samples)
        flotation_recovery = np.clip(flotation_recovery, 0.45, 0.92)

        # Concentrate grade improvement
        flotation_concentrate_grade = feed_grade * (1.1 + 0.2 * flotation_recovery)
        flotation_concentrate_grade = np.clip(flotation_concentrate_grade, feed_grade, 52)

        # Tailings grade
        flotation_tailings_grade = feed_grade * (1 - flotation_recovery) * 0.3

        # Froth characteristics
        froth_stability = 0.6 + 0.3 * (frother_dosage - 15) / 20 + np.random.normal(0, 0.1, n_samples)
        froth_stability = np.clip(froth_stability, 0.3, 0.95)

        froth_grade = flotation_concentrate_grade * (0.9 + 0.1 * froth_stability)

        # Create timestamps
        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 3)
                      for i in range(n_samples)]

        flotation_data = pd.DataFrame({
            'timestamp': timestamps,
            'feed_grade_pct': np.round(feed_grade, 2),
            'collector_dosage_gt': np.round(collector_dosage, 1),
            'frother_dosage_gt': np.round(frother_dosage, 1),
            'ph_value': np.round(ph_value, 2),
            'pulp_density_pct_solids': np.round(pulp_density, 1),
            'air_flow_m3_min': np.round(air_flow, 1),
            'residence_time_min': np.round(residence_time, 1),
            'flotation_recovery': np.round(flotation_recovery, 3),
            'concentrate_grade_pct': np.round(flotation_concentrate_grade, 2),
            'tailings_grade_pct': np.round(flotation_tailings_grade, 3),
            'froth_stability_index': np.round(froth_stability, 2),
            'froth_grade_pct': np.round(froth_grade, 2),
            'ore_type': ore_type
        })

        print(f"Generated {len(flotation_data)} flotation records")
        return flotation_data

    def generate_dms_data(self, ore_data, n_samples=8000):
        """Generate Dense Media Separation data"""
        print("Generating Dense Media Separation Dataset...")

        # Sample from ore data for DMS feed (coarser material)
        ore_sample_idx = np.random.choice(len(ore_data), n_samples, replace=True)
        base_ore = ore_data.iloc[ore_sample_idx].reset_index(drop=True)

        # Filter for coarse material suitable for DMS
        coarse_mask = base_ore['p80_mm'] >= 10  # DMS typically for +10mm

        # DMS operating parameters
        media_density = np.random.uniform(*self.dms_params['media_density_range'], n_samples)
        cyclone_pressure = np.random.uniform(*self.dms_params['cyclone_pressure_range'], n_samples)
        feed_size = base_ore['p80_mm']
        media_consumption = np.random.uniform(*self.dms_params['media_consumption_range'], n_samples)

        # DMS separation efficiency
        base_efficiency = self.dms_params['separation_efficiency_base']

        # Separation based on density difference
        ore_density = base_ore['specific_gravity']
        density_difference = abs(ore_density - media_density)

        # Better separation with larger density difference
        density_factor = 1.0 - 0.3 * np.exp(-2 * density_difference)

        # Size factor (better separation for coarser particles)
        size_factor = np.clip(feed_size / 25, 0.8, 1.2)

        dms_efficiency = base_efficiency * density_factor * size_factor
        dms_efficiency += np.random.normal(0, 0.08, n_samples)
        dms_efficiency = np.clip(dms_efficiency, 0.6, 0.96)

        # Sink product (high density - manganese rich)
        sink_grade = base_ore['mn_grade_pct'] * (1.2 + 0.3 * dms_efficiency)
        sink_grade = np.clip(sink_grade, base_ore['mn_grade_pct'], 50)

        # Float product (low density - gangue rich)
        float_grade = base_ore['mn_grade_pct'] * (1 - dms_efficiency) * 0.4

        # Yield to sink
        sink_yield = 0.3 + 0.4 * (base_ore['mn_grade_pct'] / 50)
        sink_yield = np.clip(sink_yield, 0.2, 0.8)

        # Recovery calculation
        dms_recovery = (sink_grade * sink_yield) / base_ore['mn_grade_pct']
        dms_recovery = np.clip(dms_recovery, 0.5, 0.9)

        # Media circuit parameters
        media_recovery = np.random.uniform(0.98, 0.995, n_samples)  # % media recovered

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 4)
                      for i in range(n_samples)]

        dms_data = pd.DataFrame({
            'timestamp': timestamps,
            'feed_grade_pct': np.round(base_ore['mn_grade_pct'], 2),
            'feed_size_mm': np.round(feed_size, 1),
            'media_density_sg': np.round(media_density, 2),
            'cyclone_pressure_kpa': np.round(cyclone_pressure, 0),
            'media_consumption_kg_t': np.round(media_consumption, 2),
            'media_recovery_pct': np.round(media_recovery * 100, 2),
            'sink_grade_pct': np.round(sink_grade, 2),
            'float_grade_pct': np.round(float_grade, 3),
            'sink_yield_pct': np.round(sink_yield * 100, 1),
            'dms_recovery': np.round(dms_recovery, 3),
            'separation_efficiency': np.round(dms_efficiency, 3),
            'ore_density_sg': np.round(ore_density, 2)
        })

        print(f"Generated {len(dms_data)} DMS records")
        return dms_data

    def generate_jigging_data(self, ore_data, n_samples=10000):
        """Generate jigging circuit data"""
        print("Generating Jigging Circuit Dataset...")

        ore_sample_idx = np.random.choice(len(ore_data), n_samples, replace=True)
        base_ore = ore_data.iloc[ore_sample_idx].reset_index(drop=True)

        # Jigging operating parameters
        stroke_length = np.random.uniform(*self.jigging_params['stroke_length_range'], n_samples)
        stroke_frequency = np.random.uniform(*self.jigging_params['stroke_frequency_range'], n_samples)
        water_flow = np.random.uniform(*self.jigging_params['water_flow_range'], n_samples)
        bed_height = np.random.uniform(*self.jigging_params['bed_height_range'], n_samples)
        hutch_water = np.random.uniform(*self.jigging_params['hutch_water_range'], n_samples)

        # Jigging efficiency based on particle size and density
        size_factor = np.clip(base_ore['p80_mm'] / 20, 0.7, 1.3)  # Optimal around 20mm
        density_factor = (base_ore['specific_gravity'] - 2.5) / 1.5  # Better for higher density

        # Stroke optimization
        stroke_work = stroke_length * stroke_frequency / 1000  # Work index
        stroke_factor = 1.0 - 0.2 * abs(stroke_work - 4) / 4  # Optimal around 4

        jigging_efficiency = 0.72 * size_factor * density_factor * stroke_factor
        jigging_efficiency += np.random.normal(0, 0.08, n_samples)
        jigging_efficiency = np.clip(jigging_efficiency, 0.45, 0.88)

        # Concentrate and tailings
        jig_concentrate_grade = base_ore['mn_grade_pct'] * (1.15 + 0.25 * jigging_efficiency)
        jig_concentrate_grade = np.clip(jig_concentrate_grade, base_ore['mn_grade_pct'], 48)

        jig_tailings_grade = base_ore['mn_grade_pct'] * (1 - jigging_efficiency) * 0.35

        # Recovery
        jig_recovery = jigging_efficiency * 0.82 + np.random.normal(0, 0.05, n_samples)
        jig_recovery = np.clip(jig_recovery, 0.4, 0.85)

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 2.5)
                      for i in range(n_samples)]

        jigging_data = pd.DataFrame({
            'timestamp': timestamps,
            'feed_grade_pct': np.round(base_ore['mn_grade_pct'], 2),
            'stroke_length_mm': np.round(stroke_length, 1),
            'stroke_frequency_spm': np.round(stroke_frequency, 0),
            'water_flow_m3h_m2': np.round(water_flow, 2),
            'bed_height_mm': np.round(bed_height, 0),
            'hutch_water_m3h': np.round(hutch_water, 2),
            'concentrate_grade_pct': np.round(jig_concentrate_grade, 2),
            'tailings_grade_pct': np.round(jig_tailings_grade, 3),
            'jig_recovery': np.round(jig_recovery, 3),
            'separation_efficiency': np.round(jigging_efficiency, 3),
            'feed_size_mm': np.round(base_ore['p80_mm'], 1),
            'ore_type': base_ore['ore_type']
        })

        print(f"Generated {len(jigging_data)} jigging records")
        return jigging_data

    def generate_dewatering_data(self, flotation_data, dms_data, n_samples=8000):
        """Generate dewatering circuit data"""
        print("Generating Dewatering Circuit Dataset...")

        # Combine concentrates from flotation and DMS for dewatering
        all_concentrates = []

        # Sample from flotation concentrates
        if len(flotation_data) > 0:
            flot_sample = flotation_data.sample(n=min(n_samples // 2, len(flotation_data)), replace=True)
            flot_sample['source_circuit'] = 'flotation'
            flot_sample['feed_grade_dewater'] = flot_sample['concentrate_grade_pct']
            all_concentrates.append(flot_sample[['timestamp', 'source_circuit', 'feed_grade_dewater']])

        # Sample from DMS concentrates
        if len(dms_data) > 0:
            dms_sample = dms_data.sample(n=min(n_samples // 2, len(dms_data)), replace=True)
            dms_sample['source_circuit'] = 'dms'
            dms_sample['feed_grade_dewater'] = dms_sample['sink_grade_pct']
            all_concentrates.append(dms_sample[['timestamp', 'source_circuit', 'feed_grade_dewater']])

        if not all_concentrates:
            # Generate synthetic if no input data
            timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 4)
                          for i in range(n_samples)]
            base_data = pd.DataFrame({
                'timestamp': timestamps,
                'source_circuit': np.random.choice(['flotation', 'dms'], n_samples),
                'feed_grade_dewater': np.random.uniform(42, 50, n_samples)
            })
        else:
            base_data = pd.concat(all_concentrates, ignore_index=True)
            if len(base_data) < n_samples:
                base_data = base_data.sample(n=n_samples, replace=True, ignore_index=True)

        # Thickening parameters
        feed_solids = np.random.uniform(15, 25, n_samples)  # % solids in feed
        flocculant_dosage = np.random.uniform(*self.dewatering_params['flocculant_dosage_range'], n_samples)
        retention_time = np.random.uniform(*self.dewatering_params['retention_time_range'], n_samples)

        # Thickener performance
        underflow_solids = np.random.uniform(*self.dewatering_params['thickener_underflow_range'], n_samples)
        overflow_clarity = np.random.uniform(10, 50, n_samples)  # NTU

        # Thickening efficiency
        thickening_efficiency = (underflow_solids - feed_solids) / (70 - feed_solids)
        thickening_efficiency = np.clip(thickening_efficiency, 0.6, 0.95)

        # Filtration parameters
        filter_pressure = np.random.uniform(200, 400, n_samples)  # kPa
        filter_cycle_time = np.random.uniform(45, 90, n_samples)  # minutes

        # Final cake moisture
        cake_moisture = np.random.uniform(*self.dewatering_params['filter_cake_moisture_range'], n_samples)

        # Cake moisture influenced by pressure and grade
        pressure_factor = (400 - filter_pressure) / 200 * 0.2  # Higher pressure = lower moisture
        cake_moisture = cake_moisture + pressure_factor
        cake_moisture = np.clip(cake_moisture, 6, 15)

        # Water recovery
        water_recovery = np.random.uniform(0.85, 0.95, n_samples)

        # Solid recovery in dewatering
        solid_recovery = np.random.uniform(0.98, 0.999, n_samples)

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 4)
                      for i in range(n_samples)]

        dewatering_data = pd.DataFrame({
            'timestamp': timestamps[:n_samples],
            'source_circuit': base_data['source_circuit'].iloc[:n_samples],
            'feed_grade_pct': np.round(base_data['feed_grade_dewater'].iloc[:n_samples], 2),
            'feed_solids_pct': np.round(feed_solids, 1),
            'flocculant_dosage_gt': np.round(flocculant_dosage, 1),
            'retention_time_hr': np.round(retention_time, 1),
            'underflow_solids_pct': np.round(underflow_solids, 1),
            'overflow_clarity_ntu': np.round(overflow_clarity, 0),
            'thickening_efficiency': np.round(thickening_efficiency, 3),
            'filter_pressure_kpa': np.round(filter_pressure, 0),
            'cycle_time_min': np.round(filter_cycle_time, 0),
            'cake_moisture_pct': np.round(cake_moisture, 1),
            'water_recovery_pct': np.round(water_recovery * 100, 1),
            'solid_recovery_pct': np.round(solid_recovery * 100, 2)
        })

        print(f"Generated {len(dewatering_data)} dewatering records")
        return dewatering_data

    def generate_complete_enhanced_datasets(self, base_datasets):
        """Generate all enhanced beneficiation datasets"""
        print("\nENHANCED MANGANESE BENEFICIATION MODULES")
        print("=" * 60)

        # Extract base datasets
        ore_data = base_datasets.get('ore_feed', pd.DataFrame())
        separation_data = base_datasets.get('separation_circuit', pd.DataFrame())

        # Generate enhanced datasets
        flotation_data = self.generate_flotation_data(separation_data, 12000)
        dms_data = self.generate_dms_data(ore_data, 8000)
        jigging_data = self.generate_jigging_data(ore_data, 10000)
        dewatering_data = self.generate_dewatering_data(flotation_data, dms_data, 8000)

        enhanced_datasets = {
            'flotation_circuit': flotation_data,
            'dms_circuit': dms_data,
            'jigging_circuit': jigging_data,
            'dewatering_circuit': dewatering_data
        }

        print(f"\nENHANCED MODULES SUMMARY")
        print("=" * 40)
        for name, df in enhanced_datasets.items():
            print(f"{name.replace('_', ' ').title()}: {len(df):,} records")

        return enhanced_datasets

    def save_enhanced_datasets(self, datasets, output_dir='./synthetic/'):
        """Save enhanced datasets to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print(f"\nSaving enhanced datasets to {output_dir}")

        for name, df in datasets.items():
            filename = f"{output_dir}manganese_{name}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {filename} ({len(df):,} records)")

        return True


# Main execution - Generate beneficiation datasets independently
if __name__ == "__main__":
    print("ENHANCED MANGANESE BENEFICIATION DATA GENERATION")
    print("=" * 60)

    # Initialize the enhanced modules generator
    enhanced_generator = EnhancedManganeseModules(random_state=42)

    # Create synthetic base data for beneficiation circuits
    # (Since we need some feed characteristics for the circuits)
    print("Creating synthetic feed data for beneficiation circuits...")

    # Minimal ore characteristics for beneficiation
    n_base = 5000
    synthetic_ore = pd.DataFrame({
        'mn_grade_pct': np.random.uniform(35, 50, n_base),
        'p80_mm': np.random.uniform(8, 25, n_base),
        'specific_gravity': np.random.uniform(3.8, 4.2, n_base),
        'ore_type': np.random.choice(['oxide', 'carbonate', 'silicate'], n_base, p=[0.6, 0.3, 0.1])
    })

    # Minimal separation data for flotation feed
    synthetic_separation = pd.DataFrame({
        'final_concentrate_grade_pct': np.random.uniform(42, 48, n_base),
        'ore_type': np.random.choice(['oxide', 'carbonate', 'silicate'], n_base, p=[0.6, 0.3, 0.1])
    })

    # Generate all beneficiation datasets
    flotation_data = enhanced_generator.generate_flotation_data(synthetic_separation, 12000)
    dms_data = enhanced_generator.generate_dms_data(synthetic_ore, 8000)
    jigging_data = enhanced_generator.generate_jigging_data(synthetic_ore, 10000)
    dewatering_data = enhanced_generator.generate_dewatering_data(flotation_data, dms_data, 8000)

    # Compile beneficiation datasets
    beneficiation_datasets = {
        'flotation_circuit': flotation_data,
        'dms_circuit': dms_data,
        'jigging_circuit': jigging_data,
        'dewatering_circuit': dewatering_data
    }

    # Save all beneficiation datasets
    enhanced_generator.save_enhanced_datasets(beneficiation_datasets)

    # Display summary
    print(f"\nBENEFICIATION DATASETS SUMMARY")
    print("=" * 50)

    total_records = 0
    for name, df in beneficiation_datasets.items():
        records = len(df)
        total_records += records
        print(f"{name.replace('_', ' ').title()}: {records:,} records")

        # Show sample columns
        print(f"  Key columns: {', '.join(df.columns[:5])}...")
        print()

    print(f"Total Beneficiation Records: {total_records:,}")
    print(f"Datasets saved to: ./synthetic/")

    # Display sample data
    print(f"\nSAMPLE DATA PREVIEW")
    print("=" * 40)

    for name, df in beneficiation_datasets.items():
        print(f"\n{name.upper()} (first 2 rows):")
        print(df.head(2))
        print(f"Shape: {df.shape}")

    print(f"\nBeneficiation data generation complete! Ready for ML development.")