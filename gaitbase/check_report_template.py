# -*- coding: utf-8 -*-
"""
Run some checks on the report template.

@author: jussi (jnu@iki.fi)
"""


from .rom_reporter import _get_format_fields
from .dump_varlist import get_vars_and_affinities


def _check_template(template):
    """Check the Python text template"""

    exec_namespace = dict()
    try:
        template_code = compile(open(template, "rb").read(), template, 'exec')
        exec(template_code, exec_namespace)
    except (SyntaxError, NameError) as e:
        print(f'The report template contains syntax errors:\n{e}')
        return

    blocks = exec_namespace['_text_blocks']

    template_fields = set()
    for block in blocks:
        if isinstance(block, str):
            template_fields.update(_get_format_fields(block))

    # get the ROM vars defined in the UI and compare
    ui_vars = set(get_vars_and_affinities())
    # the report may also reference columns from the patients table
    ui_vars.update({'firstname', 'lastname', 'ssn', 'patient_code', 'diagnosis'})
    not_in_report = ui_vars - template_fields
    unrecognized = template_fields - ui_vars

    if unrecognized:
        print(f'*** {template} refers to following unrecognized fields: {unrecognized}')
        return

    print(f'*** {template} checks OK')
    print(f'*** {template} refers to {len(template_fields)} variables\n')
    print(f'*** variables not referenced by the template:')
    print('\n'.join(sorted(not_in_report)))


if __name__ == '__main__':
    TEMPLATE = r'templates/text_template.py'
    _check_template(TEMPLATE)
