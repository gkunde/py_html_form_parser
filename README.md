# Python HTML Form Parser

> **IMPORTANT:**
>
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
For all examples, an assumption is made that the markup to be parsed has already been fetched into a variable called "html_doc."

### Example 1 - Parsing form markup and accessing a field by name
```python
import html_form_parser

form = html_form_parser.Form(html_doc)
name_family = form.fields["familyName"].value

print(name_family)
```


### Example 2 - Updating a "text" input
Updating the value of a text entry field is available by using the field's name attribute in the fields property. The value property can then be updated.
```python
from html_form_parser import Form

form = Form(html_doc)
form.fields["familyName"].value = "Smith"
form.fields["givenName"].value = "John"
```

### Example 3 - Checking the "checkbox" input
Access to a checkbox, radio button, or select option can be done by providing a tuple pair containing the field's name attribute and field's value attribute. Then the is_selected property can be enabled or disabled with a boolean value.
```python
from html_form_parser import Form

form = Form(html_doc)
form.fields[("musicGenre", "Classical", )].is_selected = True
```

### Example 4 - Updating the properties of a field by index
All of the form elements are available with an integer index. The fields in the collection are not sorted and are not stored in the order they are presented in the HTML markup. This approach is useful if the calling method has built it's own index of the fields.
```python
from html_form_parser import Form

form = Form(html_doc)
form.fields[0].value = "Smith"
form.fields[1].value = "John"
form.fields[8].is_selected = True
```

### Example 5 - Selecting form by name
If the markup contains two form elements, the desired form can be selected by passing a value to the name parameter.
```python
from html_form_parser import Form

form = Form(html_doc, name="alternateForm")
```
