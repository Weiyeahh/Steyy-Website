import os
import openai

def botres(prompttext,usertext,responselist):

  openai.api_key ="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"
  start_sequence = "\nAI: "
  restart_sequence = "\nHuman: "
  responselist+=f'\nHuman: {usertext}\n AI: '
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f'{prompttext}{responselist}',
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.27,
    presence_penalty=1.2,
    stop=[" Human: ", " AI: "]
  )
  botres=response["choices"][0]["text"].replace("\n","")
  responselist+=botres
  with open(f'datafile/userinfo.txt', 'a',encoding="UTF8") as f:
        f.write(responselist)
  return(botres)


