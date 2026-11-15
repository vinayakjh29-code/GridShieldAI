
import plotly.graph_objects as go


def create_grid_topology(abnormal=False, breaker_status="CLOSED"):

    fig = go.Figure()

    nodes = [
        ("POWER PLANT", 0, 1),
        ("TRANSMISSION", 1.5, 1),
        ("SUBSTATION", 3, 1),
        ("DISTRIBUTION", 4.5, 1),
        ("CONSUMERS", 6, 1)
    ]

    line_color = "#ef4444" if abnormal else "#22c55e"

    for i in range(len(nodes) - 1):

        x1, y1 = nodes[i][1], nodes[i][2]
        x2, y2 = nodes[i + 1][1], nodes[i + 1][2]

        isolated = (
            abnormal
            and breaker_status == "OPEN"
            and i == 2
        )

        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(
                color="#ef4444" if isolated else line_color,
                width=5,
                dash="dash" if isolated else "solid"
            ),
            hoverinfo="skip",
            showlegend=False
        ))

    for name, x, y in nodes:

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            marker=dict(
                size=38,
                color="#ef4444" if abnormal else "#22c55e",
                line=dict(color="white", width=2)
            ),
            text=[name],
            textposition="bottom center",
            textfont=dict(color="white", size=11),
            hovertemplate=name + "<extra></extra>",
            showlegend=False
        ))

    fig.update_layout(
        title=dict(
            text="GRIDSHIELD AI | SMART GRID DIGITAL TWIN",
            font=dict(color="#38bdf8", size=18)
        ),
        paper_bgcolor="#081426",
        plot_bgcolor="#081426",
        font=dict(color="white"),
        height=330,
        margin=dict(l=20, r=20, t=65, b=55),
        xaxis=dict(visible=False, range=[-0.5, 6.5]),
        yaxis=dict(visible=False, range=[0.5, 1.5])
    )

    return fig
