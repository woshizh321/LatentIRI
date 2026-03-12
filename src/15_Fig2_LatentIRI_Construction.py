"""Generate Figure 2 for Grant Application — Latent_IRI Construction.

2x2 composite layout:
  A  Survey-weighted correlation matrix (reuse aim4/figures/Fig1_correlation_heatmap.png)
  B  PCA scree plot                     (reuse aim4/figures/Fig2_scree_plot.png)
  C  PC1 loadings bar chart             (reuse aim4/figures/Fig3_pc1_loadings.png)
  D  Latent_IRI score distribution with quartile shading (new, from locked dataset)

Reads existing 300-DPI PNGs for A/B/C — no need to rerun original scripts.
"""

import warnings
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------- #
#  Config
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

PROJECT  = Path(r"C:\Users\Wenxi He\projects\NHANES_Data")
AIM4_FIG = PROJECT / "aim4" / "figures"
OUT_DIR  = PROJECT / "aim4" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
#  Helper
# --------------------------------------------------------------------------- #
def panel_label(ax, letter, x=-0.10, y=1.06):
    ax.text(x, y, letter, transform=ax.transAxes,
            fontsize=12, fontweight="bold", va="top", ha="left")


def imshow_panel(ax, png_path: Path, letter: str):
    """Display an existing PNG as a matplotlib axes image, no border."""
    img = plt.imread(str(png_path))
    ax.imshow(img, aspect="equal", interpolation="lanczos")
    ax.axis("off")
    panel_label(ax, letter, x=0.01, y=0.99)


# --------------------------------------------------------------------------- #
#  Panel D — Latent_IRI score distribution
# --------------------------------------------------------------------------- #
QUARTILE_COLORS = ["#D94F3D", "#F0A500", "#5B9BD5", "#2E7D32"]
QUARTILE_LABELS = ["Q1 — Low\nResilience", "Q2", "Q3", "Q4 — High\nResilience"]


def plot_iri_distribution(ax, df: pd.DataFrame):
    scores = df["Latent_IRI"].dropna().values
    q1, q2, q3 = np.percentile(scores, [25, 50, 75])
    iqr = q3 - q1
    # Clip to IQR-based fence to suppress extreme outliers
    xmin = max(scores.min(), q1 - 4.0 * iqr)
    xmax = min(scores.max(), q3 + 4.0 * iqr)
    scores = scores[(scores >= xmin) & (scores <= xmax)]

    # Quartile background shading
    boundaries = [xmin, q1, q2, q3, xmax]
    for i in range(4):
        ax.axvspan(boundaries[i], boundaries[i + 1],
                   color=QUARTILE_COLORS[i], alpha=0.12, zorder=0)

    # Histogram
    ax.hist(scores, bins=55, density=True, color="#4A6FA5",
            edgecolor="white", linewidth=0.3, alpha=0.75, zorder=1)

    # KDE curve
    kde = gaussian_kde(scores)
    xr = np.linspace(xmin, xmax, 400)
    ax.plot(xr, kde(xr), color="#1a1a2e", linewidth=1.6, zorder=2)

    # Quartile boundary lines
    for q, label in zip([q1, q2, q3], ["Q1", "Q2\n(Median)", "Q3"]):
        ax.axvline(q, color="#555555", linestyle="--", linewidth=0.9, zorder=3)
        ax.text(q, ax.get_ylim()[1] * 0.01, label,
                ha="center", va="bottom", fontsize=6.5, color="#555555",
                transform=ax.get_xaxis_transform())

    # Annotation: mean ± SD
    ax.text(0.97, 0.95,
            f"N = {len(scores):,}\nMean = {scores.mean():.2f}\nSD = {scores.std():.2f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=7, color="#333333",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", lw=0.7))

    # Legend patches
    patches = [
        mpatches.Patch(color=QUARTILE_COLORS[i], alpha=0.45, label=QUARTILE_LABELS[i])
        for i in range(4)
    ]
    ax.legend(handles=patches, fontsize=6.2, loc="upper left",
              framealpha=0.8, ncol=2, handlelength=1.2, columnspacing=0.8)

    ax.set_xlabel("Latent_IRI Score (PC1, arbitrary units)")
    ax.set_ylabel("Density")
    ax.set_title("Latent_IRI Score Distribution\n(NHANES 2017–2023, N = 15,378)",
                 fontweight="bold", pad=4)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.spines[["top", "right"]].set_visible(False)

    panel_label(ax, "D", x=-0.12, y=1.06)


# --------------------------------------------------------------------------- #
#  Master figure assembly
# --------------------------------------------------------------------------- #
def build_figure2():
    fig = plt.figure(figsize=(13.5, 9.5))

    gs = gridspec.GridSpec(
        2, 2, figure=fig,
        hspace=0.30, wspace=0.22,
        left=0.04, right=0.97,
        top=0.92, bottom=0.06,
    )

    # ---- A: correlation heatmap ---- #
    ax_a = fig.add_subplot(gs[0, 0])
    imshow_panel(ax_a, AIM4_FIG / "Fig1_correlation_heatmap.png", "A")

    # ---- B: scree plot ---- #
    ax_b = fig.add_subplot(gs[0, 1])
    imshow_panel(ax_b, AIM4_FIG / "Fig2_scree_plot.png", "B")

    # ---- C: PC1 loadings ---- #
    ax_c = fig.add_subplot(gs[1, 0])
    imshow_panel(ax_c, AIM4_FIG / "Fig3_pc1_loadings.png", "C")

    # ---- D: Latent_IRI distribution (new) ---- #
    ax_d = fig.add_subplot(gs[1, 1])
    df = pd.read_parquet(
        PROJECT / "aim4" / "data" / "nhanes_latent_iri_locked.parquet"
    )
    plot_iri_distribution(ax_d, df)

    # ---- Figure title ---- #
    fig.suptitle(
        "Figure 2.  Construction of the Latent Immune Resilience Index (Latent_IRI)\n"
        "via Survey-Weighted Principal Component Analysis (NHANES 2017\u20132023)",
        fontsize=10, fontweight="bold", y=0.985,
    )

    return fig


# --------------------------------------------------------------------------- #
#  Save
# --------------------------------------------------------------------------- #
def save_figure(fig, stem: Path):
    for ext in ("pdf", "png"):
        path = stem.with_suffix(f".{ext}")
        kw = dict(dpi=300, bbox_inches="tight", format=ext)
        if ext == "pdf":
            kw["metadata"] = {"Date": None}
        fig.savefig(path, **kw)
        print(f"  Saved: {path.name}")
    plt.close(fig)


# --------------------------------------------------------------------------- #
#  Main
# --------------------------------------------------------------------------- #
def main():
    print("=" * 65)
    print("Generate Figure 2 (Grant) — Latent_IRI Construction")
    print("=" * 65)

    print("\n[1/2] Building figure ...")
    fig = build_figure2()

    print("\n[2/2] Saving ...")
    stem = OUT_DIR / "Figure2_LatentIRI_Construction_Grant"
    save_figure(fig, stem)

    print("\nDone. Output:")
    print(f"  {stem}.pdf")
    print(f"  {stem}.png")
    print("=" * 65)


if __name__ == "__main__":
    main()
