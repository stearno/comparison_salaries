# import plotly.offline as pyo
import plotly.graph_objs as go
import dash
from dash import Input, Output, dcc, html
import pandas as pd
import dash_auth

USERNAME_PASSWORD_PAIRS = [['helena','C@mc0@2014'],['jonathan','Human@2018']]

CamGreen = 'rgb(0,170,145)'

df = pd.read_csv('Current_Salaries.csv')

app = dash.Dash()
server = app.server

auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)

grade = df['Grade'].unique()
grade.sort()
salary_type = ['Basic','Housing','Transportation','Total']

app.layout = html.Div([
            html.Div([
                dcc.RadioItems(id='ComparisonCat',
                             options=['Market','Budget'],
                             style={'color':'black'},
                             inline=1,
                             value='Budget'
                             )          
                ],style={'width':'10%','color': 'black','display':'inline-block'}),                
            html.Div([
                dcc.Dropdown(id='grade',
                             style = {'color':'black'},
                             options=[{'label': i,'value': i} for i in grade],
                             placeholder="Select a Grade",
                             ) #value=grade[0]
                ],style={'width':'10%','color':'black','display':'inline-block'}),
            html.Div([
                dcc.Dropdown(id='SalaryType',
                             style = {'color':'black'},
                             options=[{'label': i,'value': i} for i in salary_type],
                             placeholder="Select Salary Type",
                             )      #value=salary_type[0]          
                ],style={'width':'10%','color': 'black','display':'inline-block'}),
            html.Div([
                dcc.RadioItems(id='BudgetLevel',
                             options=[{'label': i,'value': i} for i in df['Budget in Grade'].unique()],
                             style={'color':'black'},
                             inline=1,
                             value=50
                             )          
                ],style={'width':'10%','color': 'black','display':'inline-block'}),
                dcc.Graph(id='Salaries vs Budget'),
            # html.Div(
            #     html.Pre(id='hover_data',style={'paddingTop':35}),
            #     style={'width':'30%'}
            #     )
    ],style={'padding':10,'background':CamGreen})#'black',


@app.callback(Output('Salaries vs Budget','figure'),
              [Input('grade','value'),
               Input('SalaryType','value'),
               Input('BudgetLevel','value'),
               Input('ComparisonCat','value')])
def update_graph(grade_choice,type_choice,budgetlevel,compCat):
    typedict = {'Basic':'Basic Salary','Housing':'Housing Allowance','Transportation':'Transportation Allowance','Total':'Total Salary'}
    currentchoice = typedict[type_choice]
    if compCat == 'Budget':
        type_compare = 'Budget_'+ type_choice
    else:
        type_compare = 'Market_'+ type_choice
    #Can make the above a radio button in futdure version.  So can choose Budget or Market
    
    df_Grade = df[df['Grade'] == grade_choice]
    df_Grade = df_Grade[df_Grade['Budget in Grade'] == budgetlevel]
    
    df_Gd_RATP = df_Grade[df_Grade['Contract Type'] == 'RATPDEV']
    df_Gd_CAM = df_Grade[df_Grade['Contract Type'] == 'CAMCO']
    
    trace0 = go.Scatter(
        x = df_Gd_CAM['Employee ID'],
        y = df_Gd_CAM[currentchoice].astype(float),
        mode = 'markers',
        name = 'CAMCO ' + type_choice,
        marker = dict(
            size = 12,
            color = 'Green',
            symbol = 'pentagon',
            opacity = 0.7,
            line = dict(
                width = 2,
            )
        )
    )

    trace1 = go.Scatter(
        x = df_Gd_RATP['Employee ID'],
        y = df_Gd_RATP[currentchoice].astype(float),
        mode = 'markers',
        name = 'RATP ' + type_choice,
        marker = dict(      # change the marker style
            size = 12,
            color = 'Red',
            symbol = 'pentagon',
            opacity = 0.7,
            line = dict(
                width = 2,
            )
        )
    )

    trace2 = go.Scatter(
        x = df_Grade['Employee ID'],
        y = df_Grade[type_compare], #Market_Basic
        mode = 'lines',
        name ='Budget',
        marker = dict(     
            color = 'yellow',
            line = dict(
                width = 6,
            )
        )
    )
    
    layout = go.Layout(
        title = 'Current Salaries Versus Budget', # Graph title
        xaxis = dict(title = 'Employee Number'), # x-axis label
        yaxis = dict(title = currentchoice), # y-axis label
        hovermode ='closest' # handles multiple points landing on the same vertical
    )
    return {'data':[trace0, trace1, trace2],'layout':layout}

# @app.callback(Output('hover_data','children')
#               [Input()])
# def callback_data(hoverData):
#     return json.dumps(hoverData,indent=2)


if __name__ == '__main__':
    app.run_server()




# fig = go.Figure(data=data, layout=layout)
# fig.update_yaxes(categoryorder='category ascending')
# pyo.plot(fig, filename='scatter1.html')
