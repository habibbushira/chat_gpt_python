import openai
import gradio as gr

from decouple import config

openai.api_key = config('API_KEY')

message_history = []

def predict(input):
  global message_history
  message_history.append({"role": "user", "content": input})

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message_history
  )

  replay_content = completion.choices[0].message.content
  print(replay_content)
  message_history.append({"role": "assistant", "content": replay_content})
  response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(len(message_history)-1, 2)]
  return response

with gr.Blocks() as demo:
  chatbot = gr.Chatbot()
  with gr.Row():
    txt = gr.Textbox(show_label=False, placeholder="Type your message...").style(container=False)
    txt.submit(predict, txt, chatbot)
    txt.submit(None, None, txt, _js="() => {''}")

demo.launch()