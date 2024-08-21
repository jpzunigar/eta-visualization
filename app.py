import streamlit as st
import leafmap.maplibregl as leafmap
import geopandas as gpd
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
data_eta = './data/suertes_eta.geojson'

# Load the GeoJSON data with GeoPandas
gdf = gpd.read_file(data_eta)

# Calculate the centroid of the GeoJSON
centroid = gdf.geometry.centroid[0]
centroid_lat, centroid_lon = centroid.y, centroid.x

# Calculate quantiles
quantiles = gdf['_mean'].quantile([0, 0.25, 0.5, 0.75, 1.0]).values

# Define the colors for the stops using hex codes
colors = ["#808080", "#FFFF00", "#FFA500", "#8B0000", "#ADD8E6"]

# Create a function to assign colors based on quantiles


def assign_color(value):
    if value <= quantiles[1]:
        return colors[0]
    elif value <= quantiles[2]:
        return colors[1]
    elif value <= quantiles[3]:
        return colors[2]
    elif value <= quantiles[4]:
        return colors[3]
    else:
        return colors[4]


# Apply the function to the column and create the 'color' column
gdf['color'] = gdf['_mean'].apply(assign_color)

with st.sidebar:
    st.title("About")
    st.write(
        """
        Welcome to the ETa Visualization App for Sugar Cane Fields,
        a tool designed to provide insightful visualizations
        of actual evapotranspiration (ETa) data across sugar cane 
        plantations. This app allows users to easily analyze ETa patterns, 
        assess water usage efficiency, and make data-driven decisions to 
        optimize irrigation practices.
        """
    )
    st.header("Actual evapotranspiration")
    st.write(
        """
        ETa, or actual evapotranspiration, is the amount of water that is transferred from the land to the atmosphere
        through processes of evaporation (from soil and water surfaces) and transpiration (from plants).
        In agricultural contexts, ETa is a critical measure of water usage efficiency, 
        as it reflects how much water is being used by crops like sugar cane. 
        Monitoring ETa helps farmers and agronomists optimize irrigation practices, 
        ensuring that crops receive the right amount of water without wastage.
        """)
    st.header("Contact information")
    st.write(
        """
        **Juan Pablo Zuñiga**
        - Email: jpzuniga@cenicana.org

        **Julian David Ome Narvaez**
        - Email: jdome@cenicana.org

        **Alberto Mario Arroyo **
        - Email: amarroyo@cenicana.org

        """
    )


st.title("ETa visualization on sugarcane Field")
st.write("")
st.write("")

if "basemap" not in st.session_state:
    st.session_state.basemap = "Esri.WorldImagery"

options = list(leafmap.basemaps.keys())

# Create a DataFrame for Altair with quantile bins
gdf['quantile_bin'] = pd.cut(
    gdf['_mean'],
    bins=[-float("inf"), *quantiles[1:], float("inf")],
    labels=["Very Low ETa", "Low ETa",
            "Moderate ETa", "High ETa", "Very High ETa"]
)

df = gdf[['quantile_bin', '_mean']]

# Create the bar chart
bar = alt.Chart(df).mark_bar().encode(
    y=alt.X('_mean', bin=alt.Bin(
        extent=[quantiles[0], quantiles[-1]], step=(quantiles[-1] - quantiles[0]) / 10)),
    x='count()',
    color=alt.Color('quantile_bin:N', scale=alt.Scale(domain=[
                    "Very Low ETa", "Low ETa", "Moderate ETa", "High ETa", "Very High ETa"], range=colors)),
).properties(
    title="ETa Distribution",
    height=700,
)

col1, col2 = st.columns([3, 1])

with col2:
    st.session_state.basemap = st.selectbox(
        "Select basemap", options, index=options.index("Esri.WorldImagery"))
    st.altair_chart(bar, use_container_width=True)

with col1:
    # Initialize the map centered on the GeoJSON centroid
    m = leafmap.Map(
        center=(centroid_lat, centroid_lon),  # Center the map on the centroid
        zoom=10,  # Adjust the zoom level as needed
        style="positron"
    )
    m.add_basemap(st.session_state.basemap)
    m.add_geojson(
        leafmap.gdf_to_geojson(gdf),
        layer_type="fill-extrusion",
        name="ETa",
        paint={
            "fill-extrusion-height": ["*", 200, ["get", "_mean"]],
            "fill-extrusion-opacity": 0.6,
            "fill-extrusion-color": ["get", "color"],
        },
    )

    # Add a legend to the map using hex color codes
    legend_dict = {
        "Very Low ETa": "#808080",  # grey
        "Low ETa": "#FFFF00",       # yellow
        "Moderate ETa": "#FFA500",  # orange
        "High ETa": "#8B0000",      # darkred
        "Very High ETa": "#ADD8E6",  # lightblue
    }
    m.add_legend(
        title="ETa Levels",
        legend_dict=legend_dict,
        bg_color="rgba(255, 255, 255, 0.5)",
        position="bottom-left",
    )

    m.add_layer_control()
    m.to_streamlit(height=700)
