# This file contains the code to style the Black & White Horror UI theme correctly. You can copy this file into your own project's game folder. Remember to also include the fonts from the font's folder and all the necessary gui files.
# You will also need to adjust some portions of code in your screens.rpy and options.rpy files in your project. Please have a look at these files in this example project and search for the comments "CUSTOM CODE". Then change the code the same way in your own project's files.

## Fonts
# This UI theme uses two fonts from google fonts called IMFellDWPica and Literata.
# You can swap these for your own fonts if you want. In that case, change the name of the variable as well and go through this file to update the font settings to use that name instead.
define imfelldwpica_font = "fonts/IMFellDWPica/IMFellDWPica-Regular.ttf"
define literata_font = "fonts/Literata/Literata-Regular.ttf"

define aashigemingxinpian_font = "fonts/AaShiGeMingXinPian-2.ttf"

## General Interface
# The font used for text for user interface elements, like the main and game menus, buttons, and so on.
define gui.interface_text_font = imfelldwpica_font
# The accent color is used in many places in the GUI, including titles and labels.
define gui.accent_color = "#ffffff"
# In-game text
define gui.text_font = aashigemingxinpian_font
# Color of dialogue text as well as other text displayables (like the sync screen in load/save menu's).
define gui.text_color = "#ffffff"
# General buttons
style button_text font aashigemingxinpian_font
style button_text idle_color "#ffffff"
style button_text hover_color "#9e9e9e"
style button_text selected_color "#9e9e9e"

## Say/ADV-dialogue
style say_window xalign 0.5
style say_window xsize 1000
style say_window ysize 250
style say_label color "#ffffff"
style say_label font aashigemingxinpian_font
style say_label size 45
style say_label text_align 0.0
style namebox padding (0, 0, 0, 0)
style say_dialogue size 28
style say_dialogue adjust_spacing True

define gui.name_xpos = 0.0
define gui.name_ypos = 0.12
define gui.dialogue_xpos = 0.0
define gui.dialogue_ypos = 0.35
define gui.namebox_borders = Borders(3, 0, 3, 17, 10, 0, 10, 0)
define gui.namebox_tile = True
define gui.namebox_height = 55

# CTC (click-to-continue)
image ctc:
    "gui/ctc.png"
    zoom 1.0
    offset(10, 10)
    easein 1.0 offset(10, 15)
    easein 1.0 offset(10, 10)
    repeat

## NVL dialogue
style nvl_label size 35
style nvl_label yalign 0.0
style nvl_dialogue size 27
style nvl_dialogue adjust_spacing True
style nvl_dialogue yoffset 30
style nvl_button_text size 27

define gui.nvl_height = None
define gui.nvl_spacing = 30
define gui.nvl_borders = Borders(75, 75, 75, 75, 0, 0, 0, 0) # For padding the nvl window only.
define gui.nvl_name_xpos = 0.3
define gui.nvl_name_xalign = 0.0
define gui.nvl_text_xpos = 0.3
define gui.nvl_text_width = 720
define gui.nvl_thought_xpos = 0.3
define gui.nvl_thought_width = 720
define gui.nvl_button_xpos = 0.3

## Quick menu
style quick_button_text:
    idle_color "#ffffff"
    hover_color "#9e9e9e"
    selected_color "#9e9e9e"
    insensitive_color "#4b4b4b"

define gui.quick_button_text_font = aashigemingxinpian_font
define gui.quick_button_text_size = 25

## Frames
define gui.frame_borders = Borders(43, 43, 43, 43, 20, 20, 20, 20)

## Confirm
style confirm_button ysize 25
style confirm_prompt_text color "#ffffff"
define gui.confirm_frame_borders = Borders(43, 43, 43, 43, 50, 30, 50, 30)

style choice_button_text:
    yalign 0.5

define gui.choice_button_text_font = aashigemingxinpian_font
define gui.choice_button_height = 70
define gui.choice_button_text_idle_color = "#bdbdbd"
define gui.choice_button_text_hover_color = "#ffffff"

style nvl_button:
    ysize 30 
    padding (0, 0)
    hover_background "#dedede"

## Notify
style notify_frame padding (30, 10, 60, 10)
style notify_text font aashigemingxinpian_font
style notify_text color "#ffffff"

define gui.notify_frame_borders = Borders(0, 7, 65, 7)

## Skip
style skip_frame padding (30, 10, 60, 10)
style skip_triangle line_spacing 0
style skip_triangle line_leading 0
style skip_text color "#ffffff"

define gui.skip_frame_borders = Borders(0, 7, 65, 7)

## Game/Main Menu's
# Navigation
# Remove the "size_group" for navigation menu items so they're not all the same size, and then apply a custom spacing between them.
style navigation_button size_group None
define gui.navigation_spacing = 10

style navigation_button_text:
    idle_color "#ffffff"
    hover_color "#9e9e9e"
    font aashigemingxinpian_font
    size 40

# The naivgation frame displayable is used to reserve space for the default left side navigation menu.
style game_menu_navigation_frame:
    xsize 0 # Since we relocated the menu to the bottom instead, we can now "remove" that empty space to allow the menu content to take more of that space.
    background "gui/sub_menu_background.png"
    yoffset -30

style game_menu_label_text:
    font aashigemingxinpian_font
    size 65

style game_menu_label:
    xanchor 0.0
    xpos 0.18
    xsize 1300
    yalign 0.05
    ysize 90
    top_padding 40
    bottom_padding 10
    left_padding 20
    right_padding 20

## Scrollbars
style vscrollbar:
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", Borders(10, 10, 10, 10, 0, 0, 0, 0))
    thumb "gui/scrollbar/vertical_[prefix_]thumb.png"
    thumb_offset 13
    top_gutter 10
    bottom_gutter 10
    xsize 38

style scrollbar:
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", Borders(10, 10, 10, 10, 0, 0, 0, 0))
    thumb "gui/scrollbar/horizontal_[prefix_]thumb.png"
    thumb_offset 13
    left_gutter 10
    right_gutter 10
    ysize 38

## Bars
define gui.bar_borders = Borders(15, 15, 15, 15)
define gui.vbar_borders = Borders(15, 15, 15, 15)

style bar ysize 31

## Menu content
style game_menu_content_frame:
    # Change the width of the game menu's content to be full width, now that the menu is horizontal on the bottom instead.
    left_margin 0
    xfill True

style game_menu_side:
    xpos 350
    # Change the height of the game menu's content, so it doesn't overlap the menu items at the bottom.
    ysize 700

## Preferences
style radio_button_text:
    selected_color "#ffffff"
    line_leading -10

style radio_button left_padding 40

style check_button_text:
    selected_color "#ffffff"
    line_leading -10

style check_button left_padding 40

## Save/Load menu
style page_label yalign -0.05
style slot_button_text:
    insensitive_color "#dedede"
    idle_color "#ffffff"

style slot_grid:
    yspacing -20
    yoffset -10

## Help menu
style help_text:
    color "#ffffff"

## About menu
style about_text color "#ffffff"

## History
style history_text color "#ffffff"
style history_text size 30
style history_name xsize 180
style history_name_text text_align 0.5
style history_name_text minwidth 180
style history_name_text size 30
style history_name_text left_padding 20
style history_window xfill False
style history_window ysize None
style history_window ymargin 20

define gui.history_height = None

## Return button
style return_button idle_background "gui/back_idle_button.png"
style return_button hover_background "gui/back_hover_button.png"
style return_button left_padding 50
style return_button top_padding 0
style return_button xalign 0.1
style return_button yalign 0.14
style return_button xsize 190
style return_button_text yalign 0.5
style return_button_text line_leading -15

## Sliders
style slider:
    thumb_offset 13
    left_gutter 10
    right_gutter 10
    right_bar "gui/slider/horizontal_reveal_bar.png"

style vslider:
    thumb_offset 13
    top_gutter 10
    bottom_gutter 10

define gui.slider_tile = True
define gui.slider_size = 38
