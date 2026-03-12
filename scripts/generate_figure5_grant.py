"""Generate Figure 5 for Grant Application — Trajectory & Systemic Decoupling (Aim 6).

Single-panel wrapper around the existing publication-ready composite:
  aim6/figures/Aim6_Trajectory_Decoupling_Clean.png

Layout (preserved from original):
  A  Gender-stratified age trajectories: Latent_IRI (solid, blue) vs SII (dashed, red)
  B  SII component Spearman correlations, Age < 60
  C  SII component Spearman correlations, Age >= 60
  D  Latent_IRI feature Spearman correlations, Age < 60
  E  Latent_IRI feature Spearman correlations, Age >= 60

Reads existing 300-DPI PNG — no re-running of upstream analysis required.
"""

import warnings
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------- #
#  Config
# --------------------------------------------------------------------------- #
matplotlib.rcParams.update(
    {
        "font.family": "Arial",
        "axes.unicode_minus": False,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

PROJECT  = Path(r"C:\Users\Wenxi He\projects\NHANES_Data")
AIM6_FIG = PROJECT / "aim6" / "figures"
OUT_DIR  = PROJECT / "aim6" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_PNG = AIM6_FIG / "Aim6_Trajectory_Decoupling_Clean.png"


# --------------------------------------------------------------------------- #
#  Build figure
# --------------------------------------------------------------------------- #
def build_figure5():
    fig, ax = plt.subplots(figsize=(15.0, 9.0))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.91, bottom=0.02)

    if not SOURCE_PNG.exists():
        ax.text(0.5, 0.5, f"Missing:\n{SOURCE_PNG.name}",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=10, color="red")
    else:
        img = plt.imread(str(SOURCE_PNG))
        ax.imshow(img, aspect="equal", interpolation="lanczos")

    ax.axis("off")

    fig.suptitle(
        "Figure 5.  Age-Trajectory Sensitivity and Systemic Decoupling:\n"
        "Why PCA Outperforms Fixed-Ratio Indices in Aging Populations\n"
        "(Local Health-Check Cohort, N = 96,578; NHANES 2017\u20132023)",
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
    print("Generate Figure 5 (Grant) -- Trajectory & Decoupling (Aim 6)")
    print("=" * 65)

    print("\n[1/3] Checking source panel ...")
    status = "OK" if SOURCE_PNG.exists() else "MISSING"
    print(f"  {SOURCE_PNG.name}: {status}")

    print("\n[2/3] Building figure ...")
    fig = build_figure5()

    print("\n[3/3] Saving ...")
    stem = OUT_DIR / "Figure5_Trajectory_Decoupling_Grant"
    save_figure(fig, stem)

    print("\nDone. Output:")
    print(f"  {stem}.pdf")
    print(f"  {stem}.png")
    print("=" * 65)


if __name__ == "__main__":
    main()
