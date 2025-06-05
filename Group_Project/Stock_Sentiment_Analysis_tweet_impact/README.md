# 📈 Stock Sentiment Analysis: Assessing the Impact of Tweets on Stock Prices

This project investigates the relationship between Twitter sentiment and fluctuations in stock prices. By aligning tweet sentiment data with stock market activity, we aim to understand how public opinion on social media may influence financial trends.

---

## 🧠 Objective

To evaluate whether sentiments expressed in tweets mentioning specific stocks can predict corresponding stock price movements, offering insights into the influence of public sentiment on market behavior.

---

## 🛠️ Tools & Technologies

* **Programming Language**: Python
* **Libraries**: `pandas`, `NumPy`, `scikit-learn`, `TextBlob`, `matplotlib`, `seaborn`
* **Data Sources**:

  * Twitter API (for tweet data)
  * Yahoo Finance API (for historical stock prices)

---

## 🔍 Methodology

1. **Data Collection**

   * Gathered tweets referencing target stock tickers using the Twitter API.
   * Retrieved corresponding stock price data from Yahoo Finance.

2. **Data Preprocessing**

   * Cleaned tweets by removing noise such as URLs, mentions, hashtags, and special characters.
   * Addressed missing values and ensured time alignment between tweet and price data.

3. **Sentiment Analysis**

   * Used TextBlob to compute sentiment polarity for each tweet.
   * Classified tweets as positive, negative, or neutral based on polarity thresholds.

4. **Correlation Analysis**

   * Aggregated sentiment scores on a daily basis.
   * Calculated correlation coefficients between average daily sentiment and daily stock price changes.
   * Visualized patterns to interpret potential relationships.

---

## 📊 Results

* **Report**: `Datawarehouse-and-Pipeline/Group_Project/Stock_Sentiment_Analysis_tweet_impact/groupproject_report.pdf`
* **Presentation**: `Datawarehouse-and-Pipeline/Group_Project/Stock_Sentiment_Analysis_tweet_impact/Data 226 Presentation.pdf`
* Discovered a **moderate positive correlation** between tweet sentiment and stock price changes for select stocks.
* Noted that spikes in positive sentiment often **preceded stock price increases**, indicating potential predictive value.

---

## 🚀 How to Run the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/IamSavitha/DataWarehouse-and-Pipeline.git
   cd DataWarehouse-and-Pipeline/Group_Project/Stock_Sentiment_Analysis_tweet_impact
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Project**:

   * **With Airflow**:

     * Start Docker and run:

       ```bash
       docker-compose up
       ```
     * Access the Airflow UI, trigger the DAG to run the Python scripts, and store results.
     * Optionally, schedule the DAG to run at specified intervals.
   * **Without Airflow**:

     * Run the Python script(s) manually to execute the ETL pipeline.

4. **Transform and Load Data (ELT)**:

   * After ETL, use **DBT** to transform and load data into the warehouse.
   * Can be triggered manually or scheduled via Airflow.

5. **Query and Visualization**:

   * Use SQL queries in the DBT `models` folder to retrieve final outputs.
   * Visualize results using tools like **Tableau**, **Power BI**, or **Apache Superset**.

---

## 📈 Visualizations

* Time series plots: Average daily sentiment vs. stock prices
* Scatter plots: Sentiment scores vs. stock price changes
* Correlation heatmaps: Sentiment metrics and price trends

---

## 📬 Contact

For questions or feedback, please contact: **[savitha.vijayarangan09@gmail.com](mailto:savitha.vijayarangan09@gmail.com)**

---

Let me know if you'd like a shortened version or one formatted for a GitHub `README.md`.
