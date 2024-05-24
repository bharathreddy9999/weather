#importing all the required modules 
import streamlit as st
import pyowm
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
import pytz
import statistics
import matplotlib
# OpenWeatherMap API key
api_key = '73f8ab4c93851f9bfcb07104b6e49efd'
owm = pyowm.OWM(api_key)
mgr = owm.weather_manager()
# Streamlit app layout
st.title("5 Day Weather Forecast")
# User input
place = st.text_input("NAME OF THE CITY :", "")
unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

if place:
    # Get the 5-day weather forecast for the specified city
    try:
        forecast = mgr.forecast_at_place(place, '3h')
        forecast_data = forecast.forecast
    except pyowm.commons.exceptions.NotFoundError:
        st.error("City not found. Please enter a valid city name.")
        forecast_data = None

    if forecast_data:
        dates_list = []
        temps = []

        for weather in forecast_data:
            local_time = weather.reference_time('date').astimezone(pytz.timezone('Etc/UTC'))
            if unit == "Celsius":
                temp = weather.temperature('celsius')["temp"]
            else:
                temp = weather.temperature('fahrenheit')["temp"]

            dates_list.append(local_time)
            temps.append(temp)

        # Plotting
        fig, ax = plt.subplots()
        if g_type == "Line Graph":
            ax.plot(dates_list, temps, label='Temperature')
        elif g_type == "Bar Graph":
            ax.bar(dates_list, temps, label='Temperature',width=0.2)

        # Formatting the plot
        ax.set_xlabel('Date')
        ax.set_ylabel(f'Temperature ({unit})')
        ax.set_title(f'5-Day Weather Forecast for {place}')
        ax.legend()
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M', tz=pytz.timezone('Etc/UTC')))
        fig.autofmt_xdate()

        # Display the plot in Streamlit
        st.pyplot(fig)
        st.text(f'Highest temperature recorded in last 5 days: {max(temps)}')
        avg=statistics.mean(temps)
        if avg>=36 or avg>=97:
            st.title("High temperature alert! Please take necessary precautions!")
        else:
            st.title("MODERATE!")
else:
    st.write("Input a CITY!")
#footer element
footer_html = """<div style='text-align: center;'>
  <p>Developed with ❤️ by Bharath</p>
  <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAApVBMVEX////ox8j89/e5Ky//1tbIa2y7OTzi19f/S0vkvb29QEONVFj/vb3/CQn/AAD/YWH/4uLq4uOXZmpxFB5zHCXQvb7/Kyv/ISH/cnL/6+vx7Oyhdnl5LTN9NTv/fn7/Hh6qhoj/EhLnMjS7QEN8Ji3/Pz/jODq1QER8MjiEREn/rq7/FxfaOz2ePULFra//eXn8Li/RPkD2MjLwAAD/xMT/mpr/iopqCY8wAAAA00lEQVR4AdXO1Q3DUABDUYc5ZWaGMO4/Wh+V2wFyf49kGQ1Okv6brCgyXlPxTNN1Dc8MmOaDLcW2FetBjgPX81ttMWqTxHCn2+sPAH848scTNkqRDU9nvfmiB2C5GhJeymSUpVjymtBiviao+kPSarO1d1z1/XxB6hsgHYai447zidr5Ato1GN4LOUcE9zFDmew++USZYE8GKxm9aJoRPi3mM/BUT8CD7YjcEaXD9/Jsd8Y91/e9TbBajUirVbDx/MLCs4laXqt6mSTLurqW6gQN7AYfFRhollEAsQAAAABJRU5ErkJggg==" />
  <span>&copy;<span>2024 May 24
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)
