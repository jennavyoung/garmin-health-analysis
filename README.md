# 🏃 Garmin Fitness & Sleep Data Analysis

> **Personal health analytics project** using Python to extract insights from Garmin wearable data.  
> Built to demonstrate data cleaning, exploratory analysis, and visualization skills.

---

## 📌 Overview

This project analyzes real wearable data exported from a **Garmin fitness watch** via Garmin Connect. It covers two datasets — **activity tracking** and **sleep quality** — and transforms raw CSV/Excel exports into meaningful health insights using Python.

| Project | Data | Key Question |
|---|---|---|
| 🏋️ Activity Analysis | `Activities.csv` | What do my workout patterns reveal about my fitness habits? |
| 😴 Sleep Analysis | `Sleep_Analysis.xlsx` | How does my sleep quality correlate with duration and recovery? |

---

## 📊 Dashboards

### Activity Analysis
![Activity Dashboard](outputs/garmin_dashboard.png)

### Sleep Analysis
![Sleep Dashboard](outputs/sleep_dashboard.png)

---

## 🔍 Key Findings

### Activity (Feb 7 – Mar 4, 2026)
- Logged **25 workouts** across 26 days — averaging **5 sessions/week**
- Burned **7,319 total calories** over **21 hours** of exercise
- **Strength training** made up 52% of sessions (13 sessions)
- Peak heart rate reached **190 bpm** during outdoor running
- Most active week: **Week 7** with 8 sessions

### Sleep (Feb 8 – Mar 4, 2026)
- Average sleep score: **77.9 / 100** across 21 nights
- Strong correlation between sleep duration and score: **r = 0.72**
- Excellent nights averaged **8.5 hrs** vs Poor nights at **6.2 hrs**
- **57% of nights** rated Good or Excellent
- Best sleep day: **Fridays** (avg score: 89.3)

---

## 🛠️ Tech Stack

```
Python 3.x
├── pandas       — data loading, cleaning, aggregation
├── numpy        — numerical operations, correlation analysis
├── matplotlib   — multi-panel dashboards, custom styling
├── seaborn      — statistical visualization
└── openpyxl     — Excel file ingestion
```

---

## 📁 Project Structure

```
garmin-health-analysis/
│
├── data/
│   ├── Activities.csv          # Raw Garmin activity export
│   └── Sleep_Analysis.xlsx     # Sleep data (raw + cleaned sheets)
│
├── outputs/
│   ├── garmin_dashboard.png    # Activity analysis dashboard
│   └── sleep_dashboard.png     # Sleep analysis dashboard
│
├── garmin_analysis.py          # Activity data analysis script
├── sleep_analysis.py           # Sleep data analysis script
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🚀 How to Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/garmin-health-analysis.git
cd garmin-health-analysis
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the analyses**
```bash
python garmin_analysis.py   # Generates activity dashboard
python sleep_analysis.py    # Generates sleep dashboard
```

Dashboards will be saved to the `outputs/` folder.

---

## 🧹 Data Pipeline

```
Garmin Connect Export
        │
        ▼
  Raw CSV / Excel
        │
        ▼
  Data Cleaning
  ├── Parse dates & durations
  ├── Remove '--' null placeholders
  ├── Convert comma-formatted numbers
  └── Standardize activity categories
        │
        ▼
  Exploratory Analysis
  ├── Aggregations by activity type & week
  ├── Correlation analysis (sleep duration ↔ score)
  └── Day-of-week patterns
        │
        ▼
  Visualization Dashboard
  └── 6-panel matplotlib figure with custom dark theme
```

---

## 📈 Skills Demonstrated

- **Data wrangling** with pandas (handling nulls, type parsing, groupby)
- **Exploratory Data Analysis (EDA)** — distributions, correlations, trends
- **Data visualization** — multi-panel dashboards with matplotlib
- **Excel integration** — reading multi-sheet workbooks with openpyxl/pandas
- **Statistical thinking** — correlation coefficients, trend lines
- **Clean, modular Python** — functions, docstrings, separation of concerns

---

## 🔮 Future Improvements

- [ ] Combine sleep and activity data to find cross-dataset correlations
- [ ] Add interactive Plotly/Dash dashboard
- [ ] Automate Garmin data ingestion via Garmin Connect API
- [ ] Build a predictive model for sleep score based on daily activity

---

*Data exported from Garmin Connect. All data is personal and anonymized.*
