import Interc1, Interc2, Psat, Sec_meth

from dash import Dash, dcc, html, Output, Input    # dcc: dash core components. Output and Input are parts of the Callback
import dash_bootstrap_components as dbc     # dbc: dash bootstrap component

# (Patm, Tairk, xair, TfumK, xfum)

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])  # starts Dash up, and choose a theme

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

#mytitle = dcc.Markdown(children='# Fumes Re-heater')

# Customise your own layout
app.layout = html.Div([html.H1("Fumes Re-heater"),
                            dcc.Input(id='Patm', type='number', placeholder='Enter Patm (Pa)'),
                            dcc.Input(id='TairC', type='number', placeholder='Enter Tair (oC)'),
                            dcc.Input(id='RH_air', type='number', placeholder='Enter RH_air (%)'),
                            dcc.Input(id='TfumC', type='number', placeholder='Enter Tfum (oC)'),
                            dcc.Input(id='RH_fum', type='number', placeholder='Enter RH_fum (%)'),
                            html.Div(id='output1'),
                            html.Div(id='output2'),
                            html.Div(id='output3'),
                            html.Div(id='output4'),
                            html.Div(id='output5'),
                            html.Button('Calculate', id='button'),
])   # This line put the dcc components inside the layout

@app.callback(
    Output('output1', 'children'),
    [Input('button', 'n_clicks')],
    [Input('Patm', 'value')],
    [Input('TairC', 'value')],
    [Input('RH_air', 'value')],
    [Input('TfumC', 'value')],
    [Input('RH_fum', 'value')],
)

def update_output(n_clicks, Patm, TairC, RH_air, TfumC, RH_fum):
    if n_clicks is None:
        return ''
    else:


        Patm = Patm #100600
        Tairk = TairC + 273.15 #5 + 273.15
        RHatm = RH_air #70
        Tfumk = TfumC + 273.15 #64 + 273.15
        RHfum = RH_fum # 40

        Psat_air = Psat.Psat(Tairk)
        Psat_fum = Psat.Psat(Tfumk)

        Pw_air = RHatm/100 * Psat_air
        Pw_fum = RHfum/100 * Psat_fum

        xair = 0.62198 * Pw_air / (Patm - Pw_air)
        xfum = 0.62198 * Pw_fum / (Patm - Pw_fum)

        m_air_fum = (xfum - xair) / (Tfumk - Tairk)

        Der_xs = Sec_meth.sec_meth(Tairk, RHatm, Patm)

        if Der_xs > m_air_fum:
            return f'There is not condensation'
            #print("There is not condensation")
        else:
            Tcb = Interc2.Interc2(Tairk, Patm, xair, Tfumk, xfum)  # Condensantion begins at this temperature oC
            Tce = Interc1.Interc1(Patm, Tairk, xair, Tfumk, xfum)  # Condensantion ends at this temperature oC
            Treheat = (xfum-xair)/Der_xs + (Tairk-273.15)  # Temp to avoid condensation oC
            RH_reheat = Patm * xfum * 100 / ((0.62198 + xfum) * Psat.Psat(Treheat + 273.15))

            # return  f"""There is condensation,
            #  begins @ {round(Tcb,1)}oC and ends @ {round(Tce,1)}oC
            #  The temperature to avoid condensation is {round(Treheat)}oC,
            #  with this new temperature the fumes RH is {round(RH_reheat,1)}%"""

            return f"""There is condensation,
                        begins @ {round(Tcb,1)}oC and ends @ {round(Tce,1)}oC
                        The temperature to avoid condensation is {round(Treheat)}oC, 
                        with this new temperature the fumes RH is {round(RH_reheat,1)}%"""

            #print(f"There is condensation, begins @ {round(Tcb,1)}oC and ends @ {round(Tce,1)}oC,\nTemperature to avoid condensation {round(Treheat)}oC, \nNew RH_fumes at Trheat {round(RH_reheat,1)}% ")

if __name__=='__main__':
   # app.run_server(debug=True, host='0.0.0.0', port=8050)
    app.run_server(port=8050)





#print(f"the values is {Psat_air} and {Psat_fum} and {Tfumk} and {m_air_fum} and {Der_xs}")

