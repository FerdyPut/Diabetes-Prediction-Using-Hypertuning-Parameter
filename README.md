# Diabetes Prediction Using Hypertuning Parameter

## Background:
Diabetes is one of the most dangerous non-communicable diseases, caused by excessive blood sugar levels. According to the World Health Organization (WHO), approximately 1 in 11 adults worldwide suffer from diabetes, totaling around 537 million people in 2021. Diabetes is also a leading cause of death globally.
Given the severity of this disease, I was motivated to develop a diabetes risk prediction system using machine learning algorithms. The goal is to support early detection, allowing individuals to assess their risk and take preventive actions accordingly.

## Project Details:

### Data Source:
Dataset obtained from Kaggle - Diabetes Prediction Dataset

### Objective:
To build a predictive model using machine learning algorithms to determine the likelihood of an individual developing diabetes based on various health-related features, and to evaluate the impact of using SMOTENC for handling class imbalance.

### Machine Learning Algorithms Used:
- K-Nearest Neighbors (KNN)
- Decision Tree
- Random Forest
- Logistic Regression

### Methodology:
- Data Preprocessing: Includes normalization and handling class imbalance using SMOTENC (Synthetic Minority Oversampling Technique for Nominal and Continuous data).
- Experimental Design:
a) Baseline models (without SMOTENC).
b) Models trained with balanced data using SMOTENC.
c) Hyperparameter Tuning: Conducted using GridSearchCV to optimize each model’s performance.

### Model Evaluation:
Evaluation metrics used: Recall and ROC-AUC
The performance of models with and without SMOTENC will be compared to assess the effect of data balancing.

### Results:
![image](https://github.com/user-attachments/assets/d27a8b4e-976b-4033-aa48-942a5ab53caf)

![image](https://github.com/user-attachments/assets/77353f28-a26d-4038-9bcb-f96d8f6a16bc)

Interpretation: 
The Random Forest model (NON SMOTE) performed the best as it achieved the highest recall score and did not exhibit significant overfitting. This indicates that the model is able to generalize well across both the training and testing datasets. This is further supported by the ROC-AUC results, where the closer the ROC-AUC values are between the training and testing sets, the more stable and less overfitted the model tends to be.

![image](https://github.com/user-attachments/assets/f804c528-c0c8-4e98-bb82-abafcd5233e9)

![image](https://github.com/user-attachments/assets/3fa98324-ecb5-42aa-a9b4-51741368869f)

Interpretation: 
The Random Forest model (SMOTE) performed the best as it achieved the highest recall score and did not exhibit significant overfitting. This indicates that the model is able to generalize well across both the training and testing datasets. This is further supported by the ROC-AUC results, where the closer the ROC-AUC values are between the training and testing sets, the more stable and less overfitted the model tends to be.

Therefore, the chosen model between Random Forest with SMOTE and without SMOTE is the Random Forest without SMOTE. This is because it has a relatively low overfitting gap—around 4%, which indicates better generalization—compared to the SMOTE version. In addition, the recall score on the testing set is also considerably high, making it a more reliable option for prediction.


                                                                      -THANK YOU-
FOLLOW MORE:

Linkedln: linkedin.com/in/ferdypput

