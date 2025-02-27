import pandas as pd
from collections import OrderedDict
from datetime import datetime

def get_average(dict: dict)->float:
    if dict:
        return sum(dict.values())/len(dict)
    return 0.0

def filter_reviews(dict1 : OrderedDict, start_date :datetime, end_date :datetime, keep_all_data = False, key = "")->OrderedDict:
    filtered_reviews = {}
    if key not in dict1:
        key = ""
    for customer,review in dict1.items():
        current_date = datetime.strptime(review["Date"], "%B %d, %Y").date()
        if start_date > current_date:
            break
        if start_date <= current_date <= end_date:
            if keep_all_data and key == "":
                filtered_reviews[customer] = review
            elif key != "":
                filtered_reviews[customer] = review[key]
            else:
                filtered_reviews[current_date.strftime("%B %d, %Y")] = get_average(review["Rating"])
    return filtered_reviews

def create_review_df(restaurant_reviews: dict, restaurant_name: str)->pd.DataFrame:
    data = []
    for date, review in restaurant_reviews.items():
        date_obj = datetime.strptime(date, "%B %d, %Y")
        data.append({"Date": date_obj, "Ratings": review, "Restaurant": restaurant_name})
    return pd.DataFrame(data)


def get_average_reviews(dict1 : OrderedDict)->list:
    data = [0,0,0,0]
    num_customers = len(dict1)

    # Loop through each customer and sum the ratings for each category
    for customer in dict1.values():
        ratings = customer["Rating"]
        data[0] += ratings["Overall"]
        data[1] += ratings["Food"]
        data[2] += ratings["Service"]
        data[3] += ratings["Ambience"]

    # Calculate the average for each category and store it in the list
    averages = [rating_sum / num_customers for rating_sum in data]
    
    return averages

def get_ratings(dict1 : OrderedDict)->list:
    data = [0,0,0,0,0]
    # Loop through each customer and sum the ratings for each category
    for customer in dict1.values():
        rating = customer["Rating"]["Overall"]
        if 1 <= rating <= 5:
            data[rating - 1] += 1
    return data
