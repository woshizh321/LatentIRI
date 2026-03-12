"""Generate Figure 3 for Grant Application — Local Cohort Validation (Aim 5).

2x3 composite layout (row x col):
  A [0,0]  LOWESS age trajectory by sex         aim5/figures/Fig_D1a_IRI_trajectory_v2.png
  B [0,1]  Gender scissors (OLS interaction)    aim5/figures/Fig_D1b_gender_scissors_v2.png
  C [0,2]  CRP & ESR boxplots by IRI quartile   aim5/figures/Fig_D2a_CRP_ESR_boxplot_v2.png
  D [1,0]  Min-Max radar (5-domain validity)    aim5/figures/Fig_D2b_radar_chart_v2.png
  E [1,1]  Kaplan-Meier survival curves Q1-Q4   aim5/figures/Fig_D3a_KM_curve_v2.png
  F [1,2]  Cox PH forest plot (adjusted HR)     aim5/figures/Fig_D3b_Cox_forest_v2.png

Reads existing 300-DPI PNGs — no re-running of upstream analysis required.
"""

import warnings
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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
AIM5_FIG = PROJECT / "aim5" / "figures"
OUT_DIR  = PROJECT / "aim5" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Panel definitions in row-major order: (png_filename, panel_letter)
PANELS = [
    # Row 0
    ("Fig_D1a_IRI_trajectory_v2.png",   "A"),
    ("Fig_D1b_gender_scissors_v2.png",  "B"),
    ("Fig_D2a_CRP_ESR_boxplot_v2.png",  "C"),
    # Row 1
    ("Fig_D2b_radar_chart_v2.png",      "D"),
    ("Fig_D3a_KM_curve_v2.png",         "E"),
    ("Fig_D3b_Cox_forest_v2.png",       "F"),
]


# --------------------------------------------------------------------------- #
#  Helper
# --------------------------------------------------------------------------- #
def panel_label(ax, letter, x=0.01, y=0.99):
    ax.text(
        x, y, letter,
        transform=ax.transAxes,
        fontsize=12, fontweight="bold", va="top", ha="left",
    )


def imshow_panel(ax, png_path: Path, letter: str):
    """Display an existing PNG as a matplotlib axes image, no border."""
    img = plt.imread(str(png_path))
    ax.imshow(img, aspect="equal", interpolation="lanczos")
    ax.axis("off")
    panel_label(ax, letter)


# --------------------------------------------------------------------------- #
#  Master figure assembly
# --------------------------------------------------------------------------- #
def build_figure3():
    fig = plt.figure(figsize=(18.0, 11.0))

    gs = gridspec.GridSpec(
        2, 3, figure=fig,
        hspace=0.22, wspace=0.12,
        left=0.02, right=0.98,
        top=0.92, bottom=0.04,
    )

    for idx, (png_name, letter) in enumerate(PANELS):
        row, col = divmod(idx, 3)
        ax = fig.add_subplot(gs[row, col])
        png_path = AIM5_FIG / png_name
        if not png_path.exists():
            ax.text(0.5, 0.5, f"Missing:\n{png_name}",
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=8, color="red")
            ax.axis("off")
            panel_label(ax, letter)
        else:
            imshow_panel(ax, png_path, letter)

    fig.suptitle(
        "Figure 3.  Latent_IRI Construct and Predictive Validity in the Local Health-Check Cohort\n"
        "(Guangxi, China, 2021\u20132025; N = 99,873)",
        fontsize=11, fontweight="bold", y=0.975,
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
    print("Generate Figure 3 (Grant) -- Local Cohort Validation (Aim 5)")
    print("=" * 65)

    print("\n[1/3] Checking source panels ...")
    all_ok = True
    for png_name, letter in PANELS:
        p = AIM5_FIG / png_name
        status = "OK" if p.exists() else "MISSING"
        print(f"  Panel {letter}: {status}  ({png_name})")
        if not p.exists():
            all_ok = False
    if not all_ok:
        print("\n  [WARN] One or more panels missing -- placeholders will be shown.")

    print("\n[2/3] Building figure ...")
    fig = build_figure3()

    print("\n[3/3] Saving ...")
    stem = OUT_DIR / "Figure3_LocalCohort_Grant"
    save_figure(fig, stem)

    print("\nDone. Output:")
    print(f"  {stem}.pdf")
    print(f"  {stem}.png")
    print("=" * 65)


if __name__ == "__main__":
    main()
