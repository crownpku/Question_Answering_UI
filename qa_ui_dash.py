import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import requests
import json

app = dash.Dash(__name__)
app.title = 'Question Answering Demo'
app.layout = html.Div([
    html.H1(
        children = "Question Answering Demo",
        style={
            'textAlign': 'center'
        }
    ),
    html.H2(
        children = "crownpku@gmail.com",
        style={
            'textAlign': 'center'
        }
    ),
    html.H3("Please input text here:"),
    dcc.Textarea(
        id='raw-text',
        value="Singapore (/ˈsɪŋ(ɡ)əpɔːr/), 新加坡 in Chinese, officially the Republic of Singapore, is a sovereign island city-state in maritime Southeast Asia. It lies about one degree of latitude (137 kilometres or 85 miles) north of the equator, off the southern tip of the Malay Peninsula, bordering the Straits of Malacca to the west, the Riau Islands (Indonesia) to the south, and the South China Sea to the east. The country's territory is composed of one main island, 63 satellite islands and islets, and one outlying islet, the combined area of which has increased by 25% since the country's independence as a result of extensive land reclamation projects. It has the second greatest population density in the world. The country has almost 5.7 million residents, 61% (3.4 million) of whom are Singaporean citizens. There are four official languages of Singapore: English, Malay, Chinese and Tamil. English is the lingua franca. Multiracialism is enshrined in the constitution, and continues to shape national policies in education, housing, and politics.",
        style={'width': '100%', 'height': 300},
    ),
    html.H3("Please input your question here:"),
    dcc.Textarea(
        id='raw-question',
        value='What is the population of Singapore?',
        style={'width': '100%', 'height': 50},
    ),
    html.Button('Submit', id='qa-submit-button', n_clicks=0),
    html.Div(id='qa-output', style={'whiteSpace': 'pre-line'})
])

@app.callback(
    Output('qa-output', 'children'),
    Input('qa-submit-button', 'n_clicks'),
    State('raw-text', 'value'),
    State('raw-question', 'value')
)
def update_output(n_clicks, text, question):
    if n_clicks > 0:
        headers = {
            'Content-Type': 'application/json',
        }
        data_dic = {}
        data_dic['document'] = text
        data_dic['question'] = question
        data = json.dumps(data_dic)
        #data = '{ "document": "' + text.encode('utf-8') + '","question":"' + question.encode('utf-8') + '" }'
        #data = '{ "document": "' + text + '","question":"' + question + '" }'
        response = requests.post('http://0.0.0.0:8000/predict', headers=headers, data=data)
        res_json = json.loads(response.text)
        answer = res_json['result']['answer']
        confidence = res_json['result']['confidence']
        doc_lst = res_json['result']['document']
        start_pos = res_json['result']['start']
        end_post = res_json['result']['end']
        highlght_text = ""
        for n, item in enumerate(doc_lst):
            if n >= start_pos and n <= end_post:
                highlght_text = highlght_text + '**' + item + '** '
            else:
                highlght_text = highlght_text + item + ' '
        highlght_text = highlght_text.strip()
        
        md_results = f'''
        Answer is **{answer}**
        Confidence is **{confidence}**
        ### Answer Source
        {highlght_text}
        '''
         
        return dcc.Markdown(md_results)
        #return 'Your answers are: \n{}'.format(answer)

if __name__ == '__main__':
    app.run_server(debug=True)
