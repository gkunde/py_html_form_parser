# Python HTML Form Parser
Parse any static HTML web form into a data model.

> **IMPORTANT:**
>
> Please consider this project as alpha release. Breaking changes may not always be documented or logged.

## Dependencies
The latest version of the listed libraries will work. Older versions *should* work as well. 

Requires:
* BeautifulSoup4
* html5lib

## Purpose
Many websites continue to use static HTML forms as a primary interface to their applications. The goal with this library is to provide a client application with the ability to interact with a web form like a traditional web browser provides.

## Usage
The fields and their attributes are stored in a flattened collection. The models follow how the data would be presented if a traditional web browser were to submit the form. This means that element collections, such as "select," are split into individual elements. FormElement's provide properties to assist in re-grouping element sets.

### FormElement Properties
|Property|Meaning|
|:-------|:------|
|primary_type |Maps to an element's tag such as: button, input, select, or textarea|
|secondary_type |Maps to an element's type attribute |
|name |The name attribute of the element |
|value |The value attribute of the element |
|is_selected |A flag to indicate the element is selected to be submitted during form submission. |
|binary_path |A local file path, to a file that would be submitted with the form data. When used, the "name" property is intended to be used as the destination file name. |

## Examples
For all examples, an assumption is made that the markup to be parsed has already been fetched into a variable called "html_doc."

### Example 1 &ndash; Parsing form markup and accessing a field by name
```python
import html_form_parser

form = html_form_parser.Form(html_doc)
name_family = form.fields["familyName"].value

print(name_family)
```


### Example 2 &ndash; Updating a "text" input
Updating the value of a text entry field is available by using the field's name attribute in the fields property. The value property can then be updated.
```python
from html_form_parser import Form

form = Form(html_doc)
form.fields["familyName"].value = "Smith"
form.fields["givenName"].value = "John"
```

### Example 3 &ndash; Checking or selecting the "checkbox" input
Access to a checkbox, radio button, or select option can be done by providing a tuple pair containing the field's name attribute and field's value attribute. Then the is_selected property can be enabled or disabled with a boolean value.
```python
from html_form_parser import Form

form = Form(html_doc)
form.fields[("musicGenre", "Classical", )].is_selected = True
```

### Example 4 &ndash; Updating the properties of a field by index
All of the form elements are available with an integer index. The fields in the collection are not sorted and are not stored in the order they are presented in the HTML markup. This approach is useful if the calling method has built its own index of the fields.
```python
from html_form_parser import Form

form = Form(html_doc)
form.fields[0].value = "Smith"
form.fields[1].value = "John"
form.fields[8].is_selected = True
```

### Example 5 &ndash; Selecting a form by name
If the markup contains two form elements, the desired form can be selected by passing a value to the name parameter.
```python
from html_form_parser import Form

form = Form(html_doc, name="alternateForm")
```

### Example 6 &ndash; Re-grouping a select element
Select elements are parsed into separate `FormElement` objects. If an application needs to validate only one option is selected, this is a possible approach:
```python
from html_form_parser import Form

form = Form(html_doc)

select_options = [option for option in form.fields 
                  if option.primary_type == "select"
                          and option.name == "example"
                          and option.is_selected]

if len(select_options) != 1:
    raise RuntimeError("too many options selected")
```