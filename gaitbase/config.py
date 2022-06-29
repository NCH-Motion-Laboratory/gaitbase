# -*- coding: utf-8 -*-
"""
Handles the configuration for the gait database.

If the user-specific config file does not exist (e.g. on the first run of the
package), it is created in the user's home directory. Next, the package default
configuration is loaded. Finally the configuration is updated from the user's
config file.
"""

from pathlib import Path
from configdot import parse_config, update_config, dump_config
from pkg_resources import resource_filename
import logging


logger = logging.getLogger(__name__)

# location of the default config file
cfg_package_fn = resource_filename(__name__, 'data/default.cfg')
# Location of the user specific config file. On Windows, this typically puts the
# config at C:\Users\Username, since the USERPROFILE environment variable points
# there. Putting the config in a networked home dir requires some tinkering with
# environment variables (e.g. setting HOME)
cfg_user_fn = Path.home() / '.gaitbase.cfg'

# provide the global cfg instance
# we assume that config files are encoded in utf-8
cfg = parse_config(cfg_package_fn, encoding='utf-8')

# update cfg from user file
if cfg_user_fn.is_file():
    logger.debug(f'reading user config from {cfg_user_fn}')
    cfg_user = parse_config(cfg_user_fn)
    update_config(
        cfg,
        cfg_user,
        create_new_items=False,
        create_new_sections=False,
        update_comments=False,
    )
else:
    logger.warning(f'no config file, trying to create {cfg_user_fn}')
    cfg_txt = dump_config(cfg)
    with open(cfg_user_fn, 'w', encoding='utf8') as f:
        f.writelines(cfg_txt)


# if template locations are not configured by the user, we revert to package
# default templates
if cfg.templates.text is None:
    cfg.templates.text = resource_filename(
        'gaitbase', 'templates/text_template.py'
    )

if cfg.templates.xls is None:
    cfg.templates.xls = resource_filename(
        'gaitbase', 'templates/rom_excel_template.xls'
    )
