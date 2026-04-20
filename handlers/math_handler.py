import ast
import operator
import re


MATH_HINT_RE = re.compile(
    r"^(ile to|ile to jest|oblicz|policz|calculate|calc)?\s*[-+*/().,\d\s%^]+[=?]?\s*$",
    re.IGNORECASE,
)
PREFIX_RE = re.compile(r"^(ile to jest|ile to|oblicz|policz|calculate|calc)\s+", re.IGNORECASE)

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def extract_expression(message):
    text = message.strip().rstrip("=?").strip()
    text = PREFIX_RE.sub("", text).replace(",", ".").replace("^", "**")
    return text


def is_math_expression(message):
    return bool(MATH_HINT_RE.match(message.strip()))


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Zbyt duży wykładnik.")
        return OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Nieobsługiwane wyrażenie matematyczne.")


def calculate(message):
    expression = extract_expression(message)
    if not expression:
        return None

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree)
    except ZeroDivisionError:
        return "Nie można dzielić przez zero."
    except Exception:
        return None

    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return f"Wynik: {result}"
