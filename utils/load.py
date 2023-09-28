#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 09:25:16 2023

@author: tristan
"""


# =============================================================================
# Imports et librairies.
# =============================================================================

import sqlite3
from datetime import datetime

import streamlit as st

import pandas as pd


# =============================================================================
# Fonctions d'import.
# =============================================================================


@st.cache_data
def load_data():
    """Load data and cache them."""
    # The datasource is a sqlite file. This could be changed, because it is clunky AF.
    database = 'data/database.sqlite'
    conn = sqlite3.connect(database)

    # Informations about players are in two tables, Player_Attributes containes statistics pulled directly from FIFA.
    # The Player table contains misc infos such as height, weight, date of birth.
    # We combine both dataset and it is our data source for most of the dashboard.
    df_player = pd.read_sql(""" SELECT * FROM Player_Attributes """, conn)
    df_player = df_player.sort_values('date').groupby('player_fifa_api_id').tail(1)

    df_playernames = pd.read_sql(""" SELECT player_fifa_api_id, player_name, birthday, height, weight FROM Player """, conn)
    df_player = df_player.merge(df_playernames, on='player_fifa_api_id')
    del df_playernames

    # Some graphs freak out when there are na in the dataset so I drop them like a savage.
    df_player = df_player.dropna()

    # Computing ages.
    df_player['birthday'] = pd.to_datetime(df_player['birthday'])
    df_player['age'] = datetime.today() - df_player['birthday']
    df_player['age'] = df_player['age'].dt.days // 365

    return df_player
