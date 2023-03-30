import os
import openai

#https://platform.openai.com/docs/api-reference/making-requests

#key = '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'
def get_models(org,key):
    openai.organization = org
    openai.api_key = os.getenv(key)
    models = openai.Model.list(key)
    return models

def send_prompt(*args):
    #args list: model,prompt,max_tokens,temp,top_p,n,stream,logprobs,api_k
    model_engine = args[0]
    prompt = args[1]
    max_tokens = args[2]
    openai.api_key = args[8]
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    #print(completion)
    #print(completion.usage)
    return completion.choices[0].text,completion.usage

if __name__ == '__main__':
    #print(get_models('org-0QodRYXdUMliQNKfWvX1D9E7',key))
    print(send_prompt('text-davinci-003',"Say this is a test!",10))