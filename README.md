# 🛡️ SentinelNet – Intelligent Network Behaviour Analysis

**A Machine Learning-based Network Security Application for Intrusion Detection and Network Behaviour Analysis.**

## 📌 Project Overview

SentinelNet is a machine learning project developed using the **UNSW-NB15 dataset** to analyse network traffic through two complementary approaches:

1. **Intrusion Detection:** Classifies network traffic as Normal or Attack using supervised machine learning.
2. **Network Behaviour Analysis:** Identifies groups of similar network traffic patterns using unsupervised learning.

Both models are integrated into an interactive Streamlit application.

## 🎯 Project Objectives

- Detect potentially malicious network traffic.
- Discover network communication patterns through clustering.
- Identify meaningful network traffic characteristics using feature engineering.
- Compare machine learning algorithms and select suitable models.
- Provide interpretable outputs through an interactive application.

## 🔬 Methodology – CRISP-ML(Q)

The project follows the **CRISP-ML(Q) (Cross-Industry Standard Process for Machine Learning with Quality Assurance)** methodology.

**1. Business & Data Understanding**
- Identified the need for automated network intrusion detection and behavioural analysis.
- Explored the UNSW-NB15 dataset, including its features, distributions, data types and target variables.
- Defined separate objectives for classification and clustering.

**2. Data Preparation**
- Performed data cleaning, missing-value checks and exploratory data analysis.
- Conducted feature selection to identify relevant network attributes.
- Performed **Feature Engineering** to create meaningful traffic characteristics, including total packets, total packet size and other network-related features.
- Applied categorical encoding and feature scaling.
- Prepared separate datasets for classification and clustering, excluding target labels from clustering.
- Applied PCA for dimensionality reduction in the clustering workflow.

**3. Model Engineering**
- **Classification:** Experimented with multiple classification algorithms and selected Random Forest as the best-performing model based on comparative evaluation.
- **Clustering:** Experimented with clustering approaches and selected K-Means for network traffic behavioural grouping.

**4. Model Evaluation**
- **Classification:** Evaluated models using Accuracy, Precision, Recall, F1-score and Confusion Matrix.
- **Clustering:** Used the Elbow Method, Silhouette Score, cluster distribution and behavioural profiling to evaluate clustering quality and interpretability.

**5. Model Deployment**
- Saved the trained Random Forest model and complete clustering pipeline using Pickle.
- Integrated both models into an interactive Streamlit application.

**6. Monitoring & Quality Assurance**
- Maintained consistent preprocessing between training and application inference.
- Incorporated input validation and prediction handling.
- Identified opportunities for future model monitoring and improvements.

## 🧠 Model 1 – Intrusion Detection

**Algorithm: Random Forest Classifier (Supervised Learning)**

**Objective:** Classify network traffic into Normal or Attack categories.

**Approach:**
- Used the `label` column as the binary classification target.
- Prepared network traffic features through preprocessing and feature engineering.
- Experimented with and compared multiple classification algorithms.
- Selected Random Forest based on comparative model evaluation.

**Output:**
- `0` – Normal
- `1` – Attack

Random Forest uses an ensemble of decision trees to capture relationships between network traffic characteristics and their corresponding classes.

## 🔍 Model 2 – Network Behaviour Analysis

**Algorithm: K-Means Clustering (Unsupervised Learning)**

**Objective:** Discover groups of network traffic records with similar communication characteristics without using predefined labels.

**Approach:**
- Excluded `label` and `attack_cat` from clustering inputs.
- Applied categorical encoding and feature scaling.
- Used PCA to retain 95% explained variance with 22 principal components.
- Experimented with clustering configurations and selected K-Means for final behavioural grouping.
- Evaluated clusters using the Elbow Method, Silhouette Score and behavioural profiling.

**Output:**

Network traffic records are assigned to behavioural clusters based on similarities in their communication patterns, such as protocol usage, packet volume, data transfer and connection characteristics.

*Cluster IDs represent behavioural groups and do not automatically indicate attacks.*


## 🖥️ Streamlit Application

The application provides three main sections:

- **Home:** SentinelNet introduction and navigation.
- **Intrusion Detection:** Accepts network traffic inputs and displays classification predictions.
- **Behaviour Analysis:** Processes network traffic and displays the assigned behavioural cluster with its interpretation.

## 🛠️ Technologies Used

- **Programming:** Python
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn
- **Classification:** Random Forest
- **Clustering:** K-Means
- **Dimensionality Reduction:** PCA
- **Deployment:** Streamlit
- **Model Serialization:** Pickle


## 🚀 Future Enhancements

- Real-time network traffic analysis.
- Improved behavioural cluster interpretation.
- Additional machine learning model experimentation.
- Advanced network traffic visualizations.
- Model monitoring and periodic retraining.


---

**SentinelNet – Understanding Network Traffic. Discovering Behaviour. Supporting Security.**
