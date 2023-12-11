import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from scipy.stats import ttest_ind

st.title("Age and Gender Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("**Select your data**", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding="windows-1251")

    # Preparation
    data[["work_days", "age", "gender"]] = data[
        'Количество больничных дней,"Возраст","Пол"'
    ].str.split(",", expand=True)
    data["work_days"] = data["work_days"].astype(int)
    data["age"] = data["age"].astype(int)
    data["gender"] = data["gender"].replace(['"М"', '"Ж"'], ["m", "f"])
    data.drop(['Количество больничных дней,"Возраст","Пол"'], axis=1, inplace=True)

    # Sliders
    st.write("## Select Data Ranges")

    age_threshold_range = st.slider(
        "Select Age Threshold Range",
        min_value=data.age.min(),
        max_value=data.age.max(),
        value=(data.age.min(), data.age.max()),
    )

    work_days_threshold_range = st.slider(
        "Select Work Days Threshold Range",
        min_value=data.work_days.min(),
        max_value=data.work_days.max(),
        value=(data.work_days.min(), data.work_days.max()),
    )

    st.write("## Select Age Threshold and p-value")

    age_threshold = st.slider(
        "Select Age Threshold",
        min_value=data.age.min(),
        max_value=data.age.max(),
        value=35,
    )

    pvalue_threshold = st.slider(
        "Select p-value",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
    )

    # Filtering data based on user input
    filtered_data = data[
        (data["age"] >= age_threshold_range[0])
        & (data["age"] <= age_threshold_range[1])
        & (data["work_days"] >= work_days_threshold_range[0])
        & (data["work_days"] <= work_days_threshold_range[1])
    ]

    # Men vs Women
    men_group = filtered_data[filtered_data["gender"] == "m"]
    women_group = filtered_data[filtered_data["gender"] == "f"]

    # Older vs Younger
    older_group = filtered_data[filtered_data["age"] >= age_threshold]
    younger_group = filtered_data[filtered_data["age"] < age_threshold]

    bins = age_threshold_range[1] - age_threshold_range[0]

    st.write("## Data Visualization")

    # Gender distribution
    fig, ax = plt.subplots()
    men_group["work_days"].hist(
        alpha=0.5, label="Men", bins=bins, width=0.7, align="mid"
    )
    women_group["work_days"].hist(
        alpha=0.5, label="Women", bins=bins, width=0.7, align="mid"
    )
    plt.title("Distribution of Sick Days by Gender")
    plt.xlabel("Sick Days")
    plt.ylabel("Frequency")
    plt.legend()
    st.pyplot(fig)

    st.write(
        f"H0: Мужчины пропускают в течение года более 2 рабочих дней       (work_days) по болезни так же часто, как и женщины.\n\nH1: Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин."
    )

    st.write(
        f"Уровень значимости α = {pvalue_threshold} \n\n Статистический критерий: t-критерий Стьюдента для независимых выборок."
    )

    ttest_result_gender = ttest_ind(
        men_group["work_days"], women_group["work_days"], equal_var=False
    )

    st.write(
        f"Значение p-value : {ttest_result_gender.pvalue} {'<' if ttest_result_gender.pvalue < pvalue_threshold else '>'} α"
    )

    if ttest_result_gender.pvalue < pvalue_threshold:
        st.write(
            "Гипотеза H0 отвергается в пользу H1. Различия в пропусках по болезни между мужчинами и женщинами являются статистически значимыми."
        )
    else:
        st.write(
            "Принимается гипотеза H0. Различия в пропусках по болезни между мужчинами и женщинами не являются статистически значимыми."
        )

    # Age distribution
    fig, ax = plt.subplots()
    older_group["work_days"].hist(
        alpha=0.5, label=f"Age {age_threshold}+", bins=bins, width=0.7, align="mid"
    )
    younger_group["work_days"].hist(
        alpha=0.5, label=f"Age < {age_threshold}", bins=bins, width=0.7, align="mid"
    )
    plt.title("Distribution of Sick Days by Age")
    plt.xlabel("Sick Days")
    plt.ylabel("Frequency")
    plt.legend()
    st.pyplot(fig)

    st.write(
        f"H0: Работники старше {age_threshold} лет пропускают в течение года более 2 рабочих дней (work_days) по болезни так же часто, как и молодые.\n\nH1: Работники старше {age_threshold} лет пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще молодых."
    )

    ttest_result_age = ttest_ind(
        older_group["work_days"], younger_group["work_days"], equal_var=False
    )

    st.write(
        f"Уровень значимости α = {pvalue_threshold}. \n\n Статистический критерий: t-критерий Стьюдента для независимых выборок."
    )

    st.write(
        f"Значение p-value : {ttest_result_age.pvalue} {'<' if ttest_result_age.pvalue < pvalue_threshold else '>'} α"
    )

    if ttest_result_age.pvalue < pvalue_threshold:
        st.write(
            f"Гипотеза H0 отвергается в пользу H1. Различия в пропусках по болезни между работниками старше {age_threshold} лет и молодыми являются статистически значимыми."
        )
    else:
        st.write(
            f"Принимается гипотеза H0. Различия в пропусках по болезни между работниками старше {age_threshold} лет и молодыми не являются статистически значимыми."
        )
