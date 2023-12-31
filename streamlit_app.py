import requests
import streamlit as st
import pandas as pd
import json

st.title('Credit accordance prediction')
df = pd.read_csv("test_dataframe.csv")
list_index = df.index


def get_age(new_index):
    days_birth = df.iloc[new_index]['DAYS_BIRTH']
    age = int(days_birth/365)
    return -age


def get_days_employer(new_index):
    days_employed = df.iloc[new_index]['DAYS_EMPLOYED']
    return -int(days_employed)


def get_children(new_index):
    return int(df.iloc[new_index]['CNT_CHILDREN'])


def get_gender(new_index):
    if df.iloc[new_index]['CODE_GENDER'] == 0:
        return 'male'
    return 'female'


def get_total_income(new_index):
    return df.iloc[new_index]['AMT_INCOME_TOTAL']


def get_credit(new_index):
    return df.iloc[new_index]['AMT_CREDIT']


def get_education(new_index):
    if df.iloc[new_index]['NAME_EDUCATION_TYPE_Highereducation'] == 1:
        return 'yes'
    return 'no'


def is_married(new_index):
    if df.iloc[new_index]['NAME_FAMILY_STATUS_Married'] == 1:
        return 'yes'
    return 'no'



def get_credit_proba(index = 0):
    # Our API ENDPoint
    url = "https://obscure-taiga-00950-2103a4620388.herokuapp.com/api/credit/"
    #url = "http://192.168.1.89:5000/api/credit"
    #url = "http://0.0.0.0:5001/api/credit"
    test_param_2 = df.iloc[index].to_dict()
    response = requests.post(url, json=json.dumps(test_param_2))
    response_json= response.json()
    return f'''**Credit should be granted:** :orange[{str(response_json['credit_granted'])}].  \n**Found with a probability to be able to pay of:** :orange[{str(response_json['probability'])}].  \n**The treshold being:** :orange[{str(response_json['credit_proba_limit'])}]'''


add_selectbox = st.sidebar.selectbox('label',
                                     list_index,
                                     index=0,
                                     key=None,
                                     help=None,
                                     args=None,
                                     kwargs=None,
                                     placeholder="Choose an option",
                                     disabled=False,
                                     label_visibility="visible")


add_age = st.sidebar.markdown(f'''**Age:** {str(get_age(add_selectbox))}''')

add_gender = st.sidebar.markdown(f'''**Gender:** {str(get_gender(add_selectbox))}''')

add_days_employed = st.sidebar.markdown(f'''**Days employed:** {str(get_days_employer(add_selectbox))}''')

add_children = st.sidebar.markdown(f'''**Children:** {str(get_children(add_selectbox))}''')

add_total_income = st.sidebar.markdown(f'''**Total income:** {str(get_total_income(add_selectbox))}''')

add_credit = st.sidebar.markdown(f'''**Credit:** {str(get_credit(add_selectbox))}''')

add_education = st.sidebar.markdown(f'''**Has higher education:** {str(get_education(add_selectbox))}''')

add_married = st.sidebar.markdown(f'''**Is married:** {str(is_married(add_selectbox))}''')

add_result_credit_granted = st.markdown(str(get_credit_proba(add_selectbox)))






