from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, flash
from config import app
import tmdb_client
import random
from model import Contacts, db
import errors


@app.route("/")
def homepage():
    selected_list = request.args.get("list_type", "popular")
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    random.shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list)


@app.route("/about/")
def about_us():
    return render_template("about.html")


@app.route("/services/")
def get_services():
    return render_template("services.html")


@app.route("/contact/", methods=["POST", "GET"])
def contact_us():
    if request.method == "POST":
        if (
            not request.form["name"]
            or not request.form["email"]
            or not request.form["phone"]
            or not request.form["message"]
        ):
            flash("Please enter all required data", "error")
        else:
            message = Contacts(
                request.form["name"], request.form["email"], request.form["phone"], request.form["message"]
            )

            db.session.add(message)
            db.session.commit()

            flash("Message successfully send.")
            return render_template("/contact_send.html")
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


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)