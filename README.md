
# Factory-to-Customer Shipping Route Efficiency Analysis

## Project Overview

This project analyzes shipment records for Nassau Candy Distributor to explore shipping lead times, factory-to-customer routes, shipping modes, geographic performance, sales, and product profitability.

It uses Python for data analysis and Streamlit to provide an interactive dashboard for exploring shipment data and identifying routes that may require further investigation.

## Objectives

- Calculate shipping lead time from order and ship dates.
- Analyze factory-to-state and factory-to-region routes.
- Compare shipment volumes and calculated lead times across shipping modes.
- Identify high-volume routes and possible geographic bottlenecks.
- Analyze sales and gross profit by product and region.
- Provide interactive filters and visualizations in a Streamlit dashboard.

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- CSV data analysis
- Visual analytics

## Project Files

- `analysis.py` — data cleaning, feature engineering, and analysis.
- `dashboard.py` — interactive Streamlit dashboard.
- `Nassau Candy Distributor.csv` — original dataset, if permitted for public sharing.
- `cleaned_nassau_candy.csv` — cleaned dataset.
- `route_analysis.csv` — factory-to-state route summaries.
- `high_volume_routes.csv` — route summaries filtered by shipment volume.
- `Nassau_Candy_Shipping_Analysis_Project_Report.docx` — project report, if included.

## Dashboard Features

- Interactive date, region, state, shipping-mode, and lead-time filters.
- Shipping overview KPIs.
- Shipping-mode and regional comparisons.
- Factory-to-customer route rankings.
- Geographic shipping heatmap and bottleneck analysis.
- Product sales and gross-profit analysis.
- Order-level shipment timeline.
- CSV downloads of filtered analysis results.

## Data Quality Limitation

The available dataset produces calculated shipping lead times ranging from 904 to 1,642 days. These unusually long durations require verification of the source dates before they can be interpreted as actual delivery performance.

The dataset's manufacturing cost is not the same as transportation cost, so a true shipping cost-versus-time comparison requires additional cost data.

## How to Run the Project

1. Install Python.
2. Install the required packages:

   ```bash
   python -m pip install pandas streamlit plotly
   ```

3. Run the analysis:

   ```bash
   python analysis.py
   ```

4. Start the dashboard:

   ```bash
   python -m streamlit run dashboard.py
   ```

5. Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Author

Venugopal M

## Project Context

Prepared as a data analytics project based on the Factory-to-Customer Shipping Route Efficiency Analysis requirements provided by Unified Mentor.
