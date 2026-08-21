# Football stats tracker for matches with friends
This a simple streamlit dashboard built to track football stats of frindley matches with friends.

## Setup
In order to keep things simple, the dashboard was designed to consume the data from a Google Spreadsheet.
To make the dashboard work properly you'll need to add a Spreadsheet's URL in the `.streamlit/secrets.toml` file.
```toml
[connections.gsheets]
spreadsheet = "YOUR-LINK-HERE"
```
You'll also need to make the Spreadsheet public. Go to the sharing options, edit the settings to "Anyone with the link" and set
the role to read-only.

The table schema is currently:
```
| Player      | Matches | Wins | Draw | Losses | Goals | Assists |
|-------------|---------|------|------|--------|-------|---------|
| John Doe #1 | 2       | 1    | 0    | 1      | 1     | 0       |
| John Doe #2 | 2       | 1    | 0    | 1      | 0     | 1       |
| John Doe #3 | 1       | 1    | 0    | 0      | 1     | 0       |
```
Currently, the dashboard is not making use of Matches/Wins/Draws/Losses, since for my use case, this would not be so easy to keep track of.
Of course this can (and should be) changed in the future.

Once the Spreadsheet is set up, you can run the app locally with:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## App State
Currently the app is very early developments stages and has a lot of hardcoded UI texts, which I plan to change in the future.
The idea for this originated in the Projeto de Extensão FEF-Unicamp, where FEF (Physical Education School - UNICAMP) offers classes
for a variaty of sports. The teachers of this classes are the P.E. students themselves so the porject serve to give the first teaching experience for them.
The dashboard was made by the students of the football class from 2s2026.

