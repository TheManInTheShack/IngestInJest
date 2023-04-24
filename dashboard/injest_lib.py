# ==================================================================================================
# General functions
# ==================================================================================================

# ==================================================================================================
# Imports
# ==================================================================================================
import sys
import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from datetime import datetime, timedelta

# ==================================================================================================
# FUNCTIONS FOR GENERATING AND DISPLAYING TABLES
# ==================================================================================================

# ------------------------------------------------------------------------------
# This is the generic code to generate a table from any dataframe; this is
# the simple bootstrap table, only suitable for small outputs
# ------------------------------------------------------------------------------
def generate_simple_table(data, idx, max_rows=50):
    # --------------------------------------------------------------------------
    # The table object
    # --------------------------------------------------------------------------
    head = html.Thead(html.Tr([html.Th(col) for col in data.columns]))
    body = html.Tbody([ html.Tr([html.Td(data.iloc[i][col]) for col in data.columns]) for i in range(min(len(data), max_rows)) ])
    table = dbc.Table([head, body],id=idx,bordered=True,dark=True,hover=True,responsive=True,striped=True,size='sm',style={'overflowY':'scroll'})

    # --------------------------------------------------------------------------
    # Consolidate
    # --------------------------------------------------------------------------
    components = []
    components.append(get_empty_col())
    components.append(html.Div(table, className = 'col-10'))
    components.append(get_empty_col())

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return html.Div(components, className = 'row')

# ------------------------------------------------------------------------------
# Bundle the components used to display a simple table
# ------------------------------------------------------------------------------
def display_simple_table(df, idx="", title=""):
    components = []

    components.append(get_empty_row())
    components.append(html.H3(title))
    components.append(generate_simple_table(df, idx))

    return components

# ------------------------------------------------------------------------------
# This is for 'real' tables
# ------------------------------------------------------------------------------
def generate_data_table(df, idx, height='500px'):
    # --------------------------------------------------------------------------
    # The table object
    # --------------------------------------------------------------------------
    table = dash_table.DataTable(
            id=idx,
            data = df.to_dict('records'),
            columns = [{'id':c, 'name':c} for c in df.columns],
            filter_action='native',
            page_action='none',
            #fixed_rows={'headers':True},    <------TODO WHEN THIS IS ON, THE FILTERS SHOW NOTHING
            style_cell={'whiteSpace':'normal','height':'auto','textAlign':'left', 'minWidth':'50px', 'maxWidth':'180px'},
            style_table={'height':height, 'overflowY':'auto' },
            style_header={'backgroundColor':'Black', 'fontWeight':'bold', 'textAlign':'center' },
            style_data_conditional=[{'if': {'row_index':'odd'},'backgroundColor':'rgb(0,0,0)'},{'if': {'row_index':'even'},'backgroundColor':'rgb(25,25,25)'}],
            style_as_list_view=False,
            sort_action='native',
            sort_mode='multi'
            )

    # --------------------------------------------------------------------------
    # Consolidate
    # --------------------------------------------------------------------------
    components = []
    components.append(get_empty_col())
    components.append(html.Div(table, className = 'col-10'))
    components.append(get_empty_col())

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return html.Div(components, className = 'row')

# ------------------------------------------------------------------------------
# Bundle the components used to display a data table
# ------------------------------------------------------------------------------
def display_data_table(df, idx="", title="", height="500px"):
    components = []

    components.append(get_empty_row())
    components.append(html.H3(title))
    components.append(generate_data_table(df, idx, height))

    return components

# ==================================================================================================
# Chart-related functions
# ==================================================================================================

# ------------------------------------------------------------------------------
# Complete chart system with controls
# ------------------------------------------------------------------------------
def charts_with_controls(charts, controls, layout):
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    #print(controls)
    #print(data)
    # --------------------------------------------------------------------------
    # Create the chart objects
    # --------------------------------------------------------------------------
    for chart in charts:
        thischart = charts[chart]
        details   = charts[chart]['details']
        if thischart['chart_type'] == 'bar':
            if 'color' in details:
                figure = generate_bar(data=details['data'],x=details['x'],y=details['y'],style=details['style'],color=details['color'])
            else:
                figure = generate_bar(data=details['data'],x=details['x'],y=details['y'],style=details['style'])

        if thischart['chart_type'] == 'line':
            figure = generate_line(details['data'],details['x'],details['y'],style=details['style'])
        charts[chart]['figure'] = dcc.Graph(id=charts[chart]['idx'],figure=figure)
    
    # --------------------------------------------------------------------------
    # Create the matrix for the chart based on the shape input
    # --------------------------------------------------------------------------
    chart_shape = shape_matrixify(layout['chart_shape'])
    # --------------------------------------------------------------------------
    # Place into the appropriate shape
    # --------------------------------------------------------------------------
    row = -1
    numcols = len(chart_shape[0])
    for col,chart in enumerate(charts):
        # ----------------------------------------------------------------------
        # Figure out what column we should be in
        # ----------------------------------------------------------------------
        thiscol = col % numcols
        # ----------------------------------------------------------------------
        # Increment row if we're at the beginning of row
        # ----------------------------------------------------------------------
        if thiscol == 0:
            row += 1
        # ----------------------------------------------------------------------
        # Place the object in
        # ----------------------------------------------------------------------
        chart_shape[row][thiscol] = charts[chart]['figure']
        
    # --------------------------------------------------------------------------
    # Compile the components
    # --------------------------------------------------------------------------
    chart_components = []
    for row in chart_shape:
        rowinp = list(map(create_div_col,row))
        thisrow = []
        thisrow.append(get_empty_col())
        thisrow.append(html.Div(dbc.Row(rowinp),className='col-10'))
        thisrow.append(get_empty_col())
        chart_components.append(html.Div(thisrow, className='row'))
        chart_components.append(get_empty_row())


    # --------------------------------------------------------------------------
    # Create the control objects
    # --------------------------------------------------------------------------
    for control in controls:
        # ----------------------------------------------------------------------
        # Create a drop down
        # ----------------------------------------------------------------------
        if controls[control]['control_type'] == 'dropdown':
            details = controls[control]['details']
            controls[control]['obj'] = dcc.Dropdown(id=controls[control]['idx'],options=details['options'],
                                                    value=details['value'],multi=details['multi'],
                                                    style=details['style'])
            continue
        # ----------------------------------------------------------------------
        # Button
        # ----------------------------------------------------------------------
        if controls[control]['control_type'] == 'button':
            details = controls[control]['details']
            controls[control]['obj'] = dbc.Button(details['label'],id=controls[control]['idx'])
            # controls[control]['obj'] = html.Button(details['label'],id=controls[control]['idx'])
            continue
        # ----------------------------------------------------------------------
        # Add more as they come
        # ----------------------------------------------------------------------
        # if controls[control]['control_type'] ==

    # --------------------------------------------------------------------------
    # Make components list
    # --------------------------------------------------------------------------
    control_components = []
    # --------------------------------------------------------------------------
    # Go through each control and create a title + dropdown object
    # --------------------------------------------------------------------------
    for control in controls:
        thiscontrolset = []
        thiscontrolset.append(html.P(controls[control]['details']['title']))
        thiscontrolset.append(controls[control]['obj'])
        control_components.append(dbc.Col(html.Div(thiscontrolset)))
    controlset = [html.Div([get_empty_col(),html.Div(dbc.Row(control_components),className='col-10'),get_empty_col()],className='row')]

    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    if layout['controls_orient'] == 'top':
        construct = html.Div(controlset + chart_components, style=layout['style_default'])
    elif layout['controls_orient'] == 'bottom':
        construct = html.Div(chart_components + controlset, style=layout['style_default'])
    else:
        construct = html.Div(controlset + chart_components, style=layout['style_default'])

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return construct

# ==================================================================================================
# Page layout functions
# ==================================================================================================
# ------------------------------------------------------------------------------
# Empty row
# This returns an empty row of a defined height
# ------------------------------------------------------------------------------
def get_empty_row(h='45px'):
    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow
# ------------------------------------------------------------------------------
# Empty column for spacing
# ------------------------------------------------------------------------------
def get_empty_col():
    empty_col = html.Div([], className = 'col-1')
    return empty_col

# ------------------------------------------------------------------------------
# Create a div col object (for charts)
# ------------------------------------------------------------------------------
def create_div_col(obj=[None]):
    col = dbc.Col(html.Div(obj))
    return col

# ------------------------------------------------------------------------------
# Navbar, using bootstrap
# ------------------------------------------------------------------------------
def get_navbar(pages, title):
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    page_links = []
    for page in pages:
        page_links.append(dbc.NavItem(dbc.NavLink(pages[page]['name'], href=pages[page]['href'])))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    navbar = dbc.NavbarSimple(
            children=page_links,
            brand=title,
            brand_href="/",
            color="black",
            dark=True
        )

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    return navbar

# ==================================================================================================
# Utility functions for doing data-related stuff
# ==================================================================================================

# ------------------------------------------------------------------------------
# Take in a dataframe, aggregate by group -> mean
# ------------------------------------------------------------------------------
def aggregate_df_mean(inpdf,agg_col,metrics):
    out = inpdf.groupby(agg_col)[metrics].mean()
    out[agg_col] = out.index.to_list()
    return out

# ------------------------------------------------------------------------------
# From a date string, we want to know the month, quarter, and year
# ------------------------------------------------------------------------------
def get_date_hierarchy(date):
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    ddate = datetime.strptime(date, '%Y-%m-%d')
    year  = ddate.year
    month = ddate.month

    if month <= 3:
        qnum = 1
    elif month <= 6:
        qnum = 2
    elif month <= 9:
        qnum = 3
    elif month <= 12:
        qnum = 4

    quarter = str(year) + " Q" + str(qnum)

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return month, quarter, year

# ==================================================================================================
# Creating control objects
# ==================================================================================================

# ==================================================================================================
# Creating figures
# ==================================================================================================
def generate_line(data, x, y, color="", legend_title=None, style={}, config={}):
    # --------------------------------------------------------------------------
    # Initialize the line object
    # --------------------------------------------------------------------------
    line = px.line(data,x=x,y=y)
    # --------------------------------------------------------------------------
    # Update styling
    # --------------------------------------------------------------------------
    if 'backgroundColor' in style:
        line.update_layout(plot_bgcolor=style['backgroundColor'])
        line.update_layout(paper_bgcolor=style['backgroundColor'])
    if 'color' in style:
        line.update_layout(font_color=style['color'])
    # --------------------------------------------------------------------------
    # Update the legend title
    # --------------------------------------------------------------------------
    if legend_title is not None:
        line.update_layout(legend_title_text  = legend_title)
    return line

def generate_bar(data, x, y, color="", style={}, config={}, barmode='', facet=''):
    # --------------------------------------------------------------------------
    # Make the bar chart figure
    # --------------------------------------------------------------------------
    if color:
        bar = px.bar(data, x=x, y=y, color=color)
    else:
        bar = px.bar(data, x=x, y=y)

    # --------------------------------------------------------------------------
    # Update mode if needed
    # --------------------------------------------------------------------------
    if barmode:
        bar.update_layout(barmode=barmode)

    # --------------------------------------------------------------------------
    # Update facet if needed
    # --------------------------------------------------------------------------
    #if facet:
    #    bar.update_layout(facet=facet)

    # --------------------------------------------------------------------------
    # Update styling
    # --------------------------------------------------------------------------
    if 'backgroundColor' in style:
        bar.update_layout(plot_bgcolor=style['backgroundColor'])
        bar.update_layout(paper_bgcolor=style['backgroundColor'])
    if 'color' in style:
        bar.update_layout(font_color=style['color'])

    # --------------------------------------------------------------------------
    # Kick out before making the whole chart object if we are refreshing
    # --------------------------------------------------------------------------
    return bar

def generate_data_table(df, idx, height='500px'):
    # --------------------------------------------------------------------------
    # The table object
    # --------------------------------------------------------------------------
    table = dash_table.DataTable(
            id=idx,
            data = df.to_dict('records'),
            columns = [{'id':c, 'name':c} for c in df.columns],
            filter_action='native',
            page_action='none',
            #fixed_rows={'headers':True},    <------TODO WHEN THIS IS ON, THE FILTERS SHOW NOTHING
            style_cell={'whiteSpace':'normal','height':'auto','textAlign':'left', 'minWidth':'50px', 'maxWidth':'180px'},
            style_table={'height':height, 'overflowY':'auto' },
            style_header={'backgroundColor':'Black', 'fontWeight':'bold', 'textAlign':'center' },
            style_data_conditional=[{'if': {'row_index':'odd'},'backgroundColor':'rgb(0,0,0)'},{'if': {'row_index':'even'},'backgroundColor':'rgb(25,25,25)'}],
            style_as_list_view=False,
            sort_action='native',
            sort_mode='multi'
            )

    # --------------------------------------------------------------------------
    # Consolidate
    # --------------------------------------------------------------------------
    components = []
    components.append(get_empty_col())
    components.append(html.Div(table, className = 'col-10'))
    components.append(get_empty_col())

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return html.Div(components, className = 'row')

# ==================================================================================================
# Helper Functions
# ==================================================================================================
def shape_matrixify(shape):
    """
    Create matrix based on shape description
    """
    try:
        rows = int(shape.lower().split('x')[0])
        cols = int(shape.lower().split('x')[1])
        out = [[] for i in range(rows)]
        for row in out:
            for i in range(cols):
                row.append(None)
        return out
    except:
        return [[]]


# ==================================================================================================
# General functions for this project
# ==================================================================================================
# ------------------------------------------------------------------------------
# Get the existing marked-up data, no frills
# ------------------------------------------------------------------------------
def get_marked_data(data_fname):
    # --------------------------------------------------------------------------
    # Start
    # --------------------------------------------------------------------------
    print("...reading data from file " + data_fname + "...")

    # --------------------------------------------------------------------------
    # Get the whole mess at once
    # --------------------------------------------------------------------------
    existing_data = pd.read_excel(data_fname, sheet_name=None, usecols = lambda x: 'Unnamed' not in x,)

    # --------------------------------------------------------------------------
    # Set up the index for each
    # --------------------------------------------------------------------------
    existing_data['People']       = existing_data['People'].set_index('Name', drop=False).dropna(how='all')
    existing_data['Instruments']  = existing_data['Instruments'].set_index('Name', drop=False).dropna(how='all')
    existing_data['Genres']       = existing_data['Genres'].set_index('Name', drop=False).dropna(how='all')
    existing_data['Bands']        = existing_data['Bands'].set_index('Name', drop=False).dropna(how='all')
    existing_data['Albums']       = existing_data['Albums'].set_index(['Name','Band'], drop=False).dropna(how='all')
    existing_data['Songs']        = existing_data['Songs'].set_index(['Name','Band'], drop=False).dropna(how='all')
    existing_data['Places']       = existing_data['Places'].set_index('Name', drop=False).dropna(how='all')
    existing_data['Series']       = existing_data['Series'].set_index('Name', drop=False).dropna(how='all')
    existing_data['Gigs']         = existing_data['Gigs'].set_index(['Series','Series Index'], drop=False).dropna(how='all')
    existing_data['Performances'] = existing_data['Performances'].set_index(['Series','Series Index','Set','Set Position'], drop=False).dropna(how='all')
    existing_data['Image']        = existing_data['Image'].set_index('File Name', drop=False).dropna(how='all')
    existing_data['Audio']        = existing_data['Audio'].set_index('File Name', drop=False).dropna(how='all')
    existing_data['Video']        = existing_data['Video'].set_index('File Name', drop=False).dropna(how='all')

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return existing_data



# ------------------------------------------------------------------------------
# Prepare the performance-based data
# ------------------------------------------------------------------------------
def get_data_performances(data):
    # --------------------------------------------------------------------------
    # Start with the performances
    # --------------------------------------------------------------------------
    sdata = data['Performances'][['Series Index','Set Position','Song','Artist']]
    sdata = sdata.rename(columns={'Series Index':'Show', 'Set Position':'Position'})

    # --------------------------------------------------------------------------
    # Add the year and the composers from the song Table
    # --------------------------------------------------------------------------
    songdata = data['Songs'][['Album','Year','Composer']]
    sdata = sdata.merge(songdata, how='left', left_on=['Song','Artist'], right_on=['Name','Band'])

    # --------------------------------------------------------------------------
    # Add the 'family' of artists
    # --------------------------------------------------------------------------
    family = data['Bands'][['Band Family']]
    sdata =sdata.merge(family, how='left', left_on=['Artist'], right_on=['Name'])
    sdata = sdata.rename(columns={'Band Family':'Family'})

    # --------------------------------------------------------------------------
    # Calculate the number of times played
    # --------------------------------------------------------------------------
    numtimes = data['Performances'][['Song','Artist']].reset_index(drop=True)
    numtimes['Times Played'] = 1
    numtimes = numtimes.groupby(['Song','Artist']).sum()

    sdata = sdata.merge(numtimes, how='left', on=['Song','Artist'])

    # --------------------------------------------------------------------------
    # Flag as CH original or not
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata

# ------------------------------------------------------------------------------
# Prepare the Show-based data
# ------------------------------------------------------------------------------
def get_data_shows(data):
    # --------------------------------------------------------------------------
    # Start with the shows
    # --------------------------------------------------------------------------
    sdata = data['Gigs'][['Location','Date/Time Start','Show Title']]

    # --------------------------------------------------------------------------
    # Get the number of songs played
    # --------------------------------------------------------------------------
    numsongs = data['Performances'][['Series Index']].reset_index(drop=True)
    numsongs['Count'] = 1
    numsongs = numsongs.groupby('Series Index').sum()

    sdata = sdata.merge(numsongs, how='left', left_on=['Series Index'], right_on=['Series Index'])

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata

# ------------------------------------------------------------------------------
# Prepare the Song-based data
# ------------------------------------------------------------------------------
def get_data_songs(data):
    # --------------------------------------------------------------------------
    # Start with the songs
    # --------------------------------------------------------------------------
    sdata = data['Songs'][['Name','Band','Album','Year','Genre','Composer','Covered']].reset_index(drop=True)
    sdata = sdata.rename(columns={'Name':'Song', 'Band':'Artist'})

    # --------------------------------------------------------------------------
    # Get the number of times played
    # --------------------------------------------------------------------------
    numtimes = data['Performances'][['Song','Artist']].reset_index(drop=True)
    numtimes['Times Played'] = 1
    numtimes = numtimes.groupby(['Song','Artist']).sum()

    sdata = sdata.merge(numtimes, how='left', on=['Song','Artist'])

    # --------------------------------------------------------------------------
    # Flag as a holt original
    # --------------------------------------------------------------------------
    sdata['CH Original'] = sdata['Artist']
    sdata['CH Original'] = sdata['CH Original'].apply(band_is_original, args=([data['Bands']]))

    sdata = sdata[sdata['CH Original'] == 'No']

    print(sdata['Year'].mean())
    print(sdata['Year'].median())

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata


# ------------------------------------------------------------------------------
# Prepare the Album-based data
# ------------------------------------------------------------------------------
def get_data_albums(data):
    # --------------------------------------------------------------------------
    # Start with the Albums
    # --------------------------------------------------------------------------
    sdata = data['Albums'][['Name','Band','Year']].reset_index(drop=True)
    sdata = sdata.rename(columns={'Name':'Album','Band':'Artist'})

    # --------------------------------------------------------------------------
    # TODO Can we get the track listing for each album?
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # TODO derive a list of the songs that have been played from each album
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # TODO Fields for total # of songs and # of songs played
    # ...that would give us a % of the album that is 'complete'.
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata

# ------------------------------------------------------------------------------
# Prepare the Artist-based data
# ------------------------------------------------------------------------------
def get_data_artists(data):
    # --------------------------------------------------------------------------
    # Start with the Artists
    # --------------------------------------------------------------------------
    sdata = data['Bands'][['Name','Genres','Chris Relationship','Band Family','Band Birthplace']].reset_index(drop=True)
    sdata = sdata.rename(columns={'Name':'Artist','Chris Relationship':'CH Relation'})

    # --------------------------------------------------------------------------
    # TODO Get number of times played from performances
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata

# ------------------------------------------------------------------------------
# Prepare the People-based data
# ------------------------------------------------------------------------------
def get_data_people(data):
    # --------------------------------------------------------------------------
    # Start with the People
    # --------------------------------------------------------------------------
    sdata = data['People'][['Name','Year Born','Year Died','Instruments','Bands','Notes','AllMusic','Wikipedia']].reset_index(drop=True)
    sdata = sdata.rename(columns={'Name':'Person'})

    # --------------------------------------------------------------------------
    # TODO Get number of times referenced?
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata

# ------------------------------------------------------------------------------
# Prepare the Originals-based data
# ------------------------------------------------------------------------------
def get_data_originals(data):
    # --------------------------------------------------------------------------
    # Start with the Songs
    # --------------------------------------------------------------------------
    sdata = data['Songs'][['Name','Band','Album','Year','Genre','Composer','Covered']].reset_index(drop=True)
    sdata = sdata.rename(columns={'Name':'Song', 'Band':'Artist'})
    sdata = sdata[sdata['Composer'] == 'Chris Holt']

    # --------------------------------------------------------------------------
    # TODO Get number of times played
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return sdata


# ==================================================================================================
# Helper functions for this project
# ==================================================================================================


# ------------------------------------------------------------------------------
# Footnote has the credits and the rev#
# ------------------------------------------------------------------------------
def get_footnote(footnote):
    # --------------------------------------------------------------------------
    # Start
    # --------------------------------------------------------------------------
    components = []

    # --------------------------------------------------------------------------
    # Parts
    # --------------------------------------------------------------------------
    components.append(get_empty_row())
    components.append(html.P(footnote['credits']))
    components.append(html.P(footnote['revnum']))

    # --------------------------------------------------------------------------
    # Consolidate
    # --------------------------------------------------------------------------
    fnote = html.Div(components, style={'font-size':'small'})

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return fnote

# ------------------------------------------------------------------------------
# Return Yes/No for whether the band is one of Chris's originals...takes
# in the band and the lookup table
# ------------------------------------------------------------------------------
def band_is_original(band, band_data):
    # --------------------------------------------------------------------------
    # Maybe there's a mismatch in the data
    # --------------------------------------------------------------------------
    if not band in band_data.index:
        print("WARNING! Name not found in data['band']: " + band)
        return "No"
    # --------------------------------------------------------------------------
    # Or maybe we can look it up
    # --------------------------------------------------------------------------
    else:
        this_one = band_data['Chris Relationship'].loc[band]
        if str(this_one).lower() == "original":
            return "Yes"
        else:
            return "No"


