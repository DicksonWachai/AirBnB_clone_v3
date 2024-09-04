#!/usr/bin/python3

"""Handles all RESTful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def states(state_id=None):
    """Handles state objects based on HTTP methods"""
    if state_id is None:
        if request.method == 'GET':
            """Retrieve all state objects"""
            states = [state.to_dict() for state in storage.all(State).values()]
            return jsonify(states)

        elif request.method == 'POST':
            """Create a new State object"""
            my_dict = request.get_json()
            if not my_dict:
                abort(400, 'Not a JSON')
            if 'name' not in my_dict:
                abort(400, 'Missing name')

            new_state = State(**my_dict)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
    
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        if request.method == 'GET':
            """Retrieve a specific State object"""
            return jsonify(state.to_dict())

        elif request.method == 'PUT':
            """Update a State object"""
            my_dict = request.get_json()
            if not my_dict:
                abort(400, 'Not a JSON')
            
            """Update fields in the State object"""
            for key, value in my_dict.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200

        elif request.method == 'DELETE':
            """Delete a specific State object"""
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
