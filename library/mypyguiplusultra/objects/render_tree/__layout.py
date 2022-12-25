from mypyguiplusultra.core.util import Object
from mypyguiplusultra.objects.cssom import css_enums

class LayoutHelper:
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

        parentContentXStart=0, # Coordinate of top left of content box
        parentContentYStart=0,

        reflowedElement=None,
        contentSize=(0, 0) # TODO: Make this contentSizeFunction
    ):
        '''Layouts nodes with `display:block`'''

        node.layoutInformation.content_x_offset = styleHints.padding_left
        node.layoutInformation.content_y_offset = styleHints.padding_top

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
        if node is not reflowedElement:
            contentWidth, contentHeight = LayoutHelper.layoutChildren(node, node.layoutInformation.content_width, node.layoutInformation.content_x_offset, node.layoutInformation.content_y_offset)
        else:
            contentWidth, contentHeight = contentSize

        if styleHints.height is None and styleHints.aspect_ratio is None: # i.e if the height wasnt set before
            node.layoutInformation.height = LayoutHelper.validatedHeight(LayoutHelper.getHeightFromContentHeight(contentHeight, styleHints), styleHints)
            # Note that the validatedHeight might not conform with the contentHeight but that ok :) (and thats also why im recalculating the content height in the next line)

        # Set the content_height (it isnt really that important, just defining it for consistency)
        node.layoutInformation.content_height = LayoutHelper.getContentHeightFromHeight(node.layoutInformation.height, styleHints)

        # Layout the slaves that arent my children
        for i in node.slaves:
            for slave in node.slaves[i]:
                if slave().domNode().parent().renderNode is not node:
                    slave.layout(lineWidth=node.layoutInformation.content_width)

        # Set position
        node.layoutInformation.x = styleHints.margin_left + parentContentXStart
        node.layoutInformation.y = lineHeight + suggestedYPosition + max(styleHints.margin_top-providedMarginTop, 0) + parentContentYStart


        # Apply offset
        # TODO: Apply offsets

        node.setRenderInformation()

        return (
            node.layoutInformation.width + styleHints.margin_right + max(styleHints.margin_left-providedMarginLeft, 0),
            node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top-providedMarginTop, 0),
            styleHints.margin_right, styleHints.margin_bottom,
            True
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

        parentContentXStart=0, # Coordinate of top left of content box
        parentContentYStart=0,

        reflowedElement=None,
        contentSize=(0, 0)
    ):
        '''Layouts nodes with `display:inline-block`'''
        isOneNewLine = False

        node.layoutInformation.content_x_offset = styleHints.padding_left
        node.layoutInformation.content_y_offset = styleHints.padding_top

        if styleHints.width is None: # inline block elements will extend their width as much as possible if their width isnt specified
            node.layoutInformation.width = LayoutHelper.validatedWidth(lineWidth - suggestedXPosition - max(styleHints.margin_left - providedMarginLeft, 0) - styleHints.margin_right, styleHints)
        else:
            node.layoutInformation.width = LayoutHelper.validatedWidth(styleHints.width, styleHints)

        if suggestedXPosition + node.layoutInformation.width > lineWidth:
            isOneNewLine = True
        # Set the content_width (i.e the maximum space suggested for children to take)
        node.layoutInformation.content_width = LayoutHelper.getContentWidthFromWidth(node.layoutInformation.width, styleHints)

        if styleHints.height is not None: # If the height was stated, set it
            node.layoutInformation.height = LayoutHelper.validatedHeight(styleHints.height, styleHints)

        if styleHints.height is None and styleHints.aspect_ratio is not None: # If an aspect ratio is specified and height is not explicitly set, explicitly set the height
            node.layoutInformation.height = LayoutHelper.validatedHeight(node.layoutInformation.width * styleHints.aspect_ratio[1] / styleHints.aspect_ratio[0], styleHints) # height = width * (y/x)

        # NOTE: This content size is the actual size the content takes while layoutInformation.content_height and layoutInformation.content_width specify the 'maximum size' of content
        if node is not reflowedElement:
            contentWidth, contentHeight = LayoutHelper.layoutChildren(node, node.layoutInformation.content_width, styleHints.padding_left, styleHints.padding_top)
        else:
            contentWidth, contentHeight = contentSize


        if styleHints.height is None and styleHints.aspect_ratio is None: # i.e if the height wasnt set before
            node.layoutInformation.height = LayoutHelper.validatedHeight(LayoutHelper.getHeightFromContentHeight(contentHeight, styleHints), styleHints)
            # Note that the validatedHeight might not conform with the contentHeight but that ok :) (and thats also why im recalculating the content height in the next line)

        # Set the content_height (it isnt really that important, just defining it for consistency)
        node.layoutInformation.content_height = LayoutHelper.getContentHeightFromHeight(node.layoutInformation.height, styleHints)

        # Layout the slaves that arent my children
        for i in node.slaves:
            for slave in node.slaves[i]:
                if slave().domNode().parent().renderNode is not node:
                    slave.layout(lineWidth=node.layoutInformation.content_width)

        # Set position
        if isOneNewLine:
            node.layoutInformation.x = styleHints.margin_left + parentContentXStart
            node.layoutInformation.y = lineHeight + suggestedYPosition + max(styleHints.margin_top-providedMarginTop, 0) + parentContentYStart
        else:
            node.layoutInformation.x = suggestedXPosition + parentContentXStart + max(styleHints.margin_left - providedMarginLeft, 0)
            node.layoutInformation.y = suggestedYPosition + parentContentYStart + max(styleHints.margin_top - providedMarginTop, 0)

        # Apply offset
        # TODO: Apply offsets

        node.setRenderInformation()

        return (
            node.layoutInformation.width + styleHints.margin_right + max(styleHints.margin_left - providedMarginLeft, 0),
            node.layoutInformation.height + styleHints.margin_bottom + max(styleHints.margin_top - providedMarginTop, 0),
            styleHints.margin_right, styleHints.margin_bottom,
            isOneNewLine
        )

    @staticmethod
    def layoutInlineNode(node, styleHints):
        raise NotImplementedError('layout_helper.layoutInlineNode')

    @staticmethod
    def layoutFlexNode(node):
        raise NotImplementedError('layout_helper.layoutFlexNode')

    @staticmethod
    def layoutNormalNode(node, *args, **kwargs):
        '''Layouts a node thats like normal ykwim?'''
        styleHints = LayoutHelper.getStyleHints(node)

        # TODO: This should not be here bastard
        node.renderInformation.font = styleHints.font

        if styleHints.display == css_enums.Display.none:
            return 0, 0, 0, 0, False
        elif styleHints.display == css_enums.Display.block:
            return LayoutHelper.layoutBlockNode(node, styleHints, *args, **kwargs)
        elif styleHints.display == css_enums.Display.inline:
            return LayoutHelper.layoutInlineNode(node, styleHints, *args, **kwargs)
        elif styleHints.display == css_enums.Display.inline_block:
            return LayoutHelper.layoutInlineBlockNode(node, styleHints, *args, **kwargs)
        elif styleHints.display == css_enums.Display.flex:
            return LayoutHelper.layoutFlexNode(node, styleHints, *args, **kwargs)

    @staticmethod
    def layoutTextNode(node, styleHints):
        # The only difference really is that instead of getting content size with layoutChildren, we use the text size
        # NOTE: ValidatedWidth gives the final width (that we then use with textitem.setWidth())
        raise NotImplemented('layoutHelper.layoutTextNode')

    @staticmethod
    def reflow(node, reflowedElement = None, contentSize = (0, 0)):
        '''Reflows the node'''

        from .root import RootRenderNode
        if isinstance(node, RootRenderNode): # If the node is the root render node, just layout
            node.layout(reflowedElement=reflowedElement, contentSize=contentSize)
            return node

        # Store the previous position and size
        x = node.renderInformation.x
        y = node.renderInformation.y
        width = node.renderInformation.width
        height = node.renderInformation.height

        master = node.master()
        # Layout the master
        contentSize = LayoutHelper.layoutChildren(master, master.layoutInformation.content_width, node.layoutInformation.content_x_offset, node.layoutInformation.content_y_offset, reflowedElement=reflowedElement, contentSize=contentSize)

        if node.renderInformation.x == x and node.renderInformation.y == y and node.renderInformation.width == width and node.renderInformation.height == height:
            # Nothing has changed, the layout is fine
            return node

        # The layout has changed, then reflow the master
        return LayoutHelper.reflow(node.master(), reflowedElement=node, contentSize=contentSize)



    @staticmethod
    def getContentWidthFromWidth(width, styleHints):
        '''Given the width of the border box, calculates the width of the content box'''
        return width - styleHints.padding_left - styleHints.padding_right - (2 * styleHints.border_width)

    @staticmethod
    def getContentHeightFromHeight(height, styleHints):
        '''Given the height of the border box, calculates the height of the content box'''
        return height - styleHints.padding_bottom - styleHints.padding_top - (2 * styleHints.border_width)

    @staticmethod
    def getWidthFromContentWidth(content_width, styleHints):
        '''Given the width of the content box, calculates the width of the border box'''
        return content_width + styleHints.padding_left + styleHints.padding_right + (2 * styleHints.border_width)

    @staticmethod
    def getHeightFromContentHeight(content_height, styleHints):
        return content_height + styleHints.padding_bottom + styleHints.padding_top + (2 * styleHints.border_width)
        '''Given the height of the content box, calculates the height of the border box'''

    @staticmethod
    def validatedWidth(width, styleHints):
        '''Validates the width by checking min and max width'''
        if styleHints.min_width is not None and width < styleHints.min_width:return styleHints.min_width
        if styleHints.max_width is not None and width > styleHints.max_width:return styleHints.max_width
        return width

    @staticmethod
    def validatedHeight(height, styleHints):
        '''Validates the height by checking min and max height'''
        if styleHints.min_height is not None and height < styleHints.min_height:return styleHints.min_height
        if styleHints.max_height is not None and height > styleHints.max_height:return styleHints.max_height
        return height

    @staticmethod
    def getStyleHints(node):
        '''Gets the style hints from the dom node'''
        xs = Object()
        dn = node.domNode()
        if dn is None:return {}

        xs.font = (dn.styles.font_family, int(node.getValue(dn.styles.font_size)), dn.styles.font_weight)

        xs.display = dn.styles.display
        xs.aspect_ratio = dn.styles.aspect_ratio

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

    @staticmethod
    def layoutChildren(node, maxContentWidth, contentXStart, contentYStart, reflowedElement = None, contentSize = (0, 0)):
        '''Layouts the children of a node'''

        lineUnmarginedHeight = 0 # The height(max) of the current line (excluding margins)
        lineMarginedHeight = 0 # The  height(max) of the current line (including margins)

        suggestedYPosition = 0 # The vertical position 'of' the current line
        suggestedXPosition = 0 # The horizontal position 'on' the current line

        providedMarginLeft = 0 # The margin already provided towards the left (i.e. the right of the sibling element)
        providedMarginTop = 0 # The margin already provided towards the top

        contentWidth = 0 # The maximum width the children of the node are taking

        dn = node.domNode()

        for child in dn.children:

            # Elements not in normal flow are not to be layouted here
            if child.styles.position not in [css_enums.Position.static, css_enums.Position.relative]:continue

            xSpace, ySpace, marginRight, marginBottom, isOnNewLine = child.renderNode.layout(suggestedXPosition, suggestedYPosition, maxContentWidth, lineMarginedHeight, providedMarginLeft, providedMarginTop, lineMarginedHeight - lineUnmarginedHeight, contentXStart, contentYStart, reflowedElement=reflowedElement, contentSize=contentSize)
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
                # print("TEST non isOnNewLine shit properly") # debug
                suggestedXPosition += xSpace # Change suggested X
                contentWidth = max(contentWidth, suggestedXPosition) # Recheck contentWidth
                providedMarginLeft = marginRight # Same in both
                lineMarginedHeight = max(ySpace, lineMarginedHeight) # update line height if needed
                lineUnmarginedHeight = max(lineUnmarginedHeight, ySpace - marginBottom) # update line height if needed

        return (contentWidth, suggestedYPosition + lineMarginedHeight) # ez
