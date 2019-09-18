from Tkinter import *

canvasWidth = 800
canvasHeight = 800
frameWidth = 800
frameHeight = 800

backgroundColour = "#DDEEFF"
scoreBoxColour = "#FFFFFF"

main = Tk()

frame1 = Frame(
    master = main,
    width=frameWidth,
    height = frameHeight
)
frame1.grid(row=0, column=0)

canvas = Canvas(
    master = frame1,
    width = canvasWidth,
    height = canvasHeight,
    background = backgroundColour
)

scoreBox = canvas.create_rectangle(
    [2, canvasWidth/2+1, canvasWidth+1, canvasHeight+1],
    fill=scoreBoxColour
)



canvas.pack()
main.mainloop()
