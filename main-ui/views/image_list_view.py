from typing import List
from controller.controller_inputs import ControllerInput
from display.display import Display
from display.font_purpose import FontPurpose
from display.render_mode import RenderMode
import sdl2
from devices.device import Device
from controller.controller import Controller
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry
from views.non_descriptive_list_view import NonDescriptiveListView

class ImageListView(NonDescriptiveListView):
    SHOW_ICONS = True
    DONT_SHOW_ICONS = False

    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, top_bar_text,
                 options: List[GridOrListEntry], img_offset_x : int, img_offset_y : int, img_width : int, img_height: int,
                 selected_index : int, show_icons : bool, image_render_mode: RenderMode, selected_bg = None):
        super().__init__(display=display,
                         controller=controller,
                         device=device,
                         theme=theme,
                         top_bar_text=top_bar_text,
                         options=options,
                         selected_index=selected_index,
                         show_icons=show_icons,
                         image_render_mode=image_render_mode,
                         selected_bg=selected_bg)

        self.img_offset_x = img_offset_x
        self.img_offset_y = img_offset_y
        self.img_width = img_width
        self.img_height = img_height
    

    def _render_text(self, visible_options):
        for visible_index, (imageTextPair) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
           
            x_value = 20 #TODO get this from somewhere
            y_value = (self.base_y_offset + visible_index * self.line_height)  + self.line_height//2
            render_mode=RenderMode.MIDDLE_LEFT_ALIGNED
            if actual_index == self.selected:
                color = self.theme.text_color_selected(FontPurpose.LIST)
                if(self.selected_bg is not None):
                    self.display.render_image(self.selected_bg,0, y_value, render_mode)
            else:
                color = self.theme.text_color(FontPurpose.LIST)

            if(self.show_icons and imageTextPair.get_icon() is not None):
                icon_width, icon_height = self.display.render_image(imageTextPair.get_icon(),x_value, y_value, render_mode)
                x_value += icon_width
            else:
                pass

            self.display.render_text(imageTextPair.get_primary_text(), x_value, y_value, color, FontPurpose.LIST,
                                    render_mode)


    def _render_image(self, visible_options):
        for visible_index, (imageTextPair) in enumerate(visible_options):
            actual_index = self.current_top + visible_index
            imagePath = imageTextPair.get_image_path_selected() if actual_index == self.selected else imageTextPair.get_image_path()
            if(actual_index == self.selected and imagePath is not None):
                self.display.render_image(imagePath, 
                                     self.img_offset_x, 
                                     self.img_offset_y,
                                     self.image_render_mode,
                                     self.img_width,
                                     self.img_height)
