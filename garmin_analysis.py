"""
========================================================
Garmin Fitness Watch - Activity Data Analysis
========================================================
Author: Portfolio Project | Information Systems Management
Tools: Python, Pandas, Matplotlib, Seaborn, NumPy
Data:  Garmin Connect Export (Activities.csv)
========================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. DATA LOADING & CLEANING
# ─────────────────────────────────────────────

def load_and_clean(filepath):
    """Load Garmin CSV and clean all columns for analysis."""
    df = pd.read_csv(filepath)

    # Replace '--' with NaN
    df.replace('--', np.nan, inplace=True)

    # Parse date
    df['Date'] = pd.to_datetime(df['Date'])
    df['Week'] = df['Date'].dt.isocalendar().week.astype(int)
    df['Day'] = df['Date'].dt.day_name()
    df['Month_Day'] = df['Date'].dt.strftime('%b %d')

    # Clean numeric columns (remove commas)
    numeric_cols = ['Calories', 'Avg HR', 'Max HR', 'Distance', 'Steps']
    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(',', ''), errors='coerce'
        )

    # Parse HH:MM:SS duration to minutes
    def parse_duration(t):
        try:
            parts = str(t).strip().split(':')
            if len(parts) == 3:
                return int(parts[0]) * 60 + int(parts[1]) + float(parts[2]) / 60
            return np.nan
        except:
            return np.nan

    df['Duration_min'] = df['Time'].apply(parse_duration)

    # Simplify activity types
    type_map = {
        'Treadmill Running': 'Treadmill Run',
        'Strength Training': 'Strength',
        'Running': 'Outdoor Run',
        'Walking': 'Walking',
        'Yoga': 'Yoga',
        'Stair Stepper': 'Stair Stepper'
    }
    df['Activity'] = df['Activity Type'].map(type_map).fillna(df['Activity Type'])

    return df


# ─────────────────────────────────────────────
# 2. STYLING CONFIGURATION
# ─────────────────────────────────────────────

PALETTE = {
    'Strength':      '#E63946',
    'Treadmill Run': '#457B9D',
    'Outdoor Run':   '#2A9D8F',
    'Walking':       '#E9C46A',
    'Yoga':          '#A8DADC',
    'Stair Stepper': '#F4A261',
}

BG       = '#0D1117'
PANEL    = '#161B22'
TEXT     = '#E6EDF3'
SUBTEXT  = '#8B949E'
ACCENT   = '#58A6FF'
GRID     = '#21262D'

def apply_dark_style(ax, title='', xlabel='', ylabel=''):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=SUBTEXT, labelsize=9)
    ax.xaxis.label.set_color(SUBTEXT)
    ax.yaxis.label.set_color(SUBTEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(color=GRID, linewidth=0.6, alpha=0.8)
    if title:
        ax.set_title(title, color=TEXT, fontsize=11, fontweight='bold', pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, color=SUBTEXT, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, color=SUBTEXT, fontsize=9)


# ─────────────────────────────────────────────
# 3. GENERATE DASHBOARD
# ─────────────────────────────────────────────

def generate_dashboard(df, output_path):
    fig = plt.figure(figsize=(18, 13), facecolor=BG)
    fig.suptitle(
        'GARMIN FITNESS ANALYSIS  |  Feb – Mar 2026',
        fontsize=18, fontweight='bold', color=TEXT,
        y=0.97, fontfamily='monospace'
    )

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.52, wspace=0.38,
                           left=0.06, right=0.97, top=0.91, bottom=0.06)

    colors = [PALETTE.get(a, '#888') for a in df['Activity']]

    # ── KPI Banner ──────────────────────────────────────────
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.set_facecolor(PANEL)
    ax_kpi.axis('off')
    for spine in ax_kpi.spines.values():
        spine.set_edgecolor(GRID)

    kpis = [
        ('🏃 Total Activities', f"{len(df)}"),
        ('🔥 Total Calories', f"{int(df['Calories'].sum()):,}"),
        ('⏱ Total Hours', f"{df['Duration_min'].sum()/60:.1f} hrs"),
        ('❤️ Avg Heart Rate', f"{df['Avg HR'].mean():.0f} bpm"),
        ('👟 Total Steps', f"{int(df['Steps'].sum()):,}"),
        ('📅 Active Days', f"{df['Date'].dt.date.nunique()}"),
    ]

    for i, (label, value) in enumerate(kpis):
        x = 0.08 + i * 0.155
        ax_kpi.text(x, 0.75, value, transform=ax_kpi.transAxes,
                    fontsize=20, fontweight='bold', color=ACCENT,
                    ha='center', fontfamily='monospace')
        ax_kpi.text(x, 0.2, label, transform=ax_kpi.transAxes,
                    fontsize=8, color=SUBTEXT, ha='center')

    # ── Chart 1: Calories by Activity Type (donut) ──────────
    ax1 = fig.add_subplot(gs[1, 0])
    ax1.set_facecolor(PANEL)
    cal_by_type = df.groupby('Activity')['Calories'].sum().sort_values(ascending=False)
    wedge_colors = [PALETTE.get(a, '#888') for a in cal_by_type.index]
    wedges, texts, autotexts = ax1.pie(
        cal_by_type, labels=None, colors=wedge_colors,
        autopct='%1.0f%%', pctdistance=0.82,
        wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
        startangle=140
    )
    for at in autotexts:
        at.set_color(TEXT); at.set_fontsize(8)
    legend_patches = [mpatches.Patch(color=PALETTE.get(k,'#888'), label=k)
                      for k in cal_by_type.index]
    ax1.legend(handles=legend_patches, loc='lower center',
               bbox_to_anchor=(0.5, -0.22), ncol=2,
               fontsize=7, labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)
    ax1.set_title('Calories by Activity Type', color=TEXT, fontsize=11,
                  fontweight='bold', pad=10)

    # ── Chart 2: Weekly Calories ─────────────────────────────
    ax2 = fig.add_subplot(gs[1, 1])
    week_cal = df.groupby('Week')['Calories'].sum()
    week_labels = [f"Wk {w}" for w in week_cal.index]
    bars = ax2.bar(week_labels, week_cal.values,
                   color=[ACCENT, '#F4A261', ACCENT, '#E63946', ACCENT],
                   edgecolor=BG, linewidth=0.8, width=0.6)
    for bar, val in zip(bars, week_cal.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                 f'{int(val):,}', ha='center', va='bottom',
                 color=TEXT, fontsize=8, fontweight='bold')
    apply_dark_style(ax2, 'Weekly Calories Burned', '', 'Calories')
    ax2.set_ylim(0, max(week_cal.values) * 1.18)

    # ── Chart 3: Avg HR by Activity ──────────────────────────
    ax3 = fig.add_subplot(gs[1, 2])
    hr_data = df.groupby('Activity')[['Avg HR', 'Max HR']].mean().sort_values('Avg HR')
    y_pos = range(len(hr_data))
    ax3.barh(y_pos, hr_data['Max HR'], color='#E63946', alpha=0.4,
             label='Max HR', height=0.5)
    ax3.barh(y_pos, hr_data['Avg HR'], color='#E63946', alpha=0.9,
             label='Avg HR', height=0.5)
    ax3.set_yticks(list(y_pos))
    ax3.set_yticklabels(hr_data.index, color=TEXT, fontsize=8)
    apply_dark_style(ax3, 'Heart Rate by Activity', 'BPM', '')
    leg = ax3.legend(fontsize=7, labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)

    # ── Chart 4: Activity Timeline ───────────────────────────
    ax4 = fig.add_subplot(gs[2, :2])
    df_sorted = df.sort_values('Date')
    scatter_colors = [PALETTE.get(a, '#888') for a in df_sorted['Activity']]
    sc = ax4.scatter(df_sorted['Date'], df_sorted['Duration_min'],
                     c=scatter_colors, s=df_sorted['Calories']/3,
                     alpha=0.85, edgecolors=BG, linewidths=0.8, zorder=3)
    ax4.plot(df_sorted['Date'], df_sorted['Duration_min'],
             color=GRID, linewidth=0.8, alpha=0.5, zorder=2)
    apply_dark_style(ax4, 'Activity Timeline  (bubble size = calories burned)',
                     'Date', 'Duration (minutes)')
    ax4.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %d'))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=30, ha='right')
    legend_patches2 = [mpatches.Patch(color=v, label=k) for k, v in PALETTE.items()
                       if k in df['Activity'].values]
    ax4.legend(handles=legend_patches2, loc='upper right', fontsize=7,
               labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID, ncol=2)

    # ── Chart 5: Duration Distribution ──────────────────────
    ax5 = fig.add_subplot(gs[2, 2])
    dur_by_type = df.groupby('Activity')['Duration_min'].sum().sort_values()
    bar_colors = [PALETTE.get(a, '#888') for a in dur_by_type.index]
    bars5 = ax5.barh(dur_by_type.index, dur_by_type.values,
                     color=bar_colors, edgecolor=BG, linewidth=0.8, height=0.6)
    for bar, val in zip(bars5, dur_by_type.values):
        ax5.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                 f'{val/60:.1f}h', va='center', color=TEXT, fontsize=8)
    apply_dark_style(ax5, 'Total Duration by Type', 'Minutes', '')
    ax5.set_yticklabels(dur_by_type.index, color=TEXT, fontsize=8)
    ax5.set_xlim(0, dur_by_type.max() * 1.2)

    # Footer
    fig.text(0.5, 0.01,
             'Data Source: Garmin Connect Export  |  Python Analysis: pandas · matplotlib · seaborn · numpy',
             ha='center', color=SUBTEXT, fontsize=8, fontfamily='monospace')

    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close()
    print(f"✅ Dashboard saved → {output_path}")


# ─────────────────────────────────────────────
# 4. PRINT INSIGHTS SUMMARY
# ─────────────────────────────────────────────

def print_insights(df):
    print("\n" + "="*55)
    print("  GARMIN FITNESS INSIGHTS REPORT")
    print("="*55)

    print(f"\n📊 OVERVIEW")
    print(f"   Activities logged : {len(df)}")
    print(f"   Date range        : {df['Date'].min().strftime('%b %d')} – {df['Date'].max().strftime('%b %d, %Y')}")
    print(f"   Total hours       : {df['Duration_min'].sum()/60:.1f} hrs")
    print(f"   Total calories    : {int(df['Calories'].sum()):,} kcal")
    print(f"   Total steps       : {int(df['Steps'].sum()):,}")

    print(f"\n🏆 ACTIVITY BREAKDOWN")
    breakdown = df.groupby('Activity').agg(
        Sessions=('Activity','count'),
        Avg_Duration=('Duration_min','mean'),
        Total_Calories=('Calories','sum'),
        Avg_HR=('Avg HR','mean')
    ).sort_values('Sessions', ascending=False)
    for act, row in breakdown.iterrows():
        print(f"   {act:<16} | {int(row.Sessions)} sessions | "
              f"{row.Avg_Duration:.0f} min avg | "
              f"{int(row.Total_Calories):,} cal total | "
              f"HR: {row.Avg_HR:.0f} bpm")

    print(f"\n🔥 BEST SESSIONS")
    print(f"   Highest Calories : {df.loc[df['Calories'].idxmax(), 'Title']} "
          f"({int(df['Calories'].max())} kcal)")
    print(f"   Longest Session  : {df.loc[df['Duration_min'].idxmax(), 'Title']} "
          f"({df['Duration_min'].max():.0f} min)")
    print(f"   Peak Heart Rate  : {int(df['Max HR'].max())} bpm")

    print(f"\n📅 WEEKLY CONSISTENCY")
    week_counts = df.groupby('Week').size()
    for week, count in week_counts.items():
        bar = '█' * count
        print(f"   Week {week}: {bar} ({count} sessions)")

    print(f"\n💡 KEY INSIGHTS")
    dominant = df['Activity'].value_counts().index[0]
    pct = df['Activity'].value_counts().iloc[0] / len(df) * 100
    print(f"   • {dominant} dominates at {pct:.0f}% of all sessions")
    print(f"   • Averaging {len(df) / df['Date'].dt.isocalendar().week.nunique():.1f} workouts/week")
    cals_per_hr = df['Calories'].sum() / (df['Duration_min'].sum() / 60)
    print(f"   • Burning ~{cals_per_hr:.0f} calories/hour on average")
    print(f"   • Most active week: Week {week_counts.idxmax()} ({week_counts.max()} sessions)")
    print("\n" + "="*55)


# ─────────────────────────────────────────────
# 5. MAIN
# ─────────────────────────────────────────────

if __name__ == '__main__':
    INPUT  = '/mnt/user-data/uploads/Activities.csv'
    OUTPUT = '/mnt/user-data/outputs/garmin_dashboard.png'

    df = load_and_clean(INPUT)
    print_insights(df)
    generate_dashboard(df, OUTPUT)
