from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import requests, os
from . import db

main = Blueprint('main', __name__)

# @main.route('/')
# def index():
#     return render_template('index.html')
    
@main.route('/')
def index():
    return redirect(url_for('auth.invitation'))

# @main.route('/profile')
# @login_required # Decorator to protect route from unauthenticated users
# def profile():
#     # curent_user represents the ORM object, User in this case, that login_manager
#     # used to authenticate the user via signed cookie on the client side
#     return render_template('profile.html', name=current_user.name)
    
@main.route('/subject')
@login_required # Decorator to protect route from unauthenticated users
def subject():

    # Code here to show a simple list of subjects from DDB table
    
    aa_api_get_db_items_url = os.getenv('AA_API_GET_DB_ITEMS_URL')
    
    response_aa_api_get_db_items = requests.get(aa_api_get_db_items_url)
    
    response_json_dict = response_aa_api_get_db_items.json()
    
    print(f'DEBUG -- response_json_dict -- {response_json_dict}')
    
    render_subjects = []
    num_names = 1
    for subject_name in response_json_dict:
        print(f"Name {num_names}: {response_json_dict[subject_name]['subject']}")
        print("Sanitizing string...")
        
        sanitized_string = response_json_dict[subject_name]['subject'].replace("_"," ")
        
        print(f'Sanitized string -- {sanitized_string}')
        
        print("Beautifying string...")
        character_count = 0
        for character in sanitized_string:
            if character_count == 0:
                formatted_name = character.upper()
            elif capitalize_next_char:
                formatted_name =  formatted_name + character.upper()
            else:
                formatted_name = formatted_name + character
                
            if character == " ":
                capitalize_next_char = True
            else:
                capitalize_next_char = False
            
                
            character_count += 1
        
        print(f'Formatted name: {formatted_name}')
        print(f"Full name CSV: {formatted_name},{response_json_dict[subject_name]['subject']}")
        
        render_subjects.append(f"{formatted_name},{response_json_dict[subject_name]['subject']}")
        num_names +=1
    
    return render_template(
        'subject.html',
        render_subjects=render_subjects
    )

# https://pythonbasics.org/flask-tutorial-routes/
@main.route('/update/<subject>')
@login_required # Decorator to protect route from unauthenticated users
def update(subject):
    
    # Code here to render the DDB table and provide updatable fields and update button
    
    aa_api_get_db_item_by_pk_url = os.getenv('AA_API_GET_DB_ITEMS_BY_PK_URL')
    aa_api_update_ddb_item_by_pk_url = os.getenv('AA_API_UPDATE_DDB_ITEM_BY_PK_URL')
    
    aa_ddb_get_item_by_pk_request_body_dict = { 
        'pk': subject,
    }
    
    response_aa_api_update_ddb_item_by_pk = requests.post(
        aa_api_get_db_item_by_pk_url, 
        json=aa_ddb_get_item_by_pk_request_body_dict,
    )

    # if status code...
    
    response_json_dict = response_aa_api_update_ddb_item_by_pk.json()
    
    print(f'DEBUG -- {subject}')
    print(f'DEBUG -- {response_json_dict}')
    
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

    # TODO -- Make this dynamic somehow...
    # Form input handling
    # form_input_subject = request.form.get('subject')
    form_input_subject = subject
    form_input_birth_date = request.form.get('birthdate')
    form_input_favorite_color = request.form.get('favcolor')
    form_input_test_value = request.form.get('testvalue')
    form_input_favorite_dog_breed = request.form.get('favdogbreed')
    
    aa_api_update_ddb_item_by_pk_url = os.getenv('AA_API_UPDATE_DDB_ITEM_BY_PK_URL')

    aa_ddb_update_dict_birthdate = { 
        "pk": 'subject',
        "pk_value": subject,
        "update_key": "birth_date",
        'update_value': form_input_birth_date,
    }
    
    aa_ddb_update_dict_favcolor = { 
        "pk": 'subject',
        "pk_value": subject,
        "update_key": "favorite_color",
        'update_value': form_input_favorite_color,
    }
    
    aa_ddb_update_dict_testvalue = { 
        "pk": 'subject',
        "pk_value": subject,
        "update_key": "test_value",
        'update_value': form_input_test_value,
    }
    
    aa_ddb_update_dict_favdogbreed = { 
        "pk": 'subject',
        "pk_value": subject,
        "update_key": "favorite_dog_breed",
        'update_value': form_input_favorite_dog_breed,
    }
    
    response_aa_ddb_update_dict_birthdate = requests.post(
        aa_api_update_ddb_item_by_pk_url, 
        json=aa_ddb_update_dict_birthdate,
    )

    response_aa_ddb_update_dict_favcolor = requests.post(
        aa_api_update_ddb_item_by_pk_url, 
        json=aa_ddb_update_dict_favcolor,
    )

    response_aa_ddb_update_dict_testvalue = requests.post(
        aa_api_update_ddb_item_by_pk_url, 
        json=aa_ddb_update_dict_testvalue,
    )

    response_aa_ddb_update_dict_favdogbreed = requests.post(
        aa_api_update_ddb_item_by_pk_url, 
        json=aa_ddb_update_dict_favdogbreed,
    )
    
    # Check status codes
    # if status code ...
    
    response_json_dict = response_aa_ddb_update_dict_favdogbreed.json()
    response_json_dict_ddb_updated = response_json_dict['operation_message']
    
    render_subject = response_json_dict_ddb_updated['subject']
    render_birth_date = response_json_dict_ddb_updated['birth_date']
    render_favorite_color = response_json_dict_ddb_updated['favorite_color']
    render_test_value = response_json_dict_ddb_updated['test_value']
    render_favorite_dog_breed = response_json_dict_ddb_updated['favorite_dog_breed']
    
    return redirect(url_for('main.update'))
