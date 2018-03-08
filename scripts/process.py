import pandas as pd

from glob import glob
from pathlib import Path

root = Path(__file__).parents[1]
archive_path = root / "archive"
data_path = root / "data"

def save(df, filepath):
    csvname = filepath.lower()
    if csvname.endswith(".xlsx"):
        csvname = csvname.split(". ")[1][:-5].replace(
        ",", "").replace(
        " - ", "-").replace(
        " ", "-").replace(
        "_", "-")
    csvname += ".csv"
    print(csvname)
    df.to_csv(data_path / csvname)

# Global cement emissions
filepath = archive_path / "1. Cement_emissions.xlsx"
cement = pd.read_excel(filepath, sheet_name=0, index_col=0, na_values=-1)

# Columns with only -1 or 0 are read as `int` and have no NaNs yet.
cement = cement.replace(-1, pd.np.nan)

# Remove columns with all NaN.
cement = cement.dropna(how="all", axis=1)

# Yemen is contained as Yemen (twice) and Democratic Yemen, after reading in
# and removing NaNs only the 2nd Yemen ("Yemen.1") has values.
cement = cement.rename(columns={"Yemen.1": "Yemen"})

# Drop all columns with value 0 or NaN, 0 could mean no data or actually zero.
cement = cement.loc[:, ~(cement.sum(axis=0) == 0)]

# Scale cement to match sum of other countries.
cement.World = cement.World * 1000

save(cement, filepath.name)

# UNFCCC data
filepath = archive_path / "2. UNFCCC, 2017 - main.xlsx"
unfccc = pd.read_excel(filepath, sheet_name=0, index_col=0, na_values=-1)

# Countries with pre-1990 data.
filepath = archive_path / "3. UNFCCC, 2017 - extra.xlsx"
unfccc_extra = pd.read_excel(filepath, sheet_name=0, index_col=0, na_values=-1)
unfccc_extra = unfccc_extra.reset_index().pivot(
    index="Year", columns="ISO", values="CO2 (kt)")

# Join them again.
unfccc = unfccc_extra.append(unfccc)

save(unfccc, "unfccc-2017")
