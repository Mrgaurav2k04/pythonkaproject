# fertilizer_analysis_final.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Dark theme for aesthetics
plt.style.use("dark_background")
sns.set_theme(style="darkgrid", palette="Set2", font_scale=1.2)

# Load dataset
df = pd.read_csv("ICRISAT-District Level Data.csv")

# Rename columns for clarity
df.rename(columns={
    'Dist Code': 'District_Code',
    'Year': 'Year',
    'State Code': 'State_Code',
    'State Name': 'State',
    'Dist Name': 'District',
    'NITROGEN CONSUMPTION (tons)': 'Nitrogen_tons',
    'NITROGEN SHARE IN NPK (Percent)': 'Nitrogen_percent',
    'NITROGEN PER HA OF NCA (Kg per ha)': 'Nitrogen_per_ha_NCA',
    'NITROGEN PER HA OF GCA (Kg per ha)': 'Nitrogen_per_ha_GCA',
    'PHOSPHATE CONSUMPTION (tons)': 'Phosphate_tons',
    'PHOSPHATE SHARE IN NPK (Percent)': 'Phosphate_percent',
    'PHOSPHATE PER HA OF NCA (Kg per ha)': 'Phosphate_per_ha_NCA',
    'PHOSPHATE PER HA OF GCA (Kg per ha)': 'Phosphate_per_ha_GCA',
    'POTASH CONSUMPTION (tons)': 'Potash_tons',
    'POTASH SHARE IN NPK (Percent)': 'Potash_percent',
    'POTASH PER HA OF NCA (Kg per ha)': 'Potash_per_ha_NCA',
    'POTASH PER HA OF GCA (Kg per ha)': 'Potash_per_ha_GCA',
    'TOTAL CONSUMPTION (tons)': 'Total_tons',
    'TOTAL PER HA OF NCA (Kg per ha)': 'Total_per_ha_NCA',
    'TOTAL PER HA OF GCA (Kg per ha)': 'Total_per_ha_GCA'
}, inplace=True)

# Remove any rows with missing essential values
df.dropna(subset=["Year", "State", "Total_tons"], inplace=True)

# 1. Total Fertilizer Consumption Over the Years
yearly_totals = df.groupby("Year")["Total_tons"].sum().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=yearly_totals, x="Year", y="Total_tons", linewidth=2.5)
plt.title("India-Wide Total Fertilizer Consumption Over the Years")
plt.xlabel("Year")
plt.ylabel("Total Fertilizer Consumption (tons)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Top States by Average Fertilizer Use
state_avg_total = df.groupby("State")["Total_tons"].mean().sort_values(ascending=False).reset_index()
plt.figure(figsize=(12, 8))
sns.barplot(data=state_avg_total.head(15), x="Total_tons", y="State", palette="Set3")
plt.title("Top 15 States by Average Annual Fertilizer Consumption")
plt.xlabel("Average Fertilizer Consumption (tons)")
plt.ylabel("State")
plt.tight_layout()
plt.show()

# 3. NPK Share Pie Chart
npk_share = df[["Nitrogen_percent", "Phosphate_percent", "Potash_percent"]].mean()
plt.figure(figsize=(6, 6))
colors = sns.color_palette("Set1")
npk_share.plot(kind="pie", autopct="%1.1f%%", startangle=140, colors=colors)
plt.title("Average NPK Share in Fertilizer Consumption")
plt.ylabel("")
plt.tight_layout()
plt.show()

# 4. Heatmap: Fertilizer Use by State-Year
heatmap_data = df.groupby(["State", "Year"])["Total_tons"].mean().reset_index()
heatmap_pivot = heatmap_data.pivot(index="State", columns="Year", values="Total_tons")
plt.figure(figsize=(16, 10))
sns.heatmap(heatmap_pivot, cmap="coolwarm", linewidths=0.5)
plt.title("Heatmap of Average Fertilizer Usage by State and Year")
plt.xlabel("Year")
plt.ylabel("State")
plt.tight_layout()
plt.show()

# 5. Fertilizer per Hectare (NCA vs GCA)
per_ha_df = df[["Year", "Total_per_ha_NCA", "Total_per_ha_GCA"]].groupby("Year").mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=per_ha_df, x="Year", y="Total_per_ha_NCA", label="Per ha NCA", linewidth=2.5)
sns.lineplot(data=per_ha_df, x="Year", y="Total_per_ha_GCA", label="Per ha GCA", linewidth=2.5)
plt.title("Fertilizer Consumption per Hectare (NCA vs GCA)")
plt.xlabel("Year")
plt.ylabel("Fertilizer per ha (Kg)")
plt.legend()
plt.tight_layout()
plt.show()

# 6. Correlation Heatmap of Usage Metrics
correlation_features = [
    "Nitrogen_tons", "Phosphate_tons", "Potash_tons",
    "Total_tons", "Total_per_ha_NCA", "Total_per_ha_GCA"
]
correlation_matrix = df[correlation_features].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="viridis", linewidths=0.5)
plt.title("Correlation Matrix of Fertilizer Usage Metrics")
plt.tight_layout()
plt.show()

# 7. NPK Year-wise Area Chart
yearly_npk = df.groupby("Year")[["Nitrogen_tons", "Phosphate_tons", "Potash_tons"]].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.stackplot(yearly_npk["Year"],
              yearly_npk["Nitrogen_tons"],
              yearly_npk["Phosphate_tons"],
              yearly_npk["Potash_tons"],
              labels=["Nitrogen", "Phosphate", "Potash"],
              colors=sns.color_palette("Set2", 3))
plt.title("Year-wise NPK Fertilizer Usage in India")
plt.xlabel("Year")
plt.ylabel("Total Usage (tons)")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
