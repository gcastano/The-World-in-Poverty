import streamlit as st
from numerize.numerize import numerize
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import utils
from numerize.numerize import numerize


st.set_page_config(
    page_title="The World in Poverty",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap')
</style>
         """,unsafe_allow_html=True)

utils.local_css('estilo.css')
utils.remote_css("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css")
utils.remote_css("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap")



# Data preparation
dfPovertyData = pd.read_csv('PovertyData.csv')
dfPopulation = pd.read_csv('Population.csv')

# Selection functions
def getIndicator(df,indicatorCode):
    return df[df["Indicator Code"]==indicatorCode]
    
def getLastData(df):
    dfLastData=df.dropna().groupby('Country Code')['year'].max().reset_index()
    return df.merge(dfLastData, on=['Country Code','year'])

dfGini = getIndicator(dfPovertyData,"SI.POV.GINI")
dfPovDDAY =getIndicator(dfPovertyData,"SI.POV.DDAY")
dfPovNAHC =getIndicator(dfPovertyData,"SI.POV.NAHC")


dfPovDDAYRegion = dfPovDDAY.groupby(['year','Region']).agg({'population_indicator':'sum','population':'sum'}).reset_index()
dfPovDDAYRegion['percPovDDAY']=dfPovDDAYRegion['population_indicator']/dfPovDDAYRegion['population']
dfPovDDAYyear = dfPovDDAY.groupby('year').agg({'population_indicator':'sum','population':'sum'}).reset_index()
dfPovDDAYyearRegion = dfPovDDAY.groupby(['year','Region']).agg({'population_indicator':'sum','population':'sum'}).reset_index()
dfPovDDAYyear['percPovDDAY']=dfPovDDAYyear['population_indicator']/dfPovDDAYyear['population']


# Continuos variables categorization
dfPovDDAY['Poverty_level'] =pd.cut(dfPovDDAY['value'],bins=[0,3,10,20,30,40,50,60,70,80,100],labels=["3%","10%","20%","30%","40%","50%","60%","70%","80%","No Data"],ordered=True)
dfPovNAHC['Poverty_level'] =pd.cut(dfPovNAHC['value'],bins=[0,3,10,20,30,40,50,60,70,80,100],labels=["3%","10%","20%","30%","40%","50%","60%","70%","80%","No Data"],ordered=True)
# dfGini['Gini_level'] =pd.cut(dfGini['value'],bins=[0,10,20,30,40,50,60,70,80,100],labels=["10%","20%","30%","40%","50%","60%","70%","80%","No Data"],ordered=True)



dfPovDDAYLast = getLastData(dfPovDDAY)
dfPovNAHCLast = getLastData(dfPovNAHC)
dfGiniLast = getLastData(dfGini)
populationPoverty=dfPovDDAYLast['population_indicator'].sum()
population=dfPovDDAYLast['population'].sum()
countriesOver80=dfPovDDAYLast[dfPovDDAYLast['value']>=50]['Country Code'].count()
porcPoverty=populationPoverty/population

# Sidebar
with st.sidebar:
    st.write("**Author:** Germán Andrés Castaño Vásquez**")
    st.write("""
             **Sources:**
             * [World Bank Poverty Data](https://data.worldbank.org/topic/11)
             * [World Bank Population](https://data.worldbank.org/indicator/SP.POP.TOTL)
             * Some texts generated using ChatGPT and adapted by the author.
             """)

# Dashboard start
cols = st.columns([40,15,15,15,15])
with cols[0]:
    c1,c2 = st.columns([20,80])
    with c1:
        st.image('woman-with-no-money.svg',width=110)
    with c2:
        st.markdown('# The World in Poverty')
        st.write("Not up to date data, but sadly close...")
with cols[1]:
    st.metric('Total Population',numerize(population))
    st.caption("Data up to 2022")
with cols[2]:
    st.metric('People in poverty <$2.5',numerize(populationPoverty))    
    st.caption("Living with less than $2.5 per day")
with cols[3]:
    st.metric('% Population in poverty',f'{porcPoverty:.2%}')    
with cols[4]:
    st.metric('Countries with poverty > 50%',countriesOver80)  

c1,c2,c3= st.columns([40,35,25])
with c1:
    fig = px.choropleth(dfPovDDAYLast.sort_values('Poverty_level'), locations="Country Code",
                        color="Poverty_level", 
                        hover_name="Country Name",                               
                        color_discrete_sequence=px.colors.sequential.Reds[:10]+['grey'],
                        custom_data=['Country Name','population','population_indicator','value','year'],
                        labels={'Poverty_level':'Poverty level'},
                        title="Poverty headcount ratio at $2.15 a day (2017 PPP)"
                        )    
    hovertemp = "<b><span style='font-size:20px;color:#A94438'>%{customdata[0]}</span></b><br>"
    hovertemp += "Population:  %{customdata[1]:,.1f}<br>"
    hovertemp += "Poor people:  %{customdata[2]:,.1f}<br>"
    hovertemp += "Poverty %:  %{customdata[3]} %<br>"
    hovertemp += "Year data %:  %{customdata[4]}"
    fig.update_traces(hovertemplate=hovertemp)   
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="right",
        x=1
        ),
        margin=dict(l=20, r=20, t=20, b=20),)

    st.plotly_chart(utils.aplicarFormatoChart(fig,legend=True),use_container_width=True)
    
with c2:    
    dfScatter=dfPovDDAY.query('year>1980').dropna(subset=['Region']) 
    fig2 =px.scatter(dfScatter,x='year',y='value',                
                color='Region',
                trendline='ols',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hover_data=['Country Name','population','value','year'],                  
                labels={'Country Name':'Country','population':'Population','value':'% poverty'},
                title="Trend Poverty per year and region")    
    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="right",
        x=1
        ),
        margin=dict(l=20, r=20, t=20, b=20),)
    st.plotly_chart(utils.aplicarFormatoChart(fig2,legend=True),use_container_width=True)
with c3:
    st.subheader("Positive news? maybe...")
    st.write("""
            Global poverty has decreased due to economic growth, especially in Asia and Latin America, where industrialization and tech advancements boosted job opportunities. Education investments have empowered people to access better jobs, and social safety nets offer essential support. Inequality and climate change remain, requiring sustained efforts through sustainable development strategies, targeted policies, and international cooperation for further poverty reduction and a more prosperous future.
            **Central Africa remains critical and this haven't changed in years.**
            Although we don't have updated data for every country we could see decreasing trend what it's positive, **but we still have people who go to sleep hungry many times**.

             """)
c1,c2= st.columns(2)
with c1:
    c01,c02= st.columns([30,70])
    with c01:
        st.image('woman-sad.svg',width=200)
    with c02:
        st.subheader('National news are not as positive... sorry')
        st.write("""                
National poverty lines delineate the income threshold below which individuals or households are deemed impoverished within a particular country. They are determined by governments and factor in regional disparities, cost of living variations, and socio-economic conditions unique to each nation. Unlike global poverty measures, which offer a broad perspective across countries, national poverty lines provide a localized understanding of poverty within specific contexts.

However, **national poverty lines often reveal a more critical poverty scenario compared to global measures**. This is because they consider the actual cost of living and basic needs within each country, setting the poverty threshold higher. Consequently, while global measures may indicate progress in poverty reduction, national poverty lines may highlight a larger portion of the population struggling to meet their basic needs.
                 """)
with c2:
    fig = px.choropleth(dfPovNAHC.sort_values('Poverty_level'), locations="Country Code",
                        color="Poverty_level", 
                        hover_name="Country Name",
                        color_discrete_sequence=px.colors.sequential.Reds[:10]+['grey'],
                        custom_data=['Country Name','population','population_indicator','value','year'],
                        labels={'Poverty_level':'Poverty level'},
                        title="Poverty headcount ratio at national poverty lines (% of population)"
                        )
    hovertemp = "<b><span style='font-size:20px;color:#A94438'>%{customdata[0]}</span></b><br>"
    hovertemp += "Population:  %{customdata[1]:,.1f}<br>"
    hovertemp += "Poor people:  %{customdata[2]:,.1f}<br>"
    hovertemp += "Poverty %:  %{customdata[3]} %<br>"
    hovertemp += "Year data %:  %{customdata[4]}"
    fig.update_traces(hovertemplate=hovertemp)   
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="right",
        x=1
    ))

    st.plotly_chart(utils.aplicarFormatoChart(fig,legend=True),use_container_width=True)

c1,c2,c3= st.columns([40,35,25])
with c1:
    fig = px.choropleth(dfGiniLast, locations="Country Code",
                            color="value", 
                            hover_name="Country Name",                               
                            color_continuous_scale=px.colors.sequential.RdBu_r,
                            custom_data=['Country Name','population','population_indicator','value','year'],
                            labels={'value':'Gini level'},
                            title="Gini Index - Inequality measurement"
                            )
    hovertemp = "<b><span style='font-size:20px;color:#A94438'>%{customdata[0]}</span></b><br>"
    hovertemp += "Gini index:  %{y}<br>"
    hovertemp += "Population:  %{customdata[1]:,.1f}<br>"
    hovertemp += "Poor people:  %{customdata[2]:,.1f}<br>"
    hovertemp += "Gini Index:  %{customdata[3]} <br>"
    hovertemp += "Year data %:  %{customdata[4]}"
    fig.update_traces(hovertemplate=hovertemp)   
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="right",
        x=1
    ))
    st.plotly_chart(utils.aplicarFormatoChart(fig,legend=True),use_container_width=True)
with c2:
    dfTopGini=dfGiniLast.sort_values('value',ascending=False).head(10)[['Country Name','value','year']]
    dfTopGini.columns=['Country','Gini Index','Year']
    utils.generateTable(dfTopGini)
with c3:
    st.subheader("Sadly, being poor it's related to inequality")
    st.write("""
The Gini index, or Gini coefficient, is a statistical measure used to quantify the level of income or wealth inequality within a population. It is represented by a value between 0 and 1, where 0 represents perfect equality (everyone has the same income or wealth) and 1 represents perfect inequality (one person has all the income or wealth, while everyone else has none).

Essentially, the Gini index measures the extent to which the distribution of income or wealth deviates from perfect equality. A higher Gini index indicates greater inequality, meaning that a smaller portion of the population holds a larger share of the total income or wealth, while a lower Gini index suggests a more equal distribution.
             """)
st.subheader("How is this in your region or country?")


dfPovDDAY=dfPovDDAY.dropna(subset=['Region'])
parmCountry=st.selectbox("Country",options=dfPovDDAY['Country Name'].unique(),index=0)
if len(parmCountry)>0:    
    dfPovDDAY=dfPovDDAY[dfPovDDAY['Country Name']==parmCountry]    
    countryRegion=dfPovDDAY.head(1)['Region'].values[0]    
    dfGini=dfGini[(dfGini['Country Name']==parmCountry)]
    dfPovNAHC=dfPovNAHC[(dfPovNAHC['Country Name']==parmCountry)]    
c1,c2,c3 = st.columns(3)
with c1:
    if len(dfPovDDAY.dropna(subset='value'))>0:
        fig=px.line(dfPovDDAY,x='year',y='value',color_discrete_sequence=['#f4b3b3'], 
                    labels={'value':'Poverty %'},
                    title=f"Poverty under $2.15 for {parmCountry}")
        st.plotly_chart(utils.aplicarFormatoChart(fig,controls=True),use_container_width=True)

        dfPovDDAYLast=dfPovDDAYLast[dfPovDDAYLast['Region']==countryRegion]
        dfTop=dfPovDDAYLast.sort_values('value',ascending=False)[['Country Name','value','year']]    
        dfTop['Rank']=dfTop['value'].rank(ascending=False)
        dfTop.columns=['Country','Poverty %','Year','Rank']
        dfTop=dfTop[['Rank','Country','Poverty %','Year']]
        with st.container(height=300):
            st.write(f"**Region:** {countryRegion}")
            utils.generateTable(dfTop)
    else:
        st.warning(f'No data available about Poverty under $2.15 for {parmCountry}')
with c2:
    if len(dfPovNAHC.dropna(subset='value'))>0:
        fig=px.line(dfPovNAHC,x='year',y='value',color_discrete_sequence=['#f4b3b3'], 
                    labels={'value':'Under Poverty line %'},
                    title=f"Poverty under National poverty line for {parmCountry}")
        st.plotly_chart(utils.aplicarFormatoChart(fig,controls=True),use_container_width=True)
        dfPovNAHCLast=dfPovNAHCLast[dfPovNAHCLast['Region']==countryRegion]
        dfTop=dfPovNAHCLast.sort_values('value',ascending=False)[['Country Name','value','year']]
        dfTop['Rank']=dfTop['value'].rank(ascending=False)
        dfTop.columns=['Country','National Poverty %','Year','Rank']    
        dfTop=dfTop[['Rank','Country','National Poverty %','Year']]
        with st.container(height=300):
            st.write(f"**Region:** {countryRegion}")
            utils.generateTable(dfTop)
    else:
        st.warning(f'No data available about National Poverty for {parmCountry}')
with c3:
    if len(dfGini.dropna(subset='value'))>0:
        fig=px.line(dfGini,x='year',y='value',color_discrete_sequence=['#f4b3b3'], 
                    labels={'value':'Under Poverty line %'},
                    title=f"Gini index for {parmCountry}")
        st.plotly_chart(utils.aplicarFormatoChart(fig,controls=True),use_container_width=True)
        dfGiniLast=dfGiniLast[dfGiniLast['Region']==countryRegion]
        dfTop=dfGiniLast.sort_values('value',ascending=False)[['Country Name','value','year']]
        dfTop['Rank']=dfTop['value'].rank(ascending=False)
        dfTop.columns=['Country','Gini Index','Year','Rank']
        dfTop=dfTop[['Rank','Country','Gini Index','Year']]
        with st.container(height=300):
            st.write(f"**Region:** {countryRegion}")
            utils.generateTable(dfTop)
    else:
        st.warning(f'No data available about Gini index for {parmCountry}')