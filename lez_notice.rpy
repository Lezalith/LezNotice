
###### Style and Preferences ##########################################################################################

### Transform of every notice.
transform notice_trans():
    yoffset 30 alpha 1.0 xoffset 30
    linear 4.0  yoffset 200 alpha 0.0

### Style of the notice's frame.
style notice_frame:
    background Frame("gui/notify.png")

### Style of a plain text notice.
style notice_text:
    color "fff"
    italic True

### Preference variables

# Seconds for how long the notice is guaranteed to be shown.
# This should be equal or slightly longer than how long the transform takes.
define notice_time = 4.5

# Seconds of how often an attempt at marking* old notice(s) is executed.
# Should be faster if you display notices often and/or many at once.
define notice_remove_interval = 10.0

# If True, certain print statements are ran that output to the console.
define notice_log_add = False    # Prints whenever a new notice gets shown and what it is.
define notice_log_remove = False # Prints whenever an old notice gets marked* to be removed and what it is.
define notice_log_clear = False  # Prints a notification when the list is cleared of all notices.

# *How removal of old notices from memory works (More technical talk):
#
# Old notices are marked periodically, and everytime that happens, the script
# checks whether all notices are marked, and if so, clears all of them from memory.
#
# This is to improve performance while not affecting the list of notices while any
# of them are being shown (as that messes up transforms).

###### Code ###########################################################################################################

### Working stuff ######

# List containing all the current notices - tuple of (displayable, timestamp_when_shown)
define notice_list = []

init -1 python:

    # For recording time
    from time import time

    # Adds a new notice.
    def new_notice(message, image = False):
        global notice_list, Text, notice_log_add

        # If message is supposed to be an image, use the usual rules to determine name/file.
        if image is True:
            message = renpy.displayable(message)

        # If message is a string, convert it to a Text displayable.
        elif isinstance(message, str):
            message = Text(message, style = "notice_text")

        # In any other case, message should be a Displayable.

        # Current timestamp.
        t = time()

        # Add it to the list of notices being shown, with the current time recorded.
        notice_list.append((message, t))

        if notice_log_add:
            print("[Notice] At the time of {}, new notice added: {}".format(t, message))

    def mark_old_notices():
        global notice_list, notice_log_remove

        # Do something only when the list isn't empty.
        for i, notice_tuple in enumerate(notice_list):

            # Skip already marked notices.
            if notice_tuple == (None,):
                continue

            # If the notice has been on for longer than notice_time, mark it as None.
            if notice_tuple[1] + notice_time <= time():

                if notice_log_remove:
                    print("[Notice] At the time of {}, notice marked for removal: {}".format(time(), notice_tuple[0]))

                notice_list[i] = (None,)

                # Check if we're at the end of notice_list.
                if i == len(notice_list) - 1:

                    # Check if the list now only contains None values, meaning nothing is being shown.
                    if notice_list.count((None,)) == len(notice_list):
                        clear_notices()

    # Clears notice_list.
    def clear_notices():
        global notice_list, notice_log_clear
        notice_list = []
        if notice_log_clear:
            print("[Notice] At the time of {}, the list of notices has been cleared.".format(time()))

# Run clear_notices when the game (re)starts.
define config.start_callbacks += [clear_notices]

### Screen stuff #######

# Screen displaying all the notices.
screen notice_screen():

    # Timer responsible for marking and removing old notices. 
    timer store.notice_remove_interval action Function(mark_old_notices) repeat True 

    zorder 99 # Just below Ren'Py's Notify, to make sure it's not overwritten. Could be changed if needed.
    style_prefix "notice"

    # Display of all the notices.
    for notice_tuple in store.notice_list:
        frame at notice_trans:
            add notice_tuple[0]

# Make sure the screen is part of the overlay - screens on top.
define config.overlay_screens += ["notice_screen"]

####### Examples ######################################################################################################

init python:

    def displayable_ex_func(st, at):
        t = round((st + 1) * 5, 3)
        return (Text(str(t)), 0.1)

image example_image = Solid("f80", xysize = (200, 200))

label lezNotice_examples:
    scene ex

    "Lezalith" "I'm about to display some notices!"

    $ new_notice("A plain notice!")
    "Lezalith" "First, a plain text one."

    $ new_notice(Text("Text displayable notice!", color = "0f0", underline = True))
    "Lezalith" "Second, a Displayable Text."

    $ new_notice("gui/window_icon.png", image = True)
    "Lezalith" "Third, an Image Displayable from a file."

    $ new_notice("example_image", image = True)
    "Lezalith" "Fourth, an Image Displayable from an image statement."

    $ a = DynamicDisplayable(displayable_ex_func)
    $ new_notice(a)
    "Lezalith" "Fifth, Displayable that's a bit more complex (DynamicDisplayable specifically)."

    "Finally, let me show a couple of notices in quick succession."
    $ new_notice("First!")
    "Lezalith" "One!"
    $ new_notice("Second!")
    "Lezalith" "Two!"
    $ new_notice("Third!")
    "Lezalith" "Three!"
    "Lezalith" "Stop! It was just those three."

    "Lezalith" "And that's it. Ready to go back?"
    return