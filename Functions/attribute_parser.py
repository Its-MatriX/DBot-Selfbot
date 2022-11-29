from re import sub


def parse_attributes(input_value):
    # EX: name = str; Just a role name & position = int; 5
    #      ⌃      ⌃          ⌃         ⌃     ⌃       ⌃   ⌃
    #      1      2          3         4     1       2   3

    # 1. Name of attribute
    # 2. Class of attribute
    # 3. Value of attribute
    # 4. Attribute splitter

    out_attributes = {}

    input_value = sub('\s+&\s+', '&', input_value)
    attribute_input_split = input_value.split('&') if '&' in input_value else [
        input_value
    ]

    for attribute in attribute_input_split:
        attribute = sub('\s+=\s+', '=', attribute)

        attribute_name = attribute.split('=', 1)[0]
        attribute_class = attribute.split(';')[0].split('=')[1]
        attribute_value = ';'.join(attribute.split(';')[1:]).strip()

        out_attributes.update(
            {attribute_name: eval(f'{attribute_class}("{attribute_value}")')})

    return out_attributes