# Copyright (c) 2023, The Commit Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.csvutils import read_csv_content
from frappe.utils.xlsxutils import (
	read_xls_file_from_attached_file,
	read_xlsx_file_from_attached_file,
)
from datetime import datetime
class TXTransactionImporter(Document):

	@frappe.whitelist()
	def import_transactions(self):
		# Iterate over all the transactions and create the TX Transaction
		if not self.import_file:
			frappe.throw("Please upload a file to import")

		parsed_data = self.generate_preview()

		date_formats = []

		date_column_index = parsed_data["columns"].index("date")
		for row in parsed_data["data"]:
			if row[date_column_index]:
				date_formats.append(frappe.utils.guess_date_format(row[date_column_index]))
		
		unique_date_formats = set(date_formats)
		max_occurred_date_format = max(unique_date_formats, key=date_formats.count)
		print(unique_date_formats)
		if len(unique_date_formats) > 1:
			# fmt: off
			frappe.throw(_("The column has different date formats."))

		for row in parsed_data["data"]:
			json_mapped_data = {}

			for index, column in enumerate(parsed_data["columns"]):
				if column == "DO NOT IMPORT":
					continue
				if column == "date":
					if row[index]:
						json_mapped_data[column] = datetime.strptime(row[index], max_occurred_date_format)
				
				else:
					json_mapped_data[column] = row[index]
			if not json_mapped_data["date"]:
				continue
			transaction = frappe.get_doc({
				"doctype": "TX Transaction",
				"account": self.account,
				**json_mapped_data
			})
			transaction.insert()
		
		frappe.db.commit()

		self.status = "Success"
		self.save()

		return "Imported successfully"

		"""
		  TODO: Use DataImport for this. Add realtime progress bar, status checks etc
		  Show error logs
		  """

		pass

	@frappe.whitelist()
	def generate_preview(self):
		if not self.import_file:
			frappe.throw("Please upload a file to import")
		# Generate preview of the transactions
		import_template = frappe.get_doc("TX Import Template", self.template)

		self.file_doc = frappe.get_doc("File", {"file_url": self.import_file})


		self.raw_data = self.get_data_from_template_file()
		print(self.raw_data)

		columns = []
		
		for column in import_template.template_columns:
			columns.append(column.field_name)
		
		return {
			"columns": columns,
			"data": self.raw_data
		}

	def get_data_from_template_file(self):
		content = None
		extension = None

		if self.file_doc:
			parts = self.file_doc.get_extension()
			extension = parts[1]
			content = self.file_doc.get_content()
			extension = extension.lstrip(".")

		if not content:
			frappe.throw(_("Invalid or corrupted content for import"))

		if not extension:
			extension = "csv"

		if content:
			return self.read_content(content, extension)
	
	def read_content(self, content, extension):
		error_title = _("Template Error")
		if extension not in ("csv", "xlsx", "xls"):
			frappe.throw(_("Import template should be of type .csv, .xlsx or .xls"), title=error_title)

		if extension == "csv":
			data = read_csv_content(content)
		elif extension == "xlsx":
			data = read_xlsx_file_from_attached_file(fcontent=content)
		elif extension == "xls":
			data = read_xls_file_from_attached_file(content)

		return data
	pass
