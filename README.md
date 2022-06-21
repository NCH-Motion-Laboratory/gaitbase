

# gaitbase


## Overview 

NOTE: this program is for the purposes of Helsinki Gait Lab and most of the user interface is in Finnish. Thus, it's probably not useful for other labs in its current state.

gaitbase is a simple SQLite patient database with a Qt-based GUI. The GUI allows the user to browse, insert, delete and search patients.

In addition to patients, various measurement modalities can be implemented. The idea is to have a SQL table for each modality. Each row in such a table corresponds to one measurement (session), and each column corresponds to a variable. Every row must be associated with a patient in the patients table. Data for each modality will be shown in the main patient window when a patient is selected.

## Overview of the ROM app

Currently, one modality is implemented: range of motion (ROM). This modality includes ROM, strength and other manual measurements typically carried out by physiotherapists. The ROM SQL schema currently includes 300+ different variables (columns). When a patient is selected, the GUI shows the ROM measurements corresponding to that patient.

When a measurement is opened, it is loaded in the ROM editor window. The editor contains a lot of data entry widgets, organized into tabs. Each variable corresponds to an entry widget. The entry widgets are recognized by their special names, and the variable names are automatically derived from the widgets. On the SQL side, the ROM data is contained in a table called “roms”. Each row in the table corresponds to a patient (entry in the patients table).  Whenever new ROM data is entered, this table is updated accordingly and the changes are immediately committed. Thus, crashes should not cause significant data loss.


## Data entry widgets

The UI is created in Qt Designer. (Nowadays there is a newer alternative called Qt Creator, which may also work). The widgets for data entry are given names starting with the string `data`. The app gathers input data from these widgets, and automatically derives variable names from the widget names by removing the `data` prefix. Currently, six types of data entry widgets are supported:


<table>
  <tr>
   <td><strong>Widget type</strong>
   </td>
   <td><strong>Purpose</strong>
   </td>
   <td><strong>Notes</strong>
   </td>
  </tr>
  <tr>
   <td>QSpinBox, QDoubleSpinBox
   </td>
   <td>Numeric values
   </td>
   <td>The spinboxes must be properly configured in Qt Designer. See notes below.
   </td>
  </tr>
  <tr>
   <td>QLineEdit
   </td>
   <td>Short text (one line)
   </td>
   <td>Leading and trailing whitespace will be stripped when reading from the widget.
   </td>
  </tr>
  <tr>
   <td>QComboBox
   </td>
   <td>Multiple-choice
   </td>
   <td>The choices need to be configured in Qt Designer. See notes below.
   </td>
  </tr>
  <tr>
   <td>CheckableSpinBox
   </td>
   <td>Numeric values, with a choice of the variable being “within normal range”
   </td>
   <td>A custom spinbox widget. See notes below.
   </td>
  </tr>
  <tr>
   <td>QTextEdit
   </td>
   <td>Longer text (e.g. comments)
   </td>
   <td>Leading and trailing whitespace will be stripped when reading from the widget.
   </td>
  </tr>
  <tr>
   <td>QCheckBox
   </td>
   <td>Boolean values (yes/no)
   </td>
   <td>Note that the plain checkbox does not have a distinct “not measured” value. If the distinction is needed, use the combobox instead.
   </td>
  </tr>
</table>


Any other (non-data-entry) widgets may also exist in the UI. Obviously, their names must not start with “data”.


## Configuring the data entry widgets

Widgets of type `QLineEdit`, `QTextEdit` and `QCheckBox` usually need no special configuration. The other types must be configured in Qt Designer.

Qt supports a ‘special value’ for spinboxes. If the `QAbstractSpinBox.specialValue` property (string) is set, this text will be displayed by the widget whenever it is at its minimum value. We use the special value property to indicate unmeasured values. Thus, the specialValue property should be set to “Ei mitattu” (unmeasured). 

The `QSpinBox.minimum` and `QSpinBox.maximum` properties should be set to reasonable minimum and maximum values for each variable. Note that the minimum actually corresponds to the special value, so the minimum property should be set at least one step lower than the actual expected minimum value.

The `QSpinBox.value` property (default value) should be set to equal the minimum, so that the variable is unmeasured by default. 

Finally, the `QSpinBox.suffix` property should be set to indicate the units of the variable, if any. Insert a leading space before the unit, so that the spinbox displays it properly. For example, if the variable is measured in millimeters, set the suffix as “ mm”. For the degree sign, do not use a space.

For `QComboBox` widgets, the only configuration necessary is to input the relevant choices in Qt Designer. One of the choices should be “Ei mitattu” (unmeasured) and it should be the default.


## Example: introducing a new variable

To introduce a new ROM variable, you must insert a new UI widget in Qt Designer, name it according to your variable, and update the SQL schema. For example, here’s the steps for introducing a new variable, Head Circumference.

* Decide on a descriptive variable name. Let’s say “HeadCirc”. The variable name must match between the SQL schema and the UI widget (and the report template, if the variable is used by the report).
* Decide on a suitable type of input widget. Head circumference is numeric and an integer step can be used, so a `QSpinBox` is a good choice.
* Open the user interface `rom_entryapp.ui` in Qt Designer. Create your widget on a suitable tab (in this case probably the anthropometric measures tab) and name it “dataHeadCirc”. Insert a text label next to the widget, so the user knows what the widget is for.
* Configure the widget by opening the `QSpinBox` properties. Set `minimum` and `maximum` to reasonable minimum and maximum values, e.g. 200 mm and 600 mm. Set `suffix` to ‘ mm’. Set the `QAbstractSpinBox` property `specialValueText` to ‘Ei mitattu’. Set the default value (value property of `QSpinBox`) to the minimum (200).
* Finally, update the SQL schema. Insert a column called “HeadCirc” in the “roms” table. This can be automatically accomplished by running `python update_rom_schema.py <database_path> -a` in the package directory.


## The `CheckableSpinBox` widget

`CheckableSpinBox` is a custom Qt widget. Its main purpose is to support variables that may be either measured or be declared to be within “normal range”, without supplying an exact value. By default, the widget will consist of a spinbox with an associated checkbox. If the checkbox is checked, it indicates “normal range”, and the spinbox is disabled. In this state, the widget will return its defaultText property as its input value. If the checkbox is unchecked, the widget functions like a normal spinbox.

The CheckableSpinBox can be configured in Qt Designer just like the other spinboxes. By default, CheckableSpinBoxes accept values from -180 to 180, with a unit (suffix) of degrees. The defaultText is set to ‘NR’ (normal range) by default. These widget defaults are set in the plugin code. To be able to use the widget in Qt Designer, you must set the environment variable `PYQTDESIGNERPATH` to point to the package directory (the directory containing `checkablespinbox_plugin.py`) before launching Qt Designer.


## Relationship between widgets and SQLite columns

The data entry widgets are the “ground truth” for the variable names used by the ROM data entry app. The SQL columns are automatically  derived from the widget names as explained above. The SQL schema must have a column for each data entry widget, or the program will raise an exception when collecting data.

If a variable is no longer needed, it can be simply deleted from the UI using Qt Designer. The corresponding column will still exist in the database table, but the program will not use it. Running the `update_rom_schema.py` script will report variables that are inconsistent between the UI and the database. It can add columns for new variables if necessary.

gaitbase doesn't do any type conversion before SQL writes. For a given variable, the type of the value might change from one write to another (i.e. from string "Ei mitattu" to float 5.0). This is possible with SQLite, since it uses dynamic typing. For most other database engines, it would be necessary to convert the values on read/write, so that static typing is maintained.


## Reporting

The ROM entry app supports reporting of the ROM values in text or Excel format. The reporting is based on templates.

The text template defines a Python variable called `text_blocks`, which is a list of strings. Each text block may contain fields referring to a ROM or patient variable. An example block would be:

```
Pituus: {AntropPituus}
Paino: {AntropPaino}
```

Fields are denoted by curly braces, as in standard Python string formatting. In this block, the ROM variables `AntropPituus` and `AntropPaino` would be replaced by their corresponding values. Additionally, if the block contains fields and all the fields have default values, the block will not be printed, to prevent cluttering the report by noninformative text.

The report may also use any other Python logic to build up the text_blocks variable. Note that the code in the report is executed by exec() without any sanity checks, so be careful. After the report code has been executed, the text blocks will be processed one by one and the variables filled in. 

In addition to the ROM variables, the report may refer to variables from the patients table (name, SSN, diagnosis etc.) to display patient information. 

The Excel report template works in a very similar fashion. Each cell may contain either text or fields denoted by curly braces referring to variables. The program will scan through the cells in the template and replace field names by the corresponding values. 

The user may define their own templates. See next section.


## Package configuration

The package has a default configuration file under `gaitbase/data/default.cfg`. On the first run of the package, this will be copied to the user’s home directory under the name `.gaitbase.cfg` (notice the leading dot). Any items defined in the user-specific configuration file then supersede the values from the default configuration file.

The most important options are the database path (`database.database`) and the template paths (`template.text` and `template.xls`).


## Random notes on SQLite

SQLite is designed for a local database file. Having the database file on a network drive is not really kosher. In this situation, a proper database server would be a more correct solution. However, database servers have their disadvantages. A server needs to be set up and maintained, the database files must be backed up etc. Additionally, it's tricky (if even possible) to set up access to a database server from outside the hospital. The network drives, on the other hand, are easy to access using VPN from home. 

While the network drive approach has worked thus far, multiple clients can cause a significant slowdown in database access. The reason is probably that Windows network filesystems disable caching when multiple clients perform read/write access on a file.

sqlite3 database writes require an EXCLUSIVE lock while they are carried out. This means that all SHARED locks must be released before writes can take place. For example, QtSql may hold SHARED locks indefinitely in some circumstances (e.g. lazy reads), preventing writes (at least writes from different processes). These problems must be worked around, i.e. locks must be released as soon as possible after reads are completed.

SQLite uses NULL for values that are completely missing (e.g. due to schema changes). These are different from default values written out by the UI. NULL means that the value was never written to the database. The program detects NULL values and converts them to default values for each variable. Note that in the Qt SQL interface, NULL values can only be read correctly by disabling PyQt type autoconversion, reading data as QVariants and using isNull() to detect NULLs. Hence, the ROM entry app does all SQL reads with the autoconversion feature disabled.

TODO:

replace functions

installation

OS compat