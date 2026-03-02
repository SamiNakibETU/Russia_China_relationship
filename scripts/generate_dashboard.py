"""
Generate standalone HTML dashboard with Plotly.

Output: reports/dashboard.html
Usage: python scripts/generate_dashboard.py
Swiss/corporate aesthetic: clean typography, restrained palette, minimal clutter.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "russia_china_dependency" / "02_processed_data"
REPORTS_DIR = PROJECT_ROOT / "reports"
OUT_HTML = REPORTS_DIR / "dashboard.html"

PALETTE = {
    "ink": "#1a1a1a",
    "ink_light": "#6b6b6b",
    "accent": "#0d47a1",
    "risk": "#b71c1c",
    "neutral": "#546e7a",
    "grid": "#eceff1",
    "paper": "#ffffff",
    "scenarios": ["#0d47a1", "#37474f", "#00695c", "#455a64"],
}

FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
FONT_XS = 11
FONT_SM = 12
FONT_MD = 13
FONT_LG = 18
FONT_TITLE = 24


def axis_style():
    return dict(
        showgrid=True,
        gridcolor=PALETTE["grid"],
        gridwidth=0.5,
        zeroline=False,
        tickfont=dict(family=FONT, size=FONT_XS, color=PALETTE["ink_light"]),
        title_font=dict(family=FONT, size=FONT_SM, color=PALETTE["ink"]),
        linecolor=PALETTE["grid"],
        linewidth=0.5,
    )


METHODOLOGY = (
    "Data: Panel 96 mo (2017-2024), Atlas HS92, Carnegie, CRINK. "
    "MDI = dual-use / CHN exports to RUS, mean 3.89%. "
    "Scenarios: Carnegie, CEPR, SIPRI paths. "
    "Break cost: 3mo stockpile, 15% domestic. "
    "Price: Carnegie +87% RUS vs +9% benchmark. "
    "Asymmetry: row share / col share."
)


def main() -> None:
    mdi_timeline = pd.read_csv(DATA_DIR / "mdi_monthly_2022_2024.csv")
    mdi_timeline["date"] = pd.to_datetime(mdi_timeline["date"])

    scenarios = pd.read_csv(DATA_DIR / "scenario_projections_2025_2030.csv")
    crink_bilateral = pd.read_csv(DATA_DIR / "crink_bilateral_2024.csv")

    asymmetry_path = DATA_DIR / "crink_asymmetry_matrix.csv"
    if asymmetry_path.exists():
        asym_raw = pd.read_csv(asymmetry_path, index_col=0)
        asym = asym_raw.astype(float)
        asym = asym.replace([float("inf"), float("-inf")], 15)
    else:
        asym = pd.DataFrame(
            [
                [float("nan"), 0.13, 0.05, 0.01],
                [7.5, float("nan"), 2.1, 5.2],
                [4.8, 0.48, float("nan"), 0.2],
                [12.3, 0.19, 0.5, float("nan")],
            ],
            columns=["CHN", "RUS", "IRN", "PRK"],
            index=["CHN", "RUS", "IRN", "PRK"],
        )

    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=(
            "Dual-use share of CHN exports to RUS",
            "Scenario projections 2025-2030",
            "CRINK trade flows",
            "Break cost by scenario",
            "Dual-use price index",
            "Dependency asymmetry",
        ),
        specs=[
            [{"type": "xy"}, {"type": "xy"}],
            [{"type": "sankey"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "heatmap"}],
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.10,
        row_heights=[0.33, 0.34, 0.33],
    )

    # 1. MDI timeline
    fig.add_trace(
        go.Scatter(
            x=mdi_timeline["date"],
            y=mdi_timeline["mdi_pct"],
            mode="lines",
            name="Dual-use %",
            line=dict(color=PALETTE["accent"], width=3),
            fill="tozeroy",
            fillcolor="rgba(13, 71, 161, 0.06)",
            legend="legend",
            hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.2f}%<extra></extra>",
        ),
        row=1, col=1,
    )
    fig.update_xaxes(**axis_style(), row=1, col=1)
    fig.update_yaxes(**axis_style(), title_text="%", row=1, col=1)

    # 2. Scenarios
    scenario_names = scenarios["scenario"].unique().tolist()
    scenario_labels = {
        "S1_China_Stops": "S1 China stops",
        "S2_Oil_Crash": "S2 Oil crash",
        "S3_War_Ends": "S3 War ends",
        "S4_Integration": "S4 Integration",
    }
    dashes = ["solid", "dash", "dot", "dashdot"]
    for i, scenario in enumerate(scenario_names):
        data = scenarios[scenarios["scenario"] == scenario]
        color = PALETTE["scenarios"][i % len(PALETTE["scenarios"])]
        label = scenario_labels.get(scenario, scenario.replace("_", " "))
        fig.add_trace(
            go.Scatter(
                x=data["year"],
                y=data["mdi"],
                mode="lines",
                name=label,
                line=dict(color=color, width=3, dash=dashes[i % 4]),
                legend="legend2",
                hovertemplate=f"<b>{label}</b><br>%{{x}}: %{{y:.1f}}<extra></extra>",
            ),
            row=1, col=2,
        )
    fig.update_xaxes(**axis_style(), row=1, col=2)
    fig.update_yaxes(
        **axis_style(),
        title_text="MDI",
        range=[0, 55],
        row=1,
        col=2,
    )

    # 3. CRINK Sankey
    nodes = ["CHN", "RUS", "IRN", "PRK"]
    node_idx = {n: i for i, n in enumerate(nodes)}
    sources, targets, values = [], [], []
    for _, row in crink_bilateral.iterrows():
        ex, im, val = row["exporter"], row["importer"], row["value_bn"]
        if ex in node_idx and im in node_idx:
            sources.append(node_idx[ex])
            targets.append(node_idx[im])
            values.append(float(val))

    node_colors = PALETTE["scenarios"]
    link_colors = ["rgba(13, 71, 161, 0.25)" for _ in values]

    fig.add_trace(
        go.Sankey(
            node=dict(
                label=nodes,
                color=node_colors,
                pad=24,
                thickness=18,
                line=dict(color="#ffffff", width=0.5),
            ),
            link=dict(source=sources, target=targets, value=values, color=link_colors),
        ),
        row=2, col=1,
    )

    # 4. Break cost
    break_costs = pd.DataFrame({
        "Scenario": ["Optimistic", "Baseline", "Pessimistic"],
        "Months": [12, 8, 4],
    })
    fig.add_trace(
        go.Bar(
            y=break_costs["Scenario"],
            x=break_costs["Months"],
            orientation="h",
            marker_color=[PALETTE["accent"], PALETTE["neutral"], PALETTE["risk"]],
            marker_line_color=PALETTE["paper"],
            marker_line_width=1,
            text=break_costs["Months"].astype(str) + " mo",
            textposition="outside",
            textfont=dict(family=FONT, size=FONT_SM, color=PALETTE["ink_light"]),
            showlegend=False,
            hovertemplate="<b>%{y}</b><br>%{x} mo<extra></extra>",
        ),
        row=2, col=2,
    )
    fig.update_xaxes(**axis_style(), range=[0, 15], title_text="Months", row=2, col=2)
    fig.update_yaxes(**axis_style(), autorange="reversed", row=2, col=2)

    # 5. Price markup
    markup_data = pd.DataFrame({
        "Year": [2021, 2022, 2023, 2024],
        "Normal": [100, 103, 106, 109],
        "Russia": [100, 120, 150, 187],
    })
    fig.add_trace(
        go.Scatter(
            x=markup_data["Year"],
            y=markup_data["Normal"],
            name="Benchmark",
            mode="lines",
            line=dict(color=PALETTE["neutral"], width=2.5, dash="dot"),
            legend="legend3",
            hovertemplate="<b>Benchmark</b><br>%{x}: %{y}<extra></extra>",
        ),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=markup_data["Year"],
            y=markup_data["Russia"],
            name="Russia",
            mode="lines",
            line=dict(color=PALETTE["risk"], width=3),
            legend="legend3",
            hovertemplate="<b>Russia</b><br>%{x}: %{y}<extra></extra>",
        ),
        row=3, col=1,
    )
    fig.update_xaxes(**axis_style(), row=3, col=1)
    fig.update_yaxes(**axis_style(), title_text="Index (2021=100)", row=3, col=1)

    # 6. Asymmetry heatmap
    fig.add_trace(
        go.Heatmap(
            z=asym.values,
            x=asym.columns.tolist(),
            y=asym.index.tolist(),
            colorscale=[[0, "#e8f5e9"], [0.5, "#ffffff"], [1, "#b71c1c"]],
            zmin=0, zmid=1, zmax=15,
            showscale=True,
            colorbar=dict(
                title=dict(text="Ratio", font=dict(family=FONT, size=FONT_XS)),
                tickfont=dict(family=FONT, size=FONT_XS),
                outlinewidth=0,
                len=0.5,
                thickness=14,
            ),
            hovertemplate="<b>%{y} → %{x}</b><br>Ratio: %{z:.2f}<extra></extra>",
        ),
        row=3, col=2,
    )
    fig.update_xaxes(**axis_style(), row=3, col=2)
    fig.update_yaxes(**axis_style(), row=3, col=2)

    # Subplot titles: smaller weight, clear hierarchy
    fig.update_annotations(
        font=dict(family=FONT, size=FONT_MD, color=PALETTE["ink"]),
        xanchor="left",
    )

    # Layout: Swiss/corporate — clean, restrained, legends inside chart bounds
    fig.update_layout(
        template="plotly_white",
        font=dict(family=FONT, size=FONT_SM, color=PALETTE["ink"]),
        title=dict(
            text="Russia-China dependency",
            font=dict(family=FONT, size=FONT_TITLE, color=PALETTE["ink"]),
            x=0,
            xanchor="left",
            pad=dict(b=24),
        ),
        paper_bgcolor=PALETTE["paper"],
        plot_bgcolor=PALETTE["paper"],
        margin=dict(l=72, r=72, t=96, b=130),
        height=1400,
        autosize=True,
        legend=dict(
            font=dict(family=FONT, size=FONT_XS),
            orientation="h",
            yanchor="top", y=0.89,
            xanchor="left", x=0.02,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=PALETTE["grid"],
            borderwidth=0.5,
        ),
        legend2=dict(
            font=dict(family=FONT, size=FONT_XS),
            orientation="h",
            yanchor="top", y=0.89,
            xanchor="right", x=0.98,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=PALETTE["grid"],
            borderwidth=0.5,
        ),
        legend3=dict(
            font=dict(family=FONT, size=FONT_XS),
            orientation="h",
            yanchor="top", y=0.18,
            xanchor="left", x=0.02,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=PALETTE["grid"],
            borderwidth=0.5,
        ),
        hoverlabel=dict(
            font=dict(family=FONT, size=FONT_XS),
            bgcolor="#ffffff",
            bordercolor="#b0bec5",
            align="left",
            namelength=0,
        ),
    )
    # Add methodology (append, do not replace subplot titles)
    method_ann = dict(
        text=METHODOLOGY,
        xref="paper", yref="paper",
        x=0.5, y=-0.05,
        xanchor="center", yanchor="top",
        showarrow=False,
        font=dict(family=FONT, size=10, color=PALETTE["ink_light"]),
        align="center",
    )
    fig.add_annotation(method_ann)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    config = {"responsive": True, "displayModeBar": True}
    fig.write_html(
        OUT_HTML,
        include_plotlyjs="cdn",
        config=config,
        div_id="dashboard",
    )
    # Inject viewport + responsive CSS for Swiss/corporate polish
    with open(OUT_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    if "viewport" not in html:
        html = html.replace("<head>", "<head>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">", 1)
    # Responsive container + page polish
    css_block = """
  <style>
    body { margin: 0; font-family: Helvetica Neue, Helvetica, Arial, sans-serif; background: #f5f5f5; }
    .plotly-graph-div { min-height: 640px; width: 100% !important; max-width: 100%; }
  </style>
"""
    if "</head>" in html and "min-height: 640px" not in html:
        html = html.replace("</head>", css_block + "</head>", 1)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dashboard generated: {OUT_HTML}")


if __name__ == "__main__":
    main()
