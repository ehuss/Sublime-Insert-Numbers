import sublime, sublime_plugin

class InsertNumbersCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        s = self.view.sel()
        default = '1'
        # if len(s) > 1:
        #     default = '1 %i' % (len(s),)
        self.view.window().show_input_panel('Enter Start [Stop [Step]]', default, self.on_done, None, None)

    def on_done(self, text):
        parts = text.split(' ')
        stop = None
        step = 1
        try:
            start = int(parts[0])
            if len(parts) > 1:
                stop = int(parts[1])
                if len(parts) > 2:
                    step = int(parts[2])
        except ValueError:
            sublime.error_message('Values must be numbers.')
            return

        edit = self.view.begin_edit()
        try:
            if stop == None:
                stop = len(self.view.sel())
                for i, r in enumerate(self.view.sel()):
                    self.view.insert(edit, r.begin(), str(i+1))
            else:
                text = '\n'.join(map(str, range(start, stop+1, step)))
                for r in self.view.sel():
                    self.view.insert(edit, r.begin(), text)

        finally:
            self.view.end_edit(edit)
