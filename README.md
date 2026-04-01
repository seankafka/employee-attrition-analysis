# Employee Attrition Analysis

## Repository Outline

```
.
├── streamlit_app.py                         - Entry point for Streamlit Cloud deployment
├── requirements.txt                         - Python dependencies for Streamlit
├── deployment/
│   ├── app.py                               - Main Streamlit application
│   └── src/
│       ├── __init__.py
│       ├── analysis.py                      - Statistical analysis functions
│       ├── charts.py                        - Plotly visualization functions
│       └── data.py                          - Data loading and preprocessing
├── project-notebooks/
│   └── employee-attrition_analysis.ipynb    - Notebook for data analysis
├── dataset/
│   └── HR_Attrition.csv                     - Employee attrition dataset
├── README.md                                - Project documentation
└── LICENSE
```

---

## Deployment Notes

**Root-level files** (`streamlit_app.py`, `requirements.txt`) are required for Streamlit Cloud deployment. Streamlit Cloud expects these files at the repository root to properly configure the app and install dependencies. The main application code remains organized in the `deployment/` folder for clean project structure.

---

## Overview

This project explores employee attrition using an end-to-end data analysis approach.
The main objective is to understand what factors are most associated with employees leaving the company, and translate those findings into actionable business insights.

The analysis focuses not only on statistical relationships, but also on how employees experience their work on a day-to-day basis. This is important because attrition is rarely driven by a single factor, but rather by a combination of workload, compensation, and overall work experience.

Dashboard Deployment: [Streamlit](https://employee-attrition-db.streamlit.app)

---

## Objectives

The goals of this project are:

* Identify key factors associated with employee attrition
* Understand how work conditions, compensation, and employee experience influence attrition
* Distinguish between statistically significant variables and practically meaningful ones
* Translate analytical findings into clear business recommendations
* Build a portfolio-ready analysis that is understandable for non-technical stakeholders

---

## Dataset
This project uses dataset authored by Mark Bradbourne, accessed through [Data.World](https://data.world/markbradbourne/rwfd-real-world-fake-data-season-2/workspace/file?filename=HR_Attrition.csv)  
The dataset contains employee-level information related to:

* Demographics (e.g., Age, Marital Status)
* Career and role (e.g., Job Role, Department, Job Level)
* Work conditions (e.g., OverTime, Business Travel)
* Compensation and benefits (e.g., Monthly Income, Stock Option Level)
* Employee experience (e.g., Job Satisfaction, Work-Life Balance)

Target variable:
* **Attrition** (Yes / No)

---

## Key Findings

Several consistent patterns emerge from the analysis:

### 1. Workload and Work Structure Matter Most

* Overtime and job role show strong association with attrition
* Business travel and workload intensity increase risk

### 2. Day-to-Day Experience Is a Major Driver

* Lower job satisfaction, environment satisfaction, and work-life balance are strongly linked to attrition
* Job involvement also plays a role in whether employees stay or leave

### 3. Compensation Alone Is Not Enough

* Lower income and lack of stock options are associated with higher attrition
* However, salary hike does not appear to be a strong differentiator

### 4. Career Stability Reduces Attrition Risk

* Employees with longer tenure, higher job level, and more stable roles are less likely to leave

### 5. Performance Rating Is Not Informative

* Limited variation in performance ratings reduces its usefulness
* It does not meaningfully differentiate between employees who leave and those who stay

---

## Key Insight

Attrition in this dataset is not primarily driven by poor performance.
Instead, it is more closely related to a combination of:

* Unsustainable workload
* Lack of perceived long-term value
* Unsatisfying day-to-day work experience

This shifts the focus from evaluation metrics to **work design and employee experience**.

---

## Business Recommendations

Based on the findings, several actions can be considered:

### 1. Manage Workload and Overtime

* Monitor and reduce excessive overtime
* Rebalance workload across roles

### 2. Improve Employee Experience

* Focus on work-life balance and job satisfaction
* Improve the working environment and daily experience

### 3. Strengthen Long-Term Value

* Enhance retention through benefits like stock options
* Communicate long-term growth opportunities more clearly

### 4. Focus on High-Risk Segments

* Identify roles and groups with higher attrition risk
* Apply targeted retention strategies instead of one-size-fits-all policies

---

## Limitations

* Statistical significance does not imply causation
* Some variables (e.g., performance rating) have limited variability
* Small group sizes in certain categories may affect interpretation

---

## Tools & Libraries

* Language: Python
* Data Handling: Pandas, NumPy
* Visualization: Matplotlib, Seaborn, Plotly
* Statistics: SciPy
* Dashboard: Streamlit

---

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/seankafka/employee-attrition-analysis.git
   cd employee-attrition-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r deployment/requirements.txt
   ```

### Running the Dashboard

To launch the interactive Streamlit dashboard:

```bash
streamlit run deployment/app.py
```

The dashboard will open at `http://localhost:8501` and provide interactive filters and visualizations of the analysis.

---

## Author
This project was developed as part of a data learning journey, with a focus on building practical and business-relevant analytical skills.

Sean Kafka Adhyaksa
[Github](https://github.com/seankafka) || [LinkedIn](https://www.linkedin.com/in/seankafka/)
