import numpy as np
import pandas as pd
import ast

from helper_lib import YearExtractor  

import logging
from logger import setup_logging
setup_logging()

# Initialize the YearExtractor object
extractor = YearExtractor()


# Specify the file path to the csv input file
file_path = 'movies_dataset.csv'

def load_dataset_from_csv(file_path):
    """
    Loads movies dataset from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file containing the movies data.

    Returns:
    pd.DataFrame: A Pandas DataFrame containing the movies data.
    """
    try:
        logging.info(f"Loading data from {file_path}")
        print("")
        print(f"Loading data from {file_path}")
        print("")
        movies_df = pd.read_csv(file_path, low_memory=False)
        return movies_df
    except Exception as e:
        logging.error(f"Error loading the data: {e}")
        print("")
        print(f"Error loading the data: {e}")
        return None

# Calling the function above
movies_df = load_dataset_from_csv(file_path)


def count_unique_movies(movies_df):
    """
    Counts the number of unique movie titles in the DataFrame.

    Parameters:
    movies_df (pd.DataFrame): DataFrame containing movies data in the 'title' column.

    Returns:
    int: Number of unique movie titles.
    None: If an error occurs during the counting.
    """
    try:
        unique_movie_count = movies_df['title'].nunique()
        logging.info(f"Number of unique movies: {unique_movie_count}")
        print("")
        print("Number of unique movies:", unique_movie_count)
        print("")
        return unique_movie_count
    except Exception as e:
        logging.error(f"Error counting the unique movies: {e}")
        print("")
        print(f"Error counting the unique movies: {e}")
        return None


# Filter and convert 'vote_count' to integers
vote_counts = movies_df[movies_df['vote_count'].notnull()]['vote_count'].astype('int')

# Filter and convert 'vote_average' to integers
vote_averages = movies_df[movies_df['vote_average'].notnull()]['vote_average'].astype('int')


def calculate_average_rating_of_all_movies(movies_df):
    """
    Calculates the average rating and weighted average rating of movies.

    Parameters:
    movies_df (pd.DataFrame): DataFrame containing movies data with 'vote_count' and 'vote_average' columns.

    Returns:
    tuple: A tuple containing the average rating and weighted average rating, or (None, None) if an error occurs.
    """
    try:
        # Check if vote_counts and vote_averages are not empty
        if vote_counts.empty or vote_averages.empty:
            logging.warning("No valid vote counts or vote averages found.")
            print("")
            print("No valid vote counts or vote averages found.")
            return None, None

        # Calculate the average rating of all movies
        avg_rating = vote_averages.mean()
        logging.info(f"Average rating of all movies: {avg_rating}")
        print("")
        print("Average rating of all movies:", avg_rating)
        print("")

        # Calculate the weighted average rating of all movies
        weighted_avg_rating = (movies_df['vote_average'] * movies_df['vote_count']).sum() / movies_df['vote_count'].sum()
        logging.info(f"Weighted average rating of all movies: {weighted_avg_rating}")
        print("")
        print("Weighted average rating of all movies:", weighted_avg_rating)
        print("")

        return avg_rating, weighted_avg_rating
    except Exception as e:
        logging.error(f"Error calculating movie ratings: {e}")
        print("")
        print(f"Error calculating movie ratings: {e}")
        return None, None


def calculate_top_5_rated_movies(movies_df):
    """
    Calculates the top 250 movies using IMDB's Weighted Rating formula (Bayes estimator) and prints the top 5.

    Parameters:
    movies_df (pd.DataFrame): DataFrame containing movies data with 'vote_count' and 'vote_average' columns - as calculated previously.

    Returns:
    pd.DataFrame: A DataFrame containing the top 250 movies sorted by IMDB's weighted rating.
    None: If an error occurs during the calculation.
    """
    try:
        # Check if vote_counts and vote_averages are not empty
        if vote_counts.empty or vote_averages.empty:
            print("No valid vote counts or vote averages found.")
            return None

        # Calculate the mean vote average (mn) and the 95th percentile vote count (perc)
        mn = vote_averages.mean()
        perc = vote_counts.quantile(0.95)

        def bayes_est(x):
            vc = x['vote_count']
            va = x['vote_average']
            # Bayes estimator formula
            return (vc / (vc + perc) * va) + (perc / (perc + vc) * mn)

        # Filter qualified movies above/equal to the 95th percentile - avoid movies outside the top 5%
        qualified = movies_df[(movies_df['vote_count'] >= perc) & 
                              (movies_df['vote_count'].notnull()) & 
                              (movies_df['vote_average'].notnull())][['title', 'release_date', 'vote_count', 'vote_average', 'popularity', 'genres']]

        # Apply the Bayes estimator
        qualified['wr'] = qualified.apply(bayes_est, axis=1)

        # Sort by weighted rating and get the top 250 movies
        qualified = qualified.sort_values('wr', ascending=False).head(250)

        logging.info("Top 5 movies by IMDB's weighted rating:")
        logging.info(qualified.head(5))
        print("")
        print("Top 5 movies by IMDB's weighted rating:")
        print(qualified.head(5))
        print("")

        return qualified
    except Exception as e:
        logging.error(f"Error calculating top movies: {e}")
        print("")
        print(f"Error calculating top movies: {e}")
        return None


def count_movies_by_release_year(movies_df, extractor):
    """
    Counts and prints the number of movies released each year, ranked by movie count.

    Parameters:
    movies_df (pd.DataFrame): DataFrame containing movies data with 'release_date' column.
    extractor (YearExtractor): An instance of the YearExtractor class used to extract the year from release dates string.

    Returns:
    None
    """
    try:
        # Extract the year from 'release_date' using the YearExtractor's extract_year method
        movies_df['year'] = pd.to_datetime(movies_df['release_date'], errors='coerce').apply(extractor.extract_year)
        logging.info("Number of movies by release year:")
        logging.info(movies_df['year'].value_counts(dropna=False))
        print("")
        print("Number of movies by release year:")
        print(movies_df['year'].value_counts(dropna=False))
        print("")
    except Exception as e:
        logging.error(f"Error extracting and counting movie release years: {e}")
        print("")
        print(f"Error extracting and counting movie release years: {e}")


def count_movies_in_each_genre(movies_df):
    """
    Processes the genres column in the movies DataFrame, normalizes it, and prints the genre.

    Parameters:
    movies_df (pd.DataFrame): DataFrame containing movies data with 'genres' column.

    Returns:
    pd.DataFrame: A DataFrame containing the normalized genres.
    None: If an error occurs during the processing.
    """
    def parse_genres(genres_str):
        """
        Parses a genre string into a list of dictionaries.

        Parameters:
        genres_str (str): A string representing genres in list of dictionaries format.

        Returns:
        list: A list of dictionaries if parsing is successful, otherwise an empty list is returned.
        """
        try:
            return ast.literal_eval(genres_str)
        except (ValueError, SyntaxError):
            return []

    try:
        # Apply the parsing function to the 'genres' column
        movies_df['parsed_genres'] = movies_df['genres'].apply(parse_genres)

        # Normalize the parsed genres
        genres_normalized = movies_df['parsed_genres'].explode().dropna()

        # Convert the normalized genres into a DataFrame
        genres_df = pd.json_normalize(genres_normalized)

        # Count the occurrences of each genre
        genre_counts = genres_df['name'].value_counts()
        # If the genre occurs more than once - to filter for outliers
        logging.info("Number of movies in each genre:")
        logging.info(genre_counts[genre_counts > 1])
        print("")
        print("Number of movies in each genre:")
        print(genre_counts[genre_counts > 1])
        print("")

        return genres_df
    except Exception as e:
        logging.error(f"Error processing genres: {e}")
        print("")
        print(f"Error processing genres: {e}")
        return None


def save_dataset_to_json(movies_df, movies_df_output):
    """
    Saves the movies dataset to a JSON file.

    Parameters:
    movies_df (pd.DataFrame): DataFrame containing movies data.
    movies_df_output (str): The path to the output JSON file.

    Returns:
    bool: True if the operation is successful, False otherwise.
    """
    try:
        movies_df.to_json(movies_df_output, orient='records', lines=True)
        logging.info(f"Output data successfully saved to {movies_df_output}")
        print("")
        print(f"Output data successfully saved to {movies_df_output}")
        print("")
        return True
    except Exception as e:
        logging.error(f"Error saving DataFrame to JSON: {e}")
        print("")
        print(f"Error saving DataFrame to JSON: {e}")
        return False


def main():
    # load_dataset_from_csv(file_path)
    count_unique_movies(movies_df)
    calculate_average_rating_of_all_movies(movies_df)
    calculate_top_5_rated_movies(movies_df)
    count_movies_by_release_year(movies_df, extractor)
    count_movies_in_each_genre(movies_df)
    save_dataset_to_json(movies_df, 'movies_output.json')


if __name__ == "__main__":
    main()
