# Quantitative Investment Strategy Analysis

This is a Python-based framework to backtest a momentum-based trading strategy using historical stock market data for Mercedes-Benz (MBG.DE).

The goal of this project was not to find a profitable strategy, but to **build the complete system** for quantitative analysis. It proves the ability to create a data pipeline, build a backtester from scratch, and apply rigorous statistical models to evaluate performance.

## 📈 Dashboard Preview

**[YOUR-SCREENSHOT-HERE]**

## 🛠️ Tech Stack
* **Data Pipeline:** `yfinance`
* **Backtesting & Analysis:** `pandas` & `numpy`
* **Dashboard:** `Streamlit` & `Plotly`

## 🚀 How to Run This Project

1.  **Clone or download** this repository.
2.  **Create a virtual environment** and install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the full pipeline** in order. The dashboard will *not* work until the data is generated.
    ```bash
    # Step 1: Download the historical stock data
    python download_data.py

    # Step 2: Run the backtest and generate strategy returns
    python backtest.py

    # Step 3: Analyze the performance and calculate metrics
    python analyze.py
    ```
4.  **Run the dashboard!**
    ```bash
    streamlit run dashboard.py
    ```