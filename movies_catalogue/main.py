from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, flash
from config import app
import tmdb_client
import random
from forms import ContactForm
import errors
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@app.route("/")
def homepage():
    selected_list = request.args.get("list_type", "popular")
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    random.shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list)


@app.route("/about/")
def about_us():
    return render_template("about.html")


@app.route("/contact/", methods=["POST", "GET"])
def contact_us():
    form = ContactForm()
    if request.method == "POST":
        if not form.validate_on_submit():

            email = request.form["email"]
            name = request.form["name"]
            title = request.form["title"]
            message = request.form["message"]

            message = Mail(
                from_email=os.environ.get("MAIL_DEFAULT_SENDER"),
                to_emails=os.environ.get("MAIL_DEFAULT_RECEIVER"),
                subject=f"From {email}. Message title: {title} ",
                html_content=f"<strong>Message from: <p>{name}.</p><p>From Email: {email}</p><p>MESSAGE:</p> <p>{message}</p> </strong>",
            )
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                flash("Message Send.", "success")
                return render_template("/contact_send.html")
            except Exception as e:
                print(f"error", e.body)
    return render_template("/contact.html")


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images["backdrops"])
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)


@app.route("/search")
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)

    return {"tmdb_image_url": tmdb_image_url}


if __name__ == "__main__":
    app.run(debug=True)