from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "¡Webhook conectado a OpenAI (actualizado)!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    mensaje_usuario = data.get("message", {}).get("text", "")
    numero_cliente = data.get("message", {}).get("from", "")

    if not mensaje_usuario:
        return jsonify({"error": "Mensaje vacío"}), 400

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Responde como un asistente profesional y amable."},
                {"role": "user", "content": mensaje_usuario}
            ]
        )

        mensaje_respuesta = respuesta.choices[0].message.content

        return jsonify({
            "text": mensaje_respuesta,
            "to": numero_cliente
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500