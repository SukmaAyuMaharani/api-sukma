from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data contoh untuk smartphone dan detailnya
smartphones = [
    {"id": "1", "name": "Phone A", "description": "Smartphone high-end", "price": 1000},
    {"id": "2", "name": "Phone B", "description": "Smartphone mid-range", "price": 700}
]

details = {
    "1": {"id": "1", "name": "Phone A", "customerReviews": []},
    "2": {"id": "2", "name": "Phone B", "customerReviews": []}
}

class SmartphoneList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(smartphones),
            "smartphones": smartphones
        }

class SmartphoneDetail(Resource):
    def get(self, smartphone_id):
        if smartphone_id in details:
            return {
                "error": False,
                "message": "success",
                "smartphone": details[smartphone_id]
            }
        return {"error": True, "message": "Smartphone not found"}, 404

class SmartphoneSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [s for s in smartphones if query in s['name'].lower() or query in s['description'].lower()]
        return {
            "error": False,
            "founded": len(result),
            "smartphones": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        smartphone_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if smartphone_id in details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            details[smartphone_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "customerReviews": details[smartphone_id]['customerReviews']
            }
        return {"error": True, "message": "Smartphone not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        smartphone_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if smartphone_id in details:
            reviews = details[smartphone_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Smartphone not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        smartphone_id = data.get('id')
        name = data.get('name')
        
        if smartphone_id in details:
            reviews = details[smartphone_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Smartphone not found"}, 404

api.add_resource(SmartphoneList, '/list')
api.add_resource(SmartphoneDetail, '/detail/<string:smartphone_id>')
api.add_resource(SmartphoneSearch, '/search')
api.add_resource(AddReview, '/review')
api.add_resource(UpdateReview, '/review/update')
api.add_resource(DeleteReview, '/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
