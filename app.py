import streamlit as st
import geopandas as gpd
import pandas as pd
import altair as alt
import leafmap.kepler as leafmap

st.set_page_config(
    layout="wide", page_title="ETa Visualization App", page_icon=":bar_chart:")
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

        **Alberto Mario Arroyo**
        - Email: amarroyo@cenicana.org

        """
    )

st.title("ETa visualization on sugarcane Field")
st.write("")
st.write("")

# Create a DataFrame for Altair with quantile bins
gdf['quantile_bin'] = pd.cut(
    gdf['_mean'],
    bins=[-float("inf"), *quantiles[1:], float("inf")],
    labels=["Very Low ETa", "Low ETa",
            "Moderate ETa", "High ETa", "Very High ETa"]
)
gdf['eta'] = gdf['_mean']

df = gdf[['quantile_bin', '_mean']]

# Create the bar chart
bar = alt.Chart(df).mark_bar().encode(
    y=alt.Y('_mean', bin=alt.Bin(
        extent=[quantiles[0], quantiles[-1]], step=(quantiles[-1] - quantiles[0]) / 10),
        axis=alt.Axis(title='ETa Value Range')),
    x='count()',
    color=alt.Color('quantile_bin:N', scale=alt.Scale(domain=[
                    "Very Low ETa", "Low ETa", "Moderate ETa", "High ETa", "Very High ETa"], range=colors)),
).properties(
    title="ETa Distribution",
    height=700,
)

col1, col2 = st.columns([3, 1])

with col2:
    st.altair_chart(bar, use_container_width=True)

# Use KeplerGl for the map visualization
with col1:
    m = leafmap.Map(height=700)

    # Add the data to KeplerGl
    m.add_data(data=gdf, name="ETa Levels")

    # Kepler.gl configuration
    config = {
        "version": "v1",
        "config": {
            "visState": {
                "filters": [],
                "layers": [
                    {
                        "id": "tdp4as8",
                        "type": "geojson",
                        "config": {
                            "dataId": "ETa Levels",
                            "label": "ETa",
                            "color": [
                                18,
                                147,
                                154
                            ],
                            "columns": {
                                "geojson": "geometry"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.72,
                                "strokeOpacity": 0.8,
                                "thickness": 0.5,
                                "strokeColor": [
                                    221,
                                    178,
                                    124
                                ],
                                "colorRange": {
                                    "name": "Custom Palette",
                                    "type": "custom",
                                    "category": "Custom",
                                    "colors": [
                                        "#808080",
                                        "#FFFF00",
                                        "#FFA500",
                                        "#8B0000",
                                        "#ADD8E6"
                                    ]
                                },
                                "strokeColorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300"
                                    ]
                                },
                                "radius": 10,
                                "sizeRange": [
                                    0,
                                    10
                                ],
                                "radiusRange": [
                                    0,
                                    50
                                ],
                                "heightRange": [
                                    0,
                                    500
                                ],
                                "elevationScale": 1,
                                "stroked": False,
                                "filled": True,
                                "enable3d": True,
                                "wireframe": False
                            },
                            "hidden": False,
                            "textLabel": [
                                {
                                    "field": None,
                                    "color": [
                                        255,
                                        255,
                                        255
                                    ],
                                    "size": 18,
                                    "offset": [
                                        0,
                                        0
                                    ],
                                    "anchor": "start",
                                    "alignment": "center"
                                }
                            ]
                        },
                        "visualChannels": {
                            "colorField": {
                                "name": "color",
                                "type": "string"
                            },
                            "colorScale": "ordinal",
                            "sizeField": None,
                            "sizeScale": "linear",
                            "strokeColorField": None,
                            "strokeColorScale": "quantile",
                            "heightField": {
                                "name": "eta",
                                "type": "real"
                            },
                            "heightScale": "linear",
                            "radiusField": None,
                            "radiusScale": "linear"
                        }
                    }
                ],
                "interactionConfig": {
                    "tooltip": {
                        "fieldsToShow": {
                            "ETa Levels": [
                                {
                                    "name": "AREA",
                                    "format": None
                                },
                                {
                                    "name": "Perimetro",
                                    "format": None
                                },
                                {
                                    "name": "eta",
                                    "format": None
                                },
                                {
                                    "name": "quantile_bin",
                                    "format": None
                                }
                            ]
                        },
                        "compareMode": False,
                        "compareType": "absolute",
                        "enabled": True
                    },
                    "brush": {
                        "size": 0.5,
                        "enabled": False
                    },
                    "geocoder": {
                        "enabled": False
                    },
                    "coordinate": {
                        "enabled": False
                    }
                },
                "layerBlending": "normal",
                "splitMaps": [],
                "animationConfig": {
                    "currentTime": None,
                    "speed": 1
                }
            },
            "mapState": {
                "bearing": 2.6192893401015205,
                "dragRotate": True,
                "latitude": 3.777306559818618,
                "longitude": -76.37071390286864,
                "pitch": 37.374216241015446,
                "zoom": 10.75174663737936,
                "isSplit": False
            },
            "mapStyle": {
                "styleType": "dark",
                "topLayerGroups": {},
                "visibleLayerGroups": {
                    "label": True,
                    "road": True,
                    "border": False,
                    "building": True,
                    "water": True,
                    "land": True,
                    "3d building": False
                },
                "threeDBuildingColor": [
                    9.665468314072013,
                    17.18305478057247,
                    31.1442867897876
                ],
                "mapStyles": {}
            }
        }
    }

    # Pass the configuration to the KeplerGl map
    m.config = config

    # Display the map in Streamlit
    m.to_streamlit(height=700)
