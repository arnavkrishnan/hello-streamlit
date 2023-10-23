# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st

def us_cities_plot():
    def get_city_data():
        df = pd.read_csv("US_city_populations.csv")
        return df.set_index("City")

    try:
        df = get_city_data()
        cities = st.multiselect(
            "Choose cities", list(df.index), ["Abilene (TX)", "Akron (OH)"]
        )
        if not cities:
            st.error("Please select at least one city.")
        else:
            data = df.loc[cities]
            data = data.loc[data["Sex"]=="Both Sexes"]
            data = data.loc[data["City type"]=="City proper"]
            data = data.reset_index()
            chart = (
                alt.Chart(data)
                .mark_line()
                .encode(
                    x="Year:T",
                    y="Value:Q",
                    color="City:N",
                )
            )
            st.write(chart)
            st.line_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="US Cities Population", page_icon="📊")
st.markdown("# US Cities Population")
us_cities_plot()
