from htmlbuilder import builder, css

body_style = css(width="100%", height="100%")


@builder
def page_index(tag, stag, text):
    with tag.html():
        with tag.head():
            pass
        with tag.body(style=body_style):
            with tag.h1(style=css(color="red")):
                text("Hello World")


with open("example-simple.html", "w") as f:
    f.write(page_index())
