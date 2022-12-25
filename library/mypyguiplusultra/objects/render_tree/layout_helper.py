from mypyguiplusultra.objects.cssom import css_enums
from PyQt6.QtGui import QFont, QFontMetrics

class LayoutHelper:

    #region common layout functions (based on display property)
    @staticmethod
    def layoutHiddenNode(node, *args, **kwargs):
        '''`display:none`'''
        for child in node.domNode().children:
            child.renderNode.layout(hidden=True)

        node.setRenderInformation(hidden=True)

        return 0, 0, 0, 0, False, False

    @staticmethod
    def layoutBlockNode(
        node, styleHints,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
        contentSizeCalculator=lambda n:(0,0) # Function that calculates the size of the node's content
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''`display:block`'''
        if styleHints.width is None: # Blcck elements will extend their width as much as possible if their width isnt specified
            node.layoutInformation.width = LayoutHelper.validatedWidth(lineWidth - styleHints.margin_left - styleHints.margin_right, styleHints)
        else:
            node.layoutInformation.width = LayoutHelper.validatedWidth(styleHints.width, styleHints)
        # Set the content_width (i.e the maximum space suggested for children to take)
        node.layoutInformation.content_width = LayoutHelper.getContentWidthFromWidth(node.layoutInformation.width, styleHints)

        if styleHints.height is not None: # If the height was stated, set it
            node.layoutInformation.height = LayoutHelper.validatedHeight(styleHints.height, styleHints)

        if styleHints.height is None and styleHints.aspect_ratio is not None: # If an aspect ratio is specified and height is not explicitly set, explicitly set the height
            node.layoutInformation.height = LayoutHelper.validatedHeight(node.layoutInformation.width * styleHints.aspect_ratio[1] / styleHints.aspect_ratio[0], styleHints) # height = width * (y/x)

        # NOTE: This content size is the actual size the content takes while layoutInformation.content_height and layoutInformation.content_width specify the 'maximum size' of content
        contentWidth, contentHeight = contentSizeCalculator(node)

        node.layoutInformation.scroll_region_x = contentWidth
        node.layoutInformation.scroll_region_y = contentHeight

        if styleHints.height is None and styleHints.aspect_ratio is None: # i.e if the height wasnt set before
            node.layoutInformation.height = LayoutHelper.validatedHeight(LayoutHelper.getHeightFromContentHeight(contentHeight, styleHints), styleHints)
            # Note that the validatedHeight might not conform with the contentHeight but that ok :) (and thats also why im recalculating the content height in the next line)

        # Set the content_height (it isnt really that important, just defining it for consistency)
        node.layoutInformation.content_height = LayoutHelper.getContentHeightFromHeight(node.layoutInformation.height, styleHints)

        # Layout the slaves that arent my children
        LayoutHelper.layoutOrphanedSlaves(node)

        # Set position
        node.layoutInformation.x = styleHints.margin_left + parentContentXStart
        node.layoutInformation.y = lineHeight + suggestedYPosition + max(styleHints.margin_top-providedMarginTop, 0) + parentContentYStart

        dx, dy = LayoutHelper.getOffset(node, styleHints)
        node.layoutInformation.x += dx
        node.layoutInformation.y += dy

        if styleHints.isAbsolute:
            node.layoutInformation.x, node.layoutInformation.y = LayoutHelper.getAbsoluteyPosition(node, styleHints)

        node.setRenderInformation()

        return (
            node.layoutInformation.width + styleHints.margin_right + styleHints.margin_left,
            node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top-providedMarginTop, 0),
            styleHints.margin_right, styleHints.margin_bottom,
            True, True
        )

    @staticmethod
    def layoutInlineBlockNode(
        node, styleHints,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
        contentSizeCalculator=lambda n:(0,0) # Function that calculates the size of the node's content
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''`display:inline-block`'''
        isOnNewLine = False

        if styleHints.width is None: # Block elements will extend their width as much as possible if their width isnt specified
            node.layoutInformation.width = LayoutHelper.validatedWidth(lineWidth - suggestedXPosition - max(styleHints.margin_left - providedMarginLeft, 0) - styleHints.margin_right, styleHints)
        else:
            node.layoutInformation.width = LayoutHelper.validatedWidth(styleHints.width, styleHints)

        if suggestedXPosition + node.layoutInformation.width > lineWidth:
            isOnNewLine = True
        # Set the content_width (i.e the maximum space suggested for children to take)
        node.layoutInformation.content_width = LayoutHelper.getContentWidthFromWidth(node.layoutInformation.width, styleHints)

        if styleHints.height is not None: # If the height was stated, set it
            node.layoutInformation.height = LayoutHelper.validatedHeight(styleHints.height, styleHints)

        if styleHints.height is None and styleHints.aspect_ratio is not None: # If an aspect ratio is specified and height is not explicitly set, explicitly set the height
            node.layoutInformation.height = LayoutHelper.validatedHeight(node.layoutInformation.width * styleHints.aspect_ratio[1] / styleHints.aspect_ratio[0], styleHints) # height = width * (y/x)

        # NOTE: This content size is the actual size the content takes while layoutInformation.content_height and layoutInformation.content_width specify the 'maximum size' of content
        contentWidth, contentHeight = contentSizeCalculator(node)
        node.layoutInformation.scroll_region_x = contentWidth
        node.layoutInformation.scroll_region_y = contentHeight

        if styleHints.height is None and styleHints.aspect_ratio is None: # i.e if the height wasnt set before
            node.layoutInformation.height = LayoutHelper.validatedHeight(LayoutHelper.getHeightFromContentHeight(contentHeight, styleHints), styleHints)
            # Note that the validatedHeight might not conform with the contentHeight but that ok :) (and thats also why im recalculating the content height in the next line)

        # Set the content_height (it isnt really that important, just defining it for consistency)
        node.layoutInformation.content_height = LayoutHelper.getContentHeightFromHeight(node.layoutInformation.height, styleHints)

        # Layout the slaves that arent my children
        LayoutHelper.layoutOrphanedSlaves(node)

        # Set position
        if isOnNewLine:
            node.layoutInformation.x = styleHints.margin_left + parentContentXStart
            node.layoutInformation.y = lineHeight + suggestedYPosition + max(styleHints.margin_top-providedMarginBottom, 0) + parentContentYStart
        else:
            node.layoutInformation.x = suggestedXPosition + parentContentXStart + max(styleHints.margin_left - providedMarginLeft, 0)
            node.layoutInformation.y = suggestedYPosition + parentContentYStart + max(styleHints.margin_top - providedMarginTop, 0)

        # Apply offset
        dx, dy = LayoutHelper.getOffset(node, styleHints)
        node.layoutInformation.x += dx
        node.layoutInformation.y += dy

        if styleHints.isAbsolute:
            node.layoutInformation.x, node.layoutInformation.y = LayoutHelper.getAbsoluteyPosition(node, styleHints)

        node.setRenderInformation()

        if isOnNewLine:
            return (
                node.layoutInformation.width + styleHints.margin_right + styleHints.margin_left,
                node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top - providedMarginTop, 0),
                styleHints.margin_right, styleHints.margin_bottom,
                isOnNewLine, False
            )
        else:
            return (
                node.layoutInformation.width + styleHints.margin_right + max(styleHints.margin_left - providedMarginLeft, 0),
                node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top - providedMarginTop, 0),
                styleHints.margin_right, styleHints.margin_bottom,
                isOnNewLine, False
            )

    @staticmethod
    def layoutInlineNode(
        node, styleHints,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
        contentSizeCalculator=lambda n:(0,0) # Function that calculates the size of the node's content
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''`display:inline`'''
        isOnNewLine = False

        # NOTE: This content size is the actual size the content takes while layoutInformation.content_height and layoutInformation.content_width specify the 'maximum size' of content (They may be the same but it is not always the case)
        contentWidth, contentHeight = contentSizeCalculator(node)
        node.layoutInformation.scroll_region_x = contentWidth
        node.layoutInformation.scroll_region_y = contentHeight

        node.layoutInformation.content_width = contentWidth
        node.layoutInformation.content_height = contentHeight

        node.layoutInformation.width = LayoutHelper.validatedWidth(LayoutHelper.getWidthFromContentWidth(contentWidth, styleHints), styleHints)

        if styleHints.height is None and styleHints.aspect_ratio is None: # i.e if the height wasnt set before
            node.layoutInformation.height = LayoutHelper.validatedHeight(LayoutHelper.getHeightFromContentHeight(contentHeight, styleHints), styleHints)
            # Note that the validatedHeight might not conform with the contentHeight but that ok :) (and thats also why im recalculating the content height in the next line)

        if suggestedXPosition + node.layoutInformation.width > lineWidth:
            isOnNewLine = True

        # Layout the slaves that arent my children
        LayoutHelper.layoutOrphanedSlaves(node)

        # Set position
        if isOnNewLine:
            node.layoutInformation.x = styleHints.margin_left + parentContentXStart
            node.layoutInformation.y = lineHeight + suggestedYPosition + max(styleHints.margin_top-providedMarginBottom, 0) + parentContentYStart
        else:
            node.layoutInformation.x = suggestedXPosition + parentContentXStart + max(styleHints.margin_left - providedMarginLeft, 0)
            node.layoutInformation.y = suggestedYPosition + parentContentYStart + max(styleHints.margin_top - providedMarginTop, 0)

        # Apply offset
        dx, dy = LayoutHelper.getOffset(node, styleHints)
        node.layoutInformation.x += dx
        node.layoutInformation.y += dy


        if styleHints.isAbsolute:
            node.layoutInformation.x, node.layoutInformation.y = LayoutHelper.getAbsoluteyPosition(node, styleHints)

        node.setRenderInformation()

        if isOnNewLine:
            return (
                node.layoutInformation.width + styleHints.margin_right + styleHints.margin_left,
                node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top - providedMarginTop, 0),
                styleHints.margin_right, styleHints.margin_bottom,
                isOnNewLine, False
            )
        else:
            return (
                node.layoutInformation.width + styleHints.margin_right + max(styleHints.margin_left - providedMarginLeft, 0),
                node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top - providedMarginTop, 0),
                styleHints.margin_right, styleHints.margin_bottom,
                isOnNewLine, False
            )

    @staticmethod
    def layoutInlineOnlyNode(
        node, styleHints,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
        contentSizeCalculator=lambda n:(0,0) # Function that calculates the size of the node's content
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''`display:inline-only`'''
        isOnNewLine = False

        # NOTE: This content size is the actual size the content takes while layoutInformation.content_height and layoutInformation.content_width specify the 'maximum size' of content (They may be the same but it is not always the case)
        contentWidth, contentHeight = contentSizeCalculator(node)
        node.layoutInformation.scroll_region_x = contentWidth
        node.layoutInformation.scroll_region_y = contentHeight

        node.layoutInformation.content_width = contentWidth
        node.layoutInformation.content_height = contentHeight

        node.layoutInformation.width = LayoutHelper.validatedWidth(LayoutHelper.getWidthFromContentWidth(contentWidth, styleHints), styleHints)

        if styleHints.height is None and styleHints.aspect_ratio is None: # i.e if the height wasnt set before
            node.layoutInformation.height = LayoutHelper.validatedHeight(LayoutHelper.getHeightFromContentHeight(contentHeight, styleHints), styleHints)
            # Note that the validatedHeight might not conform with the contentHeight but that ok :) (and thats also why im recalculating the content height in the next line)


        # Layout the slaves that arent my children
        LayoutHelper.layoutOrphanedSlaves(node)

        # Set position
        if isOnNewLine:
            node.layoutInformation.x = styleHints.margin_left + parentContentXStart
            node.layoutInformation.y = lineHeight + suggestedYPosition + max(styleHints.margin_top-providedMarginBottom, 0) + parentContentYStart
        else:
            node.layoutInformation.x = suggestedXPosition + parentContentXStart + max(styleHints.margin_left - providedMarginLeft, 0)
            node.layoutInformation.y = suggestedYPosition + parentContentYStart + max(styleHints.margin_top - providedMarginTop, 0)

        # Apply offset
        dx, dy = LayoutHelper.getOffset(node, styleHints)
        node.layoutInformation.x += dx
        node.layoutInformation.y += dy

        if styleHints.isAbsolute:
            node.layoutInformation.x, node.layoutInformation.y = LayoutHelper.getAbsoluteyPosition(node, styleHints)

        node.setRenderInformation()

        if isOnNewLine:
            return (
                node.layoutInformation.width + styleHints.margin_right + styleHints.margin_left,
                node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top - providedMarginTop, 0),
                styleHints.margin_right, styleHints.margin_bottom,
                isOnNewLine, False
            )
        else:
            return (
                node.layoutInformation.width + styleHints.margin_right + max(styleHints.margin_left - providedMarginLeft, 0),
                node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top - providedMarginTop, 0),
                styleHints.margin_right, styleHints.margin_bottom,
                isOnNewLine, False
            )

    @staticmethod
    def layoutBlockInlineNode(*args, **kwargs):
        '''Basically the same as `display:inline` BUT forces siblings onto next line'''
        xs = LayoutHelper.layoutInlineNode(*args, **kwargs)
        return xs[:5] + (True,) # Ye it looks kinda jank but like it works so..... :)


    @staticmethod
    def layoutFlexNode(*args, **kwargs):
        raise NotImplementedError('layoutHelper.layoutFlexNode')
    #endregion

    @staticmethod
    def layoutNode(
        node, styleHints,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
        contentSizeCalculator=lambda n:(0,0) # Function that calculates the size of the node's content
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''Layouts basically any type of node (pushes the work onto functions based on the display property)'''
        node.layoutInformation.content_x_offset = styleHints.padding_left
        node.layoutInformation.content_y_offset = styleHints.padding_top

        if hidden or styleHints.display == css_enums.Display.none:
            return LayoutHelper.layoutHiddenNode(
                node, styleHints,
                suggestedXPosition = suggestedXPosition,
                suggestedYPosition = suggestedYPosition,
                lineWidth = lineWidth,
                lineHeight = lineHeight,
                providedMarginLeft = providedMarginLeft,
                providedMarginTop = providedMarginTop,
                providedMarginBottom = providedMarginBottom,
                parentContentXStart = parentContentXStart,
                parentContentYStart = parentContentYStart,
                contentSizeCalculator = contentSizeCalculator
            )
        elif styleHints.display == css_enums.Display.block:
            return LayoutHelper.layoutBlockNode(
                node, styleHints,
                suggestedXPosition = suggestedXPosition,
                suggestedYPosition = suggestedYPosition,
                lineWidth = lineWidth,
                lineHeight = lineHeight,
                providedMarginLeft = providedMarginLeft,
                providedMarginTop = providedMarginTop,
                providedMarginBottom = providedMarginBottom,
                parentContentXStart = parentContentXStart,
                parentContentYStart = parentContentYStart,
                contentSizeCalculator = contentSizeCalculator
            )
        elif styleHints.display == css_enums.Display.inline:
            return LayoutHelper.layoutInlineNode(
                node, styleHints,
                suggestedXPosition = suggestedXPosition,
                suggestedYPosition = suggestedYPosition,
                lineWidth = lineWidth,
                lineHeight = lineHeight,
                providedMarginLeft = providedMarginLeft,
                providedMarginTop = providedMarginTop,
                providedMarginBottom = providedMarginBottom,
                parentContentXStart = parentContentXStart,
                parentContentYStart = parentContentYStart,
                contentSizeCalculator = contentSizeCalculator
            )
        elif styleHints.display == css_enums.Display.block_inline: # NOTE: This is not a typo, inline_block is handled next
            return LayoutHelper.layoutBlockInlineNode(
                node, styleHints,
                suggestedXPosition = suggestedXPosition,
                suggestedYPosition = suggestedYPosition,
                lineWidth = lineWidth,
                lineHeight = lineHeight,
                providedMarginLeft = providedMarginLeft,
                providedMarginTop = providedMarginTop,
                providedMarginBottom = providedMarginBottom,
                parentContentXStart = parentContentXStart,
                parentContentYStart = parentContentYStart,
                contentSizeCalculator = contentSizeCalculator
            )
        elif styleHints.display == css_enums.Display.inline_block:
            return LayoutHelper.layoutInlineBlockNode(
                node, styleHints,
                suggestedXPosition = suggestedXPosition,
                suggestedYPosition = suggestedYPosition,
                lineWidth = lineWidth,
                lineHeight = lineHeight,
                providedMarginLeft = providedMarginLeft,
                providedMarginTop = providedMarginTop,
                providedMarginBottom = providedMarginBottom,
                parentContentXStart = parentContentXStart,
                parentContentYStart = parentContentYStart,
                contentSizeCalculator = contentSizeCalculator
            )
        elif styleHints.display == css_enums.Display.inline_only:
            return LayoutHelper.layoutInlineOnlyNode(
                node, styleHints,
                suggestedXPosition = suggestedXPosition,
                suggestedYPosition = suggestedYPosition,
                lineWidth = lineWidth,
                lineHeight = lineHeight,
                providedMarginLeft = providedMarginLeft,
                providedMarginTop = providedMarginTop,
                providedMarginBottom = providedMarginBottom,
                parentContentXStart = parentContentXStart,
                parentContentYStart = parentContentYStart,
                contentSizeCalculator = contentSizeCalculator
            )
        elif styleHints.display == css_enums.Display.flex:
            return LayoutHelper.layoutFlexNode(
                node, styleHints,
                suggestedXPosition = suggestedXPosition,
                suggestedYPosition = suggestedYPosition,
                lineWidth = lineWidth,
                lineHeight = lineHeight,
                providedMarginLeft = providedMarginLeft,
                providedMarginTop = providedMarginTop,
                providedMarginBottom = providedMarginBottom,
                parentContentXStart = parentContentXStart,
                parentContentYStart = parentContentYStart,
                contentSizeCalculator = contentSizeCalculator
            )
        else:
            from mypyguiplusultra.core import exceptions
            raise exceptions.UnkownDisplayValueException(node, styleHints.display)

    @staticmethod
    def reflow(node):
        '''Reflows the node'''
        master = node.master()

        if node.domNode().styles.position == css_enums.Position.absolute: # If the node is the root render node, just layout
            node.layout(lineWidth=master.layoutInformation.content_width)
            return node



        # Store the previous position and size
        x = node.renderInformation.x
        y = node.renderInformation.y
        width = node.renderInformation.width
        height = node.renderInformation.height

        # Layout the master
        contentSize = LayoutHelper.getBoxContentSize(master)

        if node.renderInformation.x == x and node.renderInformation.y == y and node.renderInformation.width == width and node.renderInformation.height == height:
            # Nothing has changed, the layout is fine
            return node

        master.layoutInformation.calculated_content_size = contentSize
        # The layout has changed, then reflow the master
        return LayoutHelper.reflow(master)

    #region layout functions that are called by render node (box, text, img)
    @staticmethod
    def layoutImageNode(
        node,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''Layouts an image node'''
        styleHints = LayoutHelper.getStyleHints(node)
        return LayoutHelper.layoutNode(
            node, styleHints,
            suggestedXPosition = suggestedXPosition,
            suggestedYPosition = suggestedYPosition,
            lineWidth = lineWidth,
            lineHeight = lineHeight,
            providedMarginLeft = providedMarginLeft,
            providedMarginTop = providedMarginTop,
            providedMarginBottom = providedMarginBottom,
            parentContentXStart = parentContentXStart,
            parentContentYStart = parentContentYStart,
            contentSizeCalculator = lambda n:n.layoutInformation.calculated_content_size if n.layoutInformation.calculated_content_size is not None else LayoutHelper.getTextContentSize(n)
        )

    @staticmethod
    def layoutTextNode(
        node,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''Layouts a text node'''
        styleHints = LayoutHelper.getStyleHints(node)
        node.renderInformation.font = QFont(*styleHints.font)
        node.renderInformation.text_overflow = styleHints.text_overflow
        node.renderInformation.text_align = styleHints.text_align
        xs = LayoutHelper.layoutNode(
            node, styleHints,
            suggestedXPosition = suggestedXPosition,
            suggestedYPosition = suggestedYPosition,
            lineWidth = lineWidth,
            lineHeight = lineHeight,
            providedMarginLeft = providedMarginLeft,
            providedMarginTop = providedMarginTop,
            providedMarginBottom = providedMarginBottom,
            parentContentXStart = parentContentXStart,
            parentContentYStart = parentContentYStart,
            contentSizeCalculator = lambda n:n.layoutInformation.calculated_content_size if n.layoutInformation.calculated_content_size is not None else LayoutHelper.getTextContentSize(n, styleHints)
        )
        node.renderInformation.text_x_offset = node.layoutInformation.content_x_offset
        node.renderInformation.text_y_offset = node.layoutInformation.content_y_offset
        if node.renderInformation.text_align == 'center':
            node.renderInformation.text_x_offset += (node.renderInformation.width - node.renderInformation.scroll_region_x) / 2
            node.renderInformation.text_y_offset += (node.renderInformation.height - node.renderInformation.scroll_region_y) / 2
        node.renderInformation.mask_children = node.renderInformation.text_overflow == css_enums.TextOverflow.clip
        return xs

    @staticmethod
    def layoutBoxNode(
        node,

        suggestedXPosition=0, # The suggested X position
        suggestedYPosition=0, # The suggested Y position

        lineWidth=0, # The maximum width suggested
        lineHeight=0, # The height of the current line

        providedMarginLeft=0, # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop=0, # The margin already provided towards the top
        providedMarginBottom=0, # The margin provided already on the next line towards the top (i.e bottom of the current line)

        parentContentXStart=0, # Coordinate of top left of content box (wrt parent)
        parentContentYStart=0,

        hidden=False, # Whether the current node must be hidden or not
    ) -> (
        float, # Space taken in x direction
        float, # Spave taken in y direction
        float, # Margin provided to the node's right
        float, # Margin provided to the node's bottom
        bool,  # Whether the node was positioned on a new line or not
        bool,  # Whether the next node is forced to be on new line or not
    ):
        '''Layouts a box node'''
        styleHints = LayoutHelper.getStyleHints(node)
        return LayoutHelper.layoutNode(
            node, styleHints,
            suggestedXPosition = suggestedXPosition,
            suggestedYPosition = suggestedYPosition,
            lineWidth = lineWidth,
            lineHeight = lineHeight,
            providedMarginLeft = providedMarginLeft,
            providedMarginTop = providedMarginTop,
            providedMarginBottom = providedMarginBottom,
            parentContentXStart = parentContentXStart,
            parentContentYStart = parentContentYStart,
            contentSizeCalculator = lambda n:n.layoutInformation.calculated_content_size if n.layoutInformation.calculated_content_size is not None else LayoutHelper.getBoxContentSize(n)
        )
    #endregion

    #region offsets
    @staticmethod
    def getOffset(node, styleHints):
        dx = 0 # If the node is not a relatively positioned object, then the offset is 0,0
        dy = 0
        if styleHints.isRelative:
            if styleHints.left is not None:
                dx = styleHints.left
            elif styleHints.right is not None:
                dx = -styleHints.right

            if styleHints.top is not None:
                dy = styleHints.top
            elif styleHints.bottom is not None:
                dy = -styleHints.bottom
        return dx, dy

    @staticmethod
    def getAbsoluteyPosition(node, styleHints): # It is not a type
        '''Calculates the position of an absolutely positioned node'''
        x = styleHints.margin_left
        y = styleHints.margin_top

        master_w = node.master().layoutInformation.width
        master_h = node.master().layoutInformation.height

        if styleHints.left is not None:
            x = styleHints.left + styleHints.margin_left
        elif styleHints.right is not None:
            x = master_w - node.layoutInformation.width - styleHints.right - styleHints.margin_right

        if styleHints.top is not None:
            y = styleHints.top + styleHints.margin_top
        elif styleHints.bottom is not None:
            y = master_h - node.layoutInformation.height - styleHints.bottom - styleHints.margin_bottom

        return x,y

    #region nice util
    @staticmethod
    def layoutOrphanedSlaves(node):
        '''Layout all the slaves that arent the node's children'''
        for slave in LayoutHelper.iterateSlaves(node):
            if slave.domNode().styles.position not in [css_enums.Position.static, css_enums.Position.relative]:
                slave.layout(lineWidth=node.layoutInformation.content_width)

    @staticmethod
    def iterateSlaves(node):
        '''Iterates through all the slaves of the node'''
        for i in node.slaves:
            for slave in node.slaves[i]:
                yield slave()

    @staticmethod
    def getStyleHints(node) -> object:
        '''Gets the style hints from the dom node'''
        from mypyguiplusultra.core.util import Object

        xs = Object()
        dn = node.domNode()
        if dn is None:return xs

        xs.font = (dn.styles.font_family, int(node.getValue(dn.styles.font_size)), dn.styles.font_weight)
        xs.text_overflow = dn.styles.text_overflow
        xs.text_align = dn.styles.text_align

        xs.display = dn.styles.display
        xs.aspect_ratio = dn.styles.aspect_ratio

        xs.isAbsolute = dn.styles.position == css_enums.Position.absolute
        xs.isRelative = dn.styles.position == css_enums.Position.relative

        xs.top = node.getValue(dn.styles.top, default=None)
        xs.bottom = node.getValue(dn.styles.bottom, default=None)
        xs.right = node.getValue(dn.styles.right, default=None)
        xs.left = node.getValue(dn.styles.left, default=None)

        xs.padding_top = node.getValue(dn.styles.padding_top)
        xs.padding_right = node.getValue(dn.styles.padding_right)
        xs.padding_bottom = node.getValue(dn.styles.padding_bottom)
        xs.padding_left = node.getValue(dn.styles.padding_left)
        xs.margin_top = node.getValue(dn.styles.margin_top)
        xs.margin_right = node.getValue(dn.styles.margin_right)
        xs.margin_bottom = node.getValue(dn.styles.margin_bottom)
        xs.margin_left = node.getValue(dn.styles.margin_left)
        xs.border_width = node.getValue(dn.styles.border_width)

        xs.max_height = node.getValue(dn.styles.max_height, default=None)
        xs.min_height = node.getValue(dn.styles.min_height, default=None)
        xs.max_width = node.getValue(dn.styles.max_width, default=None)
        xs.min_width = node.getValue(dn.styles.min_width, default=None)

        xs.height = node.getValue(dn.styles.height, default=None)
        xs.width = node.getValue(dn.styles.width, default=None)
        if dn.styles.box_sizing == css_enums.BoxSizing.content_box:

            if xs.content_height is not None:xs.height += (2 * xs.border_width) + xs.padding_bottom + xs.padding_top
            if xs.content_width is not None: xs.width  += (2 * xs.border_width) + xs.padding_left + xs.padding_right

            if xs.max_height is not None:xs.max_height += (2 * xs.border_width) + xs.padding_bottom + xs.padding_top
            if xs.min_height is not None:xs.min_height += (2 * xs.border_width) + xs.padding_bottom + xs.padding_top
            if xs.max_width is not None:xs.max_width += (2 * xs.border_width) + xs.padding_left + xs.padding_right
            if xs.min_width is not None:xs.min_width += (2 * xs.border_width) + xs.padding_left + xs.padding_right
        return xs
    #endregion

    #region Content size calculation
    @staticmethod
    def getTextContentSize(node, styleHints) -> (float, float):
        '''


        '''
        #https://doc.qt.io/qtforpython/PySide6/QtGui/QFontMetrics.html
        fm = QFontMetrics(node.renderInformation.font)
        if styleHints.text_overflow == css_enums.TextOverflow.clip or styleHints.text_overflow == css_enums.TextOverflow.nowrap:
            size = fm.size(0, node.domNode().content)
            return size.width(), size.height()
        if styleHints.text_overflow ==css_enums.TextOverflow.wrap:
            from PyQt6.QtCore import Qt
            size = fm.boundingRect(0, 0, int(node.layoutInformation.content_width), 0, Qt.TextFlag.TextWordWrap, node.domNode().content)
            return size.width(), size.height()

        return 32, 32
        raise NotImplementedError('layoutHelper.getTextContentSize')

    @staticmethod
    def getImageContentSize(node) -> (float, float):
        raise NotImplementedError('layoutHelper.getImageContentSize')

    @staticmethod
    def getBoxContentSize(node) -> (float, float):
        '''Layouts the children of a node'''
        maxContentWidth, contentXStart, contentYStart = node.layoutInformation.content_width, node.layoutInformation.content_x_offset, node.layoutInformation.content_y_offset

        lineUnmarginedHeight = 0 # The height(max) of the current line (excluding margins)
        lineMarginedHeight = 0 # The  height(max) of the current line (including margins)

        suggestedYPosition = 0 # The vertical position 'of' the current line
        suggestedXPosition = 0 # The horizontal position 'on' the current line

        providedMarginLeft = 0 # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop = 0 # The margin already provided towards the top

        contentWidth = 0 # The maximum width the children of the node are taking

        dn = node.domNode()
        nextForcedOnNewLine = False
        for child in dn.children:

            # Elements not in normal flow are not to be layouted here
            if child.styles.position not in [css_enums.Position.static, css_enums.Position.relative]:continue


            xSpace, ySpace, marginRight, marginBottom, isOnNewLine, nextForcedOnNewLine = child.renderNode.layout(suggestedXPosition, suggestedYPosition, maxContentWidth, lineMarginedHeight, providedMarginLeft, providedMarginTop, lineMarginedHeight - lineUnmarginedHeight, contentXStart, contentYStart)
            # NOTE: The xSpace and ySpace are space taken wrt suggested pos or next suggested pos

            if isOnNewLine:

                contentWidth = max(contentWidth, xSpace) # I recheck the contentWidth
                suggestedXPosition = xSpace # If I am on a new line the next suggested position is 0+xSpace
                suggestedYPosition += lineMarginedHeight # The next line basically

                lineMarginedHeight = ySpace # Only this element is on the line right now
                lineUnmarginedHeight = ySpace - marginBottom # Only this element is there on the line right now

                providedMarginLeft = marginRight # Same in both
                providedMarginTop = lineMarginedHeight - lineUnmarginedHeight # I need to update the margins given

            else:
                suggestedXPosition += xSpace # Change suggested X
                contentWidth = max(contentWidth, suggestedXPosition) # Recheck contentWidth
                providedMarginLeft = marginRight # Same in both
                lineMarginedHeight = max(ySpace, lineMarginedHeight) # update line height if needed
                lineUnmarginedHeight = max(lineUnmarginedHeight, ySpace - marginBottom) # update line height if needed

            if nextForcedOnNewLine: # THIS IS NOT NEEDED AS LONG AS THE NEXT ELEMENT LIKE KNOWS HOW TO CALCULATE THEIR WIDTH (ONLY USEFUL WHEN INLINE BLOCK ELEMENT IS AFTER BLOCK ELEMENT)
                contentWidth = max(contentWidth, xSpace) # I recheck the contentWidth

                suggestedXPosition = 0 # If I am on a new line the next suggested position is 0+xSpace
                suggestedYPosition += lineMarginedHeight # The next line basically

                providedMarginTop = lineMarginedHeight - lineUnmarginedHeight # I need to update the margins given

                lineMarginedHeight = 0 # No element is on the line right now
                lineUnmarginedHeight = 0 # No element is there on the line right now

                providedMarginLeft = 0

        return (contentWidth, suggestedYPosition + lineMarginedHeight) # ez
    #endregion

    #region Size calculation
    @staticmethod
    def getContentWidthFromWidth(width, styleHints) -> float:
        '''Given the width of the border box, calculates the width of the content box'''
        return width - styleHints.padding_left - styleHints.padding_right - (2 * styleHints.border_width)

    @staticmethod
    def getContentHeightFromHeight(height, styleHints) -> float:
        '''Given the height of the border box, calculates the height of the content box'''
        return height - styleHints.padding_bottom - styleHints.padding_top - (2 * styleHints.border_width)

    @staticmethod
    def getWidthFromContentWidth(content_width, styleHints) -> float:
        '''Given the width of the content box, calculates the width of the border box'''
        return content_width + styleHints.padding_left + styleHints.padding_right + (2 * styleHints.border_width)

    @staticmethod
    def getHeightFromContentHeight(content_height, styleHints) -> float:
        return content_height + styleHints.padding_bottom + styleHints.padding_top + (2 * styleHints.border_width)
        '''Given the height of the content box, calculates the height of the border box'''

    @staticmethod
    def validatedWidth(width, styleHints) -> float:
        '''Validates the width by checking min and max width'''
        if styleHints.min_width is not None and width < styleHints.min_width:return styleHints.min_width
        if styleHints.max_width is not None and width > styleHints.max_width:return styleHints.max_width
        return width

    @staticmethod
    def validatedHeight(height, styleHints) -> float:
        '''Validates the height by checking min and max height'''
        if styleHints.min_height is not None and height < styleHints.min_height:return styleHints.min_height
        if styleHints.max_height is not None and height > styleHints.max_height:return styleHints.max_height
        return height
    #endregion
