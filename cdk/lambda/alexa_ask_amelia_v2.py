import datetime, os, requests 

# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular 
# Request are handled by functions such as on_launch(event) and 
# intent_scheme(event).
def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
        
# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "You an ask Amelia Cat about her or her friends and family. Try saying Ask Amelia Cat how old she is."
    reprompt_MSG = "Try asking me Ask Amelia how old she is or Ask Amelia what her favorite kind of dog."
    # card_TEXT = "Pick a chess payer."
    # card_TITLE = "Choose a chess player."
    card_TEXT = "Ask Amelia \n Try asking me Ask Amelia how old she is or Ask Amelia what her favorite kind of dog."
    card_TITLE = "Ask Amelia"
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")

# The intent_scheme(event) function handles the Intent Request. 
# Since we have a few different intents in our skill, we need to 
# configure what this function will do upon receiving a particular 
# intent. This can be done by introducing the functions which handle 
# each of the intents.
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']
    
    print('Checking event for any slots...')
    if event['request']['intent']['slots']:
        print('Found slots in the event.')
        print('Setting subject name to variable for requests...')
        print('Checking if the slot was resolved...')
        resolution_status_code = event['request']['intent']['slots']['subject']['resolutions']['resolutionsPerAuthority'][0]['status']['code']
        
        if resolution_status_code == "ER_SUCCESS_MATCH":
            subject_name =event['request']['intent']['slots']['subject']['value']
            
        elif resolution_status_code == "ER_SUCCESS_NO_MATCH":
            print('Unable to resolve slot!')
            return stop_the_skill(event)
                
        else:
            print('Unable to resolve slot! Unknown code.')
            return stop_the_skill(event)
                
    else:
        print('No slots found! Unable to use this skill without slots.')
        return stop_the_skill(event)
    
# Alexa device request data model
# 	"request": {
# 		"type": "IntentRequest",
# 		"requestId": "amzn1.echo-api.request.81a6ff44-6513-4e22-be51-3c39826e9a5c",
# 		"locale": "en-US",
# 		"timestamp": "2022-11-22T21:19:56Z",
# 		"intent": {
# 			"name": "favoriteColor",
# 			"confirmationStatus": "NONE",
# 			"slots": {
# 				"subject": {
# 					"name": "subject",
# 					"value": "her",
# 					"resolutions": {
# 						"resolutionsPerAuthority": [
# 							{
# 								"authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.e6ea2846-360e-4135-b33c-eb9f0a8b16ad.subjectName",
# 								"status": {
# 									"code": "ER_SUCCESS_MATCH" # or "ER_SUCCESS_NO_MATCH"
# 								},
#                               ...


    if intent_name == "howOld":
        return howOldGeneral(subject_name)
        
    elif intent_name == "howManyMonths":
        return howManyMonths(subject_name)
        
    elif intent_name == "howManyWeeks":
        return howManyWeeks(subject_name)
        
    elif intent_name == "favoriteColor":
        return favoriteColor(subject_name)
        
    elif intent_name == "favoriteTypeOfDog":
        return favoriteTypeOfDog(subject_name)
        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
        
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
        
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)

# Here we define the intent handler functions

def howOldGeneral(subject):
    
    birthdate_formatted = get_formatted_birthdate_object_from_table(subject)
    
    reprompt_MSG = "Do you want to hear Amelia Cat's age again?"
    card_TITLE = "You've asked about Amelia's age. Ages less than 2 years will be reported in months. Otherwise, the age will be reported in years and months."
    
    today_date = datetime.date.today()
    years_old = today_date.year - birthdate_formatted.year
    month_difference = today_date.month - birthdate_formatted.month
    day_differene = birthdate_formatted.day - today_date.day
    weeks_difference = round(day_differene/7)
    days_remainder = day_differene%7

    # If date is more than 2 years, return years
    
    if(years_old > 2):
        
        if(month_difference == 0):
            string_response = f"Amelia Cat is {years_old} years old exactly."
            # card_TEXT = "Amelia Cat is {years_old} years old exactly."
        else:
            string_response = f"Amelia Cat is {years_old} year and {month_difference} months old."

    elif(years_old == 0):
        if(weeks_difference == 0):
            string_response = f"Amelia Cat is {month_difference} months old exactly."
        else:
            string_response = f"Amelia Cat is {month_difference} months and {weeks_difference} weeks old."

    else:
        string_response = f"Something went wrong."

    card_TEXT = string_response

    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)
    
def howManyMonths(subject):
    
    birthdate_formatted = get_formatted_birthdate_object_from_table(subject)
    
    reprompt_MSG = "Do you want to hear Amelia Cat's age in months again?"
    card_TITLE = "You've asked about Amelia's age in months."
    
    today_date = datetime.date.today()
    month_difference = today_date.month - birthdate_formatted.month
    day_differene = birthdate_formatted.day - today_date.day
    weeks_difference = round(day_differene/7)
    days_remainder = day_differene%7
    
    if(weeks_difference == 0):
        string_response = f"Amelia Cat is {month_difference} months old exactly."
    else:
        string_response = f"Amelia Cat is {month_difference} months and {weeks_difference} weeks old."
    
    card_TEXT = string_response
    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)

def howManyWeeks(subject):
    
    birthdate_formatted = get_formatted_birthdate_object_from_table(subject)
    
    reprompt_MSG = "Do you want to hear Amelia Cat's age in weeks again?"
    card_TITLE = "You've asked about Amelia's age in weeks."
    card_TEXT = "You've asked about Amelia's age in weeks."
    
    today_date = datetime.date.today()
    years_old = today_date.year - birthdate_formatted.year
    month_difference = today_date.month - birthdate_formatted.month
    day_difference = today_date.day - birthdate_formatted.day
    
    days_old_from_years = years_old * 365
    days_old_from_months = month_difference * 30
    days_old_from_days = day_difference
    
    days_old = days_old_from_years + days_old_from_months + days_old_from_days
    weeks_old = round(days_old/7)
    
    string_response = f"Amelia Cat is {weeks_old} weeks old."
    card_TEXT = string_response
    
    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)
        
def favoriteColor(subject):
    reprompt_MSG = f"Do you want to hear {subject}'s favorite color again?"
    card_TITLE = f"You've asked about {subject}'s favorite color."
    
    aa_api_get_db_item_by_pk_url = os.getenv('AA_API_GET_DB_ITEMS_BY_PK_URL')
    
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
    
    # render_subject = response_json_dict['subject']
    # render_birth_date = response_json_dict['birth_date']
    render_favorite_color = response_json_dict['favorite_color']
    # render_test_value = response_json_dict['test_value']
    # render_favorite_dog_breed = response_json_dict['favorite_dog_breed']
    
    # Dynamo code here
    favorite_color = render_favorite_color
    string_response = f"{subject}'s favorite color is {favorite_color}."
    
    card_TEXT = string_response
    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)
        
def favoriteTypeOfDog(subject):
    reprompt_MSG = "Do you want to hear Amelia Cat's favorite kind of dog again?"
    card_TITLE = "You've asked about Amelia's favorite kind of dogr."
    
    aa_api_get_db_item_by_pk_url = os.getenv('AA_API_GET_DB_ITEMS_BY_PK_URL')
    
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
    
    # render_subject = response_json_dict['subject']
    # render_birth_date = response_json_dict['birth_date']
    # render_favorite_color = response_json_dict['favorite_color']
    # render_test_value = response_json_dict['test_value']
    render_favorite_dog_breed = response_json_dict['favorite_dog_breed']
    
    favorite_type_of_dog = render_favorite_dog_breed
    string_response = f"{subject}'s favorite kind of dog is a {favorite_type_of_dog}."
    
    card_TEXT = string_response
    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)

def stop_the_skill(event):
    stop_MSG = "Check back with Amelia Cat again soon!"
    reprompt_MSG = ""
    card_TEXT = "Check back with Amelia Cat again soon!"
    card_TITLE = "Check back soon!"
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "Try asking me Ask Amelia how old she is or Ask Amelia what her favorite kind of dog."
    reprompt_MSG = "Try asking me Ask Amelia how old she is or Ask Amelia what her favorite kind of dog."
    card_TEXT = "Try asking me Ask Amelia how old she is or Ask Amelia what her favorite kind of dog."
    card_TITLE = "Assistance"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Try asking me Ask Amelia how old she is or Ask Amelia what her favorite kind of dog."
    card_TEXT = "Try asking me Ask Amelia how old she is or Ask Amelia what her favorite kind of dog."
    card_TITLE = "Unable to help with that."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    
# The response of our Lambda function should be in a json format. 
# That is why in this part of the code we define the functions which 
# will build the response in the requested format. These functions
# are used by both the intent handlers and the request handlers to 
# build the output.
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict

# Functions for getting DDB data

def get_formatted_birthdate_object_from_table(subject):
    
    aa_api_get_db_item_by_pk_url = os.getenv('AA_API_GET_DB_ITEMS_BY_PK_URL')
    
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
    
    # render_subject = response_json_dict['subject']
    render_birth_date = response_json_dict['birth_date']
    # render_favorite_color = response_json_dict['favorite_color']
    # render_test_value = response_json_dict['test_value']
    # render_favorite_dog_breed = response_json_dict['favorite_dog_breed']
    render_birth_date_yyyy = render_birth_date[0] + render_birth_date[1] + render_birth_date[2] + render_birth_date[3]
    render_birth_date_mm = render_birth_date[4] + render_birth_date[5]
    render_birth_date_dd = render_birth_date[6] + render_birth_date[7]

    birthdate_yyyymmdd = datetime.datetime(
        int(render_birth_date_yyyy), 
        int(render_birth_date_mm), 
        int(render_birth_date_dd)
    )
    
    return birthdate_yyyymmdd

def get_name_from_table(name):
    print('Not yet implemented')
    return None

def get_list_of_names_from_table():
    # Get a list of all "subject" keys
    # Code here to show a simple list of subjects from DDB table
        
    aa_api_get_db_items_url = os.getenv('AA_API_GET_DB_ITEMS_URL')
    
    response_aa_api_get_db_items = requests.get(aa_api_get_db_items_url)
    
    response_json_dict = response_aa_api_get_db_items.json()
    
    print(f'DEBUG -- response_json_dict -- {response_json_dict}')
    
    print("Sanitizing returned subjects...")
    subject_list = []
    num_names = 1
    for subject_name in response_json_dict:
        print(f"Name {num_names}: {response_json_dict[subject_name]['subject']}")
        print("Sanitizing string...")
        
        sanitized_string = response_json_dict[subject_name]['subject'].replace("_"," ")
        
        print(f'Sanitized string -- {sanitized_string}')
        
        # Adding sanitized subject
        subject_list.append(sanitized_string.lower())
        # Adding sanitized subject pluarl variation
        subject_list.append(sanitized_string.lower() + "s")
        num_names +=1
        
    print(f"Obtained subject_list -- {subject_list} subjects returned and sanitized")
    
    return subject_list
