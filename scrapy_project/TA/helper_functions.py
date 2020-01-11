def user_info_splitter(raw_user_info):
    """

    :param raw_user_info:
    :return:
    """

    user_info = {}

    splited_info = raw_user_info.split()
    for element in splited_info:
        converted_element = get_convertible_elements_as_dic(element)
        if converted_element:
            user_info[converted_element[0]] = converted_element[1]

    return user_info



def get_convertible_elements_as_dic(splited_element):
    """

    :param splited_info:
    :return:
    """

    if "=" in splited_element:
        try:
            key = splited_element.split("=")[0]
            value = splited_element.split("=")[1].replace("\"","")

            return key, value

        except:

            return None


