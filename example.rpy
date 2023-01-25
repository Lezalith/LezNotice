init python:

    def displayable_ex_func(st, at):
        t = round((st + 1) * 5, 3)
        return (Text(str(t)), 0.1)

image example_image = Solid("f80", xysize = (200, 200))

label lezNotice_examples:
    scene ex

    "Lezalith" "I'm about to display some notices!"

    $ leznotice.new_notice("A plain notice!")
    "Lezalith" "First, a plain text one."

    $ leznotice.new_notice(Text("Text displayable notice!", color = "0f0", underline = True))
    "Lezalith" "Second, a Displayable Text."

    $ leznotice.new_notice("gui/window_icon.png", image=True)
    "Lezalith" "Third, an Image Displayable from a file."

    $ leznotice.new_notice("example_image", image=True)
    "Lezalith" "Fourth, an Image Displayable from an image statement."

    $ a = DynamicDisplayable(displayable_ex_func)
    $ leznotice.new_notice(a)
    "Lezalith" "Fifth, Displayable that's a bit more complex (DynamicDisplayable specifically)."

    "Finally, let me show a couple of notices in quick succession."
    $ leznotice.new_notice("First!")
    "Lezalith" "One!"
    $ leznotice.new_notice("Second!")
    "Lezalith" "Two!"
    $ leznotice.new_notice("Third!")
    "Lezalith" "Three!"
    "Lezalith" "Stop! It was just those three."

    "Lezalith" "And that's it. Ready to go back?"
    return
