from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

# Load GPT-2 model and tokenizer from Hugging Face Transformers
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2")

def generate_email_body(prompt):
    # Encode the prompt text to tokens
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate the output tokens from the model
    outputs = model.generate(inputs.input_ids, max_length=200, num_return_sequences=1)

    # Decode the generated tokens back to text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_text

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.get_json()  # Get data from POST request
    subject = data['subject']
    key_points = data['keyPoints']

    # Create a prompt to generate the email
    prompt = f"Subject: {subject}\n\nEmail Body: Based on the following key points: {key_points}."
    
    # Generate the email body using the custom function
    generated_email = generate_email_body(prompt)

    # Return the generated email as JSON
    return jsonify({'email_body': generated_email})

if __name__ == '__main__':
    app.run(debug=True)
