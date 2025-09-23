# Intelligent Manganese Processing Plant Optimization

## 🎯 Project Overview

This project develops machine learning models to optimize manganese ore processing operations, focusing on recovery maximization, energy efficiency, and predictive maintenance. The system targets typical manganese processing workflows including crushing, screening, gravity separation, and magnetic separation.

## 📊 Problem Statement

Manganese processing plants face critical challenges:
- **Low Recovery Rates**: Typical manganese recovery rates of 60-75% leave significant value on table
- **High Energy Costs**: Energy represents 40-50% of operating costs
- **Equipment Downtime**: Unplanned maintenance reduces throughput by 15-20%
- **Quality Variability**: Inconsistent concentrate grades affect market pricing

**Target Improvements:**
- 5-8% increase in manganese recovery
- 12-15% reduction in energy consumption per ton
- 25% reduction in unplanned downtime
- Improved concentrate grade consistency (±2% Mn content)

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   ML Pipeline    │    │   Optimization  │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ • Process Data  │───▶│ • Data Ingestion │───▶│ • Recovery Max  │
│ • Equipment     │    │ • Feature Eng    │    │ • Energy Min    │
│ • Lab Results   │    │ • Model Training │    │ • Maintenance   │
│ • Sensors       │    │ • Validation     │    │ • Quality Ctrl  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start (1-Week Implementation)

### Day 1-2: Environment Setup & Data Collection
```bash
git clone git@github.com:Darlene-13/Intelligent-Manganese-Processing-Plant-Optimization.git
cd Intelligent-Manganese-Processing-Plant-Optimization
pip install -r requirements.txt
```

### Day 3-4: Data Analysis & Feature Engineering
```bash
python src/data_preprocessing.py
python src/exploratory_analysis.py
python src/feature_engineering.py
```

### Day 5-6: Model Development
```bash
python src/train_models.py --model recovery_prediction
python src/train_models.py --model energy_optimization
python src/train_models.py --model maintenance_prediction
```

### Day 7: Deployment & Documentation
```bash
python src/deploy_models.py
python src/generate_reports.py
```

## 📁 Project Structure

```
manganese-ml-optimization/
├── README.md
├── requirements.txt
├── config/
│   ├── model_config.yaml
│   ├── data_config.yaml
│   └── processing_parameters.yaml
├── data/
│   ├── raw/
│   │   ├── process_data/
│   │   ├── equipment_data/
│   │   ├── lab_results/
│   │   └── synthetic/
│   ├── processed/
│   └── external/
├── src/
│   ├── data_preprocessing.py
│   ├── exploratory_analysis.py
│   ├── feature_engineering.py
│   ├── models/
│   │   ├── recovery_model.py
│   │   ├── energy_model.py
│   │   ├── maintenance_model.py
│   │   └── quality_model.py
│   ├── optimization/
│   │   ├── process_optimizer.py
│   │   └── maintenance_scheduler.py
│   ├── deployment/
│   │   ├── api_server.py
│   │   └── dashboard.py
│   └── utils/
│       ├── data_validation.py
│       └── model_evaluation.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_process_analysis.ipynb
│   ├── 03_model_development.ipynb
│   └── 04_optimization_analysis.ipynb
├── tests/
│   ├── test_data_processing.py
│   ├── test_models.py
│   └── test_optimization.py
├── docs/
│   ├── technical_documentation.md
│   ├── deployment_guide.md
│   └── user_manual.md
├── dashboards/
│   ├── streamlit_app.py
│   └── plotly_dashboard.py
└── reports/
    ├── analysis_report.md
    ├── model_performance.md
    └── optimization_results.md
```

## 💾 Datasets & Data Sources

### Primary Datasets (Available)

1. **Synthetic Manganese Plant Dataset** (Start Here - Day 1)
   - **Source**: Generate using `src/data_generation/synthetic_plant.py`
   - **Size**: 10,000 records, 50+ features
   - **Content**: Crusher data, spiral separator performance, magnetic separator efficiency
   - **Download**: Auto-generated on first run

2. **Industrial IoT Sensor Dataset**
   - **Source**: Kaggle - "Mineral Processing Plant Sensor Data"
   - **URL**: `kaggle datasets download -d industrial-iot/mineral-processing`
   - **Size**: 25MB, 15,000+ records
   - **Features**: Temperature, vibration, power consumption

3. **Metallurgical Test Results**
   - **Source**: Create synthetic using geological constraints
   - **Script**: `src/data_generation/metallurgical_tests.py`
   - **Content**: Grade analysis, recovery tests, concentrate quality

### Secondary Datasets (Week 2+)

4. **Equipment Maintenance Records**
   - **Source**: Generate based on industry patterns
   - **Content**: Failure modes, maintenance costs, downtime records

5. **Energy Consumption Data**
   - **Source**: Synthetic based on typical manganese plant power curves
   - **Content**: Hourly power consumption, equipment-specific usage

### Getting Started with Data (Execute in Order)

```bash
# 1. Generate synthetic process data (Day 1)
python src/data_generation/synthetic_plant.py --plant_type manganese --days 365

# 2. Download external datasets (Day 1)
kaggle datasets download -d industrial-iot/mineral-processing
python src/data_ingestion/external_data.py

# 3. Create metallurgical test data (Day 2)
python src/data_generation/metallurgical_tests.py --ore_type manganese

# 4. Validate and clean all data (Day 2)
python src/data_preprocessing.py --validate --clean
```

## 🔧 Key Features & Models

### 1. Recovery Optimization Model
- **Algorithm**: XGBoost Regressor
- **Input**: Ore grade, particle size, separator settings
- **Output**: Predicted manganese recovery %
- **Target**: >75% recovery rate

### 2. Energy Efficiency Model
- **Algorithm**: Neural Network
- **Input**: Throughput, equipment settings, ore hardness
- **Output**: kWh per ton processed
- **Target**: <45 kWh/ton

### 3. Predictive Maintenance
- **Algorithm**: Isolation Forest + LSTM
- **Input**: Vibration, temperature, runtime hours
- **Output**: Failure probability, RUL estimation
- **Target**: 95% accuracy in failure prediction

### 4. Quality Control System
- **Algorithm**: Multi-output Random Forest
- **Input**: Process parameters, feed grade
- **Output**: Concentrate grade, impurity levels
- **Target**: ±1% Mn grade consistency

## 📈 Performance Metrics

| Metric | Baseline | Target | Current |
|--------|----------|--------|---------|
| Mn Recovery | 70% | 78% | TBD |
| Energy Efficiency | 50 kWh/t | 42 kWh/t | TBD |
| Equipment Uptime | 85% | 95% | TBD |
| Grade Consistency | ±5% | ±2% | TBD |

## 🔍 Week 1 Milestones

- **Day 1**: ✅ Environment setup, synthetic data generation
- **Day 2**: ✅ Data preprocessing, initial EDA
- **Day 3**: ✅ Feature engineering, correlation analysis
- **Day 4**: ✅ Baseline model development
- **Day 5**: ✅ Model optimization, hyperparameter tuning
- **Day 6**: ✅ Integration testing, performance validation
- **Day 7**: ✅ Documentation, dashboard deployment

## 🛠️ Technologies Used

- **Data Processing**: Pandas, NumPy, Scipy
- **Machine Learning**: Scikit-learn, XGBoost, TensorFlow
- **Optimization**: CVXPY, Scipy.optimize
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Deployment**: FastAPI, Streamlit, Docker
- **Monitoring**: MLflow, Weights & Biases

## 📋 Installation Requirements

```bash
pip install pandas numpy scikit-learn xgboost tensorflow
pip install plotly matplotlib seaborn streamlit
pip install fastapi uvicorn mlflow wandb
pip install cvxpy scipy
```

## 🚀 Quick Demo

```python
# Load sample data and run prediction
from src.models.recovery_model import ManganeseRecoveryModel

model = ManganeseRecoveryModel()
model.load_pretrained()

# Sample input: [grade%, particle_size_mm, spiral_speed_rpm, magnetic_intensity_T]
sample_input = [32.5, 0.5, 45, 1.2]
recovery_prediction = model.predict(sample_input)
print(f"Predicted Mn Recovery: {recovery_prediction:.1f}%")
```

## 📊 Expected Results

After 1 week of development:
- **Functional ML Pipeline**: Complete data-to-model workflow
- **3-4 Trained Models**: Recovery, energy, maintenance, quality
- **Interactive Dashboard**: Real-time monitoring interface
- **Performance Analysis**: Baseline vs optimized scenarios
- **Documentation**: Technical and user guides

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## 📞 Support

- **Technical Issues**: Create GitHub issue
- **Questions**: Email support@yourcompany.com
- **Documentation**: Check `docs/` folder

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

**Ready to optimize your manganese processing plant? Let's start with Day 1! 🚀**