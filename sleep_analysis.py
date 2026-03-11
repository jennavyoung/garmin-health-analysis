"""
========================================================
Garmin Sleep Analysis - Python Data Analysis Project
========================================================
Author: Portfolio Project | Information Systems Management
Tools: Python, Pandas, Matplotlib, Seaborn, NumPy
Data:  Garmin Connect Sleep Export (Cleaned via Excel)
========================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. DATA LOADING & CLEANING
# ─────────────────────────────────────────────

def load_data(filepath):
    """Load and clean the Garmin sleep dataset."""
    df = pd.read_excel(filepath, sheet_name='Cleaned Data')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    # Normalize quality labels
    quality_order = ['Poor', 'Fair', 'Good', 'Excellent']
    df['Quality'] = pd.Categorical(df['Quality'], categories=quality_order, ordered=True)

    # Bedtime hour as numeric (0=midnight, 1=1am, etc.)
    df['Bedtime_Hour'] = pd.to_numeric(df['Bedtime_Hour'], errors='coerce')

    return df


# ─────────────────────────────────────────────
# 2. STYLING CONFIG
# ─────────────────────────────────────────────

BG     = '#0D1117'
PANEL  = '#161B22'
TEXT   = '#E6EDF3'
SUB    = '#8B949E'
GRID   = '#21262D'
ACCENT = '#58A6FF'

QUALITY_COLORS = {
    'Poor':      '#E63946',
    'Fair':      '#F4A261',
    'Good':      '#457B9D',
    'Excellent': '#2A9D8F',
}

def style_ax(ax, title='', xlabel='', ylabel=''):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=SUB, labelsize=9)
    ax.xaxis.label.set_color(SUB)
    ax.yaxis.label.set_color(SUB)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(color=GRID, linewidth=0.6, alpha=0.8)
    if title:  ax.set_title(title, color=TEXT, fontsize=11, fontweight='bold', pad=10)
    if xlabel: ax.set_xlabel(xlabel, color=SUB, fontsize=9)
    if ylabel: ax.set_ylabel(ylabel, color=SUB, fontsize=9)


# ─────────────────────────────────────────────
# 3. DASHBOARD
# ─────────────────────────────────────────────

def generate_dashboard(df, output_path):
    fig = plt.figure(figsize=(18, 14), facecolor=BG)
    fig.suptitle(
        'GARMIN SLEEP ANALYSIS  |  Feb – Mar 2026',
        fontsize=18, fontweight='bold', color=TEXT,
        y=0.97, fontfamily='monospace'
    )

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.52, wspace=0.38,
                           left=0.06, right=0.97, top=0.91, bottom=0.06)

    # ── KPI Banner ──────────────────────────────────────────
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.set_facecolor(PANEL)
    ax_kpi.axis('off')
    for spine in ax_kpi.spines.values():
        spine.set_edgecolor(GRID)

    kpis = [
        ('🌙 Avg Sleep Score',   f"{df['Score'].mean():.0f} / 100"),
        ('⏱ Avg Sleep Duration', f"{df['Duration_Hours'].mean():.1f} hrs"),
        ('❤️ Avg Resting HR',    f"{df['RestingHR_Clean'].mean():.0f} bpm"),
        ('🔋 Avg Body Battery',  f"{df['BodyBattery_Clean'].mean():.0f} / 100"),
        ('💨 Avg Respiration',   f"{df['Respiration_Clean'].mean():.1f} br/min"),
        ('✨ Excellent Nights',  f"{(df['Quality']=='Excellent').sum()} / {len(df)}"),
    ]

    for i, (label, value) in enumerate(kpis):
        x = 0.08 + i * 0.155
        ax_kpi.text(x, 0.75, value, transform=ax_kpi.transAxes,
                    fontsize=19, fontweight='bold', color=ACCENT,
                    ha='center', fontfamily='monospace')
        ax_kpi.text(x, 0.18, label, transform=ax_kpi.transAxes,
                    fontsize=8, color=SUB, ha='center')

    # ── Chart 1: Sleep Score Over Time ──────────────────────
    ax1 = fig.add_subplot(gs[1, :2])
    colors_line = [QUALITY_COLORS.get(str(q), '#888') for q in df['Quality']]
    ax1.fill_between(df['Date'], df['Score'], alpha=0.12, color=ACCENT)
    ax1.plot(df['Date'], df['Score'], color=GRID, linewidth=1.2, zorder=2)
    ax1.scatter(df['Date'], df['Score'], c=colors_line, s=55,
                zorder=3, edgecolors=BG, linewidths=0.8)
    # Avg line
    avg = df['Score'].mean()
    ax1.axhline(avg, color=ACCENT, linestyle='--', linewidth=1, alpha=0.6)
    ax1.text(df['Date'].max(), avg + 1.5, f'Avg: {avg:.0f}',
             color=ACCENT, fontsize=8)
    style_ax(ax1, 'Sleep Score Over Time', 'Date', 'Score')
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %d'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')
    ax1.set_ylim(40, 105)
    patches = [mpatches.Patch(color=v, label=k) for k, v in QUALITY_COLORS.items()]
    ax1.legend(handles=patches, loc='lower right', fontsize=7,
               labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)

    # ── Chart 2: Sleep Quality Distribution ─────────────────
    ax2 = fig.add_subplot(gs[1, 2])
    qual_counts = df['Quality'].value_counts().reindex(['Poor','Fair','Good','Excellent'])
    bar_colors = [QUALITY_COLORS[k] for k in qual_counts.index]
    bars = ax2.bar(qual_counts.index, qual_counts.values,
                   color=bar_colors, edgecolor=BG, linewidth=0.8, width=0.6)
    for bar, val in zip(bars, qual_counts.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(val), ha='center', va='bottom', color=TEXT,
                 fontsize=10, fontweight='bold')
    style_ax(ax2, 'Sleep Quality Distribution', 'Quality', 'Nights')

    # ── Chart 3: Duration vs Score Scatter ──────────────────
    ax3 = fig.add_subplot(gs[2, 0])
    sc_colors = [QUALITY_COLORS.get(str(q), '#888') for q in df['Quality']]
    ax3.scatter(df['Duration_Hours'], df['Score'], c=sc_colors,
                s=70, edgecolors=BG, linewidths=0.8, alpha=0.9)
    # Trend line
    mask = df['Duration_Hours'].notna() & df['Score'].notna()
    z = np.polyfit(df.loc[mask, 'Duration_Hours'], df.loc[mask, 'Score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['Duration_Hours'].min(), df['Duration_Hours'].max(), 100)
    ax3.plot(x_line, p(x_line), color=ACCENT, linestyle='--',
             linewidth=1.2, alpha=0.7, label='Trend')
    style_ax(ax3, 'Duration vs Sleep Score', 'Hours Slept', 'Sleep Score')
    ax3.legend(fontsize=7, labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)

    # ── Chart 4: Resting HR vs Score ────────────────────────
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.scatter(df['RestingHR_Clean'], df['Score'],
                c=sc_colors, s=70, edgecolors=BG, linewidths=0.8, alpha=0.9)
    mask2 = df['RestingHR_Clean'].notna() & df['Score'].notna()
    z2 = np.polyfit(df.loc[mask2, 'RestingHR_Clean'], df.loc[mask2, 'Score'], 1)
    p2 = np.poly1d(z2)
    x2 = np.linspace(df['RestingHR_Clean'].min(), df['RestingHR_Clean'].max(), 100)
    ax4.plot(x2, p2(x2), color='#E63946', linestyle='--',
             linewidth=1.2, alpha=0.7, label='Trend')
    style_ax(ax4, 'Resting HR vs Sleep Score', 'Resting HR (bpm)', 'Sleep Score')
    ax4.legend(fontsize=7, labelcolor=TEXT, facecolor=PANEL, edgecolor=GRID)

    # ── Chart 5: Avg Score by Day of Week ───────────────────
    ax5 = fig.add_subplot(gs[2, 2])
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_scores = df.groupby('DayOfWeek')['Score'].mean().reindex(day_order).dropna()
    day_colors = [ACCENT if v >= day_scores.mean() else '#4A5568' for v in day_scores]
    bars5 = ax5.bar(range(len(day_scores)), day_scores.values,
                    color=day_colors, edgecolor=BG, linewidth=0.8, width=0.6)
    ax5.set_xticks(range(len(day_scores)))
    ax5.set_xticklabels([d[:3] for d in day_scores.index], color=SUB, fontsize=8)
    ax5.axhline(day_scores.mean(), color=ACCENT, linestyle='--',
                linewidth=1, alpha=0.5)
    for bar, val in zip(bars5, day_scores.values):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{val:.0f}', ha='center', va='bottom', color=TEXT, fontsize=8)
    style_ax(ax5, 'Avg Sleep Score by Day', '', 'Avg Score')
    ax5.set_ylim(60, 100)

    # Footer
    fig.text(0.5, 0.01,
             'Data Source: Garmin Connect Export  |  Python Analysis: pandas · matplotlib · numpy',
             ha='center', color=SUB, fontsize=8, fontfamily='monospace')

    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close()
    print(f"✅ Dashboard saved → {output_path}")


# ─────────────────────────────────────────────
# 4. PRINT INSIGHTS
# ─────────────────────────────────────────────

def print_insights(df):
    print("\n" + "="*55)
    print("  GARMIN SLEEP INSIGHTS REPORT")
    print("="*55)

    print(f"\n📊 OVERVIEW  ({df['Date'].min().strftime('%b %d')} – {df['Date'].max().strftime('%b %d, %Y')})")
    print(f"   Nights tracked    : {len(df)}")
    print(f"   Avg sleep score   : {df['Score'].mean():.1f} / 100")
    print(f"   Avg duration      : {df['Duration_Hours'].mean():.2f} hrs")
    print(f"   Avg resting HR    : {df['RestingHR_Clean'].mean():.1f} bpm")
    print(f"   Avg body battery  : {df['BodyBattery_Clean'].mean():.1f} / 100")

    print(f"\n🌙 SLEEP QUALITY BREAKDOWN")
    for q in ['Excellent','Good','Fair','Poor']:
        n = (df['Quality'] == q).sum()
        pct = n / len(df) * 100
        bar = '█' * n
        print(f"   {q:<10} {bar:<20} {n} nights ({pct:.0f}%)")

    print(f"\n🏆 BEST & WORST NIGHTS")
    best = df.loc[df['Score'].idxmax()]
    worst = df.loc[df['Score'].idxmin()]
    print(f"   Best:  {best['Date'].strftime('%b %d')} — Score {int(best['Score'])}, {best['Duration_Hours']:.1f} hrs ({best['Quality']})")
    print(f"   Worst: {worst['Date'].strftime('%b %d')} — Score {int(worst['Score'])}, {worst['Duration_Hours']:.1f} hrs ({worst['Quality']})")

    print(f"\n📅 BEST DAYS OF WEEK")
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_avg = df.groupby('DayOfWeek')['Score'].mean().reindex(day_order).dropna()
    for day, score in day_avg.sort_values(ascending=False).head(3).items():
        print(f"   {day:<12} avg score: {score:.1f}")

    print(f"\n💡 KEY INSIGHTS")
    corr_dur = df[['Duration_Hours','Score']].corr().iloc[0,1]
    corr_hr  = df[['RestingHR_Clean','Score']].corr().iloc[0,1]
    print(f"   • Sleep duration ↔ score correlation : r = {corr_dur:.2f}")
    print(f"   • Resting HR ↔ score correlation     : r = {corr_hr:.2f}")
    excellent_dur = df[df['Quality']=='Excellent']['Duration_Hours'].mean()
    poor_dur      = df[df['Quality']=='Poor']['Duration_Hours'].mean()
    print(f"   • Excellent nights avg duration : {excellent_dur:.1f} hrs")
    print(f"   • Poor nights avg duration      : {poor_dur:.1f} hrs")
    print(f"   • {(df['Quality'].isin(['Good','Excellent'])).sum()} of {len(df)} nights were Good or Excellent ({(df['Quality'].isin(['Good','Excellent'])).mean()*100:.0f}%)")
    print("\n" + "="*55)


# ─────────────────────────────────────────────
# 5. MAIN
# ─────────────────────────────────────────────

if __name__ == '__main__':
    INPUT  = '/mnt/user-data/uploads/Sleep_Analysis.xlsx'
    OUTPUT = '/mnt/user-data/outputs/sleep_dashboard.png'

    df = load_data(INPUT)
    print_insights(df)
    generate_dashboard(df, OUTPUT)
