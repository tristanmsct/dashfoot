#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:44:25 2023

@author: tristan
"""

# =============================================================================
# librairies and Imports.
# =============================================================================

import streamlit as st

from utils.load import load_data
from utils.graphs import graph_all_scatter_only, add_player_on_scatter

from dashfoot import logger

# =============================================================================
# Skill Page.
# =============================================================================

logger.info("Displaying Skill Page.")

# Sould always be at the start of the code.
st.set_page_config(
    page_title="Accueil - Analyse Players",
    page_icon="img/artichoke_o.png",
    layout="wide"
)

# Loading a few css elements.
with open('css/custom.css', encoding='utf8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading data, retrieving players and skill lists.
df_player = load_data()

lst_players = df_player['player_name'].unique()
lst_players.sort()

# 9 to -4 are the actual FIFA skills, I got them by hand.
lst_ind = df_player.columns[9:-4]

# Page elements.
# Multiselect boxes for the main player in the side bar.
selected_players = st.sidebar.multiselect('Add players to the graph', lst_players, key="skill_scatter")

# Select box for the main player in the side bar.
selected_skills = st.sidebar.multiselect('Choose a list of skills', lst_ind)

# Create a dictionary to store slider values.
slider_values = {}

# Create sliders based on selected skills.
for skill in selected_skills:
    slider_value = st.sidebar.slider(f"Threshold for {skill}", 0, 100, 0, key=skill)
    slider_values[skill] = slider_value

# Constructing our three tabs.
tab_skill, tab_skill2 =\
    st.tabs(["Skill Filter", "Skill Filter 2"])

with tab_skill:
    # Page elements.
    st.markdown("# Scatter plot of players by age and skills")
    st.markdown("<p style='font-size=10px'><em>Players are presented by age and overall score.\
        Choose skills to filter out players.</em></p>", unsafe_allow_html=True)

    # Filtering our df_player dataframe based on every cutoff created with the sliders.
    for column, cutoff in slider_values.items():
        df_player = df_player[((df_player[column] >= cutoff) | (df_player['player_name'].isin(selected_players)))]

    fig = graph_all_scatter_only(df_player, 'overall_rating', 'age')

    for player in selected_players:
        info_player = df_player.loc[df_player['player_name'].str.contains(player)]
        add_player_on_scatter(fig, info_player, 'overall_rating', 'age')

    fig.update_layout(xaxis_range=[30, 100], yaxis_range=[15, 55], template="simple_white", height=750)
    st.plotly_chart(fig, use_container_width=True)

with tab_skill2:
    # Page elements.
    st.markdown("# Scatter plot of players and skill filtering")
    st.markdown("<p style='font-size=10px'><em>A graph a created from the two first selected skills, but any number can be selected.\
        Then use the sliders to filter out players based on skill thresholds.</em></p>", unsafe_allow_html=True)

    if len(slider_values) >= 2:

        # Filtering our df_player dataframe based on every cutoff created with the sliders.
        for column, cutoff in slider_values.items():
            df_player = df_player[((df_player[column] >= cutoff) | (df_player['player_name'].isin(selected_players)))]

        # The graph is only created based on the first two skills, other are just used as cutoffs.
        skill_1 = list(slider_values.keys())[0]
        skill_2 = list(slider_values.keys())[1]

        fig = graph_all_scatter_only(df_player, skill_1, skill_2)

        for player in selected_players:
            info_player = df_player.loc[df_player['player_name'].str.contains(player)]
            add_player_on_scatter(fig, info_player, skill_1, skill_2)

        fig.update_layout(xaxis_range=[0, 100], yaxis_range=[0, 100], template="simple_white", height=750)
        st.plotly_chart(fig, use_container_width=True)
