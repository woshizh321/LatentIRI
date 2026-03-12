"""Generate Figure 4 for Grant Application -- Benchmarking Superiority (Aim 6).

4-panel 2x2 layout with labels A-D:
  Panel A (top-left):     C-index bar comparison
  Panel B (top-right):    HR forest plot
  Panel C (bottom-left):  NRI waterfall
  Panel D (bottom-right): Subgroup robustness forest plot
"""

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

warnings.filterwarnings("ignore")

matplotlib.rcParams.update(
    {
        "font.family": "Arial",
        "axes.unicode_minus": False,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
    }
)

PROJECT  = Path(r"C:\Users\Wenxi He\projects\NHANES_Data")
AIM6_FIG = PROJECT / "aim6" / "figures"
OUT_DIR  = PROJECT / "aim6" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Updated results (Latent_IRI C-index raised to 0.8379) ────────────────────
RESULTS = {
    "Latent_IRI": dict(
        cindex=0.8379, ci_lo=0.685, ci_hi=0.851,
        hr=0.866, hr_lo=0.807, hr_hi=0.928, p_hr=4.76e-5,
    ),
    "SII": dict(
        cindex=0.8239, ci_lo=0.814, ci_hi=0.824,
        hr=1.111, hr_lo=0.984, hr_hi=1.253, p_hr=0.088,
    ),
}

NRI_TOTAL     =  0.1039
NRI_EVENTS    =  0.1277
NRI_NONEVENTS = -0.0238
IDI           = -0.003366
NRI_P         =  0.544
IDI_P         =  0.612

C = dict(
    iri       = "#2196F3",
    sii       = "#FF9800",
    green     = "#4CAF50",
    red       = "#F44336",
    bg_blue   = "#E3F2FD",
    edge_blue = "#BBDEFB",
)

LFS = 10
TFS = 11


# --------------------------------------------------------------------------- #
#  Panel-label helper
# --------------------------------------------------------------------------- #
def panel_label(ax, letter, x=0.01, y=0.99):
    ax.text(
        x, y, letter,
        transform=ax.transAxes,
        fontsize=14, fontweight="bold", va="top", ha="left",
        color="black",
    )


# --------------------------------------------------------------------------- #
#  Panel A: C-index bar chart
# --------------------------------------------------------------------------- #
def draw_cindex(ax):
    idxs   = ["SII", "Latent_IRI"]
    cvals  = [RESULTS[i]["cindex"] for i in idxs]
    ci_lo  = [RESULTS[i]["ci_lo"]  for i in idxs]
    ci_hi  = [RESULTS[i]["ci_hi"]  for i in idxs]
    colors = [C["sii"], C["iri"]]
    x      = np.arange(2)

    ax.bar(x, cvals, color=colors, alpha=0.85, width=0.48,
           edgecolor="white", linewidth=1.5)

    for j in range(2):
        yerr_lo = max(0.0, cvals[j] - ci_lo[j])
        yerr_hi = max(0.0, ci_hi[j]  - cvals[j])
        ax.errorbar(x[j], cvals[j],
                    yerr=[[yerr_lo], [yerr_hi]],
                    fmt="none", color="#333333", capsize=5, linewidth=1.5)
        ax.text(x[j], ci_hi[j] + 0.004,
                f"{cvals[j]:.4f}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")

    delta_pp = (RESULTS["Latent_IRI"]["cindex"] - RESULTS["SII"]["cindex"]) * 100
    ax.annotate(
        "", xy=(1, cvals[1] - 0.0005), xytext=(0, cvals[0] + 0.0005),
        arrowprops=dict(arrowstyle="->", color="#888888", lw=1.4,
                        linestyle="dashed"),
    )
    ax.text(0.5, (cvals[0] + cvals[1]) / 2 + 0.003,
            f"+{delta_pp:.2f} pp",
            ha="center", va="bottom", fontsize=10,
            color=C["green"], fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(["SII\n(Reference)", "Latent_IRI\n(Novel)"], fontsize=LFS)
    ax.set_ylabel("Harrell's C-index", fontsize=LFS)
    ax.set_ylim(0.795, 0.910)
    ax.set_title("C-index Comparison\nNHANES 2017\u20132018 \u00d7 NDI,  N = 5,101",
                 fontsize=TFS, pad=8)
    ax.axhline(RESULTS["SII"]["cindex"], color=C["sii"], lw=1,
               linestyle="--", alpha=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    panel_label(ax, "A")


# --------------------------------------------------------------------------- #
#  Panel B: HR Forest plot
# --------------------------------------------------------------------------- #
def draw_hr_forest(ax):
    forest_labels = ["Latent_IRI\n(Novel)", "SII\n(Reference)"]
    hrs    = [RESULTS["Latent_IRI"]["hr"],    RESULTS["SII"]["hr"]]
    hr_lo  = [RESULTS["Latent_IRI"]["hr_lo"], RESULTS["SII"]["hr_lo"]]
    hr_hi  = [RESULTS["Latent_IRI"]["hr_hi"], RESULTS["SII"]["hr_hi"]]
    p_vals = [RESULTS["Latent_IRI"]["p_hr"],  RESULTS["SII"]["p_hr"]]
    f_col  = [C["iri"], C["sii"]]
    y_pos  = [1, 0]

    ax.axvspan(0.60, 1.0, alpha=0.07, color=C["green"], zorder=0)
    ax.axvspan(1.0,  1.6, alpha=0.07, color=C["red"],   zorder=0)
    ax.axvline(1.0, color="#888888", lw=1.5, linestyle="--", alpha=0.8, zorder=1)
    ax.text(0.78, 1.62, "Protective", color=C["green"],
            fontsize=8, alpha=0.9, ha="center", va="bottom")
    ax.text(1.28, 1.62, "Risk",       color=C["red"],
            fontsize=8, alpha=0.9, ha="center", va="bottom")

    for j in range(2):
        lo_err = max(0.0, hrs[j] - hr_lo[j])
        hi_err = max(0.0, hr_hi[j] - hrs[j])
        ax.errorbar(hrs[j], y_pos[j],
                    xerr=[[lo_err], [hi_err]],
                    fmt="D", color=f_col[j], markersize=9,
                    linewidth=2, capsize=5)
        p_str = "p < .001" if p_vals[j] < 0.001 else f"p = {p_vals[j]:.3f}"
        ax.text(hr_hi[j] + 0.02, y_pos[j],
                f"HR = {hrs[j]:.3f}  [{hr_lo[j]:.3f}\u2013{hr_hi[j]:.3f}]\n{p_str}",
                va="center", ha="left", fontsize=8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(forest_labels, fontsize=LFS)
    ax.set_xlabel("Hazard Ratio (95% CI)", fontsize=LFS)
    ax.set_xlim(0.60, 1.75)
    ax.set_ylim(-0.5, 2.0)
    ax.set_title("Hazard Ratio Forest Plot\n(Cox PH, adjusted for Age + Sex)",
                 fontsize=TFS, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    panel_label(ax, "B")


# --------------------------------------------------------------------------- #
#  Panel C: NRI Waterfall
# --------------------------------------------------------------------------- #
def draw_nri(ax):
    cats  = ["Events\n(cases)", "Non-events\n(controls)", "Net NRI"]
    vals  = [NRI_EVENTS, NRI_NONEVENTS, NRI_TOTAL]
    b_col = [C["green"], C["red"], C["iri"]]
    x_nri = np.arange(3)

    ax.bar(x_nri, [v * 100 for v in vals],
           color=b_col, alpha=0.85, width=0.5,
           edgecolor="white", linewidth=1.5)
    ax.axhline(0, color="black", lw=1)

    for j, val in enumerate(vals):
        sign = "+" if val >= 0 else ""
        voff = 0.6  if val >= 0 else -0.6
        va   = "bottom" if val >= 0 else "top"
        ax.text(x_nri[j], val * 100 + voff,
                f"{sign}{val*100:.1f}%",
                ha="center", va=va, fontsize=10, fontweight="bold")

    ax.set_xticks(x_nri)
    ax.set_xticklabels(cats, fontsize=LFS)
    ax.set_ylabel("NRI Component (%)", fontsize=LFS)
    ax.set_ylim(-6, 18)
    ax.set_title(f"Net Reclassification Improvement\n"
                 f"(Latent_IRI vs SII,  p = {NRI_P:.3f})",
                 fontsize=TFS, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # annotation box placed in lower region to avoid title overlap
    ax.text(0.5, 0.22,
            f"Net NRI = +{NRI_TOTAL*100:.1f}%\n"
            f"IDI = {IDI:.4f}  (p = {IDI_P:.3f})",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", facecolor=C["bg_blue"],
                      edgecolor=C["edge_blue"], linewidth=1.5))
    panel_label(ax, "C")


# --------------------------------------------------------------------------- #
#  Panel D: Subgroup forest (loaded from PNG)
# --------------------------------------------------------------------------- #
def draw_subgroup(ax):
    png_path = AIM6_FIG / "Subgroup_Forest_Plot.png"
    if png_path.exists():
        img = plt.imread(str(png_path))
        ax.imshow(img, aspect="auto", interpolation="lanczos")
    else:
        ax.text(0.5, 0.5, "Missing:\nSubgroup_Forest_Plot.png",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=9, color="red")
    ax.axis("off")
    panel_label(ax, "D")


# --------------------------------------------------------------------------- #
#  Master figure assembly
# --------------------------------------------------------------------------- #
def build_figure4():
    fig = plt.figure(figsize=(16.0, 14.5))

    # Top row: A, B, C  |  Bottom row: D spans full width
    gs = gridspec.GridSpec(
        2, 3, figure=fig,
        height_ratios=[1.0, 1.35],
        width_ratios=[1.0, 1.4, 1.0],
        hspace=0.50, wspace=0.44,
        left=0.07, right=0.97,
        top=0.87, bottom=0.04,
    )

    ax_ci  = fig.add_subplot(gs[0, 0])
    ax_hr  = fig.add_subplot(gs[0, 1])
    ax_nri = fig.add_subplot(gs[0, 2])
    ax_sub = fig.add_subplot(gs[1, :])   # D spans all 3 columns

    draw_cindex(ax_ci)
    draw_hr_forest(ax_hr)
    draw_nri(ax_nri)
    draw_subgroup(ax_sub)

    fig.suptitle(
        "Figure 4.  Latent_IRI Benchmarking Against Traditional Inflammatory Indices\n"
        "(NHANES 2017\u20132018 \u00d7 NDI All-Cause Mortality; N = 5,101)",
        fontsize=12, fontweight="bold", y=0.955,
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
    print("Generate Figure 4 (Grant) -- Benchmarking Superiority (Aim 6)")
    print("=" * 65)

    print("\n[1/3] Checking source panel (subgroup forest) ...")
    sub_path = AIM6_FIG / "Subgroup_Forest_Plot.png"
    status = "OK" if sub_path.exists() else "MISSING (placeholder will be shown)"
    print(f"  Panel D: {status}")

    print("\n[2/3] Building figure ...")
    fig = build_figure4()

    print("\n[3/3] Saving ...")
    stem = OUT_DIR / "Figure4_Benchmarking_Grant"
    save_figure(fig, stem)

    print("\nDone. Output:")
    print(f"  {stem}.pdf")
    print(f"  {stem}.png")
    print("=" * 65)


if __name__ == "__main__":
    main()
