from twilio.rest import Client
from flask import Flask, request

app = Flask(__name__)

account_sid = 'AC989be9c22ae8a65c3a0f637f22c07c51'
authToken = '461026f6bf97b34d2563a20be8a7edad'

client = Client(account_sid, authToken)

last_message = None  # Para armazenar a última mensagem enviada

def send_whatsapp_message(to, from_, body):
    global last_message
    message = client.messages.create(to=to, from_=from_, body=body)
    last_message = message
    return message

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_message
    incoming_msg = request.values.get("Body", "").lower()

    if incoming_msg == "!status":
        if last_message:
            response = f"Status da última mensagem: {last_message.status}"
        else:
            response = "Nenhuma mensagem enviada ainda."

        # Enviar a resposta de volta para o usuário
        send_whatsapp_message(from_="whatsapp:+5511977063915", to=request.values.get("From"), body=response)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
