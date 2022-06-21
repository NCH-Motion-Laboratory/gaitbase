# -*- coding: utf-8 -*-
"""

Create reports for liikelaajuus

@author: Jussi (jnu@iki.fi)
"""

import string
from xlrd import open_workbook
from xlutils.copy import copy

from gaitbase.constants import Constants
from .config import cfg


def make_text_report(template, data, fields_at_default):
    """Create report using a Python template"""
    # some text replacements to improve readability
    for field, value in data.items():
        if value in cfg.report.text_replace:
            data[field] = cfg.report.text_replace[value]
    # compile the template code
    template_code = compile(open(template, "rb").read(), template, 'exec')
    # namespace of executed code
    exec_namespace = dict()
    exec(template_code, exec_namespace)
    blocks = exec_namespace['text_blocks']
    return process_blocks(blocks, data, fields_at_default)


def process_blocks(blocks, data, fields_at_default):
    """Process a list of text/separator blocks into text"""
    ITEM_SEPARATOR = '. '
    block_formatted = ''
    report_text = ''
    for k, block in enumerate(blocks):
        if block == Constants.conditional_dot:
            if blocks[k - 1] != Constants.conditional_dot and block_formatted:
                report_text += ITEM_SEPARATOR
        else:
            block_formatted = _conditional_format(block, data, fields_at_default)
            if block_formatted:
                report_text += block_formatted
    return report_text


def _conditional_format(thestr, data, fields_at_default):
    """Conditionally format string thestr. Fields given as {variable} are
    formatted using the data. If all fields are default, an empty string is
    returned."""
    flds = list(_get_format_fields(thestr))
    if not flds or any(fld not in fields_at_default for fld in flds):
        return thestr.format(**data)
    else:
        return ''


def _get_format_fields(thestr):
    """Yield fields from a format string.

    Example:
    input: '{foo} is {bar}' would give output: ('foo', 'bar')
    """
    formatter = string.Formatter()
    pit = formatter.parse(thestr)  # returns parser generator
    for items in pit:
        if items[1]:
            yield items[1]  # = the field


def make_excel_report(xls_template, data, fields_at_default):
    """Create an Excel report (xlrd workbook) from a template.
    xls_template should have Python-style format strings in cells that
    should be filled in, e.g. {TiedotNimi} would fill the cell using
    the corresponding key in self.data.
    xls_template must be in .xls (not xlsx) format, since style info
    cannot be read from xlsx (xlutils limitation).
    """
    workbook_in = open_workbook(xls_template, formatting_info=True)
    workbook_out = copy(workbook_in)
    r_sheet = workbook_in.sheet_by_index(0)
    w_sheet = workbook_out.get_sheet(0)
    # loop through cells, conditionally replace fields with variable names
    for row in range(r_sheet.nrows):
        for col in range(r_sheet.ncols):
            cell = r_sheet.cell(row, col)
            cell_value = cell.value
            if cell_value:  # format non-empty cells only
                # if variable is at default, the result will be an empty cell
                new_value = _conditional_format(cell_value, data, fields_at_default)
                # apply replacement dict only if formatting changed something;
                # this is to avoid changing text-only cells
                if new_value != cell_value:
                    for oldstr, newstr in cfg.report.xls_replace.items():
                        if oldstr in new_value:
                            new_value = new_value.replace(oldstr, newstr)
                _xlrd_set_cell(w_sheet, col, row, new_value)
    return workbook_out


def _xlrd_get_cell(outSheet, colIndex, rowIndex):
    """HACK: Extract the internal cell representation."""
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row:
        return None
    cell = row._Row__cells.get(colIndex)
    return cell


def _xlrd_set_cell(outSheet, col, row, value):
    """HACK: change cell value without changing formatting.
    See: http://stackoverflow.com/questions/3723793/
    preserving-styles-using-pythons-xlrd-xlwt-and-xlutils-copy?lq=1
    """
    previousCell = _xlrd_get_cell(outSheet, col, row)
    outSheet.write(row, col, value)
    if previousCell:
        newCell = _xlrd_get_cell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
