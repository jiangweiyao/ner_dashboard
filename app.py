import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash
from dash.dependencies import Output, Input
from dash_extensions.javascript import arrow_function
import geojson
from io import BytesIO
from wordcloud import WordCloud
import base64
import json
from collections import Counter
import pandas as pd

#Load GeoJSON data
with open("map1.geojson") as f:
    gj = geojson.load(f)


#Load NER JSON data
entities_json = "entities.txt"
with open(entities_json) as f:
    entities = json.load(f)

df = pd.DataFrame(entities)
df = df[~df.word.str.contains('#')]
df = df[df.score > 0.9]
word_count = Counter(df["word"].to_list())


# Create example app.
app = dash.Dash()
app.title = 'Named Entity Dashboard'
server = app.server

app.layout = html.Div([
    html.H2('Named Entity Word Cloud'),
    html.Img(id="image_wc"),
    html.H2('Location Entity Map'),
    dl.Map(center=[39, 0], zoom=2, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=gj, id="markers", cluster=True, zoomToBoundsOnClick=True, superClusterOptions={"radius": 100}),  # geojson resource (faster than in-memory)
    ], style={'width': '1000px', 'height': '500px'}, id="map"),
    html.Div(id="marker")
])


@app.callback(Output("marker", "children"), [Input("markers", "click_feature")])
def capital_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['name']}"


def plot_wordcloud(data):
    wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(word_count)
    return wordcloud.to_image()

@app.callback(Output('image_wc', 'src'), [Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=df).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0',debug=True, port=8050)
