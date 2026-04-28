import streamlit as st

from utils import (
    available_variables,
    build_precipitation_boxplot,
    build_temperature_trend_chart,
    discover_data_files,
    filter_dataframe,
    load_climate_data,
)


st.set_page_config(
    page_title="Climate Insights Dashboard",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def get_data():
    return load_climate_data()


def main() -> None:
    st.title("Interactive Climate Dashboard")
    st.caption("Explore temperature, precipitation, and humidity patterns across countries and years.")

    df = get_data()
    variable_options = available_variables(df)
    has_project_data = bool(discover_data_files())

    if df.empty:
        st.error("No climate records were found. Add CSV or Parquet files to `data/` and rerun the app.")
        return
    if not variable_options:
        st.error("The dataset is missing supported variables. Expected one of: T2M, PRECTOTCORR, RH2M.")
        return

    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    country_options = sorted(df["country"].dropna().unique().tolist())

    if not has_project_data:
        st.info("No files were found in `data/`, so the dashboard is showing a built-in demo dataset.")

    st.sidebar.header("Filters")
    selected_countries = st.sidebar.multiselect(
        "Select countries",
        options=country_options,
        default=country_options,
    )
    selected_years = st.sidebar.slider(
        "Select year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    selected_variable = st.sidebar.selectbox(
        "Select variable",
        options=variable_options,
        index=0,
    )

    filtered_df = filter_dataframe(df, selected_countries, selected_years)
    if filtered_df.empty:
        st.warning("No records match the current filters.")
        return

    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Countries", filtered_df["country"].nunique())
    metric_2.metric("Years", filtered_df["year"].nunique())
    metric_3.metric(
        f"Mean {selected_variable}",
        f"{filtered_df[selected_variable].mean():.2f}",
    )

    line_col, box_col = st.columns(2)
    with line_col:
        st.subheader("Temperature Trend")
        st.pyplot(build_temperature_trend_chart(filtered_df), use_container_width=True)

    with box_col:
        st.subheader("Precipitation Distribution")
        st.pyplot(build_precipitation_boxplot(filtered_df), use_container_width=True)

    st.subheader(f"{selected_variable} Snapshot")
    summary = (
        filtered_df.groupby(["country", "year"], as_index=False)[selected_variable]
        .mean()
        .sort_values(["country", "year"])
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.caption("Charts and summary table reflect the active country and year filters.")


if __name__ == "__main__":
    main()
