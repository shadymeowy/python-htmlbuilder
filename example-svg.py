from htmlbuilder import builder, css

style_body = css(
    width="100%",
    height="100%"
)

palette = {
    -1: "grey",
    0: "white",
    1: "lime",
    2: "aqua",
    3: "red",
    4: "yellow",
    5: "purple",
    6: "blue",
}


@builder
def draw_layout(tag, stag, text, arr, scale=35):
    h = len(arr)
    w = len(arr[0])
    with tag.html():
        with tag.head():
            pass
        with tag.body(style=style_body):
            with tag.svg(width=w * scale, height=h * scale):
                for y in range(h):
                    for x in range(w):
                        stag.rect(
                            x=x * scale,
                            y=y * scale,
                            width=scale,
                            height=scale,
                            style=css(stroke="black", fill=palette[arr[y][x]])
                        )


arr = [
    [1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 1],
    [3, 4, 5, 6, 1, 2],
    [4, 5, 6, 1, 2, 3],
    [5, 6, 1, 2, 3, 4],
    [6, 1, 2, 3, 4, 5]
]

with open("example-svg.html", "w") as f:
    f.write(draw_layout(arr))
