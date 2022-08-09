from flask import request, redirect, url_for, render_template
from models.gen_utils import gen_list_str, extract_args_from_form
from utils.db_utils import gen_query_statement, gen_order_clause
import json
import inspect


def gen_base_path(request_form,
                  table_mode,
                  query_data,
                  json_data
                  ):

    col_json_dict = json_data
    col_json_raw = json.dumps(json_data).encode('utf8')
    page_name = 'gen_table_interface'
    if request.method == 'POST':
        if request.form['action'] == 'Search Data':
            field_list = gen_list_str(request_form, 'field')
            expr_list = gen_list_str(request_form, 'select_expr')
            col_list = gen_list_str(request_form, 'select_col')
            col_order_list = gen_list_str(request_form, 'order_col')
            sort_order_list = gen_list_str(request_form, 'order_sort')

            return redirect(
                url_for('search_{}'.format(table_mode),
                        page_num=1,
                        field_list=field_list,
                        expr_list=expr_list,
                        col_list=col_list,
                        col_order_list=col_order_list,
                        sort_order_list=sort_order_list,
                        table_mode=table_mode,
                        col_json_raw=col_json_raw
                        )
            )

    else:
        return render_template('{}.html'.format(page_name),
                               data=query_data,
                               table_mode=table_mode,
                               col_json_dict=col_json_dict)


def gen_search_path(request_form,
                    table_mode,
                    model,
                    json_data):
    col_json_dict = json_data
    col_json_raw = json.dumps(json_data).encode('utf8')
    page_name = 'search_table_interface'
    if request.method == 'POST':
        if request.form['action'] == 'Search Data':
            field_list = gen_list_str(request_form, 'field')
            expr_list = gen_list_str(request_form, 'select_expr')
            col_list = gen_list_str(request_form, 'select_col')
            col_order_list = gen_list_str(request_form, 'order_col')
            sort_order_list = gen_list_str(request_form, 'order_sort')

            return redirect(
                url_for('search_{}'.format(table_mode),
                        page_num=1,
                        field_list=field_list,
                        expr_list=expr_list,
                        col_list=col_list,
                        col_order_list=col_order_list,
                        sort_order_list=sort_order_list,
                        table_mode=table_mode,
                        col_json_raw=col_json_raw
                        )
            )

    else:
        page_num = extract_args_from_form(request, 'page_num', 1, type=int)
        field_list = extract_args_from_form(request, 'field_list')
        expr_list = extract_args_from_form(request, 'expr_list')
        col_list = extract_args_from_form(request, 'col_list')
        col_order_list = extract_args_from_form(request, 'col_order_list')
        sort_order_list = extract_args_from_form(request, 'sort_order_list')

        field_list_split = field_list.split('|')
        expr_list_split = expr_list.split('|')
        col_list_split = col_list.split('|')
        col_order_list_split = col_order_list.split('|')
        sort_order_list_split = sort_order_list.split('|')
        queried_data = gen_query_statement(field_list_split, expr_list_split, col_list_split, model)
        ordered_data = gen_order_clause(col_order_list_split, sort_order_list_split, queried_data, model)
        final_data = ordered_data.paginate(per_page=10, page=page_num, error_out=False)

        return render_template('{}.html'.format(page_name),
                               data=final_data,
                               field_list=field_list,
                               expr_list=expr_list,
                               col_list=col_list,
                               col_order_list=col_order_list,
                               sort_order_list=sort_order_list,
                               table_mode=table_mode,
                               col_json_dict=col_json_dict
                               )
