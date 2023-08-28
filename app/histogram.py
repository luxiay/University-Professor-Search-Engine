import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import numpy as np
import hashlib

def color_per_table(university):
    m = hashlib.md5()
    m.update(university.encode('UTF-8'))
    np.random.seed(int(m.hexdigest(), 16)%10000000)
    return '#%02X%02X%02X' % tuple(np.random.randint(0, 255, 3))

def CreateCitationFigure(df):
    all_universities = list(df.university.unique())
    if len(all_universities) == 0:
        return make_subplots(rows = 1, cols = 1)
    ncol = 2
    nrow = int(math.ceil(len(all_universities)/float(ncol)))
    fig = make_subplots(rows = nrow, cols = ncol, vertical_spacing = 0.4, horizontal_spacing = 0.4)
    row, col = 1, 1
    for idx, uni in enumerate(all_universities):
        row, col = (idx // ncol) + 1, (idx % ncol) + 1
        df_per_uni = df[df["university"] == uni]
        xaxis_label = df['title'].values.tolist()
        shortened_label = [x[:10] + "..." for x in xaxis_label]
        customdata = np.stack((df['title'], df['university']), axis = -1)
        fig.add_trace(go.Histogram(
            histfunc = "sum",
            y = df_per_uni["total_citation"],
            #x = df_per_uni["title"],
            x = shortened_label,
            customdata = customdata,
            hovertemplate = 'Title: %{customdata[0]}',
            name = uni,
            marker_color = color_per_table(uni),
            opacity = 0.75
        ), row, col)

    fig.update_yaxes(title = 'Total Citations', tickfont = dict(size=12), titlefont = dict(size=16))
    fig.update_layout(
        width = 1000,
        height = 600,
        template='plotly_white'
    )

    return fig
