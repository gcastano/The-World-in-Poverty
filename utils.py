import plotly.express as px
import streamlit as st
from streamlit_extras.stylable_container import stylable_container



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)   


def generateIconMetric(fa_icon):              
    return st.write(f'<div class="iconMetric" style="background-color:#5155c3;height:70px;width:70px;text-align:center"><i class="fa-solid {fa_icon} fa-2xl" style="line-height:50px;margin:auto;color:white;"></i></div>', unsafe_allow_html=True)        

def aplicarFormatoChart(fig,controls=False,legend=False,hoverTemplate=None):
    fig.update_layout(paper_bgcolor='white')
    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(showlegend=legend)
    fig.update_layout(title_pad_l=20)
    fig.update_layout(
    #font_family="Open Sans",
    #font_color="#8dc73f",
    # title_font_family="Open Sans",
    title_font_color="#A94438",
    title_font_size=20,
    font_size=15,
    #legend_title_font_color="green"
    )

    if hoverTemplate:
        if hoverTemplate=="%":
            fig.update_traces(hovertemplate='<b>%{x}</b> <br> %{y:,.2%}')
        elif hoverTemplate=="$":
            fig.update_traces(hovertemplate='<b>%{x}</b> <br> $ %{y:,.1f}')
        elif hoverTemplate=="#":
            fig.update_traces(hovertemplate='<b>%{x}</b> <br> %{y:,.0f}')
    if controls:
        fig.update_xaxes(
            rangeslider_visible=True,
            # rangeselector=dict(
            #     buttons=list(
            #         [
            #             dict(step="day", stepmode="backward", label="1 semana", count=7),
            #             dict(step="month", stepmode="backward", label="1 mes", count=1),
            #             dict(step="month", stepmode="backward", label="3 meses", count=3),
            #             dict(step="month", stepmode="backward", label="6 meses", count=6),
            #             dict(label="Todos", step="all"),
            #         ]
            #     )
            # ),
        )
    fig.update_layout(
            autosize=True,
            margin=dict(
                # l=0,
                # r=0,
                b=0,
                t=100,
                # pad=4
            )
    )
    return fig


def adicionarAnotacion(fig,txtFecha,txtValor,colorbg,colortxt,xAnchor='auto',yAnchor='auto'):
    fig.add_annotation(x=txtFecha, y=txtValor,
                text=f"{txtValor:,.2%} <br> {txtFecha:%b %d %Y}",
                showarrow=True,
                align="center",
            font=dict(
                #family="Courier New, monospace",
                size=15,
                color=colortxt
                ),
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=colorbg,
            ax=20,
            ay=-30,
            bordercolor=colorbg,
            borderwidth=2,
            borderpad=4,
            bgcolor=colorbg,
            opacity=0.8,
            xanchor=xAnchor,
            yanchor=yAnchor)
    return fig

def generarFunnel(dfDatos,color_pallete, titulo):
    data = dict(
    number=[dfDatos['Población total']*1000, dfDatos['Población en edad de trabajar']*1000,dfDatos['Fuerza de trabajo']*1000,dfDatos['Población desocupada']*1000],
    percent=[1, dfDatos['Población en edad de trabajar']/dfDatos['Población total'],dfDatos['Fuerza de trabajo']/dfDatos['Población en edad de trabajar'],dfDatos['Población desocupada']/dfDatos['Fuerza de trabajo']],
    stage=["Población total (PT)", "Población en edad de trabajar (PET)", "Fuerza de trabajo (FT)", "Población desocupada (DS)"])
    figFunnelGeneral = px.funnel(data, x='number', y='stage',text='number', custom_data=['percent'], color_discrete_sequence=color_pallete,title=titulo)
    figFunnelGeneral.update_traces(texttemplate= '<b>%{text:,.0f} personas </b><br> %{customdata[0]:,.2%}') 
    figFunnelGeneral.update_layout(hovermode=False)
    return figFunnelGeneral

def generarTextoIndicador(valorVariacion,formato='#',textoComplemento='',inverse=False):
    
    if inverse:        
        if valorVariacion<=0:
            icono='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-jhkj9c ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"></path></svg>'
            colorAno='rgb(9, 171, 59);'
        else:            
            icono='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-jhkj9c ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"></path></svg>'                                                
            colorAno='rgb(255, 43, 43)'
    else:
        if valorVariacion<=0:
            icono='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-jhkj9c ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"></path></svg>'            
            colorAno='rgb(255, 43, 43)'
        else:
            icono='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-jhkj9c ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"></path></svg>'
            colorAno='rgb(9, 171, 59);'            

    if formato=="#":
        textoMensaje = f'''
                <div class='texto2Metrica' style='top:-20px;position:relative;color:{colorAno}'>
                {icono}{valorVariacion:,.0f} {textoComplemento}.
                </div>
            '''
    else:
        textoMensaje = f'''
                <div class='texto2Metrica' style='top:-20px;position:relative;color:{colorAno}'>
                {icono}{valorVariacion:,.2%} % {textoComplemento}.
                </div>
            '''
        
    return textoMensaje


def iconMetricContainer(key,iconUnicode,color='grey'):
    """Function that returns a CSS styled container for adding a Material Icon to a Streamlit st.metric value

    Args:
        key (str): Unique key for the component
        iconUnicode (str): Code point for a Material Icon, you can find them here https://fonts.google.com/icons. Sample \e8b6 
        color (str, optional): HTML Hex color value for the icon. Defaults to 'grey'.

    Returns:
        DeltaGenerator: A container object. Elements can be added to this container using either the 'with'
        notation or by calling methods directly on the returned object.
    """
    css_style=f'''                 
                    div[data-testid="stMetricValue"]>div::before
                    {{                            
                        font-family: "Material Icons";
                        content: "{iconUnicode}";
                        vertical-align: -20%;
                        color: {color};
                    }}                    
                    '''
    iconMetric=stylable_container(
                key=key,
                css_styles=css_style
            )
    return iconMetric

def generateTable(df):
    """Generate HTML table formated for the dashboard

    Args:
        df (DataFrame): Dataframe used to generate the table
    """    
    style = '''
<style type="text/css">
.dashboardTable {
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 0.9em;
    font-family: sans-serif;    
    max-width:100%
}
.dashboardTable thead tr {
    background-color: #f4b3b3;
    color: #ffffff;
    text-align: left;
}
.dashboardTable th,
.dashboardTable td {
    /* padding: 5px 5px; */
    border:none;
}

.dashboardTable tbody tr {
    border-bottom: 1px solid #dddddd;
    background-color:white;
}

.dashboardTable tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}
</style>
'''
    header = '</th><th>'.join(df.columns)
    header = f'<thead><tr><th>{header}</th><tr></thead>'
    items = ''
    for index, row in df.iterrows():        
        item= [f'<td>{x}</td>' if type(x)==str else f'<td style="text-align:right">{x:,.1f}</td>' for x in row.tolist()]        
        item=''.join(item)
        item = f'<tr>{item}<tr>'
        items=items+item
    table = f'<table class="dashboardTable">{header}<tbody>{items}</tbody></table>'
    # return table
    st.write(table,unsafe_allow_html=True)