# Magic Formula Daily Digest - Development Checklist

## **Environment Setup**
- [ ] Create project structure:
  ```bash
  mkdir -p magic_formula_digest/{data/{raw_stocks,processed},utils,tests/fixtures}
  ```
- [ ] Set up virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  ```
- [ ] Install core dependencies:
  ```bash
  pip install requests pandas python-dotenv
  pip freeze > requirements.txt
  ```
- [ ] Create `.env` file with template:
  ```ini
  ALPHA_VANTAGE_API_KEY=your_key
  NEWS_API_KEY=your_key
  SMTP_USER=your_email@example.com
  SMTP_PASSWORD=your_app_password
  ```

---

## **Phase 1: Data Collection**
### Stock Data
- [ ] `utils/config.py`: Load environment variables
- [ ] `utils/stock_client.py`:
  - [ ] Implement Alpha Vantage API client
  - [ ] Add retry logic with backoff
  - [ ] Save raw JSON responses to `data/raw_stocks/`
  - [ ] Handle rate limiting (5 calls/minute)

### News Data
- [ ] `utils/news_client.py`:
  - [ ] Implement NewsAPI/GNews client
  - [ ] Filter by reputable sources
  - [ ] Save news to `data/processed/news_[date].csv`

---

## **Phase 2: Data Processing**
- [ ] `utils/processor.py`:
  - [ ] Calculate earnings yield
  - [ ] Calculate return on capital
  - [ ] Filter invalid metrics (negative values)
  - [ ] Generate ranked CSV output
- [ ] SQLite database setup:
  - [ ] Create `data/history.db`
  - [ ] Implement daily ranking insertion

---

## **Phase 3: Email System**
- [ ] `utils/email_template.py`:
  - [ ] Build HTML table template
  - [ ] Format news bullet points
  - [ ] Add recommendation logic
- [ ] `utils/email_sender.py`:
  - [ ] Configure SMTP with SSL
  - [ ] Add email retry logic
  - [ ] Implement attachment-free sending

---

## **Phase 4: Core Workflow**
- [ ] `main.py`:
  - [ ] Implement workflow:
    1. Fetch stock data
    2. Process rankings
    3. Fetch news for top 10
    4. Generate email
    5. Send notification
- [ ] Add logging:
  - [ ] Success logs to `system.log`
  - [ ] Errors to `error.log`

---

## **Phase 5: Automation**
- [ ] Create `run_daily.sh`:
  ```bash
  #!/bin/bash
  cd /path/to/project && source venv/bin/activate && python main.py
  ```
- [ ] Set up cron job:
  ```bash
  # Open crontab
  crontab -e
  
  # Add line
  0 18 * * 1-5 /path/to/run_daily.sh >/dev/null 2>&1
  ```

---

## **Testing & Validation**
### Unit Tests
- [ ] `tests/test_calculations.py`:
  - [ ] Verify Magic Formula math
  - [ ] Test news filtering
  - [ ] Validate email template generation

### Integration Tests
- [ ] Test end-to-end flow:
  ```bash
  python main.py --test  # Uses mock data
  ```
- [ ] Verify email output in `tests/output/`

### Edge Cases
- [ ] Test with empty API responses
- [ ] Test negative EBIT handling
- [ ] Verify rate limit recovery

---

## **Deployment**
- [ ] Documentation:
  - [ ] Add API key setup instructions to README
  - [ ] Note cron job timing (6PM EST)
- [ ] Dry run:
  ```bash
  python main.py --dry-run  # Skip actual email send
  ```
- [ ] First production run monitoring:
  - [ ] Check `system.log`
  - [ ] Verify email delivery

---

## **Future Iterations (Optional)**
- [ ] Add yfinance fallback
- [ ] Implement simple web dashboard
- [ ] Add sector filtering