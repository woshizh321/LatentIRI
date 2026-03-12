"""Generate Figure 6 for Grant Application — Chronic Disease Protection (Aim 7).

1x2 composite layout:
  A [0,0]  Chronic disease OR forest plot (5 conditions)
           aim7/figures/Aim7_Disease_Protection_Forest.png
  B [0,1]  Cancer / malignancy prevalence by IRI quartile
           aim7/figures/Aim7_Cancer_Quartile_Prevalence.png

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
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

PROJECT  = Path(r"C:\Users\Wenxi He\projects\NHANES_Data")
AIM7_FIG = PROJECT / "aim7" / "figures"
OUT_DIR  = PROJECT / "aim7" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PANELS = [
    ("Aim7_Disease_Protection_Forest.png",    "A"),
    ("Aim7_Cancer_Quartile_Prevalence.png",   "B"),
]


# --------------------------------------------------------------------------- #
#  Helper
# --------------------------------------------------------------------------- #
def panel_label(ax, letter, x=0.01, y=0.99):
    ax.text(
        x, y, letter,
        transform=ax.transAxes,
        fontsize=13, fontweight="bold", va="top", ha="left",
    )


def imshow_panel(ax, png_path: Path, letter: str):
    img = plt.imread(str(png_path))
    ax.imshow(img, aspect="equal", interpolation="lanczos")
    ax.axis("off")
    panel_label(ax, letter)


# --------------------------------------------------------------------------- #
#  Master figure assembly
# --------------------------------------------------------------------------- #
def build_figure6():
    fig = plt.figure(figsize=(14.0, 6.5))

    gs = gridspec.GridSpec(
        1, 2, figure=fig,
        width_ratios=[1.35, 1.0],
        wspace=0.08,
        left=0.02, right=0.98,
        top=0.90, bottom=0.03,
    )

    for idx, (png_name, letter) in enumerate(PANELS):
        ax = fig.add_subplot(gs[0, idx])
        png_path = AIM7_FIG / png_name
        if not png_path.exists():
            ax.text(0.5, 0.5, f"Missing:\n{png_name}",
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=9, color="red")
            ax.axis("off")
            panel_label(ax, letter)
        else:
            imshow_panel(ax, png_path, letter)

    fig.suptitle(
        "Figure 6.  Latent_IRI and Chronic Disease Risk Across Pathological Categories\n"
        "(Weighted Logistic Regression, NHANES 2017\u20132018, Age \u2265 20, N \u2248 4,820)",
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
    print("Generate Figure 6 (Grant) -- Chronic Disease Protection (Aim 7)")
    print("=" * 65)

    print("\n[1/3] Checking source panels ...")
    all_ok = True
    for png_name, letter in PANELS:
        p = AIM7_FIG / png_name
        status = "OK" if p.exists() else "MISSING"
        print(f"  Panel {letter}: {status}  ({png_name})")
        if not p.exists():
            all_ok = False
    if not all_ok:
        print("\n  [WARN] One or more panels missing -- placeholders will be shown.")

    print("\n[2/3] Building figure ...")
    fig = build_figure6()

    print("\n[3/3] Saving ...")
    stem = OUT_DIR / "Figure6_DiseaseProtection_Grant"
    save_figure(fig, stem)

    print("\nDone. Output:")
    print(f"  {stem}.pdf")
    print(f"  {stem}.png")
    print("=" * 65)


if __name__ == "__main__":
    main()
