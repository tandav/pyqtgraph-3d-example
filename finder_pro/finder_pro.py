from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import signal
from functools import partial
import webbrowser
import shutil

home = '/Users/tandav'

safari_shortcuts = {
    'big-pic'   : home + '/Documents/108/meta/map/big-pic.svg',
    'shortcuts' : home + '/Documents/108/meta/map/shortcuts.svg',
    'study-plan': home + '/Documents/108/meta/map/study-plan.html',
    # 'github'    : 'https://github.com/tandav?tab=repositories',
    # 'gist'      : 'https://gist.github.com/tandav',
    # 'wm'        : 'https://www.youtube.com/playlist?list=PL4qBE1-4ZNC0Wam6r8MaZoUfZ8ektEVYe',
    # 'YT'        : 'https://www.youtube.com',
    # 'HN'        : 'https://news.ycombinator.com',
    # 'TW'        : 'https://twitter.com',
    # 'WF'        : 'https://workflowy.com',
}



path_shortcuts = {
    '108'         : home + '/Documents/108',
    # 'knowledge'   : home + '/Documents/108/knowledge',
    '~'           : home,
    'Desktop'     : home + '/Desktop',
    'Downloads'   : home + '/Downloads',
    'Documents'   : home + '/Documents',
    # 'GoogleDrive' : home + '/GoogleDrive',
    'dotfiles'    : home + '/Documents/108/dotfiles',
    # 'Notes'       : home + '/GoogleDrive/Notes',

}

projects_shortcuts = {
    # 'steth'       : home + '/Documents/ultrasonic-stethoscope',
    # 'spectrogram' : home + '/Documents/108/bhairava/spectrogram',
    'dashboard'   : home + '/Documents/108/spaces/brain-tools/brain-tools/finder-pro/dashboard'
}

editor = '/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl'


class AppGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.filesystem = QFileSystemModel()
        self.filesystem.setRootPath('/')

        self.cwd = sys.argv[1] if len(sys.argv) > 1 else '/Users/tandav/Documents'
        
        self.readme_exists = None

        self.init_ui()
        self.qt_connections()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.add_dir_up_down()

        self.add_tree()

        self.add_action_buttons()
        self.add_here_action_buttons()




        self.add_safari_shortcuts()

        self.add_path_shortcuts()
        self.add_projects_shortcuts()
        self.add_shortcuts_buttons()



        self.setLayout(self.layout)
        self.setGeometry(0, 0, 1000, 800)


        self.show()

    def add_dir_up_down(self):
        self.dir_up_down_layout = QHBoxLayout()
        self.button_directory_up = QPushButton('⬆')
        self.button_directory_down = QPushButton('⬇︎')
        self.dir_up_down_layout.addWidget(self.button_directory_up)
        self.dir_up_down_layout.addWidget(self.button_directory_down)    
        self.button_directory_up.clicked.connect(self.directory_up)
        self.button_directory_down.clicked.connect(self.directory_down)
        self.layout.addLayout(self.dir_up_down_layout)    

    def add_tree(self):
        self.tree = QTreeView()
        self.tree.setModel(self.filesystem)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(2, Qt.AscendingOrder)

        self.tree.setColumnWidth(0, 600)
        # self.tree.setWindowTitle("Dir View")
        # self.tree.resize(640, 480)
        # self.tree.setRootIndex(self.filesystem.rootPath())
        # self.tree.setRootIndex(self.filesystem.index(self.filesystem.rootPath()))
        self.tree.setRootIndex(self.filesystem.index(self.cwd))
        self.setWindowTitle(self.cwd)


        self.tree.clicked.connect(self.dummy)
        # self.tree.clicked.connect(self.quicklook)

        self.layout.addWidget(self.tree)

    def dummy(self):
        print(self.filesystem.filePath(self.tree.currentIndex()))


    def add_action_buttons(self):
        self.actions_buttons_layout = QHBoxLayout()

        self.button_quicklook = QPushButton('Quick Look')
        self.button_open = QPushButton('Open')
        self.button_reveal_in_finder = QPushButton('Reveal in Finder')
        self.button_open_in_terminal = QPushButton('Open in Terminal')
        self.button_open_in_sublime = QPushButton('Open in Sublime')
        self.button_symlink = QPushButton('Symlink')
        self.button_copy_path = QPushButton('Copy Path')

        
        self.actions_buttons_layout.addWidget(self.button_quicklook)
        self.actions_buttons_layout.addWidget(self.button_open)
        self.actions_buttons_layout.addWidget(self.button_reveal_in_finder)
        self.actions_buttons_layout.addWidget(self.button_open_in_terminal)
        self.actions_buttons_layout.addWidget(self.button_open_in_sublime)
        self.actions_buttons_layout.addWidget(self.button_symlink)
        self.actions_buttons_layout.addWidget(self.button_copy_path)

        self.button_quicklook.clicked.connect(self.quicklook)
        self.button_open.clicked.connect(self.open)
        self.button_reveal_in_finder.clicked.connect(self.reveal_in_finder)
        self.button_open_in_terminal.clicked.connect(self.open_in_terminal)
        self.button_open_in_sublime.clicked.connect(self.open_in_sublime)
        self.button_symlink.clicked.connect(self.create_symlink)
        self.button_copy_path.clicked.connect(self.copy_path)

        self.layout.addLayout(self.actions_buttons_layout)

    def add_here_action_buttons(self):
        self.here_action_buttons_layout  = QHBoxLayout()

        self.button_finder_here   = QPushButton('Finder Here')
        self.button_terminal_here = QPushButton('Terminal Here')
        self.button_sublime_here  = QPushButton('Sublime Here')
        self.button_disk_inventory_here  = QPushButton('DiskInv Here')
        self.button_readme = QPushButton('README')
        self.handle_readme_dir()

        self.here_action_buttons_layout.addWidget(self.button_finder_here)
        self.here_action_buttons_layout.addWidget(self.button_terminal_here)
        self.here_action_buttons_layout.addWidget(self.button_sublime_here)
        self.here_action_buttons_layout.addWidget(self.button_disk_inventory_here)
        self.here_action_buttons_layout.addWidget(self.button_readme)


        self.button_finder_here.clicked.connect(self.finder_here)
        self.button_terminal_here.clicked.connect(self.terminal_here)
        self.button_sublime_here.clicked.connect(self.sublime_here)
        self.button_disk_inventory_here.clicked.connect(self.disk_inventory_here)
        self.button_readme.clicked.connect(self.readme_click)
        

        self.layout.addLayout(self.here_action_buttons_layout)

    def finder_here(self):
        os.system(f'open -a Finder "{self.cwd}"')

    def terminal_here(self):
        os.system(f'open -a Terminal "{self.cwd}"')

    def sublime_here(self):
        os.system(f'{editor} "{self.cwd}"')

    def disk_inventory_here(self):
        os.system(f'open -a Disk\ Inventory\ X "{self.cwd}"')

    def add_shortcuts_buttons(self):
        self.shortcuts_buttons_layout = QHBoxLayout()
        
        self.button_telegram = QPushButton('Telegram')
        self.button_mtop = QPushButton('mtop')
        self.button_system_preferences = QPushButton('Night Shift')
        
        self.shortcuts_buttons_layout.addWidget(self.button_telegram)
        self.shortcuts_buttons_layout.addWidget(self.button_mtop)
        self.shortcuts_buttons_layout.addWidget(self.button_system_preferences)

        self.button_telegram.clicked.connect(self.open_telegram)
        self.button_mtop.clicked.connect(self.open_mtop)
        self.button_system_preferences.clicked.connect(self.open_system_preferences)

        self.layout.addLayout(self.shortcuts_buttons_layout)

    def open_telegram(self):
        os.system(f'open -a Telegram')

    def open_mtop(self):
        os.system(f'open -a Activity\ Monitor')

    def open_system_preferences(self):
        os.system(f'open -a System\ Preferences')
        # os.system('bash /Users/tandav/Documents/108/spaces/brain-tools/brain-tools/finder-pro/dashboard/scripts/night-shift.sh')
        # os.system(f'open /System/Library/PreferencePanes/Displays.prefPane')
        # os.system('osascript -e "tell application \"System Preferences\"" -e "set the current pane to pane id \"com.apple.preference.displays\"" -e "reveal anchor \"displaysNightShiftTab\" of pane id \"com.apple.preference.displays\"" -e "activate"  -e "end tell"')
        # os.system('''open -a Telegram''')
                   # osascript -e "tell application \"System Preferences\"" -e "set the current pane to pane id \"com.apple.preference.displays\"" -e "reveal anchor \"displaysNightShiftTab\" of pane id \"com.apple.preference.displays\"" -e "activate"  -e "end tell"
                   # norm in terminal, fix it 
    def add_safari_shortcuts(self):
        self.safari_shortcuts_layout = QHBoxLayout()
        for name, url in safari_shortcuts.items():
            button_shortcut = QPushButton(name)
            self.safari_shortcuts_layout.addWidget(button_shortcut)
            button_shortcut.clicked.connect(partial(self.open_safari_shortcut, url))
        self.layout.addLayout(self.safari_shortcuts_layout)

    def add_path_shortcuts(self):
        self.path_shortcuts_layout = QHBoxLayout()
        for name, url in path_shortcuts.items():
            button_shortcut = QPushButton(name)
            self.path_shortcuts_layout.addWidget(button_shortcut)
            button_shortcut.clicked.connect(partial(self.change_tree_path, url))
        self.layout.addLayout(self.path_shortcuts_layout)

    def add_projects_shortcuts(self):
        self.projects_shortcuts_layout = QHBoxLayout()
        for name, url in projects_shortcuts.items():
            button_shortcut = QPushButton(name)
            self.projects_shortcuts_layout.addWidget(button_shortcut)
            button_shortcut.clicked.connect(partial(self.change_tree_path, url))
        self.layout.addLayout(self.projects_shortcuts_layout)


    def open_safari_shortcut(self, url):
        os.system(f'open -a Safari {url}')

    def change_tree_path(self, url):
        self.tree.setRootIndex(self.filesystem.index(url))
        self.cwd = url
        self.setWindowTitle(self.cwd)
        self.handle_readme_dir()



    def qt_connections(self):
        pass




    def selected_item_path(self):
        return self.filesystem.filePath(self.tree.currentIndex())

    def directory_up(self):
        self.change_tree_path(
            self.filesystem.filePath(
                self.filesystem.parent(
                    self.tree.rootIndex()
                )
            )
        )
        # self.tree.setRootIndex(self.filesystem.parent(self.tree.rootIndex()))
        # self.setWindowTitle(self.filesystem.filePath(self.tree.rootIndex()))

    def directory_down(self):
        self.change_tree_path(
            self.filesystem.filePath(
                self.tree.currentIndex()
            )
        )

        # self.tree.setRootIndex(self.tree.currentIndex())
        # self.setWindowTitle(self.filesystem.filePath(self.tree.rootIndex()))

    def quicklook(self):
        os.system(f'qlmanage -p "{self.selected_item_path()}" &> /dev/null')

    def open(self):
        os.system(f'open "{self.selected_item_path()}"')

    def reveal_in_finder(self):
        os.system(f'open -R "{self.selected_item_path()}"')

    def open_in_terminal(self):
        os.system(f'open -a Terminal "{self.selected_item_path()}"')

    def open_in_sublime(self):
        os.system(f'{editor} "{self.selected_item_path()}"')

    def create_symlink(self):
        os.symlink(self.selected_item_path(), os.path.splitext(self.selected_item_path())[0] + '-symlink')

    def copy_path(self):
        os.system(f'echo "{self.selected_item_path()}" | pbcopy')

    def handle_readme_dir(self):
        if os.path.isfile(f'{self.cwd}/README/README.html'):
            self.readme_exists = True
            print(f'README exists: {self.readme_exists}')
            self.button_readme.setStyleSheet('color: green')
        else:
            self.readme_exists = False
            print(f'README exists: {self.readme_exists}')
            self.button_readme.setStyleSheet('color: grey')

    def readme_click(self):

        path = f'{self.cwd}/README/README.html'
        if self.readme_exists:
            webbrowser.open(f'file://{self.cwd}/README/README.html')
            os.system(f'{editor} "{self.cwd}/README"')
            os.system(f'{editor} --add "{self.cwd}/README/README.html"')
        else:
            if not os.path.isdir(f'{self.cwd}/README'):
                os.mkdir(f'{self.cwd}/README')
                shutil.copy('/Users/tandav/Documents/108/dotfiles/README/README.html', f'{self.cwd}/README/README.html')
        self.handle_readme_dir()
                # print('Fake Creating README...')




app = QApplication(sys.argv)
# print(sys.argv[1])
gui = AppGUI()
signal.signal(signal.SIGINT, signal.SIG_DFL)
sys.exit(app.exec())
