import datetime

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
    onlunch_MSG = "Hi, I can tell you about Amelia Cat. Me and her are close friends."
    reprompt_MSG = "Try asking me how old Amelia is or what's her favorite kind of dog."
    # card_TEXT = "Pick a chess payer."
    # card_TITLE = "Choose a chess player."
    card_TEXT = "This is card text."
    card_TITLE = "This is card title."
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

    if intent_name == "howOld":
        return howOldGeneral(birthdate_yyyymmdd)
    elif intent_name == "howManyMonths":
        return howManyMonths(birthdate_yyyymmdd)
    elif intent_name == "howManyWeeks":
        return howManyWeeks(birthdate_yyyymmdd)
    elif intent_name == "favoriteColor":
        return favoriteColor()
    elif intent_name == "favoriteTypeOfDog":
        return favoriteTypeOfDog()
        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)

# Here we define the intent handler functions

def howOldGeneral(birthdate_formatted):
    reprompt_MSG = "Do you want to hear Amelia Cat's age again?"
    card_TITLE = "You've asked about Amelia's age. Ages less than 2 years will be reported in months."
    
    today_date = datetime.date.today()
    years_old = today_date.year - birthdate_formatted.year
    month_difference = today_date.month - birthdate_formatted.month - 1
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
            string_response = f"Amelia Cat is {month_difference} months and {weeks_difference} old."

    else:
        string_response = f"Something went wrong."

    card_TEXT = string_response

    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)
    
def howManyMonths(birthdate_formatted):
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
        string_response = f"Amelia Cat is {month_difference} months and {weeks_difference} old."
    
    card_TEXT = string_response
    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)

def howManyWeeks(birthdate_formatted):
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
        
def favoriteColor():
    reprompt_MSG = "Do you want to hear Amelia Cat's favorite color again?"
    card_TITLE = "You've asked about Amelia's favorite color."
    
    # Dynamo code here
    favorite_color = "red"
    string_response = f"Amelia Cat's favorite color is {favorite_color}."
    
    card_TEXT = string_response
    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)
        
def favoriteTypeOfDog():
    reprompt_MSG = "Do you want to hear Amelia Cat's favorite kind of dog again?"
    card_TITLE = "You've asked about Amelia's favorite kind of dogr."
    
    # Dynamo code here
    favorite_type_of_dog = "Corgi"
    string_response = f"Amelia Cat's favorite kind of dog is a {favorite_type_of_dog}."
    
    card_TEXT = string_response
    print(f"Returning string: {string_response}")
    return output_json_builder_with_reprompt_and_card(
        string_response, card_TEXT, card_TITLE, reprompt_MSG, 
        False)

def stop_the_skill(event):
    stop_MSG = "Check back again to see how much Amelia has grown. Goodbye!"
    reprompt_MSG = ""
    card_TEXT = "Bye! Check back again to see how much Amelia has grown!"
    card_TITLE = "Bye!"
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "Try asking me about Amelia Cat."
    reprompt_MSG = "What do you want to know about Amelia Cat?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to know more about Amelia Cat?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
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

# Static birthdate for now. Will go in Dynamo DB Table later
birthdate_yyyymmdd = datetime.datetime(2022, 6, 22)
