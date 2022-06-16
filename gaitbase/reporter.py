# -*- coding: utf-8 -*-
"""

Create reports for liikelaajuus

@author: Jussi (jnu@iki.fi)
"""

from asyncio.log import logger
import string
from xlrd import open_workbook
from xlutils.copy import copy
import importlib

from gaitbase.constants import Constants


# Next 2 xlrd hacks copied from:
# http://stackoverflow.com/questions/3723793/
# preserving-styles-using-pythons-xlrd-xlwt-and-xlutils-copy?lq=1


def _getOutCell(outSheet, colIndex, rowIndex):
    """HACK: Extract the internal xlwt cell representation."""
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row:
        return None
    cell = row._Row__cells.get(colIndex)
    return cell


def _setOutCell(outSheet, col, row, value):
    """Change cell value without changing formatting."""
    # HACK to retain cell style.
    previousCell = _getOutCell(outSheet, col, row)
    # END HACK, PART I
    outSheet.write(row, col, value)
    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
    # END HACK


class Report:
    """A class to create text and Excel (.xls) reports from data.

    The report is based on a simple template engine. For example, the template
    text may be 'Name: {name} Age: {Age}' and the data may be {'Name': 'John',
    'Age': 30}. The fields in the template are filled in using the data,
    resulting in the string 'Name: John Age: 30'. This is similar to Python text
    formatting, but it has a simple conditional formatting feature: if all the
    data for a given template are 'default', an empty block will be returned.
    The purpose is to easily generate reports where blocks with no input data
    are not printed at all."""

    def __init__(self, data, field_default_vals):
        """Init report with data."""
        # text replacements for text report, to make it prettier
        self.text_replace_dict = {'Ei mitattu': '-', 'EI': 'Ei'}
        # string replacements to be done in Excel report cells
        # these will be applied after filling in the data
        self.cell_postprocess_dict = {'(EI)': '', '(Kyllä)': '(kl.)'}
        self.data = data.copy()  # be sure not to mutate args
        self.data_text = data.copy()
        for key, item in self.data_text.items():
            if item in self.text_replace_dict:
                self.data_text[key] = self.text_replace_dict[item]
        self.fields_default = field_default_vals
        self._item_separator = '. '  # inserted by item_sep()

    def process_blocks(self, blocks):
        """Process a list of text/separator block into text"""
        block_formatted = ''
        report_text = ''
        for k, block in enumerate(blocks):
            if block == Constants.conditional_dot:
                if blocks[k-1] != Constants.conditional_dot and block_formatted:
                    report_text += self._item_separator
            else:
                block_formatted = self._cond_format(block, self.data_text)            
                if block_formatted:
                    report_text += block_formatted

    def _cond_format(self, thestr, data):
        """Conditionally format string thestr. Fields given as {variable} are
        formatted using the data. If all fields are default, an empty string is
        returned."""
        flds = list(Report._get_format_fields(thestr))
        if not flds or any(fld not in self.fields_default for fld in flds):
            return thestr.format(**data)
        else:
            return ''

    @staticmethod
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

    def make_text_report(self, py_template):
        """Create report using the Python template py_template"""
        importlib.import_module(py_template)
        importlib.reload(text_template_test)
        return self.process_blocks(text_template_test.report_blocks)

    def make_excel_report(self, xls_template):
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
        # loop through cells, conditionally replace fields with variable names.
        # for unclear reasons, wb and rb are very different structures,
        # so we read from rb and write to corresponding cells of wb
        # (using the hacky methods above)
        for row in range(r_sheet.nrows):
            for col in range(r_sheet.ncols):
                cell = r_sheet.cell(row, col)
                varname = cell.value
                if varname:  # format non-empty cells
                    newval = self._cond_format(varname, self.data)
                    # apply replacement dict only if formatting actually did
                    # something. this is to avoid changing text-only cells.
                    if newval != varname:
                        for oldstr, newstr in iter(self.cell_postprocess_dict.items()):
                            if oldstr in newval:
                                newval = newval.replace(oldstr, newstr)
                    _setOutCell(w_sheet, col, row, newval)
        return workbook_out
