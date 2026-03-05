import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def render_radar_chart(input_data: dict):
    """
    Renders a Radar Chart comparing User's Inputs vs 'Safe' Baselines or Max Limits.
    """
    # Normalize keys/values for display
    # Filter out non-numeric
    categories = []
    values = []
    
    for k, v in input_data.items():
        if isinstance(v, (int, float)) and v > 0 and 'gender' not in k.lower():
            categories.append(k.replace('_', ' ').title())
            values.append(v)
            
    if not categories:
        st.info("Not enough data for Radar Chart")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Status',
        line=dict(color='#0EA5E9', width=4),
        fillcolor='rgba(14, 165, 233, 0.3)',
        marker=dict(color='#00f2ff', size=10, line=dict(width=2, color='#ffffff'))
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.2 if values else 100],
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0',
                tickfont=dict(color='#64748B', size=10),
            ),
            angularaxis=dict(
                gridcolor='#e2e8f0',
                linecolor='#e2e8f0',
                tickfont=dict(color='#0f172a', size=11, weight='bold'),
            ),
            bgcolor='rgba(255, 255, 255, 0.5)' 
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=40, b=40),
        font=dict(color='#0f172a', family='Manrope, sans-serif'),
        template='plotly_white'
    )
    # Add a rounded border effect via HTML container if possible, but let's stick to Plotly layout
    
    st.plotly_chart(fig, use_container_width=True)

def render_trend_chart(records: list, metric_key: str, label: str):
    """
    Renders a Line Chart for a specific metric over time.
    records: List of dicts from api.fetch_records()
    """
    if not records:
        st.info("No historical data for trends.")
        return

    # Extract Data
    dates = []
    values = []
    
    import json
    for r in records:
        try:
            d = json.loads(r['data'])
            if metric_key in d:
                dates.append(r['timestamp'])
                values.append(d[metric_key])
        except:
            continue
            
    if not dates:
        st.warning(f"No data found for {label}")
        return
        
    df = pd.DataFrame({"Date": dates, label: values})
    # Sort by date
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    
    fig = px.line(df, x="Date", y=label, markers=True)
    
    fig.update_traces(
        line=dict(color='#22d3ee', width=4),
        marker=dict(size=12, color='#ffffff', line=dict(width=3, color='#0ea5e9')),
        fill='tozeroy',
        fillcolor='rgba(34, 211, 238, 0.15)'
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title=label,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#0f172a', family='Manrope, sans-serif'),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#e2e8f0',
            tickfont=dict(size=11, color='#64748B')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=False,
            tickfont=dict(size=11, color='#64748B')
        ),
        hovermode="x unified",
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
