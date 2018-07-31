"""A module to generate html forms from json file.

"""

import json


def __load_file(file_name):
    """Loads a json file

    """
    read_in = open(file_name, 'r')
    return json.load(read_in)


def __generate_label(text):
    """Generates a label with a given text as the innerHTML

    """
    return "<label>" + text + "</label>\n"


def __generate_input_type(value, attr_list, attr_vals):
    """Generates an input tag based on given information

    """
    output = '<input type="' + value + '"'
    for i in range(len(attr_list)):
        output += __generate_input_attr(attr_list[i], attr_vals[i])

    output += ">"

    return output


def __generate_input_attr(name, value):
    """Generates an html tag attribute and value

    """
    return name + '="' + value + '" '


def __generate_break():
    """Creates a html break tag

    """
    return "<br>"


def generate_html(element):
    """Generates html based on type

    """
    try:
        type_of = element["supertype"]
    except KeyError:
        return '<h3 style="color:red";>Supertype keywork missing in Json</h3>'

    if type_of == "text":
        return generate_text_type(element)
    if type_of == "choice":
        return generate_choice(element)

    return '<h3 style="color:red;">Invalid supertype ' + element["supertype"] + "</h3>"


def generate_text_type(element):
    """Generates text based non-choice input items

    """
    output = __generate_label(element["label"])
    attributes = element["attributes"]
    keys = list()
    for key in attributes.keys():
        keys.append(key)

    values = list()
    for key in keys:
        values.append(attributes[key])

    output += __generate_input_type(
        element["type"],
        keys,
        values
    )

    output += __generate_break()

    return output


def generate_choice(element):
    """Generates radio button inputs

    """
    output = __generate_label(element["label"]) + __generate_break()
    output += "<fieldset>"
    for item in element["options"]:
        output += __generate_input_type(
            element["type"],
            ["name", "id"],
            [element["name"], item["value"]]
        )

        output += __generate_label(item["label"])
        output += __generate_break()

    output += "</fieldset>"
    return output


def generate_form(file_name):
    """The main function for the formMaker program

    file_name: string: the name of the json file to be imported
    """
    f_json = __load_file(file_name)

    output = ""
    output += "<html>\n<body>\n<h1>Autogen Form</h1>\n"

    if(f_json["address"] is not str() and f_json["method"] is not str()):
        output += '<form action="' + f_json["address"] + '" method="' + f_json["method"] + '">\n'
    else:
        output += "<form>"
    output += "<fieldset>"
    if f_json["items"] is not list():
        for element in f_json["items"]:
            output += generate_html(element)

    output += "</fieldset>"
    output += '<input type="submit" value="Submit">\n'
    output += "</form>\n</body>\n</html>"

    print(":::Output:::")
    print(output)

    file = open("formHtml.html", 'w')
    file.write(output)
    file.close()


generate_form("text.json")
