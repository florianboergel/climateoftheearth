import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

from IPython.display import HTML
from IPython.display import display

import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from model import ebm
from readData import readDataTemp, createCO2timeSeries, readDataCO2

co2Data = pd.read_csv("ssp/mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_AerChemMIP_UoM-AIM-ssp370-lowNTCF-1-2-1_gr1-GMNHSH_2015-2500.csv", index_col=0)
co2Data2024Onwards = co2Data.loc[2024:]
co2levels = createCO2timeSeries(co2Data2024Onwards["data_mean_global"])

def CO2_scenario(t, co2levels = co2levels):
    return co2levels.values[t]

#### App ##### 

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f9f9f9',
        'padding': '20px'
    },
    children=[
        html.H1(
            "Die Erde als einzelner Pixel - ein stark vereinfachtes Klimamodell",
            style={
                'textAlign': 'center',
                'color': '#333'
            }
        ),
        html.Div(
            children=[
                html.Img(src='/assets/ebm.png', style={'width': '400px', 'height': 'auto'}),
            ],
            style={
                'textAlign': 'center',
                'marginBottom': '20px'
            }
        ),
        dcc.Dropdown(
            id='file-dropdown',
            options=[
                {'label': 'SSP119', "value": "mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-IMAGE-ssp119-1-2-1_gr1-GMNHSH_2015-2500.csv"},
                {'label': 'SSP245', 'value': 'mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-MESSAGE-GLOBIOM-ssp245-1-2-1_gr1-GMNHSH_2015-2500.csv'},
                {'label': 'SSP370', 'value': 'mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_AerChemMIP_UoM-AIM-ssp370-lowNTCF-1-2-1_gr1-GMNHSH_2015-2500.csv'},
                {'label': 'SSP460', 'value': "mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-GCAM4-ssp460-1-2-1_gr1-GMNHSH_2015-2500.csv"},
                {'label': 'SSP585', "value": "mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.csv"},
                # Add more file options as needed
            ],
            value='mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_AerChemMIP_UoM-AIM-ssp370-lowNTCF-1-2-1_gr1-GMNHSH_2015-2500.csv',
            style={
                'marginBottom': '20px'
            }
        ),
        dcc.Markdown(
            id='ssp-description',
            style={
                'whiteSpace': 'pre-line',
                'padding': '15px',
                'border': '1px solid #ccc',
                'borderRadius': '5px',
                'backgroundColor': '#fff',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'marginBottom': '20px'
            }
        ),
        dcc.Graph(
            id='temperature-graph',
            style={
                'marginBottom': '20px'
            }
        ),
        dcc.Graph(
            id='co2-graph'
        )
    ]
)

@app.callback(
    [Output('co2-graph', 'figure'),
     Output('temperature-graph', 'figure'),
     Output('ssp-description', 'children')],
    Input('file-dropdown', 'value')
)

def update_figure(selected_file):
    # Load the selected CSV file (this example assumes files are in the same format)
    # Replace the file paths as necessary
    print(selected_file)

    co2Data = pd.read_csv(f"ssp/{selected_file}", index_col=0, engine='python')
    co2Data2024Onwards = co2Data.loc[2024:]
    co2levels = createCO2timeSeries(co2Data2024Onwards["data_mean_global"])
    temp = readDataTemp()
    co2_data = readDataCO2()

    def CO2_scenario(t, co2levels = co2levels):
        return co2levels.values[t]
    model = ebm(14, 0, int(1), CO2_scenario)
    model.run(651)
    print("model finished")

    fig_co2 = go.Figure()

    fig_co2.add_trace(go.Scatter(x=np.arange(1850, 2501), y=CO2_scenario(np.arange(0, 651)), mode='lines', name='EBM model'))
    fig_co2.add_trace(go.Scatter(x=co2_data.index, y=co2_data.values, mode='lines', name='Keeling Curve'))

    fig_co2.update_layout(
        xaxis_title='Year',
        yaxis_title='CO2 concentration [ppm]',
        title='CO2 Concentration over Time'
    )

    fig_temperature = go.Figure()
    
    fig_temperature.add_trace(go.Scatter(x=np.arange(1850, 2502), y=model.T, mode='lines', name='EBM model'))
    temp_series = temp.squeeze()
    print(temp_series.values[:,0])
    fig_temperature.add_trace(go.Scatter(x=temp_series.index, y=temp_series.values[:,0], mode='lines', name='NASA Observations'))

    fig_temperature.update_layout(
        yaxis2=dict(
            title='Temperature [°C]',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            x=0,
            y=1,
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    fig_temperature.add_hline(y=16, line=dict(dash='dash', color='black'), annotation_text="Paris Agreement\nthreshold (2°C warming)", annotation_position="bottom right")

    fig_co2.update_xaxes(range=[1850, 2100])
    fig_temperature.update_xaxes(range=[1850, 2100])
    fig_temperature.update_yaxes(range=[13.5,17])


    ssp_description = ""

    if selected_file == 'mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-IMAGE-ssp119-1-2-1_gr1-GMNHSH_2015-2500.csv':
        ssp_description = """
        **SSP1-2.9 (Nachhaltigkeit)**: Der nachhaltige und grüne Weg beschreibt eine zunehmend nachhaltige Welt. Globale Gemeinschaftsgüter werden bewahrt, die Grenzen der Natur werden respektiert. Statt Wirtschaftswachstum steht zunehmend das menschliche Wohlbefinden im Fokus. Einkommensungleichheiten zwischen den Staaten und innerhalb der Staaten werden reduziert. Der Konsum orientiert sich an geringem Material- und Energieverbrauch.
        
        - Strenge Klimapolitik und globale Zusammenarbeit zur Reduzierung von Treibhausgasemissionen.
        - Schneller technischer Fortschritt und breiter Zugang zu sauberen Energiequellen.
        - Änderungen im Konsumverhalten hin zu weniger ressourcenintensiven Lebensstilen.
        - Bedeutende Investitionen in Bildung und Gesundheit, um soziale Ungleichheiten zu verringern.
        """

    elif selected_file == 'mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-MESSAGE-GLOBIOM-ssp245-1-2-1_gr1-GMNHSH_2015-2500.csv':
        ssp_description = """
        **SSP2-4.5 (Mittlere Straße)**: Der mittlere Weg schreibt die bisherige Entwicklung fort. Einkommensentwicklungen einzelner Länder gehen weit auseinander. Es gibt eine gewisse Zusammenarbeit zwischen den Staaten, die jedoch nur geringfügig weiterentwickelt wird. Das globale Bevölkerungswachstum ist moderat und schwächt sich in der zweiten Jahrhunderthälfte ab. Umweltsysteme erfahren eine gewisse Verschlechterung.
        
        - Moderate Klimapolitik mit einem ausgewogenen Ansatz zwischen wirtschaftlichem Wachstum und Reduzierung von Treibhausgasemissionen.
        - Stetiger technischer Fortschritt mit zunehmender, aber nicht allgegenwärtiger Nutzung sauberer Energiequellen.
        - Stabilisierung des Konsumverhaltens, wobei sowohl ressourcenintensive als auch nachhaltigere Lebensstile koexistieren.
        - Kontinuierliche, aber begrenzte Investitionen in Bildung und Gesundheit zur Minderung sozialer Ungleichheiten.
        """

    elif selected_file == 'mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-GCAM4-ssp460-1-2-1_gr1-GMNHSH_2015-2500.csv':
        ssp_description = """
        **SSP4-6.0 (Ungleiche Welt)**:  Die Kluft zwischen entwickelten Gesellschaften, die auch global kooperieren, und solchen, die auf einer niedrigen Stufe der Entwicklung mit niedrigem Einkommen und geringem Bildungsstand verharren, nimmt weiter zu. In einigen Regionen ist Umweltpolitik bei lokalen Problemen erfolgreich, in anderen nicht.
        
        - Moderat strenge Klimapolitik mit ungleicher Umsetzung, stark abhängig von regionalen Gegebenheiten und Interessen.
        - Technischer Fortschritt variiert stark zwischen fortgeschrittenen und weniger entwickelten Regionen, mit beschränktem Zugang zu sauberen Energiequellen in ärmeren Ländern.
        - Stark variierendes Konsumverhalten, wobei reiche Regionen ressourcenintensive Lebensstile pflegen und ärmere Regionen eher ressourcenschonend agieren müssen.
        - Unterschiedliche Investitionen in Bildung und Gesundheit, was die sozialen Ungleichheiten weiter verstärkt und die Kluft zwischen verschiedenen gesellschaftlichen Gruppen vertieft.
        """

    elif selected_file == 'mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_AerChemMIP_UoM-AIM-ssp370-lowNTCF-1-2-1_gr1-GMNHSH_2015-2500.csv':
        ssp_description = """
        **SSP3-7.0 (Regionale Rivalität)**: Eine Wiederbelebung des Nationalismus und regionale Konflikte rücken globale Themen in den Hintergrund. Die Politik orientiert sich zunehmend an nationalen und regionalen Sicherheitsfragen. Investitionen in Bildung und technologische Entwicklung nehmen ab. Ungleichheiten nehmen zu. In einigen Regionen kommt es zu starken Umweltzerstörungen.
        
        - Schwache Klimapolitik und begrenzte internationale Zusammenarbeit zur Reduzierung von Treibhausgasemissionen.
        - Langsamer technischer Fortschritt und uneinheitlicher Zugang zu sauberen Energiequellen.
        - Stark ressourcenintensive Konsummuster, da regionale Märkte und Eigeninteressen dominieren.
        - Geringe Investitionen in Bildung und Gesundheit, was zu anhaltenden oder sogar zunehmenden sozialen Ungleichheiten führt.
        """

    elif selected_file == 'mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.csv':
        ssp_description = """
        **SSP5-8.5 (Fossil-getriebene Entwicklung)**: Die globalen Märkte sind zunehmend integriert, mit der Folge von Innovationen und technologischem Fortschritt. Die soziale und ökonomische Entwicklung basiert jedoch auf der verstärkten Ausbeutung fossiler Brennstoffressourcen mit einem hohen Kohleanteil und einem weltweit energieintensiven Lebensstil. Die Weltwirtschaft wächst und lokale Umweltprobleme wie die Luftverschmutzung werden erfolgreich bekämpft.
        
        - Lockerere Klimapolitik mit Schwerpunkt auf wirtschaftlicher Expansion und hoher Nutzung fossiler Brennstoffe.
        - Rascher technischer Fortschritt, jedoch stark auf fossile Energiequellen gestützt.
        - Hoher Ressourcenverbrauch und ressourcenintensive Konsummuster aufgrund des starken Wirtschaftswachstums.
        - Bedeutende Investitionen in Bildung und Gesundheit, um die Ungleichheiten zu verringern, jedoch mit einem Fokus auf wirtschaftliche Produktivität und technologische Innovation.
        """

    return fig_co2, fig_temperature, ssp_description

if __name__ == '__main__':
    app.server.run(port=8050, host='127.0.0.1', debug=False)
