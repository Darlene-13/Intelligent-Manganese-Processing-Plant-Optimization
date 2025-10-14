# Data Cleaning in Machine Learning

A comprehensive guide to cleaning and preparing data for machine learning models using the Titanic dataset.

## Overview

Data cleaning is a critical step in machine learning that involves identifying and removing missing, duplicate, or irrelevant data. Raw data is often noisy, incomplete, and inconsistent, which can negatively impact model accuracy. This guide demonstrates systematic approaches to ensure your data is accurate, consistent, and ready for analysis.

## Why Data Cleaning Matters

- **Improved Model Performance**: Clean data helps models learn better patterns
- **Increased Accuracy**: Ensures predictions are based on reliable information
- **Better Insights**: Enhanced interpretability during exploratory data analysis (EDA)
- **Data Quality**: Creates reliable and accurate datasets for analysis

## Prerequisites

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
```

## Dataset

This tutorial uses the Titanic dataset (`Titanic-Dataset.csv`), which contains passenger information including survival status, age, class, and other features.

## Step-by-Step Process

### 1. Load and Inspect Data
- Import necessary libraries
- Load the dataset using pandas
- Review data structure with `.info()` and `.head()`

### 2. Identify Data Issues
- Check for duplicate rows
- Separate categorical and numerical columns
- Count unique values in categorical features
- Calculate missing value percentages

### 3. Handle Missing Data
- Drop columns with excessive missing values (e.g., Cabin)
- Remove rows with missing critical values (e.g., Embarked)
- Impute missing values using mean for numerical features

### 4. Remove Outliers
- Visualize distributions using box plots
- Calculate outlier boundaries using mean ± 2 standard deviations
- Filter data to remove extreme values
- Repeat the process to ensure consistency

### 5. Data Validation
- Select relevant features for modeling
- Separate independent variables (X) from target variable (Y)
- Remove features that don't contribute to predictions

### 6. Data Formatting
- Apply Min-Max Scaling to normalize features between 0 and 1
- Consider Standardization (Z-score) for Gaussian distributions

## Key Techniques Covered

**Missing Value Handling**
- Deletion of irrelevant columns
- Row removal for critical missing values
- Mean imputation for numerical features

**Outlier Detection**
- Statistical methods (mean ± 2σ)
- Visual identification with box plots
- Iterative removal process

**Data Transformation**
- Min-Max Scaling: Rescales values to [0, 1] range
- Standardization: Transforms to zero mean and unit variance

## Tools Mentioned

- **OpenRefine**: Free, open-source data cleaning tool
- **Trifacta Wrangler**: AI-powered transformation platform
- **TIBCO Clarity**: Data profiling and cleansing
- **Cloudingo**: Cloud-based deduplication
- **IBM InfoSphere QualityStage**: Enterprise-grade data quality management

## Advantages

✅ Improved model performance through error removal  
✅ Increased accuracy and consistency  
✅ Better representation of underlying patterns  
✅ Enhanced data security by removing sensitive information  

## Limitations

⚠️ **Time-consuming**: Especially for large datasets  
⚠️ **Risk of information loss**: Important data may be accidentally removed  
⚠️ **Resource-intensive**: Requires expertise and specialized tools  
⚠️ **Overfitting risk**: Excessive cleaning can remove valuable variation  

## Best Practices

1. Always keep a backup of your original dataset
2. Document every cleaning step for reproducibility
3. Validate assumptions before removing data
4. Balance thoroughness with the risk of information loss
5. Consider domain expertise when handling outliers
6. Test your model performance at each cleaning stage

## Usage Example

```python
# Load data
df = pd.read_csv('Titanic-Dataset.csv')

# Remove duplicates and irrelevant columns
df = df.drop_duplicates()
df = df.drop(columns=['Name', 'Ticket', 'Cabin'])

# Handle missing values
df.dropna(subset=['Embarked'], inplace=True)
df['Age'].fillna(df['Age'].mean(), inplace=True)

# Remove outliers
mean, std = df['Age'].mean(), df['Age'].std()
lower_bound, upper_bound = mean - 2*std, mean + 2*std
df = df[(df['Age'] >= lower_bound) & (df['Age'] <= upper_bound)]

# Prepare features
X = df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]
Y = df['Survived']

# Scale numerical features
scaler = MinMaxScaler()
num_cols = X.select_dtypes(include=[np.number]).columns
X[num_cols] = scaler.fit_transform(X[num_cols])
```

## Contributing

Feel free to suggest improvements or report issues with the data cleaning process.

## License

This tutorial is provided for educational purposes.

---

**Last Updated**: September 16, 2025