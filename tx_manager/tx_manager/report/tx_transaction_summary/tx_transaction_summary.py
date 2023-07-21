# Copyright (c) 2023, The Commit Company and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	if not filters:
		return [], []
	
	account = filters.get("account")

	month = filters.get("month")
	year = filters.get("year")
	
	data = frappe.db.sql("""SELECT category, MONTHNAME(date) AS month, YEAR(date) AS year, SUM(credit_amount) AS credit_amount, SUM(debit_amount) AS debit_amount FROM `tabTX Transaction` 
WHERE account = '{}' AND MONTHNAME(date) = '{}' AND YEAR(date) = '{}'
GROUP BY category""".format(account, month, year), as_dict=True)
	
	# Report is in the following way
	# Columns will be category, and then groups of month + year and within wvery montn year - a credit and debit amount
	
	columns = get_columns()
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "category",
			"label": "Category",
			"fieldtype": "Link",
			"options": "TX Transaction Category",
			"width": 200
		},
		{
			"fieldname": "credit_amount",
			"label": "Credit Amount",
			"fieldtype": "Float",
			"width": 200,
			"precision": 2
		},
		{
			"fieldname": "debit_amount",
			"label": "Debit Amount",
			"fieldtype": "Float",
			"width": 200,
			"precision": 2
		}
	]