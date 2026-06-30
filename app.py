from flask import Flask, jsonify, request

app = Flask(__name__)

# The Event blueprint required by your lab instructions
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# Simulated in-memory database storage
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]
next_id = 3

# Reusable helper function to find an event by its ID
def find_event(event_id):
    return next((event for event in events if event.id == event_id), None)

# 1. Welcome Route
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Event Management API!"}), 200

# 2. Get All Events Route
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# 3. POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    global next_id
    data = request.get_json(silent=True)
    
    # Input Validation: Check if title exists
    if not data or "title" not in data:
        return jsonify({"error": "Bad Request. 'title' is a required field."}), 400
        
    new_event = Event(id=next_id, title=data["title"])
    events.append(new_event)
    next_id += 1
    
    return jsonify(new_event.to_dict()), 201

# 4. PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = find_event(id)
    if not event:
        return jsonify({"error": f"Event with ID {id} not found."}), 404
        
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "Bad Request. 'title' field is required for update."}), 400
        
    event.title = data["title"]
    return jsonify(event.to_dict()), 200

# 5. DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    global events
    event = find_event(id)
    if not event:
        return jsonify({"error": f"Event with ID {id} not found."}), 404
        
    events = [e for e in events if e.id != id]
    return jsonify({"message": f"Event {id} deleted successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)
