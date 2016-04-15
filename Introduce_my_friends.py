"""
My first custom Alexa Skill - william.jeffrey.harding@gmail.com
"""

from __future__ import print_function

friend_info = {"Stefan":{
					"worksAt":"Point Mark",
					"pronoun":"he",
					"likes":"hiking"
					}, 
			"James":{
				"worksAt":"Lightspeed Research",
				"pronoun":"he",
				"likes":"playing the ukulele"
			},
			"Stacia":{
				"worksAt":"Shoreline High School",
				"pronoun":"she",
				"likes":"running and working out"
			},
			"Matt":{
				"worksAt":"Amazon",
				"pronoun":"he",
				"likes":"rock climbing"
			},
			"Colin":{
				"worksAt":"Optimedia",
				"pronoun":"he",
				"likes":"Natural Language Proccessing"
			}}

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != "<key>"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts 
	This is just to note the session info on the beginning of a request.
	"""

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getMyFriendInfo":
        return get_my_friend_info(intent, session)
    elif intent_name == "introduceMyFrend":
        return introduce_my_friend(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Whith this app I can greet your friends. " \
                    "I can only greet friends if they are listed in your list of friends, " \
                    "You can add or delete friends in the amazon app developer set"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry I didn't catch that." 
                    
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def introduce_my_friend(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'Friend' in intent['slots']:
        friend_name = intent['slots']['Friend']['value']
        session_attributes = create_friend_attributes(friend_name)
        speech_output = "Hello, " + \
                        friend_name + \
                        ". I'm very pleased to meet you."+ \
						"I'm Alexa: human cyborg relations."
        reprompt_text = "I believe that I asked you a question."
    else:
        speech_output = "I don't know who that is."
        reprompt_text = "I don't know who that is."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_friend_attributes(friend_name):
    return {"friendName": friend_name}


def get_my_friend_info(intent, session):
	session_attributes = {}	
	should_end_session = True
	
	if 'Friend' in intent['slots']:
		friend_name = intent['slots']['Friend']['value']
		friend_data = friend_info[friend_name]
		session_attributes = create_friend_attributes(friend_name)
		speech_output = "Of course I know " + \
						friend_name + \
						". "+ \
						friend_data['pronoun'] + \
						" works at " + \
						friend_data['worksAt'] + \
						"and likes " + \
						friend_data['likes']
						
		reprompt_text = "I believe that I asked you a question."
	else:
		speech_output = "I don't know who that is."
		reprompt_text = "I don't know who that is."
		
	return build_response(session_attributes, build_speechlet_response(
		intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }