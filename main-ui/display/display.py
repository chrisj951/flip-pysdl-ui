from display.font_purpose import FontPurpose
from display.loaded_font import LoadedFont
from display.font_size import FontSize
from display.render_mode import RenderMode
from menus.common.top_bar import TopBar
import sdl2
import sdl2.ext
import sdl2.sdlttf
from themes.theme import Theme
from devices.device import Device

class Display:
    def __init__(self, theme: Theme, device: Device):
        self.theme = theme
        self.device = device
        self._init_display()
        self.fonts = {
            purpose: self._load_font(purpose)
            for purpose in FontPurpose
        }        
        self.bg_path = ""
        self._check_for_bg_change()
        self.top_bar = TopBar(self,device,theme)
        self.clear("init")
        self.present()

    def _init_display(self):
        sdl2.ext.init(controller=True)
        sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_GAMECONTROLLER)
        display_mode = sdl2.SDL_DisplayMode()
        if sdl2.SDL_GetCurrentDisplayMode(0, display_mode) != 0:
            print("Failed to get display mode, using fallback 640x480")
            width, height = self.device.screen_width(), self.device.screen_height()
        else:
            width, height = display_mode.w, display_mode.h
            print(f"Display size: {width}x{height}")

        self.window = sdl2.ext.Window("Minimal SDL2 GUI", size=(width, height), flags=sdl2.SDL_WINDOW_FULLSCREEN)
        self.window.show()

        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"2")
        # Use default renderer flags
        self.renderer = sdl2.ext.Renderer(self.window, flags=sdl2.SDL_RENDERER_ACCELERATED)

    def _deinit_display(self):
        sdl2.SDL_DestroyRenderer(self.renderer.sdlrenderer)
        self.renderer = None
        sdl2.SDL_DestroyWindow(self.window.window)
        self.window = None
        sdl2.SDL_QuitSubSystem(sdl2.SDL_INIT_VIDEO)

    def reinitialize(self):
        self._deinit_display()
        self._init_display()
        self.clear("reinitialize")
        self.present()

    def _check_for_bg_change(self):
        if(self.bg_path != self.theme.background):
            surf = sdl2.ext.load_image(self.theme.background)
            self.background_texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.sdlrenderer, surf)
            sdl2.SDL_FreeSurface(surf)


    def _load_font(self, font_purpose):
        if sdl2.sdlttf.TTF_Init() == -1:
            raise RuntimeError("Failed to initialize SDL_ttf")

        # Load the TTF font
        # font_path = "/mnt/sdcard/spruce/Font Files/Noto.ttf"
        font_path = self.theme.get_font(font_purpose)
        font_size = self.theme.get_font_size(font_purpose)
        
        font = sdl2.sdlttf.TTF_OpenFont(font_path.encode('utf-8'), font_size)
        if not font:
            raise RuntimeError("Could not load font")
        line_height = sdl2.sdlttf.TTF_FontHeight(font)
        return LoadedFont(font,line_height)
        
    def clear(self, screen):
        self._check_for_bg_change()
        sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, self.background_texture, None, None)
        self.top_bar.render_top_bar(screen)
    
    def render(self, x, y, texture, surface, render_mode):
        adj_x = x
        adj_y = y

        # Get the width and height of the surface
        if(RenderMode.X_CENTERED == render_mode) :
            adj_x = x - int(surface.contents.w/2)
        elif(RenderMode.XY_CENTERED == render_mode):
            adj_x = x - int(surface.contents.w/2)
            adj_y = x - int(surface.contents.h/2)
        elif(RenderMode.TOP_RIGHT_ADJUST == render_mode):
            adj_x = x - int(surface.contents.w)

        rect = sdl2.SDL_Rect(adj_x, adj_y, surface.contents.w, surface.contents.h)

        # Copy the texture to the renderer
        sdl2.SDL_RenderCopy(self.renderer.renderer, texture, None, rect)

        # Clean up
        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_FreeSurface(surface)

        return surface.contents.w, surface.contents.h

    def render_text(self,text, x, y, color, purpose : FontPurpose, render_mode = RenderMode.ABSOLUTE):
        # Create an SDL_Color
        sdl_color = sdl2.SDL_Color(color[0], color[1], color[2])
        
        # Render the text to a surface
        surface = sdl2.sdlttf.TTF_RenderUTF8_Blended(self.fonts[purpose].font, text.encode('utf-8'), sdl_color)
        if not surface:
            raise RuntimeError("Failed to render text surface")

        # Create a texture from the surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.renderer, surface)
        if not texture:
            sdl2.SDL_FreeSurface(surface)
            raise RuntimeError("Failed to create texture from surface")

        return self.render(x, y, texture, surface, render_mode)

    def render_text_centered(self,text, x, y, color, purpose : FontPurpose):
        self.render_text(text, x, y, color, purpose, RenderMode.X_CENTERED)

    def render_image(self, image_path: str, x: int, y: int, render_mode = RenderMode.ABSOLUTE):
        # Load the image into an SDL_Surface
        surface = sdl2.sdlimage.IMG_Load(image_path.encode('utf-8'))
        if not surface:
            raise RuntimeError(f"Failed to load image: {image_path}")

        # Create a texture from the surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.renderer, surface)
        if not texture:
            sdl2.SDL_FreeSurface(surface)
            raise RuntimeError("Failed to create texture from surface")

        return self.render(x, y, texture, surface, render_mode)
    
    def render_image_centered(self, image_path: str, x: int, y: int):
        return self.render_image(image_path,x,y,RenderMode.X_CENTERED)

    def get_line_height(self, purpose : FontPurpose):
        return self.fonts[purpose].line_height;
        
    def present(self):
        self.renderer.present()

    def get_top_bar_height(self):
        return self.top_bar.get_top_bar_height()

    def get_image_dimensions(self, img):        
        contents = sdl2.sdlimage.IMG_Load(img.encode('utf-8')).contents
        return contents.w, contents.h
