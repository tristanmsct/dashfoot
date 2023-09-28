#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 17:38:34 2023

@author: tristan
"""

# =============================================================================
# librairies and Imports.
# =============================================================================

import streamlit as st

import pandas as pd

from sklearn.neighbors import NearestNeighbors

from utils.load import load_data
from utils.graphs import graph_all_scatter_only, add_player_on_scatter

from dashfoot import logger

# =============================================================================
# Skill Page.
# =============================================================================

logger.info("Displaying Search Page.")

# Sould always be at the start of the code.
st.set_page_config(
    page_title="FDA - Search Similar Players",
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
st.markdown('# Search function of similar players to a model')

# Select boxes for the main player in the side bar.
# Index should be None when not debugging. Otherwise 5699 is Messi.
opt_player = st.sidebar.selectbox('Select a player', lst_players, index=None, placeholder='Player Name')

# Used with the KNN with a +1 because the player himself is always is nearest neighbor.
sl_neigh = st.sidebar.slider("Number of similar players wanted", 0, 20, 5, key='sl_neigh')

opt_skill = st.sidebar.selectbox('Choose a first skill', lst_ind, index=None, key="p3sk1", placeholder='Skill')
opt_skill_2 = st.sidebar.selectbox('Choose a second skill', lst_ind, key="p3sk2", index=None, placeholder='Skill')

# Can't do anything without these two skills so everything else is wrapped in this if.
if opt_skill and opt_skill_2:

    # A secondary skill search is enabled without the two already selected skills.
    lst_ind_cp = list(lst_ind)
    lst_ind_cp.remove(opt_skill)
    lst_ind_cp.remove(opt_skill_2)
    selected_skills = st.sidebar.multiselect('Choose additional skills', lst_ind_cp)

    # Same thing, can't do anything is no player is selected.
    if opt_player:
        # Using all skills or only selected skill to train the KNN.
        bx_skills = st.sidebar.checkbox('Use only selected skills')

        # If this is ticked, each row (player) is normalised by himself. This allows to find players
        # who have a similar skill distribution but a different overall score.
        # Player A (finishing 80 ; dribbling 60) is similar to player B (finishing 50 ; dribbling 35) if we
        # normalise but not otherwise.
        bx_norm = st.sidebar.checkbox('Normalise Research')

        st.sidebar.markdown("<p style='font-size=6px'><em>Normalising the search allow\
            to look for players with similar skill profile but a smaller overall score.</em></p>", unsafe_allow_html=True)

        # Creating a copy of the dataframe because we may have to normalise some skills and if we do the graph
        # gets out of wack. It absolutly pains me to do something so disgusting but I will have to do better later.
        df_search = df_player.copy()

        # Normalisation function, the 9:-6 is nasty, should do better.
        if bx_norm:
            df_search.iloc[:, 9:-6] = df_search.iloc[:, 9:-6].apply(lambda row: row / max(row), axis=1)

        # Treating the two cases separately but it could be simplet with only a list created in the if and the list being
        # used regardless of its content with the dataframe.
        if bx_skills:
            lst_skills = [opt_skill, opt_skill_2] + selected_skills
            neigh = NearestNeighbors(n_neighbors=2, radius=0.4)
            neigh.fit(df_search.loc[:, lst_skills])

            lst_sim_players = neigh.kneighbors(
                df_search.loc[df_search['player_name'].str.contains(opt_player)].loc[:, lst_skills].values, sl_neigh + 1,
                return_distance=False
                )[0]
        else:
            neigh = NearestNeighbors(n_neighbors=2, radius=0.4)
            neigh.fit(df_search.iloc[:, 9:-6])

            lst_sim_players = neigh.kneighbors(
                df_search.loc[df_search['player_name'].str.contains(opt_player)].iloc[:, 9:-6].values, sl_neigh + 1,
                return_distance=False
                )[0]

        fig = graph_all_scatter_only(df_player, opt_skill, opt_skill_2)

        for ind_player in lst_sim_players:
            info_player = pd.DataFrame(df_player.iloc[ind_player]).T
            add_player_on_scatter(fig, info_player, opt_skill, opt_skill_2)

        fig.update_layout(xaxis_range=[0, 100], yaxis_range=[0, 100], template="simple_white", height=750)
        st.plotly_chart(fig, use_container_width=True)
