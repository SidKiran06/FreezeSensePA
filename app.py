import io
import base64
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
.fs-logo{width:43px;height:43px;object-fit:contain;flex-shrink:0;}
.fs-brand .fs-title{display:flex;align-items:center;gap:10px;}
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
.stat-card{height:100%;display:flex;flex-direction:column;justify-content:space-between;background:linear-gradient(125deg,#153e60,#2877a7);border:1px solid #397da9;border-radius:16px;padding:23px 25px;min-height:190px;color:white;box-shadow:0 6px 18px rgba(18,47,75,.1);box-sizing:border-box;}
.stat-card.blue,.stat-card.purple,.stat-card.teal{background:linear-gradient(125deg,#153e60,#2877a7);}
.stat-card .stat-label{font-size:clamp(.93rem,1.08vw,1.12rem);font-weight:700;color:#d5ebf9;}
.stat-card .stat-value{font-size:clamp(2.5rem,3.5vw,4.1rem);font-weight:800;letter-spacing:-.05em;line-height:1.2;margin:10px 0;}
.stat-card .stat-detail{font-size:clamp(.88rem,1vw,1rem);line-height:1.45;color:#e1f1fb;}
.section-title{font-size:clamp(1.5rem,2vw,2.1rem);font-weight:800;color:#153e60;margin:20px 0 14px;}
.feature-card{height:100%;display:flex;flex-direction:column;background:#fff;border:1px solid #c9deeb;border-top:5px solid #3179a7;border-radius:14px;padding:22px;min-height:195px;box-sizing:border-box;box-shadow:0 5px 15px rgba(25,60,90,.055);}
.feature-card .feature-icon{font-size:2rem;line-height:1.3;}
.feature-card .feature-name{font-size:1.3rem;font-weight:800;margin:11px 0 8px;color:#153e60;}
.feature-card .feature-desc{font-size:1rem;color:#4d697d;line-height:1.55;flex:1;}
.action-panel{background:#dcecf7;border:1px solid #b6d5e8;border-radius:14px;padding:20px 24px;margin:18px 0;font-size:1.06rem;color:#194661;}
.notice{background:#f1f6fa;border-left:5px solid #377fae;padding:13px 17px;border-radius:9px;margin:15px 0;font-size:.94rem;color:#23475f;}
/* Normalize Streamlit columns and the card wrappers to identical row heights. */
[data-testid="stHorizontalBlock"]{align-items:stretch!important;}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]{display:flex;flex-direction:column;min-width:0;}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"]{height:100%;}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has(.stat-card),
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has(.feature-card){height:100%;}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has(.stat-card) > div,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has(.feature-card) > div{height:100%;}
.fact-panel{background:linear-gradient(115deg,#123c5c,#246a94);color:#fff;border-radius:15px;padding:22px 26px;min-height:165px;}
.fact-panel .eyebrow{color:#bfe5fa;font-weight:800;letter-spacing:.07em;font-size:.83rem;}
.fact-panel .fact-title{font-size:clamp(1.15rem,1.6vw,1.55rem);font-weight:800;margin:8px 0;}
.fact-panel .fact-body{color:#e2f3fd;font-size:1.04rem;line-height:1.55;}
.home-interact{background:#fff;border:1px solid #c9deeb;border-radius:14px;padding:16px 20px;margin:15px 0 8px;}
@media(max-width:850px){.fs-brand{flex-direction:column;align-items:flex-start;gap:2px}.stTabs [data-baseweb="tab-list"]{min-height:64px!important}.stTabs [data-baseweb="tab"]{padding:11px 12px!important}}
@media(max-width:650px){[data-testid="stMainBlockContainer"],.main .block-container,.block-container{padding:.4rem .55rem 1.5rem!important}.stat-card{min-height:160px;padding:18px}.feature-card{min-height:145px;padding:17px}}

/* Equal-height homepage cards: one CSS grid, not independently sized Streamlit columns. */
.fs-stats-grid,.fs-features-grid{display:grid;align-items:stretch;gap:18px;width:100%;}
.fs-stats-grid{grid-template-columns:repeat(3,minmax(0,1fr));}
.fs-features-grid{grid-template-columns:repeat(4,minmax(0,1fr));}
.fs-stats-grid>.stat-card,.fs-features-grid>.feature-card{height:100%;min-width:0;margin:0;}
.fs-stats-grid>.stat-card{min-height:208px;border:2px solid #6aa7ce;box-shadow:0 6px 18px rgba(16,47,77,.13);}
.fs-features-grid>.feature-card{min-height:205px;border:2px solid #91bdd9;border-top:6px solid #2e79aa;box-shadow:0 6px 18px rgba(16,47,77,.09);}
/* Consistent borders for panels, charts, controls, and expandable content on every tab. */
.stTabs [data-testid="stVerticalBlockBorderWrapper"]:has(>div[data-testid="stVerticalBlock"]),
.stTabs [data-testid="stForm"],
.stTabs [data-testid="stExpander"],
.stTabs [data-testid="stPlotlyChart"],
.stTabs [data-testid="stDataFrame"],
.stTabs [data-testid="stMetric"]{border:1.5px solid #9dc4de!important;border-radius:12px!important;box-shadow:0 2px 9px rgba(16,47,77,.06);}
.stTabs [data-testid="stMetric"]{background:#fff;padding:15px 18px;min-height:110px;}
.stTabs [data-testid="stPlotlyChart"],.stTabs [data-testid="stDataFrame"]{background:#fff;overflow:hidden;}
.stTabs [data-testid="stForm"]{background:#f8fbfe;padding:18px!important;}
.stTabs [data-testid="stExpander"]{background:#fff;overflow:hidden;}
.stTabs [data-testid="stAlert"]{border:1.5px solid #9dc4de;border-radius:11px;}
.stTabs [data-testid="stWidgetLabel"]{font-weight:600;color:#163e5d;}
.action-panel,.notice,.fact-panel,.home-interact{border:2px solid #8bb9d7;box-shadow:0 4px 12px rgba(16,47,77,.08);}
@media(max-width:1050px){.fs-features-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media(max-width:700px){.fs-stats-grid,.fs-features-grid{grid-template-columns:1fr;}.fs-stats-grid>.stat-card,.fs-features-grid>.feature-card{min-height:0;}}
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

FREEZESENSE_LOGO = "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"
st.markdown(f'<div class="fs-brand"><div class="fs-title"><img class="fs-logo" src="data:image/png;base64,{FREEZESENSE_LOGO}" alt="FreezeSense house and snowflake logo"><strong>FreezeSense</strong></div><span>Protecting Homes, One Winter at a Time.</span></div>',unsafe_allow_html=True)
tabs=st.tabs(['🏠 Home','🌡️ Freeze Risk','📦 Safety Kits','✅ Safety Check','📈 Impact Dashboard','📝 Activity Tracker','🗓️ Roadmap'])

with tabs[0]:
    st.markdown('<div class="hero-intro"><h1>Protecting homes, one winter at a time.</h1><p>Helping Pennsylvania households prepare for freezing temperatures through practical supplies, education, and community action.</p></div>',unsafe_allow_html=True)
    stats=[
        ('blue','PA INSURER CLAIMS','$17.4M','State Farm frozen-pipe and water-damage claims reported for 2024–June 2025; not all PA insurers.'),
        ('purple','AVERAGE U.S. CLAIM','$15,400','Average water-damage and freezing homeowners claim, 2019–2023 (Triple-I).'),
        ('teal','INITIAL SERVICE TARGET','20 homes','Proposed first-phase kit goal — not completed deliveries.')
    ]
    stats_html=''.join(f'<div class="stat-card {tone}"><div class="stat-label">{label}</div><div class="stat-value">{value}</div><div class="stat-detail">{detail}</div></div>' for tone,label,value,detail in stats)
    st.markdown(f'<div class="fs-stats-grid">{stats_html}</div>',unsafe_allow_html=True)
    st.caption('Source figures from mentor plan: BCTV / State Farm (Jan 2026); Insurance Information Institute (2019–2023). Verify original sources before public claims.')
    st.markdown('<div class="section-title">One initiative. Four ways to help.</div>',unsafe_allow_html=True)
    cards=[
        ('📦','Protect','Plan affordable winter-prevention kits with supplies and simple instructions.'),
        ('🌡️','Inform','Explore outdoor freeze scenarios and find practical preparation guidance.'),
        ('📣','Remind','Plan partner-approved cold-weather outreach before severe winter nights.'),
        ('📈','Measure','Track kits, activities, volunteer hours and anonymous survey outcomes.')
    ]
    features_html=''.join(f'<div class="feature-card"><div class="feature-icon">{ico}</div><div class="feature-name">{title}</div><div class="feature-desc">{desc}</div></div>' for ico,title,desc in cards)
    st.markdown(f'<div class="fs-features-grid">{features_html}</div>',unsafe_allow_html=True)
    st.markdown('<div class="action-panel"><b>Our proposed approach:</b> Begin with 20 prevention kits, seek donated supplies, publish the FreezeSense website, coordinate awareness reminders, and measure household preparedness. <b>Target audience:</b> older adults and households with limited resources.</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Did you know? Test your winter knowledge</div>',unsafe_allow_html=True)
    fact_left, fact_right = st.columns([1.15, 1], gap='large')
    with fact_left:
        st.markdown('''<div class="fact-panel"><div class="eyebrow">FREEZESENSE • WINTER FACT</div><div class="fact-title">A pipe can freeze without bursting immediately.</div><div class="fact-body">Ice may block the flow of water. Damage can become apparent later as the pipe thaws and water starts leaking. Know where the main shutoff valve is before an emergency.</div></div>''' , unsafe_allow_html=True)
    with fact_right:
        st.markdown('**Quick question: What should you do if you suspect a frozen pipe?**')
        answer = st.radio('Choose your answer', ['Select an answer', 'Use an open flame to thaw it quickly', 'Shut off water if needed and seek safe thawing guidance', 'Ignore it until spring'], key='fact_answer', label_visibility='collapsed')
        if answer == 'Shut off water if needed and seek safe thawing guidance':
            st.success('Correct! Avoid flames or other unsafe heating methods. Contact a qualified plumber if needed.')
        elif answer != 'Select an answer':
            st.warning('Not quite. Avoid open flames and act promptly if you suspect a freeze or leak.')
    with st.expander('Explore 3 more frozen-pipe facts'):
        st.markdown('''**1.** Pipes in unheated spaces such as garages, crawl spaces and exterior walls can be especially vulnerable.

**2.** A thermostat set above freezing does not guarantee every pipe stays warm; pipe location and insulation matter.

**3.** Outdoor temperature alone cannot predict whether a particular home’s pipes will freeze.''' )
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
