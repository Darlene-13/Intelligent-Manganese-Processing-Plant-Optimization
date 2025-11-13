# Intelligent Manganese Processing Plant Optimization

##  Project Overview

This project develops machine learning models to optimize manganese ore processing operations, focusing on recovery maximization, energy efficiency, and predictive maintenance. The system targets typical manganese processing workflows including crushing, screening, gravity separation, and magnetic separation.

## Problem Statement

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

##️ System Architecture

### PYTHON DATA BACKEND
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

### INDUSTRIAL BACKEND (JAVA)
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Plant Sensors  │─────>│  Java Streaming  │─────>│  ML Models      │
│  (SCADA/PLC)    │      │  (Kafka/Flink)   │      │  (Python/DJL)   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │                          │
                                  v                          v
                         ┌──────────────────┐      ┌─────────────────┐
                         │  Spring Boot API │<─────│  Optimization   │
                         │  (Java Backend)  │      │  Results        │
                         └──────────────────┘      └─────────────────┘
                                  │
                                  v
                         ┌──────────────────┐
                         │  Web Dashboard   │
                         │  (React/Angular) │
                         └──────────────────┘

```


##  Project Structure
### MACHINE LEARNING PROJECT STRUCTURE
```
manganese-ml-optimization/
├── README.md
├── requirements.txt
├── config/
│   ├── model_config.yaml
│   ├── data_config.yaml
│   └── processing_parameters.yaml
├── data/
│   ├── synthetic/
│   │   ├── manganese_crushing_circuit.csv/
│   │   ├── manganese_energy_consumption.csv/
│   │   ├── manganese_equipment_health.csv/
│   │   └── manganese_ore_feed.csv/
│   │   ├── manganese_separation_circuit.csv
│   ├── manganese_synthetic_generator.py
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
### INDUSTRIAL JAVA BACKEND STRUCTURE
```
manganese-optimization-api/
│
├── pom.xml                                    # Maven dependencies
├── README.md
├── .gitignore
│
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── manganese/
│   │   │           └── optimization/
│   │   │               │
│   │   │               ├── ManganeseOptimizationApplication.java    # Main Spring Boot application
│   │   │               │
│   │   │               ├── config/
│   │   │               │   ├── AppConfig.java                       # General app configuration
│   │   │               │   ├── SecurityConfig.java                  # Security settings
│   │   │               │   ├── KafkaConfig.java                     # Kafka configuration
│   │   │               │   ├── WebSocketConfig.java                 # WebSocket configuration
│   │   │               │   └── SwaggerConfig.java                   # API documentation
│   │   │               │
│   │   │               ├── controller/
│   │   │               │   ├── PredictionController.java            # ML prediction endpoints
│   │   │               │   ├── OptimizationController.java          # Optimization endpoints
│   │   │               │   ├── DataIngestionController.java         # Data upload endpoints
│   │   │               │   ├── MonitoringController.java            # Plant monitoring endpoints
│   │   │               │   └── HealthCheckController.java           # Health check endpoints
│   │   │               │
│   │   │               ├── service/
│   │   │               │   ├── prediction/
│   │   │               │   │   ├── PredictionService.java           # Main prediction service
│   │   │               │   │   ├── RecoveryPredictionService.java   # Recovery rate prediction
│   │   │               │   │   ├── EnergyPredictionService.java     # Energy consumption prediction
│   │   │               │   │   └── MaintenancePredictionService.java # Maintenance prediction
│   │   │               │   │
│   │   │               │   ├── optimization/
│   │   │               │   │   ├── OptimizationService.java         # Process optimization logic
│   │   │               │   │   ├── RecoveryOptimizer.java           # Recovery maximization
│   │   │               │   │   └── EnergyOptimizer.java             # Energy minimization
│   │   │               │   │
│   │   │               │   ├── integration/
│   │   │               │   │   ├── ModelIntegrationService.java     # Python model integration
│   │   │               │   │   ├── ScadaIntegrationService.java     # SCADA system integration
│   │   │               │   │   └── DatabaseSyncService.java         # Database synchronization
│   │   │               │   │
│   │   │               │   ├── streaming/
│   │   │               │   │   ├── KafkaConsumerService.java        # Kafka consumer for real-time data
│   │   │               │   │   ├── KafkaProducerService.java        # Kafka producer for results
│   │   │               │   │   └── DataStreamProcessor.java         # Stream processing logic
│   │   │               │   │
│   │   │               │   └── validation/
│   │   │               │       ├── DataValidationService.java       # Input data validation
│   │   │               │       └── ModelOutputValidator.java        # ML output validation
│   │   │               │
│   │   │               ├── model/
│   │   │               │   ├── dto/
│   │   │               │   │   ├── PredictionRequest.java           # Prediction request DTO
│   │   │               │   │   ├── PredictionResponse.java          # Prediction response DTO
│   │   │               │   │   ├── OptimizationRequest.java         # Optimization request DTO
│   │   │               │   │   ├── OptimizationResponse.java        # Optimization response DTO
│   │   │               │   │   ├── ProcessDataDTO.java              # Process data DTO
│   │   │               │   │   ├── EquipmentStatusDTO.java          # Equipment status DTO
│   │   │               │   │   └── LabResultDTO.java                # Lab results DTO
│   │   │               │   │
│   │   │               │   ├── entity/
│   │   │               │   │   ├── ProcessData.java                 # Process data entity
│   │   │               │   │   ├── Equipment.java                   # Equipment entity
│   │   │               │   │   ├── LabResult.java                   # Lab result entity
│   │   │               │   │   ├── PredictionHistory.java           # Prediction history
│   │   │               │   │   └── OptimizationHistory.java         # Optimization history
│   │   │               │   │
│   │   │               │   └── enums/
│   │   │               │       ├── ProcessStage.java                # Crushing, screening, etc.
│   │   │               │       ├── EquipmentStatus.java             # Running, maintenance, etc.
│   │   │               │       └── OptimizationType.java            # Recovery, energy, etc.
│   │   │               │
│   │   │               ├── repository/
│   │   │               │   ├── ProcessDataRepository.java           # Process data JPA repository
│   │   │               │   ├── EquipmentRepository.java             # Equipment JPA repository
│   │   │               │   ├── LabResultRepository.java             # Lab result JPA repository
│   │   │               │   ├── PredictionHistoryRepository.java     # Prediction history
│   │   │               │   └── OptimizationHistoryRepository.java   # Optimization history
│   │   │               │
│   │   │               ├── exception/
│   │   │               │   ├── GlobalExceptionHandler.java          # Global exception handler
│   │   │               │   ├── ModelException.java                  # ML model exceptions
│   │   │               │   ├── ValidationException.java             # Validation exceptions
│   │   │               │   └── IntegrationException.java            # Integration exceptions
│   │   │               │
│   │   │               ├── util/
│   │   │               │   ├── DataPreprocessor.java                # Data preprocessing utilities
│   │   │               │   ├── FeatureExtractor.java                # Feature extraction
│   │   │               │   ├── MetricsCalculator.java               # Metrics calculation
│   │   │               │   └── DateTimeUtil.java                    # Date/time utilities
│   │   │               │
│   │   │               ├── websocket/
│   │   │               │   ├── RealTimeDataHandler.java             # WebSocket handler
│   │   │               │   └── NotificationHandler.java             # Alert notifications
│   │   │               │
│   │   │               └── scheduler/
│   │   │                   ├── ModelRetrainingScheduler.java        # Scheduled model retraining
│   │   │                   ├── DataSyncScheduler.java               # Scheduled data sync
│   │   │                   └── HealthCheckScheduler.java            # Scheduled health checks
│   │   │
│   │   └── resources/
│   │       ├── application.yml                                      # Main configuration
│   │       ├── application-dev.yml                                  # Development config
│   │       ├── application-prod.yml                                 # Production config
│   │       │
│   │       ├── db/
│   │       │   └── migration/
│   │       │       ├── V1__initial_schema.sql                       # Database schema
│   │       │       └── V2__add_optimization_tables.sql              # Schema updates
│   │       │
│   │       ├── ml-models/                                           # Stored ML models
│   │       │   ├── recovery_model.pkl
│   │       │   ├── energy_model.pkl
│   │       │   └── maintenance_model.pkl
│   │       │
│   │       └── static/
│   │           └── swagger-ui/                                      # API documentation
│   │
│   └── test/
│       └── java/
│           └── com/
│               └── manganese/
│                   └── optimization/
│                       ├── controller/
│                       │   ├── PredictionControllerTest.java
│                       │   └── OptimizationControllerTest.java
│                       │
│                       ├── service/
│                       │   ├── PredictionServiceTest.java
│                       │   └── OptimizationServiceTest.java
│                       │
│                       └── integration/
│                           ├── PredictionIntegrationTest.java
│                           └── OptimizationIntegrationTest.java
│
├── docker/
│   ├── Dockerfile                                                   # Docker image
│   ├── docker-compose.yml                                           # Multi-container setup
│   └── init-scripts/
│       └── init-db.sql                                              # Database initialization
│
├── scripts/
│   ├── start-dev.sh                                                 # Start development server
│   ├── deploy-prod.sh                                               # Production deployment
│   └── run-tests.sh                                                 # Run test suite
│
└── docs/
    ├── API.md                                                       # API documentation
    ├── ARCHITECTURE.md                                              # Architecture overview
    ├── DEPLOYMENT.md                                                # Deployment guide
    └── INTEGRATION.md                                               # Integration guide

```

## Datasets & Data Sources

### Primary Datasets (Available)

1. **Simulated Manganese Plant Dataset**
   - **Source**: Generate using `src/data_generation/synthetic_plant.py`
   - **Size**: 10,000 records, 50+ features
   - **Content**: Crusher data, spiral separator performance, magnetic separator efficiency
   - **Download**: Auto-generated on first run

2. **Industrial IoT Sensor Dataset** # To be simulated
   - **Source**: Kaggle - "Mineral Processing Plant Sensor Data"
   - **URL**: `src/data_generation/industrial-iot/mineral-processing`
   - **Size**: 25MB, 15,000+ records
   - **Features**: Temperature, vibration, power consumption

3. **Metallurgical Test Results**
   - **Source**: Generated synthetic using geological constraints
   - **Script**: `src/data_generation/metallurgical_tests.py`
   - **Content**: Grade analysis, recovery tests, concentrate quality

### Secondary Datasets (Week 2+)

4. **Equipment Maintenance Records**
   - **Source**: Generated based on industry patterns
   - **Content**: Failure modes, maintenance costs, downtime records

5. **Energy Consumption Data**
   - **Source**: Synthetic (Generated) based on typical manganese plant power curves
   - **Content**: Hourly power consumption, equipment-specific usage

## 🔧 Key Features & Models

# Manganese Processing Plant Optimization - Key Features

## Machine Learning Models

### 1. Recovery Optimization Model
- **Algorithm**: XGBoost Regressor
- **Input**: Ore grade, particle size, separator settings
- **Output**: Predicted manganese recovery %
- **Target**: >75% recovery rate
- **Java Integration**: REST API endpoint for real-time recovery prediction

### 2. Energy Efficiency Model
- **Algorithm**: Neural Network
- **Input**: Throughput, equipment settings, ore hardness
- **Output**: kWh per ton processed
- **Target**: <45 kWh/ton
- **Java Integration**: Streaming analytics via Kafka for continuous energy monitoring

### 3. Predictive Maintenance
- **Algorithm**: Isolation Forest + LSTM
- **Input**: Vibration, temperature, runtime hours
- **Output**: Failure probability, RUL estimation
- **Target**: 95% accuracy in failure prediction
- **Java Integration**: WebSocket alerts for maintenance warnings, scheduled batch predictions

### 4. Quality Control System
- **Algorithm**: Multi-output Random Forest
- **Input**: Process parameters, feed grade
- **Output**: Concentrate grade, impurity levels
- **Target**: ±1% Mn grade consistency
- **Java Integration**: Real-time quality monitoring dashboard with automated alerts

---

## Java Backend Features

### 5. Real-Time Data Ingestion Pipeline
- **Technology**: Apache Kafka + Kafka Streams
- **Functionality**: 
  - Ingest sensor data from SCADA/PLC systems
  - Process 10,000+ data points per second
  - Data validation and cleaning
  - Stream processing for immediate insights
- **Target**: <100ms latency for data processing

### 6. Production-Ready ML API Service
- **Technology**: Spring Boot REST API
- **Endpoints**:
  - `/api/v1/predict/recovery` - Recovery rate prediction
  - `/api/v1/predict/energy` - Energy consumption forecast
  - `/api/v1/predict/maintenance` - Equipment failure prediction
  - `/api/v1/optimize/process` - Process parameter optimization
  - `/api/v1/quality/monitor` - Real-time quality metrics
- **Features**:
  - Request validation and sanitization
  - Response caching for frequently requested predictions
  - Rate limiting and authentication
  - Comprehensive API documentation (Swagger/OpenAPI)

### 7. Model Integration Layer
- **Technology**: Spring Boot + Python Model Serving
- **Functionality**:
  - Seamless integration with Python ML models
  - Model versioning and A/B testing
  - Fallback mechanisms for model failures
  - Model performance monitoring
- **Integration Methods**:
  - HTTP-based model serving (Flask/FastAPI)
  - File-based communication via shared storage
  - gRPC for high-performance inference

### 8. SCADA/PLC Integration Module
- **Technology**: Java OPC UA Client / Modbus TCP
- **Functionality**:
  - Connect to industrial control systems
  - Real-time equipment status monitoring
  - Bidirectional communication (read sensors, send control signals)
  - Protocol translation and data normalization
- **Target**: Support for 500+ concurrent sensor connections

### 9. WebSocket Real-Time Dashboard Backend
- **Technology**: Spring WebSocket + STOMP
- **Features**:
  - Live plant metrics streaming
  - Real-time alerts and notifications
  - Equipment status updates
  - Performance KPI broadcasting
- **Target**: Push updates to 100+ concurrent dashboard users

### 10. Batch Processing & Historical Analysis
- **Technology**: Spring Batch
- **Functionality**:
  - Nightly batch predictions for process optimization
  - Historical data aggregation and trend analysis
  - Report generation (daily, weekly, monthly)
  - Data archival and cleanup
- **Target**: Process 1M+ historical records per batch job

### 11. Alert & Notification System
- **Technology**: Spring Event-Driven Architecture
- **Features**:
  - Multi-channel notifications (email, SMS, in-app)
  - Configurable alert thresholds
  - Alert prioritization and escalation
  - Alert history and audit trail
- **Alert Types**:
  - Equipment failure warnings
  - Quality deviations
  - Energy consumption anomalies
  - Recovery rate drops

### 12. Data Persistence & Analytics
- **Technology**: PostgreSQL + Spring Data JPA
- **Features**:
  - Time-series data storage for sensor readings
  - Prediction history tracking
  - Equipment maintenance logs
  - Quality control records
- **Performance**: Optimized queries with indexing, partitioning for time-series data

### 13. Model Performance Monitoring
- **Technology**: Spring Actuator + Micrometer
- **Metrics Tracked**:
  - Model prediction latency
  - Prediction accuracy over time
  - Model drift detection
  - API endpoint performance
  - System resource utilization
- **Integration**: Prometheus, Grafana for visualization

### 14. Security & Access Control
- **Technology**: Spring Security + JWT
- **Features**:
  - Role-based access control (RBAC)
  - JWT authentication for API access
  - Audit logging for all operations
  - Encrypted data transmission (TLS/SSL)
- **Roles**: Admin, Plant Manager, Operator, Read-Only

### 15. Multi-Environment Deployment
- **Technology**: Docker + Kubernetes
- **Environments**:
  - Development (local testing)
  - Staging (pre-production validation)
  - Production (live plant operations)
- **Features**:
  - Containerized microservices
  - Auto-scaling based on load
  - Rolling updates with zero downtime
  - Environment-specific configurations

### 16. Optimization Recommendation Engine
- **Technology**: Java Optimization Algorithms + ML Integration
- **Functionality**:
  - Generate actionable process improvement recommendations
  - Multi-objective optimization (recovery vs. energy vs. quality)
  - Constraint-aware suggestions (equipment limits, safety bounds)
  - ROI calculation for recommendations
- **Output**: Ranked list of optimization actions with expected impact

### 17. Integration Testing & CI/CD Pipeline
- **Technology**: JUnit 5, Mockito, TestContainers
- **Features**:
  - Unit tests for all services
  - Integration tests for API endpoints
  - End-to-end tests for critical workflows
  - Automated testing in CI/CD pipeline
- **Target**: >80% code coverage

### 18. Scheduled Model Retraining Coordinator
- **Technology**: Spring Scheduler
- **Functionality**:
  - Trigger Python model retraining jobs
  - Monitor retraining progress
  - Validate new model performance
  - Automated model deployment after validation
- **Schedule**: Weekly retraining with performance validation

---

## Integration Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                        Plant Floor Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ SCADA    │  │ Sensors  │  │ Equipment│  │ Lab      │       │
│  │ Systems  │  │ (IoT)    │  │ PLCs     │  │ Systems  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
└───────────────────────────────────────────────────────────────

```


## Performance Metrics

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

## Technologies Used

- **Data Processing**: Pandas, NumPy, Scipy
- **Machine Learning**: Scikit-learn, XGBoost, TensorFlow
- **Optimization**: CVXPY, Scipy.optimize
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Deployment**: FastAPI, Streamlit, Docker
- **Monitoring**: MLflow, Weights & Biases

## Installation Requirements

```bash
pip install uv
uv pip install -r requirements.txt
```

## Quick Demo

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

## Expected Results

- **Functional ML Pipeline**: Complete data-to-model workflow
- **Trained Models**: Recovery, energy, maintenance, quality
- **Interactive Dashboard**: Real-time monitoring interface
- **Performance Analysis**: Baseline vs optimized scenarios
- **Production-Ready API**: High Performance Java APIs
- **Real-Time Data Integration**: Using Kafka
- **Scalable Architecture**: Industrial Levele
- **Documentation**: Technical and user guides

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

##  Support

- **Technical Issues**: Create GitHub issue
- **Questions**: Email darlenewendie@gmail.com
- **Documentation**: Check `docs/` and `reports/` folder

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---
### Written By:
Darlene Wendie