# FreezeSense — Streamlit FBLA community service prototype

## Deploy
Upload `app.py` and `requirements.txt` to the **root** of the new `FreezeSensePA` GitHub repository. On Streamlit Community Cloud deploy that repository, branch `main`, main file path `app.py`. This does not change the RadonReady repository or deployment.

## Features
Top navigation tabs, interactive freeze-risk scenario, configurable kit budget, private preparedness checklist, large-point milestone journey chart, clearly hypothetical demonstration mode, session-recorded activity logs and anonymous before/after survey entries, CSV export/import, and project roadmap.

## Important data notes
- The demonstration chart and sample survey percentages are **fictional** and prominently labeled.
- Recorded activity and survey entries are stored **only in Streamlit session state**. They are not shared between users or reliably persistent. Export the CSV to retain them, and restore it using the import tool. For a real multi-user program, implement a secure authenticated database with adviser oversight before collecting any data.
- Never enter personally identifying household information.
- The freeze-risk slider is educational and not a live weather feed.
- The planning kit prices are illustrative, not vendor quotations.
- Historical statistics originate from the mentor planning document and should be verified against their original sources.

## Run locally
`pip install -r requirements.txt`
`streamlit run app.py`
