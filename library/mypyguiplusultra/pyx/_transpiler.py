# This parser is a modifed version of the parser implemented by https://github.com/RudreshVeerkhare/ReactPy

from pypeg2 import (
    List,
    Symbol,
    compose,
    ignore,
    maybe_some,
    optional,
    parse,
    attr,
    name,
)
import sys
import re


WHITESPACE = re.compile(r"\s+")
EXP1 = re.compile(r"(?m)(\W)(\s+)(\W)")
EXP2 = re.compile(r"(?m)[\r\n]+")  # to remove all new lines
CREATE_METHOD = "createElement"
AUTO_IMPORTS = """# Automatic Imports
from pathlib import Path
# End of automatic imports :(
"""
CSS_IMPORT_FUNCTION = "importCSS"

def string_difference_transform(text, t_prev, t_next):
    """
    As we are replacing all whitespaces with single, it's affecting parser
    to keep parser going properly we must transform resulting text again in
    indented form
    Parameters::
        text: original text
        t_prev: processed text before parsing
        t: text after parsing
    """

    rw = re.compile(r"\s")

    def _skip(_i, _text):
        while _i < len(_text) and rw.match(_text[_i]):
            _i += 1
        return _i

    # it's basically a string matching while ignoring whitespaces and newlines
    t_start = t_prev[: len(t_prev) - len(t_next)]
    i = j = 0

    while i < len(t_start) and j < len(text):
        i = _skip(i, t_start)
        j = _skip(j, text)

        if t_start[i] == text[j]:
            i += 1
            j += 1

    return text[j:]


class SingleQuoteString(str):
    grammar = "'", re.compile(r"[^']*"), "'"


class DoubleQuoteString(str):
    grammar = '"', re.compile(r"[^\"]*"), '"'


String = [SingleQuoteString, DoubleQuoteString]


class EscapeString:
    """
    it's intermidiate form of inline code that to be stored so that
    it shouldn't be interpreted as string
    """

    def __init__(self, content):
        self.content = content

    def __repr__(self) -> str:
        return f"{self.content.strip()}"


class DictEntry:
    """This is for each key-value entry in a dictionary"""

    grammar = (
        attr("key", String),
        ":",
        attr(
            "value",
            [String, re.compile(r"[^,}]+")],
        ),
        optional(","),
    )


class Dictionary(List):
    """
    Grammer to recognize Dictionary
    """

    grammar = "{", maybe_some(DictEntry), "}"

    def to_dict(self):
        res = dict()
        for entry in self:
            if isinstance(entry.value, SingleQuoteString) or isinstance(
                entry.value, DoubleQuoteString
            ):
                res[entry.key] = entry.value
            else:
                res[entry.key] = EscapeString(entry.value)
        return res


class InlineCode:
    """
    To represent Inline code in PYX syntax
    """

    grammar = "{", attr("code", [Dictionary, re.compile(r"[^}]*")]), "}"

    def to_code(self):
        if isinstance(self.code, Dictionary):
            return self.code.to_dict()
        if isinstance(self.code, TagChildren):
            return self.code.compose()
        return EscapeString(self.code)

    def compose(self):
        return f"{self.to_code()}"


class Attribute:
    """Matches attribute passed to tag in format key="value" or key={value} or key={{key: val, ...}}"""

    grammar = (
        name(),
        ignore(optional(WHITESPACE)),
        "=",
        attr("value", [String, InlineCode]),
    )

    def to_dict(self):
        res = dict()
        key = self.name.name
        if isinstance(self.value, str):
            if key != 'src':
                res[key] = self.value
                return res
            res['source'] = EscapeString(f"Path(__file__).parent.joinpath(r\"{self.value}\").as_posix()")
            return res

        if isinstance(self.value, InlineCode):
            if key != 'src':
                res[key] = self.value.to_code()
                return res
            res['source'] = EscapeString(f"Path(__file__).parent.joinpath({self.value.to_code()}).as_posix()")
            return res
        


class Attributes(List):
    """Matches zero or more Attribute"""

    grammar = optional(
        ignore(WHITESPACE), Attribute, maybe_some(ignore(WHITESPACE), Attribute)
    )

    def to_dict(self):
        res = dict()
        for attribute in self:
            res.update(attribute.to_dict())
        return res


class Text(object):
    """Matches text between tags and/or inline code sections."""

    grammar = attr("value", re.compile(r"[^<{]+"))

    def compose(self):
        return f'"{self.value.strip()}"'


class PairedTag:
    """
    This are tags which have children elements
    Ex. -> <h1>Hello, World</h1>
    """

    @staticmethod
    def parse(parser, text, pos):

        # Replace all whitespaces in PYX to single whitespace and then parse it
        text_org = text
        # text = replace_whitespaces(text)
        t_prev = text
        result = PairedTag()
        try:
            text, _ = parser.parse(text, "<")
            text, tag = parser.parse(text, Symbol)
            result.tag = tag
            text, attributes = parser.parse(text, Attributes)
            result.attributes = attributes
            text, _ = parser.parse(text, ">")
            text, children = parser.parse(text, TagChildren)
            result.children = children
            text, _ = parser.parse(text, optional(WHITESPACE))
            text, _ = parser.parse(text, "</")
            text, _ = parser.parse(text, result.tag)
            text, _ = parser.parse(text, ">")
        except SyntaxError as e:
            return text_org, e

        # we have replaced whitespaces, but parser is not aware so we have to transform it back
        text = string_difference_transform(text_org, t_prev, text)

        return text, result

    def compose(self):
        tag = f'"{self.tag}"'
        if self.tag[0].isupper():
            tag = self.tag
        return f"{CREATE_METHOD}({tag}, {self.attributes.to_dict()}, {self.children.compose()})"


class SelfClosingTag:
    """
    This tags are self closing.
    Ex. -> <Counter />
    """

    grammar = (
        "<",
        attr("tag", Symbol),
        attr("attributes", Attributes),
        ignore(re.compile(r"\s*")),
        "/>",
    )

    @staticmethod
    def parse(parser, text, pos):
        # Replace all whitespaces in PYX to single whitespace and then parse it
        t = text
        # t = replace_whitespaces(text)
        t_prev = t
        t, r = parser._parse(t, SelfClosingTag.grammar, pos)

        if type(r) == SyntaxError:
            return text, r

        # we have replaced whitespaces, but parser is not aware so we have to transform it back
        text = string_difference_transform(text, t_prev, t)

        obj = SelfClosingTag()
        for _r in r:
            setattr(obj, _r.name, _r.thing)
        return text, obj

    def compose(self):
        # Component name has to be first char capital
        tag = f'"{self.tag}"'
        if self.tag[0].isupper():
            tag = self.tag

        return f"{CREATE_METHOD}({tag}, {self.attributes.to_dict()})"


class TagChildrenInlineCode:
    """
    To represent Inline code in PYX syntax
    """

    grammar = (
        "{",
        attr("pre_tag", optional([SelfClosingTag, PairedTag])),
        attr("code_1", [Dictionary, re.compile(r"[^<}]*")]),
        attr("mid_tag", optional([SelfClosingTag, PairedTag])),
        attr("code_2", [Dictionary, re.compile(r"[^<}]*")]),
        attr("end_tag", optional([SelfClosingTag, PairedTag])),
        "}",
    )

    def compose(self):
        pre_tag = self.pre_tag.compose().strip() if self.pre_tag else ""
        mid_tag = self.mid_tag.compose().strip() if self.mid_tag else ""
        end_tag = self.end_tag.compose().strip() if self.end_tag else ""
        return f"{pre_tag} {self.code_1.to_dict() if isinstance(self.code_1, Dictionary) else self.code_1} {mid_tag} {self.code_2.to_dict() if isinstance(self.code_2, Dictionary) else self.code_2} {end_tag}"


class TagChildren(List):
    """Matches valid tag children which can be other tags, plain text, {values} or a mix of all
    three."""

    grammar = maybe_some([SelfClosingTag, PairedTag] + [TagChildrenInlineCode, Text])

    def compose(self):
        text = []
        for entry in self:
            # Skip pure whitespace
            text.append(entry.compose())
            text.append(", ")

        return "".join(text)


class CSSFilenameSingleQuote(str):
    grammar = "'", re.compile("[^']*\.css"), "'"


class CSSFilenameDoubleQuote(str):
    grammar = '"', re.compile('[^"]*\.css'), '"'


CSSFilename = [CSSFilenameSingleQuote, CSSFilenameDoubleQuote]


class CSSImport:
    """
    This pattern is to detect css file import
    Ex. import name from '../assets/style.css'
    """

    grammar = (
        "import",
        ignore(WHITESPACE),
        attr("namespace", str),
        ignore(WHITESPACE),
        "from",
        ignore(WHITESPACE),
        attr("filename", CSSFilename),
    )

    def get_filename(self):
        return self.filename, self.namespace


class PYXBlock(List):
    """
    This is the actual PYX code
    """

    grammar = attr("line_start", re.compile(r"[^#<\n]+")), [SelfClosingTag, PairedTag]

    @staticmethod
    def parse(parser, text, pos):
        # Replace all whitespaces in PYX to single whitespace and then parse it
        t = text  # replace_whitespaces(text)
        t, r = parser._parse(t, PYXBlock.grammar, pos)

        if type(r) == SyntaxError:
            return t, r

        obj = PYXBlock(r[1:])
        setattr(obj, r[0].name, r[0].thing)
        return t, obj

    def compose(self):
        text = [self.line_start]
        for entry in self:
            if isinstance(entry, str):
                text.append(entry)
            else:
                text.append(entry.compose())

        return "".join(text)

class BigString:
    grammar = '"""', attr("content", re.compile(r"[^(\"\"\")]*")), '"""'
    def compose(self):
        return '"""%s"""' % self.content

class NonPYXLine:
    grammar = attr("content", re.compile(".*")), "\n"

    def compose(self):
        return "%s\n" % self.content


class CodeBlock(List):
    grammar = maybe_some([PYXBlock, CSSImport, BigString, NonPYXLine, re.compile(r".+")])

    def compose(self, parser, attr_of=None):
        text = []
        text.append(AUTO_IMPORTS)
                
        for entry in self:
            if isinstance(entry, str):
                text.append(entry)
            elif isinstance(entry, CSSImport):
                xs = entry.get_filename()
                text.append(f"{xs[1]} = {CSS_IMPORT_FUNCTION}(Path(__file__).parent.joinpath('{xs[0]}'))")
            else:
                text.append(entry.compose())

        return "".join(text)

def setGlobals(
    createMethod, 
    autoImports, 
    cssImportMethod
):
    global CREATE_METHOD, AUTO_IMPORTS, CSS_IMPORT_FUNCTION
    CREATE_METHOD = createMethod
    AUTO_IMPORTS = autoImports
    CSS_IMPORT_FUNCTION = cssImportMethod



def transform(
    input_code, 
    ):
    """
    Parses given string input and also extracts imported .css files
    """
    result = parse(input_code, CodeBlock, whitespace=None)
    return compose(result)