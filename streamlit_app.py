import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def bayes_disease_test(P_disease = 0.1, P_positive_acc = 0.85, P_negative_acc = 0.98, n_tests = 1):
    prob_covid_positive_test = P_positive_acc * P_disease / (P_positive_acc * P_disease + (1 - P_negative_acc )* (1 - P_disease))
    prob_covid_negative_test = (1 - P_positive_acc) * P_disease / ((1 - P_positive_acc) * P_disease + P_negative_acc * (1 - P_disease))
    return P_disease, prob_covid_positive_test, prob_covid_negative_test, P_positive_acc, P_negative_acc


def plot_function(df, cols, title = None, alpha=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df['P_disease_pre_test'], y = df['P_disease_pre_test'],
                        mode='lines',
                        name='Pre-Test'))
    fig.add_trace(go.Scatter(x = df['P_disease_pre_test'], y = df['prob_covid_given_positive_test'],
                        mode='lines+markers',
                        name='Post-Positive-Test (PPV)'))
    fig.add_trace(go.Scatter(x = df['P_disease_pre_test'], y = df['prob_covid_given_negative_test'],
                        mode='lines+markers',
                        name='Post-Negative-Test (1 - NPV)'))
    
    fig.update_layout(title = title, xaxis_title='Pre-Test probability <br> that you have disease',
                      yaxis_title= 'Post-Test probability <br> that you have disease', 
                      #autosize=True, #height = 600, 
                      font=dict(family="Courier New, monospace", size=16,color="White"), margin=dict(t=30, b=0, l=0, r=0)) #
    fig.update_layout(hovermode="x unified")
    fig.update_layout(legend=dict(
                        yanchor="top",
                        y=1.2,
                        xanchor="left",
                        x=0.01
                          ))
    return fig

st.title('Post Probability vs. prior probability based on given Sensitivity and Specificity numbers. (For 1 test)')

st.text('You can change the Sensitivity and Specificity numbers in the graph below.')
    
pre_test_prob = list(np.linspace(0, 1, 100))
P_positive_acc = st.slider(label = 'Sensitivity %', min_value=0, max_value=100, value=85, step=1) /100
P_negative_acc =  st.slider(label = 'Specificity %', min_value=0, max_value=100, value=98, step=1) /100

probs = [bayes_disease_test(P_disease = p_disease, P_positive_acc=P_positive_acc, P_negative_acc=P_negative_acc) for p_disease in pre_test_prob]

probs_df = pd.DataFrame(probs, columns = ['P_disease_pre_test', 'prob_covid_given_positive_test', 'prob_covid_given_negative_test', 'P_positive_acc', 'P_negative_acc'])

# Plot!
st.plotly_chart(plot_function(probs_df, cols = ['P_disease_pre_test', 'prob_covid_given_positive_test']), use_container_width=True)

st.markdown(r"____")
st.subheader("Notes")
st.markdown(r"* __Sensitivity__: the ability of a test to correctly identify patients with a disease. It is given by, \
$\dfrac{TP}{TP + FN}$")
st.markdown(r"* __Specificity__: the ability of a test to correctly identify people without the disease. It is given by, \
$\dfrac{TN}{TN + FP}$")
st.markdown(r"where,")
st.markdown(r"* TP: True positives --> Number of people who have the disease and were correctly tested positive by the test.")
st.markdown(r"* FP: False positives --> Number of people who don't have the disease, but were incorrectly tested positive by the test.")
st.markdown(r"* TN: True negatives --> Number of people who don't have the disease, and were correctly tested negative by the test.")
st.markdown(r"* FN: False negatives --> Number of people who have the disease but were incorrectly tested negative by the test.")
st.text("")
st.markdown(r"____")

st.markdown("* __${Positive\ Predictive\ Value}$__ (the value plotted on the y-axis above as Post Positive Test)")
st.markdown(r"is the probability that a person who has a positive test result most likely has the infection. We will have more confidence in a positive test if this value is higher. Pretest probability and test specificity have the greatest impact on false-positive rates. As the pretest probability and the specificity of the test increases, the false-positive rate decreases and the positive predictive value increases.")

st.markdown("* __${Negative\ Predictive\ Value}$__ (1 minus the value plotted on the y-axis above as Post Negative Test)")
st.markdown(r"is the probability that a person who has a negative test result most likely does not have the infection. We will have more confidence in a negative test if this value is higher (that is, the plotted value in green is lower). Pretest probability and test sensitivity have the greatest impact on false-negative rates. As the pretest probability decreases, the false-negative rate decreases and the negative predictive value increases. As the sensitivity of the test increases, the false-negative rate decreases and the negative predictive value increases.")

st.markdown(r"* If a disease is rare, the probability that a test result reflects the patient’s true disease state may still be low, even with a really good test.") 
