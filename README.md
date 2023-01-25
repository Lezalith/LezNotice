# Displaying multiple notices inside Ren'Py Projects
In Ren'Py code, the `renpy.notify` function can be used to display a simple message on a pre-defined screen (located on top left by default). It is great for testing or, well, notifying the player, but comes with some limitations, mainly that it only takes a string - even if that string can use Ren'Py text tags.

LezNotice can be viewed as an improved version of this function, always showing a Displayable, aka an image.

- It can take a string with possible text tags, just like `renpy.notify`, but that Text is always converted into a displayable according to a pre-defined style.
- It can take a displayable or a defined image to display it instead of text.

# How to use
All of the code is located in a single file, **lez_notice.rpy**. It is split into three sections:

- Style and Preferences
- Code
- Examples

## Style and Preferences
First part allows for quick setup of the script. It consists of a **transform** and several **styles** and **preference variables**.

```py
transform notice_trans():
    yoffset 30 alpha 1.0 xoffset 30
    linear 4.0  yoffset 200 alpha 0.0
```
`notice_trans` is the **transform** used by every notice displayed. By default, it displays it at the left side of the screen slowly moving down and fading away.

```py
style notice_frame:
    background Frame("gui/notify.png")
```
`notice_frame` is the **style** that represents frames the notices are contained in. Besides other things, **background** can be set to **None** to make them invisible.

```py
style notice_text:
    color "fff"
    italic True
```
`notice_text` is the **style** that is used for notices created with only a text string. While `notice_frame` is used directly inside the screen responsible for displaying the notices, `notice_text` is used for Text displayable generation.

```py
define notice_time = 4.5
```
`notice_time` is a **variable** which should be a **float**. It is the time Notices are guaranteed to be on screen before the script tries to remove them. This should be either the time it takes for `notice_trans` to finish, or slightly more than that.

```py
define notice_remove_interval = 10.0
```
`notice_removal_interval` is a **variable** which should be a **float**. It is the frequency at which the script tries to remove finished notices - should be lower number (more often) if you display notices often or many at once, and can be higher (less often) if not.

```py
define notice_log_add = False    # Prints whenever a new notice gets shown and what it is.
define notice_log_remove = False # Prints whenever an old notice gets marked* to be removed and what it is.
define notice_log_clear = False  # Prints a notification when the list is cleared of all notices.
```
Finally, there are three variables that each control a different **print** function. These messages are outputted to the console and the log.txt file. `notice_log_add` prints a message when a new notice is added and what it is. `notice_log_remove` prints a message whenever a notice (and which one) is ready to be removed. `notice_log_clear` prints a message when the list of notices becomes empty.

## Code
Second part contains all of the script's code, split into **Working stuff** where all the variables and functions are defined, and **Screen stuff**, where the `notice_screen` screen (which is responsible for displaying all Notices) is located.

The essential function of this script is `new_notice`:
```py
new_notice(message, image = False)
```
`message` is the thing to be displayed, either a string or a displayable. String, as already mentioned, is converted into a **Text** displayable based on the `notice_text` style.
If `image` is passed as **True**, `message` is expected to be something that can be *converted* to a displayable, following the [usual Ren'Py rules](https://www.renpy.org/doc/html/displayables.html#displayables) - a **string of a filename**, a **color**, an **image name** or a **list**.

There are few more names which shouldn't be overwritten: `notice_list`, `mark_old_notices` and `clear_notices`.

## Examples
Finally, here are the examples featured inside the script's `lezNotice_examples` label.

```py
new_notice("A plain notice!")
```
First example displays a simple text notice, formed according to the `notice_text` style.

```py
new_notice(Text("Text displayable notice!", color = "0f0", underline = True))
```
Second example also displays a text notice, however this one is passed directly as a Text displayable, allowing for styling different from the default. 

```py
new_notice("gui/window_icon.png", image = True)
```
Third example displays an image from a file. For this, `image` has to be passed as **True**.

```py
image example_image = Solid("f80", xysize = (200, 200))

new_notice("example_image", image = True)
```
Fourth example displays a defined image correlating to a passed image name. For this, `image` has to be passed as **True**.

```py
init python:
    def displayable_ex_func(st, at):
        t = round((st + 1) * 5, 3)
        return (Text(str(t)), 0.1)

a = DynamicDisplayable(displayable_ex_func)
new_notice(a)
```
Fifth and final example displays a more complex displayable, a counter which keeps on increasing and is displayed as text. Putting aside the definition, creating a notice showing it is just as simple as it is in all other examples.

# Final words and terms of use

This script is under the **MIT License**. This means you can use, modify and/or distribute this script, as long as I am credited ("Lezalith" is enough, but a link to my website with Ren'Py content, LezCave.com, is greatly appreciated!) and as long as the **LICENSE.txt** file stays included. Feel free to move it into its own folder, though.

Thank you very much for reading all the way here if you did. Now, go do great things!