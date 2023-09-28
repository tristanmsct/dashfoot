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
from utils.graphs import graph_pl_info, graph_pl_skill, graph_pl_comp_info, graph_pl_comp_dist, graph_all_scatter_tot

from dashfoot import logger

# =============================================================================
# Player Page.
# =============================================================================

logger.info("Displaying Player Page.")

# Sould always be at the start of the code.
st.set_page_config(
    page_title="FDA - Player Analysis",
    page_icon="img/artichoke_o.png",
    layout="wide"
)

# Loading a few css elements.
with open('css/custom.css', encoding="utf8") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading data, retrieving players and skill lists.
df_player = load_data()

lst_players = df_player['player_name'].unique()
lst_players.sort()

lst_ind = df_player.columns[9:-4]

# Page elements.
# Select boxes for the main player in the side bar.
# Index should be None when not debugging. Otherwise 5699 is Messi.
opt_player = st.sidebar.selectbox('Select a player', lst_players, index=None, placeholder='Player Name')

# Index 1 is good here for testing.
opt_skill = st.sidebar.selectbox('Choose a skill', lst_ind, index=None, placeholder='Skill')

# Constructing our three tabs.
tab_player, tab_comparison, tab_all =\
    st.tabs(["Player Information", "Comparison", "All players"])

# This first tab is for general info on a given player, and the ability to visualise one skill.
with tab_player:
    if opt_player:
        str_title_t1 = f"# Player Info - {opt_player}"
    else:
        str_title_t1: str = "# Choose a player :)"

    st.write(str_title_t1)

    if opt_player:
        info_player = df_player.loc[df_player['player_name'].str.contains(opt_player)]

        graph_pl_info(info_player)

        if opt_skill:
            graph_pl_skill(df_player, info_player, opt_skill)

# This tab is for comparing two players. Main info are placed side by side and both players are put on a graph.
with tab_comparison:
    st.write("# Players Comparison")

    # Index options : 7275 Neymar / 1839 Ronaldo.
    opt_player_2 = st.selectbox('Select a second football player', lst_players, key='pl2', index=None, placeholder='Player Name')

    if opt_player_2 and opt_player:
        info_player_2 = df_player.loc[df_player['player_name'].str.contains(opt_player_2)]

        graph_pl_comp_info(info_player, info_player_2)

        if opt_skill:
            graph_pl_comp_dist(df_player, opt_player, opt_player_2, opt_skill, lst_players)

# This tab is for placing the main selected player in a scatterplot with all other players.
with tab_all:
    st.write("# Player ")

    opt_skill_2: str = None
    if opt_player:
        # Index 9.
        opt_skill_2 = st.selectbox('Choose a second skill', lst_ind, key='sk2', index=None, placeholder='Skill')

    if opt_skill_2:
        graph_all_scatter_tot(df_player, opt_skill, opt_skill_2, info_player, lst_players)
