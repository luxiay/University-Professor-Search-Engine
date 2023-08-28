from mongo_db import MongoConnector
from sql_db import MySqlConnector
from neo4j_db import Neo4jConnector
from histogram import *
from dash import Dash, html, dash_table, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash


sql_db = MySqlConnector()
mongo_db = MongoConnector()
neo4j_db = Neo4jConnector()

sql_db.IndexCreate('uni_name', 'university', 'name', 'academicworld')
sql_db.IndexCreate('keyword_name', 'keyword', 'name', 'academicworld')
sql_db.IndexCreate('prof_url', 'faculty', 'photo_url', 'academicworld')
sql_db.Create_view()

sql_db.CreateFavoriteProf()


app = Dash(external_stylesheets=[dbc.themes.JOURNAL])
favorites = []

top_publication = mongo_db.GetPublicationsInfo()

app.layout = html.Div(
    children = [
    # title of our project
    dbc.Row(dbc.Col(
                html.Div(
                    html.H1('University Professor Search Engine', style = {'margin-left':'20px'}),
                    style = {'color': 'white', 'height': '80px', 'background-color': 'black','background-size': '800px', 'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'}
                )
    )),
    # widget 1&2: Top N kewords (Neo4j), Top publication (mongoDB)
    dbc.Row([dbc.Col(
                html.Div([
                    html.H2('Top N Keywords', style={'height': '50px','textAlign': 'center','color': 'white', 'background-color': 'grey'}),
                    html.Label('Please select the number:'),
                    dcc.Slider(5, 20, 5, value=10, id='slider-1'),
                    html.Label('Keywords:'),
                    html.Br(),
                    dcc.Graph(id='graph-1') #scatter plot
                ]),width=6),
            dbc.Col(
                html.Div([
                    html.H2('Top Publications', style={'height': '50px','textAlign': 'center','color': 'white', 'background-color': 'grey'}),
                    html.Br(),
                    dbc.Table.from_dataframe(top_publication, striped=True, bordered=True, hover=True)
                ]),width=6)], style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'}),

    # widget 3: Top 5 keywords per school
    dbc.Row(dbc.Col(
            html.H2('Top 5 Keywords per School', style={'height': '50px','textAlign':'center','textAlign': 'center','color': 'white', 'background-color': 'grey'}),
            style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'})),

    dbc.Row([dbc.Col(dbc.Label('University Name'), width = 'auto',
            style = {'margin-left':'40px', 'margin-top':'20px'}),
            dbc.Col(dbc.Input(id="school_name", placeholder="e.g. school name", type="text", style={'width': '400px'}),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px'}),
            dbc.Col(
                dbc.Button("Search", id = 'top-keyword-button', n_clicks=0, color="primary", className="me-1"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'}),
        ]),
    dbc.Row([dbc.Col(html.Div(id='uni-container'),
            width = {'size': '6'},
            style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'5px'}),
            dbc.Col(html.Div([
                dcc.Graph(id='graph-4') #pie chart
            ]), style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'100px'})]),

    # widget 4: Most cited publications per school
    dbc.Row(dbc.Col(
            html.H2('Most Cited Publications per University', style={'height': '50px','textAlign':'center','textAlign': 'center','color': 'white', 'background-color': 'grey'}),
            style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'})),

    dbc.Row([dbc.Col(html.Label('University Name:'), width = 'auto',
            style = {'margin-left':'40px', 'margin-top':'20px'}),
            dbc.Col(dbc.Input(id="school_name_seperate", placeholder="e.g. school 1, school 2", type="text", style={'width': '400px'}),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px'}),
            dbc.Col(
                dbc.Button("Search", id = 'most-cited-button', n_clicks=0, color="primary", className="me-1"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'}),
    ]),

    dbc.Row(dbc.Col(
        dcc.Graph(id="cited_pub_graph"),
        width = {'size': '6', 'offset': '3'}), style = {'margin-left':'20px', 'margin-top':'20px', 'margin-right':'40px'}),

    # widget 5: Top five Faculty
    dbc.Row(dbc.Col(
        html.H2('Top 5 Faculty per University per Keyword', style={'height': '50px','textAlign':'center','textAlign': 'center','color': 'white', 'background-color': 'grey'}),
        style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'})),

    dbc.Row([dbc.Col(dbc.Label('University Name'), width = 'auto',
            style = {'margin-left':'40px', 'margin-top':'20px'}),
            dbc.Col(dbc.Input(id="university_search", placeholder="input university name...", type="text"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px'}),
            dbc.Col(dbc.Label('Keyword', className="me-1"),
                width = 'auto',
                style = {'margin-left':'20px', 'margin-top':'20px', 'margin-right':'0px'}),
            dbc.Col(dbc.Input(id="keyword_search", placeholder="input keyword...", type="text"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'}),
            dbc.Col(
                dbc.Button("Search", id = 'submit-button', n_clicks=0, color="primary", className="me-1"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'}),
        ]),
    dbc.Row(dbc.Col(dcc.Graph(id="faculty_graph"),style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'})),


    # widget 6&7: Faculty Information Search and add or remove Favorite Faculty
    dbc.Row(dbc.Col(
            html.H2('Faculty Information Search', style={'height': '50px','textAlign':'center','textAlign': 'center','color': 'white', 'background-color': 'grey'}),
            style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'})),

    dbc.Row([dbc.Col(dbc.Label('University Name'), width = 'auto',
            style = {'margin-left':'40px', 'margin-top':'20px'}),
            dbc.Col(dbc.Input(id="university_info_search", placeholder="input university name...", type="text"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px'}),
            dbc.Col(dbc.Label('Faculty Name', className="me-1"),
                width = 'auto',
                style = {'margin-left':'20px', 'margin-top':'15px', 'margin-right':'0px'}),
            dbc.Col(dbc.Input(id="faculty_info_name", placeholder="input faculty name...", type="text"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'}),
            dbc.Col(
                dbc.Button("Search", id = 'submit_info-button', n_clicks=0, color="primary", className="me-1"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'}),
            dbc.Col(
                dbc.Button("follow", id = 'add-button', n_clicks=0, color="primary", className="me-1"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'}),
            dbc.Col(
                dbc.Button("remove", id = 'remove-button', n_clicks=0, color="primary", className="me-1"),
                width = 'auto',
                style = {'margin-left':'0px', 'margin-top':'10px', 'margin-right':'0px'})]),

    dbc.Row([
    dbc.Col(html.Div(id='output-container'),
        #width = {'size': '5'},
        style = {'margin-left':'40px', 'margin-top':'20px', 'margin-right':'5px'}),

    dbc.Col(html.Div([
        dcc.Graph(id='key-graph') # pie chart
        ]),
        #width={'size': '4'},
        style={'margin-left': '10px', 'margin-top': '20px', 'margin-right': '20px'}
        ),

    dbc.Col(html.Div(id='output-table'),
        width = {'size': '2'}, #"order": "last",
        style = {'margin-left':'0px', 'margin-top':'20px', 'margin-right':'0px'})
    ], style = {'margin-left':'0px', 'margin-top':'20px', 'margin-right':'40px'}),

    dbc.Row(dbc.Col(
                html.Div(
                    #html.H4('Find your favorite University and Faculty'),
                    style = {'color': 'white', 'height': '50px', 'background-color': 'black','background-size': '800px', 'margin-left':'40px', 'margin-top':'20px', 'margin-right':'40px'}
                )
    ))
])

# widget 1&2: Top N kewords (Neo4j)
@app.callback(Output('graph-1', 'figure'),
              Input('slider-1', 'value'))
def update_widget_1(input):
      df = neo4j_db.widgetOne(input)
      fig = px.scatter(df, x='top words', y='count')
      fig.update_traces(marker_size = 15)
      fig.update_xaxes(title_text = "Keyword", title_font = {"size": 20}, tickfont={'size': 15})
      fig.update_yaxes(title_text = "Count", title_font = {"size": 20}, tickfont={'size': 15})
      return fig

# widget 3: Top 5 keywords per school
@app.callback(
    output = Output('graph-4', 'figure'),
    inputs = Input('top-keyword-button', 'n_clicks'),
    state = State('school_name', 'value'))
def top_keyword(n_clicks,input_school_name):
    if n_clicks == 0:
        input_school_name = 'University of illinois at Urbana Champaign'
    df = sql_db.Query_top_keyword(input_school_name)
    fig = px.pie(df, values='count', names='keyword', hole=0.6, title=f"Top 5 Keywords for {input_school_name}", color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

# widget 3: get the university.photo_url
@callback(
    output = Output('uni-container', 'children'),
    inputs = Input('top-keyword-button', 'n_clicks'),
    state = State("school_name", "value"))
def uni_photo(n_clicks, input_school_name):
    if n_clicks == 0:
        input_school_name = 'University of illinois at Urbana Champaign'
    df = sql_db.Query_uni_photo(input_school_name)
    records = df.to_dict(orient='records')
    return html.Div(
        children = [
            html.Div([
                html.Img(src=records[0]['photo_url'], width='400px')],
                style={'width': '500px', 'margin-left':'200px', 'margin-top':'150px', 'display': 'inline-block'}
                )])

# widget 4: Most cited publications per school
@app.callback(
    output=Output("cited_pub_graph", "figure"),
    inputs=[Input('most-cited-button', 'n_clicks')],
    state=[State("school_name_seperate", "value")]
)
def update_bar_chart(n_clicks, input_query_schools):
    if n_clicks == 0:
        universities = ["University of illinois at Urbana Champaign", "Yale University"]
        print(f"yujia Debug first iteration is called.")
    else:
        print(f"yujia Debug this is called.")
        universities = input_query_schools.split(',')
    quoted_universities = ", ".join([f"'{university.strip()}'" for university in universities])
    df = sql_db.QueryTopPublications(quoted_universities)
    return CreateCitationFigure(df)

# widget 5: Top five Faculty
@callback(
    output = Output("faculty_graph", "figure"),
    inputs = Input('submit-button', 'n_clicks'),
    state = [State('university_search', 'value'), State('keyword_search', 'value')]
)
def update_output(n_clicks, university_name, keyword):
    if n_clicks == 0:
        university_name = 'University of illinois at Urbana Champaign'
        keyword = 'machine learning'
    df = sql_db.QueryTopfauclty(university_name, keyword)
    fig = px.bar(df, x="name", y="score",
                 color="name",
                 #text = "score",
                 # when mousr put on it, it will show
                 #hover_data = {"score":False},
                 barmode="group",
                 color_discrete_sequence = px.colors.qualitative.Vivid,
                 orientation='v')
    fig.update_layout(barmode='group', xaxis_tickangle=-20)
    fig.update_traces(width = 0.6)
    #fig = create_chart(fdf=df)
    #return dcc.Graph(figure=fig)
    return fig

# widget 6: Faculty Information Search
@app.callback(
    output = Output('output-container', 'children'),
    inputs = Input('submit_info-button', 'n_clicks'),
    state = [State('university_info_search', 'value'), State('faculty_info_name', 'value')]
)
def search_person(n_clicks, university_name, faculty_name):
    if n_clicks == 0:
        university_name = 'University of illinois at Urbana Champaign'
        faculty_name = 'Kevin Chenchuan Chang'
    df = mongo_db.QueryFacultyTable(university_name, faculty_name)
    #print(f"yujia debug person info {df}")

    records = df.to_dict(orient='records')
    if not records:
        # No matching records found, set default values
        phone_value = 'NULL'
        email_value = 'NULL'
    else:
        # Matching record found, extract phone and email values
        phone_value = records[0]['phone'] if records[0]['phone'] else 'Phone: Null'
        email_value = records[0]['email'] if records[0]['email'] else 'Null'
    #print(f"yujia debug person records {records}")
    return html.Div(
        children=[
            html.Div([
                html.Img(src=records[0]['photoUrl'], width='200px')],
                style={'width': '200px', 'display': 'inline-block'}
            ),
            html.Div([
                html.H4(f"{records[0]['name']}"),
                html.P(f"{records[0]['position']}"),
                html.P(f"{records[0]['university']}"),
                html.P(f"{phone_value}"),
                html.P(f"Email:  {email_value}")
            ],
                style={'width': '50%', 'margin-left': '10px', 'margin-top': '30px', 'display': 'inline-block',
                       'textAlign': 'left', "verticalAlign": "top"}
            ),
        ],
    )

# widget 6: get the top 5 keywords for faculty
@app.callback(
    output = Output('key-graph', 'figure'),
    inputs = Input('submit_info-button', 'n_clicks'),
    state = [State('university_info_search', 'value'), State('faculty_info_name', 'value')]
)
def faculty_keyword(n_clicks, university_name, faculty_name):
    if n_clicks == 0:
        university_name = 'University of illinois at Urbana Champaign'
        faculty_name = 'Kevin Chenchuan Chang'
    df = sql_db.QueryFacultyKeyword(university_name, faculty_name)
    fig = px.pie(df, values='total_score', names='keyword_name', hole=0.5, title=f"Top 5 Keywords for {faculty_name}", color_discrete_sequence=px.colors.qualitative.Vivid)
    return fig


# widget 7: add or remove Favorite Faculty
@app.callback(
    output=Output('output-table', 'children'),
    inputs=[Input('add-button', 'n_clicks'),
            Input('remove-button', 'n_clicks')],
    state=[State('university_info_search', 'value'),
           State('faculty_info_name', 'value')]
)
def add_remove_faculty(click_add, click_remove, university_name, professor_name):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    msg = ''
    if triggered_id == 'add-button' and professor_name:
        raw_conn = sql_db.engine.raw_connection()
        cur = raw_conn.cursor()
        result_args = cur.callproc('check_valid_prof', [professor_name, university_name, None])
        is_valid = result_args[-1]

        #print(f"yujia debug person records {type(is_valid)}, {is_valid}")
        if is_valid == 1:
            if professor_name not in favorites:
                favorites.append(professor_name)
                msg = f'{professor_name} has been added to your favorites table.'
                sql_db.AddProf(f'{professor_name}', True)
            else:
                msg = f'{professor_name} is already in your favorites table.'
        else:
            msg = f"{professor_name} is not a faculty for {university_name}."
    elif triggered_id == 'remove-button' and professor_name:
        favorites.remove(professor_name)
        sql_db.RemoveProf(f'{professor_name}')
    df = sql_db.get_favorite_prof()
    children = [
        dbc.Label('My Favorite Professor'),
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    ]
    if msg:
        children.append(html.P(msg))
    df = sql_db.get_favorite_prof()
    return html.Div(children, style={'margin-top': '30px'})



if __name__ == '__main__':
    app.run(debug=True)
