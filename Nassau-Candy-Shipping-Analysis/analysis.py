import pandas as pd

# Load the Nassau Candy dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Display basic dataset information
print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nOrder Date values:")
print(df["Order Date"].head())

print("\nShip Date values:")
print(df["Ship Date"].head())

# Convert date columns into datetime format
df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="%d-%m-%Y", errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], format="%d-%m-%Y", errors="coerce"
)

print("\nConverted date columns:")
print(df[["Order Date", "Ship Date"]].head())

print("\nMissing order dates:", df["Order Date"].isna().sum())
print("Missing ship dates:", df["Ship Date"].isna().sum())

# Calculate shipping lead time in days
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print("\nShipping Lead Time:")
print(df[["Order Date", "Ship Date", "Shipping Lead Time"]].head())

print("\nAverage shipping lead time:",
      df["Shipping Lead Time"].mean(), "days")

print("Minimum shipping lead time:",
      df["Shipping Lead Time"].min(), "days")

print("Maximum shipping lead time:",
      df["Shipping Lead Time"].max(), "days")

# Check invalid shipping lead times
negative_times = (df["Shipping Lead Time"] < 0).sum()
missing_times = df["Shipping Lead Time"].isna().sum()
zero_times = (df["Shipping Lead Time"] == 0).sum()

print("\n--- Shipping Data Quality Check ---")
print("Negative shipping times:", negative_times)
print("Missing shipping times:", missing_times)
print("Zero-day shipping times:", zero_times)

# Create a cleaned dataset
clean_df = df.dropna(
    subset=["Order Date", "Ship Date", "Shipping Lead Time"]
).copy()

clean_df = clean_df[
    clean_df["Shipping Lead Time"] >= 0
].copy()

# Save the cleaned dataset
clean_df.to_csv("cleaned_nassau_candy.csv", index=False)

print("\n--- Cleaning Results ---")
print("Original rows:", len(df))
print("Cleaned rows:", len(clean_df))
print("Saved file: cleaned_nassau_candy.csv")

# Analyze shipping performance by ship mode
ship_mode_analysis = clean_df.groupby("Ship Mode").agg(
    Total_Shipments=("Order ID", "count"),
    Average_Lead_Time=("Shipping Lead Time", "mean"),
    Minimum_Lead_Time=("Shipping Lead Time", "min"),
    Maximum_Lead_Time=("Shipping Lead Time", "max")
).reset_index()

print("\n--- Shipping Mode Analysis ---")
print(ship_mode_analysis.round(2))

# Find states with the most shipment records
state_analysis = clean_df.groupby("State/Province").agg(
    Total_Shipments=("Order ID", "count"),
    Average_Lead_Time=("Shipping Lead Time", "mean")
).reset_index()

state_analysis = state_analysis.sort_values(
    by="Total_Shipments",
    ascending=False
)

print("\n--- Top 10 States by Shipment Volume ---")
print(state_analysis.head(10).round(2))

# Analyze shipping performance by region
region_analysis = clean_df.groupby("Region").agg(
    Total_Shipments=("Order ID", "count"),
    Average_Lead_Time=("Shipping Lead Time", "mean"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum")
).reset_index()

region_analysis = region_analysis.sort_values(
    by="Total_Shipments",
    ascending=False
)

print("\n--- Shipping Analysis by Region ---")
print(region_analysis.round(2))

# Analyze profitability by product
product_analysis = clean_df.groupby("Product Name").agg(
    Total_Units=("Units", "sum"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum")
).reset_index()

product_analysis = product_analysis.sort_values(
    by="Total_Profit",
    ascending=False
)

print("\n--- Top 10 Products by Gross Profit ---")
print(product_analysis.head(10).round(2).to_string(index=False))

# Map products to their factories
factory_mapping = {
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

# Add factory name to each record
clean_df["Factory"] = clean_df["Product Name"].map(factory_mapping)

print("\n--- Factory Mapping Check ---")
print("Records without a factory:", clean_df["Factory"].isna().sum())
print(clean_df[["Product Name", "Factory"]].head(10))

# Create factory-to-customer routes
clean_df["Shipping Route"] = (
    clean_df["Factory"]
    + " -> "
    + clean_df["State/Province"].astype(str)
)

# Summarize route performance
route_analysis = clean_df.groupby("Shipping Route").agg(
    Total_Shipments=("Order ID", "count"),
    Average_Lead_Time=("Shipping Lead Time", "mean"),
    Lead_Time_Std=("Shipping Lead Time", "std")
).reset_index()

route_analysis = route_analysis.sort_values(
    by="Average_Lead_Time",
    ascending=True
)

print("\n--- Top 10 Routes by Average Lead Time ---")
print(route_analysis.head(10).round(2).to_string(index=False))

print("\nTotal unique routes:", len(route_analysis))

# Find routes with the highest average lead time
least_efficient_routes = route_analysis.sort_values(
    by="Average_Lead_Time",
    ascending=False
)

print("\n--- Top 10 Routes with Highest Average Lead Time ---")
print(
    least_efficient_routes.head(10)
    .round(2)
    .to_string(index=False)
)

# Find routes with at least 20 shipments
# and rank them by average lead time
busy_routes = route_analysis[
    route_analysis["Total_Shipments"] >= 20
].copy()

busy_routes = busy_routes.sort_values(
    by="Average_Lead_Time",
    ascending=False
)

print("\n--- High-Volume Routes with Highest Lead Times ---")
print(
    busy_routes.head(10)
    .round(2)
    .to_string(index=False)
)

print("\nNumber of routes with at least 20 shipments:",
      len(busy_routes))

# Save route analysis results
route_analysis.to_csv("route_analysis.csv", index=False)

busy_routes.to_csv(
    "high_volume_routes.csv",
    index=False
)

print("\nRoute analysis files saved successfully!")
print("Created: route_analysis.csv")
print("Created: high_volume_routes.csv")