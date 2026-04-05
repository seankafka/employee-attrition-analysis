
# Employee Attrition Analysis

## Repository Outline

```
.
├── dataset/
│   └── HR_Attrition.csv                    - Employee attrition dataset
├── project-notebook /
│   └── employee-attrition_analysis.ipynb   - Project notebook covering employee attrition analysis
│
├── LICENSE                                 - License information for this repository
└── README.md                               - Project documentation

```

## Overview

This project explores employee attrition using an end-to-end data analysis approach. The main objective is to understand what factors are most associated with employees leaving the company, and translate those findings into actionable business insights.

The analysis focuses not only on statistical relationships, but also on how employees experience their work on a day-to-day basis. This is important because attrition is rarely driven by a single factor, but rather by a combination of workload, compensation, and overall work experience.

Dashboard Deployment: [Hugging Face Spaces](https://huggingface.co/spaces/seankafka/Employee-Attrition-Dashboard).

## Objectives

The goals of this project are:

* Identify key factors associated with employee attrition
* Understand how work conditions, compensation, and employee experience influence attrition
* Distinguish between statistically significant variables and practically meaningful ones
* Translate analytical findings into clear business recommendations
* Build a portfolio-ready analysis that is understandable for non-technical stakeholders

## Dataset

This project uses the dataset authored by Mark Bradbourne and published on [Data.World](https://data.world/markbradbourne/rwfd-real-world-fake-data-season-2/workspace/file?filename=HR_Attrition.csv).
The dataset contains **1,470 employee records** and initially includes **37 columns** covering:

* Demographics (e.g., Age, Marital Status)
* Career and role (e.g., Job Role, Department, Job Level)
* Work conditions (e.g., OverTime, Business Travel)
* Compensation and benefits (e.g., Monthly Income, Stock Option Level)
* Employee experience (e.g., Job Satisfaction, Work-Life Balance)

Target variable:
* **Attrition** (Yes / No)

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

## Limitations

* Statistical significance does not imply causation
* Some variables, such as performance rating, have limited variability
* Small group sizes in certain categories may affect interpretation

## Tools and Libraries

* Language: Python
* Data Handling: Pandas, NumPy
* Visualization: Plotly
* Statistics: SciPy
* Dashboard: Streamlit
* Deployment: Hugging Face Spaces (Docker)

## Author

This project was developed as part of a data learning journey, with a focus on building practical and business-relevant analytical skills.

Sean Kafka Adhyaksa  
[Github](https://github.com/seankafka) || [LinkedIn](https://www.linkedin.com/in/seankafka/)
