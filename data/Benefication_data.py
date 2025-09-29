"""
Enhanced Manganese Processing Plant - Equipment-Linked Beneficiation Modules
Links beneficiation performance to actual equipment health for realistic ML modeling

AUTHOR: DARLENE WENDY NASIMIYU
Purpose: Generate beneficiation data with equipment performance correlations
"""

import pandas as pd
import numpy as np
import datetime
import warnings

warnings.filterwarnings('ignore')


class EnhancedManganeseModules:
    """Additional beneficiation modules with equipment health correlation"""

    def __init__(self, random_state=42):
        np.random.seed(random_state)

        # Equipment IDs (matching the enhanced equipment health dataset)
        self.equipment_ids = {
            'flotation_cells_rougher': ['flotation_cell_rougher_01', 'flotation_cell_rougher_02',
                                        'flotation_cell_rougher_03', 'flotation_cell_rougher_04',
                                        'flotation_cell_rougher_05', 'flotation_cell_rougher_06'],
            'flotation_cells_cleaner': ['flotation_cell_cleaner_01', 'flotation_cell_cleaner_02',
                                        'flotation_cell_cleaner_03', 'flotation_cell_cleaner_04'],
            'flotation_cells_scavenger': ['flotation_cell_scavenger_01', 'flotation_cell_scavenger_02',
                                          'flotation_cell_scavenger_03'],
            'air_blowers': ['air_blower_01', 'air_blower_02', 'air_blower_03', 'air_blower_04'],
            'agitators': ['agitator_01', 'agitator_02', 'agitator_03', 'agitator_04', 'agitator_05'],
            'reagent_pumps': ['reagent_dosing_pump_01', 'reagent_dosing_pump_02', 'reagent_dosing_pump_03',
                              'reagent_dosing_pump_04', 'reagent_dosing_pump_05', 'reagent_dosing_pump_06'],
            'dms_cyclones': ['dms_cyclone_01', 'dms_cyclone_02', 'dms_cyclone_03'],
            'jigs': ['jig_01', 'jig_02', 'jig_03', 'jig_04'],
            'thickeners': ['thickener_01', 'thickener_02'],
            'filters': ['vacuum_filter_01', 'vacuum_filter_02', 'vacuum_filter_03',
                        'filter_press_01', 'filter_press_02']
        }

        # Flotation circuit parameters
        self.flotation_params = {
            'collector_dosage_range': (80, 200),
            'frother_dosage_range': (15, 35),
            'ph_range': (8.5, 10.5),
            'pulp_density_range': (25, 35),
            'air_flow_range': (8, 15),
            'residence_time_range': (8, 16),
        }

        # Dense Media Separation parameters
        self.dms_params = {
            'media_density_range': (2.8, 3.2),
            'cyclone_pressure_range': (80, 120),
            'feed_size_range': (6, 50),
            'separation_efficiency_base': 0.88,
            'media_consumption_range': (0.5, 2.0)
        }

        # Jigging parameters
        self.jigging_params = {
            'stroke_length_range': (15, 25),
            'stroke_frequency_range': (150, 250),
            'water_flow_range': (2.0, 4.0),
            'bed_height_range': (150, 300),
            'hutch_water_range': (1.0, 2.5)
        }

        # Dewatering parameters
        self.dewatering_params = {
            'thickener_underflow_range': (55, 70),
            'filter_cake_moisture_range': (8, 12),
            'flocculant_dosage_range': (20, 80),
            'retention_time_range': (2, 6)
        }

    def generate_equipment_health_sample(self, equipment_type, n_samples):
        """Generate realistic equipment health values for correlation"""
        health_scores = np.random.uniform(50, 100, n_samples)
        wear_rates = 100 - health_scores + np.random.normal(0, 10, n_samples)
        wear_rates = np.clip(wear_rates, 0, 100)

        return health_scores, wear_rates

    def generate_flotation_data(self, separation_data, n_samples=12000):
        """Generate froth flotation circuit data with equipment linkage"""
        print("Generating Froth Flotation Circuit Dataset...")

        sep_sample_idx = np.random.choice(len(separation_data), n_samples, replace=True)
        base_feed = separation_data.iloc[sep_sample_idx].reset_index(drop=True)

        # Assign equipment IDs
        flotation_cell_ids = np.random.choice(self.equipment_ids['flotation_cells_rougher'], n_samples)
        air_blower_ids = np.random.choice(self.equipment_ids['air_blowers'], n_samples)
        agitator_ids = np.random.choice(self.equipment_ids['agitators'], n_samples)
        reagent_pump_ids = np.random.choice(self.equipment_ids['reagent_pumps'], n_samples)

        # Generate equipment health for correlation
        cell_health, cell_wear = self.generate_equipment_health_sample('flotation_cell', n_samples)
        blower_health, blower_wear = self.generate_equipment_health_sample('blower', n_samples)
        agitator_health, agitator_wear = self.generate_equipment_health_sample('agitator', n_samples)
        pump_health, pump_wear = self.generate_equipment_health_sample('pump', n_samples)

        # Operating parameters
        collector_dosage = np.random.uniform(*self.flotation_params['collector_dosage_range'], n_samples)
        frother_dosage = np.random.uniform(*self.flotation_params['frother_dosage_range'], n_samples)
        ph_value = np.random.uniform(*self.flotation_params['ph_range'], n_samples)
        pulp_density = np.random.uniform(*self.flotation_params['pulp_density_range'], n_samples)
        air_flow = np.random.uniform(*self.flotation_params['air_flow_range'], n_samples)
        residence_time = np.random.uniform(*self.flotation_params['residence_time_range'], n_samples)

        feed_grade = base_feed['final_concentrate_grade_pct']
        ore_type = base_feed['ore_type']

        # Base efficiency by ore type
        base_efficiency = np.where(ore_type == 'oxide', 0.65,
                                   np.where(ore_type == 'carbonate', 0.78, 0.85))

        # Equipment health impact on performance
        cell_efficiency_factor = 0.7 + 0.3 * (cell_health / 100)  # 70-100% of design
        blower_efficiency_factor = 0.8 + 0.2 * (blower_health / 100)  # Air flow efficiency
        agitator_efficiency_factor = 0.85 + 0.15 * (agitator_health / 100)  # Mixing efficiency

        # Reagent dosing accuracy affected by pump health
        dosing_accuracy = 0.9 + 0.1 * (pump_health / 100)
        effective_collector = collector_dosage * dosing_accuracy
        effective_frother = frother_dosage * dosing_accuracy

        # pH optimization effect
        ph_factor = 1.0 + 0.1 * np.sin(2 * np.pi * (ph_value - 9.0) / 2.0)

        # Collector dosage effect with equipment consideration
        collector_factor = 0.7 + 0.3 * (effective_collector - 80) / 120
        collector_factor = np.clip(collector_factor, 0.7, 1.0)

        # Calculate flotation recovery with equipment degradation
        flotation_recovery = (base_efficiency * ph_factor * collector_factor *
                              cell_efficiency_factor * blower_efficiency_factor *
                              agitator_efficiency_factor)
        flotation_recovery += np.random.normal(0, 0.05, n_samples)
        flotation_recovery = np.clip(flotation_recovery, 0.45, 0.92)

        # Concentrate grade improvement
        flotation_concentrate_grade = feed_grade * (1.1 + 0.2 * flotation_recovery)
        flotation_concentrate_grade = np.clip(flotation_concentrate_grade, feed_grade, 52)

        # Tailings grade
        flotation_tailings_grade = feed_grade * (1 - flotation_recovery) * 0.3

        # Froth characteristics influenced by frother dosing and cell condition
        froth_stability = (0.6 + 0.3 * (effective_frother - 15) / 20 +
                           0.1 * (cell_health / 100))
        froth_stability += np.random.normal(0, 0.1, n_samples)
        froth_stability = np.clip(froth_stability, 0.3, 0.95)

        froth_grade = flotation_concentrate_grade * (0.9 + 0.1 * froth_stability)

        # Reagent consumption increases with poor equipment health
        actual_collector_consumed = collector_dosage * (1 + 0.2 * (cell_wear / 100))
        actual_frother_consumed = frother_dosage * (1 + 0.15 * (cell_wear / 100))

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 3)
                      for i in range(n_samples)]

        flotation_data = pd.DataFrame({
            'timestamp': timestamps,
            'flotation_cell_id': flotation_cell_ids,
            'air_blower_id': air_blower_ids,
            'agitator_id': agitator_ids,
            'reagent_pump_id': reagent_pump_ids,
            'cell_health_score': np.round(cell_health, 1),
            'blower_health_score': np.round(blower_health, 1),
            'feed_grade_pct': np.round(feed_grade, 2),
            'collector_dosage_gt': np.round(collector_dosage, 1),
            'frother_dosage_gt': np.round(frother_dosage, 1),
            'actual_collector_consumed_gt': np.round(actual_collector_consumed, 1),
            'actual_frother_consumed_gt': np.round(actual_frother_consumed, 1),
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

        print(f"Generated {len(flotation_data)} flotation records with equipment linkage")
        return flotation_data

    def generate_dms_data(self, ore_data, n_samples=8000):
        """Generate Dense Media Separation data with equipment linkage"""
        print("Generating Dense Media Separation Dataset...")

        ore_sample_idx = np.random.choice(len(ore_data), n_samples, replace=True)
        base_ore = ore_data.iloc[ore_sample_idx].reset_index(drop=True)

        # Assign DMS cyclone IDs
        dms_cyclone_ids = np.random.choice(self.equipment_ids['dms_cyclones'], n_samples)

        # Generate equipment health
        cyclone_health, cyclone_wear = self.generate_equipment_health_sample('dms_cyclone', n_samples)

        # DMS operating parameters
        media_density = np.random.uniform(*self.dms_params['media_density_range'], n_samples)
        cyclone_pressure = np.random.uniform(*self.dms_params['cyclone_pressure_range'], n_samples)
        feed_size = base_ore['p80_mm']
        media_consumption = np.random.uniform(*self.dms_params['media_consumption_range'], n_samples)

        # Base separation efficiency
        base_efficiency = self.dms_params['separation_efficiency_base']

        ore_density = base_ore['specific_gravity']
        density_difference = abs(ore_density - media_density)

        density_factor = 1.0 - 0.3 * np.exp(-2 * density_difference)
        size_factor = np.clip(feed_size / 25, 0.8, 1.2)

        # Equipment health impact (cyclone liner wear reduces efficiency)
        equipment_factor = 0.75 + 0.25 * (cyclone_health / 100)

        dms_efficiency = base_efficiency * density_factor * size_factor * equipment_factor
        dms_efficiency += np.random.normal(0, 0.08, n_samples)
        dms_efficiency = np.clip(dms_efficiency, 0.6, 0.96)

        # Wear increases media consumption
        adjusted_media_consumption = media_consumption * (1 + 0.3 * (cyclone_wear / 100))

        # Products
        sink_grade = base_ore['mn_grade_pct'] * (1.2 + 0.3 * dms_efficiency)
        sink_grade = np.clip(sink_grade, base_ore['mn_grade_pct'], 50)

        float_grade = base_ore['mn_grade_pct'] * (1 - dms_efficiency) * 0.4

        sink_yield = 0.3 + 0.4 * (base_ore['mn_grade_pct'] / 50)
        sink_yield = np.clip(sink_yield, 0.2, 0.8)

        dms_recovery = (sink_grade * sink_yield) / base_ore['mn_grade_pct']
        dms_recovery = np.clip(dms_recovery, 0.5, 0.9)

        media_recovery = np.random.uniform(0.98, 0.995, n_samples)

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 4)
                      for i in range(n_samples)]

        dms_data = pd.DataFrame({
            'timestamp': timestamps,
            'dms_cyclone_id': dms_cyclone_ids,
            'cyclone_health_score': np.round(cyclone_health, 1),
            'cyclone_wear_rate_pct': np.round(cyclone_wear, 1),
            'feed_grade_pct': np.round(base_ore['mn_grade_pct'], 2),
            'feed_size_mm': np.round(feed_size, 1),
            'media_density_sg': np.round(media_density, 2),
            'cyclone_pressure_kpa': np.round(cyclone_pressure, 0),
            'media_consumption_kg_t': np.round(adjusted_media_consumption, 2),
            'media_recovery_pct': np.round(media_recovery * 100, 2),
            'sink_grade_pct': np.round(sink_grade, 2),
            'float_grade_pct': np.round(float_grade, 3),
            'sink_yield_pct': np.round(sink_yield * 100, 1),
            'dms_recovery': np.round(dms_recovery, 3),
            'separation_efficiency': np.round(dms_efficiency, 3),
            'ore_density_sg': np.round(ore_density, 2)
        })

        print(f"Generated {len(dms_data)} DMS records with equipment linkage")
        return dms_data

    def generate_jigging_data(self, ore_data, n_samples=10000):
        """Generate jigging circuit data with equipment linkage"""
        print("Generating Jigging Circuit Dataset...")

        ore_sample_idx = np.random.choice(len(ore_data), n_samples, replace=True)
        base_ore = ore_data.iloc[ore_sample_idx].reset_index(drop=True)

        # Assign jig IDs
        jig_ids = np.random.choice(self.equipment_ids['jigs'], n_samples)

        # Generate equipment health
        jig_health, jig_wear = self.generate_equipment_health_sample('jig', n_samples)

        # Jigging operating parameters
        stroke_length = np.random.uniform(*self.jigging_params['stroke_length_range'], n_samples)
        stroke_frequency = np.random.uniform(*self.jigging_params['stroke_frequency_range'], n_samples)
        water_flow = np.random.uniform(*self.jigging_params['water_flow_range'], n_samples)
        bed_height = np.random.uniform(*self.jigging_params['bed_height_range'], n_samples)
        hutch_water = np.random.uniform(*self.jigging_params['hutch_water_range'], n_samples)

        # Process efficiency factors
        size_factor = np.clip(base_ore['p80_mm'] / 20, 0.7, 1.3)
        density_factor = (base_ore['specific_gravity'] - 2.5) / 1.5

        stroke_work = stroke_length * stroke_frequency / 1000
        stroke_factor = 1.0 - 0.2 * abs(stroke_work - 4) / 4

        # Equipment health impact (screen wear reduces stratification)
        equipment_factor = 0.7 + 0.3 * (jig_health / 100)

        jigging_efficiency = (0.72 * size_factor * density_factor *
                              stroke_factor * equipment_factor)
        jigging_efficiency += np.random.normal(0, 0.08, n_samples)
        jigging_efficiency = np.clip(jigging_efficiency, 0.45, 0.88)

        # Products
        jig_concentrate_grade = base_ore['mn_grade_pct'] * (1.15 + 0.25 * jigging_efficiency)
        jig_concentrate_grade = np.clip(jig_concentrate_grade, base_ore['mn_grade_pct'], 48)

        jig_tailings_grade = base_ore['mn_grade_pct'] * (1 - jigging_efficiency) * 0.35

        jig_recovery = jigging_efficiency * 0.82 + np.random.normal(0, 0.05, n_samples)
        jig_recovery = np.clip(jig_recovery, 0.4, 0.85)

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 2.5)
                      for i in range(n_samples)]

        jigging_data = pd.DataFrame({
            'timestamp': timestamps,
            'jig_id': jig_ids,
            'jig_health_score': np.round(jig_health, 1),
            'jig_wear_rate_pct': np.round(jig_wear, 1),
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

        print(f"Generated {len(jigging_data)} jigging records with equipment linkage")
        return jigging_data

    def generate_dewatering_data(self, flotation_data, dms_data, n_samples=8000):
        """Generate dewatering circuit data with equipment linkage"""
        print("Generating Dewatering Circuit Dataset...")

        all_concentrates = []

        if len(flotation_data) > 0:
            flot_sample = flotation_data.sample(n=min(n_samples // 2, len(flotation_data)), replace=True)
            flot_sample['source_circuit'] = 'flotation'
            flot_sample['feed_grade_dewater'] = flot_sample['concentrate_grade_pct']
            all_concentrates.append(flot_sample[['timestamp', 'source_circuit', 'feed_grade_dewater']])

        if len(dms_data) > 0:
            dms_sample = dms_data.sample(n=min(n_samples // 2, len(dms_data)), replace=True)
            dms_sample['source_circuit'] = 'dms'
            dms_sample['feed_grade_dewater'] = dms_sample['sink_grade_pct']
            all_concentrates.append(dms_sample[['timestamp', 'source_circuit', 'feed_grade_dewater']])

        if not all_concentrates:
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

        # Assign equipment IDs
        thickener_ids = np.random.choice(self.equipment_ids['thickeners'], n_samples)
        filter_ids = np.random.choice(self.equipment_ids['filters'], n_samples)

        # Generate equipment health
        thickener_health, thickener_wear = self.generate_equipment_health_sample('thickener', n_samples)
        filter_health, filter_wear = self.generate_equipment_health_sample('filter', n_samples)

        # Operating parameters
        feed_solids = np.random.uniform(15, 25, n_samples)
        flocculant_dosage = np.random.uniform(*self.dewatering_params['flocculant_dosage_range'], n_samples)
        retention_time = np.random.uniform(*self.dewatering_params['retention_time_range'], n_samples)

        # Thickener performance affected by equipment health
        base_underflow_solids = np.random.uniform(*self.dewatering_params['thickener_underflow_range'], n_samples)
        equipment_factor = 0.85 + 0.15 * (thickener_health / 100)
        underflow_solids = base_underflow_solids * equipment_factor
        underflow_solids = np.clip(underflow_solids, 45, 70)

        overflow_clarity = np.random.uniform(10, 50, n_samples) * (1 + 0.5 * (thickener_wear / 100))

        thickening_efficiency = (underflow_solids - feed_solids) / (70 - feed_solids)
        thickening_efficiency = np.clip(thickening_efficiency, 0.6, 0.95)

        # Filtration parameters
        filter_pressure = np.random.uniform(200, 400, n_samples)
        filter_cycle_time = np.random.uniform(45, 90, n_samples)

        # Filter wear increases cycle time
        adjusted_cycle_time = filter_cycle_time * (1 + 0.3 * (filter_wear / 100))

        # Cake moisture affected by filter health
        base_cake_moisture = np.random.uniform(*self.dewatering_params['filter_cake_moisture_range'], n_samples)
        pressure_factor = (400 - filter_pressure) / 200 * 0.2
        health_factor = 0.2 * (1 - filter_health / 100)  # Poor health = higher moisture

        cake_moisture = base_cake_moisture + pressure_factor + health_factor
        cake_moisture = np.clip(cake_moisture, 6, 15)

        water_recovery = np.random.uniform(0.85, 0.95, n_samples) * (thickener_health / 100)
        solid_recovery = np.random.uniform(0.98, 0.999, n_samples) * (filter_health / 100)

        timestamps = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i * 4)
                      for i in range(n_samples)]

        dewatering_data = pd.DataFrame({
            'timestamp': timestamps[:n_samples],
            'thickener_id': thickener_ids,
            'filter_id': filter_ids,
            'thickener_health_score': np.round(thickener_health, 1),
            'filter_health_score': np.round(filter_health, 1),
            'source_circuit': base_data['source_circuit'].iloc[:n_samples],
            'feed_grade_pct': np.round(base_data['feed_grade_dewater'].iloc[:n_samples], 2),
            'feed_solids_pct': np.round(feed_solids, 1),
            'flocculant_dosage_gt': np.round(flocculant_dosage, 1),
            'retention_time_hr': np.round(retention_time, 1),
            'underflow_solids_pct': np.round(underflow_solids, 1),
            'overflow_clarity_ntu': np.round(overflow_clarity, 0),
            'thickening_efficiency': np.round(thickening_efficiency, 3),
            'filter_pressure_kpa': np.round(filter_pressure, 0),
            'cycle_time_min': np.round(adjusted_cycle_time, 0),
            'cake_moisture_pct': np.round(cake_moisture, 1),
            'water_recovery_pct': np.round(water_recovery * 100, 1),
            'solid_recovery_pct': np.round(solid_recovery * 100, 2)
        })

        print(f"Generated {len(dewatering_data)} dewatering records with equipment linkage")
        return dewatering_data

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


# Main execution
if __name__ == "__main__":
    print("ENHANCED MANGANESE BENEFICIATION DATA GENERATION")
    print("With Equipment Health Correlation")
    print("=" * 60)

    enhanced_generator = EnhancedManganeseModules(random_state=42)

    print("Creating synthetic feed data for beneficiation circuits...")

    n_base = 5000
    synthetic_ore = pd.DataFrame({
        'mn_grade_pct': np.random.uniform(35, 50, n_base),
        'p80_mm': np.random.uniform(8, 25, n_base),
        'specific_gravity': np.random.uniform(3.8, 4.2, n_base),
        'ore_type': np.random.choice(['oxide', 'carbonate', 'silicate'], n_base, p=[0.6, 0.3, 0.1])
    })

    synthetic_separation = pd.DataFrame({
        'final_concentrate_grade_pct': np.random.uniform(42, 48, n_base),
        'ore_type': np.random.choice(['oxide', 'carbonate', 'silicate'], n_base, p=[0.6, 0.3, 0.1])
    })

    # Generate all beneficiation datasets with equipment linkage
    flotation_data = enhanced_generator.generate_flotation_data(synthetic_separation, 12000)
    dms_data = enhanced_generator.generate_dms_data(synthetic_ore, 8000)
    jigging_data = enhanced_generator.generate_jigging_data(synthetic_ore, 10000)
    dewatering_data = enhanced_generator.generate_dewatering_data(flotation_data, dms_data, 8000)

    beneficiation_datasets = {
        'flotation_circuit': flotation_data,
        'dms_circuit': dms_data,
        'jigging_circuit': jigging_data,
        'dewatering_circuit': dewatering_data
    }

    enhanced_generator.save_enhanced_datasets(beneficiation_datasets)

    print(f"\nBENEFICIATION DATASETS SUMMARY")
    print("=" * 50)

    total_records = 0
    for name, df in beneficiation_datasets.items():
        records = len(df)
        total_records += records
        print(f"{name.replace('_', ' ').title()}: {records:,} records")
        print(f"  Equipment columns: {[col for col in df.columns if '_id' in col or 'health' in col]}")
        print()

    print(f"Total Beneficiation Records: {total_records:,}")
    print(f"All datasets include equipment health correlation for ML modeling")