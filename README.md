# Route Fare Comparator

A five-day team prototype for comparing public and informal transport fare estimates between locations. The app uses **Python, Streamlit and pandas** so contributors can focus on collecting trustworthy data, calculating commute estimates and validating the result.

> **Important:** The records currently in `data/fares.csv` are illustrative sample data. They are not verified transport prices. Replace them with collected, dated and sourced records before presenting the app as a factual fare guide.

## What the prototype does

- Lets a user select an origin and destination from the dataset.
- Shows matching fare records across transport modes.
- Estimates weekly and monthly fare ranges using a user-provided number of one-way trips.
- Displays fare options in a table and a simple chart.
- Keeps calculation logic in `calculator.py`, separate from the Streamlit interface.
- Includes tests for route filtering, input validation and monthly cost arithmetic.

## Repository structure

```text
route-fare-comparator/
├── app.py                 # Streamlit UI and data loading
├── calculator.py           # Reusable fare validation and calculation logic
├── data/
│   └── fares.csv          # Shared dataset; agreed columns
├── tests/
│   └── test_calculator.py # Automated tests
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer recommended
- Git
- A terminal and a GitHub account
- Internet connection for installing packages and deploying

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/route-fare-comparator.git
cd route-fare-comparator
```

Replace the URL with your repository URL.

### 2. Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the app

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## Run tests

From the repository root, with the virtual environment activated:

```bash
pytest -q
```

Run tests before opening a pull request. Add tests when changing calculations or data validation.

## Shared dataset contract

The team must preserve these column names in `data/fares.csv`:

| Column | Meaning | Example |
|---|---|---|
| `origin` | Starting location | Central Market |
| `destination` | Ending location | University Gate |
| `mode` | Transport mode | Bus, Keke, Taxi |
| `min_fare` | Lowest observed/credible one-way fare, numeric NGN | `300` |
| `max_fare` | Highest observed/credible one-way fare, numeric NGN | `500` |
| `duration_min` | Estimated journey duration in minutes | `35` |
| `source` | Where/how the fare was collected | Operator quote, field survey |
| `date_collected` | Date the fare was collected, ISO format | `2026-10-20` |

### Data quality rules

1. Keep fares as numbers only: do not put `₦`, commas or explanatory text in numeric cells.
2. `min_fare` must be less than or equal to `max_fare`.
3. Fare and duration values cannot be negative.
4. Every record needs a source and collection date. If something is unknown, flag it for the Data Lead rather than inventing it.
5. Do not silently combine different routes or directions. If the reverse journey differs, add a separate record with the reverse origin and destination.
6. Use consistent location names. Agree on spelling before data collection begins.
7. Mark estimates, negotiated prices or unverified reports clearly in the `source` field or a team-maintained notes sheet.
8. The sample rows are placeholders. Remove or replace them before the public demo.

## Calculation assumptions

- `trips_per_week` means **one-way journeys**, not commute days.
- A return commute five days a week is 10 one-way trips.
- Monthly estimates use 4.33 weeks by default (52 weeks / 12 months).
- The low estimate multiplies `min_fare`; the high estimate multiplies `max_fare`.
- These are estimates, not guarantees. Prices, route availability and traffic can change.

The reusable `monthly_cost()` function in `calculator.py` accepts the fare range, one-way trips per week and weeks per month. Keep business logic there rather than duplicating arithmetic in `app.py`.

## Team ownership and collaboration

Suggested ownership for an eight-person team:

| Role | Ownership | Main deliverable |
|---|---|---|
| 1. Team Lead / Integrator | Task board, check-ins, repository, final merge and demo | Integrated working app |
| 2. Data Collector A | Formal transport fares: bus, BRT, rail where applicable | Formal fares sheet |
| 3. Data Collector B | Informal transport: taxi, keke, minibus etc. | Informal fares sheet |
| 4. Data Lead / Validator | Merge, normalize names, check required fields, verify suspicious values | Clean `data/fares.csv` |
| 5. UI Developer 1 | Input and route-selection experience in `app.py` | Input section / agreed function |
| 6. UI Developer 2 | Results table, chart and visual polish in `app.py` | Results section / agreed function |
|  7. Logic Developer | `calculator.py`, fare ranges and cost calculations | Calculation functions + tests |
|  8. QA, Docs and Presentation | Tests, README updates, demo script and slides | QA checklist and presentation |

### Avoiding conflicts in `app.py`

Two people editing the same file can create merge conflicts. Before work begins, the UI developers should agree on function boundaries and avoid editing the same section. A better arrangement is for each developer to work in a separate branch and submit a pull request. The integrator merges changes and runs the app and tests.

If the team has time, refactor UI sections into separate files (for example `ui_inputs.py` and `ui_results.py`) after the first working version. Do not spend Day 1 overengineering the architecture.

## Git workflow for collaborators

### Team Lead: create and push the repository

```bash
git init
git add .
git commit -m "Initial Streamlit fare comparator scaffold"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/route-fare-comparator.git
git push -u origin main
```

If you created the repository on GitHub with a README or license already, follow GitHub's instructions for reconciling the existing remote commit before pushing.

### Invite collaborators

On GitHub:

1. Open the repository.
2. Go to **Settings → Collaborators** (or **Collaborators and teams**, depending on the interface).
3. Choose **Add people**.
4. Search each teammate's GitHub username and send the invitation.
5. Ask each person to accept the invitation.

Only grant access to people who should be able to contribute to this project.

### Each collaborator: clone and create a branch

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/route-fare-comparator.git
cd route-fare-comparator
git switch -c feat/short-description
```

Examples:

```bash
git switch -c data/formal-fares
git switch -c data/informal-fares
git switch -c feat/results-chart
git switch -c feat/calculator-tests
```

After making changes:

```bash
git add path/to/changed-files
git commit -m "Describe the change"
git push -u origin feat/short-description
```

Then open a **Pull Request** on GitHub targeting `main`. Describe what changed and how it was tested. The Team Lead or Data Lead reviews and merges it.

### Keep `main` stable

- Do not all push directly to `main`.
- Pull the latest `main` before starting a new task.
- Keep pull requests focused and small.
- Never commit `.env`, API keys, passwords or private credentials.
- Resolve conflicts with the file owner or integrator; do not discard another person's work without checking.

## Five-day build plan

### Day 1 - Setup and data contract
- Team Lead creates repository, invites collaborators and sets up task board.
- Everyone agrees on route naming and CSV columns.
- Data collectors identify sources and begin collecting.
- Logic and UI developers agree on function inputs/outputs.
- All contributors clone the repository and run the starter app.

**Day 1 exit check:** everyone can run the app; data columns and ownership are agreed.

### Day 2 - Data and core logic
- Collectors gather fares and record sources/dates.
- Data Lead normalizes and validates records.
- Logic Developer implements and tests route filtering and fare calculations.
- UI developers build input and result sections on separate branches.

**Day 2 exit check:** calculator tests pass and the app can show a route using team data.

### Day 3 - Integration
- Merge reviewed pull requests.
- Connect UI to the cleaned dataset and calculation functions.
- Test empty routes, reversed routes, missing data and invalid fare ranges.
- QA records bugs and assigns owners.

**Day 3 exit check:** one end-to-end route comparison works from the UI.

### Day 4 - QA and deployment
- Run tests and verify calculations manually against a few examples.
- Check data source labels and collection dates.
- Deploy to Streamlit Community Cloud or another agreed host.
- Fix high-priority issues and rehearse the demo.

**Day 4 exit check:** deployed app opens and core flow works.

### Day 5 - Freeze and present
- Avoid large new features.
- Re-test the deployed version.
- Prepare slides, limitations, data methodology and demo route.
- Ensure the team can explain where fares came from and how monthly estimates are calculated.

**Day 5 exit check:** stable live demo, README, and presentation ready.

## Deploy to Streamlit Community Cloud

1. Push the finished repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create a new app and select the repository, branch (`main`) and main file (`app.py`).
4. Deploy.
5. Open the public app URL and test the complete route-selection flow.

Deployment options and account requirements can change; follow the current Streamlit Community Cloud instructions if the UI differs.

## Definition of done

Before presenting, confirm:

- [ ] App launches from a clean clone using `pip install -r requirements.txt`.
- [ ] `pytest -q` passes.
- [ ] Dataset follows the agreed schema and contains sources and dates.
- [ ] Illustrative sample rows have been removed or unmistakably excluded from real results.
- [ ] Fare estimates and one-way trip assumptions are explained.
- [ ] At least two routes and multiple transport modes have been checked.
- [ ] Deployed link works on another team member's device.
- [ ] README, slides and demo script are up to date.

## Known limitations / next improvements

This is a starter prototype, not a production fare service. Potential next steps:

- Add a data-entry/CSV upload workflow with validation.
- Support route aliases and reverse-direction fares.
- Show freshness warnings for old collection dates.
- Add filters by transport mode and travel time.
- Add a map only if the team has reliable geospatial data.
- Add provenance notes and a clear method for resolving conflicting fare reports.
