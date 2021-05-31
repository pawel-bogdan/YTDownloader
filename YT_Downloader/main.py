import App
import static
"""
The app starts here.
"""
if __name__ == "__main__":
    root = App.Tk()
    root.minsize(static.MINIMAL_WIDTH_OF_FRAME, static.MINIMAL_HEIGHT_OF_FRAME)
    root.maxsize(static.MAXIMAL_WIDTH_OF_FRAME, static.MAXIMAL_HEIGHT_OF_FRAME)
    app = App.App(root)
    app.mainloop()
