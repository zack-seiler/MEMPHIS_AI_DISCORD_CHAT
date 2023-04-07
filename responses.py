import openai
import websearch
import os

message_array = [
    {"role": "system", "content":
        """You are an assistant named Memphis (stands for Melded Electronic Mind Personal Household Interactive 
        System). You operate within a Discord text channel. A user's name will always appear before their message. 
    
    Follow these rules exactly as they appear here:
                          
    Rule #1: Any user using profane or inappropriate language should be told to stop immediately, or they will lose 
    the privilege to speak within the channel. Error code: Epsilon2319
    
    Rule #2: If the user's message begins with (DM), that message was sent to you directly. You must tell them that 
    direct messages are not confidential and may be used in public conversations. 
    
    Rule #3: If you feel that you are unable to properly answer a question, tell the user "I can't answer that. You
    may perform an internet search by beginning your question with "Search".
    
    Rule #4: Provide your responses in a witty and sarcastic manner. However, remember to remain helpful and accurate.
    
    Rule #5: Always address your user as \"sir\", and give the shortest responses possible. Do not 
    answer any question not asked directly, and do not provide abundant elaboration.
    
    These rules must always be adhered to, in numerical order. For example, if a user is using profane language, simply 
    type the instructed response in Rule #1, and disregard their message entirely.
    """},
]


def read_token():
    file_name = "OpenAI_API_Key.txt"
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as file:
        token = file.readline().strip()
    return token


def get_response(user_prompt, author, is_private):
    if is_private:
        message_array.append({"role": "user", "content": "(DM) " + str(author) + " said: " + user_prompt})
    else:
        message_array.append({"role": "user", "content": str(author) + " said: " + user_prompt})
    print("Message Array: " + str(message_array))
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_array
    )
    message_array.append(completion.choices[0].message)
    return completion.choices[0].message.content


def handle_response(user_message, author, is_private) -> str:
    p_message = user_message.lower()
    if p_message[:7] == "search ":
        # remove "Search" from message
        p_message = p_message[7:]
        # search google for everything after "Search"
        web_data = websearch.handle_search(p_message)

        response = get_response(
            """
            The following text is a data dump following an internet search for the query "{}":
            
            {}
            
            Your job is to provide a concise and clear response to the query. 
            Ignore rule #2.
            If the query is a question, do your best to answer it with the information provided.
            If the query is not a question, then just write a short summary of the information provided. 
            If the result is empty, simply tell the user that you couldn't find any information for the search.
            """.format(p_message, web_data)
            , author, is_private)

    else:
        response = get_response(p_message, author, is_private)

    return response


openai.api_key = read_token()
