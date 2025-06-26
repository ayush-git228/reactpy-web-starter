from reactpy import hooks

def use_local_storage(key, initial_value):
    # Placeholder: ReactPy does not have direct localStorage access
    # For now, just return a state hook
    value, set_value = hooks.use_state(initial_value)
    return value, set_value
