# -*- coding: utf-8 -*-
"""
Create ROM reports for gaitbase.

@author: Jussi (jnu@iki.fi)
"""
import string
import re
from xlrd import open_workbook
from xlutils.copy import copy

from .constants import Constants
from .config import cfg


def make_text_report(template, data, fields_at_default):
    """Create a text report using a Python template.

    For documentation of the template format, see the example templates under
    gaitbase/templates.

    Parameters
    ----------
    template : str | Path
        Path to the template.
    data : dict
        Fields and their corresponding values.
    fields_at_default : list
        Fields that are at their default values.

    Returns
    -------
    str
        The resulting text.
    """
    # replace some values to improve readability
    for field, value in data.items():
        if value in cfg.report.replace_data:
            data[field] = cfg.report.replace_data[value]
    # compile the template code
    template_code = compile(open(template, "rb").read(), template, 'exec')
    # namespace of executed code
    exec_namespace = dict()
    exec(template_code, exec_namespace)
    blocks = exec_namespace['text_blocks']
    return _process_blocks(blocks, data, fields_at_default)


def _process_blocks(blocks, data, fields_at_default):
    """Process a list of text blocks.

    For template formatting rules, see the example Python template under
    gaitbase/templates.
    """
    block_formatted = ''
    report_text = ''
    for block in blocks:
        if block == Constants.end_line:
            # remove preceding end-of-line comma, if any
            report_text = re.sub(r',\s*$', '', report_text)
            # add dot & linefeed (only at end of line)
            if report_text[-1] != '\n':
                report_text += '.\n'
        elif block_formatted := _conditional_format(block, data, fields_at_default):
            if report_text and report_text[-1] == '\n':
                # if the block starts a new line, capitalize the first letter
                block_formatted = block_formatted[0].upper() + block_formatted[1:]
            report_text += block_formatted
    return report_text


def _conditional_format(thestr, data, fields_at_default):
    """Conditionally format string thestr.

    Fields given as {field} are replaced with their values in the data dict. If
    all the fields are in the fields_at_default list, an empty string is returned."""
    flds = _get_format_fields(thestr)
    if not flds or any(fld not in fields_at_default for fld in flds):
        return thestr.format(**data)
    else:
        return ''


def _get_format_fields(thestr):
    """Return a list of fields, given a format string.

    For '{foo} is {bar}' would return ['foo', 'bar']
    """
    formatter = string.Formatter()
    return [fieldname for (_, fieldname, _, _) in formatter.parse(thestr) if fieldname]


def make_excel_report(xls_template, data, fields_at_default):
    """Make an Excel report from a template.

    The template should have Python-style format strings in cells that should be
    filled in, e.g. {TiedotNimi} would fill the cell using the corresponding key
    in self.data.

    xls_template must be in .xls (not xlsx) format, since style info cannot be
    read from xlsx (xlutils limitation).

    Parameters
    ----------
    xls_template : str | Path
        Path to the template.
    data : dict
        Fields and their corresponding values.
    fields_at_default : list
        Fields that are at their default values.

    Returns
    -------
    workbook
        xlrd workbook.
    """
    workbook_in = open_workbook(xls_template, formatting_info=True)
    workbook_out = copy(workbook_in)
    r_sheet = workbook_in.sheet_by_index(0)
    w_sheet = workbook_out.get_sheet(0)
    # replace some values to improve readability
    for field, value in data.items():
        if value in cfg.report.replace_data:
            data[field] = cfg.report.replace_data[value]
    # loop through cells, conditionally replace fields with variable names
    for row in range(r_sheet.nrows):
        for col in range(r_sheet.ncols):
            cell = r_sheet.cell(row, col)
            cell_text = cell.value
            if cell_text:  # format non-empty cells only
                # if all variables are at default, the result will be an empty cell
                cell_text_formatted = _conditional_format(
                    cell_text, data, fields_at_default
                )
                # apply replacement text only if formatting changed something
                # (to avoid undesired changes to text-only cells)
                if cell_text_formatted != cell_text:
                    for oldstr, newstr in cfg.report.xls_replace_strings.items():
                        cell_text_formatted = cell_text_formatted.replace(
                            oldstr, newstr
                        )
                _xlrd_set_cell(w_sheet, col, row, cell_text_formatted)
    return workbook_out


def _xlrd_get_cell(out_sheet, col_index, row_index):
    """HACK: Extract the internal cell representation."""
    if row := out_sheet._Worksheet__rows.get(row_index):
        return row._Row__cells.get(col_index)  # a cell


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
