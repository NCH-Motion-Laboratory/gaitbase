# -*- coding: utf-8 -*-
"""

Create reports for liikelaajuus

@author: Jussi (jnu@iki.fi)
"""

import string
from xlrd import open_workbook
from xlutils.copy import copy

from .constants import Constants


# Next 2 xlrd hacks copied from:
# http://stackoverflow.com/questions/3723793/
# preserving-styles-using-pythons-xlrd-xlwt-and-xlutils-copy?lq=1

def _getOutCell(outSheet, colIndex, rowIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row:
        return None
    cell = row._Row__cells.get(colIndex)
    return cell

def _setOutCell(outSheet, col, row, value):
    """ Change cell value without changing formatting. """
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


class Report():
    """A simple template engine. For example, the template text may be
    'Name: {name} Age: {Age}' and the data may be {'Name': 'John', 'Age': 30}.
    The fields in the template are filled in using the data, resulting in
    the string 'Name: John Age: 30'
    This is similar to Python text formatting, but it has a simple conditional
    formatting feature: if all the data for a given template are 'default', an
    empty block will be returned. The purpose is to easily generate reports
    where sections with missing data are not printed at all."""

    def __init__(self, data, fields_default):
        """Init report with data dict."""
        # text replacements for text report, to make it prettier
        self.text_replace_dict = {'Ei mitattu': '-', 'EI': 'Ei'}
        # string replacements to be done in Excel report cells
        # these will be applied after filling in the data
        self.cell_postprocess_dict = {'(EI)': '', '(Kyllä)': '(kl.)'}
        self.text = ''  # the report text
        self.data = data.copy()  # be sure not to mutate args
        self.data_text = data.copy()
        for key, it in self.data_text.items():
            if it in self.text_replace_dict:
                self.data_text[key] = self.text_replace_dict[it]
        self.fields_default = fields_default
        self._item_separator = '. '  # inserted by item_sep()

    def __add__(self, s):
        """ Format and add a text block to report """
        self.text += self._cond_format(s, self.data_text)
        return self

    def item_sep(self):
        """Insert item separator if appropriate"""
        seplen = len(self._item_separator)
        if (self.text[-seplen:] != self._item_separator and
           self.text[-2:] != ': '):  # bit of a hack
            self.text += self._item_separator

    def __repr__(self):
        return self.text

    def _cond_format(self, s, data):
        """ Conditionally format string s. Fields given as {variable} are
        formatted using the data. If all fields are default, an
        empty string is returned. """
        flds = list(Report._get_fields(s))
        if not flds or any(fld not in self.fields_default for fld in flds):
            return s.format(**data)
        else:
            return ''

    @staticmethod
    def _get_fields(s):
        """Yield fields from a format string, e.g.
        '{foo} is {bar}'  ->  ['foo', 'bar']  """
        fi = string.Formatter()
        pit = fi.parse(s)  # returns parser generator
        for items in pit:
            if items[1]:
                yield items[1]  # = the field

    def make_text_report(self, py_template):
        """Create report using the template py_template
        We want to use the code in py_template to modify a local variable,
        however function locals cannot be directly modified. Thus we pass
        in another dict to hold the modified values."""
        report = self  # the Report instance to modify
        # any other variables needed by the template
        checkbox_yes = Constants.checkbox_yestext
        ldict = locals()
        # the recommended Python 3 alternative to execfile()
        # exec() arguments for globals and locals are a bit tricky. this form
        # allows us to read in the function local namespace and modify it
        exec(compile(open(py_template, "rb").read(), py_template, 'exec'),
             ldict, ldict)
        return ldict['report'].text

    def make_excel_report(self, xls_template):
        """Create an Excel report (xlrd workbook) from a template.
        xls_template should have Python-style format strings in cells that
        should be filled in, e.g. {TiedotNimi} would fill the cell using
        the corresponding key in self.data.
        xls_template must be in .xls (not xlsx) format, since style info
        cannot be read from xlsx (xlutils limitation).
        """
        rb = open_workbook(xls_template, formatting_info=True)
        wb = copy(rb)
        r_sheet = rb.sheet_by_index(0)
        w_sheet = wb.get_sheet(0)
        # loop through cells, conditionally replace fields with variable names.
        # for unclear reasons, wb and rb are very different structures,
        # so we read from rb and write to corresponding cells of wb
        # (using the hacky methods above)
        for row in range(r_sheet.nrows):
            for col in range(r_sheet.ncols):
                cl = r_sheet.cell(row, col)
                varname = cl.value
                if varname:  # format non-empty cells
                    newval = self._cond_format(varname, self.data)
                    # apply replacement dict only if formatting actually did
                    # something. this is to avoid changing text-only cells.
                    if newval != varname:
                        for str, newstr in (iter(self.cell_postprocess_dict.
                                            items())):
                            if str in newval:
                                newval = newval.replace(str, newstr)
                    _setOutCell(w_sheet, col, row, newval)
        return wb
