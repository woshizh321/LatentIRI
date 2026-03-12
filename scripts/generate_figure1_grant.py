"""Generate Figure 1 for Grant Application — Cohort Characteristics.

Layout (2-row composite, SCI double-column width):
  Row A: [Age Distribution: NHANES | HC] [Ethnicity: NHANES pie | HC pie]
  Row B: [Neutrophil]  [Lymphocyte]  [Platelet]  [Albumin]

Fixes vs. original generate_supplementary_figures_sci.py:
  - CBC x-axis clipped to physiological range (no outlier stretching)
  - Gender double-counting bug removed
  - NLR replaced by Albumin (model input vs. derived ratio)
  - Panel labels A-F added for grant readability
"""

import sys
import warnings
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------- #
#  Matplotlib config (mirrors sci_plot_config.py)
# --------------------------------------------------------------------------- #
matplotlib.rcParams.update(
    {
        "font.family": "Arial",
        "axes.unicode_minus": False,
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

PROJECT = Path(r"C:\Users\Wenxi He\projects\NHANES_Data")
OUT_DIR = PROJECT / "aim2" / "output" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COLOR_NHANES = "#4682B4"   # steelblue
COLOR_HC     = "#2E8B57"   # seagreen


# --------------------------------------------------------------------------- #
#  Data loading
# --------------------------------------------------------------------------- #
def load_nhanes() -> pd.DataFrame:
    """Try multiple candidate paths for the NHANES merged dataset."""
    candidates = [
        PROJECT / "data" / "nhanes_merged_with_demo.parquet",
        PROJECT / "data" / "nhanes_2017_2020_clean.parquet",
        PROJECT / "aim4" / "data" / "nhanes_latent_iri_locked.parquet",
    ]
    for p in candidates:
        if p.exists():
            df = pd.read_parquet(p)
            print(f"  NHANES loaded: {p.name}  N={len(df)}")
            return df
    raise FileNotFoundError(
        "No NHANES parquet found. Checked:\n" + "\n".join(str(c) for c in candidates)
    )


def load_hc() -> pd.DataFrame:
    p = PROJECT / "aim3" / "data" / "master_enriched_v2.parquet"
    df = pd.read_parquet(p)
    print(f"  Health Check loaded: {p.name}  N={len(df)}")
    return df


# --------------------------------------------------------------------------- #
#  Helper utilities
# --------------------------------------------------------------------------- #
def panel_label(ax, letter, x=-0.14, y=1.05):
    """Add bold panel letter (A, B, …) at top-left of axes."""
    ax.text(
        x, y, letter,
        transform=ax.transAxes,
        fontsize=11, fontweight="bold", va="top", ha="left",
    )


def kde_overlay(ax, data, color, lw=1.2):
    """Draw KDE curve if ≥20 valid values."""
    data = data.dropna()
    if len(data) < 20:
        return
    kde = gaussian_kde(data)
    xr = np.linspace(data.min(), data.max(), 300)
    ax.plot(xr, kde(xr), color=color, linewidth=lw)


def resolve_col(df, *candidates):
    """Return first column name found in df; raise if none."""
    for c in candidates:
        if c in df.columns:
            return c
    raise KeyError(f"None of {candidates} found in DataFrame columns: {list(df.columns[:20])}")


# --------------------------------------------------------------------------- #
#  Panel A — Age Distribution
# --------------------------------------------------------------------------- #
def plot_age(ax_n, ax_h, df_nhanes, df_hc):
    age_col_n = resolve_col(df_nhanes, "age", "RIDAGEYR", "age_year")
    age_col_h = resolve_col(df_hc,     "age_year", "age", "RIDAGEYR")

    n_age = df_nhanes[age_col_n].dropna()
    h_age = df_hc[age_col_h].dropna()

    for ax, data, color, title, n_label in [
        (ax_n, n_age, COLOR_NHANES, "NHANES (2017\u20132023)", f"N = {len(n_age):,}"),
        (ax_h, h_age, COLOR_HC,     "Health Check (2021\u20132025)", f"N = {len(h_age):,}"),
    ]:
        ax.hist(data, bins=28, density=True, alpha=0.75,
                color=color, edgecolor="white", linewidth=0.4)
        kde_overlay(ax, data, color="darkred")
        ax.axvline(data.mean(), color="darkred", linestyle="--",
                   linewidth=1.1, label=f"Mean = {data.mean():.1f} yr")
        ax.set_title(title, fontweight="bold", pad=3)
        ax.set_xlabel("Age (years)")
        ax.set_ylabel("Density")
        ax.legend(loc="upper right", framealpha=0.7)
        ax.text(0.97, 0.90, n_label, transform=ax.transAxes,
                ha="right", va="top", fontsize=7, color="gray")
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ax.spines[["top", "right"]].set_visible(False)


# --------------------------------------------------------------------------- #
#  Panel B — Ethnicity / Race
# --------------------------------------------------------------------------- #
NHANES_RACE_MAP = {
    1.0: "Mexican\nAmerican",
    2.0: "Other\nHispanic",
    3.0: "Non-Hispanic\nWhite",
    4.0: "Non-Hispanic\nBlack",
    5.0: "Other",
}
HC_ETH_KEEP = ["Han", "Zhuang", "Yao", "Miao", "Other"]

COLORS_NHANES_PIE = ["#5DA5DA", "#FAA43A", "#60BD68", "#F17CB0", "#B2912F"]
COLORS_HC_PIE     = ["#E8513A", "#5DA5DA", "#60BD68", "#FAA43A", "#B2912F"]

WEDGE_KW = dict(edgecolor="white", linewidth=0.8)


def _pie_hc_ethnicity(df_hc):
    """Aggregate HC ethnicities into top-4 + Other."""
    eth_col = resolve_col(df_hc, "ethnicity", "ethnic", "race")
    counts = df_hc[eth_col].value_counts()

    # Normalise common variants
    rename = {
        "汉族": "Han", "Han": "Han",
        "壮族": "Zhuang", "Zhuang": "Zhuang",
        "瑶族": "Yao", "Yao": "Yao",
        "苗族": "Miao", "Miao": "Miao",
    }
    idx = [rename.get(str(k), "Other") for k in counts.index]
    agg = pd.Series(counts.values, index=idx).groupby(level=0).sum()

    # Consolidate into keep list
    top4 = ["Han", "Zhuang", "Yao", "Miao"]
    result = {}
    for k in top4:
        result[k] = agg.get(k, 0)
    result["Other"] = agg.drop(labels=[k for k in top4 if k in agg.index],
                               errors="ignore").sum()
    return pd.Series(result)


def plot_ethnicity(ax_n, ax_h, df_nhanes, df_hc):
    # NHANES race
    race_col = resolve_col(df_nhanes, "race", "RIDRETH1", "RIDRETH3")
    nhanes_race = (
        df_nhanes[race_col]
        .map(NHANES_RACE_MAP)
        .value_counts()
        .reindex(list(NHANES_RACE_MAP.values()))
        .fillna(0)
    )

    # HC ethnicity
    hc_eth = _pie_hc_ethnicity(df_hc)

    for ax, data, colors, title, n_total in [
        (ax_n, nhanes_race, COLORS_NHANES_PIE,
         "NHANES\nRace/Ethnicity", len(df_nhanes)),
        (ax_h, hc_eth,     COLORS_HC_PIE,
         "Health Check\nEthnicity", len(df_hc)),
    ]:
        wedges, texts, autotexts = ax.pie(
            data,
            labels=data.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors[:len(data)],
            wedgeprops=WEDGE_KW,
            textprops={"fontsize": 6.5},
            pctdistance=0.78,
        )
        for at in autotexts:
            at.set_fontsize(6)
        ax.set_title(title, fontweight="bold", pad=4)
        ax.text(0.5, -0.06, f"N = {n_total:,}", transform=ax.transAxes,
                ha="center", fontsize=7, color="gray")


# --------------------------------------------------------------------------- #
#  Panel C/D/E/F — Biomarker Distributions (fixed xlim)
# --------------------------------------------------------------------------- #
BIOMARKERS = [
    # (nhanes_col,        hc_col,           xlabel,           xlim,      panel)
    ("neutrophil_num",   "neutrophil_num",  "Neutrophil (×10⁹/L)",  (0, 14),   "C"),
    ("lymphocyte_num",   "lymphocyte_num",  "Lymphocyte (×10⁹/L)",  (0, 8),    "D"),
    ("platelet_num",     "platelet_num",    "Platelet (×10⁹/L)",    (50, 600), "E"),
    ("albumin_serum",    "ALB",             "Albumin (g/dL)",        (2.0, 6.0),"F"),
]


def plot_biomarker(ax, df_nhanes, df_hc, nhanes_col, hc_col, xlabel, xlim):
    n_data = df_nhanes[nhanes_col].dropna() if nhanes_col in df_nhanes.columns else pd.Series(dtype=float)
    h_data = df_hc[hc_col].dropna()       if hc_col     in df_hc.columns     else pd.Series(dtype=float)

    # Clip to xlim before histogram to remove display-distorting outliers
    xlo, xhi = xlim
    n_data = n_data[(n_data >= xlo) & (n_data <= xhi)]
    h_data = h_data[(h_data >= xlo) & (h_data <= xhi)]

    bins = np.linspace(xlo, xhi, 30)

    if len(n_data) > 0:
        ax.hist(n_data, bins=bins, density=True, alpha=0.55,
                color=COLOR_NHANES, edgecolor="white", linewidth=0.3,
                label=f"NHANES (n={len(n_data):,})")
        kde_overlay(ax, n_data, COLOR_NHANES)

    if len(h_data) > 0:
        ax.hist(h_data, bins=bins, density=True, alpha=0.55,
                color=COLOR_HC, edgecolor="white", linewidth=0.3,
                label=f"HC (n={len(h_data):,})")
        kde_overlay(ax, h_data, COLOR_HC)

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Density")
    ax.set_xlim(xlim)
    ax.legend(framealpha=0.7, loc="upper right")
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.spines[["top", "right"]].set_visible(False)


# --------------------------------------------------------------------------- #
#  Master figure assembly
# --------------------------------------------------------------------------- #
def build_figure1(df_nhanes, df_hc):
    fig = plt.figure(figsize=(14.0, 7.5))

    # Outer GridSpec: 2 rows, 2 mega-columns (A+B | C+D+E+F)
    # We use a single 2-row, 4-column gs and nest inner gridspecs
    outer = gridspec.GridSpec(
        2, 1, figure=fig,
        height_ratios=[1.15, 1.0],
        hspace=0.50,
    )

    # ---- Row 0: Age (left half) + Ethnicity (right half) ---- #
    row0 = gridspec.GridSpecFromSubplotSpec(
        1, 2, subplot_spec=outer[0], wspace=0.32
    )

    # Age: 2 sub-panels
    age_gs = gridspec.GridSpecFromSubplotSpec(
        1, 2, subplot_spec=row0[0], wspace=0.38
    )
    ax_age_n = fig.add_subplot(age_gs[0, 0])
    ax_age_h = fig.add_subplot(age_gs[0, 1])
    plot_age(ax_age_n, ax_age_h, df_nhanes, df_hc)
    panel_label(ax_age_n, "A", x=-0.18, y=1.12)

    # Ethnicity: 2 pie sub-panels
    eth_gs = gridspec.GridSpecFromSubplotSpec(
        1, 2, subplot_spec=row0[1], wspace=0.05
    )
    ax_eth_n = fig.add_subplot(eth_gs[0, 0])
    ax_eth_h = fig.add_subplot(eth_gs[0, 1])
    plot_ethnicity(ax_eth_n, ax_eth_h, df_nhanes, df_hc)
    panel_label(ax_eth_n, "B", x=-0.12, y=1.12)

    # ---- Row 1: 4 biomarker panels ---- #
    row1 = gridspec.GridSpecFromSubplotSpec(
        1, 4, subplot_spec=outer[1], wspace=0.42
    )
    for col_idx, (ncol, hcol, xlabel, xlim, letter) in enumerate(BIOMARKERS):
        ax = fig.add_subplot(row1[0, col_idx])
        plot_biomarker(ax, df_nhanes, df_hc, ncol, hcol, xlabel, xlim)
        panel_label(ax, letter, x=-0.18, y=1.08)

    # ---- Figure-level annotations ---- #
    fig.suptitle(
        "Figure 1.  Cohort Characteristics — NHANES 2017–2023 and Local Health Check 2021–2025",
        fontsize=10, fontweight="bold", y=1.005,
    )

    # Gender footnote (correct counts)
    try:
        gcol_n = resolve_col(df_nhanes, "gender", "RIAGENDR")
        if df_nhanes[gcol_n].dtype in [object, "category", "string"]:
            nm = (df_nhanes[gcol_n] == "Male").sum()
            nf = (df_nhanes[gcol_n] == "Female").sum()
        else:
            nm = (df_nhanes[gcol_n] == 1).sum()
            nf = (df_nhanes[gcol_n] == 2).sum()
        hm = (df_hc["gender"] == "Male").sum()
        hf = (df_hc["gender"] == "Female").sum()
        gender_note = (
            f"Gender — NHANES: {nm:,} male / {nf:,} female  |  "
            f"Health Check: {hm:,} male / {hf:,} female"
        )
    except Exception:
        gender_note = "Gender distribution — see Table 1."

    fig.text(
        0.5, -0.012, gender_note,
        ha="center", fontsize=7, color="#555555", style="italic",
    )

    return fig


# --------------------------------------------------------------------------- #
#  Save
# --------------------------------------------------------------------------- #
def save_figure(fig, stem: Path):
    for ext in ("pdf", "png"):
        path = stem.with_suffix(f".{ext}")
        fig.savefig(path, dpi=300, bbox_inches="tight",
                    format=ext, metadata={"Date": None} if ext == "pdf" else None)
        print(f"  Saved: {path.name}")
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Main
# --------------------------------------------------------------------------- #
def main():
    print("=" * 65)
    print("Generate Figure 1 (Grant Application) — Cohort Characteristics")
    print("=" * 65)

    print("\n[1/3] Loading data ...")
    df_nhanes = load_nhanes()
    df_hc     = load_hc()

    print("\n[2/3] Building figure ...")
    fig = build_figure1(df_nhanes, df_hc)

    print("\n[3/3] Saving ...")
    stem = OUT_DIR / "Figure1_Cohort_Characteristics_Grant"
    save_figure(fig, stem)

    print("\nDone. Output:")
    print(f"  {OUT_DIR / 'Figure1_Cohort_Characteristics_Grant.pdf'}")
    print(f"  {OUT_DIR / 'Figure1_Cohort_Characteristics_Grant.png'}")
    print("=" * 65)


if __name__ == "__main__":
    main()
