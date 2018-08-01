"""A module to generate html forms from json file.

@Author: Dustin Roan dustin.a.roan@gmail.com
@Version: 7/31/2018
"""

import json


def __handle_error_and_exit(message, error):
    """Prints out errors and custom message when and error occurs. Exits the program

    @param message: string - a message to display to the user.
    @param error: Error - the error created
    """

    print(message)
    print("Error Occured: {}".format(error))
    exit(1)

def __load_file(file_name):
    """Loads a json file

    @param file_name: string - the name of the json file
    @return: dict - a json loaded into python dict
    """
    try:
        read_in = open(file_name, 'r')
        jobj = json.load(read_in)
        read_in.close()
    except IOError as error:
        message = "Unable to open {}.\n".format(file_name)
        message += "Make sure that {} exists in ".format(file_name) +\
                    "the current working directory."
        __handle_error_and_exit(message, error)

    return jobj

def __save_file(output, file_name):
    """Saves output to given file
    
    @param output: string - the html to be saved to file
    @param file_name: string - the name of the html file to be created (no extention)
    """
    try:
        file = open("{}.html".format(file_name), 'w')
        file.write(output)
        file.close()
    except IOError as error:
        message = "Unable to create {}\n.".format(file_name)
        message += "Make sure you have write permissions in " +\
                    "the current working directory."
        __handle_error_and_exit(message, error)


def __generate_label(text):
    """Generates a label with a given text as the innerHTML

    @param text: string - the text to be shown in a label
    @return: string - label and its included text
    """
    return "<label>" + text + "</label>\n"


def __generate_input_type(type_of, attr_list, attr_vals):
    """Generates an input tag based on given information

    @param type_of: string - name of the input type
    @param attr_list: list - all the attributes to add to the input tag
    @param attr_vals: list - all of the values of the attribues to add to input tag
    @return output: string - generated input tag
    """
    output = '<input type="{}"'.format(type_of)
    for i in range(len(attr_list)):
        output += __generate_input_attr(attr_list[i], attr_vals[i])

    output += ">"

    return output


def __generate_input_attr(name, value):
    """Generates an html tag attribute and value

    @param name: string - the name of html input tag attribute
    @param value: string - the value associated with an html input tag attribute
    @return: string - an html tag attribute and value
    """
    return '{}="{}"'.format(name,value)


def __generate_break():
    """Creates a html break tag"""
    return "<br>"


def generate_html(element):
    """Generates html based on type

    @param element: dict - dictionary containing information about an input tag
    @return: string - generated html of an element or error warning
    """
    try:
        type_of = element["supertype"]
    except KeyError:
        return '<h3 style="color:red";>Supertype keywork missing in Json</h3>'

    if type_of == "text":
        return generate_simple_type(element)
    if type_of == "choice":
        return generate_choice(element)

    return '<h3 style="color:red;">Invalid supertype {}!</h3>'.format(element["supertype"])


def generate_simple_type(element):
    """Generates text based non-choice input items

    @param element: dict - dictionary containing information about an input tag
    @return output: string - html generated for simple type elements
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

    @param element: dict - dictionary containing information about an input tag
    @return output: string - generated html of choice type items
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

    @param file_name: string - the name of the json file to be imported
    """
    f_json = __load_file(file_name)

    output = "<html>\n<body>\n<h1>Autogen Form</h1>\n"

    if(f_json["address"] is not str() and f_json["method"] is not str()):
        output += '<form action="{}" method="{}">\n'.format(f_json["address"],
                                                            f_json["method"])

    else:
        output += "<form>"
    output += "<fieldset>"
    if f_json["items"] is not list():
        for element in f_json["items"]:
            output += generate_html(element)

    output += "</fieldset>"
    output += '<input type="submit" value="Submit">\n'
    output += "</form>\n</body>\n</html>"

    __save_file(output, "auto_form")

generate_form("text.json")
