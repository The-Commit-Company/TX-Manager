// Copyright (c) 2023, The Commit Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("TX Transaction Importer", {
    refresh(frm) {
        frm.fields_dict['preview'].$wrapper.html("")
        if (!frm.is_new()) {
            frm.add_custom_button(__("Generate Preview"), function () {
                frm.call('generate_preview')
                    .then(r => {
                        console.log(r)

                        html = `<div>${r.message.columns.length} columns and ${r.message.data.length} rows</div><table class='table table-bordered'><thead>`

                        r.message.columns.forEach(function (column) {
                            html += `<th>${column}</th>`
                        })

                        html += "</thead><tbody>"

                        r.message.data.forEach(function (row) {
                            html += "<tr>"
                            row.forEach(function (column) {
                                html += `<td>${column}</td>`
                            })
                            html += "</tr>"
                        }
                        )

                        html += "</tbody></table>"

                        frm.fields_dict['preview'].$wrapper.html(html)

                    })
            })
            if (frm.doc.status == "Not Started") {
                frm.add_custom_button(__("Import"), function () {
                    frm.call('import_transactions')
                        .then(r => {
                            console.log(r)
                            if (r.message) {
                                frappe.msgprint(r.message)
                            }
                        })
                })
            }
        }

    },
});
