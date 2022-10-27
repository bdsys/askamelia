from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import requests, os
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
    
# @main.route('/')
# def index():
#     return redirect(url_for('auth.invitation'))
    

@main.route('/profile')
@login_required # Decorator to protect route from unauthenticated users
def profile():
    # curent_user represents the ORM object, User in this case, that login_manager
    # used to authenticate the user via signed cookie on the client side
    return render_template('profile.html', name=current_user.name)
    
@main.route('/subject')
@login_required # Decorator to protect route from unauthenticated users
def subject():

    # Code here to show a simple list of subjects from DDB table
    # Singular right now.
    
    aa_api_get_db_items_url = os.getenv('AA_API_GET_DB_ITEMK_URL')
    
    response_aa_api_get_db_items = requests.get(aa_api_get_db_items_url)
    
    response_json_dict = response_aa_api_get_db_items.json()
    
    render_subject = response_json_dict['subject']
    
    return render_template(
        'subject.html',
        render_subject=render_subject,
    )

# https://pythonbasics.org/flask-tutorial-routes/
@main.route('/update/<subject>')
@login_required # Decorator to protect route from unauthenticated users
def update(subject):
    
    # Code here to render the DDB table and provide updatable fields and update button
    
    aa_api_get_db_item_by_pk_url = os.getenv('AA_API_GET_DB_ITEMS_BY_PK_URL')
    aa_api_update_ddb_item_by_pk_url = os.getenv('AA_API_UPDATE_DDB_ITEM_BY_PK_URL')
    
    aa_ddb_get_item_by_pk_request_body_dict = { 
        "pk": subject,
    }
    
    response_aa_api_update_ddb_item_by_pk = requests.post(
        aa_api_get_db_item_by_pk_url, 
        json=aa_ddb_get_item_by_pk_request_body_dict,
    )

    response_aa_api_get_db_item_by_pk = requests.get(aa_api_get_db_item_by_pk_url)
    
    # if status code...
    
    response_json_dict = response_aa_api_get_db_item_by_pk.json()
    
    render_subject = response_json_dict['subject']
    render_birth_date = response_json_dict['birth_date']
    render_favorite_color = response_json_dict['favorite_color']
    render_test_value = response_json_dict['test_value']
    render_favorite_dog_breed = response_json_dict['favorite_dog_breed']
    
    return render_template(
        'update.html',
        render_subject=render_subject,
        render_birth_date = render_birth_date,
        render_favorite_color = render_favorite_color,
        render_test_value = render_test_value,
        render_favorite_dog_breed = render_favorite_dog_breed,
    )
    
@main.route('/update/<subject>', methods=['POST'])
@login_required # Decorator to protect route from unauthenticated users
def update_post(subject):

    # Form input handling
    # form_input_subject = request.form.get('subject')
    form_input_subject = subject
    form_input_birth_date = request.form.get('password')
    form_input_favorite_color = request.form.get('favcolor')
    form_input_test_value = request.form.get('testvalue')
    form_input_favorite_dog_breed = request.form.get('favdogbreed')
    
    aa_api_update_ddb_item_by_pk_url = os.getenv('AA_API_UPDATE_DDB_ITEM_BY_PK_URL')
    
    aa_ddb_update_dict = { 
        # "subject": form_input_subject,
        "subject": subject,
        'birth_date': form_input_birth_date,
        'favorite_color': form_input_favorite_color,
        'test_value': form_input_test_value,
        'favorite_dog_breed': form_input_favorite_dog_breed,
    }
    
    response_aa_api_update_ddb_item_by_pk = requests.post(
        aa_api_update_ddb_item_by_pk_url, 
        json=aa_ddb_update_dict,
    )
    
    response_json_dict = response_aa_api_update_ddb_item_by_pk.json()
    response_json_dict_ddb_updated = response_json_dict['operation_message']
    
    render_subject = response_json_dict_ddb_updated['subject']
    render_birth_date = response_json_dict_ddb_updated['birth_date']
    render_favorite_color = response_json_dict_ddb_updated['favorite_color']
    render_test_value = response_json_dict_ddb_updated['test_value']
    render_favorite_dog_breed = response_json_dict_ddb_updated['favorite_dog_breed']
    
    return render_template(
        'update.html',
        render_subject=render_subject,
        render_birth_date = render_birth_date,
        render_favorite_color = render_favorite_color,
        render_test_value = render_test_value,
        render_favorite_dog_breed = render_favorite_dog_breed,
    )
