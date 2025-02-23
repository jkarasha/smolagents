Here’s a step-by-step blueprint broken into **small, iterative prompts** for code generation. Each step builds on the prior work and includes integration/testing:

---

### **Phase 1: Project Setup & Data Collection**
#### **Step 1.1: Initialize Project Structure**
```text
Create a Python project with the following structure:
- magic_formula_digest/
  ├── data/ (for raw/processed data)
  ├── utils/ (helper modules)
  ├── .gitignore (exclude .env, data/, __pycache__/)
  ├── requirements.txt (list: requests, pandas, python-dotenv)
  └── README.md (basic setup instructions)
```

#### **Step 1.2: Configure Environment Variables**
```text
Create a .env file to store API credentials:
- ALPHA_VANTAGE_API_KEY=your_key_here
- NEWS_API_KEY=your_key_here
- SMTP_USER=your_email@example.com
- SMTP_PASSWORD=your_app_specific_password

Add code to load these variables using python-dotenv in a new module utils/config.py.
```

#### **Step 1.3: Fetch Stock Data (Alpha Vantage)**
```text
Write a function in utils/stock_client.py that:
1. Uses Alpha Vantage's `OVERVIEW` endpoint to fetch EBIT, enterprise value, etc.
2. Uses `TIME_SERIES_DAILY` to get closing price and % change.
3. Saves raw JSON responses to data/raw_stocks/[ticker].json.
4. Implements retries (3 attempts) for API errors.
5. Logs failures to data/error.log.
```

---

### **Phase 2: Data Processing**
#### **Step 2.1: Calculate Magic Formula Metrics**
```text
Create utils/processor.py with:
1. A function to compute earnings yield (EBIT / Enterprise Value).
2. A function to compute return on capital (EBIT / (Net Fixed Assets + Working Capital)).
3. Filter out stocks with missing/negative metrics.
4. Output a CSV to data/processed/ranked_stocks_[date].csv with columns: 
   [Ticker, Price, PctChange, EarningsYield, ROC].
```

#### **Step 2.2: Historical Tracking (SQLite)**
```text
Add a SQLite database at data/history.db with a table:
CREATE TABLE stock_rankings (
    date TEXT,
    ticker TEXT,
    earnings_yield REAL,
    roc REAL,
    rank INTEGER
);

Update utils/processor.py to insert daily rankings into this table.
```

---

### **Phase 3: News Integration**
#### **Step 3.1: Fetch Company News**
```text
Build utils/news_client.py to:
1. Use NewsAPI's /everything endpoint with query="stock ticker".
2. Filter headlines from sources: Bloomberg, Reuters, CNBC, MarketWatch.
3. Save relevant news to data/processed/news_[date].csv with columns:
   [Ticker, Headline, Source, URL].
4. Skip if API fails, log to error.log.
```

---

### **Phase 4: Email Generation**
#### **Step 4.1: Build Email Template**
```text
Create utils/email_template.py with:
1. A function to generate plain text + HTML tables for top 10 stocks.
2. Format news headlines as bullet points with sources.
3. Include a "Why this stock?" line for each entry (e.g., "High ROC of 15%").
4. Add recommendations based on consistency (e.g., "Ranked top 10 for 5 days").
```

#### **Step 4.2: SMTP Email Sender**
```text
Write utils/email_sender.py to:
1. Use smtplib with SMTP_SSL.
2. Read credentials from .env.
3. Send emails with subject "Magic Formula Daily Digest – [YYYY-MM-DD]".
4. Retry failed sends once after 5 minutes.
```

---

### **Phase 5: Integration & Automation**
#### **Step 5.1: Main Workflow Script**
```text
Create main.py that:
1. Calls stock_client to fetch data.
2. Runs processor to rank stocks.
3. Fetches news for top 10 stocks.
4. Generates and sends the email.
5. Logs success/failure to system.log.
```

#### **Step 5.2: Scheduling & Logging**
```text
Add a bash script run_daily.sh:
#!/bin/bash
cd /path/to/project && /usr/bin/python3 main.py

Set up a cron job:
0 18 * * 1-5 /path/to/run_daily.sh >/dev/null 2>&1
```

---

### **Phase 6: Testing & Validation**
#### **Step 6.1: Unit Tests**
```text
Write tests/test_calculations.py to verify:
- Earnings yield calculation with mock EBIT/Enterprise Value.
- ROC calculation with mock EBIT/(Net Fixed Assets + Working Capital).
- News filtering logic (e.g., exclude non-reputable sources).
```

#### **Step 6.2: End-to-End Test**
```text
Create a test mode in main.py (--test) that:
1. Uses mock stock/news data from tests/fixtures/.
2. Generates an email without sending it.
3. Outputs results to tests/output/test_email.html.
```

---

### **Iteration Plan**
1. **Week 1:** Implement Phases 1-2 (data collection/processing).  
2. **Week 2:** Add Phases 3-4 (news/email).  
3. **Week 3:** Complete Phase 5 (integration) and Phase 6 (testing).  

Each prompt above can be directly fed to a code-generation LLM (e.g., GPT-4, Claude) with the instruction:  
*"Write Python code for [STEP DESCRIPTION] following best practices. Integrate with existing modules as specified."*