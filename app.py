import io
from datetime import date
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='FreezeSense | Community Winter Safety', page_icon='❄️', layout='wide', initial_sidebar_state='collapsed')
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {--navy:#102f4d;--deep:#153e60;--blue:#246d9d;--pale:#e9f3fa;--ink:#15354e;}
.stApp {background:#edf4f9;color:var(--ink);font-family:Inter,system-ui,sans-serif;}
[data-testid="stMainBlockContainer"],.main .block-container,.block-container {width:100%!important;max-width:100%!important;box-sizing:border-box!important;padding:.5rem 1.2rem 2rem!important;margin:0 auto!important;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stHeader"]{height:1.8rem;background:transparent;}
[data-testid="stDecoration"]{display:none;}
/* Keep actual Streamlit tabs, without pseudo-elements over the click targets. */
.fs-brand {background:linear-gradient(110deg,#102f4d,#225e89);color:#fff;border-radius:13px 13px 0 0;padding:12px 22px 10px;margin:0;display:flex;align-items:center;justify-content:space-between;gap:18px;}
.fs-brand strong {font-size:clamp(1.3rem,1.9vw,1.85rem);font-weight:800;letter-spacing:-.035em;}
.fs-brand span {font-size:clamp(.83rem,1vw,1rem);color:#dceefa;}
.stTabs [data-baseweb="tab-list"] {background:#153e60!important;display:flex!important;gap:6px!important;width:100%!important;min-height:69px!important;padding:9px 12px!important;border-radius:0 0 13px 13px!important;overflow-x:auto!important;scrollbar-width:thin;box-sizing:border-box!important;}
.stTabs [data-baseweb="tab"] {flex:1 0 auto!important;min-width:max-content!important;padding:13px 15px!important;background:#205276!important;border:1px solid #396d90!important;border-radius:9px!important;color:#fff!important;cursor:pointer!important;position:relative!important;z-index:2!important;}
.stTabs [data-baseweb="tab"] p,.stTabs [data-baseweb="tab"] span {font-family:Inter,system-ui,sans-serif!important;color:#fff!important;font-size:clamp(1rem,1.2vw,1.17rem)!important;font-weight:700!important;white-space:nowrap!important;}
.stTabs [data-baseweb="tab"]:hover {background:#3276a4!important;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {background:#3986b8!important;border-color:#a8daf7!important;box-shadow:inset 0 -4px 0 #d0edff!important;}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:1rem!important;}
.hero-intro{padding:13px 3px 16px;}
.hero-intro h1{font-size:clamp(2rem,3vw,3.15rem);color:#123858;line-height:1.13;margin:0 0 7px;font-weight:800;}
.hero-intro p{font-size:clamp(1rem,1.25vw,1.22rem);color:#4e6a80;margin:0;}
.stat-card{background:linear-gradient(125deg,#153e60,#2877a7);border:1px solid #397da9;border-radius:16px;padding:23px 25px;min-height:190px;color:white;box-shadow:0 6px 18px rgba(18,47,75,.1);box-sizing:border-box;}
.stat-card.blue,.stat-card.purple,.stat-card.teal{background:linear-gradient(125deg,#153e60,#2877a7);}
.stat-card .stat-label{font-size:clamp(.93rem,1.08vw,1.12rem);font-weight:700;color:#d5ebf9;}
.stat-card .stat-value{font-size:clamp(2.5rem,3.5vw,4.1rem);font-weight:800;letter-spacing:-.05em;line-height:1.2;margin:10px 0;}
.stat-card .stat-detail{font-size:clamp(.88rem,1vw,1rem);line-height:1.45;color:#e1f1fb;}
.section-title{font-size:clamp(1.5rem,2vw,2.1rem);font-weight:800;color:#153e60;margin:20px 0 14px;}
.feature-card{background:#fff;border:1px solid #c9deeb;border-top:5px solid #3179a7;border-radius:14px;padding:22px;min-height:195px;box-sizing:border-box;box-shadow:0 5px 15px rgba(25,60,90,.055);}
.feature-card .feature-icon{font-size:2rem;line-height:1.3;}
.feature-card .feature-name{font-size:1.3rem;font-weight:800;margin:11px 0 8px;color:#153e60;}
.feature-card .feature-desc{font-size:1rem;color:#4d697d;line-height:1.55;}
.action-panel{background:#dcecf7;border:1px solid #b6d5e8;border-radius:14px;padding:20px 24px;margin:18px 0;font-size:1.06rem;color:#194661;}
.notice{background:#f1f6fa;border-left:5px solid #377fae;padding:13px 17px;border-radius:9px;margin:15px 0;font-size:.94rem;color:#23475f;}
.home-interact{background:#fff;border:1px solid #c9deeb;border-radius:14px;padding:16px 20px;margin:15px 0 8px;}
@media(max-width:850px){.fs-brand{flex-direction:column;align-items:flex-start;gap:2px}.stTabs [data-baseweb="tab-list"]{min-height:64px!important}.stTabs [data-baseweb="tab"]{padding:11px 12px!important}}
@media(max-width:650px){[data-testid="stMainBlockContainer"],.main .block-container,.block-container{padding:.4rem .55rem 1.5rem!important}.stat-card{min-height:160px;padding:18px}.feature-card{min-height:145px;padding:17px}}
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

st.markdown('<div class="fs-brand"><strong>❄ FreezeSense</strong><span>Protecting Homes, One Winter at a Time.</span></div>',unsafe_allow_html=True)
tabs=st.tabs(['🏠 Home','🌡️ Freeze Risk','📦 Safety Kits','✅ Safety Check','📈 Impact Dashboard','📝 Activity Tracker','🗓️ Roadmap'])

with tabs[0]:
    st.markdown('<div class="hero-intro"><h1>Protecting homes, one winter at a time.</h1><p>Helping Pennsylvania households prepare for freezing temperatures through practical supplies, education, and community action.</p></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3,gap='large')
    stats=[
        ('blue','PA INSURER CLAIMS','$17.4M','State Farm frozen-pipe and water-damage claims reported for 2024–June 2025; not all PA insurers.'),
        ('purple','AVERAGE U.S. CLAIM','$15,400','Average water-damage and freezing homeowners claim, 2019–2023 (Triple-I).'),
        ('teal','INITIAL SERVICE TARGET','20 homes','Proposed first-phase kit goal — not completed deliveries.')
    ]
    for col,(tone,label,value,detail) in zip([c1,c2,c3],stats):
        with col:
            st.markdown(f'<div class="stat-card {tone}"><div class="stat-label">{label}</div><div class="stat-value">{value}</div><div class="stat-detail">{detail}</div></div>',unsafe_allow_html=True)
    st.caption('Source figures from mentor plan: BCTV / State Farm (Jan 2026); Insurance Information Institute (2019–2023). Verify original sources before public claims.')
    st.markdown('<div class="section-title">One initiative. Four ways to help.</div>',unsafe_allow_html=True)
    cards=[
        ('📦','Protect','Plan affordable winter-prevention kits with supplies and simple instructions.'),
        ('🌡️','Inform','Explore outdoor freeze scenarios and find practical preparation guidance.'),
        ('📣','Remind','Plan partner-approved cold-weather outreach before severe winter nights.'),
        ('📈','Measure','Track kits, activities, volunteer hours and anonymous survey outcomes.')
    ]
    cols=st.columns(4,gap='large')
    for col,(ico,title,desc) in zip(cols,cards):
        with col:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{ico}</div><div class="feature-name">{title}</div><div class="feature-desc">{desc}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="action-panel"><b>Our proposed approach:</b> Begin with 20 prevention kits, seek donated supplies, publish the FreezeSense website, coordinate awareness reminders, and measure household preparedness. <b>Target audience:</b> older adults and households with limited resources.</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">❄ Quick winter readiness check</div>',unsafe_allow_html=True)
    st.caption('Interactive demonstration: explore basic household preparedness. No personal information is collected.')
    q1,q2,q3=st.columns(3)
    with q1: h_shutoff=st.checkbox('I know where the main water shutoff is',key='home_shutoff')
    with q2: h_pipes=st.checkbox('I have checked exposed pipes',key='home_pipes')
    with q3: h_plan=st.checkbox('I have a cold-weather preparation plan',key='home_plan')
    readiness=sum([h_shutoff,h_pipes,h_plan])
    st.progress(readiness/3,text=f'{readiness} of 3 preparation steps checked')
    if readiness==3: st.success('All three basic preparation steps checked. Continue reviewing official winter safety guidance.')
    elif readiness: st.info('Good start — check the remaining items to improve your preparedness.')
    else: st.info('Start by locating your main water shutoff valve and reviewing exposed pipes.')
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
