from flask import Flask, request, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_secret"

@app.route('/')
def home_page():
    return render_template("mainPage.html", title="Home_Page")

@app.route("/resultpage", methods=["POST","GET"])
def result_page():
    if request.method == "POST":
        result = request.form
        # user_id = result['user_id']
        skin_type = result['skin_type']
        item_type = result['item_type']
        brand_type = result['brand_type']
        #if len(user_id) != 0:
        #    print(user_id)
        #else:
        #    print(skin_type, item_type, brand_type)
    return render_template("mainPage.html", title="Home_Page")


if __name__ == "__main__":
    app.run()