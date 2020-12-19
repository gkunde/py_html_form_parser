# Python HTML Form Parser

> [!IMPORTANT]
> Please consider this project as alpha release. Breaking changes may not always be logged.

A library for parsing a static HTML form into a model. The purpose is to enable capture of form data, read and update values, and provide a set of serialize methods for storing or submitting the form data.

## Dependencies
To use the Form Manager, you must have:
* BeautifulSoup4
* html5lib

There are no dependencies for using the models directly.

## Usage
A library that enables storage of scraped data from a static or server side dynamically generated HTML forms. There is no support for client side dynamically generated HTML forms.

The primary use is with the `FormManager` class, which allows a string value containing HTML to be parsed. The `FormManager` also provides convience methods for manging the forms, especially useful when multiple forms are present.

The model classes can also be used directly, population can be done manually or through the convience methods offered.

All models provide two methods for parsing:
* `from_dict()` - These methods are capable of reading in a dictionary containing the attributes and elements that have been parsed. These compliment the `to_dict()` methods provided in the models.
* `from_bs4()` - These methods accept a BeautifulSoup4 (or compatible) object and extract attributes and children elements with in.

## Examples
### Example 1 - Use with FormManager() class
```python
import urllib.request

import html_form_parser

html_doc = urllib.request.urlopen('https://www.example.com').page_read()

form_manager = html_form_parser.FormManager(html_doc)
name_family = form_manager.forms[0].get_field_by_name("familyName").values[0].value

print(name_family)
```

### Example 2 - Using the data models directly
```python
import urllib.request

import bs4.BeautifulSoup

from html_form_parser.form import Form

html_doc = urllib.request.urlopen('https://www.example.com').page_read()

bs4_form = bs4.BeautifulSoup(html_doc, "html5lib").find("form")

form = Form.from_bs4(bs4_form)
name_family = form.get_field_by_name("familyName").values[0].value

print(name_family)
```
