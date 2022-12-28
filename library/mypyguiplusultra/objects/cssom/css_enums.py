from mypyguiplusultra.core.util import Enum

class Unit(Enum):
    '''Specifies all the known units'''
    px               = Enum.auto(first=True)
    em               = Enum.auto()
    rem              = Enum.auto()
    viewport_height  = Enum.auto()
    viewport_width   = Enum.auto()
    null             = Enum.auto()

    master_height    = Enum.auto()
    master_width     = Enum.auto()
    self_height      = Enum.auto()
    self_width       = Enum.auto()

class Position(Enum):
    '''How the element should be placed on the screen'''
    static   = Enum.auto(first=True) # Normal flow of the page
    relative = Enum.auto() # Get normal position but can move itself
    fixed    = Enum.auto() # Positioned wrt the body (cannot scroll)
    absolute = Enum.auto() # Position wrt the nearest relative parent
    #sticky   = Enum.auto() # Static until a point then fixed


class Display(Enum):
    '''How the element should be displayed'''
    none = Enum.auto(first=True)
    block = Enum.auto() # default width is to fill and forces siblings on next
    inline = Enum.auto() # width is the widht of content, deos not force sibling on next
    inline_block = Enum.auto() # width is fill, does not force sibling on next
    flex = Enum.auto()
    block_inline = Enum.auto() # width is width of content and foces sibling on next (opposite of inline block)
    inline_only = Enum.auto() # Same as inline but does not move to next line if width is too much
    inline_block_only = Enum.auto() # Same as inline-block but does not move to next line if width is too much
    #inlineFlex = Enum.auto()
    # grid = Enum.auto() # not implemented
    #inlineGrid = Enum.auto()
    #flowRoot = Enum.auto()

class Overflow(Enum):
    none = Enum.auto(first=True)
    hidden = Enum.auto()
    scroll = Enum.auto()

class TextOverflow(Enum):
    nowrap = Enum.auto(first=True)
    wrap = Enum.auto()
    clip = Enum.auto()
    ellipsis = Enum.auto()

class Visibility(Enum):
    visible = Enum.auto(first=True)
    hidden  = Enum.auto()

class BoxSizing(Enum):
    content_box = Enum.auto(first=True)
    border_box  = Enum.auto()

class FontVariant(Enum):
    normal = Enum.auto(first=True)
    small_caps = Enum.auto()

class BorderWidth(Enum):
    medium = Enum.auto(first=True)
    thin = Enum.auto()
    thick = Enum.auto()

class BorderStyle(Enum):
    none = Enum.auto(first=True)
    dotted = Enum.auto()
    dashed = Enum.auto()
    solid = Enum.auto()
    # double = Enum.auto()
    # groove = Enum.auto()
    # ridge = Enum.auto()
    # inset = Enum.auto()
    # outset = Enum.auto()
