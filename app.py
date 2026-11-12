import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / 'data'

def load_csv(name):
    p = DATA / name
    return pd.read_csv(p) if p.exists() else pd.DataFrame()

temp = load_csv('temp_clean.csv')
anom = load_csv('temp_anomalies.csv')
heat = load_csv('heatwave_per_year.csv')
merged = load_csv('features_merged_1975_2019.csv')
deaths = load_csv('IMD_Heat_Cold_Deaths_Cleaned.csv')

st.set_page_config(page_title='HEATWATCH | Climate Intelligence', page_icon='🌡️', layout='wide', initial_sidebar_state='expanded')
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'Manrope', sans-serif;}
.stApp {background: radial-gradient(ellipse at 85% 0%, #321c1b 0%, #111315 42%, #0a0c0e 100%); color:#f4f2ed;}
.block-container {padding-top:2.2rem; max-width:1450px;}
section[data-testid="stSidebar"] {background:#101315; border-right:1px solid #292d2e;}
.hero {padding:30px 34px; border:1px solid #373331; border-radius:22px; background:linear-gradient(120deg,rgba(239,86,55,.18),rgba(27,31,32,.92) 58%); margin-bottom:22px;}
.kicker {font:500 11px 'DM Mono'; letter-spacing:2.5px; color:#ff8062; text-transform:uppercase;}
.hero h1 {font-size:clamp(42px,6vw,76px); line-height:.98; margin:12px 0 12px; letter-spacing:-3px; color:#fff8f1;}
.hero p {color:#b9b7b1; font-size:15px; max-width:760px; margin:0;}
.metric {background:linear-gradient(145deg,#1a1e20,#111416); border:1px solid #303536; padding:19px 20px; border-radius:16px; min-height:115px;}
.metric-label {font:11px 'DM Mono'; letter-spacing:1.3px; color:#aaa9a2; text-transform:uppercase;}
.metric-value {font-size:31px; font-weight:800; color:#fff5ee; margin-top:7px;}
.metric-note {font-size:11px; color:#ff987c; margin-top:2px;}
.section-title {font-size:22px; font-weight:800; color:#f7f2eb; margin:12px 0 3px;}
.section-sub {font-size:12px; color:#aaa9a2; margin-bottom:14px;}
div[data-testid="stPlotlyChart"] {background:#141819; border:1px solid #2d3334; border-radius:16px; padding:8px;}
.stTabs [data-baseweb="tab-list"] {gap:8px; background:#121617; padding:7px; border-radius:12px;}
.stTabs [data-baseweb="tab"] {color:#b9b7b1; border-radius:8px;}
.stTabs [aria-selected="true"] {background:#e75d40 !important; color:white !important;}
div[data-testid="stAlert"] {background:#1a1d1d; border:1px solid #45413b;}
.small-note {color:#aaa9a2; font-size:11px;}
hr {border-color:#303536;}
</style>''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="kicker">NIErnaya 2026 · Phase 2</div>', unsafe_allow_html=True)
    st.markdown('## 🌡️ HEATWATCH')
    page = st.radio('NAVIGATION', ['Overview','Temperature intelligence','Extreme heat','Human impact','Data & methodology'], label_visibility='visible')
    st.divider()
    st.markdown('**DATA STATUS**')
    for label, df in [('Temperature',temp),('Monthly anomalies',anom),('Heat / cold waves',heat),('Merged features',merged),('Mortality',deaths)]:
        st.caption(('🟢 ' if not df.empty else '🔴 ') + f'{label} · {len(df):,} rows')
    st.caption('Local dashboard · supplied project datasets')

st.markdown('<div class="hero"><div class="kicker">CLIMATE INTELLIGENCE / INDIA</div><h1>HEAT<span style="color:#ff694a">WATCH.</span></h1><p>Reading the warming signal, tracking extreme-heat events, and examining human impact — from long-term climate records to actionable risk indicators.</p></div>', unsafe_allow_html=True)

# helper for dark plotly styling
def dark(fig, height=390):
    fig.update_layout(height=height, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Manrope',color='#ddd8d0',size=11), margin=dict(l=18,r=18,t=38,b=18),
        legend=dict(bgcolor='rgba(0,0,0,0)',orientation='h',y=1.12,x=0),
        xaxis=dict(gridcolor='#2b3031',zerolinecolor='#454b4b'), yaxis=dict(gridcolor='#2b3031',zerolinecolor='#454b4b'))
    return fig

def metric(label,value,note):
    st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',unsafe_allow_html=True)

if page == 'Overview':
    st.markdown('<div class="section-title">The climate signal, at a glance</div><div class="section-sub">A long-term warming record meets a shorter record of extreme events and human impact.</div>',unsafe_allow_html=True)
    cols=st.columns(4)
    with cols[0]: metric('Temperature record','125 yrs','1901–2025')
    with cols[1]: metric('Recent warming','2.5×','since 1981 vs long-run rate')
    with cols[2]: metric('Extreme-event overlap','45 yrs','1975–2019')
    with cols[3]: metric('PCA variance','62%','first three components')
    if not temp.empty:
        t=temp.copy(); t['Decade mean']=t['Year']//10*10
        annual=t[['Year','Annual']].dropna()
        fig=go.Figure(); fig.add_trace(go.Scatter(x=annual.Year,y=annual.Annual,mode='lines',name='Annual mean',line=dict(color='#ff7656',width=1.5),opacity=.65))
        fig.add_trace(go.Scatter(x=annual.Year,y=annual.Annual.rolling(10,center=True).mean(),mode='lines',name='10-year rolling mean',line=dict(color='#ffe0bd',width=3)))
        fig.add_hline(y=annual.Annual.mean(),line_dash='dot',line_color='#888888',opacity=.6)
        fig=dark(fig,390); fig.update_layout(title='Annual mean temperature · 1901–2025',yaxis_title='°C',xaxis_title='Year')
        st.plotly_chart(fig,use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        if not heat.empty:
            fig=px.bar(heat,x='Year',y='heat_wave_py',color='from_block',color_discrete_map={True:'#8a7770',False:'#f16a49'},title='Heat-wave days / annualised count')
            fig=dark(fig,330); fig.update_layout(xaxis_title='Year',yaxis_title='Heat-wave days')
            st.plotly_chart(fig,use_container_width=True)
    with c2:
        if not deaths.empty:
            d=deaths.copy()
            fig=go.Figure(); fig.add_trace(go.Bar(x=d.Period,y=d.Heat_Deaths_Per_Year,name='Heat-wave deaths / year',marker_color='#f16a49'))
            fig.add_trace(go.Bar(x=d.Period,y=d.Cold_Deaths_Per_Year,name='Cold-wave deaths / year',marker_color='#7198a3'))
            fig=dark(fig,330); fig.update_layout(barmode='group',title='Annualised deaths by reporting period',xaxis_title='Period',yaxis_title='Deaths per year')
            st.plotly_chart(fig,use_container_width=True)
    st.info('Interpretation: rising average temperatures do not automatically imply a smooth rise in annual heat-wave counts. The records have different time coverage and event definitions.')

elif page == 'Temperature intelligence':
    st.markdown('<div class="section-title">Temperature intelligence</div><div class="section-sub">Explore the annual trend, monthly anomaly structure, and decade-level changes.</div>',unsafe_allow_html=True)
    if not temp.empty:
        year_min,year_max=int(temp.Year.min()),int(temp.Year.max())
        yr=st.slider('Select year range',year_min,year_max,(year_min,year_max))
        t=temp[temp.Year.between(*yr)]
        f=go.Figure(); f.add_trace(go.Scatter(x=t.Year,y=t.Annual,mode='lines',name='Annual mean',line=dict(color='#f16a49',width=2)))
        f.add_trace(go.Scatter(x=t.Year,y=t.Annual.rolling(10,min_periods=1).mean(),mode='lines',name='Trailing 10-year mean',line=dict(color='#f4d4b3',width=3)))
        f=dark(f,420); f.update_layout(title='Annual mean temperature',xaxis_title='Year',yaxis_title='°C'); st.plotly_chart(f,use_container_width=True)
    if not anom.empty:
        months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        a=anom.set_index('Year')[months]
        a.index=a.index.astype(str)
        fig=go.Figure(go.Heatmap(z=a.values,x=months,y=a.index,colorscale=[[0,'#315c72'],[.5,'#e8dfd0'],[1,'#e95e3e']],zmid=0,colorbar=dict(title='°C')))
        fig=dark(fig,max(500,min(900,len(a)*5))); fig.update_layout(title='Monthly temperature anomalies · 1901–2025',xaxis_title='Month',yaxis_title='Year')
        st.plotly_chart(fig,use_container_width=True)
        decade=anom.copy(); decade['Decade']=decade.Year//10*10
        dm=decade.groupby('Decade')[months].mean().mean(axis=1).reset_index(name='Mean monthly anomaly')
        fig=px.bar(dm,x='Decade',y='Mean monthly anomaly',title='Average monthly anomaly by decade',color='Mean monthly anomaly',color_continuous_scale=['#4d8397','#e9dfd1','#ef6545'])
        fig=dark(fig,340); st.plotly_chart(fig,use_container_width=True)

elif page == 'Extreme heat':
    st.markdown('<div class="section-title">Extreme heat & climate patterns</div><div class="section-sub">Compare event counts with the temperature and seasonal features available in the shared 1975–2019 window.</div>',unsafe_allow_html=True)
    if not heat.empty:
        h=heat.copy(); h['Event data type']=np.where(h.from_block,'Annualised 5-year block','Single-year observation')
        fig=go.Figure(); fig.add_trace(go.Bar(x=h.Year,y=h.heat_wave_py,name='Heat-wave',marker_color='#f16a49'))
        fig.add_trace(go.Scatter(x=h.Year,y=h.cold_wave_py,name='Cold-wave',mode='lines+markers',line=dict(color='#79a9ba',width=2)))
        fig=dark(fig,400); fig.update_layout(title='Heat-wave and cold-wave series · 1975–2019',xaxis_title='Year',yaxis_title='Annualised count / days')
        st.plotly_chart(fig,use_container_width=True)
        st.caption('Grey-origin annualised block values represent five-year averages repeated across constituent years; they are not independent annual observations.')
    if not merged.empty:
        m=merged.copy()
        col1,col2=st.columns(2)
        with col1:
            fig=px.scatter(m,x='annual_anom',y='heat_wave_py',color='from_block',color_discrete_map={True:'#8a7770',False:'#f16a49'},hover_data=['Year'],trendline='ols',title='Annual anomaly vs heat-wave days')
            fig=dark(fig,380); fig.update_layout(xaxis_title='Annual temperature anomaly (°C)',yaxis_title='Heat-wave days'); st.plotly_chart(fig,use_container_width=True)
        with col2:
            corr=m[['annual_anom','summer_anom','monsoon_anom','winter_anom','heat_wave_py','cold_wave_py','seasonal_range']].corr(numeric_only=True)
            fig=px.imshow(corr,text_auto='.2f',color_continuous_scale=['#315c72','#e8dfd0','#e95e3e'],zmin=-1,zmax=1,title='Feature correlation matrix')
            fig=dark(fig,380); st.plotly_chart(fig,use_container_width=True)
        st.markdown('**Merged feature explorer**')
        st.dataframe(m, use_container_width=True, hide_index=True)

elif page == 'Human impact':
    st.markdown('<div class="section-title">Human impact</div><div class="section-sub">Explore the supplied IMD heat- and cold-wave mortality table. These are descriptive comparisons, not causal attribution.</div>',unsafe_allow_html=True)
    if not deaths.empty:
        d=deaths.copy()
        c1,c2,c3=st.columns(3)
        with c1: metric('Reporting periods',f'{len(d)}','5-year blocks + single years')
        with c2: metric('Highest heat deaths / yr',f'{d.Heat_Deaths_Per_Year.max():,.1f}',str(d.loc[d.Heat_Deaths_Per_Year.idxmax(),'Period']))
        with c3: metric('Highest cold deaths / yr',f'{d.Cold_Deaths_Per_Year.max():,.1f}',str(d.loc[d.Cold_Deaths_Per_Year.idxmax(),'Period']))
        fig=go.Figure(); fig.add_trace(go.Bar(x=d.Period,y=d.Heat_Deaths_Per_Year,name='Heat wave',marker_color='#f16a49'))
        fig.add_trace(go.Bar(x=d.Period,y=d.Cold_Deaths_Per_Year,name='Cold wave',marker_color='#7198a3'))
        fig=dark(fig,420); fig.update_layout(barmode='group',title='Deaths per year (five-year periods annualised)',xaxis_title='IMD reporting period',yaxis_title='Deaths per year')
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('**Mortality data table**'); st.dataframe(d,use_container_width=True,hide_index=True)
        st.download_button('Download cleaned mortality CSV',d.to_csv(index=False).encode(),file_name='IMD_Heat_Cold_Deaths_Cleaned.csv',mime='text/csv')
        st.warning('Important: the first five rows are five-year totals converted to annualised averages; later rows are individual years. Annualised values improve comparability but hide within-block variation. Death counts alone do not establish that temperature caused each death.')
    else: st.warning('Mortality dataset not found in data folder.')

elif page == 'Data & methodology':
    st.markdown('<div class="section-title">Data & methodology</div><div class="section-sub">What is included, how to interpret it, and where the analytical limitations remain.</div>',unsafe_allow_html=True)
    inventory=pd.DataFrame([{'Dataset':'Monthly temperature','File':'temp_clean.csv','Coverage':'1901–2025','Rows':len(temp),'Use':'Monthly and annual mean temperatures'}, {'Dataset':'Monthly anomalies','File':'temp_anomalies.csv','Coverage':'1901–2025','Rows':len(anom),'Use':'Monthly anomalies vs 1991–2020 normal'}, {'Dataset':'Heat / cold waves','File':'heatwave_per_year.csv','Coverage':'1975–2019','Rows':len(heat),'Use':'Event counts; block values flagged'}, {'Dataset':'Merged features','File':'features_merged_1975_2019.csv','Coverage':'1975–2019','Rows':len(merged),'Use':'Seasonal features, logs, heat risk index'}, {'Dataset':'Mortality','File':'IMD_Heat_Cold_Deaths_Cleaned.csv','Coverage':'1975–2019','Rows':len(deaths),'Use':'Heat- and cold-wave deaths by period'}])
    st.dataframe(inventory,use_container_width=True,hide_index=True)
    st.markdown('### Analytical notes')
    st.markdown('''- Temperature record: monthly and annual values span 1901–2025; anomalies are referenced to the 1991–2020 normal.
- Extreme-event record: 1975–2019, giving 45 overlapping years with the temperature record.
- Five-year block counts are annualised and flagged. Repeated annualised values must not be mistaken for independently observed single-year counts.
- Heat-wave counts are right-skewed; log-transformed features are included in the merged dataset.
- The proposed Heat Risk Index is a composite indicator. Equal weighting is a modelling assumption and should be tested with sensitivity analysis.
- Correlation is descriptive, not causal. Health outcomes also depend on exposure, vulnerability, adaptation, healthcare access, and reporting quality.''')
    st.markdown('### Data preview')
    chosen=st.selectbox('Choose dataset',['temp_clean.csv','temp_anomalies.csv','heatwave_per_year.csv','features_merged_1975_2019.csv','IMD_Heat_Cold_Deaths_Cleaned.csv'])
    st.dataframe(load_csv(chosen),use_container_width=True,hide_index=True)

st.divider()
st.markdown('<div class="small-note">HEATWATCH · NIErnaya 2026 · Climate intelligence prototype · Built with Streamlit + Plotly · For research and educational use</div>',unsafe_allow_html=True)
