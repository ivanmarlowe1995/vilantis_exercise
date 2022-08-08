def gen_list_str(lst, list_name):
    gen_list = [v for k, v in lst.items() if list_name in k]
    combined_str_list = '|'.join(gen_list)

    return combined_str_list


def extract_args_from_form(request, name, default='', type=str):
    list_data = request.args.get(name, default, type=type)
    return list_data
