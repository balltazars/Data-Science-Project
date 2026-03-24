import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image

def run():
    # Introduction
    st.title("Predicting Student Academic Performance and Identifying Key Success Factors")
    st.subheader("Exploratory Data Analysis (EDA)")
    st.markdown("---")

    # Identity
    st.write('Name : Clarence Manzo')
    st.write('Batch: 036')

    # Display image
    image = Image.open('./src/img.webp')
    st.image(image, caption = 'Final Examination')
    
    # Load both datasets and combine into one dataframe
    df_mat = pd.read_csv("./src/student-mat.csv", sep=";", quotechar='"')
    df_por = pd.read_csv("./src/student-por.csv", sep=";", quotechar='"')
    df = pd.concat([df_mat, df_por], ignore_index=True)

    # Display dataset
    st.write('# Dataset')
    st.dataframe(df)

    # EDA 1 ------------------------------------------------------------------------------------------------------
    st.write('## 1. Does study time significantly impact students’ final performance?')

    # Plot Boxplot
    fig = plt.figure(figsize=(8,6))
    sns.boxplot(data=df, x="studytime", y="G3")
    plt.title("Final Grade (G3) Distribution by Weekly Study Time")
    plt.xticks([0,1,2,3],["<2 hours", "2 to 5 hours", "5 to 10 hours", ">10 hours"])
    plt.xlabel("Study Time")
    plt.ylabel("Final Grade")
    st.pyplot(fig)

    # Analysis
    st.write('It shows that students who dedicate more weekly study time achieve higher final grades,' \
    'with the strongest performance observed in the 5–10 hour range. However, the highest study-time group resulting' \
    'decreases in final grades. The wide overlap across categories indicates that study time alone does not determine' \
    'academic success and should be analyzed alongside other factors.')

    # EDA 2 ------------------------------------------------------------------------------------------------------
    st.write('## 2. How does absence affect final academic performance?')

    # Plot Scatterplot
    fig = plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x="absences", y="G3", alpha=0.5)
    plt.title("Impact of Absences on Final Grade (G3)")
    plt.xlabel("Absences")
    plt.ylabel("Final Grade")
    st.pyplot(fig)

    # Analysis
    st.write('The scatterplot reveals that low absence does not guarantee high performance and high absence almost guarantees ' \
    'poor outcomes. This shows that attendance is quiete an influential predictor of student\'s final grade.')

    # EDA 3 ------------------------------------------------------------------------------------------------------
    st.write('## 3. Do students with past academic failures perform worse in the final exam?')

    # Plot Stacked Histrogram
    fig = plt.figure(figsize=(9,5))
    sns.histplot(data=df, x="G3", hue="failures", bins=20, multiple="stack")
    plt.title("Final Grade Distribution by Number of Past Failures")
    plt.xlabel("Final Grade")
    plt.ylabel("Number of Students")
    st.pyplot(fig)
    
    # Analysis
    st.write('The histogram reveals that students without prior failures consistently achieve higher and more variable final grades, ' \
    'while students with multiple failures have lower final grades. This indicates that past failures is a critical feature for ' \
    'predicting student\'s performance.')

    # EDA 4 ------------------------------------------------------------------------------------------------------
    st.write('## 4. How do social activity levels relate to academic outcomes?')

    # Average final grade by each social activity category
    goout_mean = df.groupby("goout")["G3"].mean()
    freetime_mean = df.groupby("freetime")["G3"].mean()

    # Ensure same x-axis levels (1–5) and get the value from each level
    levels = sorted(set(goout_mean.index).union(freetime_mean.index))
    goout_vals = [goout_mean.get(l, np.nan) for l in levels]
    freetime_vals = [freetime_mean.get(l, np.nan) for l in levels]

    x = np.arange(len(levels))

    # Plot Grouped Bar Chart
    fig = plt.figure(figsize=(9,5))
    plt.bar(x - 0.35/2, goout_vals, 0.35, label="Going Out")
    plt.bar(x + 0.35/2, freetime_vals, 0.35, label="Free Time")
    plt.xticks(x, levels)
    plt.xlabel("Activity Level")
    plt.ylabel("Average Final Grade")
    plt.title("Average Final Grade by Social Activity Level")
    plt.legend()
    st.pyplot(fig)

    # Analysis
    st.write('Students with moderate levels of going-out and free-time achieve higher final grades in average. ' \
    'However, excessive or minimal social activity makes students to achieve a lower final grade average. ' \
    'This conclude that balance is key for achieving higher student\'s performance rather than restriction.')

    # EDA 5 ------------------------------------------------------------------------------------------------------
    st.write('## 5. Do parents\' education level affects students academic performance?')

    # Average final grade by mother's and father's education level
    edu_means = df.groupby(["Medu", "Fedu"])["G3"].mean().reset_index()

    # Plot Grouped Bar Chart
    fig = plt.figure(figsize=(9,5))
    sns.barplot(data=edu_means, x="Medu", y="G3", hue="Fedu")
    plt.title("Average Final Grade by Parents' Education Level")
    plt.xlabel("Mother’s Education Level")
    plt.ylabel("Final Grade")
    plt.legend(title="Father’s Education Level")
    st.pyplot(fig)

    # Analysis
    st.write('The analysis shows that mother\'s education level have a more consistent effect towards student\'s final grade. ' \
    'Father\'s education level improves student\'s performance when combined with higher mother\'s education level. ' \
    'These findings prove that parental educational background have a significant impact on student\'s academic performance.')

    # EDA 6 ------------------------------------------------------------------------------------------------------
    st.write('## 6. Is there any academic performance difference between gender?')

    # Plot Boxplots
    fig = plt.figure(figsize=(7,5))
    sns.boxplot(data=df, x="sex", y="G3")
    plt.title("Final Grade Distribution by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Final Grade")
    st.pyplot(fig)

    # Analysis
    st.write('The boxplot shows the median grade for females is slightly higher compared to males which indicates a typical ' \
    'performance for female students. Both gender spanning from approximately 10 to 14 which indicates that student\'s final grade '
    'is consistent across genders. Therefore, gender is not a significant predictor for student\'s performance.')

    # EDA 7 ------------------------------------------------------------------------------------------------------
    st.write('## 7. Does the primary guardian influence students\' academic performance?')

    # Plot Boxplots
    fig = plt.figure(figsize=(8,5))
    sns.boxplot(data=df, x="guardian", y="G3")
    plt.title("Final Grade (G3) by Primary Guardian")
    plt.xlabel("Guardian")
    plt.ylabel("Final Grade (G3)")
    st.pyplot(fig)

    # Analysis
    st.write('Students with a father as their primary guardian have the highest median final grade, while students with mother or other ' \
    'guardians show a slightly lower and identical median grade at around 11. All three categories have outliers at the bottom which ' \
    'tell that a small group of students is significantly underperforming regardless of the guardian.')

    # Footer
    st.markdown("---")
    st.markdown("Exploratory Data Analysis Dashboard – Clarence Manzo")

if __name__ == "__main__":
    run()