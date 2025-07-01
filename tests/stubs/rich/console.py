class Console:
    def print(self, *args, **kwargs):
        print(*args)

    def input(self, prompt=''):
        return input(prompt)
