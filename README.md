# Stock Analyzer

A clean, modular, sector-aware fundamental stock scoring tool.

This project helps systematically evaluate companies using financial metrics and produces structured ratings (Elite / Strong / Mid-range / Weak) based on weighted criteria.

---

## Important: Data Source

**This tool does not scrape or automatically download financial data.**

All metrics must be manually copied by the user from [stockanalysis.com](https://stockanalysis.com).

The analyzer acts as a structured decision-support layer on top of that data. It is designed for personal research and educational use.

---

## Project Structure

| Path | Responsibility |
|------|----------------|
| `stock_analyzer/main.py` | Entry point of the application. |
| `stock_analyzer/data_models.py` | Defines clean data models (dataclasses / Pydantic) for stock data and results. |
| `stock_analyzer/utils.py` | Shared utilities: CAGR calculation, trend ratings, SKIP handling, score mapping. |
| `stock_analyzer/ratings/` | Contains the rating engine that calculates scores based on rules and weights. |
| `stock_analyzer/input/` | Handles interactive input collection and validation. |
| `stock_analyzer/database/` | Will manage MySQL storage of analysis results and insight queries. |
|`stock_analyzer/config/` | Holds JSON configuration files (weights, thresholds, sector rules). |

---

## Project Goals

- Consistent and transparent scoring logic
- Sector-specific rules and weights
- Config-driven design (easy to adjust thresholds and weights)
- Ability to store analysis history (MySQL planned)
- Clean, professional codebase suitable for a portfolio

---

The application is still under active development. Running it will currently do nothing useful.
