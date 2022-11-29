from graphics import *
from button import Button


def main() -> None:
    '''3 door Graphical interface'''
    # Create window to hold graphical information
    app: GraphWin = GraphWin(title="Simple GUI Demo", width=800, height=450)
    app.setCoords(0, 0, 10, 10)

    # Draw tittle on the window
    title: Text = Text(p=Point(5, 9), text="Simple Gui")
    title.setFill("blue")
    title.setStyle("bold")
    title.setSize(18)

    title.draw(app)

    # Create some buttons on the window
    #   a close button to end the application
    quit_button: Button = Button(win=app, center=Point(5, 2), width=2, height=1, label="Quit")
    quit_button.activate()
    #   Three "doors" the user can "open"
    doors: list[Button] = [
        Button(win=app, center=(Point(2,5)), width=2, height=1, label="Door #1"),
        Button(win=app, center=(Point(5,5)), width=2, height=1, label="Door #2"),
        Button(win=app, center=(Point(8,5)), width=2, height=1, label="Door #3")
    ]
    for door in doors:
        door.activate()
    prizes: list[str] = [
        "New Car",
        "No Prize",
        "Vacation"
    ]
    # Handle user input
    while True:
        click_pos: Point = app.getMouse()
        if quit_button.clicked(click_pos):
            break
        else:
            for i, door in enumerate(doors):
                supriseMe(doors, i, click_pos, prizes)
            pass
        
def supriseMe(btns: list[Button], i: int, pos: Point, prizes: list[str]):

    if btns[i].clicked(pos):
        suprise: GraphWin = GraphWin(title="Surpise!")
        Text(p=Point(100,100), text=prizes[i]).draw(suprise)
        for button in btns:
            button.deactivate()

if __name__ == "__main__":
    main()
