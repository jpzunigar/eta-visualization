# ETa Visualization App for Sugar Cane Fields

This Streamlit application provides insightful visualizations of actual evapotranspiration (ETa) data across sugar cane plantations. It enables users to analyze ETa patterns, assess water usage efficiency, and make data-driven decisions to optimize irrigation practices.

## Features

- **Interactive Map**: Visualize ETa data on a map with customizable basemaps.
- **Quantile-based Color Coding**: ETa data is color-coded based on quantiles, allowing for easy identification of areas with varying levels of evapotranspiration.
- **Centroid Calculation**: The map is centered on the centroid of the GeoJSON data for optimal viewing.
- **ETa Distribution Chart**: Analyze the distribution of ETa values using an Altair bar chart.
- **Legend and Basemap Selection**: Customize the map view by selecting different basemaps and viewing a legend for ETa levels.

## Installation

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

To run this application locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    ```

2. **Navigate to the project directory:**

    ```bash
    cd <project-directory>
    ```

3. **Install the required Python packages using Poetry:**

    ```bash
    poetry install
    ```

4. **Activate the virtual environment:**

    ```bash
    poetry shell
    ```

## Usage

1. **Prepare Your Data:**

   Place your GeoJSON file in the `./data/` directory. By default, the app expects a file named `suertes_eta.geojson`.

2. **Run the Streamlit App:**

    ```bash
    streamlit run app.py
    ```

3. **View the App:**

   Open your browser and navigate to `http://localhost:8501` to view the app.

## Project Structure

.
├── app.py # Main Streamlit app script
├── data/
│ └── suertes_eta.geojson # GeoJSON data file (replace with your own)
├── README.md # Project documentation
├── poetry.lock # Poetry lock file
├── pyproject.toml # Poetry configuration file


## How It Works

- **GeoPandas** is used to load and process GeoJSON data.
- **Leafmap** (MapLibre GL) is utilized to create an interactive map displaying the ETa data.
- **Altair** is used to generate a bar chart that visualizes the distribution of ETa values across the sugar cane fields.
- The app calculates the centroid of the GeoJSON data to center the map for optimal viewing.
- A sidebar provides information about the app and allows users to select different basemaps.

### Map Features

- **Basemap Selection:** Users can choose from various basemap options to customize the map's appearance.
- **Color-Coded Visualization:** The ETa data is color-coded based on quantiles, ranging from "Very Low ETa" to "Very High ETa".
- **Legend:** A legend is provided to help users interpret the color-coded ETa data.

### Data Visualization

- The app categorizes ETa data into quantile bins and displays the distribution in a bar chart using **Altair**.

## Customization

- **Color Scheme:** To modify the color scheme, edit the `colors` list in the `app.py` file.
- **Map Centering:** Adjust the map's zoom level and initial centering by changing the parameters in the `leafmap.Map()` function.
- **Quantile Bins:** Customize the quantile bins and labels by modifying the `gdf['quantile_bin']` creation section.

## Troubleshooting

- **Data Not Displaying:** Ensure that your GeoJSON file is correctly formatted and placed in the `./data/` directory.
- **Dependency Issues:** If you encounter issues with dependencies, make sure all packages are installed correctly using Poetry.

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

### Steps to Contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

This project utilizes the following libraries and tools:

- [Streamlit](https://streamlit.io/) - For building the web application.
- [Leafmap](https://leafmap.org/) - For interactive mapping.
- [GeoPandas](https://geopandas.org/) - For geospatial data processing.
- [Altair](https://altair-viz.github.io/) - For data visualization.

Special thanks to the open-source community for providing these tools.

