Here’s a **developer-ready specification** based on our discussion, structured for immediate implementation:

---

### **Project Name:** Magic Formula Daily Digest  
**Core Purpose:** A personal task automation agent that scans US markets daily for stocks meeting Joel Greenblatt’s Magic Formula criteria, aggregates relevant news, and delivers a text-based email summary.  

---

### **Functional Requirements**  
1. **Data Collection**  
   - **Stock Data** (via Alpha Vantage Free API):  
     - Fetch daily:  
       - Stock price (closing price and % change).  
       - Earnings Yield = EBIT / Enterprise Value.  
       - Return on Capital = EBIT / (Net Fixed Assets + Working Capital).  
     - Focus: All US-listed stocks (NYSE, NASDAQ).  
   - **News Data** (via NewsAPI/GNews Free Tier):  
     - Fetch headlines from *reputable sources* (e.g., Bloomberg, Reuters, CNBC).  
     - Filter for companies meeting Magic Formula criteria.  
     - Include source citations (e.g., "Reuters: [Headline]").  

2. **Data Processing**  
   - **Magic Formula Ranking:**  
     - Rank stocks by combined metrics (earnings yield + return on capital).  
     - Daily update: Recalculate rankings and identify new entries.  
   - **News Filtering:**  
     - Prioritize headlines related to earnings, mergers, regulatory changes, or significant price movements.  

3. **Summary Generation**  
   - **Daily Email Includes:**  
     - **Top 10 Stocks:**  
       - Table with columns: Ticker, Price, % Change (1D), Earnings Yield, Return on Capital.  
       - Brief explanation: *“AAPL ranks #1 due to a 12% earnings yield and 18% ROC.”*  
     - **Relevant News:**  
       - Bullet points with headlines and sources.  
     - **Recommendations:**  
       - Action items: *“Consider researching AAPL further – ranked #1 for 3 consecutive days.”*  

4. **Email Delivery**  
   - **SMTP Integration:**  
     - Send plain-text email with simple HTML tables (no CSS/images).  
     - Subject line: *“Magic Formula Daily Digest – [Date]”*  

---

### **Architecture**  
1. **Microservices Design:**  
   - **Data Collector Service:**  
     - Fetches stock and news data via APIs.  
     - Output: Raw JSON/CSV files stored temporarily.  
   - **Data Processor Service:**  
     - Computes Magic Formula metrics.  
     - Filters and ranks stocks.  
     - Output: Processed data (CSV or SQLite DB).  
   - **Notification Service:**  
     - Generates email template and sends via SMTP.  

2. **Scheduling:**  
   - Daily run at 6:00 PM EST (after market close).  
   - Use cron job (Linux) or Task Scheduler (Windows).  

---

### **Data Handling**  
1. **APIs & Credentials:**  
   - Alpha Vantage (API key required – store in `.env`).  
   - NewsAPI/GNews (API key required – store in `.env`).  
2. **Data Storage:**  
   - Temporary storage: Local filesystem (e.g., `./data/raw_stocks.json`).  
   - Historical tracking: SQLite DB to log daily rankings (for consistency alerts).  

---

### **Error Handling**  
1. **API Failures:**  
   - Retry with exponential backoff (max 3 retries).  
   - Log errors to `error.log` (e.g., *“Alpha Vantage rate limit exceeded”*).  
2. **Data Validation:**  
   - Skip stocks with missing/invalid metrics.  
   - Fallback: If news API fails, omit news section and include note in email.  
3. **Email Failures:**  
   - Retry once after 5 minutes.  
   - Log failures to `notification_errors.log`.  

---

### **Testing Plan**  
1. **Unit Tests:**  
   - Validate Magic Formula calculations (mock data).  
   - Test news filtering logic (e.g., exclude non-reputable sources).  
2. **Integration Tests:**  
   - Verify Alpha Vantage/NewsAPI connectivity.  
   - Test end-to-end workflow (data fetch → process → email).  
3. **Edge Cases:**  
   - Empty API responses.  
   - Stocks with negative EBIT or missing enterprise value.  
4. **User Acceptance Testing (UAT):**  
   - Send test emails to a designated inbox for format validation.  

---

### **Tech Stack Recommendations**  
- **Language:** Python (pandas for data processing, requests for APIs).  
- **Libraries:**  
  - `yfinance` (fallback for stock data if Alpha Vantage limits hit).  
  - `sqlite3` for historical data.  
  - `smtplib`/`email` for notifications.  
- **Environment:** Docker (optional for reproducibility).  

---

### **Deployment Steps**  
1. **Setup:**  
   - Install dependencies: `pip install -r requirements.txt`.  
   - Add API keys to `.env` file.  
2. **Run Locally:**  
   - Execute `main.py` (with cron job for daily automation).  
3. **Monitoring:**  
   - Logs: `system.log` (successful runs), `error.log` (failures).  

---

### **Out of Scope** (For Future Iterations)  
- User authentication or multi-user support.  
- Real-time alerts or mobile notifications.  
- Interactive dashboards or charts.  

--- 

This spec provides a clear roadmap for development. Let me know if you’d like to refine any section!