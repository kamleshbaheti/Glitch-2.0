import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

printFullResponse = False

async def openai_func(user_text): 
        
    try: 
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

        # Configure the Azure OpenAI client
        client = AsyncAzureOpenAI(
            azure_endpoint = azure_oai_endpoint, 
            api_key=azure_oai_key,  
            api_version="2024-02-15-preview"
            )
        

        # Read in system message and prompt for user message
        system_text = open(file="system.txt", encoding="utf8").read().strip()
        return await call_openai_model(system_message = system_text, 
                                user_message = user_text, 
                                model=azure_oai_deployment, 
                                client=client
                                )

    except Exception as ex:
        print(ex)
        return None

async def call_openai_model(system_message, user_message, model, client):
    # Format and send the request to the model
    messages =[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    # Call the Azure OpenAI model
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800
    )

    if printFullResponse:
        print(response)
    
    ans = response.choices[0].message.content
    return ans