# Python Web Form Browser
A web browser for interacting with static or server side generated HTML web forms.

> **IMPORTANT:**
>
> Please consider this project as alpha release. Breaking changes may not always be documented or logged.

## Dependencies
The latest version of the listed libraries will work. Older versions *should* work as well. 

Requires:

* BeautifulSoup4
* html5lib

## Purpose
Many websites continue to use static HTML forms as a presentation layer to their content. This enables an application to read that content in a normalized fashion.

## Usage
The forms and their fields are stored in a set of collections. The primary parser will parse and create a collection of forms. Each form will contain a collection of its associated fields. The data is maintained in a structure that enables an application to safely post back the data to the web forms endpoint.

### Data Models
Three primary data models are used. FormData represents a single HTML web form. FormDataCollection is a collection of the fields associated to the FormData. FormDataEntry represents a single web form entity (not an element) as it would be sent to the web froms defined "action."

#### FormData
This object represents a single form having been parsed from the HTML mark-up and in a state where a web browser would submit the contents.

|Property |Meaning |
|:--------|:-------|
|name |The name provided to the form in the HTML markup. This serves only to help differentiate different forms. |
|action |The URL the form data will be posted to. |
|method |The HTTP action that will be used to send the data, default is `GET`. |
|enctype |The encoding type the HTML markup provided as how to send the form data. |
|fields |A collection of the parsed HTML form's fields. |

#### FormDataField
This object is used to represent the HTML form input fields. The parsing of the page will break each of the input elements into individual FormDataField objects. See the parsing section for more information.
|Property|Meaning|
|:-------|:------|
|name |The name attribute of the element |
|value |The value attribute of the element |
|filename |The filename to present for the file data stored in the value property. |
|is_submitable |A flag to indicate the object is selected to be submitted during form submission. |

### Parsing
A parser is provided to render the web form in the FormData model. This parser is able to render multiple forms contained in the HTML markup, and associate all fields to the correct parent form.

Fields are parsed and broken down into individual entries.
This means that an entry like the following will create a single FormDataEntry object:
```html
<input type="text" name="example" value="example value" />
```

A field like the following will create multiple FormDataEntry objects to represent each of the options:
```html
<select name="example">
  <option value="value0">Option 1</option>
  <option value="value1">Option 2</option>
</select>
```

The parser is also able to associate form fields not contained within a "form" node. Matching the specification summarized here: https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#association-of-controls-and-forms

## Examples
For all examples, an assumption is made that the markup to be parsed has already been fetched into a variable called "html_doc."

### Example 1 &ndash; Parsing form markup and accessing a field by name
```python
import html_form_parser

form_browser = html_form_parser.HtmlFormParser(html_doc)
name_family_idx = form_browser.forms[0].index_by_name("nameFamily")

print(form.forms[0][name_family_idx].value)
```


### Example 2 &ndash; Updating a "text" input
Updating the value of a text entry field is available by using the field's name attribute in the fields property. The value property can then be updated.
```python
from html_form_parser import HtmlFormParser

form_browser = HtmlFormParser(html_doc)
name_family_idx = form_browser.forms[0].index_by_name("nameFamily")
name_given_idx = form_browser.forms[0].index_by_name("nameGiven")

form_browser.forms[0][name_family_idx].value = "Smith"
form_browser.forms[0][name_given_idx].value = "John"
```

### Example 3 &ndash; Checking or selecting the "checkbox" input
Access to a checkbox, radio button, or select option can be done by providing a tuple pair containing the field's name attribute and field's value attribute. Then the is_selected property can be enabled or disabled with a boolean value.
```python
from html_form_parser import HtmlFormParser

form_browser = HtmlFormParser(html_doc)
music_genre_option_idx = form_browser.forms[0].index_by_name_value("musicGenre", "Classical")

form_browser.forms[0][music_genre_option_idx].is_submitable = True
```

### Example 4 &ndash; Re-grouping a select element
Select elements are parsed into separate `FormElement` objects. If an application needs to validate only one option is selected, this is a possible approach:
```python
from html_form_parser import HtmlFormParser

form_browser = HtmlFormParser(html_doc)

select_options = [option for option in form_browser.forms[0].fields
                  if option.name == "musicGenre" and option.is_selected]

if len(select_options) != 1:
    raise RuntimeError("too many options selected")
```
