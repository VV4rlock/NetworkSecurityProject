
class WindowsManager:
    def __init__(self):
        self.windows={}

    def add(self,name,window):
        self.windows[name]=window

    def get_window(self,name):
        if name in self.windows:
            return self.windows[name]
        else:
            return None

    def get_keys(self):
        return list(self.windows.keys())

