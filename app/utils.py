from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt  # pyright: ignore[reportMissingImports]
import pandas as pd
import seaborn as sns  # pyright: ignore[reportMissingModuleSource]


DEFAULT_VARIABLES = ["T2M", "PRECTOTCORR", "RH2M"]
COUNTRY_COLUMN_CANDIDATES = ["country", "Country", "COUNTRY"]
YEAR_COLUMN_CANDIDATES = ["year", "Year", "YEAR"]
DATA_FILE_PATTERNS = ("*.csv", "*.parquet")


def discover_data_files(data_dir: str | Path = "data") -> list[Path]:
    """Return supported climate dataset files from the data directory."""
    base_path = Path(data_dir)
    if not base_path.exists():
        return []

    files: list[Path] = []
    for pattern in DATA_FILE_PATTERNS:
        files.extend(base_path.rglob(pattern))
    return sorted(files)


def _read_data_file(file_path: Path) -> pd.DataFrame:
    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)
    if file_path.suffix.lower() == ".parquet":
        return pd.read_parquet(file_path)
    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def _find_column(columns: Iterable[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def _normalize_dataframe(
    df: pd.DataFrame, fallback_country: str | None = None
) -> pd.DataFrame:
    data = df.copy()

    country_column = _find_column(data.columns, COUNTRY_COLUMN_CANDIDATES)
    if country_column:
        data = data.rename(columns={country_column: "country"})
    elif fallback_country:
        data["country"] = fallback_country
    else:
        data["country"] = "Unknown"

    year_column = _find_column(data.columns, YEAR_COLUMN_CANDIDATES)
    if year_column and year_column != "year":
        data = data.rename(columns={year_column: "year"})
    elif "year" not in data.columns:
        if "date" in data.columns:
            data["year"] = pd.to_datetime(data["date"], errors="coerce").dt.year
        elif "Date" in data.columns:
            data["year"] = pd.to_datetime(data["Date"], errors="coerce").dt.year
        else:
            raise ValueError(
                "Dataset must include a year column or a parseable date column."
            )

    data["year"] = pd.to_numeric(data["year"], errors="coerce")
    data = data.dropna(subset=["year"]).copy()
    data["year"] = data["year"].astype(int)

    for variable in DEFAULT_VARIABLES:
        if variable in data.columns:
            data[variable] = pd.to_numeric(data[variable], errors="coerce")

    return data


def load_climate_data(data_dir: str | Path = "notebooks/data") -> pd.DataFrame:
    """
    Load all discovered climate files. If no project data exists, return a small
    synthetic sample so the app can still render in Streamlit Community Cloud.
    """
    files = discover_data_files(data_dir)
    print(files)
    if not files:
        return build_demo_dataset()

    frames: list[pd.DataFrame] = []
    for file_path in files:
        fallback_country = file_path.stem.split("_")[0].replace("-", " ").title()
        frame = _normalize_dataframe(
            _read_data_file(file_path), fallback_country=fallback_country
        )
        frames.append(frame)

    combined = pd.concat(frames, ignore_index=True)
    return combined.sort_values(["country", "year"]).reset_index(drop=True)


def build_demo_dataset() -> pd.DataFrame:
    """Generate a lightweight fallback dataset for local development and demos."""
    records: list[dict[str, float | int | str]] = []
    countries = ["Ethiopia", "Kenya", "Nigeria"]
    for country_index, country in enumerate(countries):
        for year in range(2001, 2021):
            offset = year - 2001
            seasonal_wave = (offset % 5) * 0.12
            records.append(
                {
                    "country": country,
                    "year": year,
                    "T2M": 21.0 + country_index * 1.8 + offset * 0.04 + seasonal_wave,
                    "PRECTOTCORR": 48.0 + country_index * 9.5 + (offset % 7) * 3.2,
                    "RH2M": 57.0 + country_index * 4.0 + (offset % 6) * 1.5,
                }
            )
    return pd.DataFrame.from_records(records)


def available_variables(df: pd.DataFrame) -> list[str]:
    return [column for column in DEFAULT_VARIABLES if column in df.columns]


def filter_dataframe(
    df: pd.DataFrame, countries: list[str], year_range: tuple[int, int]
) -> pd.DataFrame:
    filtered = df.copy()
    if countries:
        filtered = filtered[filtered["country"].isin(countries)]

    start_year, end_year = year_range
    filtered = filtered[
        (filtered["year"] >= start_year) & (filtered["year"] <= end_year)
    ]
    return filtered.sort_values(["country", "year"])


def build_temperature_trend_chart(df: pd.DataFrame) -> plt.Figure:
    chart_data = df.copy()
    print(chart_data.head())

    # Ensure Date is datetime
    chart_data["Date"] = pd.to_datetime(chart_data["Date"], errors="coerce")

    # Create monthly period
    chart_data["YearMonth"] = chart_data["Date"].dt.to_period("M").dt.to_timestamp()

    # Monthly average T2M by country
    chart_data = (
        chart_data.groupby(["country", "YearMonth"], as_index=False)["T2M"]
        .mean()
        .sort_values(["country", "YearMonth"])
    )

    # Plot
    fig, ax = plt.subplots(figsize=(14, 6))

    sns.lineplot(
        data=chart_data, x="YearMonth", y="T2M", hue="country", linewidth=2, ax=ax
    )

    ax.set_title("Monthly Average T2M by Country (2015–2026)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Temperature (T2M)")
    ax.grid(alpha=0.25)

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig


def build_precipitation_boxplot(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    country_order = sorted(df["country"].dropna().unique(), key=lambda x: x.lower())
    sns.boxplot(data=df, x="country", y="PRECTOTCORR", ax=ax, order=country_order)
    ax.set_title("Precipitation Distribution by Country")
    ax.set_xlabel("Country")
    ax.set_ylabel("Precipitation (PRECTOTCORR)")
    ax.grid(axis="y", alpha=0.25)
    return fig
