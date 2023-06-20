# Copyright (c) 2023, The Commit Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TXTransaction(Document):

	def before_validate(self):
		if self.amount:
			amount = self.amount.strip().replace(" ", "").lower()
			if "cr" in amount:
				self.credit_amount = amount.replace("cr", "").replace(" ", "").strip()
				self.debit_amount = 0
			else:
				self.debit_amount = amount.replace("dr", "").replace(" ", "").strip()
				self.credit_amount = 0
		
		if self.credit_amount:
			self.credit_amount = self.credit_amount.strip().replace(" ", "").lower()
			self.type = "Credit"
		
		if self.debit_amount:
			self.debit_amount = self.debit_amount.strip().replace(" ", "").lower()
			self.type = "Debit"
	
	def validate(self):
		if not self.credit_amount and not self.debit_amount:
			frappe.throw("Please enter either credit or debit amount")
		
		if self.credit_amount and self.debit_amount:
			frappe.throw("Please enter either credit or debit amount")
	
	def before_save(self):
		# If there are duplicates in the same account, date, description and amount, mark them as potential duplicates
		# Also mark the current transaction as potential duplicate
		potential_duplicates = frappe.get_all("TX Transaction", filters={"account": self.account, "date": self.date, "description": self.description, "amount": self.amount, "override_duplicate_analysis": 0})
		if len(potential_duplicates) > 1:
			self.might_be_duplicate = 1
			for duplicate in potential_duplicates:
				if duplicate.name != self.name:
					frappe.db.set_value("TX Transaction", duplicate.name, "might_be_duplicate", 1)
					if self.override_duplicate_analysis:
						frappe.db.set_value("TX Transaction", duplicate.name, "override_duplicate_analysis", 1)
	pass
