#!/bin/env python3
import os
import sys

from create_embedding import get_embedding
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure

MOCK_API_KEY = "sk-MOCK_API_KEY"


def main():
    """
    Main function that gets the plot field for a movie, retrieves the embedding, and updates the document in the database.
    """
    try:
        # Load environment variables
        load_dotenv("/app/.env")
        URI = os.environ.get("CONNECTION_STRING")
        DB_NAME = "sample_mflix"
        COLLECTION_NAME = "embedded_movies"
        MOVIE_TITLE = "Top Gun"
        client = MongoClient(URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Get the plot description for the movie ("Top Gun")
        plot_result = collection.find_one({"title": MOVIE_TITLE}, {"plot": 1})
        if plot_result is None:
            print(f"No plot found for movie: {MOVIE_TITLE}")
            sys.exit(1)

        movie_plot = plot_result["plot"]

        # Get the vector embedding for the movie plot
        embedding = get_embedding(movie_plot, MOCK_API_KEY)
        if embedding is None:
            print(f"Failed to get embedding for {MOVIE_TITLE} plot")
            sys.exit(1)

        # Update the document with the embedding
        update_result = collection.update_one(
            {"title": MOVIE_TITLE},
            {"$set": {"plot_embedding": embedding}},
        )
        if update_result.modified_count == 1:
            print("Successfully updated document with embedding")
        else:
            print("Failed to update document with embedding")
    except OperationFailure as operation_failure:
        print(f"Operation Failure: {operation_failure}")
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
