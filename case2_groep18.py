#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Importen van benodigde packages.
import requests
import json
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


# In[3]:


#Inladen van de data via API.
url = "https://opendata.cbs.nl/ODataApi/odata/82635NED/TypedDataSet"
response = requests.get(url)
json = response.json()
df = pd.DataFrame.from_dict(json["value"])


# In[4]:


#De data filteren zodat er alleen nog gemiddelden en percentages over zijn.
df1 = df[df['Cijfersoort'] == 'B000167']


# In[5]:


#De namen in de kolommen aanpassen naar begrijpbare steekwoorden.
df2 = df1.replace({'2013JJ00' : 2013,
            '2014JJ00' : 2014,
            '2015JJ00' : 2015,
            '2016JJ00' : 2016,
            '2017JJ00' : 2017, 
            '2018JJ00' : 2018, 
            '2019JJ00' : 2019, 
            '2020JJ00' : 2020,
            '2021JJ00' : 2021, 
            'T009002' : 'Totaal',
            '3000805' : 'Niet betaald',
            '3000795' : 'Betaald',
            '2021210' : 'Minder dan 12',
            '2021220' : 'Tussen 12 en 20',
            '2021230' : 'Tussen 20 en 35',
            '2021240' : 'Meer dan 35'})


# In[6]:


#Kolomnamen aanpassen
df3 = df2.rename(columns =  {'ScoreGeluk_1' : 'Score geluk',
            'ScoreTevredenheidMetHetLeven_5' : 'Tevredenheid met het leven',
            'ScoreTevredenheidOpleidingskansen_9' : 'Tevredenheid opleidingskansen',
            'ScoreTevredenheidMetWerk_13' : 'Tevredenheid werk',
            'ScoreTevredenheidMetReistijd_17' : 'Tevredenheid met reistijd',
            'ScoreTevredenheidDagelijkseBezigheden_21' : 'Tevredenheid dagelijkse bezigheden'})
df3 = df3.fillna(0)


# In[6]:


st.title('Hoe gelukkig is de werkende bevolking in Nederland?')


# In[7]:


st.write('Het CBS heeft een onderzoek gehouden onder personen van 18 jaar en ouder. De cijfers van het CBS gaan over het welzijn van de Nederlandse bevolking in termen van geluk en tevredenheid met het leven, het werk en de reistijd naar het werk. Ook is de tevredenheid met de dagelijkse bezigheden opgenomen. Deze onderwerpen zijn uitgesplitst naar verschillende kenmerken met het betrekking tot het werk: arbeidspositie en wekelijkse arbeidsduur.')


# In[8]:


st.write('Hieronder zal er worden laten zien hoe deze data is geanalyseerd en wat voor conclusies hieruit zijn getrokken.')


# In[9]:


st.header('Het inspecteren van de data')


# In[10]:


st.write('De data van het CBS bestaat uit een algemeen deel en een deel dat betrekking heeft op opleiding en werk. Het algemene deel gaat over geluk en tevredenheid met het leven. Het deel over opleiding en werk gaat over tevredenheid met opleidingskansen, tevredenheid met werk, tevredenheid met reistijd en tevredenheid met dagelijkse bezigheden. ')


# In[11]:


#Het plaatje staat online op github.
from PIL import Image
image = Image.open('Picture welzijn in relatie met opleiding en werk.jpg')

st.image(image)


# In[12]:


st.write('De deelnemers van de enquête zijn in verschillende categorieën opgedeeld, betaald of niet betaald werken en de hoeveelheid die zij werken: minder dan 12 uur, 12 tot 20 uur, 20 tot 35 uur of voltijd. De categorieën de afbeelding hieronder aan de linkerkant afgebeeld.  ')


# In[13]:


#Het plaatje staat online op github.
image2 = Image.open('Picture variabelen.jpg')
st.image(image2)


# In[14]:


st.write('Tijdens het inspecteren van de data, kwamen we diverse onbekende waarden tegen. In de afbeelding hierboven is te zien in welke categorieën de onbekende waarden zitten, namelijk: ‘tevredenheid met werk’, ‘tevredenheid met reistijd’ en ‘tevredenheid met dagelijkse bezigheden’. De reden dat deze waarden ontbreken is dat het CBS besloten heeft om mensen die geen betaalde arbeidspositie of een werkduur van minder dan 12 uur hebben, niet te vragen naar tevredenheid met werk en reistijd. Aan deze mensen is gevraagd naar de ‘tevredenheid met de dagelijkse bezigheden’.')


# In[15]:


st.write('Daarnaast hebben we ook geconstateerd dat er een standaarddeviatie in de dataset aanwezig was. Wij hebben besloten deze buiten onze analyse te laten en ons te focussen op de gemiddelde cijfers en de percentages. In een vervolgonderzoek kan het interessant zijn om de standaarddeviaties wel mee te nemen.')


# In[16]:


st.header('Analyse')


# In[17]:


st.write('Na het inspecteren van de data zijn we deze gaan analyseren. Dit hebben we gedaan door te kijken naar de schommeling van de cijfers over de jaren 2013 tot en met 2021 per categorie en per variabele. In de visualisatie hieronder is het verloop van de cijfers door de jaren heen te zien. Zo kan u met de slider de categorie bepalen en met het dropdown-menu kiezen welke variabelen u wilt zien.')


# In[18]:


#Checkbox om wel of niet de lijnplot te laten zien
checkbox = st.checkbox(label = 'Lijnplot laten zien')


# In[19]:


#Selectbox voor alle variabelen.
variabelen = ['Score geluk', 'Tevredenheid met het leven', 'Tevredenheid opleidingskansen',
            'Tevredenheid werk', 'Tevredenheid met reistijd', 'Tevredenheid dagelijkse bezigheden']
selectbox = st.sidebar.selectbox(label = 'Variabelen', options = variabelen)


# In[20]:


#SLider maken voor de lijnplot
sliders = [
    {'steps': [
        {'method' : 'update', 'label' : 'Totaal',
        'args' : [{'visible' : [True, False, False, False, False, False, False]}]},
        {'method' : 'update', 'label' : 'Minder dan 12 uur',
        'args' : [{'visible' : [False, True, False, False, False, False, False]}]},
        {'method' : 'update', 'label' : 'Tussen de 12 en 20 uur',
        'args' : [{'visible' : [False, False, True, False, False, False, False]}]},
        {'method' : 'update', 'label' : 'Tussen de 20 en 35 uur',
        'args' : [{'visible' : [False, False, False, True, False, False, False]}]},
        {'method' : 'update', 'label' : 'Meer dan 35 uur',
        'args' : [{'visible' : [False, False, False, False, True, False, False]}]},
        {'method' : 'update', 'label' : 'Betaald werk',
        'args' : [{'visible' : [False, False, False, False, False, True, False]}]},
        {'method' : 'update', 'label' : 'Niet betaald werk',
        'args' : [{'visible' : [False, False, False, False, False, False, True]}]}
    ]}
]


# In[21]:


#Code voor de lineplot
fig = go.Figure()
for werkgroep in ['Totaal', 'Minder dan 12', 'Tussen 12 en 20', 'Tussen 20 en 35', 'Meer dan 35', 'Betaald', 'Niet betaald']:
    df = df3[df3['KenmerkenWerk'] == werkgroep]
    fig.add_trace(go.Scatter(x = df["Perioden"], y = df[selectbox], mode = 'lines',
                            name = werkgroep))
fig.update_layout({'sliders' : sliders}, 
                  yaxis_range = [7, 8.5],
                  xaxis_title = 'Jaren',
                  yaxis_title = selectbox,
                  title = 'Tevredenheid van de werkende bevolking')
if checkbox:
    st.plotly_chart(fig)


# In[22]:


st.write('Uit de lijngrafiek kunnen we concluderen dat de werkende Nederlandse bevolking de afgelopen 8 jaar ongeveer even gelukkig is gebleven.  Wel zien we dat bepaalde categorieën een kleine daling van de cijfers in de laatste jaren laten zien. De Score van Geluk van mensen die minder dan 12 uur werken daalt bijvoorbeeld met 0.3. Ook daalt de score van mensen die tussen de 12-24 uur werken met 0.3. Wij denken dat een mogelijk oorzaak hiervoor de coronacrisis kan zijn.')


# In[23]:


#Checkbox om wel of niet de barplot te laten zien
checkbox2 = st.checkbox(label = 'Barplot laten zien')


# In[24]:


#SLider maken voor de barplot
sliders2 = [
    {'steps': [
        {'method' : 'update', 'label' : 'Totaal',
        'args' : [{'visible' : [True, True, True,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False]}]},
        {'method' : 'update', 'label' : 'Minder dan 12 uur',
        'args' : [{'visible' : [False, False, False,
                                True, True, True,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False]}]},
        {'method' : 'update', 'label' : 'Tussen de 12 en 20 uur',
        'args' : [{'visible' : [False, False, False,
                                False, False, False,
                                True, True, True,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False]}]},
        {'method' : 'update', 'label' : 'Tussen de 20 en 35 uur',
        'args' : [{'visible' : [False, False, False,
                                False, False, False,
                                False, False, False,
                                True, True, True,
                                False, False, False,
                                False, False, False,
                                False, False, False]}]},
        {'method' : 'update', 'label' : 'Meer dan 35 uur',
        'args' : [{'visible' : [False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                True, True, True,
                                False, False, False,
                                False, False, False]}]},
        {'method' : 'update', 'label' : 'Betaald werk',
        'args' : [{'visible' : [False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                True, True, True,
                                False, False, False]}]},
        {'method' : 'update', 'label' : 'Niet betaald werk',
        'args' : [{'visible' : [False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                False, False, False,
                                True, True, True]}]}
    ]}
]


# In[25]:


#Code voor de barplot
fig3 = go.Figure()
for werkgroep in ['Totaal', 'Minder dan 12', 'Tussen 12 en 20', 'Tussen 20 en 35', 'Meer dan 35', 'Betaald', 'Niet betaald']:
    if selectbox == 'Score geluk':
        df = df3[df3['KenmerkenWerk'] == werkgroep][['Perioden', 'Ongelukkig_2', 'NietGelukkigNietOngelukkig_3', 'Gelukkig_4']]
        fig3.add_trace(go.Bar(name = 'Ongelukkig',
                     x = df['Perioden'],
                     y = df['Ongelukkig_2'],
                     offsetgroup = 0,
                     marker_color = 'red'))
        fig3.add_trace(go.Bar(name = 'Niet ongelukkig niet gelukkig',
                     x = df['Perioden'],
                     y = df['NietGelukkigNietOngelukkig_3'],
                     offsetgroup = 0,
                     base = df['Ongelukkig_2'],
                     marker_color = 'green'))
        fig3.add_trace(go.Bar(name = 'Gelukkig',
                     x = df['Perioden'],
                     y = df['Gelukkig_4'],
                     offsetgroup = 0,
                     base = df['NietGelukkigNietOngelukkig_3'] + df['Ongelukkig_2'],
                     marker_color = 'aqua'))
    elif selectbox == 'Tevredenheid met het leven':
        df = df3[df3['KenmerkenWerk'] == werkgroep][['Perioden', 'Ontevreden_6', 'NietTevredenNietOntevreden_7', 'Tevreden_8']]
        fig3.add_trace(go.Bar(name = 'Ontevreden',
                     x = df['Perioden'],
                     y = df['Ontevreden_6'],
                     offsetgroup = 0,
                     marker_color = 'red'))
        fig3.add_trace(go.Bar(name = 'Niet ontevreden niet tevreden',
                     x = df['Perioden'],
                     y = df['NietTevredenNietOntevreden_7'],
                     offsetgroup = 0,
                     base = df['Ontevreden_6'],
                     marker_color = 'green'))
        fig3.add_trace(go.Bar(name = 'Tevreden',
                     x = df['Perioden'],
                     y = df['Tevreden_8'],
                     offsetgroup = 0,
                     base = df['NietTevredenNietOntevreden_7'] + df['Ontevreden_6'],
                     marker_color = 'aqua'))
    elif selectbox == 'Tevredenheid opleidingskansen':
        df = df3[df3['KenmerkenWerk'] == werkgroep][['Perioden', 'Ontevreden_10', 'NietTevredenNietOntevreden_11', 'Tevreden_12']]
        fig3.add_trace(go.Bar(name = 'Ontevreden',
                     x = df['Perioden'],
                     y = df['Ontevreden_10'],
                     offsetgroup = 0,
                     marker_color = 'red'))
        fig3.add_trace(go.Bar(name = 'Niet ontevreden niet tevreden',
                     x = df['Perioden'],
                     y = df['NietTevredenNietOntevreden_11'],
                     offsetgroup = 0,
                     base = df['Ontevreden_10'],
                     marker_color = 'green'))
        fig3.add_trace(go.Bar(name = 'Tevreden',
                     x = df['Perioden'],
                     y = df['Tevreden_12'],
                     offsetgroup = 0,
                     base = df['NietTevredenNietOntevreden_11'] + df['Ontevreden_10'],
                     marker_color = 'aqua'))
    elif selectbox == 'Tevredenheid werk':
        df = df3[df3['KenmerkenWerk'] == werkgroep][['Perioden', 'Ontevreden_14', 'NietTevredenNietOntevreden_15', 'Tevreden_16']]
        fig3.add_trace(go.Bar(name = 'Ontevreden',
                     x = df['Perioden'],
                     y = df['Ontevreden_14'],
                     offsetgroup = 0,
                     marker_color = 'red'))
        fig3.add_trace(go.Bar(name = 'Niet ontevreden niet tevreden',
                     x = df['Perioden'],
                     y = df['NietTevredenNietOntevreden_15'],
                     offsetgroup = 0,
                     base = df['Ontevreden_14'],
                     marker_color = 'green'))
        fig3.add_trace(go.Bar(name = 'Tevreden',
                     x = df['Perioden'],
                     y = df['Tevreden_16'],
                     offsetgroup = 0,
                     base = df['NietTevredenNietOntevreden_15'] + df['Ontevreden_14'],
                     marker_color = 'aqua'))
    elif selectbox == 'Tevredenheid met reistijd':
        df = df3[df3['KenmerkenWerk'] == werkgroep][['Perioden', 'Ontevreden_18', 'NietTevredenNietOntevreden_19', 'Tevreden_20']]
        fig3.add_trace(go.Bar(name = 'Ontevreden',
                     x = df['Perioden'],
                     y = df['Ontevreden_18'],
                     offsetgroup = 0,
                     marker_color = 'red'))
        fig3.add_trace(go.Bar(name = 'Niet ontevreden niet tevreden',
                     x = df['Perioden'],
                     y = df['NietTevredenNietOntevreden_19'],
                     offsetgroup = 0,
                     base = df['Ontevreden_18'],
                     marker_color = 'green'))
        fig3.add_trace(go.Bar(name = 'Tevreden',
                     x = df['Perioden'],
                     y = df['Tevreden_20'],
                     offsetgroup = 0,
                     base = df['NietTevredenNietOntevreden_19'] + df['Ontevreden_18'],
                     marker_color = 'aqua'))
    else:
        df = df3[df3['KenmerkenWerk'] == werkgroep][['Perioden', 'Ontevreden_22', 'NietTevredenNietOntevreden_23', 'Tevreden_24']]
        fig3.add_trace(go.Bar(name = 'Ontevreden',
                     x = df['Perioden'],
                     y = df['Ontevreden_22'],
                     offsetgroup = 0,
                     marker_color = 'red'))
        fig3.add_trace(go.Bar(name = 'Niet ontevreden niet tevreden',
                     x = df['Perioden'],
                     y = df['NietTevredenNietOntevreden_23'],
                     offsetgroup = 0,
                     base = df['Ontevreden_22'],
                     marker_color = 'green'))
        fig3.add_trace(go.Bar(name = 'Tevreden',
                     x = df['Perioden'],
                     y = df['Tevreden_24'],
                     offsetgroup = 0,
                     base = df['NietTevredenNietOntevreden_23'] + df['Ontevreden_22'],
                     marker_color = 'aqua'))

        
fig3.update_layout({'sliders' : sliders2},
                  xaxis_title = 'Jaren',
                  yaxis_title = 'Percentage per tevredenheidscategorie')

if checkbox2:
    st.plotly_chart(fig3)


# In[26]:


st.write('In de volgende grafiek is een staafdiagram te zien van de scores van de verschillende categorieën. De scores zijn verdeeld in drie groepen: mensen die een score hebben gegeven van 1 tot en met 4 vallen in de groep ‘ongelukkig’/’ontevreden’. Mensen die een score hebben gegeven van 5 of 6 vallen in de groep ‘niet gelukkig en niet ongelukkig’/’niet ontevreden en niet tevreden’. Mensen die een score hebben gegeven van 7 tot en met 10 vallen in de groep ‘gelukkig’/’tevreden’. In de figuur hieronder is de verhouding van deze groepen per categorie te zien.')


# In[27]:


st.write('Uit de bargrafiek kunnen we concluderen dat er geen grote verandering heeft plaatsgevonden in de verdeling van gelukkige en ongelukkige mensen. Mensen die niet betaald werken hebben gedurende jaren een lagere score qua geluk dan alle andere categorieën. Daarnaast is zichtbaar dat des te meer uren een persoon werkt, de gemiddelde tevredenheid over werk toeneemt. Bij reistijd is juist te zien dat des te meer een persoon werkt de tevredenheid afneemt. Bij dagelijkse bezigheden is te bij alle groepen een daling te zien in 2020 en 2021, ook dit zou door de coronacrisis veroorzaakt kunnen zijn. ')


# In[7]:


df3

