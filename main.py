from flask import Flask, request, jsonify
import datetime
import random
import string
import db_utils

db = db_utils.DB()
app = Flask(__name__)


def random_string(length):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


class UrlShortener:
    def shorten(self, url):
        short_code = random_string(6)
        # Ensure uniqueness in the database
        while db.collection.find_one({"short_code": short_code}):
            short_code = random_string(6)
        url_info = {
            "url": url,
            "short_code": short_code,
            "created_at": datetime.datetime.now(),
            "modified_at": datetime.datetime.now(),
            "access_count": 0,
        }
        db.insert(url_info)
        return url_info

    def get(self, short_code):
        url_info = db.collection.find_one({"short_code": short_code})
        if url_info:
            # Increment access count
            db.collection.update_one(
                {"short_code": short_code},
                {
                    "$inc": {"access_count": 1},
                    "$set": {"modified_at": datetime.datetime.now()},
                },
            )
            return url_info
        else:
            return None

    def delete(self, short_code):
        db.collection.delete_one({"short_code": short_code})

    def update(self, short_code, url):
        result = db.collection.find_one({"short_code": short_code})
        if result:
            db.collection.update_one(
                {"short_code": short_code},
                {"$set": {"url": url, "modified_at": datetime.datetime.now()}},
            )
            return db.collection.find_one({"short_code": short_code})
        else:
            return None


url_shortener = UrlShortener()


@app.route("/shorten", methods=["POST"])
def shorten():
    request_data = request.get_json()
    if "url" not in request_data:
        return jsonify({"error": "URL is required"}), 400
    url = request_data["url"]
    response = url_shortener.shorten(url)
    response["_id"] = str(response["_id"])  # Convert ObjectId to string
    response["created_at"] = response["created_at"].isoformat()
    response["modified_at"] = response["modified_at"].isoformat()
    return jsonify(response)


@app.route("/shorten/<short_code>", methods=["GET"])
def get(short_code):
    url_info = url_shortener.get(short_code)
    if url_info:
        url_info["_id"] = str(url_info["_id"])  # Convert ObjectId to string
        url_info["created_at"] = url_info["created_at"].isoformat()
        url_info["modified_at"] = url_info["modified_at"].isoformat()
        url_info["access_count"] += 1
        db.collection.update_one(
            {"short_code": short_code},
            {
                "$set": {
                    "access_count": url_info["access_count"],
                    "modified_at": datetime.datetime.now(),
                }
            },
        )
        return jsonify(url_info)
    else:
        return jsonify({"error": "Not found"}), 404


@app.route("/shorten/<short_code>", methods=["DELETE"])
def delete(short_code):
    url_shortener.delete(short_code)
    return jsonify({"message": "Deleted"})


@app.route("/shorten/<short_code>", methods=["PUT"])
def update(short_code):
    request_data = request.get_json()
    if "url" not in request_data:
        return jsonify({"error": "URL is required"}), 400
    url = request_data["url"]
    updated_info = url_shortener.update(short_code, url)
    if updated_info:
        updated_info["_id"] = str(updated_info["_id"])  # Convert ObjectId to string
        updated_info["created_at"] = updated_info["created_at"].isoformat()
        updated_info["modified_at"] = updated_info["modified_at"].isoformat()
        return jsonify(updated_info)
    else:
        return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
