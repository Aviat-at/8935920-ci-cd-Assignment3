import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="contactapi")
@app.route(route="contact_api", methods=["POST"])
def contact_api(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Contact API called")

    try:
        data = req.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not all([name, email, message]):
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Missing fields"}),
                status_code=400,
                mimetype="application/json"
            )

        # Simulate logic (e.g., saving, sending, etc.)
        logging.info(f"Received: {name} <{email}>: {message}")

        return func.HttpResponse(
            json.dumps({"status": "success", "message": f"Thanks {name}, your message was received."}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
