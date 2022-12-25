from .css_property_validator import validate
from mypyguiplusultra.core.util.functions import snake_case
import tinycss2



def _get_rules(tokens : list):
    rules = {}
    current_property_name = ''
    current_property_value = []
    for token in tokens:
        if isinstance(token, tinycss2.tokenizer.LiteralToken):
            if token.value == ';':
                rules.update(validate(current_property_name, current_property_value))
                current_property_name = ''
                current_property_value.clear()
        elif isinstance(token, tinycss2.tokenizer.IdentToken):
            if not current_property_name:
                current_property_name = snake_case(token.value)
                continue
            current_property_value.append(token)
        elif isinstance(
                token,
                (tinycss2.tokenizer.DimensionToken, tinycss2.tokenizer.StringToken, tinycss2.tokenizer.HashToken, tinycss2.tokenizer.NumberToken, tinycss2.tokenizer.FunctionBlock, tinycss2.tokenizer.PercentageToken)
            ):
            current_property_value.append(token)
        elif not isinstance(token, tinycss2.tokenizer.WhitespaceToken):
            console.warn('Unkown token type', token)

    return rules

def _get_selectors(tokens : list):
    selectors = []
    current_selector_text = ''
    next_is_state = False
    for token in tokens:
        if isinstance(token, tinycss2.tokenizer.IdentToken):
            if next_is_state:
                selectors.append((current_selector_text, token.value))
                next_is_state = False
                current_selector_text = ''
            else:
                current_selector_text += token.value
        elif isinstance(token, tinycss2.tokenizer.LiteralToken):
            if token.value == ':':
                next_is_state = True
            elif token.value == ',':
                selectors.append((current_selector_text, ''))
                current_selector_text = ''
            elif token.value == '.':
                current_selector_text += '.'
            elif token.value == '*':
                current_selector_text += '*'
        elif isinstance(token, tinycss2.tokenizer.HashToken):
            current_selector_text += '#' + token.value
    if current_selector_text:
        selectors.append((current_selector_text, ''))
    return selectors

def parseRaw(raw : str, styleSheet):
    for rule in tinycss2.parse_stylesheet(raw, skip_comments=True, skip_whitespace=True):
        selectors = _get_selectors(rule.prelude)
        rules = _get_rules(rule.content)
        styleSheet.addBlock(selectors, rules)
