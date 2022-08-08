from flask import request
from datetime import datetime
from sqlalchemy import and_, or_, not_
from models.admin_interface_model import ClickHistory


def create_db_engine(secret):
    username = secret["username"]
    password = secret["password"]
    host = secret["host"]
    port = secret["port"]

    final_str = 'postgresql://{username}:{password}@{host}:{port}/postgres'.format(
        username=username,
        password=password,
        host=host,
        port=port
    )

    return final_str


def gen_order_clause(col_list, order_list, query_model, model_class):
    model_class = type(model_class)
    sql_expr_list = []
    for index, item in enumerate(col_list):
        order_item = order_list[index]
        col_item = col_list[index]
        col_attr = getattr(model_class, col_item)

        if order_item == 'desc':
            col_expr = col_attr.desc()
        else:
            col_expr = col_attr.asc()

        sql_expr_list.append(col_expr)

    final_order_by = query_model.order_by(*sql_expr_list)
    return final_order_by


def gen_query_statement(field_list, expr_list, col_list, model):
    model_class = type(model)
    print("model:{}".format(model_class))
    sql_expr_list = []

    for index, item in enumerate(field_list):
        expr_item = expr_list[index]
        val_item = field_list[index]
        col_item = col_list[index]
        col_attr = getattr(model_class, col_item)

        if expr_item == "=":
            col_expr = col_attr == val_item
        elif expr_item == ">=":
            col_expr = col_attr <= val_item
        elif expr_item == "<=":
            col_expr = col_attr >= val_item
        elif expr_item == ">":
            col_expr = col_attr < val_item
        elif expr_item == "<":
            col_expr = col_attr > val_item
        elif expr_item == "like":
            col_expr = col_attr.like('%' + val_item + '%')
        else:
            val_list = val_item.split(',')
            col_expr = col_attr.in_(val_list)

        sql_expr_list.append(col_expr)

    final_query_str = model_class.query.filter(and_(*sql_expr_list))
    # print("type:{}".format(type(final_query_str)))
    # print(str(final_query_str))
    return final_query_str


def insert_click_metadata(db):
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    http_referrer = request.referrer
    method_request = request.method
    now = datetime.now()
    dt_now = now.strftime("%d/%m/%Y %H:%M:%S")
    click_history_response = ClickHistory(user_ip_address=ip_addr,
                                          date_created=dt_now,
                                          request_type=method_request,
                                          request_referrer=http_referrer)
    db.session.add(click_history_response)
    db.session.commit()


def order_by_default_query(model, web_page_num, field_order, page_size=10):
    model_type = type(model)
    field_order_attr = getattr(model_type, field_order)
    queried_data = model.query.order_by(field_order_attr.asc()).paginate(per_page=page_size,
                                                                         page=web_page_num,
                                                                         error_out=False)
    return queried_data
