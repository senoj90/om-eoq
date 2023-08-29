import os
import sys
import time
import random
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go

title = "Fun with EOQ"

# footer text
footer_txt = '<div style="text-align: center"> &copy Koh Niak Wu, Ph.D.</div>'

st.set_page_config(
    page_title = "Operations Management",
    page_icon = '✅',
    layout = 'wide'
)


st.sidebar.title("About")
st.sidebar.subheader("Dr Koh Niak Wu's attempt to spice up his Operations Management classes")

st.sidebar.subheader("Enquiries: nwkoh@smu.edu.sg")


# dashboard title
st.title(title)

# EOQ = sqrt(2 * K * R / h)
K = st.slider('What is your setup or ordering cost ($)?', 1, 1000, 500)
R = st.slider('What is your average demand per year?', 1000, 5000, 3000)
h = st.slider('What is your holding cost per unit ($)?', 1, 20, 10)

# to introduce randomness
std = st.slider('Standard deviation in demand (%)', 0, 60, 0)

EOQ = (2 * K * R / h)**0.5
st.markdown(f"#### EOQ = {round(EOQ, 2)}")
avg_inv = EOQ / 2
st.markdown(f"#### Average inventory = {round(avg_inv, 2)}")
turns = R / EOQ
st.markdown(f"#### Inventory turns = {round(turns, 2)}")
cycle_time = EOQ / R * 12
st.markdown(f"#### Cycle time (months) = {round(cycle_time, 2)}")
cycle_time = EOQ / R * 365
st.markdown(f"#### Cycle time (days) = {int(cycle_time)}")

NUM_DAYS = 365
demand_per_day = round(R / NUM_DAYS, 2)

start_sim = st.button('Start')
stop_sim = st.button('Stop')

if stop_sim:
    placeholder = st.empty()

if start_sim:
    placeholder = st.empty()

    # near real-time / live feed simulation
    x = [0]
    y = [EOQ]

    for seconds in range(0, NUM_DAYS):
        if stop_sim:
            break

        with placeholder.container():

            # for figures
            fig = make_subplots(rows=1, cols=1)
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="inventory"), row=1, col=1)

            st.write(fig)

            demand_per_day = demand_per_day * (1 + random.uniform(-std/100, std/100))

            inv = y[-1] - demand_per_day
            if inv <= 0:
                inv = 0

            if seconds != 0 and not seconds % int(cycle_time):
                inv = [EOQ + inv, EOQ - demand_per_day]
                x_val = [seconds, seconds + 1]
                x.extend(x_val)
                y.extend(inv)
            else:
                x_val = seconds + 1
                x.append(x_val)
                y.append(inv)

            st.caption(footer_txt, unsafe_allow_html=True)

            time.sleep(1)
