import polars as pl
from pycapitol import normalize
import streamlit as st


def normalize_citation(leg_number):
    return normalize(leg_number)


st.title(
    "Congress.gov Legislation Text Search to Legislation Search Citation Converter"
)
st.markdown("""
Upload your downloaded and unchanged search results from Congress.gov's legislation text search form below.

A comma-separated string of bill citations will be displayed, which you can copy and paste into the Legislation and Law Numbers field on Congress.gov's legislation search page.
""")

st.subheader("Upload CSV file of Legislation Text search results")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="lt")

if uploaded_file is not None:
    df = pl.read_csv(uploaded_file, skip_lines=3)
    df_with_cite = df.with_columns(
        (
            pl.col("Congress").cast(pl.String)
            + pl.col("Legislation Number").map_elements(
                normalize_citation, return_dtype=pl.String
            )
        ).alias("cite")
    )
    df_cite_agg = df_with_cite.select(pl.col("cite").unique().str.join(", "))
    search_string = str(df_cite_agg["cite"].item(0))

    st.subheader("Legislation form search string:")
    st.write(search_string)
    st.write(
        "Paste the string above into the `Legislation and Law Numbers` field on the [Congress.gov](https://www.congress.gov/) legislation search form. **Be sure to select `93-119 (1973-2026)` in the `Congress (Years) field`!**"
    )
else:
    st.info("Please upload a CSV file")
