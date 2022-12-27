from pypeg2 import (
    List,
    Symbol,
    compose,
    ignore,
    maybe_some,
    some,
    optional,
    parse,
    attr,
    name,
)
import sys
import re

import tinycss2
from .css_property_validator import validate
from mypyguiplusultra.core.util.functions import snake_case
def getRule(pn, pv):
    return validate(snake_case(pn), [tinycss2.parse_one_component_value(i) for i in pv])

WHITESPACE = re.compile(r"[\s\,]+")

class Text(object):
    grammar = attr("value", re.compile(r"[^ :{}\,\;]+"))
    def compose(self):
        return self.value.strip()

class CSSRule:
    grammar=ignore(optional(WHITESPACE)), attr("propertyName", Text), ignore(optional(WHITESPACE)), ":", ignore(optional(WHITESPACE)), attr("propertyValue", some(Text, optional(WHITESPACE))), ignore(optional(WHITESPACE)), ";"

    def compose(self):
        pn = self.propertyName.compose()
        pv = [i.compose() for i in self.propertyValue if not isinstance(i, str)]
        return getRule(pn, pv)

class CSSSelector:
    grammar = attr("selector", Text), ignore(optional(WHITESPACE)), optional(
        ":", ignore(optional(WHITESPACE)), attr("state", Text)
    ), ignore(optional(WHITESPACE))
    def compose(self):
        xs = getattr(self, "state", None)
        xs = xs.compose() if xs is not None else ''
        return (self.selector.compose(),  xs)

class CSSBlock:
    grammar = attr("selectors", some(CSSSelector)), "{", ignore(optional(WHITESPACE)), attr("rules", maybe_some(CSSRule)),ignore(optional(WHITESPACE)),"}"

    def compose(self):
        rules = {}
        for i in self.rules:
            rules.update(i.compose())
        return f"""
stylesheet.addBlock(
    {[i.compose() for i in self.selectors]},
    {rules}
)""".strip()

class CSS(List):
    grammar = maybe_some(CSSBlock)

    def compose(self, parser, attr_of=None):
        text = []

        for entry in self:
            text.append(entry.compose())

        return "\n".join(text)

import runpy
def parseRaw(raw, stylesheet):
    '''Parses all rules in raw and adds them to stylesheet'''
    # print((tinycss2.parse_stylesheet(raw, skip_whitespace=True, skip_comments=True)[0].prelude))
    xs = parse(raw.strip(), CSS, whitespace=None)
    # print(compose(xs))
    # Just use tinycss2 for parsing bruh
    exec(compose(xs), {"stylesheet":stylesheet})
    # What we can do is just transpile the css into a python executable

    # Then use runpy.run to run it :)
