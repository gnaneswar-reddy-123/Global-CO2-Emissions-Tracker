"""
Global CO2 Emissions Tracker by Sector
Data preparation for Tableau dashboard.

Project requirements:
- Multi-year emissions data
- Country-level analysis
- Sector-level analysis
- Per-capita emissions
- Per-GDP emissions

Source:
Our World in Data CO2 dataset
https://github.com/owid/co2-data
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

DATA_URL = (
    "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
)


def load_data():
    print("Loading Our World in Data CO2 dataset...")

    df = pd.read_csv(DATA_URL)

    print(f"Raw rows: {len(df):,}")
    print(f"Raw columns: {len(df.columns)}")

    return df


def clean_data(df):
    required_columns = [
        "country",
        "year",
        "population",
        "gdp",
        "co2",
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df = df[required_columns + [
        "iso_code",
        "coal_co2",
        "oil_co2",
        "gas_co2",
        "cement_co2",
        "flaring_co2",
        "other_industry_co2",
    ]].copy()

    df = df.dropna(
        subset=["country", "year", "co2"]
    )

    df["country"] = df["country"].astype(str).str.strip()

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    numeric_columns = [
        "population",
        "gdp",
        "co2",
        "coal_co2",
        "oil_co2",
        "gas_co2",
        "cement_co2",
        "flaring_co2",
        "other_industry_co2",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.drop_duplicates(
        subset=["country", "year"]
    )

    return df


def calculate_metrics(df):
    # OWID CO2 is measured in million tonnes.
    # Convert to tonnes for per-person calculations.
    df["co2_tonnes"] = df["co2"] * 1_000_000

    df["emissions_per_capita"] = (
        df["co2_tonnes"] / df["population"]
    )

    df["emissions_per_gdp"] = (
        df["co2_tonnes"] / df["gdp"]
    )

    # Create a clean intensity metric in tonnes CO2
    # per million international dollars of GDP.
    df["co2_per_million_gdp"] = (
        df["co2_tonnes"] /
        (df["gdp"] / 1_000_000)
    )

    return df


def create_sector_data(df):
    """
    Create sector/source-level records from the
    available OWID emissions components.

    These are source-based categories rather than
    claiming that each source is an economic sector.
    """

    sector_columns = {
        "Coal": "coal_co2",
        "Oil": "oil_co2",
        "Gas": "gas_co2",
        "Cement": "cement_co2",
        "Flaring": "flaring_co2",
        "Other Industry": "other_industry_co2",
    }

    records = []

    base_columns = [
        "country",
        "iso_code",
        "year",
        "population",
        "gdp",
    ]

    for sector_name, column in sector_columns.items():

        if column not in df.columns:
            continue

        temp = df[base_columns + [column]].copy()

        temp = temp.rename(
            columns={column: "sector_co2_mt"}
        )

        temp["sector"] = sector_name

        temp = temp.dropna(
            subset=["sector_co2_mt"]
        )

        temp["sector_co2_tonnes"] = (
            temp["sector_co2_mt"] * 1_000_000
        )

        temp["sector_emissions_per_capita"] = (
            temp["sector_co2_tonnes"] /
            temp["population"]
        )

        temp["sector_emissions_per_gdp"] = (
            temp["sector_co2_tonnes"] /
            temp["gdp"]
        )

        records.append(temp)

    sector_df = pd.concat(
        records,
        ignore_index=True
    )

    return sector_df


def main():

    df = load_data()

    print("Cleaning data...")
    df = clean_data(df)

    print("Calculating metrics...")
    df = calculate_metrics(df)

    print("Creating sector-level data...")
    sector_df = create_sector_data(df)

    country_output = (
        PROCESSED_DIR /
        "co2_country_year_processed.csv"
    )

    sector_output = (
        PROCESSED_DIR /
        "co2_sector_processed.csv"
    )

    df.to_csv(
        country_output,
        index=False
    )

    sector_df.to_csv(
        sector_output,
        index=False
    )

    print("\nSUCCESS!")
    print("-" * 50)

    print(
        f"Country/year file: {country_output}"
    )

    print(
        f"Sector file: {sector_output}"
    )

    print(
        f"Country/year rows: {len(df):,}"
    )

    print(
        f"Sector rows: {len(sector_df):,}"
    )

    print(
        f"Years: {int(df['year'].min())} "
        f"to {int(df['year'].max())}"
    )

    print(
        f"Countries/locations: "
        f"{df['country'].nunique():,}"
    )

    print("\nFiles are ready for Tableau.")


if __name__ == "__main__":
    main()