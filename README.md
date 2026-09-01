# Global CO2 Emissions Tracker by Sector

## Objective
Track and visualize carbon emissions from energy, transport, and industry sectors across countries, with per-capita and per-GDP metrics, to identify top polluters and emission trends over time.

## Tools Used
- **Python (Pandas)** — data cleaning and metric computation
- **Tableau** — interactive dashboard (maps, bar charts by sector)
- **Excel** — quick data checks / pivot exploration

## Data Sources
- [Our World in Data — CO2 and GHG Emissions Dataset](https://github.com/owid/co2-data)
- [Climate Watch Data](https://www.climatewatchdata.org/) — sector-level emissions breakdown

## Project Structure
```
co2-emissions-tracker/
├── data/
│   ├── raw/            # raw downloaded CSVs (not committed — see .gitignore)
│   └── processed/       # cleaned, merged output
├── notebooks/           # exploratory analysis (optional)
├── data_prep.py         # cleaning + metric computation script
├── requirements.txt
├── report.pdf            # 1–2 page project report
└── README.md
```

## How to Run
1. Clone this repo and create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Download the raw datasets into `data/raw/` (see Data Sources above).
3. Run the data prep script:
   ```
   python data_prep.py
   ```
4. Open `data/processed/co2_emissions_processed.csv` in Tableau to build the dashboard.

## Dashboard
🔗 [Link to published Tableau Public dashboard] — *add this once you publish*

## Key Findings
*(Fill in after analysis — e.g. which sectors/countries are top emitters, notable trends)*

## Deliverables
- [x] Data cleaning script
- [ ] Tableau dashboard
- [ ] PDF report with policy brief on top polluters
