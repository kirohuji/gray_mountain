
define e = Character("Eileen", kind = adv, ctc="ctc")
# Narrator NVL-style
#define narrator = Character(kind = nvl, ctc = "ctc", what_italic = True, what_size = 27, what_yoffset = -10)
# Narrator ADV-style
define narrator = Character(kind = adv, ctc = "ctc", what_xalign = 0.5, what_italic = True, what_size = 30)

screen bar_test:
    frame:
        align (0.5, 0.5)
        xysize (800, 400)
        vbox:
            align (0.5, 0.5)
            spacing 20
            text "Survival" size 40 xalign 0.5
            text "Your survival potential is at 50%." size 30 xalign 0.5
            bar value 50 range 100 xsize 400 xalign 0.5
            textbutton "OK" text_size 35 action Jump("choices") xalign 0.5

label choices:
    # NVL-style menu.
    # menu(nvl = True):
    #     "What will you do?"
    #     "> Go towards the house":
    #         call test_label("house")
    #     "> Go further into the forest":
    #         call test_label("forest")
    #     "> Go back":
    #         call test_label("back")
    
    # ADV-style menu.
    menu:
        "What will you do?"
        "Go towards the house":
            call test_label("house")
        "Go further into the forest":
            call test_label("forest")
        "Go back":
            call test_label("back")
        
label test_label(chosen_path):
    if chosen_path == "house":
        "Your legs are numb from the cold air as you hastely make your way toward the house."
    elif chosen_path == "forest":
        "You cross the river to go further into the forest. Your feet keep slipping on the slippery rocks, but you make it across in one piece."
    elif chosen_path == "back":
        "You decided to go back and see if there's another path."

label start:
    scene background
    e "The air is getting colder by the minute! I better find shelter fast."
    $renpy.notify("Hurry before you freeze!")
    e "I think I can see a lit window in the distance."
    call screen bar_test

    return
