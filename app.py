import io
from datetime import date
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='FreezeSense | Community Winter Safety', page_icon='❄️', layout='wide', initial_sidebar_state='collapsed')
st.markdown("""<style>
/* Make the actual Streamlit content container span the entire browser. */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"] {max-width:100% !important;}
.stApp {background:#f4f8fc;color:#17334c;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;}
[data-testid="stMain"] {width:100% !important; flex:1 1 100% !important;}
[data-testid="stMainBlockContainer"], .main .block-container, .block-container {
  box-sizing:border-box !important; max-width:none !important;
  width:calc(100vw - 32px) !important;
  margin-left:16px !important;margin-right:16px !important;
  padding:0.35rem 0 2rem !important;
}
/* Prevent an internal element from forcing narrow columns. */
[data-testid="stMainBlockContainer"] > div {max-width:none !important;width:100% !important;}
[data-testid="stSidebar"] {display:none;}
[data-testid="stHeader"] {height:2.25rem;background:transparent;}
[data-testid="stDecoration"] {display:none;}
/* Header and tabs are one compact, edge-to-edge dark-blue navigation block. */
.brand-strip {
 display:flex;align-items:center;justify-content:space-between;gap:14px;
 box-sizing:border-box;width:100%;height:51px;min-height:51px;
 padding:7px 20px;margin:0 !important;
 background:#102d4a;color:white;border-radius:10px 10px 0 0;
}
.brand-name {font-size:1.55rem;font-weight:800;letter-spacing:-.035em;line-height:1;white-space:nowrap;color:#fff;}
.brand-tagline {font-size:.93rem;font-weight:500;color:#e5f4ff;white-space:nowrap;}
/* Streamlit inserts vertical gap between successive blocks; close it for the nav. */
[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .brand-strip) {gap:0 !important;}
[data-testid="stElementContainer"]:has(.brand-strip) {margin-bottom:0 !important;}
.stTabs {width:100% !important;}
.stTabs [data-baseweb="tab-list"] {
 box-sizing:border-box;display:flex !important;flex-wrap:nowrap !important;
 width:100% !important;gap:5px !important;overflow-x:auto !important;
 background:#102d4a !important;padding:4px 12px 10px !important;
 border-radius:0 0 10px 10px !important;scrollbar-width:thin;
}
.stTabs [data-baseweb="tab"] {
 flex:1 1 0 !important;min-width:max-content !important;
 justify-content:center !important;white-space:nowrap !important;
 border-radius:7px !important;padding:12px 10px !important;
 background:transparent !important;border:1px solid transparent !important;
 color:#fff !important;font-size:1.06rem !important;font-weight:750 !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {color:#fff !important;font-size:1.06rem !important;font-weight:750 !important;}
.stTabs [data-baseweb="tab"]:hover {background:#285778 !important;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
 background:#257fb2 !important;color:white !important;
 border-color:#74c7f1 !important;box-shadow:inset 0 -3px 0 #b7e9ff;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none !important;}
.stTabs [data-baseweb="tab-panel"] {padding-top:1rem !important;}
.notice {background:#fff1d9;border-left:5px solid #c57b1a;padding:13px 16px;border-radius:9px;margin:12px 0;}
h1,h2,h3,p,button,input {font-family:inherit;}
@media(max-width:900px) {
 [data-testid="stMainBlockContainer"], .main .block-container,.block-container {
  width:calc(100vw - 16px) !important;margin-left:8px !important;margin-right:8px !important;
 }
 .brand-strip {height:46px;min-height:46px;padding:7px 12px;}
 .brand-name {font-size:1.2rem;}
 .brand-tagline {font-size:.76rem;white-space:normal;text-align:right;}
 .stTabs [data-baseweb="tab"] {flex:0 0 auto !important;padding:10px 12px !important;}
 .stTabs [data-baseweb="tab"] p,.stTabs [data-baseweb="tab"] span {font-size:.93rem !important;}
}
</style>""",unsafe_allow_html=True)

LOG_COLS=['Date','Activity','Households reached','Kits delivered','Volunteer hours','Notes']
SURVEY_COLS=['Date','Stage','Knows shutoff','Knows prevention steps']
if 'log' not in st.session_state: st.session_state.log=pd.DataFrame(columns=LOG_COLS)
if 'surveys' not in st.session_state: st.session_state.surveys=pd.DataFrame(columns=SURVEY_COLS)
if 'checklist' not in st.session_state: st.session_state.checklist={}

def banner():
    st.markdown('<div class="notice"><b>PROPOSAL / DEMONSTRATION</b> — Sample dashboard values are fictional and clearly marked. Entries you record are session-only unless you export them. No donations, partners, kits or outcomes are claimed as completed.</div>',unsafe_allow_html=True)

def downloadable(df,filename,label):
    st.download_button(label,df.to_csv(index=False).encode('utf-8'),filename,mime='text/csv',use_container_width=True)

def plot_progress(df,target=20):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df['Period'],y=df['Cumulative kits'],mode='lines+markers+text',text=df['Cumulative kits'].astype(str)+' kits',textposition='top center',line=dict(color='#1677a8',width=5,shape='spline'),marker=dict(size=17,color='#f3a340',line=dict(color='white',width=3)),hovertemplate='<b>%{x}</b><br>%{y} kits cumulatively<extra></extra>',name='Kits delivered'))
    fig.add_hline(y=target,line_dash='dash',line_color='#7d92a2',annotation_text=f'Initial goal: {target} kits',annotation_position='bottom right')
    fig.update_layout(height=365,margin=dict(l=12,r=12,t=45,b=10),plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',showlegend=False,xaxis=dict(title='',showgrid=False),yaxis=dict(title='Cumulative kits',rangemode='tozero',gridcolor='#dce7ef'),font=dict(color='#244761'))
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})

st.markdown('<div class="brand-strip"><span class="brand-name">❄️ FreezeSense</span><span class="brand-tagline">Protecting Homes, One Winter at a Time.</span></div>',unsafe_allow_html=True)
tabs=st.tabs(['🏠 Home','🌡️ Freeze Risk','📦 Safety Kits','✅ Safety Check','📈 Impact Dashboard','📝 Activity Tracker','🗓️ Roadmap'])

with tabs[0]:
    st.header('Why FreezeSense?')
    c1,c2,c3=st.columns(3)
    c1.metric('PA insurer claims reported','$17.4M',help='State Farm frozen-pipe and water-damage claims, 2024–June 2025; BCTV Jan 2026. Not statewide total across all insurers.')
    c2.metric('Average US water/freezing claim','$15,400',help='Insurance Information Institute, 2019–2023 average.')
    c3.metric('Initial proposed kit goal','20 homes')
    st.caption('Historical figures cited in mentor plan: BCTV / State Farm (Jan 2026) and Insurance Information Institute (2019–2023). Verify original source before publication.')
    st.subheader('One initiative. Four ways to help.')
    cols=st.columns(4)
    for col,(head,desc) in zip(cols,[('📦 Protect','Prepare practical prevention kits.'),('🌡️ Inform','Explore cold-weather scenarios.'),('📣 Remind','Coordinate partner-approved Freeze Watch outreach.'),('📈 Measure','Record activities and track preparedness.')]):
        with col: st.info(f'**{head}**\n\n{desc}')
    st.markdown('**Who we hope to help:** older adults and households with limited resources. All outreach, donations and distribution are proposed until partners confirm them.')
    banner()

with tabs[1]:
    st.header('🌡️ Freeze Risk Explorer')
    st.write('Interactive **outdoor temperature scenario**, not a live forecast or a prediction of indoor pipe temperatures.')
    a,b=st.columns([2,1])
    with a:
        temp=st.slider('Choose a forecast overnight low (°F)',-20,60,15)
        exposure=st.selectbox('Where are the pipes?',['Interior heated area','Exterior wall','Unheated garage / crawl space'])
        heat=st.checkbox('Indoor heat is maintained',value=True)
    with b:
        if temp<=20: st.error('🔴 **Higher concern** — take precautions now.')
        elif temp<=32: st.warning('🟠 **Freezing possible** — review vulnerable plumbing.')
        else: st.success('🟢 **Above freezing scenario** — continue routine prevention.')
        if exposure!='Interior heated area' or not heat: st.warning('Additional exposure or heating concern: consider qualified professional advice.')
    st.subheader('Your action plan')
    for step in ['Locate the main water shutoff valve','Review insulation for exposed pipes with an adult or professional','Check outdoor faucet winterization guidance','Keep indoor heat at a safe level','Follow official weather warnings']:
        st.markdown('✓ '+step)
    st.caption('20°F is a general outdoor warning threshold cited by Consumer Reports in the mentor plan, not a guarantee. Conditions vary. See [National Weather Service](https://www.weather.gov/) for current alerts.')

with tabs[2]:
    st.header('📦 Safety Kit Planner')
    st.write('Choose proposed supplies, estimate costs, and create a funding scenario. No kits or donations are claimed as completed.')
    products=[('Foam pipe insulation',7),('Outdoor faucet cover',6),('Leak detection tablets',3),('Shutoff identification tag',2),('Printed instruction card',2)]
    selected=[]
    for name,estimate in products:
        if st.checkbox(f'{name} — illustrative ${estimate}',value=True,key='item_'+name):selected.append((name,estimate))
    qty=st.number_input('Number of kits planned',min_value=1,max_value=500,value=20)
    unit=sum(p for _,p in selected)
    donation=st.number_input('Hypothetical donations or discounts ($)',min_value=0,max_value=100000,value=0,step=25)
    gross=unit*qty
    c1,c2,c3=st.columns(3)
    c1.metric('Illustrative per-kit cost',f'${unit}')
    c2.metric('Gross budget',f'${gross:,}')
    c3.metric('Funding still needed',f'${max(0,gross-donation):,}')
    st.progress(min(1,donation/gross) if gross else 0,text=f'Illustrative funding coverage: {min(100,round(100*donation/gross)) if gross else 0}%')
    st.caption('All component prices are placeholders for planning, not vendor quotes. The mentor plan proposes a $25-per-kit ceiling; this selected-item estimate may differ.')
    kitplan=pd.DataFrame([{'Item':name,'Illustrative unit cost ($)':price,'Quantity':qty,'Illustrative total ($)':price*qty} for name,price in selected])
    downloadable(kitplan,'freezesense_kit_budget.csv','⬇️ Export kit budget')
    st.warning('Students do not install plumbing or enter homes. Partners/adults handle distribution and installation decisions.')

with tabs[3]:
    st.header('✅ Household Preparedness Check')
    st.write('A private, educational self-check. Answers are not automatically collected or transmitted.')
    questions=['I know where my main water shutoff valve is.','I have identified potentially exposed pipes.','I have checked guidance for outdoor faucets.','I know where to find official weather warnings.','I have a plan for maintaining safe indoor heat.','I know whom to contact for a plumbing emergency.']
    count=0
    for i,q in enumerate(questions):
        if st.checkbox(q,key=f'check_{i}'):count+=1
    st.progress(count/len(questions),text=f'{count} of {len(questions)} steps reviewed')
    if count==len(questions):st.success('All six preparedness topics reviewed! Keep checking conditions as winter progresses.')
    elif count<=2:st.info('Start with the unchecked items. Ask a trusted adult or professional if you are unsure.')
    else:st.info('Good progress. Review the remaining unchecked items.')
    st.download_button('⬇️ Download my checklist summary',('\n'.join(('DONE' if st.session_state.get(f'check_{i}') else 'REVIEW')+' — '+q for i,q in enumerate(questions))).encode(),file_name='winter_safety_checklist.txt',mime='text/plain')
    st.caption('Checklist progress is session-based, not a verified safety inspection. Never submit names, home addresses or other private information.')

with tabs[4]:
    st.header('📈 Community Impact Journey')
    mode=st.radio('View', ['🧪 Hypothetical demonstration','📝 My recorded session'],horizontal=True)
    if mode.startswith('🧪'):
        banner()
        months=['Nov','Dec','Jan','Feb']
        demo=st.slider('Illustrative scenario: total kits by February',0,50,20,5)
        cumulative=[0,round(demo*.25),round(demo*.7),demo]
        data=pd.DataFrame({'Period':months,'Cumulative kits':cumulative})
        households=demo+round(demo*.2)
        hours=round(demo*1.5)
    else:
        st.info('These are entries recorded during this browser session only. Export your CSV to keep them; Streamlit Community Cloud does not persist these entries reliably across sessions.')
        log=st.session_state.log.copy()
        if log.empty:
            st.warning('No activities recorded yet. Open Activity Tracker to add one.')
            data=pd.DataFrame({'Period':['No entries'],'Cumulative kits':[0]})
            households=hours=0
        else:
            log['Date']=pd.to_datetime(log['Date'],errors='coerce')
            log=log.dropna(subset=['Date']).sort_values('Date')
            grouped=log.groupby(log['Date'].dt.strftime('%b %Y'),sort=False)['Kits delivered'].sum().cumsum()
            data=pd.DataFrame({'Period':grouped.index,'Cumulative kits':grouped.values})
            households=int(log['Households reached'].sum());hours=float(log['Volunteer hours'].sum())
        demo=int(data['Cumulative kits'].iloc[-1])
    a,b,c=st.columns(3)
    a.metric('Kits recorded / illustrated',f'{demo:,}')
    b.metric('Households reached',f'{households:,}')
    c.metric('Volunteer hours',f'{hours:g}')
    st.subheader('Follow the journey — each dot is a milestone')
    plot_progress(data)
    st.progress(min(demo/20,1),text=f'{demo} / 20 initial kit goal ({min(100,round(demo/20*100))}%)')
    st.caption('Hover over each large orange dot for the cumulative kit total. Dashed line = proposed initial target. Demonstration mode values are entirely hypothetical.')
    st.subheader('Preparedness survey comparison')
    if mode.startswith('🧪'):
        st.caption('HYPOTHETICAL SAMPLE percentages — not collected from real households.')
        survey=pd.DataFrame({'Question':['Know water shutoff','Know prevention steps'],'Before':[35,40],'After':[70,85]})
    else:
        raw=st.session_state.surveys
        rows=[]
        for label,col in [('Know water shutoff','Knows shutoff'),('Know prevention steps','Knows prevention steps')]:
            before=raw.loc[raw['Stage']=='Before',col];after=raw.loc[raw['Stage']=='After',col]
            rows.append({'Question':label,'Before':round(before.mean()*100) if len(before) else None,'After':round(after.mean()*100) if len(after) else None})
        survey=pd.DataFrame(rows)
    for _,r in survey.iterrows():
        st.markdown(f"**{r['Question']}**")
        l,rcol=st.columns(2)
        with l: st.metric('Before',f"{int(r['Before'])}%" if pd.notna(r['Before']) else 'No data')
        with rcol: st.metric('After',f"{int(r['After'])}%" if pd.notna(r['After']) else 'No data')
    st.caption('Survey entries are anonymous counts of responses, not proof of preventing damage. Do not treat unpaired before/after responses as individual improvements.')

with tabs[5]:
    st.header('📝 Activity & Survey Tracker')
    st.warning('SESSION-ONLY TRACKING: entries are not stored in a shared database. Download CSV before closing/reloading, or upload a previously exported CSV. Do not enter resident names, addresses, phone numbers or sensitive details.')
    activity,survey_tab,records=st.tabs(['Record an activity','Record an anonymous survey','View / export / restore'])
    with activity:
        with st.form('activity_form',clear_on_submit=True):
            d=st.date_input('Activity date',value=date.today())
            kind=st.selectbox('Activity type',['Kit distribution','Awareness event','Freeze Watch reminder','Partner outreach','Volunteer activity'])
            a,b,c=st.columns(3)
            homes=a.number_input('Households reached',min_value=0,max_value=10000,value=0)
            kits=b.number_input('Kits delivered',min_value=0,max_value=10000,value=0)
            hours=c.number_input('Volunteer hours',min_value=0.0,max_value=10000.0,value=0.0,step=.5)
            note=st.text_input('Optional general note (no personal information)',max_chars=120)
            save=st.form_submit_button('Save activity to this session',type='primary')
        if save:
            row=pd.DataFrame([[str(d),kind,int(homes),int(kits),float(hours),note]],columns=LOG_COLS)
            st.session_state.log=pd.concat([st.session_state.log,row],ignore_index=True)
            st.success('Activity added to the session. Export CSV to retain it.')
    with survey_tab:
        with st.form('survey_form',clear_on_submit=True):
            sd=st.date_input('Survey date',value=date.today(),key='survey_date')
            stage=st.radio('Survey stage',['Before','After'],horizontal=True)
            know1=st.radio('Respondent knows where the water shutoff is',['Yes','No'],horizontal=True)
            know2=st.radio('Respondent knows winter pipe prevention steps',['Yes','No'],horizontal=True)
            submit=st.form_submit_button('Record anonymous response',type='primary')
        if submit:
            row=pd.DataFrame([[str(sd),stage,know1=='Yes',know2=='Yes']],columns=SURVEY_COLS)
            st.session_state.surveys=pd.concat([st.session_state.surveys,row],ignore_index=True)
            st.success('Anonymous survey response added to this session. Export to retain it.')
    with records:
        st.subheader('Activity records')
        st.dataframe(st.session_state.log,use_container_width=True,hide_index=True)
        downloadable(st.session_state.log,'freezesense_activities.csv','⬇️ Download activity records CSV')
        st.subheader('Anonymous survey records')
        st.dataframe(st.session_state.surveys,use_container_width=True,hide_index=True)
        downloadable(st.session_state.surveys,'freezesense_surveys.csv','⬇️ Download survey records CSV')
        st.divider()
        st.subheader('Restore from exported CSV')
        typ=st.selectbox('Import type',['Activities','Surveys'])
        upload=st.file_uploader('Choose a previously exported CSV',type=['csv'],key='csv_import')
        if upload is not None and st.button('Replace session records with imported CSV'):
            try:
                incoming=pd.read_csv(upload)
                expected=LOG_COLS if typ=='Activities' else SURVEY_COLS
                if not set(expected).issubset(incoming.columns):st.error('Wrong CSV format. Required columns: '+', '.join(expected))
                else:
                    incoming=incoming[expected]
                    if typ=='Activities':
                        for col in ['Households reached','Kits delivered','Volunteer hours']:incoming[col]=pd.to_numeric(incoming[col],errors='raise').clip(lower=0)
                        st.session_state.log=incoming
                    else:
                        for col in ['Knows shutoff','Knows prevention steps']:incoming[col]=incoming[col].astype(str).str.lower().map({'true':True,'false':False})
                        if incoming[['Knows shutoff','Knows prevention steps']].isna().any().any():raise ValueError('Invalid survey response values')
                        st.session_state.surveys=incoming
                    st.success('Records restored to this session.')
            except Exception as exc:st.error(f'Could not import: {exc}')

with tabs[6]:
    st.header('🗓️ Proposed Project Roadmap')
    for month,description in [('November 2026','Verify sources, survey needs, contact prospective partners, seek donations and build website.'),('December 2026','If funding and partners are secured, assemble first kits and begin approved awareness outreach.'),('January 2027','Coordinate partner-led distribution and Freeze Watch reminders; log actual activities.'),('Early February 2027','Gather anonymous feedback, export records, evaluate outcomes and prepare competition evidence.')]:
        with st.expander(month,expanded=True):st.write(description)
    st.subheader('Potential partners — not confirmed')
    st.write('Hardware stores · Plumbers · Insurance agencies · Area Agencies on Aging · Weatherization programs')
    st.subheader('Evidence checklist for future state presentation')
    for item in ['Partner permissions or emails','Itemized donations and expenses','Kit assembly and delivery totals','Outreach activity logs','Anonymous before/after survey summaries']:
        st.markdown('☐ '+item)
    st.info('The app is an educational prototype, not an emergency warning system, plumbing inspection, or a promise that frozen pipes will be prevented.')

st.divider()
st.caption('FreezeSense | FBLA proposal | Data-entry records are temporary until exported; do not use for private household information. Historical figures require source verification.')
