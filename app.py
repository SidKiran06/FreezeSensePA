import streamlit as st
import pandas as pd

st.set_page_config(page_title='FreezeSense | Winter Safety', page_icon='❄️', layout='wide')
st.markdown('''<style>
.stApp {background:#f5f9fd;color:#16324b} .block-container{padding-top:1.5rem;max-width:1180px}
.hero{background:linear-gradient(115deg,#102c4a,#17648b);color:white;padding:2rem;border-radius:18px;margin-bottom:1rem}
.hero h1{color:white;font-size:2.8rem;margin:0}.hero p{color:#e3f3ff;font-size:1.1rem}
.notice{background:#fff0d9;border-left:5px solid #c67811;padding:12px 16px;border-radius:8px;margin:10px 0}
.small{color:#536c80;font-size:.85rem}
</style>''', unsafe_allow_html=True)

PAGES=['🏠 Home','🌡️ Freeze Risk','📦 Safety Kits','✅ Winter Checklist','📊 Impact Dashboard','🗓️ Project Roadmap']
page=st.sidebar.radio('Explore FreezeSense',PAGES)
st.sidebar.markdown('---')
st.sidebar.info('FBLA 2026–27 | Student-led project proposal. No kits or outcomes are claimed as completed.')

if page==PAGES[0]:
    st.markdown('<div class="hero"><h1>❄️ FreezeSense</h1><p>Protecting Homes, One Winter at a Time.</p><p>A student-led initiative combining winter safety kits, practical education, and freeze-weather awareness.</p></div>',unsafe_allow_html=True)
    st.subheader('Why winter preparedness matters')
    a,b,c=st.columns(3)
    a.metric('Pennsylvania claims reported','$17.4M',help='State Farm frozen-pipe and water-damage claims in Pennsylvania, 2024–June 2025, as reported by BCTV (Jan. 2026). Not all insurers.')
    b.metric('Average US claim','$15,400',help='Water damage and freezing homeowners insurance claim average, 2019–2023; Insurance Information Institute.')
    c.metric('Initial kit target','20 homes',help='A proposed target, not an achieved outcome.')
    st.caption('Sources: BCTV reporting State Farm data (Jan. 27, 2026); Insurance Information Institute homeowners insurance statistics. Figures are from the mentor planning document; confirm against original publications before public release.')
    st.subheader('Our four-part approach')
    for title,desc in [('📦 Prevention kits','Assemble affordable supplies with donated materials.'),('💻 Safety website','Explain winter risks and practical prevention steps.'),('📣 Freeze Watch','Share approved reminders through community partners.'),('📊 Impact evaluation','Track verified deliveries and preparedness surveys once outreach begins.')]:
        st.markdown(f'**{title}** — {desc}')
    st.info('Current stage: proposal and website prototype. Partnerships, funding, and kit distribution are planned, not confirmed.')

elif page==PAGES[1]:
    st.title('🌡️ Freeze Risk Explorer')
    st.write('Explore how a **forecast outdoor low temperature** might change your preparation priorities. This is an educational scenario tool, not a live forecast or a prediction of pipe temperature.')
    temp=st.slider('Illustrative forecast outdoor low (°F)',-20,60,15)
    if temp<=20:
        st.error('Elevated concern: very cold weather. Check vulnerable pipes and follow local winter safety guidance.')
    elif temp<=32:
        st.warning('Freezing conditions possible. Review exposed pipes and monitor local forecasts.')
    else:
        st.success('Above freezing in this scenario. Continue routine leak checks and seasonal preparation.')
    st.markdown('**What to do:** Identify the main water shutoff, insulate exposed pipes correctly, protect outdoor faucets, maintain safe indoor heating, and seek professional help for vulnerable plumbing.')
    st.caption('The 20°F outdoor threshold is a general warning rule of thumb cited by Consumer Reports in the mentor plan, not a guarantee. Pipes can freeze at other temperatures depending on exposure and conditions.')
    st.markdown('**Live forecast:** Not connected in this demo. Consult the [National Weather Service](https://www.weather.gov/) for current local warnings.')

elif page==PAGES[2]:
    st.title('📦 Winter Safety Kits')
    st.write('Proposed contents — items will be selected with partner or plumbing-professional guidance. These are not assembled or distributed yet.')
    items={'Foam pipe insulation sleeves':'For suitable exposed pipes; correct sizing and installation matter.','Outdoor faucet cover':'For compatible exterior faucets.','Toilet leak-detection tablets':'Helps identify some toilet leaks.','Water shutoff identification tag':'Helps a household label its shutoff after identifying it correctly.','Winter preparedness instruction card':'Simple guidance and trusted local resources.'}
    for item,detail in items.items():
        with st.expander('✓ '+item): st.write(detail)
    st.subheader('Proposed budget calculator')
    kits=st.slider('Number of kits',5,100,20,5)
    cost=st.slider('Estimated cost per kit ($)',5,35,25)
    donated=st.slider('Illustrative donated value ($)',0,kits*cost,0,25)
    x,y,z=st.columns(3)
    x.metric('Gross budget',f'${kits*cost:,}')
    y.metric('Illustrative donations',f'${donated:,}')
    z.metric('Remaining funding need',f'${kits*cost-donated:,}')
    st.caption('Budget is hypothetical. $25 per kit is a planning ceiling, not a verified quotation. Donations slider does not represent secured funds.')
    st.warning('Students will not enter homes, install pipe insulation, or work on plumbing. Distribution and any installation guidance must be handled by appropriate adults/partners.')

elif page==PAGES[3]:
    st.title('✅ Household Winter Preparedness Checklist')
    st.write('Use this checklist as an educational guide. It does not replace a professional home assessment.')
    questions=['I know where my main water shutoff valve is.','I have checked for exposed or vulnerable pipes.','I have reviewed safe outdoor faucet winterization steps.','I know where to find local weather alerts.','I have a plan to maintain safe indoor heating during cold weather.','I know whom to contact if a pipe leaks or freezes.']
    done=[st.checkbox(q,key=f'q{i}') for i,q in enumerate(questions)]
    st.progress(sum(done)/len(done))
    st.write(f'{sum(done)} of {len(done)} preparedness steps reviewed')
    st.info('Your checklist responses stay within this browser session; this prototype does not store or submit them.')
    st.markdown('Helpful resources: [National Weather Service](https://www.weather.gov/) · [Ready PA](https://www.ready.pa.gov/) · [EPA WaterSense](https://www.epa.gov/watersense)')

elif page==PAGES[4]:
    st.title('📊 Community Impact Dashboard')
    st.markdown('<div class="notice"><b>DEMONSTRATION DATA — HYPOTHETICAL, NOT ACTUAL PROJECT RESULTS.</b><br>All sample results below are invented solely to demonstrate how future verified outcomes could be displayed.</div>',unsafe_allow_html=True)
    st.subheader('Proposed project targets')
    a,b,c=st.columns(3)
    a.metric('Initial kit target','20')
    b.metric('Stretch kit target','50')
    c.metric('Per-kit cost ceiling','$25')
    st.subheader('Illustrative dashboard preview')
    data=pd.DataFrame({'Month':['December','January','February'],'Example kits delivered':[5,8,7],'Example households reached':[5,10,9]})
    st.bar_chart(data.set_index('Month'))
    st.caption('Chart values are fictional demonstration data; they are not forecasts, commitments, or completed activities.')
    st.subheader('Example survey reporting format')
    s=pd.DataFrame({'Measure':['Know main shutoff location','Know freeze prevention steps'],'Illustrative before (%)':[35,40],'Illustrative after (%)':[70,85]})
    st.dataframe(s,hide_index=True,use_container_width=True)
    st.caption('Survey percentages above are invented for layout demonstration only. Actual baseline and follow-up surveys have not been conducted.')
    st.write('When the project launches, the team would replace this page with documented kit delivery totals, outreach logs, volunteer hours, and anonymous survey results.')

else:
    st.title('🗓️ Project Roadmap')
    steps=[('November 2026','Research community needs, verify data, contact potential partners, prepare budget and website.'),('December 2026','Seek donations, assemble initial kits if funded, launch education and outreach.'),('January 2027','Coordinate distribution with approved partners and share winter preparedness reminders.'),('Early February 2027','Collect feedback, analyze verified results, and prepare the competition presentation.')]
    for name,desc in steps:
        st.subheader(name);st.write(desc)
    st.subheader('Potential partners — not yet confirmed')
    st.write('Hardware stores • Plumbing businesses • Community service organizations • Area Agency on Aging • Weatherization agencies')
    st.subheader('How we would measure success')
    st.write('Document deliveries, reach, costs, volunteer participation, and anonymous before-and-after preparedness surveys. Never claim prevented pipe bursts without supporting evidence.')

st.divider()
st.caption('FreezeSense | FBLA Community Service proposal | Educational prototype. Not an emergency alert service, plumbing diagnosis, or guarantee against frozen pipes.')
