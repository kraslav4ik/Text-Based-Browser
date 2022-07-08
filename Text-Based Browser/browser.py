import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore


class TextBrowser:
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.history_stack = deque()

    def check_path(self):
        if not os.access(self.dir_name, os.F_OK):
            os.mkdir(os.path.join(os.getcwd(), self.dir_name))

    def check_input(self):
        while True:
            user_input = input()
            if user_input == 'exit':
                break
            if user_input == 'back':
                self.back_button()
                continue
            if user_input in os.listdir(os.getcwd()):
                self.reading_file(user_input)
                continue
            self.site_parsing(user_input)

    def reading_file(self, user_input):
        with open(f'.\\{self.dir_name}\\{user_input}') as fle:
            for line in fle:
                print(line)
            self.history_stack.append(fle)

    def site_parsing(self, user_input):
        try:
            if not user_input.startswith('https://'):
                user_input = f'https://{user_input}'
            site = requests.get(user_input)
            soup = BeautifulSoup(site.content, 'html.parser')
            for i in soup.find_all("a"):
                i.string = "".join([Fore.BLUE, i.get_text(), Fore.RESET])
            site_text = soup.get_text()
            file_name = user_input[user_input.rfind("/"):user_input.rfind(".")]
            with open(f'.\\{self.dir_name}\\{file_name}', 'w') as fle:
                fle.write(site_text)
            self.history_stack.append(site_text)
            print(site_text)
        except requests.exceptions.ConnectionError:
            print('Incorrect URL')

    def back_button(self):
        if not self.history_stack:
            return
        self.history_stack.pop()
        print(self.history_stack.pop())


if __name__ == "__main__":
    my_browser = TextBrowser(sys.argv[1])
    my_browser.check_path()
    my_browser.check_input()
