import google.generativeai as genai
import os
import random
from apikey import API_KEY_GOOGLE

tricks =['charisma','persuade','influence','mind control','hypnotize','attract','charm','impress','flirt']
leaders = ['Nelson Mandela','Winston Churchill','Mahatma Gandhi','Martin Luther King Jr.',
           'Abraham Lincoln','George Washington','Che Guevara','Steve Jobs','Elon Musk','Napoleon Bonaparte',
           'Franklin D. Roosevelt','Queen Elizabeth II','Alexander the great','John F. Kennedy',
           'Ronald Reagan','Barack Obama','Julius Caesar']
experiments = ['Stanford prison experiment','Milgram experiment','Little Albert experiment','Monster study','Marshmellow test'
               'Bobo doll experiment','Harlow monkey experiment','Asch conformity experiment','Robbers cave experiment']
topics =['Psychology tricks','Charimsatic Leader psychology analysis','dark psychological experiments in history that gone wrong']

def random_topic():
    random.shuffle(topics)  # increase randomness
    topic = topics[0]
    detail=''
    if topic =='Psychology tricks':
        detail = random.choice(tricks)
    elif topic == 'Charimsatic Leader psychology analysis':
        detail = random.choice(leaders)
    else:
        detail = random.choice(experiments)
    return topic,detail
        
    


def generate_script():
    topic, detail = random_topic()
    genai.configure(api_key=API_KEY_GOOGLE)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f" Write a short video script about {topic} of{detail} that should be less than 30 seconds. \
                                        start by asking about the  {topic}\
                                        Then explain the {topic} and {detail}\
                                        tell viewers to subscribe to the channel at the end if they want more content like this. \
                                        Only include the words of the script, without visual or sound effects descriptions. Do not use symbols such as hashtags or emojis."
                                        )

    print(response.text)
    return response.text
