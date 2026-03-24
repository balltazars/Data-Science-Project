# Predicting Student Academic Performance and Identifying Key Success Factors

## Repository Outline
1. deployment - A folder containing all files related to model deployment
2. P1M2_clarence_manzo.ipynb - Main notebook to load data, explore and analyze data, preprocess data, define and train model, and evaluate model
3. P1M2_clarence_manzo_conceptual.txt - A text file to answer given conceptual problems
4. P1M2_clarence_manzo_inf.ipynb - Notebook to test trained model on unseen data
5. README.md - Project description and documentation
6. gb_pipeline.pkl - A serialized end-to-end Gradient Boosting pipeline to predict on raw unseen data
7. url.txt - A text file containing URL to dataset, saved model, and web-app deployment

## Problem Background
Educational institutions struggle to identify which students are likely to underperform before final exam results are known. Inefficient identification of “at-risk” students leads to higher failure rates. Because academic outcomes are influenced by diverse factors, a predictive model is needed to understand how these factors influence final performance. It will help decision-making and early intervention in schools and higher education institutions.

## Project Output
A regression model to estimate student's final grade with Model Deployment on Hugging Face and Python Notebook.

## Data
This dataset is from two publicly available secondary school datasets, which are mathematics course performance and portuguese language course performance. The dataset contains demographic, social, behavioral, and academic attributes of each student.

Column Descriptions:
1. school - student's school (binary: "GP" (Gabriel Pereira), "MS" (Mousinho da Silveira))
2. sex - student's sex (binary: "F" (female), "M" (male))
3. age - student's age (numeric: 15-22)
4. address - student's home address type (binary: "U" (urban), "R" (rural))
5. famsize - family size (binary: "LE3" (less or equal to 3), "GT3" (greater than 3))
6. Pstatus - parent's cohabitation status (binary: "T" (living together), "A" (apart))
7. Medu - mother's education (numeric: 0 (none), 1 (primary education (4th grade)), 2 (5th-9th grade), 3 (secondary education), 4 (higher education))
8. Fedu - father's education (numeric: 0 (none), 1 (primary education (4th grade)), 2 (5th-9th grade), 3 (secondary education), 4 (higher education))
9. Mjob - mother's job (nominal: "teacher", "health", civil "services", "at_home", "other")
10. Fjob - father's job (nominal: "teacher", "health", civil "services", "at_home", "other")
11. reason - reason to choose this school (nominal: close to "home", school "reputation", "course" preference, "other")
12. guardian - student's guardian (nominal: "mother", "father", "other")
13. traveltime - home to school travel time (numeric: 1 (<15 min), 2 (15-30 min), 3 (30 min-1 hour), 4 (>1 hour))
14. studytime - weekly study time (numeric: 1 (<2 hours), 2 (2 to 5 hours), 3 (5 to 10 hours), 4 (>10 hours))
15. failures - number of past class failures (numeric: n if 1<=n<3, else 4)
16. schoolsup - extra educational support (binary: yes/no)
17. famsup - family educational support (binary: yes/no)
18. paid - extra paid classes within the course subject (binary: yes/no)
19. activities - extra-curricular activities (binary: yes/no)
20. nursery - attended nursery school (binary: yes/no)
21. higher - wants to take higher education (binary: yes/no)
22. internet - Internet access at home (binary: yes/no)
23. romantic - with a romantic relationship (binary: yes/no)
24. famrel - quality of family relationships (numeric: 1 (very bad) - 5 (excellent))
25. freetime - free time after school (numeric: 1 (very low) - 5 (very high))
26. goout - going out with friends (numeric: 1 (very low) - 5 (very high))
27. Dalc - weekday alcohol consumption (numeric: 1 (very low) - 5 (very high))
28. Walc - weekend alcohol consumption (numeric: 1 (very low) - 5 (very high))
29. health - current health status (numeric: 1 (very bad) - 5 (very good))
30. absences - number of school absences (numeric)
31. G1 - first period grade (numeric: 0-20)
31. G2 - second period grade (numeric: 0-20)
32. G3 - final grade (numeric: 0-20)

There's a total of 1044 records with no missing values.

## Method
1. Handle outliers: Capping (Winsorizer) with quantile method
2. Feature selection: Spearman & ANOVA F-Tests
3. Feature scaling: Min-Max Scaler
4. Feature encoding: One-Hot Encoding
5. Machine Learning Models: K-Nearest Neighbors (KNN), Support Vector Machine (SVM), Decision Tree, Random Forest, and Gradient Boosting
6. Training Methods: Cross-Validation & GridSearchCV
7. Evaluation metrics: MAE (Mean Absolute Error), RMSE (Root Mean Squared Error), MAPE (Mean Absolute Percentage Error), and R² Score

## Stacks
Programming langugage: Python

Tools: Visual Studio Code and Hugging Face

Library: pandas, numpy, scipy, matplotlib, seaborn, pickle, scikit-learn, scipy, feature_engine, imblearn

## Reference
Dataset URL: https://archive.ics.uci.edu/dataset/320/student+performance

Model URL: https://drive.google.com/file/d/1RsPBppEOOl0K65YLUu36Tqv9jnP9YurR/view?usp=sharing

Hugging Face URL: https://huggingface.co/spaces/clarencemanzo/P1M2_clarence_manzo

