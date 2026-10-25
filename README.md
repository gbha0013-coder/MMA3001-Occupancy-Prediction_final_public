
## Project Overview
This project uses machine learning to predict the maximum recorded hourly headcount in building spaces using the Monash Smart Infrastructure occupancy dataset.

Three models are compared:
- Baseline (Mean Prediction)
- Linear Regression
- Decision Tree Regression

## Dataset
The project analyses 100,000 occupancy sensor records, aggregated into 1,969 hourly observations across two monitored spaces.

**Inputs:** Hour of day, day of week and monitored space ID.

**Output:** Predicted maximum recorded hourly headcount.

The original dataset is provided through MMA3001 and is not included in this repository.

## How to Run
1. Open `occupancy_prediction.ipynb` in Google Colab.
2. Upload the original MMA3001 Dataset 2 ZIP file.
3. Run all notebook cells in order.

**Required libraries:** pandas, NumPy, matplotlib and scikit-learn.

## Results

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Baseline | 1.592 | 2.186 | -0.004 |
| Linear Regression | 1.160 | 1.692 | 0.399 |
| Decision Tree | 1.135 | 1.657 | 0.424 |

Both machine learning models outperform the baseline on the test data.

## Limitations
The analysis uses only the first 100,000 records. Sensor readings are irregular, and predictions are less accurate at high headcounts. Hours without observations are excluded.

## AI Usage
ChatGPT assisted with coding, debugging and documentation. AI-generated suggestions were checked against executed code and project results.

## Licence
MIT License applies to original project code, not the dataset.
