from reactpy import hooks

def use_store(initial_state):
    state, set_state = hooks.use_state(initial_state)
    def dispatch(action):
        # Example reducer logic (customize as needed)
        if action["type"] == "increment":
            set_state({**state, "count": state.get("count", 0) + 1})
        elif action["type"] == "decrement":
            set_state({**state, "count": state.get("count", 0) - 1})
        # Add more actions as needed
    return state, dispatch
