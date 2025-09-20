from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    user_info = None
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        try:
            # 1. Отримати userId по username
            resp = requests.post(
                "https://users.roblox.com/v1/usernames/users",
                json={"usernames": [username]}
            )
            data = resp.json()
            
            if "data" in data and len(data["data"]) > 0:
                user_id = data["data"][0]["id"]

                # 2. Отримати детальну інфу
                info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
                user_info = {
                    "id": info.get("id"),
                    "name": info.get("name"),
                    "displayName": info.get("displayName"),
                    "created": info.get("created"),
                    "description": info.get("description", "Немає опису")
                }
            else:
                error = "Користувача не знайдено!"

        except Exception as e:
            error = str(e)

    return render_template("index.html", user_info=user_info, error=error)


if __name__ == "__main__":
    app.run(debug=True)
