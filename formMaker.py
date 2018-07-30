import os
import json

def generate_form(fileName):
    """The main function for the formMaker program

    value: list: values to be used in program
    """
    json = __load_file(fileName)

    output = ""
    output += "<html>\n<body>\n<h1>Autogen Form</h1>\n"

    if(json["address"] is not "" and json["method"] is not ""):
        output += '<form action="' + json["address"] + '" method="' + json["method"] + '">\n'
    else:
        output += "<form>"
    
    output += "<fieldset>"
    
    if(json["items"] is not []):
        for element in json["items"]:
            output += generate_HTML(element)
    
    output += "</fieldset>"
    
    output += '<input type="submit" value="Submit">\n'
    output += "</form>\n</body>\n</html>"

    print(":::Output:::")
    print(output)

    file = open("formHtml.html", 'w')
    file.write(output)
    file.close()

def __load_file(file_name):
    """
    """
    read_in = open(file_name, 'r')
    return json.load(read_in)

def __generate_label(text):
    return "<label>" + text + "</label>\n"

def __generate_input_type(value, attr_list, attr_vals):
    output = '<input type="' + value + '"'
    for i in range(len(attr_list)):
        output += __generate_input_attr(attr_list[i], attr_vals[i])

    output += ">"

    return output

def __generate_input_attr(name, value):
    return name + '="' + value + '" '

def __generate_break():
    return "<br>"

def generate_HTML(element):
    """

    """
    type_of = element["supertype"]

    if type_of == "text":
        return generate_text_type(element)
    if type_of == "choice":
        return generate_radio(element)

    return ""

def generate_text_type(element):
    output = __generate_label(element["label"])
    output += __generate_input_type(
        element["type"],
        ["name","id","placeholder"],
        [element["name"], element["id"], element["placeholder"]]
        )
    output += __generate_break()

    return output

def generate_password(element):
    output = __generate_label(element["label"])
    output += __generate_input_type(
        "password",
        ["name", "id", "placeholder"],
        [element["name"], element["id"], element["placeholder"]]
        )
    output += __generate_break()

    return output

def generate_radio(element):
    output = __generate_label(element["label"]) + __generate_break()
    output += "<fieldset>"
    for item in element["options"]:
        output += __generate_input_type(
            "radio",
            ["name", "id"],
            [element["name"], item["value"]]
            )
        output += __generate_label(item["label"])
        output += __generate_break()

    output += "</fieldset>"
    return output

def generate_text_area(element):
    """

    """
    pass

def generate_option(element):
    """

    """
    pass

generate_form("text.json")
