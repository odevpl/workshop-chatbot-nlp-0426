from handlers.math_handler import calculate, is_math_expression
from handlers.model_handler import generate_response
from handlers.template_handler import find_template_response


def get_bot_response(user_message, history):
    if is_math_expression(user_message):
        math_response = calculate(user_message)
        if math_response:
            return math_response

    template_response = find_template_response(user_message)
    if template_response:
        return template_response

    return generate_response(history, user_message)
