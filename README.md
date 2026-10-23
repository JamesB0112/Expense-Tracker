# Expense Tracker & Spending Analysis

A personal finance project combining a Python desktop application, PostgreSQL database, SQL analysis, and Power BI visualization to track expenses and identify spending patterns.

## Project Overview

This project began as a Python-based expense tracker and expanded into a data analysis portfolio project. It combines application development with database management, analytical SQL queries, and interactive business intelligence reporting.

## Technologies Used

- **Python** — Application logic and expense management
- **Tkinter** — Graphical user interface
- **PostgreSQL** — Relational database and data storage
- **SQL** — Data analysis, aggregations, CTEs, window functions, and rankings
- **Power BI** — Interactive dashboard and spending visualization

## Application Features

- Add expenses with dates, categories, descriptions, and amounts
- Validate expense entries before saving
- Store expense records in PostgreSQL
- Maintain a CSV backup of expense data
- View expense records and spending summaries

## SQL Analysis

The SQL analysis explores spending patterns using ten analytical queries, including:

- Overall spending and transaction summaries
- Spending totals and averages by category
- Monthly spending trends
- Monthly spending by category
- Percentage of total spending by category
- Highest expense within each category
- Expenses above their category average
- Highest-spending category for each month
- Month-over-month spending changes
- Combined category-level spending insights

The analysis uses SQL concepts such as `GROUP BY`, aggregate functions, common table expressions (CTEs), window functions, `LAG()`, and ranking functions.

## Power BI Dashboard

The Power BI dashboard presents spending data through interactive visualizations, including:

- Total spending, transaction count, and average expense KPI cards
- Monthly spending trends
- Spending by category
- Monthly spending by category
- Month and category slicers for interactive filtering

**Dataset note:** The Power BI dashboard uses a separate dataset containing 49 expense transactions from January through July 2026. Its results are analyzed independently from the data used by the Python application.

## Key Findings

- Total spending in the Power BI dataset was approximately **$11,896.82**.
- The dataset contained **49 transactions**.
- The average transaction amount was approximately **$242.79**.
- Rent was the highest-spending category.
- April was the highest-spending month.

## What I Learned

Through this project, I developed practical experience with:

- Building a Python GUI application
- Connecting Python to a PostgreSQL database
- Validating and storing structured data
- Writing SQL queries to answer analytical questions
- Using CTEs and window functions for more advanced analysis
- Designing an interactive Power BI dashboard
- Translating spending data into meaningful business insights

## Future Improvements

- Automate data refresh between the database and dashboard
- Expand the dashboard with additional financial metrics
- Improve reporting and trend analysis
- Add automated testing and more robust error handling
