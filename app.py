import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title(" Air Quality Visualizer")

# # User input
city = st.text_input("Enter city name", "Delhi")

# # Fetch AQI data from OpenAQ API
# if st.button("Get AQI Data"):
#     url = f"https://api.openaq.org/v2/latest?city={city}"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         if data['results']:
#             measurements = data['results'][0]['measurements']
#             st.subheader(f"Air Quality in {city}")
            
#             # Show as chart
#             labels = [item['parameter'] for item in measurements]
#             values = [item['value'] for item in measurements]
            
#             fig, ax = plt.subplots()
#             ax.bar(labels, values)
#             ax.set_ylabel("Concentration (µg/m³)")
#             st.pyplot(fig)
#         else:
#             st.error("No data available for this city.")
#     else:
#         st.error("Failed to fetch data.")


# if st.button("Get AQI Data"):
#     api_key = "127dd1ddbdaa876c5a9756fe4a47d8d0"
#     geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
#     geo_res = requests.get(geocode_url).json()

#     # Debug print to see what you're getting from API
#     st.write("Geocode API response:", geo_res)

#     if geo_res and isinstance(geo_res, list) and len(geo_res) > 0:
#         # Get latitude and longitude safely
#         location = geo_res[0]
#         lat = location.get("lat")
#         lon = location.get("lon")

#         if lat is None or lon is None:
#             st.error("Could not extract latitude or longitude.")
#         else:
#             st.write(f"Latitude: {lat}, Longitude: {lon}")

#             # Proceed to get AQI
#             aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
#             aqi_res = requests.get(aqi_url).json()

#             if "list" in aqi_res and len(aqi_res["list"]) > 0:
#                 aqi = aqi_res["list"][0]["main"]["aqi"]
#                 meaning = ["Good 😊", "Fair 🙂", "Moderate 😐", "Poor 😷", "Very Poor 🛑"]

#                 st.subheader(f"Air Quality Index (AQI) in {city}:")
#                 st.metric("AQI", aqi, meaning[aqi - 1])
#             else:
#                 st.error("Failed to fetch AQI data.")
#     else:
#         st.error("City not found or invalid response.")


import requests
import streamlit as st
import pandas as pd

st.title(" Air Quality Visualizer")
city = st.text_input("Enter city name")

if st.button("Get AQI Data"):
    api_key = "127dd1ddbdaa876c5a9756fe4a47d8d0"

    #  Get coordinates
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_res = requests.get(geocode_url).json()

    if geo_res and isinstance(geo_res, list) and len(geo_res) > 0:
        lat = geo_res[0]["lat"]
        lon = geo_res[0]["lon"]

        #  Get AQI and components
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        aqi_res = requests.get(aqi_url).json()

        if "list" in aqi_res and len(aqi_res["list"]) > 0:
            aqi = aqi_res["list"][0]["main"]["aqi"]
            components = aqi_res["list"][0]["components"]

            meaning = ["Good 😊", "Fair 🙂", "Moderate 😐", "Poor 😷", "Very Poor 🛑"]

            suggestions = {
                        1: "✅ It's a great day to be outdoors!",
                        2: "🙂 Air quality is okay. Sensitive individuals should monitor their symptoms.",
                        3: "😐 Consider limiting prolonged outdoor exertion.",
                        4: "⚠️ Avoid outdoor activities if you have breathing issues or are in a vulnerable group.",
                        5: "🚫 Stay indoors! Use masks and air purifiers if available."
                          }

            st.subheader(f"Air Quality Index (AQI) in {city}:")
            st.metric("AQI", aqi, meaning[aqi - 1])
            st.info(f"AQI Category: {meaning[aqi - 1]}")
            st.warning(f"Suggestion: {suggestions[aqi]}")

            st.subheader("📍 Location on Map")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

            #  Show pollutant values in chart
            st.subheader("📊 Pollutant Concentrations (μg/m³)")
            df = pd.DataFrame(components.items(), columns=["Pollutant", "Value"])
            df = df.sort_values(by="Value", ascending=False)
            st.bar_chart(df.set_index("Pollutant"))

            # 📝 Create a downloadable CSV
            csv_data = pd.DataFrame(components.items(), columns=["Pollutant", "Value"])
            csv = csv_data.to_csv(index=False).encode("utf-8")

            st.download_button(
            label="📥 Download Pollutant Data as CSV",
            data=csv,
            file_name=f"AQI_Pollutants_{city}.csv",
            mime="text/csv"
             )     


        else:
            st.error("Failed to fetch AQI data.")
    else:
        st.error("City not found or invalid response.")

