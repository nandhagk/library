from __future__ import annotations
from .css_enums import *
from mypyguiplusultra.core.util import functions
import tinycss2 as tc
import webcolors

class VALUE(Enum):
    color = Enum.auto(first=True)
    size = Enum.auto()
    literal = Enum.auto()
    string = Enum.auto()

def _get_4_dimensions(sizes : list):
    if len(sizes) == 1:
        return (sizes[0], sizes[0], sizes[0], sizes[0])
    elif len(sizes) == 2:
        return (sizes[0], sizes[1], sizes[0], sizes[1])
    elif len(sizes) == 3:
        return (sizes[0], sizes[1], sizes[2], sizes[1])
    elif len(sizes) == 4:
        return (sizes[0], sizes[1], sizes[2], sizes[3])
    else:
        return None


def _warn_incorrect_value_length(property_name):
    print(f"`{property_name}` got an invalid property value (incorrect number of values)")
    return {}

def _warn_unexpected_value(property_name, token):
    print(f"`{property_name}` recieved an unexpected value {token}")
    return {}

def _get_color(token):
    if isinstance(token, tc.tokenizer.HashToken):
        return '#'+token.value
    elif isinstance(token, tc.tokenizer.IdentToken):
        if token.value == 'transparent':
            return ''
        try:
            hex_color = webcolors.name_to_hex(token.value)
        except:
            return
        return hex_color
    elif isinstance(token, tc.tokenizer.FunctionBlock):
        succesful, values = expect(
            token.arguments,
            f'rgb',
            ((VALUE.size, 3, False),)
        )
        if not succesful:
            return
        return webcolors.rgb_to_hex(tuple(int(value[0]) for value in values))

def _get_unit(unit_name, property_name):
    if unit_name == 'px':return Unit.px
    elif unit_name == 'em':return Unit.em
    elif unit_name == 'rem':return Unit.rem
    elif unit_name == 'vh':return Unit.viewport_height
    elif unit_name == 'vw':return Unit.viewport_width
    elif unit_name == 'null':return Unit.null
    elif unit_name == '%':
        if property_name in {'height', 'max_height', 'min_height', 'top', 'bottom', 'padding_top', 'padding_bottom', 'margin_top', 'margin_bottom'}:
            return Unit.master_height
        elif property_name in {'transform_origin_y'}:
            return Unit.self_height
        elif property_name in {'transform_origin_x', 'transform_origin'}:
            return Unit.self_width
        else:
            return Unit.master_width
    else:
        print(f"Unknown unit `{unit_name}` on `{property_name}`")
        return Unit.px

def expect(
    values : list,
    property_name,
    expected_parameters, # list<(value_type, count :int, optional :bool)>
    allow_extra=False, # Not being used rn
    ignore_whitespace = True,
):
    expecteds_dict = {xs[0]:[xs[1], xs[2]] for xs in expected_parameters}
    gotten_values = {key:[] for key in expecteds_dict}
    succesful = True

    for token in values:
        if isinstance(token, tc.tokenizer.NumberToken):
            if gotten_values.get(VALUE.size) is None:
                _warn_unexpected_value(property_name, token)
                succesful = False
                break
            gotten_values[VALUE.size].append((token.value, Unit.px))
            expecteds_dict[VALUE.size][0] -= 1
            if expecteds_dict[VALUE.size][0] < 0:
                _warn_incorrect_value_length(property_name)
                succesful = False
                break
        elif isinstance(token, (tc.tokenizer.DimensionToken, tc.tokenizer.PercentageToken)):
            if gotten_values.get(VALUE.size) is None:
                _warn_unexpected_value(property_name, token)
                succesful = False
                break
            gotten_values[VALUE.size].append((token.value, _get_unit((token.unit if isinstance(token, tc.tokenizer.DimensionToken) else '%'), property_name)))
            expecteds_dict[VALUE.size][0] -= 1
            if expecteds_dict[VALUE.size][0] < 0:
                _warn_incorrect_value_length(property_name)
                succesful = False
                break
        elif isinstance(token, tc.tokenizer.HashToken):
            color = _get_color(token)
            if gotten_values.get(VALUE.color) is None or color is None:
                _warn_unexpected_value(property_name, token)
                succesful = False
                break
            gotten_values[VALUE.color].append(color)
            expecteds_dict[VALUE.color][0] -= 1
            if expecteds_dict[VALUE.color][0] < 0:
                _warn_incorrect_value_length(property_name)
                succesful = False
                break
        elif isinstance(token, tc.tokenizer.IdentToken):
            color = _get_color(token)
            if color is None:
                if gotten_values.get(VALUE.literal) is None:
                    _warn_unexpected_value(property_name, token)
                    succesful = False
                    break
                gotten_values[VALUE.literal].append(token.value)
                expecteds_dict[VALUE.literal][0] -= 1
                if expecteds_dict[VALUE.literal][0] < 0:
                    _warn_incorrect_value_length(property_name)
                    succesful = False
                    break
            else:
                if gotten_values.get(VALUE.color) is None:
                    _warn_unexpected_value(property_name, token)
                    succesful = False
                    break
                gotten_values[VALUE.color].append(color)
                expecteds_dict[VALUE.color][0] -= 1
                if expecteds_dict[VALUE.color][0] < 0:
                    _warn_incorrect_value_length(property_name)
                    succesful = False
                    break
        elif isinstance(token, tc.tokenizer.FunctionBlock):
            if token.lower_name == 'rgb':
                color = _get_color(token)
                if gotten_values.get(VALUE.color) is None or color is None:
                    _warn_unexpected_value(property_name, token)
                    succesful = False
                    break
                gotten_values[VALUE.color].append(color)
                expecteds_dict[VALUE.color][0] -= 1
                if expecteds_dict[VALUE.color][0] < 0:
                    _warn_incorrect_value_length(property_name)
                    succesful = False
                    break
            else:
                print(f'Unsupported css function `{token}`')
                succesful = False
                break
        elif isinstance(token, tc.tokenizer.StringToken):
            if gotten_values.get(VALUE.string) is None:
                _warn_unexpected_value(property_name, token)
                succesful = False
                break
            gotten_values[VALUE.string].append(token.value)
            expecteds_dict[VALUE.string][0] -= 1
            if expecteds_dict[VALUE.string][0] < 0:
                _warn_incorrect_value_length(property_name)
                succesful = False
                break
        elif isinstance(token, (tc.tokenizer.LiteralToken, tc.tokenizer.WhitespaceToken)):pass
        else:
            print(f"Unknown token type {token}")

    for i in expecteds_dict:
        if expecteds_dict[i][0] != 0 and not expecteds_dict[i][1]:
            _warn_incorrect_value_length(property_name)
            succesful = False
    if succesful:
        return succesful, *list(gotten_values[parameter[0]] for parameter in expected_parameters)
    else:
        return succesful, ([None] * len(expected_parameters))


def background(values : list):
    '''Parse the `background` value into a dict containing the needed property'''
    succesful, colors = expect(values, 'background', (
        (VALUE.color, 1, False),
    ))
    if not succesful:return {}
    return {
        'background_color' : colors[0]
    }


def background_color(values : list):
    '''Parse the `background_color` value into a dict containing the needed property'''

    succesful, colors = expect(values, 'background_color', (
        (VALUE.color, 1, False),
    ))
    if not succesful:return {}
    return {
        'background_color' : colors[0]
    }

def border(values : list):
    '''Parse the `border` value into a dict containing the needed property'''
    succesful, colors, literals, dimensions = expect(values, 'border', (
        (VALUE.color, 1, True),
        (VALUE.literal, 1, True),
        (VALUE.size, 1, True),
    ))
    if not succesful:return {}

    res = {}

    if literals:
        xs = BorderStyle.str_to_enum(functions.snake_case(literals[0]))
        if xs is not None:
            res['border_style'] = xs

    if colors:
        res['border_color'] = colors[0]

    if dimensions:
        res['border_width'] = dimensions[0]

    return res

def border_width(values : list):
    '''Parse the `border_width` value into a dict containing the needed property'''
    succesful, size = expect(values, 'border_width', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'border_width' : size[0]
    }

def border_radius(values : list):
    '''Parse the `border_radius` value into a dict containing the needed property'''
    succesful, sizes = expect(values, 'border_radius', (
        (VALUE.size, 4, True),
    ))
    if not succesful:return {}
    sizes = _get_4_dimensions(sizes)
    if sizes is None:return {}
    return  {
        'border_top_left_radius' : sizes[0],
        'border_top_right_radius' : sizes[1],
        'border_bottom_left_radius' : sizes[2],
        'border_bottom_right_radius' : sizes[3],
    }

def border_bottom_left_radius(values : list):
    '''Parse the `border_bottom_left_radius` value into a dict containing the needed property'''
    succesful, size = expect(values, 'border_bottom_left_radius', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'border_bottom_left_radius' : size[0]
    }

def border_bottom_right_radius(values : list):
    '''Parse the `border_bottom_right_radius` value into a dict containing the needed property'''
    succesful, size = expect(values, 'border_bottom_right_radius', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'border_bottom_right_radius' : size[0]
    }

def border_top_left_radius(values : list):
    '''Parse the `border_top_left_radius` value into a dict containing the needed property'''
    succesful, size = expect(values, 'border_top_left_radius', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'border_top_left_radius' : size[0]
    }

def border_top_right_radius(values : list):
    '''Parse the `border_top_right_radius` value into a dict containing the needed property'''
    succesful, size = expect(values, 'border_top_right_radius', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'border_top_right_radius' : size[0]
    }

def border_style(values : list):
    '''Parse the `border_color` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'border_style', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = BorderStyle.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'border_style' : xs
    }

def border_color(values : list):
    '''Parse the `border_color` value into a dict containing the needed property'''
    succesful, colors = expect(values, 'border_color', (
        (VALUE.color, 1, False),
    ))
    if not succesful:return {}
    return {
        'border_color' : colors[0]
    }


def color(values : list):
    '''Parse the `color` value into a dict containing the needed property'''
    succesful, colors = expect(values, 'color', (
        (VALUE.color, 1, False),
    ))
    if not succesful:return {}
    return {
        'color' : colors[0]
    }


def opacity(values : list):
    '''Parse the `opacity` value into a dict containing the needed property'''
    succesful, numbers = expect(values, 'opacity', (
        (VALUE.size, 1, False),
    ))
    if not succesful:return {}
    return {
        'opacity' : numbers[0][0]
    }


def display(values : list):
    '''Parse the `display` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'display', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = Display.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'display' : xs
    }


def position(values : list):
    '''Parse the `position` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'position', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = Position.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'position' : xs
    }


def z_index(values : list):
    '''Parse the `z_index` value into a dict containing the needed property'''
    succesful, numbers = expect(values, 'z_index', (
        (VALUE.size, 1, False),
    ))
    if not succesful:return {}
    return {
        'z_index' : numbers[0][0]
    }


def visibility(values : list):
    '''Parse the `visibility` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'visibility', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = Visibility.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'visibility' : xs
    }


def box_sizing(values : list):
    '''Parse the `box_sizing` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'box_sizing', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = BoxSizing.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'box_sizing' : xs
    }


def top(values : PropertyValue):
    '''Parse the `top` value into a dict containing the needed property'''
    succesful, size = expect(values, 'top', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'top' : size[0]
    }


def right(values : list):
    '''Parse the `right` value into a dict containing the needed property'''
    succesful, size = expect(values, 'right', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'right' : size[0]
    }


def bottom(values : list):
    '''Parse the `bottom` value into a dict containing the needed property'''
    succesful, size = expect(values, 'bottom', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'bottom' : size[0]
    }


def left(values : list):
    '''Parse the `left` value into a dict containing the needed property'''
    succesful, size = expect(values, 'left', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'left' : size[0]
    }

def aspect_ratio(values : list):
    '''Parse the `aspect_ratio` value into a dict containing the needed property'''
    succesful, size = expect(values, 'aspect_ratio', (
        (VALUE.size, 2, True),
    ))

    if not succesful or not size:return {}
    return {
        'aspect_ratio' : (size[0][0], (size[1][0] if len(size) == 2 else 1))
    }

def height(values : list):
    '''Parse the `height` value into a dict containing the needed property'''
    succesful, size = expect(values, 'height', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'height' : size[0]
    }


def width(values : list):
    '''Parse the `width` value into a dict containing the needed property'''
    succesful, size = expect(values, 'width', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'width' : size[0]
    }


def max_height(values : list):
    '''Parse the `max_height` value into a dict containing the needed property'''
    succesful, size = expect(values, 'max_height', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'max_height' : size[0]
    }


def max_width(values : list):
    '''Parse the `max_width` value into a dict containing the needed property'''
    succesful, size = expect(values, 'max_width', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'max_width' : size[0]
    }


def min_height(values : list):
    '''Parse the `min_height` value into a dict containing the needed property'''
    succesful, size = expect(values, 'min_height', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'min_height' : size[0]
    }


def min_width(values : list):
    '''Parse the `min_width` value into a dict containing the needed property'''
    succesful, size = expect(values, 'min_width', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'min_width' : size[0]
    }


def font(values : list):
    '''Parse the `font` value into a dict containing the needed property'''
    print('css font shorthand not implemented')
    return {}


def font_family(values : list):
    '''Parse the `font_family` value into a dict containing the needed property'''
    succesful, vals = expect(values, 'font_family', (
        (VALUE.string, 1, False),
    ))
    if not succesful: return {}
    return {
        'font_family' : vals[0]
    }


def font_size(values : list):
    '''Parse the `font_size` value into a dict containing the needed property'''
    succesful, size = expect(values, 'font_size', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'font_size' : size[0]
    }


def font_weight(values : list):
    '''Parse the `font_weight` value into a dict containing the needed property'''

    succesful, vals = expect(values, 'font_weight', (
        (VALUE.size, 1, False),
    ))
    if not succesful:return {}
    return {
        'font_weight' : int(vals[0][0])
    }


def font_variant(values : list):
    '''Parse the `font_variant` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'font_variant', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = FontVariant.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'font_variant' : xs
    }

def text_overflow(values : list):
    '''Parse the `text_overflow` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'text_overflow', (
        (VALUE.literal, 1, False),
    ))

    if not succesful:return {}
    xs = TextOverflow.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'text_overflow' : xs
    }

def text_align(values : list):
    '''Parse the `text_overflow` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'text_align', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = literals[0].lower()
    return {
        'text_align' : xs
    }


def margin(values : list):
    '''Parse the `margin` value into a dict containing the needed property'''
    succesful, sizes = expect(values, 'margin', (
        (VALUE.size, 4, True),
    ))
    if not succesful:return {}
    sizes = _get_4_dimensions(sizes)
    if sizes is None:return {}
    return  {
        'margin_top' : sizes[0],
        'margin_right' : sizes[1],
        'margin_bottom' : sizes[2],
        'margin_left' : sizes[3],
    }


def margin_bottom(values : list):
    '''Parse the `margin_bottom` value into a dict containing the needed property'''
    succesful, size = expect(values, 'margin_bottom', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'margin_bottom' : size[0]
    }


def margin_left(values : list):
    '''Parse the `margin_left` value into a dict containing the needed property'''
    succesful, size = expect(values, 'margin_left', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'margin_left' : size[0]
    }


def margin_right(values : list):
    '''Parse the `margin_right` value into a dict containing the needed property'''
    succesful, size = expect(values, 'margin_right', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'margin_right' : size[0]
    }


def margin_top(values : list):
    '''Parse the `margin_top` value into a dict containing the needed property'''
    succesful, size = expect(values, 'margin_top', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'margin_top' : size[0]
    }


def padding(values : list):
    '''Parse the `padding` value into a dict containing the needed property'''
    succesful, sizes = expect(values, 'padding', (
        (VALUE.size, 4, True),
    ))
    if not succesful:return {}
    sizes = _get_4_dimensions(sizes)
    if sizes is None:return {}
    return  {
        'padding_top' : sizes[0],
        'padding_right' : sizes[1],
        'padding_bottom' : sizes[2],
        'padding_left' : sizes[3],
    }

def padding_bottom(values : list):
    '''Parse the `padding_bottom` value into a dict containing the needed property'''
    succesful, size = expect(values, 'padding_bottom', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'padding_bottom' : size[0]
    }


def padding_left(values : list):
    '''Parse the `padding_left` value into a dict containing the needed property'''
    succesful, size = expect(values, 'padding_left', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'padding_left' : size[0]
    }


def padding_right(values : list):
    '''Parse the `padding_right` value into a dict containing the needed property'''
    succesful, size = expect(values, 'padding_right', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'padding_right' : size[0]
    }


def padding_top(values : list):
    '''Parse the `padding_top` value into a dict containing the needed property'''
    succesful, size = expect(values, 'padding_top', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'padding_top' : size[0]
    }


def transform_origin(values : list):
    '''Parse the `transform_origin` value into a dict containing the needed property'''
    succesful, size = expect(values, 'transform_origin', (
        (VALUE.size, 2, True),
    ))

    if not succesful:return {}

    return {
        'transform_origin_x' : size[0],
        'transform_origin_y' : size[len(size) - 1],
    }



def transform_origin_y(values : list):
    '''Parse the `transform_origin_y` value into a dict containing the needed property'''
    succesful, size = expect(values, 'transform_origin_y', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'transform_origin_y' : size[0]
    }


def transform_origin_x(values : list):
    '''Parse the `transform_origin_x` value into a dict containing the needed property'''
    succesful, size = expect(values, 'transform_origin_x', (
        (VALUE.size, 1, False),
    ))

    if not succesful:return {}
    return {
        'transform_origin_x' : size[0]
    }

def overflow(values : list):
    '''Parse the `overflow` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'Parse', (
        (VALUE.literal, 2, True),
    ))
    if not succesful:return {}
    xs1 = Overflow.str_to_enum(functions.snake_case(literals[0]))
    xs2 = Overflow.str_to_enum(functions.snake_case(literals[len(literals) - 1]))
    if xs1 is None or xs2 is None:return {}

    return {
        'overflow_x' : xs1,
        'overflow_y' : xs2
    }


def overflow_x(values : list):
    '''Parse the `overflow_x` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'overflow_x', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = Overflow.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'overflow_x' : xs
    }


def overflow_y(values : list):
    '''Parse the `overflow_y` value into a dict containing the needed property'''
    succesful, literals = expect(values, 'overflow_y', (
        (VALUE.literal, 1, False),
    ))
    if not succesful:return {}
    xs = Overflow.str_to_enum(functions.snake_case(literals[0]))
    if xs is None:return {}
    return {
        'overflow_y' : xs
    }

def validate(rule_name : PropertyName, value_tokens : list):
    if rule_name == 'background':return background(value_tokens)
    elif rule_name == 'background_color':return background_color(value_tokens)
    elif rule_name == 'border':return border(value_tokens)
    elif rule_name == 'border_radius':return border_radius(value_tokens)
    elif rule_name == 'border_width':return border_width(value_tokens)
    elif rule_name == 'border_bottom_left_radius':return border_bottom_left_radius(value_tokens)
    elif rule_name == 'border_bottom_right_radius':return border_bottom_right_radius(value_tokens)
    elif rule_name == 'border_top_left_radius':return border_top_left_radius(value_tokens)
    elif rule_name == 'border_top_right_radius':return border_top_right_radius(value_tokens)
    elif rule_name == 'border_style':return border_style(value_tokens)
    elif rule_name == 'border_color':return border_color(value_tokens)
    elif rule_name == 'color':return color(value_tokens)
    elif rule_name == 'opacity':return opacity(value_tokens)
    elif rule_name == 'display':return display(value_tokens)
    elif rule_name == 'position':return position(value_tokens)
    elif rule_name == 'z_index':return z_index(value_tokens)
    elif rule_name == 'visibility':return visibility(value_tokens)
    elif rule_name == 'box_sizing':return box_sizing(value_tokens)
    elif rule_name == 'top':return top(value_tokens)
    elif rule_name == 'right':return right(value_tokens)
    elif rule_name == 'bottom':return bottom(value_tokens)
    elif rule_name == 'left':return left(value_tokens)
    elif rule_name == 'height':return height(value_tokens)
    elif rule_name == 'width':return width(value_tokens)
    elif rule_name == 'aspect_ratio':return aspect_ratio(value_tokens)
    elif rule_name == 'max_height':return max_height(value_tokens)
    elif rule_name == 'max_width':return max_width(value_tokens)
    elif rule_name == 'min_height':return min_height(value_tokens)
    elif rule_name == 'min_width':return min_width(value_tokens)
    elif rule_name == 'text_overflow':return text_overflow(value_tokens)
    elif rule_name == 'text_align':return text_align(value_tokens)
    elif rule_name == 'font':return font(value_tokens)
    elif rule_name == 'font_family':return font_family(value_tokens)
    elif rule_name == 'font_size':return font_size(value_tokens)
    elif rule_name == 'font_weight':return font_weight(value_tokens)
    elif rule_name == 'font_variant':return font_variant(value_tokens)
    elif rule_name == 'margin':return margin(value_tokens)
    elif rule_name == 'margin_bottom':return margin_bottom(value_tokens)
    elif rule_name == 'margin_left':return margin_left(value_tokens)
    elif rule_name == 'margin_right':return margin_right(value_tokens)
    elif rule_name == 'margin_top':return margin_top(value_tokens)
    elif rule_name == 'padding':return padding(value_tokens)
    elif rule_name == 'padding_bottom':return padding_bottom(value_tokens)
    elif rule_name == 'padding_left':return padding_left(value_tokens)
    elif rule_name == 'padding_right':return padding_right(value_tokens)
    elif rule_name == 'padding_top':return padding_top(value_tokens)
    elif rule_name == 'transform_origin':return transform_origin(value_tokens)
    elif rule_name == 'transform_origin_y':return transform_origin_y(value_tokens)
    elif rule_name == 'transform_origin_x':return transform_origin_x(value_tokens)
    elif rule_name == 'overflow':return overflow(value_tokens)
    elif rule_name == 'overflow_x':return overflow_x(value_tokens)
    elif rule_name == 'overflow_y':return overflow_y(value_tokens)
    else:
        print(f'Unsopperted css property {rule_name}', value_tokens)
        return {}
