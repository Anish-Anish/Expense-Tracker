from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import re

app = Flask(__name__)
CORS(app)

def category_matcher(df):
    categories = {
        "Travel": ["uber", "flight", "train", "bus", "cab", "transport", "ola", "rapido",
                   "metro", "boat", "petrol", "diesel", "auto", "bike", "taxi", "rental",
                   "tour", "visa", "cruise", "fuel", "sea", "gate", "toll", "ticket",
                   "boarding", "pass", "rickshaw", "subway", "shuttle", "ferry", "bicycle",
                   "highway", "travel", "hotel", "stay", "car", "air", "rail", "cycle",
                   "hike", "boat", "ship", "fun", "country", "road", "hill", "trip", "ride"],

        "Investment": ["stock", "mutual", "crypto", "gold", "grow", "silver", "platinum",
                       "forex", "bonds", "real", "estate", "nft", "sip", "equity", "land",
                       "dividend", "commodity", "index", "hedge", "fund", "bullion",
                       "pension", "fixed", "deposit", "annuity", "treasury", "derivatives",
                       "option", "trading", "private", "equity", "venture", "capital",
                       "funding", "sovereign", "investment", "reit", "cryptocurrency",
                       "bit", "coin", "tax", "elss", "securities", "stocks"],

        "Utilities": ["electricity", "water", "internet", "bill", "gas", "tablet",
                      "recharge", "postpaid", "prepaid", "landline", "garbage",
                      "sewer", "sanitation", "cable", "tv", "broadband", "subscription",
                      "wifi", "power", "heating", "cooling", "solar", "generator",
                      "housekeeping", "maintenance", "repair", "smart", "septic",
                      "data", "plan", "satellite", "security", "inverter", "utilities"],

        "Entertainment": ["movie", "netflix", "games", "mall", "amusement", "park",
                          "match", "concert", "sports", "cricket", "football", "stadium",
                          "ticket", "nightclub", "pub", "casino", "music", "theater",
                          "stand", "circus", "bowling", "theme", "hotstar", "jio",
                          "escape", "museum", "zoo", "aquarium", "festival", "exhibition",
                          "club", "streaming", "entertainment"],

        "Food": ["restaurant", "pizza", "hotel", "snacks", "bakery", "chocolate",
                 "ice cream", "fast", "veg", "non", "barbecue", "vegetables", "fruits",
                 "meat", "beverages", "tea", "organic", "drink", "street food",
                 "catering", "delivery", "takeout", "vegan", "juice", "alcohol",
                 "cocktail", "dining", "buffet", "homemade", "choc", "food", "sweet",
                 "stall", "market", "lunch", "brunch", "breakfast", "dinner", "cafe",
                 "tea", "coffee", "chai", "court"],

        "Shopping": ["clothing", "footwear", "accessories", "jewelry", "watch",
                     "handbags", "cosmetics", "perfume", "skin", "vitamin", "makeup",
                     "electronics", "gadget", "mobile", "laptop", "shoe", "headphone",
                     "decor", "furniture", "appliances", "bag", "groceries", "grocery",
                     "toy", "product", "sport", "fitness", "equipment", "book",
                     "stationery", "gift", "luxury", "online", "discount", "shopping",
                     "gear", "supermarket"]
    }

    def pattern_matcher(name):
        for category, keywords in categories.items():
            if any(re.search(r'\b' + keyword.lower() + r'\b', name.lower()) for keyword in keywords):
                return category
        return "Other Expense"

    df["Category"] = df["Transaction_Name"].apply(pattern_matcher)
    return df

@app.route('/view_data', methods=['POST'])
def view_data():
    try:
        data = request.get_json()

     
        if "data" not in data:
            return jsonify({"error": "Missing 'data' key in request JSON"}), 400

        df = pd.DataFrame(data["data"])

      
        if "Transaction_Name" not in df.columns or "Amount" not in df.columns:
            return jsonify({"error": "Invalid data format. Columns 'Transaction_Name' and 'Amount' are required."}), 400

        df = category_matcher(df)
        total = df.groupby('Category')['Amount'].sum().reset_index()
        result = total.to_dict(orient="records")

        return jsonify({"message": "File processed successfully!", "total_data": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    PORT = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=PORT)
