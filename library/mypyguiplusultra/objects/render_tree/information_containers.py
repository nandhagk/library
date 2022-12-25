
class LayoutInformationContainer:
    def init(self):
        self.x = 0
        self.y = 0

        self.width = 0
        self.height = 0

        self.content_width = 0
        self.content_height = 0

        self.scroll_region_x = 0
        self.scroll_region_y = 0

        self.content_x_offset = 0
        self.content_y_offset = 0

        self.calculated_content_size = None
    def __init__(self):
        self.init()

    def __repr__(self):
        import pprint
        return pprint.saferepr({
            'x' : self.x,
            'y' : self.y,
            'width' : self.width,
            'height' : self.height,
            'content_width' : self.content_width,
            'content_height' : self.content_height,
        })

class RenderInformationContainer:
    def __init__(self):
        self.init()
    def init(self):
        self.scroll_offset_x = 0
        self.scroll_offset_y = 0

        self.x = 0
        '''the absolute x (compared to the nearest composite)'''
        self.y = 0
        '''the absolute y (compared to the nearest composite)'''

        self.opacity = 0
        self.z_index = 1

        self.scroll_region_x = 0
        self.scroll_region_y = 0

        self.content_width  = 0
        self.content_height = 0
        self.width  = 0
        '''The width of the padding box'''
        self.height = 0
        '''The height of the padding box'''
        self.text_align = ''

        # self.border_bottom_left_radius  = 0
        # '''The bottom_left border radius'''
        # self.border_bottom_right_radius = 0
        # '''The bottom_right border radius'''
        self.border_top_left_radius     = 0
        '''The top_left border radius'''
        self.border_top_right_radius    = 0
        '''The top_right border radius'''


        self.placeholder_color = ''
        self.background_color = ''
        '''The color of the padding box'''
        self.foreground_color = ''
        '''The color of the text'''

        self.border_width = 0
        '''The width of the border'''
        self.border_color = ''
        '''The color of the border'''
        self.border_style = 0
        '''css_enums.BorderStyle'''

        self.text_overflow = 0

        self.font = None
        '''QFont'''

        self.text_offset_x = 0
        self.text_offset_y = 0

        self.mask_children = False
        '''Set to true for overflow hidden or scroll'''
        self.allow_scroll = (False, False)
        '''(allow scroll in x, allow scroll in y)'''

    def __repr__(self):
        import pprint
        return pprint.saferepr({
            'x' : self.x,
            'y' : self.y,
            'opacity' : self.opacity,
            'z_index' : self.z_index,
            'width' : self.width,
            'height' : self.height,
            # 'border_bottom_left_radius' : self.border_bottom_left_radius,
            # 'border_bottom_right_radius' : self.border_bottom_right_radius,
            'border_top_left_radius' : self.border_top_left_radius,
            'border_top_right_radius' : self.border_top_right_radius,
            'background_color' : self.background_color,
            'border_width' : self.border_width,
            'border_color' : self.border_color,
            'border_style' : self.border_style,
            'mask_children' : self.mask_children,
            'allow_scroll' : self.allow_scroll
        })
