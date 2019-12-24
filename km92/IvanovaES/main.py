import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="keys.json"

import pandas as pd
from bq_helper import BigQueryHelper
import plotly.graph_objs as go
from plotly.offline import plot

bq_assistant = BigQueryHelper('bigquery-public-data', 'nhtsa_traffic_fatalities')

QUERY = """
        SELECT state_number, consecutive_number, vehicle_number, contributing_circumstances_motor_vehicle 
        FROM `bigquery-public-data.nhtsa_traffic_fatalities.factor_2015`
        LIMIT 10000
        """
df = bq_assistant.query_to_pandas(QUERY)

state_group = df.groupby(['state_number'])
trace1_data = state_group['state_number'].count()
trace1 = go.Bar(
                    x = trace1_data.index
                    ,y = trace1_data.values
                    )
vehicle_group = df.groupby(['vehicle_number'])
trace2_data = state_group['vehicle_number'].count()
trace2 = go.Pie(
                    title = 'Vehicle number, which have an accident'
                    ,labels = trace2_data.index
                    ,values = trace2_data.values
                    )
# consecutive_number_group = df.groupby(['consecutive_number'])
# trace3_data = state_group['consecutive_number'].count()
# trace3 = go.Scatter(
#     x=trace3_data.index
#     ,y=trace3_data.values
#     ,name = 'Consecutive Number'
# )
# plot(trace3)

trace1_layout = go.Layout(title = 'Traffic fatalities'
              ,xaxis= dict(title= 'State')
              ,yaxis=dict(title='Number of vehicles')
             )

fig = dict(data = [trace1], layout = trace1_layout)

plot(fig)
plot(go.Figure(trace2))