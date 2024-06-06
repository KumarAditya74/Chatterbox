from flask import Flask, render_template, request, session, jsonify
from groq import Groq

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


client = Groq(api_key='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')

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
   
    messages = session.get('messages', [])

    if request.method == 'POST':
        user_input = request.json['input']
        messages.append({"role": "user", "content": user_input})

        
        assistant_response = get_response(messages)
        messages.append({"role": "assistant", "content": assistant_response})

        
        session['messages'] = messages[-100:]

        
        return jsonify({"response": assistant_response})

    
    return render_template('main.html', messages=messages)

def get_response(messages_list):
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages_list,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content

    return response


