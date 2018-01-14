import sublime
import sublime_plugin


last_input = '1 '


class InsertNumbersCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # s = self.view.sel()
        # if len(s) > 1:
        #     default = '1 %i' % (len(s),)
        self.view.window().show_input_panel(
            'Enter Start [Stop [Step]]', last_input, self.on_done, None, None)

    def on_done(self, text):
        global last_input
        last_input = text
        self.view.run_command('insert_numbers_act', {'text': text})


class InsertNumbersAct(sublime_plugin.TextCommand):

    def run(self, edit, text=''):
        parts = text.strip().split(' ')
        stop = None
        step = 1
        try:
            start = int(parts[0])
            width = len(parts[0])
            if len(parts) > 1:
                stop = int(parts[1])
                width = min(len(parts[1]), len(parts[0]))
                if len(parts) > 2:
                    step = int(parts[2])
        except ValueError:
            sublime.error_message('Values must be numbers.')
            return

        def pad_i(i):
            return '%0*i' % (width, i)

        if stop is None:
            i = start
            for r in self.view.sel():
                self.view.insert(edit, r.begin(), pad_i(i))
                i += step
        else:
            text = '\n'.join(map(pad_i, range(start, stop + 1, step)))
            for r in self.view.sel():
                self.view.insert(edit, r.begin(), text)
