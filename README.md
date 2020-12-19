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
name_family = form_manager.forms[0].fields["familyName"].value

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
name_family = form.fields["familyName"].value

print(name_family)
```

### Example 3 - Updating a "text" input
Updating the value of a text entry field is available by using the field's name attribute in the fields property. The value property can then be updated.
```python
import urrlib.request

import bs4.BeautifulSoup

from html_form_parser import FormManager

html_doc = urllib.request.urlopen('https://www.example.com').page_read()

form_manager = FormManager(html_doc)
form_manager.form[0].fields["familyName"].value = "Smith"
form_manager.form[0].fields["givenName"].value = "John"
```

### Example 4 - Checking the "checkbox" input
Access to a checkbox, radio button, or select option can be done by providing a tuple pair containing the field's name attribute and field's value attribute. Then the is_selected property can be enabled or disabled with a boolean value.
```python
import urrlib.request

import bs4.BeautifulSoup

from html_form_parser import FormManager

html_doc = urllib.request.urlopen('https://www.example.com').page_read()

form_manager = FormManager(html_doc)
form_manager.form[0].fields[("musicGenre", "Jazz", )].is_selected = True
```

### Example 5 - Updating the properties of a field by index
All of the form elements are available with an integer index. The fields in the collection are not sorted and are not stored in the order they are presented in the HTML markup. This approach is useful if the calling method has built it's own index of the fields.
```python
import urrlib.request

import bs4.BeautifulSoup

from html_form_parser import FormManager

html_doc = urllib.request.urlopen('https://www.example.com').page_read()

form_manager = FormManager(html_doc)
form_manager.form[0].fields[0].value = "Smith"
form_manager.form[0].fields[1].value = "John"
form_manager.form[0].fields[8].is_selected = True
```
