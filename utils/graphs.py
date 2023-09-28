#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:25:39 2023

@author: tristan
"""

import streamlit as st

import plotly.figure_factory as ff
import plotly.graph_objects as go


def graph_pl_info(info_player):
    """Displays player informations.

    Args:
        info_player (pd.DataFrame): A one line DataFrame with information about the player.
    """
    st.text("")
    st.text("")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Height", f"{info_player['height'].values[0]} cm")
    col2.metric("Weight", f"{info_player['weight'].values[0]} lbs")
    col3.metric("Preferred foot", f"{info_player['preferred_foot'].values[0]}")
    col4.metric("Age", f"{info_player['age'].values[0]}")

    st.text("")
    st.text("")
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Defensive Work Rate", f"{info_player['defensive_work_rate'].values[0]}")
    col6.metric("Attacking Work Rate", f"{info_player['attacking_work_rate'].values[0]}")
    col7.metric("Overall Rating", f"{info_player['overall_rating'].values[0]}")
    col8.metric("Potential", f"{info_player['potential'].values[0]}")


def graph_pl_dist_skill(dist_skill, str_skill):
    """Display the distribution for a given skill"""
    # TODO : the text on hover on the curve is nasty. Does not seem possible because curves like that are made with
    # figure factory, and are not really supported with graph object.
    fig = ff.create_distplot(
        [dist_skill], [f'Distribution of {str_skill}'],
        bin_size=5,
        show_rug=False, show_hist=False,
        curve_type='kde',
        colors=['#9BF6FA'],
    )

    return fig


def get_coord_on_dist(fig, target_x):
    """Get the coordinates of a player on the distribution.

    For a given skill distribution, the x coordinate is easy to get because it is the skill value of the player.
    The y coordinate is much harder to get and can be "guessed" iteratively by looking at the interval where the
    x axis of the distribution contains the x value of the player and taking the corresponding y.
    """
    # Get the data from the plot, x and y coordinates of the curve.
    hist_data = fig['data'][0]['x']
    hist_y = fig['data'][0]['y']

    # Iterate through the histogram data to find the x coordinate for the target y value.
    # I kind of looked for a better, more elegent solution but could not really find one.
    # It is mainly okay but could get problematic with huge dataset, which should never be the case.
    # One optimisation could be to go through the graph in reverse because we are most likely to search
    # for player at the top of the list rather than the bottom, but it is some silly optimisation.
    y_coordinate = None
    for i, elt in enumerate(hist_data):
        if elt >= target_x:
            y_coordinate = hist_y[i]
            break
    if not y_coordinate:
        y_coordinate = hist_y[-1]

    return y_coordinate


def add_player_on_dist(fig, target_x, y_coordinate, info_player, str_skill, str_color='#9BF6FA'):
    """Add a signle point for a player on a distribition."""
    fig.add_trace(
        go.Scatter(
            mode='markers+text',
            x=[target_x],
            y=[y_coordinate],
            marker=dict(
                color=str_color,
                size=20,
            ),
            showlegend=False,
            text=f"<b>{info_player['player_name'].values[0]}</b>",
            hovertemplate=f"<b>{info_player['player_name'].values[0]}</b><br>{str_skill} : {target_x:.2f}",
            textposition="bottom center",
            name='',
        )
    )


def graph_pl_skill(df_player, info_player, option_skill=None):
    """Graph the whole distribution for one skill and plot a point for the selected player."""
    # For display purposes. Would be nice to have this in the selectbox too.
    str_skill = option_skill.replace('_', ' ').title()

    st.markdown(f"""### {str_skill} Graph.""")

    # Displaying the whole distribution.
    dist_skill = df_player[option_skill]
    fig = graph_pl_dist_skill(dist_skill, str_skill)

    # adding the player on the distribution.
    target_x = info_player[option_skill].values[0]
    y_coordinate = get_coord_on_dist(fig, target_x)
    add_player_on_dist(fig, target_x, y_coordinate, info_player, str_skill)

    # Conf and display the graph.
    fig.update_layout(xaxis_range=[0, 100], template="simple_white", hovermode="closest")
    st.plotly_chart(fig, use_container_width=True)


def graph_pl_comp_info(info_player, player_2_info):
    """Displays comparison information between two players."""
    col1, col2 = st.columns(2)

    col1.markdown(f"# {info_player['player_name'].values[0]}")
    col1.metric("Defensive Work Rate", f"{info_player['defensive_work_rate'].values[0]}")
    col1.metric("Attacking Work Rate", f"{info_player['attacking_work_rate'].values[0]}")
    col1.metric("Overall Rating", f"{info_player['overall_rating'].values[0]}")

    # TODO : this column should be using green as a highlight color. Does not seem possible withou
    # creating custom streamlit components which is an absolute chore.
    col2.markdown(f"# {player_2_info['player_name'].values[0]}")
    col2.metric("Defensive Work Rate", f"{player_2_info['defensive_work_rate'].values[0]}")
    col2.metric("Attacking Work Rate", f"{player_2_info['attacking_work_rate'].values[0]}")
    col2.metric("Overall Rating", f"{player_2_info['overall_rating'].values[0]}")


def graph_pl_comp_dist(df_player, opt_player, opt_player_2, opt_skill, lst_players):
    """Displays a distribution for a given skill with multiple players."""
    str_skill = opt_skill.replace('_', ' ').title()

    info_player = df_player.loc[df_player['player_name'].str.contains(opt_player)]
    info_player_2 = df_player.loc[df_player['player_name'].str.contains(opt_player_2)]

    st.markdown(f"""### {str_skill} Graph.""")

    selected_players = st.multiselect('Add more players to the list', lst_players)

    # Display first the whole distribution of all players for a given skill.
    dist_skill = df_player[opt_skill]
    fig = graph_pl_dist_skill(dist_skill, str_skill)

    # Then add the main player and the other player to compare.
    target_x = info_player[opt_skill].values[0]
    target_2_x = info_player_2[opt_skill].values[0]
    y_coordinate = get_coord_on_dist(fig, target_x)
    y_2_coordinate = get_coord_on_dist(fig, target_2_x)
    add_player_on_dist(fig, target_x, y_coordinate, info_player, str_skill)
    add_player_on_dist(fig, target_2_x, y_2_coordinate, info_player_2, str_skill, str_color="#67f59b")

    for player in selected_players:
        info_player_add = df_player.loc[df_player['player_name'].str.contains(player)]
        target_p_x = info_player_add[opt_skill].values[0]
        y_p_coordinate = get_coord_on_dist(fig, target_p_x)
        add_player_on_dist(fig, target_p_x, y_p_coordinate, info_player_add, str_skill, str_color="#D152C5")

    # Conf and display the graph.
    fig.update_layout(xaxis_range=[0, 100], template="simple_white", hovermode="closest")
    st.plotly_chart(fig, use_container_width=True)


def graph_all_scatter_only(df_player, opt_skill, opt_skill_2):
    """Display the scatter plot with all player without highlighting one in particular."""
    fig =\
        go.Figure(
            data=go.Scatter(
                x=df_player[opt_skill], y=df_player[opt_skill_2],
                mode='markers',
                marker=dict(color='#67f59b'),
                showlegend=False,
                text=df_player.apply(lambda row: f"Player: {row['player_name']}\
                    <br>{opt_skill}: \t{row[opt_skill]}<br>{opt_skill_2}: \t{row[opt_skill_2]}", axis=1),
                hovertemplate='%{text}',
                name='',
                )
            )

    return fig


def add_player_on_scatter(fig, info_player, opt_skill, opt_skill_2, str_color='#9BF6FA'):
    """Add a player to highlight on the scatter plot."""
    fig.add_trace(
        go.Scatter(
            mode='markers+text',
            x=[info_player[opt_skill].values[0]],
            y=[info_player[opt_skill_2].values[0]],
            marker=dict(
                color=str_color,
                size=20,
            ),
            showlegend=False,
            text=f"<b>{info_player['player_name'].values[0]}</b>",
            hovertemplate=info_player.apply(lambda row: f"Player: {row['player_name']}\
                <br>{opt_skill}: {row[opt_skill]}<br>{opt_skill_2}: {row[opt_skill_2]}", axis=1),
            name='',
            textposition='bottom center',
        )
    )


def graph_all_scatter_tot(df_player, opt_skill, opt_skill_2, info_player, lst_players):
    """Displays a scatter plot for two skills with the main player highlighted."""
    str_skill = opt_skill.replace('_', ' ').title()
    str_skill_2 = opt_skill_2.replace('_', ' ').title()
    st.markdown(f"""### Scatter plot of {str_skill} and {str_skill_2}.""")

    selected_players = st.multiselect('Add more players to the list', lst_players, key="multi_scatter")

    fig = graph_all_scatter_only(df_player, opt_skill, opt_skill_2)

    add_player_on_scatter(fig, info_player, opt_skill, opt_skill_2)

    for player in selected_players:
        info_player_add = df_player.loc[df_player['player_name'].str.contains(player)]
        add_player_on_scatter(fig, info_player_add, opt_skill, opt_skill_2, str_color="#D152C5")

    # Conf and display the graph.
    fig.update_layout(
        xaxis_title=opt_skill,
        yaxis_title=opt_skill_2,
        height=750,
        width=750,
        template='simple_white',
    )
    st.plotly_chart(fig, use_container_width=True)
