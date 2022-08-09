from flask import Flask, request
from dotenv import load_dotenv
from os.path import join, dirname
from utils.aws_utils import get_secret
from utils.db_utils import create_db_engine, insert_click_metadata, \
    order_by_default_query
from models.country_relation_model import CountryRelationRevised, CountryRelationScore
from models.admin_interface_model import ClickHistory
from models.shared_models import db
from models.route_models import RouteModel
import boto3
import os
import json

from utils.route_utils import gen_base_path, gen_search_path

app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
DB_SECRET_NAME = os.environ.get("DB_SECRET_NAME")
DB_SCHEMA = os.environ.get("DB_SCHEMA")
ADMIN_INTERFACE_TBL = os.environ.get("ADMIN_INTERFACE_TBL")
JSON_COLUMNS_FILE = os.environ.get("JSON_COLUMNS_FILE")

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

db_secret = get_secret(DB_SECRET_NAME, session)
db_engine = create_db_engine(db_secret)

app.config['SQLALCHEMY_DATABASE_URI'] = db_engine
country_relation = CountryRelationRevised()
country_relation_score = CountryRelationScore()
click_history = ClickHistory()
json_cols = json.load(open(JSON_COLUMNS_FILE))
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/table/admin_interface', methods=['GET', 'POST'])
def admin_interface():
    json_data = json_cols[2]
    insert_click_metadata(db)
    table_mode = RouteModel.click_history.value
    request_form = request.form
    page_num = request.args.get('page_num', 1, type=int)
    queried_data = order_by_default_query(click_history, page_num, 'id')
    template_response = gen_base_path(request_form, table_mode, queried_data, json_data)
    return template_response


@app.route('/search/admin_interface', methods=['GET', 'POST'])
def search_admin_interface():
    json_data = json_cols[2]
    insert_click_metadata(db)
    table_mode = RouteModel.click_history.value
    request_form = request.form
    template_response = gen_search_path(request_form, table_mode, click_history, json_data)
    return template_response


@app.route('/table/country_relation_raw', methods=['GET', 'POST'])
def country_relation_raw():
    json_data = json_cols[0]
    insert_click_metadata(db)
    table_mode = RouteModel.country_relationships_raw.value
    request_form = request.form
    page_num = request.args.get('page_num', 1, type=int)
    queried_data = order_by_default_query(country_relation, page_num, 'id')
    template_response = gen_base_path(request_form, table_mode, queried_data, json_data)
    return template_response


@app.route('/search/country_relation_raw', methods=['GET', 'POST'])
def search_country_relation_raw():
    json_data = json_cols[0]
    insert_click_metadata(db)
    table_mode = RouteModel.country_relationships_raw.value
    request_form = request.form
    template_response = gen_search_path(request_form, table_mode, country_relation, json_data)
    return template_response


@app.route('/table/country_relationship_score', methods=['GET', 'POST'])
def country_relationship_score():
    json_data = json_cols[1]
    insert_click_metadata(db)
    table_mode = RouteModel.country_relationships_score.value
    request_form = request.form
    page_num = request.args.get('page_num', 1, type=int)
    queried_data = order_by_default_query(country_relation_score, page_num, 'country_id')
    template_response = gen_base_path(request_form, table_mode, queried_data, json_data)
    return template_response


@app.route('/search/country_relationship_score', methods=['GET', 'POST'])
def search_country_relationship_score():
    json_data = json_cols[1]
    insert_click_metadata(db)
    table_mode = RouteModel.country_relationships_score.value
    request_form = request.form
    template_response = gen_search_path(request_form, table_mode, country_relation_score, json_data)
    return template_response


if __name__ == "__main__":
    app.run(debug=True)
