import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="Nassau Candy Shipping Analysis",
    page_icon="🍬",
    layout="wide"
)

st.title("🍬 Nassau Candy Distributor")
st.subheader("Factory-to-Customer Shipping Route Efficiency Analysis")
st.caption(
    "Explore shipment lead times, factory-to-customer routes, shipping modes, "
    "geographic performance, sales, and product profitability."
)

# ------------------------------------------------------------
# Constants and mappings
# ------------------------------------------------------------
FACTORY_MAPPING = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

FACTORY_LOCATIONS = pd.DataFrame({
    "Factory": [
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Sugar Shack",
        "Secret Factory",
        "The Other Factory"
    ],
    "latitude": [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
    "longitude": [-111.768036, -81.088371, -96.18115, -90.565487, -89.971107]
})

STATE_COORDINATES = {
    "Alabama": (32.8067, -86.7911), "Alaska": (61.3707, -152.4044),
    "Arizona": (33.7298, -111.4312), "Arkansas": (34.9697, -92.3731),
    "California": (36.7783, -119.4179), "Colorado": (39.0598, -105.3111),
    "Connecticut": (41.5978, -72.7554), "Delaware": (39.3185, -75.5071),
    "Florida": (27.6648, -81.5158), "Georgia": (32.1574, -82.9071),
    "Hawaii": (19.8968, -155.5828), "Idaho": (44.2405, -114.4788),
    "Illinois": (40.0000, -89.0000), "Indiana": (39.8494, -86.2583),
    "Iowa": (42.0115, -93.2105), "Kansas": (38.5266, -96.7265),
    "Kentucky": (37.6681, -84.6701), "Louisiana": (31.1695, -91.8678),
    "Maine": (44.6939, -69.3819), "Maryland": (39.0639, -76.8021),
    "Massachusetts": (42.2302, -71.5301), "Michigan": (44.3148, -85.6024),
    "Minnesota": (46.7296, -94.6859), "Mississippi": (32.7416, -89.6787),
    "Missouri": (38.4561, -92.2884), "Montana": (46.9219, -110.4544),
    "Nebraska": (41.1254, -98.2681), "Nevada": (38.3135, -117.0554),
    "New Hampshire": (43.4525, -71.5639), "New Jersey": (40.2989, -74.5210),
    "New Mexico": (34.8405, -106.2485), "New York": (43.0000, -75.0000),
    "North Carolina": (35.7596, -79.0193), "North Dakota": (47.5515, -101.0020),
    "Ohio": (40.4173, -82.9071), "Oklahoma": (35.5653, -96.9289),
    "Oregon": (43.8041, -120.5542), "Pennsylvania": (41.2033, -77.1945),
    "Rhode Island": (41.5801, -71.4774), "South Carolina": (33.8361, -81.1637),
    "South Dakota": (43.9695, -99.9018), "Tennessee": (35.7478, -86.6923),
    "Texas": (31.0000, -100.0000), "Utah": (39.3210, -111.0937),
    "Vermont": (44.0459, -72.7107), "Virginia": (37.7693, -78.1700),
    "Washington": (47.4009, -121.4905), "West Virginia": (38.4912, -80.9545),
    "Wisconsin": (44.2685, -89.6165), "Wyoming": (42.7559, -107.3025),
    "District of Columbia": (38.9072, -77.0369)
}

STATE_ABBREVIATIONS = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

# ------------------------------------------------------------
# Load and validate data
# ------------------------------------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("cleaned_nassau_candy.csv")

    required_columns = [
        "Order ID", "Order Date", "Ship Date", "Ship Mode", "Region",
        "State/Province", "Product Name", "Sales", "Gross Profit", "Cost"
    ]
    missing_columns = [column for column in required_columns if column not in data.columns]
    if missing_columns:
        raise ValueError(
            "The cleaned dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    data["Ship Date"] = pd.to_datetime(data["Ship Date"], errors="coerce")

    # Recalculate lead time from the date fields to keep the dashboard consistent.
    data["Shipping Lead Time"] = (data["Ship Date"] - data["Order Date"]).dt.days

    # Exclude invalid dates and negative lead times from dashboard calculations.
    data = data.dropna(subset=["Order Date", "Ship Date", "Shipping Lead Time"]).copy()
    data = data[data["Shipping Lead Time"] >= 0].copy()

    data["Factory"] = data["Product Name"].map(FACTORY_MAPPING)
    data["Shipping Route"] = (
        data["Factory"].fillna("Unmapped Factory").astype(str)
        + " -> "
        + data["State/Province"].fillna("Unknown State").astype(str)
    )
    data["Factory-to-Region Route"] = (
        data["Factory"].fillna("Unmapped Factory").astype(str)
        + " -> "
        + data["Region"].fillna("Unknown Region").astype(str)
    )
    return data

try:
    df = load_data()
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.info(
        "Check that cleaned_nassau_candy.csv is in the same folder as dashboard.py."
    )
    st.stop()

if df.empty:
    st.error("No valid shipment records remain after date and lead-time validation.")
    st.stop()

# ------------------------------------------------------------
# Data-quality notice
# ------------------------------------------------------------
min_lead_time = int(df["Shipping Lead Time"].min())
max_lead_time = int(df["Shipping Lead Time"].max())
median_lead_time = float(df["Shipping Lead Time"].median())

st.warning(
    "Data-quality notice: the recorded order and ship dates produce unusually "
    f"long lead times (currently {min_lead_time:,} to {max_lead_time:,} days). "
    "The dashboard preserves the source dates and reports calculated durations; "
    "these values should not be treated as verified real-world delivery times "
    "until the source data is validated."
)

# ------------------------------------------------------------
# Filters near the top of the dashboard
# ------------------------------------------------------------
st.sidebar.header("Dashboard Filters")

date_min = df["Order Date"].min().date()
date_max = df["Order Date"].max().date()

date_selection = st.sidebar.date_input(
    "Order date range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

regions = sorted(df["Region"].dropna().astype(str).unique().tolist())
states = sorted(df["State/Province"].dropna().astype(str).unique().tolist())
modes = sorted(df["Ship Mode"].dropna().astype(str).unique().tolist())

selected_region = st.sidebar.selectbox("Region", ["All"] + regions)
selected_state = st.sidebar.selectbox("State / Province", ["All"] + states)
selected_mode = st.sidebar.selectbox("Shipping mode", ["All"] + modes)

threshold_max = max(1, int(df["Shipping Lead Time"].max()))
lead_time_threshold = st.sidebar.slider(
    "Maximum lead time (days)",
    min_value=0,
    max_value=threshold_max,
    value=threshold_max
)

delay_threshold = st.sidebar.number_input(
    "Delay threshold (days)",
    min_value=1,
    max_value=threshold_max,
    value=min(30, threshold_max),
    step=1
)

filtered_data = df.copy()

if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
    start_date, end_date = date_selection
    filtered_data = filtered_data[
        filtered_data["Order Date"].dt.date.between(start_date, end_date)
    ]
elif isinstance(date_selection, (tuple, list)) and len(date_selection) == 1:
    one_date = date_selection[0]
    filtered_data = filtered_data[filtered_data["Order Date"].dt.date == one_date]
elif not isinstance(date_selection, (tuple, list)):
    filtered_data = filtered_data[
        filtered_data["Order Date"].dt.date == date_selection
    ]

if selected_region != "All":
    filtered_data = filtered_data[filtered_data["Region"] == selected_region]
if selected_state != "All":
    filtered_data = filtered_data[filtered_data["State/Province"] == selected_state]
if selected_mode != "All":
    filtered_data = filtered_data[filtered_data["Ship Mode"] == selected_mode]

filtered_data = filtered_data[
    filtered_data["Shipping Lead Time"] <= lead_time_threshold
].copy()

st.caption(
    f"Showing {len(filtered_data):,} of {len(df):,} valid shipment records "
    "after applying the selected filters."
)

if filtered_data.empty:
    st.warning("No shipments match these filters. Change one or more selections.")
    st.stop()

# ------------------------------------------------------------
# Overview and KPIs (filtered data)
# ------------------------------------------------------------
st.header("Shipping Overview")

total_shipments = len(filtered_data)
average_lead_time = filtered_data["Shipping Lead Time"].mean()
shortest_lead_time = filtered_data["Shipping Lead Time"].min()
longest_lead_time = filtered_data["Shipping Lead Time"].max()
delayed_count = int((filtered_data["Shipping Lead Time"] > delay_threshold).sum())
delay_rate = delayed_count / total_shipments * 100 if total_shipments else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Shipments", f"{total_shipments:,}")
k2.metric("Average Lead Time", f"{average_lead_time:,.1f} days")
k3.metric("Longest Lead Time", f"{longest_lead_time:,.0f} days")
k4.metric("Above-Threshold Rate", f"{delay_rate:.2f}%")

st.caption(
    f"Delay threshold: more than {delay_threshold} days. "
    "This is a user-defined analytical threshold, not a confirmed service-level target."
)

with st.expander("Dataset overview and sample records"):
    overview1, overview2, overview3 = st.columns(3)
    overview1.metric("Valid Records in Source", f"{len(df):,}")
    overview2.metric("Columns", f"{len(df.columns):,}")
    overview3.metric("Unique Orders", f"{df['Order ID'].nunique():,}")
    st.dataframe(filtered_data.head(20), use_container_width=True)

# ------------------------------------------------------------
# Shipping mode analysis
# ------------------------------------------------------------
st.header("Shipping Mode Performance")

mode_analysis = (
    filtered_data.groupby("Ship Mode", dropna=False)
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Average_Manufacturing_Cost=("Cost", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)
mode_analysis["Average_Lead_Time"] = mode_analysis["Average_Lead_Time"].round(2)
mode_analysis["Median_Lead_Time"] = mode_analysis["Median_Lead_Time"].round(2)
mode_analysis["Average_Manufacturing_Cost"] = (
    mode_analysis["Average_Manufacturing_Cost"].round(2)
)

mode_col1, mode_col2 = st.columns(2)
with mode_col1:
    st.subheader("Shipment Volume by Mode")
    st.bar_chart(mode_analysis.set_index("Ship Mode")["Total_Shipments"])
with mode_col2:
    st.subheader("Average Lead Time by Mode")
    st.bar_chart(mode_analysis.set_index("Ship Mode")["Average_Lead_Time"])

st.dataframe(mode_analysis, use_container_width=True)
st.caption(
    "Cost is the dataset's manufacturing cost, not transportation or shipping cost. "
    "It cannot establish the actual cost-time trade-off between shipping modes."
)

# ------------------------------------------------------------
# Region analysis
# ------------------------------------------------------------
st.header("Regional Shipping Performance")

region_analysis = (
    filtered_data.groupby("Region", dropna=False)
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)
region_analysis["Average_Lead_Time"] = region_analysis["Average_Lead_Time"].round(2)

reg_col1, reg_col2 = st.columns(2)
with reg_col1:
    st.subheader("Shipment Volume by Region")
    st.bar_chart(region_analysis.set_index("Region")["Total_Shipments"])
with reg_col2:
    st.subheader("Average Lead Time by Region")
    st.bar_chart(region_analysis.set_index("Region")["Average_Lead_Time"])
st.dataframe(region_analysis, use_container_width=True)

# ------------------------------------------------------------
# Route analysis, computed from the filtered records
# ------------------------------------------------------------
st.header("Factory-to-Customer Route Efficiency")

route_analysis = (
    filtered_data.groupby(
        ["Factory", "State/Province", "Shipping Route"],
        dropna=False
    )
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Lead_Time_Std=("Shipping Lead Time", "std")
    )
    .reset_index()
)
route_analysis["Average_Lead_Time"] = route_analysis["Average_Lead_Time"].round(2)
route_analysis["Median_Lead_Time"] = route_analysis["Median_Lead_Time"].round(2)
route_analysis["Lead_Time_Std"] = route_analysis["Lead_Time_Std"].round(2)

minimum_route_shipments = st.number_input(
    "Minimum shipments required for route ranking",
    min_value=1,
    max_value=max(1, total_shipments),
    value=min(20, max(1, total_shipments)),
    step=1
)

eligible_routes = route_analysis[
    route_analysis["Total_Shipments"] >= minimum_route_shipments
].copy()

if not eligible_routes.empty:
    fastest_routes = eligible_routes.sort_values(
        ["Average_Lead_Time", "Total_Shipments"],
        ascending=[True, False]
    ).head(10)
    slowest_routes = eligible_routes.sort_values(
        ["Average_Lead_Time", "Total_Shipments"],
        ascending=[False, False]
    ).head(10)

    fast_col, slow_col = st.columns(2)
    with fast_col:
        st.subheader("10 Fastest Eligible Routes")
        st.dataframe(fastest_routes, use_container_width=True)
    with slow_col:
        st.subheader("10 Slowest Eligible Routes")
        st.dataframe(slowest_routes, use_container_width=True)

    st.subheader("Slowest High-Volume Routes")
    st.bar_chart(
        slowest_routes.set_index("Shipping Route")["Average_Lead_Time"]
    )

    # Normalized route score uses only eligible routes, making the benchmark
    # consistent with the displayed route-ranking threshold.
    min_route_time = eligible_routes["Average_Lead_Time"].min()
    max_route_time = eligible_routes["Average_Lead_Time"].max()
    if pd.notna(min_route_time) and pd.notna(max_route_time) and max_route_time > min_route_time:
        eligible_routes["Efficiency_Score"] = (
            (max_route_time - eligible_routes["Average_Lead_Time"])
            / (max_route_time - min_route_time) * 100
        ).round(2)
    else:
        eligible_routes["Efficiency_Score"] = 100.0

    st.subheader("Route Efficiency Score")
    st.caption(
        "Normalized score from 0 to 100 among routes meeting the minimum shipment "
        "count. Higher scores indicate shorter average calculated lead times; "
        "this is a relative score, not an external industry benchmark."
    )
    st.dataframe(
        eligible_routes.sort_values("Efficiency_Score", ascending=False)[
            [
                "Shipping Route", "Total_Shipments", "Average_Lead_Time",
                "Lead_Time_Std", "Efficiency_Score"
            ]
        ],
        use_container_width=True
    )
else:
    st.info(
        "No routes meet the current minimum shipment count. Lower the threshold "
        "to display route rankings."
    )

# Factory-to-region route analysis
st.subheader("Factory-to-Region Routes")
factory_region_analysis = (
    filtered_data.groupby(
        ["Factory", "Region", "Factory-to-Region Route"],
        dropna=False
    )
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Std=("Shipping Lead Time", "std")
    )
    .reset_index()
)
factory_region_analysis["Average_Lead_Time"] = (
    factory_region_analysis["Average_Lead_Time"].round(2)
)
factory_region_analysis["Lead_Time_Std"] = (
    factory_region_analysis["Lead_Time_Std"].round(2)
)
st.dataframe(
    factory_region_analysis.sort_values(
        "Average_Lead_Time", ascending=False
    ),
    use_container_width=True
)

# ------------------------------------------------------------
# Delay frequency analysis (filtered data)
# ------------------------------------------------------------
st.header("Delay Frequency Analysis")
st.write(
    f"A shipment is counted as above threshold when its calculated lead time "
    f"is greater than {delay_threshold} days."
)
delay_summary = pd.DataFrame({
    "Measure": ["Shipments in filtered data", "Shipments above threshold", "Above-threshold rate"],
    "Value": [
        f"{total_shipments:,}",
        f"{delayed_count:,}",
        f"{delay_rate:.2f}%"
    ]
})
st.dataframe(delay_summary, use_container_width=True)

# ------------------------------------------------------------
# Sales and product profitability
# ------------------------------------------------------------
st.header("Sales and Product Profitability")

sales_total = filtered_data["Sales"].sum()
profit_total = filtered_data["Gross Profit"].sum()
fin1, fin2 = st.columns(2)
fin1.metric("Total Sales", f"${sales_total:,.2f}")
fin2.metric("Total Gross Profit", f"${profit_total:,.2f}")

product_profit = (
    filtered_data.groupby("Product Name", dropna=False)
    .agg(
        Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values("Total_Gross_Profit", ascending=False)
    .head(10)
)
st.subheader("Top 10 Products by Gross Profit")
st.bar_chart(product_profit.set_index("Product Name")["Total_Gross_Profit"])
st.dataframe(product_profit, use_container_width=True)

st.subheader("Sales and Gross Profit by Region")
region_financials = filtered_data.groupby("Region")[["Sales", "Gross Profit"]].sum()
st.bar_chart(region_financials)

# ------------------------------------------------------------
# Geographic state analysis and heatmap
# ------------------------------------------------------------
st.header("Geographic Shipping Analysis")

state_analysis = (
    filtered_data.groupby("State/Province", dropna=False)
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)
state_analysis["Average_Lead_Time"] = state_analysis["Average_Lead_Time"].round(2)

st.subheader("State Shipping Summary")
st.dataframe(
    state_analysis.sort_values(
        ["Total_Shipments", "Average_Lead_Time"],
        ascending=[False, False]
    ),
    use_container_width=True
)

st.subheader("US Shipping Efficiency Heatmap")
heatmap_data = state_analysis.copy()
heatmap_data["State_Code"] = heatmap_data["State/Province"].map(STATE_ABBREVIATIONS)
heatmap_data = heatmap_data.dropna(subset=["State_Code"]).copy()

if not heatmap_data.empty:
    fig = px.choropleth(
        heatmap_data,
        locations="State_Code",
        locationmode="USA-states",
        color="Average_Lead_Time",
        hover_name="State/Province",
        hover_data={
            "Total_Shipments": True,
            "Average_Lead_Time": ":.2f",
            "State_Code": False
        },
        scope="usa",
        color_continuous_scale="YlOrRd",
        labels={"Average_Lead_Time": "Average lead time (days)"},
        title="Average Calculated Shipping Lead Time by State"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "States not represented in the filtered records are not shaded. "
        "Higher values mean longer calculated lead times, not verified delivery delays."
    )
else:
    st.info("No recognized US states are available for the heatmap under these filters.")

st.subheader("High-Volume Geographic Bottlenecks")
if not state_analysis.empty:
    volume_benchmark = state_analysis["Total_Shipments"].median()
    lead_time_benchmark = state_analysis["Average_Lead_Time"].median()
    bottlenecks = state_analysis[
        (state_analysis["Total_Shipments"] >= volume_benchmark)
        & (state_analysis["Average_Lead_Time"] >= lead_time_benchmark)
    ].sort_values(
        ["Average_Lead_Time", "Total_Shipments"],
        ascending=[False, False]
    )
    st.caption(
        f"Descriptive benchmarks: at least {volume_benchmark:.0f} shipments "
        f"and average lead time of at least {lead_time_benchmark:.2f} days "
        "within the filtered data."
    )
    st.dataframe(bottlenecks, use_container_width=True)

    st.subheader("Average Lead Time by State")
    slow_states = state_analysis.sort_values(
        "Average_Lead_Time", ascending=False
    ).head(10)
    st.bar_chart(slow_states.set_index("State/Province")["Average_Lead_Time"])

# Approximate state point map
st.subheader("Customer-State Point Map")
state_map = state_analysis.copy()
state_map["latitude"] = state_map["State/Province"].map(
    lambda state: STATE_COORDINATES.get(state, (None, None))[0]
)
state_map["longitude"] = state_map["State/Province"].map(
    lambda state: STATE_COORDINATES.get(state, (None, None))[1]
)
state_map = state_map.dropna(subset=["latitude", "longitude"]).copy()

if not state_map.empty:
    st.caption(
        f"Showing {state_map['State/Province'].nunique()} states/locations "
        "with coordinates available in the map mapping."
    )
    st.map(state_map[["latitude", "longitude"]], size="Total_Shipments")
else:
    st.info("No mapped customer states are available under the current filters.")

# Factory locations
st.subheader("Factory Locations")
st.map(FACTORY_LOCATIONS[["latitude", "longitude"]])
st.dataframe(FACTORY_LOCATIONS, use_container_width=True)

# ------------------------------------------------------------
# Order-level shipment timeline
# ------------------------------------------------------------
st.header("Order-Level Shipment Timeline")

order_ids = sorted(filtered_data["Order ID"].dropna().astype(str).unique().tolist())
if order_ids:
    selected_order = st.selectbox(
        "Select an order ID",
        order_ids,
        key="timeline_order"
    )
    order_details = filtered_data[
        filtered_data["Order ID"].astype(str) == selected_order
    ].copy()

    timeline_columns = [
        column for column in [
            "Order ID", "Order Date", "Ship Date", "Ship Mode",
            "Product Name", "State/Province", "Shipping Lead Time"
        ] if column in order_details.columns
    ]
    st.subheader("Selected Order Details")
    st.dataframe(order_details[timeline_columns], use_container_width=True)

    if not order_details.empty:
        timeline_row = order_details.iloc[0]
        timeline_plot_data = pd.DataFrame({
            "Event": ["Order Placed", "Shipment Recorded"],
            "Date": [
                timeline_row["Order Date"],
                timeline_row["Ship Date"]
            ]
        })
        timeline_fig = px.scatter(
            timeline_plot_data,
            x="Date",
            y="Event",
            text="Event",
            title="Recorded Order and Shipment Dates"
        )
        timeline_fig.update_traces(marker={"size": 14}, textposition="top center")
        timeline_fig.update_layout(
            xaxis_title="Recorded date",
            yaxis_title="",
            showlegend=False
        )
        st.plotly_chart(timeline_fig, use_container_width=True)
        st.metric(
            "Calculated Lead Time",
            f"{int(timeline_row['Shipping Lead Time']):,} days"
        )
        st.caption(
            "The shipment date is the date recorded in the dataset; it is not "
            "independent confirmation of the date the customer received the goods."
        )
else:
    st.info("No orders match the current filters.")

# ------------------------------------------------------------
# Findings and recommendations
# ------------------------------------------------------------
st.header("Key Findings and Recommendations")

st.markdown("""
**Findings**
- Standard Class is the most frequently used shipping mode in the full dataset.
- Shipment volume and average calculated lead time vary by region, state, and route.
- Route rankings are more useful when routes have a reasonable minimum shipment count.
- Recorded lead times are unusually long and require source-data validation.

**Recommendations**
1. Verify the original order and ship dates before using lead time as an operational service measure.
2. Investigate high-volume routes with high calculated lead times after date quality is confirmed.
3. Monitor shipment volume and calculated lead time by region, state, factory, and shipping mode.
4. Use manufacturing cost only for manufacturing-cost analysis; obtain transportation cost data for true shipping cost comparisons.
5. Refresh the analysis regularly as validated shipment data becomes available.
""")

st.header("Project Conclusion")
st.write(
    "This dashboard combines shipment, route, geographic, shipping-mode, sales, "
    "and product-profitability analysis. Its results support further investigation "
    "of route performance, while operational conclusions remain limited by the "
    "unusually long lead times recorded in the source dates."
)

# ------------------------------------------------------------
# Download filtered results
# ------------------------------------------------------------
st.header("Download Results")
st.download_button(
    "Download filtered shipment records (CSV)",
    data=filtered_data.to_csv(index=False).encode("utf-8"),
    file_name="filtered_nassau_shipments.csv",
    mime="text/csv"
)
st.download_button(
    "Download route analysis (CSV)",
    data=route_analysis.to_csv(index=False).encode("utf-8"),
    file_name="filtered_route_analysis.csv",
    mime="text/csv"
)
