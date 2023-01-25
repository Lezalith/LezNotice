###### Style and Preferences ##########################################################################################

### Transform of every notice.
transform leznotice.notice_trans():
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
define leznotice.notice_time = 4.5

# Seconds of how often an attempt at marking* old notice(s) is executed.
# Should be faster if you display notices often and/or many at once.
define leznotice.notice_remove_interval = 10.0

# If True, certain print statements are ran that output to the console.
define leznotice.notice_log_add = False    # Prints whenever a new notice gets shown and what it is.
define leznotice.notice_log_remove = False # Prints whenever an old notice gets marked* to be removed and what it is.
define leznotice.notice_log_clear = False  # Prints a notification when the list is cleared of all notices.

# *How removal of old notices from memory works (More technical talk):
#
# Old notices are marked periodically, and everytime that happens, the script
# checks whether all notices are marked, and if so, clears all of them from memory.
#
# This is to improve performance while not affecting the list of notices while any
# of them are being shown (as that messes up transforms).

###### Code ###########################################################################################################

### Working stuff ######

init -1 python in leznotice:

    # For recording time
    from time import time

    from store import Text

    # List containing all the current notices - tuple of (displayable, timestamp_when_shown)
    notice_list = []

    # Adds a new notice.
    def new_notice(entry, image=False):
        global notice_list

        # If entry is a string, convert it to a Text displayable.
        if isinstance(entry, str) and not image:
            entry = Text(entry, style="notice_text")

        # In any other case, entry should be a Displayable(-able).
        else:
            entry = renpy.displayable(entry)

        # Current timestamp.
        t = time()

        # Add it to the list of notices being shown, with the current time recorded.
        # This maintains increasing order of timestamps in the list
        notice_list.append((entry, t))

        if notice_log_add:
            print("[Notice] At the time of {}, new notice added: {}".format(t, entry))

    def mark_old_notices():
        global notice_list

        t = time()

        # Do something only when the list isn't empty.
        while notice_list and ((notice_list[0][1] + notice_time) <= t):

            if notice_log_remove:
                print("[Notice] At the time of {}, notice marked for removal: {}".format(t, notice_list[0][0]))

            notice_list.pop(0)

        # Not really useful now, but kept in for compatibility.
        if notice_log_remove and not notice_list:
            print("[Notice] At the time of {}, the list of notices has been cleared.".format(t))

### Screen stuff #######

# Screen displaying all the notices.
screen notice_screen():

    # Timer responsible for marking and removing old notices.
    timer leznotice.notice_remove_interval action Function(leznotice.mark_old_notices) repeat True

    zorder 99 # Just below Ren'Py's Notify, to make sure it's not overwritten. Could be changed if needed.
    style_prefix "notice"

    # Display of all the notices.
    for notice_tuple in leznotice.notice_list:
        frame:
            at leznotice.notice_trans
            add notice_tuple[0]

# Make sure the screen is part of the overlay - screens on top.
define config.overlay_screens += ["notice_screen"]
