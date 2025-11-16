# Quantitative Investment Strategy Analysis

This is a Python-based framework to backtest a momentum-based trading strategy using historical stock market data for Mercedes-Benz (MBG.DE).

The goal of this project was not to find a profitable strategy, but to **build the complete system** for quantitative analysis. It proves the ability to create a data pipeline, build a backtester from scratch, and apply rigorous statistical models to evaluate performance.

## 💡 What's the Goal?

The goal of this project is to build a "time machine" for an investment idea. We want to see if a popular trading strategy called **"Momentum"** would have actually made money or lost money if we had used it over the past 10 years.

This process is called **"backtesting,"** and it helps us answer a simple question: "Is this a good strategy, or does it just sound good?"

## 🧐 What's the "Momentum" Strategy?

The idea is very simple:
* **"Buy High":** When a stock's price is trending *up* (it has positive momentum), we "buy" it, expecting it to keep going up.
* **"Sell Low":** When its price starts trending *down* (it has negative momentum), we "sell" it to protect our money.

We defined "trending up" as "the current price is higher than its 30-day average."

## 🚀 How Did We Test It?

We built a system that works in four main steps:

### Step 1: Get the Historical Data
We built a "data pipeline" that automatically downloaded 10 years of daily stock price history for **Daimler (Mercedes-Benz)** and a market benchmark (the S&P 500).

### Step 2: Build the "Time Machine"
We built a Python script that acts as our "backtester." We fed it the 10 years of stock data and gave it our "Momentum" rules. The script then simulated being a trader, going day-by-day through the last 10 years, "buying" and "selling" based on those rules and recording its profit or loss every single day.

### Step 3: Analyze the Results (Was it any good?)
Just seeing the final profit isn't enough. We also need to know *how risky* the strategy was. We wrote a script that applied statistical models to our simulation's results to calculate three key numbers:

1.  **CAGR (Growth):** How much did our money grow each year, on average?
2.  **Max Drawdown (Risk):** What was the *biggest* drop in value we had to suffer through? (A -50% drop is terrifying!)
3.  **Sharpe Ratio (Risk vs. Reward):** Did we get a good return for the amount of risk we took?

We compared these numbers for our Strategy vs. two other options: just buying and holding the stock, and buying the S&P 500.

### Step 4: Show the Final Report on a Dashboard
We built a simple, one-page website (a dashboard) that shows the results. This lets a non-technical manager or stakeholder see the answer in 30 seconds, using two simple parts:

* **A Table:** Showing the final performance numbers (Growth, Risk, etc.) side-by-side.
* **A Chart:** Visually showing how our $1 investment would have grown (or shrunk) over the 10-year period.

## 🎯 What's the Final Result?

The final product is a **data-driven analysis tool**. It takes a trading idea, tests it against history, and provides a clear, easy-to-understand report that proves whether the strategy is worth pursuing or if it's too risky.

## 📈 Dashboard Preview

https://github.com/mikaranyadav/Quantitative-Investment-Strategy-Analysis/blob/main/Dashboard.png
https://github.com/mikaranyadav/Quantitative-Investment-Strategy-Analysis/blob/main/Dashboard1.png

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

