
# 📈 Stock Sentiment Analysis: Impact of Tweets on Stock Prices

This project explores the correlation between Twitter sentiment and stock market movements. By analyzing tweet sentiments and their temporal alignment with stock price fluctuations, we aim to determine the extent to which public opinion on social media influences financial markets.

## 🧠 Objective

To assess whether sentiment extracted from tweets mentioning specific stocks can serve as a predictor for stock price movements, thereby providing insights into market dynamics influenced by public opinion.


## 🛠️ Tools & Technologies

- **Programming Languages**: Python
- **Libraries**: pandas, NumPy, scikit-learn, TextBlob, matplotlib, seaborn
- **Data Sources**:
  - Twitter API for tweet data
  - Yahoo Finance API for stock prices

## 🔍 Methodology

1. **Data Collection**:
   - Extracted tweets mentioning target stock tickers using the Twitter API.
   - Retrieved historical stock prices corresponding to the same time frame.

2. **Data Preprocessing**:
   - Cleaned tweet text by removing URLs, mentions, hashtags, and special characters.
   - Handled missing values and ensured temporal alignment between tweets and stock prices.

3. **Sentiment Analysis**:
   - Applied TextBlob to compute sentiment polarity scores for each tweet.
   - Categorized sentiments as positive, negative, or neutral based on polarity thresholds.

4. **Correlation Analysis**:
   - Aggregated daily sentiment scores.
   - Calculated correlation coefficients between daily average sentiment and stock price changes.
   - Visualized trends and patterns to interpret the relationship.

## 📊 Results

- Identified a moderate positive correlation between tweet sentiment and stock price movements for certain stocks.
- Observed that spikes in positive sentiment often preceded stock price increases, suggesting potential predictive power.

## 🚀 How to Run

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/IamSavitha/DataWarehouse-and-Pipeline.git
   cd DataWarehouse-and-Pipeline/Group_Project/Stock_Sentiment_Analysis_tweet_impact

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt

3. **Execute Notebooks**:

Run the notebooks in the following order:

data_preprocessing.ipynb

sentiment_analysis.ipynb

correlation_analysis.ipynb

📈 Visualizations
Include plots such as:

Time series of average daily sentiment vs. stock prices.

Scatter plots showing sentiment scores against stock price changes.

Heatmaps of correlation matrices.

🤝 Contributors
Savitha Vijayarangan
Bharathi 
Jane 

📬 Contact
For questions or feedback, please contact savitha.vijayarangan09@gmail.com.


---

This `README.md` provides a clear overview of your project's purpose, structure, methodology, and results. It also guides users on how to replicate your analysis. Make sure to replace placeholder links and emails with actual information relevant to your project. Let me know if you'd like assistance with any specific section or further customization!
::contentReference[oaicite:0]{index=0}
 
