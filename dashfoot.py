#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:17:50 2023

@author: tristan
"""

# Pour la configuration de la connextion.
# https://docs.streamlit.io/library/advanced-features/configuration
# https://docs.streamlit.io/knowledge-base/deploy/remote-start

# =============================================================================
# Imports et librairies.
# =============================================================================


import streamlit as st

from utils import logger_utils

# Initialize the logger
logger = logger_utils.configure_logger()

# =============================================================================
# Fonction principale.
# =============================================================================


def run():
    """Contains the main page."""
    logger.info('Displaying main page.')

    # Sould always be at the start of the code.
    st.set_page_config(
        page_title="Football Data Analysis",
        page_icon="img/artichoke_o.png",
    )

    st.sidebar.success("Selectionnez une page.")

    st.write("# Football Data Analysis")
    st.text('')

    st.image('img/artichoke_o.png', width=100)

    st.text('')
    st.markdown(
        """
        <br>
        <hr>
        <p style="font-size:24px">Based on historical data from 2006 to 2016, taken from several \
            sources we have gathered informations about leagues,\
            matchs, teams, and players.</p>
        <p style="font-size:24px">The goal of this Dashboard is to showcase these data through several angle.
        <div>
        <ul>
            <li style="font-size:24px">Analysing a single player and comparing him to others.</li>
            <li style="font-size:24px">Filtering and matching skills to find the better suited player.</li>
            <li style="font-size:24px">Analysing teams and finding the better player to get for a position.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# Starting the program.
# =============================================================================


if __name__ == "__main__":
    run()
