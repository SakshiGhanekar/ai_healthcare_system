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
        line_color='#FF4B4B'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.2 if values else 100],
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)',
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.1)',
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=60, t=40, b=40),
        font=dict(color='#E2E8F0', size=12)
    )
    
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
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8, color='#60A5FA', line=dict(width=2, color='#1E293B')),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title=label,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            showline=False,
            tickfont=dict(size=10)
        ),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
