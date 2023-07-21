// Copyright (c) 2023, The Commit Company and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["TX Transaction Summary"] = {
	"filters": [
		{
			"fieldname": "account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "TX Account",
			"reqd": 1
		},
		{
			'fieldname': 'month',
			'label': __('Month'),
			'fieldtype': 'Select',
			"reqd": 1,
			'options': "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
		},
		{
			'fieldname': 'year',
			'label': __('Year'),
			'fieldtype': 'Select',
			"reqd": 1,
			'default': frappe.datetime.get_today().split('-')[0],
			'options': '2019\n2020\n2021\n2022\n2023\n2024\n2025\n2026\n2027\n2028\n2029\n2030',
		}
	]
};
