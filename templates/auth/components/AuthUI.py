from reactpy import component, html, hooks, event
from ...shared.components.button import Button
from ...shared.components.card import Card
from ...shared.error.error_boundary import ErrorBoundary
from ..backend.auth import generate_token, verify_token, register_user, verify_password

@component
def AuthUI(on_login_success=None):
    username, set_username = hooks.use_state("")
    password, set_password = hooks.use_state("")
    token, set_token = hooks.use_state("")
    auth_message, set_auth_message = hooks.use_state("")
    logged_in_user, set_logged_in_user = hooks.use_state("")

    @hooks.use_effect
    def check_token_on_load():
        if token:
            result = verify_token(token)
            if result:
                set_logged_in_user(result.get("user", ""))
                set_auth_message(f"Logged in as {result.get('user', '')}.")
            else:
                set_logged_in_user("")
                set_auth_message("Token is invalid or expired. Please log in again.")
        else:
            set_logged_in_user("")
            set_auth_message("Please log in or register.")
    hooks.use_effect(check_token_on_load, [token])

    @event(prevent_default=True)
    async def handle_register(e):
        if not username or not password:
            set_auth_message("Username and password cannot be empty.")
            return
        success = register_user(username, password)
        if success:
            set_auth_message(f"User '{username}' registered successfully! You can now log in.")
        else:
            set_auth_message(f"Registration failed: User '{username}' already exists.")

    @event(prevent_default=True)
    async def handle_login(e):
        if not username or not password:
            set_auth_message("Username and password cannot be empty.")
            return
        if verify_password(username, password):
            token_str = generate_token(username)
            set_token(token_str)
            set_logged_in_user(username)
            set_auth_message(f"Login successful! Welcome, {username}.")
            if on_login_success:
                on_login_success()  # <-- This will trigger the template switch
        else:
            set_auth_message("Login failed: Invalid username or password.")
            set_token("")
            set_logged_in_user("")

    @event(prevent_default=True)
    async def handle_logout(e):
        set_token("")
        set_logged_in_user("")
        set_username("")
        set_password("")
        set_auth_message("You have been logged out.")

    if logged_in_user:
        return ErrorBoundary(
            lambda e: Card(html.div({"class_name": "text-red-500"}, f"Error: {e}")),
            Card(
                html.div(
                    {"class_name": "space-y-4"},
                    html.h3({"class_name": "text-center"}, "🔐 Secure Area"),
                    html.p({"class_name": "text-center"}, f"Welcome, {logged_in_user}!"),
                    html.p({"class_name": "text-center text-sm"}, f"Your Token: {token}"),
                    Button("Logout", on_click=handle_logout, variant="danger"),
                    html.p({"class_name": "text-center"}, auth_message)
                )
            )
        )
    else:
        return ErrorBoundary(
            lambda e: Card(html.div({"class_name": "text-red-500"}, f"Error: {e}")),
            Card(
                html.div(
                    {"class_name": "space-y-4"},
                    html.h3({"class_name": "text-center"}, "🔐 Login / Register"),
                    html.form(
                        {"class_name": "space-y-2"},
                        html.input({
                            "type": "text",
                            "placeholder": "Username",
                            "value": username,
                            "on_change": lambda e: set_username(e["target"]["value"]),
                            "class_name": "input"
                        }),
                        html.input({
                            "type": "password",
                            "placeholder": "Password",
                            "value": password,
                            "on_change": lambda e: set_password(e["target"]["value"]),
                            "class_name": "input"
                        }),
                        html.div(
                            {"class_name": "flex gap-2"},
                            Button("Login", on_click=handle_login, variant="primary"),
                            Button("Register", on_click=handle_register, variant="secondary"),
                        ),
                    ),
                    html.p({"class_name": "text-center"}, auth_message)
                )
            )
        )
