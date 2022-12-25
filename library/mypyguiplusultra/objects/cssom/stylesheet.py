from collections import OrderedDict
from pathlib import Path

def _update_double_dict(updatee_dictionary : dict, key1 : str, key2 : str, updater_dictionary : dict):
    if updatee_dictionary.get(key1) is None:
        updatee_dictionary[key1] = OrderedDict()
    if updatee_dictionary[key1].get(key2) is None:
        updatee_dictionary[key1][key2] = {}
    updatee_dictionary[key1][key2].update(updater_dictionary)

def _update_deeper_dict(updatee_dictionary : dict, updater_dictionary, needed_keys):
    for key in (key for key in updater_dictionary if key in needed_keys):
        updatee_dictionary.update(updater_dictionary[key])

class StyleSheet:
    def __init__(self):
        self.selectors : dict[str, dict[str, dict[str, any]]] = OrderedDict()
        '''
        dict<
            selector_base : str,
            dict<
                state : str,
                styles : dict<property_name : str, property_value : Value>
            >
        >
        '''

    def addBlock(self, selectors, rules):
        for selector in selectors:
            _update_double_dict(self.selectors, selector[0], selector[1], rules)

    def merge(self, other):
        for selector in other.selectors:
            for state in other.selectors[selector]:
                _update_double_dict(self.selectors, selector, state, other.selectors[selector][state])
        return self

    def __call__(self, o):
        if getattr(o, "scopedStyleSheet") is not None:
            o.scopedStyleSheet.merge(self)
        else:
            o.scopedStyleSheet = self
        return o

    @classmethod
    def fromPath(cls, path : Path):
        return cls.fromString(path.read_text())

    @classmethod
    def fromString(cls, raw : str):
        from .css_parser import parseRaw
        xs = cls()
        parseRaw(raw, xs)
        return xs



    #PERFORMANCE: Figure out a better way to do this in the future
    def getStyles(self, element) -> dict:
        '''NOTE: tags < class < id | in terms of priority'''
        styles = {}
        '''dict<state : str, rules:Rules>'''
        # check for star match
        if self.selectors.get('*'):
            _update_deeper_dict(styles, self.selectors['*'], element.state)

        # check for tag match
        if self.selectors.get(element.tag):
            _update_deeper_dict(styles, self.selectors[element.tag], element.state)

        # check for class match
        for className in element.classList:
            if self.selectors.get('.' + className):
                _update_deeper_dict(styles, self.selectors['.' + className], element.state)
        # check for id
        if element.id is not None:
            if self.selectors.get('#' + element.id):
                _update_deeper_dict(styles, self.selectors['#' + element.id], element.state)
        return styles
