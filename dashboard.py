import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Setup the Page ---
st.set_page_config(layout="wide")
st.title("Quantitative Investment Strategy Analysis")
st.subheader("Backtest of a 30-Day SMA Momentum Strategy on Daimler (MBG.DE)")

# --- 2. Load Data ---
# We'll use @st.cache_data to load our files only once
@st.cache_data
def load_data(file_path):
    """Loads a CSV file with date parsing."""
    try:
        df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def load_metrics(file_path):
    """Loads the metrics CSV."""
    try:
        df = pd.read_csv(file_path, index_col=0)
        return df
    except FileNotFoundError:
        return None

equity_df = load_data('equity_curve.csv')
metrics_df = load_metrics('performance_metrics.csv')

# Check if data loaded correctly
if equity_df is None or metrics_df is None:
    st.error("Error: 'equity_curve.csv' or 'performance_metrics.csv' not found.")
    st.warning("Please run 'python analyze.py' first to generate the required files.")
else:
    # --- 3. Display Performance Metrics Table ---
    st.header("Performance Analytics")
    st.markdown("A comparison of our momentum strategy against a simple 'Buy & Hold' and the S&P 500 benchmark.")

    # Format the metrics for better readability
    metrics_formatted = metrics_df.copy()
    metrics_formatted['CAGR'] = metrics_formatted['CAGR'].apply(lambda x: f"{x:.2%}")
    metrics_formatted['Sharpe Ratio'] = metrics_formatted['Sharpe Ratio'].apply(lambda x: f"{x:.2f}")
    metrics_formatted['Max Drawdown'] = metrics_formatted['Max Drawdown'].apply(lambda x: f"{x:.2%}")
    
    st.dataframe(metrics_formatted, use_container_width=True)

    # --- 4. Display Equity Curve Chart ---
    st.header("Strategy Equity Curve (Growth of $1)")
    st.markdown("This chart shows how $1 invested at the start would have grown over time.")
    
    # We use Plotly for a nice, interactive chart
    fig = px.line(
        equity_df,
        x=equity_df.index,
        y=['Strategy_Equity', 'Daimler_Equity', 'SP500_Equity'],
        title="Strategy vs. Buy & Hold vs. Benchmark (S&P 500)"
    )
    
    # Update labels for clarity
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Growth of $1",
        legend_title="Investment"
    )
    
    # Rename legend items
    new_names = {
        'Strategy_Equity': 'Momentum Strategy',
        'Daimler_Equity': 'Buy & Hold Daimler',
        'SP500_Equity': 'S&P 500 Benchmark'
    }
    fig.for_each_trace(lambda t: t.update(name=new_names[t.name]))
    
    st.plotly_chart(fig, use_container_width=True)