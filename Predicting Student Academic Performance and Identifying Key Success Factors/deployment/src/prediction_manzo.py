import pandas as pd
import pickle
import streamlit as st

# Load the best Gradient Boosting Regressor Model
gb = pickle.load(open('./src/gb_pipeline.pkl', 'rb'))

def run():
    with st.form('form_student'):
        school = st.selectbox('School (Gabriel Pereira/Mousinho da Silveira)', ('GP', 'MS'), index=0)
        sex = st.selectbox('Sex (Male/Female)', ('M', 'F'), index=0)
        age = st.number_input('Age (10-30)', min_value=10, max_value=30, value=17, help='Input student\'s age')
        address = st.selectbox('Address (Urban/Rural)', ('U', 'R'), index=0)
        famsize = st.selectbox('Family size (Less or Equal to 3/Greater than 3)', ('LE3', 'GT3'), index=0)
        Pstatus = st.selectbox('Parent\'s cohabitation status (Living together/Apart)', ('T', 'A'), index=0)
        Medu = st.slider('Mother\'s education (0: none, 1: primary education (4th grade), 2: 5th-9th grade, 3: secondary education, 4: higher education)', 0, 4, 0)
        Fedu = st.slider('Father\'s education (0: none, 1: primary education (4th grade), 2: 5th-9th grade, 3: secondary education, 4: higher education)', 0, 4, 0)
        Mjob = st.selectbox('Mother\'s job', ('teacher', 'health', 'services', 'at_home', 'other'), index=0)
        Fjob = st.selectbox('Father\'s job', ('teacher', 'health', 'services', 'at_home', 'other'), index=0)
        reason = st.selectbox('Reason to choose this school', ('home', 'reputation', 'course', 'other'), index=0)
        guardian = st.selectbox('Student\'s guardian', ('mother', 'father', 'other'), index=0)
        traveltime = st.slider('Home to school travel time (1: <15 min, 2: 15-30 min, 3: 30 min-1 hour, 4: >1 hour)', 1, 4, 1)
        studytime = st.slider('Weekly study time (1: <2 hours, 2: 2-5 hours, 3: 5-10 hours, 4: >10 hours)', 1, 4, 1)
        failures = st.slider('Number of past class failures (0: n=0, 1: n=1, 2: n=2, 3: n=3, 4: n>3)', 0, 4, 1)
        schoolsup = st.selectbox('Extra educational support', ('yes', 'no'), index=0)
        famsup = st.selectbox('Family educational support', ('yes', 'no'), index=0)
        paid = st.selectbox('Extra paid classes within the course subject', ('yes', 'no'), index=0)
        activities = st.selectbox('Extra-curricular activities', ('yes', 'no'), index=0)
        nursery = st.selectbox('Attended nursery school', ('yes', 'no'), index=0)
        higher = st.selectbox('Wants to take higher education', ('yes', 'no'), index=0)
        internet = st.selectbox('Internet access at home', ('yes', 'no'), index=0)
        romantic = st.selectbox('With a romantic relationship', ('yes', 'no'), index=0)
        famrel = st.number_input('Quality of family relationships (1-5)', min_value=1, max_value=5, value=3, help='1 (very bad) - 5 (excellent)')
        freetime = st.number_input('Free time after school (1-5)', min_value=1, max_value=5, value=3, help='1 (very low) - 5 (very high)')
        goout = st.number_input('Going out with friends (1-5)', min_value=1, max_value=5, value=3, help='1 (very low) - 5 (very high)')
        Dalc = st.number_input('Weekday alcohol consumption (1-5)', min_value=1, max_value=5, value=3, help='1 (very low) - 5 (very high)')
        Walc = st.number_input('Weekend alcohol consumption (1-5)', min_value=1, max_value=5, value=3, help='1 (very low) - 5 (very high)')
        health = st.number_input('Current health status (1-5)', min_value=1, max_value=5, value=3, help='1 (very bad) - 5 (very good)')
        absences = st.number_input('Number of school absences (0-100)', min_value=0, max_value=100, value=0, help='Input number of absences')
        G1 = st.slider('First period grade (G1)', 0, 20, 10)
        G2 = st.slider('Second period grade (G2)', 0, 20, 10)

        submitted = st.form_submit_button('Predict')

    data_inf = pd.DataFrame([{
        'school': school,
        'sex': sex,
        'age': age,
        'address': address,
        'famsize': famsize,
        'Pstatus': Pstatus,
        'Medu': Medu,
        'Fedu': Fedu,
        'Mjob': Mjob,
        'Fjob': Fjob,
        'reason': reason,
        'guardian': guardian,
        'traveltime': traveltime,
        'studytime': studytime,
        'failures': failures,
        'schoolsup': schoolsup,
        'famsup': famsup,
        'paid': paid,
        'activities': activities,
        'nursery': nursery,
        'higher': higher,
        'internet': internet,
        'romantic': romantic,
        'famrel': famrel,
        'freetime': freetime,
        'goout': goout,
        'Dalc': Dalc,
        'Walc': Walc,
        'health': health,
        'absences': absences,
        'G1': G1,
        'G2': G2
    }])
    st.dataframe(data_inf)
  
    if submitted: 
        # Predict final grade (G3)
        prediction = gb.predict(data_inf)

        st.write('Predicted final grade (G3):', str(int(prediction)))

if __name__ == '__main__':
  run()