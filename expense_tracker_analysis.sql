-- 1. Overall Expense Summary
SELECT COUNT(*) AS total_transactions,
	SUM(amount) AS total_spending,
    ROUND(AVG(amount), 2) AS average_expense,
    MIN(amount) AS smallest_expense,
    MAX(amount) AS largest_expense
FROM portfolio_expenses;

-- 2. Spending by Category
SELECT category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_spending,
    ROUND(AVG(amount), 2) AS average_expense
FROM portfolio_expenses
GROUP BY category
ORDER BY total_spending DESC;

-- 3. Monthly Spending Trend
SELECT DATE_TRUNC('month', expense_date)::DATE AS month,
    SUM(amount) AS total_spending,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount), 2) AS average_expense
FROM portfolio_expenses
GROUP BY DATE_TRUNC('month', expense_date)
ORDER BY month;

-- 4. Monthly Spending by Category
SELECT DATE_TRUNC('month', expense_date) AS month,
	category,
	SUM(amount) AS total_spending
FROM portfolio_expenses
GROUP BY DATE_TRUNC('month', expense_date), category
ORDER by month;

-- 5. Total Percentage
WITH total AS (
	SELECT category,
		SUM(amount) AS total_spending
FROM portfolio_expenses
GROUP BY category
),
percentage AS (
	SELECT category,
		total_spending,
		SUM(total_spending) OVER () AS grand_total
FROM total
)
SELECT category,
	total_spending,
	ROUND(total_spending / grand_total * 100.00, 2) AS percentage_of_total
FROM percentage
ORDER BY total_spending DESC;

-- 6. Highest Expense in Each Category
WITH rank AS (
	SELECT category,
		expense_id,
		ROW_NUMBER() OVER (
		PARTITION BY category
		ORDER BY amount DESC) AS expense_rank,
		amount,
		expense_date
FROM portfolio_expenses
)
SELECT category,
	expense_id,
	amount,
	expense_date
FROM rank
WHERE expense_rank = 1;

-- 7. Expenses Above their Category Average
WITH cat_average AS (
	SELECT category,
			expense_id,
			amount,
			AVG(amount) OVER (
			PARTITION BY category) AS category_avg
	FROM portfolio_expenses
),
avg_difference AS (
	SELECT category,
		expense_id,
		amount,
		category_avg,
		(amount - category_avg) AS difference_from_avg
	FROM cat_average
)
SELECT category,
	expense_id,
	amount,
	category_avg,
	difference_from_avg
FROM avg_difference
WHERE difference_from_avg > 0;

-- 8. Highest Spending Category each Month
WITH monthly AS (
	SELECT DATE_TRUNC('month', expense_date) AS month,
		amount,
		category
	FROM portfolio_expenses
),
total AS (
	SELECT month,
		category,
		SUM(amount) AS monthly_total
	FROM monthly
	GROUP BY month, category
),
rank AS (
	SELECT month,
		category,
		monthly_total,
		ROW_NUMBER() OVER (
		PARTITION BY month
		ORDER BY monthly_total DESC) AS category_rank
	FROM total
)
SELECT month,
	category,
	monthly_total,
	category_rank
FROM rank
WHERE category_rank = 1
ORDER BY monthly_total DESC;

-- 9. Monthly Spending Change
WITH spending AS (
	SELECT DATE_TRUNC('month', expense_date) AS month,
		SUM(amount) AS monthly_spending
	FROM portfolio_expenses
	GROUP BY DATE_TRUNC('month', expense_date)
),
previous_spending AS (
	SELECT month,
		monthly_spending,
		LAG(monthly_spending) OVER (
		ORDER BY month ASC) AS previous_month_spending
	FROM spending
)
SELECT month,
	monthly_spending,
	previous_month_spending,
	(monthly_spending - previous_month_spending) AS change_amount
FROM previous_spending
ORDER BY month ASC;

--10. 
WITH insights AS (
	SELECT category,
		COUNT(category) AS transaction_count,
		AVG(amount) AS average_expense,
		SUM(amount) AS total_spending
	FROM portfolio_expenses
	GROUP BY category
),
total AS (
	SELECT category,
		transaction_count,
		average_expense,
		total_spending,
		SUM(total_spending) OVER () AS grand_total
	FROM insights
),
percentage AS (
	SELECT category,
		transaction_count,
		average_expense,
		total_spending,
		ROUND(total_spending * 100.0 / grand_total, 2) AS percentage_of_total
	FROM total
)
SELECT category,
	transaction_count,
	average_expense,
	total_spending,
	percentage_of_total
FROM percentage;