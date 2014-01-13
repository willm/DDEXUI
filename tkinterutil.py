import tkinter.ttk as tk
import tkinter.messagebox as mb

#thanks to http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#and http://stackoverflow.com/questions/6666882/tkinter-python-catching-exceptions
def showerrorbox(func):
    def run(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
            mb.showerror("Error", e)
            raise e
    return run
