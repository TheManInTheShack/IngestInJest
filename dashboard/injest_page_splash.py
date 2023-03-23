# ==================================================================================================
# splash page
# ==================================================================================================

# ==================================================================================================
# Imports
# ==================================================================================================
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

from app import app

from lib import *

# ==================================================================================================
# Init
# ==================================================================================================
print("...loading splash page...")

# ==================================================================================================
# Layout
# ==================================================================================================
def layout_splash(init_dict):
    # ==============================================================================================
    # Start
    # ==============================================================================================

    # ==============================================================================================
    # Grab the information from the init
    # ==============================================================================================
    style_default      = init_dict['style_default']    
    data               = init_dict['data']                         
    pages              = init_dict['pages']
    footnote           = init_dict['footnote']
    title              = init_dict['title']

    # ==============================================================================================
    # Sort out the data
    # ==============================================================================================

    # ------------------------------------------------------------------------------
    # Stuff for the splash page blurb
    # ------------------------------------------------------------------------------
    total_shows        = len(data['Gigs'])
    total_performances = len(data['Performances'])
    total_songs        = len(data['Songs'])
    total_albums       = len(data['Albums'])
    total_artists      = len(data['Bands'])
    min_year           = data['Songs']['Year'].min()
    max_year           = data['Songs']['Year'].max()
    year_span          = max_year - min_year + 1


    splash_image = 'ch1.png'
    image = html.Div([ html.Img( src = app.get_asset_url(splash_image)) ],
            className = 'col-md-5',
            style = { 'align-items': 'center', 'padding-top' : '1%'})

    blurb_1 = "Chris Holt is an award-winning multi-instrumentalist and musical encyclopedia.  Prior to 2020, he made most of his living by playing live, mostly to local crowds in Dallas, but occasionally touring with Don Henley's band and sharing the stage with many of his musical heroes.  When the Covid-19 lockdowns changed the nature of what live performance had to be, Chris put his phone on a tripod and started streaming on Facebook once a week, working strictly on tips.  It's still going on.  Three hours a week, from 7pm to 10pm Central time on Thursdays, Chris works away at an endless list of requests from a group of his fans from all over the world.  He performs every piece himself, using his collection of instruments, by building up the layers of each song in loops, then finally performing each song in its entirety.  Each week he amazes his viewers by producing from scratch a full set of music from his vast store of knowledge, performed by a world-class musician."
    blurb_2 = "So far, there have been {} shows in this series, in which Chris has done {} performances of {} songs from {} albums by {} artists, spanning {} years of music."
    blurb_2 = blurb_2.format(str(total_shows), str(total_performances), str(total_songs), str(total_albums), str(total_artists), str(year_span))
    blurb_3 = "All by himself, right in front of your eyes, song by song...welcome to the world of All Request Thursdays."
    blurbs = [blurb_1, blurb_2, blurb_3]

    blob = []
    for blurb in blurbs:
        blob.append(html.P(blurb))

    text_block = html.Div(blob, className = 'col-md-5')

    row = html.Div([get_empty_col(), image, text_block, get_empty_col()], className = 'row')

    splash_blob = html.Div([get_empty_row(), row])

    # ------------------------------------------------------------------------------
    # Stuff for the last-setlist table 
    # ------------------------------------------------------------------------------
    data_performances = get_data_performances(data)
    data_last_setlist = data_performances.loc[data_performances['Show']==max(data_performances['Show'])]

    # ------------------------------------------------------------------------------
    # Data for individual charts
    # ------------------------------------------------------------------------------
    data_num_songs_by_artist = get_data_num_songs_by_artist(data, minsongs=10)
    data_num_songs_by_year   = get_data_num_songs_by_year(data)

    # ==============================================================================================
    # Page Contents Configuration
    # ==============================================================================================
    # ------------------------------------------------------------------------------
    # Chart information
    # ------------------------------------------------------------------------------
    charts_1={}
    charts_1['num_songs_by_artist'] = {'chart_type':'bar', 
                                       'idx':'chart_num_songs_by_artist', 
                                       'details':{'data':data_num_songs_by_artist,
                                                     'x':'Originating Artist',
                                                     'y':['Number of Songs Played'], 
                                                 'color':"CH Original", 
                                                 'style':style_default}}

    charts_2={}
    charts_2['num_songs_by_year']   = {'chart_type':'bar', 
                                              'idx':'chart_num_songs_by_year', 
                                          'details':{'data': data_num_songs_by_year,
                                                        'x': "Year of Song's Origination",
                                                        'y': ['Number of Songs Played'], 
                                                    'style': style_default}}

    # ------------------------------------------------------------------------------
    # Control information
    #bu_opt = [{'label':i,'value':i} for i in list_all_depts]
    #time_opt = [{'label':i,'value':i} for i in ddata['year'].to_list()]
    #controls['business_unit']      = {'control_type':'dropdown', 'idx':'ctl_bu'        , 'details':{'options':bu_opt       , 'multi':True     ,'value':[]    ,'style':style_default   ,'title':'business_unit'}}
    #controls['time_granularity']   = {'control_type':'dropdown', 'idx':'ctl_timegran'  , 'details':{'options':time_opt       , 'multi':True     ,'value':[]    ,'style':style_default   ,'title':'time_granularity'}}
    #controls['refresh']            = {'control_type':'button'  , 'idx':'ctl_refresh'   , 'details':{'label':"Refresh"  , 'title':'refresh'}}
    # ------------------------------------------------------------------------------
    controls_1={}

    controls_2={}

    # ------------------------------------------------------------------------------
    # General layout information
    # ------------------------------------------------------------------------------
    layout_1={}
    layout_1['chart_shape']     = "1x1"
    layout_1['style_default']   = style_default
    layout_1['controls_orient'] = "top"

    layout_2={}
    layout_2['chart_shape']     = "1x1"
    layout_2['style_default']   = style_default
    layout_2['controls_orient'] = "top"

    # ==============================================================================================
    # Component layout
    # ==============================================================================================
    # ------------------------------------------------------------------------------
    # Compile components
    # ------------------------------------------------------------------------------
    components = []
    components.append(get_navbar(pages, title))

    components.append(splash_blob)

    components.extend(display_simple_table(data_last_setlist, idx="splash_setlist_table", title="Setlist from latest show"))

    components.append(html.Br())
    components.append(html.H2("Number of Songs by Artist (at least ten songs played)", style=style_default))
    components.append(charts_with_controls(charts_1, controls_1, layout_1))

    components.append(html.Br())
    components.append(html.H2("Number of Songs by Year of Origination", style=style_default))
    components.append(charts_with_controls(charts_2, controls_2, layout_2))

    components.append(get_footnote(footnote))

    # ------------------------------------------------------------------------------
    # Top Level
    # ------------------------------------------------------------------------------
    layout_splash = html.Div(components, style=style_default)
    return layout_splash

    # ==============================================================================================
    # Callbacks
    # ==============================================================================================


# ==================================================================================================
# Data functions specific to this page
# ==================================================================================================
# ------------------------------------------------------------------------------
# Get data needed for specific chart
# Number of different songs played by artist (with minimum)
# ------------------------------------------------------------------------------
def get_data_num_songs_by_artist(data, minsongs=0):
    # --------------------------------------------------------------------------
    # Get the whole count
    # --------------------------------------------------------------------------
    count = data['Songs']['Band'].value_counts(sort=True, ascending=False)

    # --------------------------------------------------------------------------
    # Reset the minimum if requested
    # --------------------------------------------------------------------------
    if minsongs > 0:
        count = count.loc[count >= minsongs]

    # --------------------------------------------------------------------------
    # Make the count into a dataframe and label the columns
    # --------------------------------------------------------------------------
    sdata = pd.DataFrame(list(zip(count.index.tolist(), count.tolist())), columns=["Originating Artist","Number of Songs Played"])

    # --------------------------------------------------------------------------
    # Add a column to say whether the band is one of Chris's originals
    # --------------------------------------------------------------------------
    sdata['CH Original'] = sdata['Originating Artist']
    sdata['CH Original'] = sdata['CH Original'].apply(band_is_original, args=([data['Bands']]))

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata

# ------------------------------------------------------------------------------
# Get data needed for specific chart
# Number of different songs played by year
# ------------------------------------------------------------------------------
def get_data_num_songs_by_year(data):
    # ----------------------------------------------------------------------
    # Get the whole count
    # ----------------------------------------------------------------------
    count = data['Songs']['Year'].value_counts(sort=True, ascending=False)

    # ----------------------------------------------------------------------
    # Make the count into a dataframe and label the columns
    # ----------------------------------------------------------------------
    sdata = pd.DataFrame(list(zip(count.index.tolist(), count.tolist())), columns=["Year of Song's Origination","Number of Songs Played"])

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata

