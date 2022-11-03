__file__ = __file__.replace('\\', '/')

import json
from asyncio import new_event_loop, set_event_loop
from os import _exit
from os.path import expanduser, sep, split
from sys import argv
from threading import Thread
from time import time
from time import sleep

from pypresence import Presence
from PyQt5 import QtCore, QtGui, QtWidgets

home = str(expanduser('~'))
folder = split(__file__)[0]


class rich_presence_state:
    is_running = False
    presence = None
    application_id = None
    start_on = None
    args = None


def rich_presence(rpc_args):
    window.prepare_stylesheet_signal.emit(0)
    async_event_loop = new_event_loop()
    set_event_loop(async_event_loop)

    try:
        rich_presence_state.presence = Presence(
            int(rich_presence_state.application_id))
        rich_presence_state.presence.connect()

    except Exception as e:
        window.warning_signal.emit(str(e))
        return

    rich_presence_state.is_running = True
    rich_presence_state.presence.update(**rpc_args)

    window.default_stylesheet_signal.emit(0)
    window.update_default_stylesheet_signal.emit(0)

    rich_presence_state.args = rpc_args

    window.work_state_signal.emit(True)

    while rich_presence_state.is_running:
        old = rich_presence_state.args
        sleep(1)

        if rich_presence_state.args != old:
            rich_presence_state.presence.update(**rich_presence_state.args)
            window.update_default_stylesheet_signal.emit(0)


class ui_main_window(QtWidgets.QMainWindow):
    warning_signal = QtCore.pyqtSignal(str)
    work_state_signal = QtCore.pyqtSignal(bool)
    default_stylesheet_signal = QtCore.pyqtSignal(int)
    prepare_stylesheet_signal = QtCore.pyqtSignal(int)
    update_default_stylesheet_signal = QtCore.pyqtSignal(int)

    def initialize_ui(self, main_window: QtWidgets.QMainWindow):
        main_window.resize(275, 495)
        main_window.setMinimumSize(QtCore.QSize(275, 495))
        main_window.setMaximumSize(QtCore.QSize(275, 495))

        main_window.setStyleSheet(
            'QCheckBox::indicator:unchecked {\n'
            f'   border-image: url({folder}/assets/asset_checkbox_unchecked.png);\n'
            '}\n'
            'QCheckBox::indicator:checked {\n'
            f'    border-image: url({folder}/assets/asset_checkbox_checked.png);\n'
            '}')

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(f'{folder+sep}assets{sep}asset_app_icon.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

        main_window.setWindowIcon(icon)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.background = QtWidgets.QLabel(self.central_widget)
        self.background.setGeometry(QtCore.QRect(0, 0, 276, 496))
        self.background.setStyleSheet('background-color: rgb(64, 68, 75);')

        self.application_id = QtWidgets.QLineEdit(self.central_widget)

        self.application_id.setGeometry(QtCore.QRect(10, 10, 256, 26))
        self.application_id.setStyleSheet(
            'background-color: rgb(64, 68, 75);\n'
            'color: rgb(255, 255, 255);\n'
            'border-radius: 5;\n'
            'font: 87 10pt \'Segoe UI Black\';\n'
            'padding-left: 5;\n'
            'padding-right: 5')
        self.settings_background = QtWidgets.QLabel(self.central_widget)
        self.settings_background.setGeometry(QtCore.QRect(5, 5, 266, 446))
        self.settings_background.setStyleSheet(
            'background-color: rgb(52, 56, 61);\n'
            'border-radius: 5')
        self.line_1_text = QtWidgets.QLineEdit(self.central_widget)
        self.line_1_text.setGeometry(QtCore.QRect(15, 70, 121, 26))
        self.line_1_text.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                       'color: rgb(255, 255, 255);\n'
                                       'border-radius: 5;\n'
                                       'font: 87 10pt \'Segoe UI Black\';\n'
                                       'padding-left: 5;\n'
                                       'padding-right: 5')
        self.line_2_text = QtWidgets.QLineEdit(self.central_widget)
        self.line_2_text.setGeometry(QtCore.QRect(140, 70, 121, 26))
        self.line_2_text.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                       'color: rgb(255, 255, 255);\n'
                                       'border-radius: 5;\n'
                                       'font: 87 10pt \'Segoe UI Black\';\n'
                                       'padding-left: 5;\n'
                                       'padding-right: 5')
        self.background_group_lines = QtWidgets.QLabel(self.central_widget)
        self.background_group_lines.setGeometry(QtCore.QRect(10, 45, 256, 101))
        self.background_group_lines.setStyleSheet(
            'background-color: rgb(41, 43, 48);\n'
            'border-radius: 5')
        self.label_group_lines = QtWidgets.QLabel(self.central_widget)
        self.label_group_lines.setGeometry(QtCore.QRect(15, 50, 246, 16))
        self.label_group_lines.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\'')
        self.checkbox_enable_time_counter = QtWidgets.QCheckBox(
            self.central_widget)
        self.checkbox_enable_time_counter.setGeometry(
            QtCore.QRect(15, 415, 246, 26))
        self.checkbox_enable_time_counter.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkbox_enable_time_counter.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\';\n')
        self.background_group_button_1 = QtWidgets.QLabel(self.central_widget)
        self.background_group_button_1.setGeometry(
            QtCore.QRect(10, 155, 256, 56))
        self.background_group_button_1.setStyleSheet(
            'background-color: rgb(41, 43, 48);\n'
            'border-radius: 5')
        self.label_group_button_1 = QtWidgets.QLabel(self.central_widget)
        self.label_group_button_1.setGeometry(QtCore.QRect(15, 160, 71, 16))
        self.label_group_button_1.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\'')
        self.button_1_text = QtWidgets.QLineEdit(self.central_widget)
        self.button_1_text.setGeometry(QtCore.QRect(15, 180, 121, 26))
        self.button_1_text.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                         'color: rgb(255, 255, 255);\n'
                                         'border-radius: 5;\n'
                                         'font: 87 10pt \'Segoe UI Black\';\n'
                                         'padding-left: 5;\n'
                                         'padding-right: 5')
        self.button_1_link = QtWidgets.QLineEdit(self.central_widget)
        self.button_1_link.setGeometry(QtCore.QRect(140, 180, 121, 26))
        self.button_1_link.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                         'color: rgb(255, 255, 255);\n'
                                         'border-radius: 5;\n'
                                         'font: 87 10pt \'Segoe UI Black\';\n'
                                         'padding-left: 5;\n'
                                         'padding-right: 5')
        self.background_group_button_2 = QtWidgets.QLabel(self.central_widget)
        self.background_group_button_2.setGeometry(
            QtCore.QRect(10, 220, 256, 56))
        self.background_group_button_2.setStyleSheet(
            'background-color: rgb(41, 43, 48);\n'
            'border-radius: 5')
        self.label_group_button_2 = QtWidgets.QLabel(self.central_widget)
        self.label_group_button_2.setGeometry(QtCore.QRect(15, 225, 71, 16))
        self.label_group_button_2.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\'')
        self.button_2_text = QtWidgets.QLineEdit(self.central_widget)
        self.button_2_text.setGeometry(QtCore.QRect(15, 245, 121, 26))
        self.button_2_text.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                         'color: rgb(255, 255, 255);\n'
                                         'border-radius: 5;\n'
                                         'font: 87 10pt \'Segoe UI Black\';\n'
                                         'padding-left: 5;\n'
                                         'padding-right: 5')
        self.button_2_link = QtWidgets.QLineEdit(self.central_widget)
        self.button_2_link.setGeometry(QtCore.QRect(140, 245, 121, 26))
        self.button_2_link.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                         'color: rgb(255, 255, 255);\n'
                                         'border-radius: 5;\n'
                                         'font: 87 10pt \'Segoe UI Black\';\n'
                                         'padding-left: 5;\n'
                                         'padding-right: 5')
        self.checkbox_enable_button_1 = QtWidgets.QCheckBox(
            self.central_widget)
        self.checkbox_enable_button_1.setGeometry(
            QtCore.QRect(170, 160, 91, 16))
        self.checkbox_enable_button_1.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkbox_enable_button_1.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\';\n')
        self.checkbox_enable_button_2 = QtWidgets.QCheckBox(
            self.central_widget)
        self.checkbox_enable_button_2.setGeometry(
            QtCore.QRect(170, 225, 91, 16))
        self.checkbox_enable_button_2.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkbox_enable_button_2.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\';\n'
            '\n')
        self.checkbox_enable_line_1 = QtWidgets.QCheckBox(self.central_widget)
        self.checkbox_enable_line_1.setGeometry(QtCore.QRect(15, 100, 246, 21))
        self.checkbox_enable_line_1.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkbox_enable_line_1.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\';\n')
        self.checkbox_enable_line_2 = QtWidgets.QCheckBox(self.central_widget)
        self.checkbox_enable_line_2.setGeometry(QtCore.QRect(15, 120, 246, 21))
        self.checkbox_enable_line_2.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkbox_enable_line_2.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\';\n')
        self.background_group_button_big = QtWidgets.QLabel(
            self.central_widget)
        self.background_group_button_big.setGeometry(
            QtCore.QRect(10, 285, 256, 56))
        self.background_group_button_big.setStyleSheet(
            'background-color: rgb(41, 43, 48);\n'
            'border-radius: 5')
        self.label_group_icon_big = QtWidgets.QLabel(self.central_widget)
        self.label_group_icon_big.setGeometry(QtCore.QRect(15, 290, 116, 16))
        self.label_group_icon_big.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\'')
        self.checkbox_enable_big_icon = QtWidgets.QCheckBox(
            self.central_widget)
        self.checkbox_enable_big_icon.setGeometry(
            QtCore.QRect(170, 290, 91, 16))
        self.checkbox_enable_big_icon.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkbox_enable_big_icon.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\';\n')
        self.big_icon_key = QtWidgets.QLineEdit(self.central_widget)
        self.big_icon_key.setGeometry(QtCore.QRect(15, 310, 121, 26))
        self.big_icon_key.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                        'color: rgb(255, 255, 255);\n'
                                        'border-radius: 5;\n'
                                        'font: 87 10pt \'Segoe UI Black\';\n'
                                        'padding-left: 5;\n'
                                        'padding-right: 5')
        self.big_icon_text = QtWidgets.QLineEdit(self.central_widget)
        self.big_icon_text.setGeometry(QtCore.QRect(140, 310, 121, 26))
        self.big_icon_text.setStyleSheet('background-color: rgb(64, 68, 75);\n'
                                         'color: rgb(255, 255, 255);\n'
                                         'border-radius: 5;\n'
                                         'font: 87 10pt \'Segoe UI Black\';\n'
                                         'padding-left: 5;\n'
                                         'padding-right: 5')
        self.background_group_icon_small = QtWidgets.QLabel(
            self.central_widget)
        self.background_group_icon_small.setGeometry(
            QtCore.QRect(10, 350, 256, 56))
        self.background_group_icon_small.setStyleSheet(
            'background-color: rgb(41, 43, 48);\n'
            'border-radius: 5')
        self.label_group_icon_small = QtWidgets.QLabel(self.central_widget)
        self.label_group_icon_small.setGeometry(QtCore.QRect(15, 355, 131, 16))
        self.label_group_icon_small.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\'')
        self.checkbox_enable_small_icon = QtWidgets.QCheckBox(
            self.central_widget)
        self.checkbox_enable_small_icon.setGeometry(
            QtCore.QRect(170, 355, 91, 16))
        self.checkbox_enable_small_icon.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkbox_enable_small_icon.setStyleSheet(
            'color: white;\n'
            'font: 87 10pt \'Segoe UI Black\';\n')
        self.small_icon_key = QtWidgets.QLineEdit(self.central_widget)
        self.small_icon_key.setGeometry(QtCore.QRect(15, 375, 121, 26))
        self.small_icon_key.setStyleSheet(
            'background-color: rgb(64, 68, 75);\n'
            'color: rgb(255, 255, 255);\n'
            'border-radius: 5;\n'
            'font: 87 10pt \'Segoe UI Black\';\n'
            'padding-left: 5;\n'
            'padding-right: 5')
        self.small_icon_text = QtWidgets.QLineEdit(self.central_widget)
        self.small_icon_text.setGeometry(QtCore.QRect(140, 375, 121, 26))
        self.small_icon_text.setStyleSheet(
            'background-color: rgb(64, 68, 75);\n'
            'color: rgb(255, 255, 255);\n'
            'border-radius: 5;\n'
            'font: 87 10pt \'Segoe UI Black\';\n'
            'padding-left: 5;\n'
            'padding-right: 5')
        self.button_main = QtWidgets.QPushButton(self.central_widget)
        self.button_main.setGeometry(QtCore.QRect(164, 460, 101, 26))
        self.button_main.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_main.setStyleSheet('background-color: rgb(96, 102, 113);\n'
                                       'border-radius: 3;\n'
                                       'color: white;\n'
                                       'font: 87 10pt \'Segoe UI Black\';')

        self.button_save = QtWidgets.QPushButton(self.central_widget)
        self.button_save.setGeometry(QtCore.QRect(10, 460, 26, 26))
        self.button_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_save.setStyleSheet('background-color: rgb(96, 102, 113);\n'
                                       'border-radius: 3;\n')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f'{folder+sep}assets{sep}asset_save.png'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_save.setIcon(icon)
        self.button_update = QtWidgets.QPushButton(self.central_widget)
        self.button_update.setGeometry(QtCore.QRect(134, 460, 26, 26))
        self.button_update.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_update.setStyleSheet('background-color: rgb(74, 79, 88);\n'
                                         'border-radius: 3;\n')
        self.button_update.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(f'{folder+sep}assets{sep}asset_update.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_update.setIcon(icon)
        self.button_update.setIconSize(QtCore.QSize(17, 17))
        self.button_update.hide()
        self.button_open = QtWidgets.QPushButton(self.central_widget)
        self.button_open.setGeometry(QtCore.QRect(40, 460, 26, 26))
        self.button_open.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_open.setStyleSheet('background-color: rgb(96, 102, 113);\n'
                                       'border-radius: 3;\n')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f'{folder+sep}assets{sep}asset_open.png'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_open.setIcon(icon)
        self.button_save.setIconSize(QtCore.QSize(17, 17))

        # Raise
        self.background.raise_()
        self.settings_background.raise_()
        self.application_id.raise_()
        self.background_group_lines.raise_()
        self.line_1_text.raise_()
        self.line_2_text.raise_()
        self.label_group_lines.raise_()
        self.checkbox_enable_time_counter.raise_()
        self.background_group_button_1.raise_()
        self.label_group_button_1.raise_()
        self.button_1_text.raise_()
        self.button_1_link.raise_()
        self.background_group_button_2.raise_()
        self.label_group_button_2.raise_()
        self.button_2_text.raise_()
        self.button_2_link.raise_()
        self.checkbox_enable_button_1.raise_()
        self.checkbox_enable_button_2.raise_()
        self.checkbox_enable_line_1.raise_()
        self.checkbox_enable_line_2.raise_()
        self.background_group_button_big.raise_()
        self.label_group_icon_big.raise_()
        self.checkbox_enable_big_icon.raise_()
        self.big_icon_key.raise_()
        self.big_icon_text.raise_()
        self.background_group_icon_small.raise_()
        self.label_group_icon_small.raise_()
        self.checkbox_enable_small_icon.raise_()
        self.small_icon_key.raise_()
        self.small_icon_text.raise_()
        self.button_main.raise_()
        self.button_save.raise_()
        self.button_update.raise_()
        self.button_open.raise_()
        main_window.setCentralWidget(self.central_widget)

        # Set texts
        main_window.setWindowTitle('DiscordRPC')
        self.label_group_lines.setText('Линии')
        self.checkbox_enable_time_counter.setText('Включить счётчик времени')
        self.label_group_button_1.setText('Кнопка #1')
        self.label_group_button_2.setText('Кнопка #2')
        self.checkbox_enable_button_1.setText('Включить')
        self.checkbox_enable_button_2.setText('Включить')
        self.checkbox_enable_line_1.setText('Линия #1')
        self.checkbox_enable_line_2.setText('Линия #2')
        self.label_group_icon_big.setText('Большая иконка')
        self.checkbox_enable_big_icon.setText('Включить')
        self.label_group_icon_small.setText('Маленькая иконка')
        self.checkbox_enable_small_icon.setText('Включить')
        self.button_main.setText('Запустить')

        # Set placeholders
        self.application_id.setPlaceholderText('ID приложения')
        self.line_1_text.setPlaceholderText('Текст линии #1')
        self.line_2_text.setPlaceholderText('Текст линии #2')
        self.button_1_text.setPlaceholderText('Текст')
        self.button_1_link.setPlaceholderText('Ссылка')
        self.button_2_text.setPlaceholderText('Текст')
        self.button_2_link.setPlaceholderText('Ссылка')
        self.big_icon_key.setPlaceholderText('Ключ')
        self.big_icon_text.setPlaceholderText('Текст')
        self.small_icon_key.setPlaceholderText('Ключ')
        self.small_icon_text.setPlaceholderText('Текст')

        # On buttons click
        self.button_main.clicked.connect(self.run_in_exception_handler)
        self.button_save.clicked.connect(self.save_config)
        self.button_open.clicked.connect(self.open_config)
        self.button_update.clicked.connect(self.update_without_time)

        # On signals
        self.warning_signal.connect(self.throw_error)
        self.work_state_signal.connect(self.change_work_state)
        self.default_stylesheet_signal.connect(self.default_stylesheet)
        self.prepare_stylesheet_signal.connect(self.prepare_stylesheet)
        self.update_default_stylesheet_signal.connect(
            self.update_default_stylesheet)

        # On checkboxes edit
        self.checkbox_enable_line_1.stateChanged.connect(
            self.checkbox_enable_line_1_on_change)
        self.checkbox_enable_line_2.stateChanged.connect(
            self.checkbox_enable_line_2_on_change)
        self.checkbox_enable_button_1.stateChanged.connect(
            self.checkbox_enable_button_1_on_change)
        self.checkbox_enable_button_2.stateChanged.connect(
            self.checkbox_enable_button_2_on_change)
        self.checkbox_enable_big_icon.stateChanged.connect(
            self.checkbox_enable_big_icon_on_change)
        self.checkbox_enable_small_icon.stateChanged.connect(
            self.checkbox_enable_small_icon_on_change)
        self.checkbox_enable_time_counter.stateChanged.connect(
            self.checkbox_enable_time_counter_on_change)

        # Startup emulate "checkboxes edit"
        self.checkbox_enable_line_1_on_change()
        self.checkbox_enable_line_2_on_change()
        self.checkbox_enable_button_1_on_change()
        self.checkbox_enable_button_2_on_change()
        self.checkbox_enable_big_icon_on_change()
        self.checkbox_enable_small_icon_on_change()
        self.checkbox_enable_time_counter_on_change()

    def update_without_time(self):
        self.button_update.setStyleSheet('background-color: rgb(74, 79, 88);\n'
                                         'border-radius: 3;\n')

        self.button_update.setEnabled(False)

        rpc_args = {}
        rich_presence_state.application_id = self.application_id.text()

        if not self.application_id.text().isdigit():
            QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                          'ID приложения указано неверно')
            return

        if self.checkbox_enable_line_1.isChecked():
            rpc_args.update({'details': self.line_1_text.text()})

        if self.checkbox_enable_line_2.isChecked():
            rpc_args.update({'state': self.line_2_text.text()})

        if self.checkbox_enable_line_2.isChecked() and (
                not self.checkbox_enable_line_1.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить линию #2, если не включена линия #1')
            return

        if self.checkbox_enable_button_2.isChecked() and (
                not self.checkbox_enable_button_1.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить кнопку #2, если не включена кнопка #1')
            return

        if self.checkbox_enable_button_1.isChecked():
            link = self.button_1_link.text()
            if not (link.startswith('https://') or link.startswith('http://')):
                link = 'https://' + link

            if link == 'https://':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Ссылка кнопки #1 не может быть пустой')
                return

            if self.button_1_text.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Текст кнопки #1 не может быть пустым')
                return

            rpc_args.update({
                'buttons': [{
                    'label': self.button_1_text.text(),
                    'url': link
                }]
            })

        if self.checkbox_enable_button_2.isChecked():
            link = self.button_2_link.text()
            if not (link.startswith('https://') or link.startswith('http://')):
                link = 'https://' + link

            if link == 'https://':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Ссылка кнопки #2 не может быть пустой')
                return

            if self.button_2_text.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Текст кнопки #2 не может быть пустым')
                return

            rpc_args['buttons'].append({
                'label': self.button_2_text.text(),
                'url': link
            })

        if self.checkbox_enable_big_icon.isChecked():
            if self.big_icon_key.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка',
                    'Требуется ключ (Asset Key) большой иконки')
                return

            rpc_args['large_image'] = self.big_icon_key.text()

            if self.big_icon_text.text() != '':
                rpc_args['large_text'] = self.big_icon_text.text()

        if self.checkbox_enable_small_icon.isChecked() and (
                not self.checkbox_enable_big_icon.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить маленькую иконку, если не включена большая')
            return

        if self.checkbox_enable_small_icon.isChecked():
            if self.small_icon_key.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка',
                    'Требуется ключ (Asset Key) маленькой иконки')
                return

            rpc_args['small_image'] = self.small_icon_key.text()

            if self.big_icon_text.text() != '':
                rpc_args['small_text'] = self.small_icon_text.text()

        if self.checkbox_enable_time_counter.isChecked():
            rpc_args['start'] = rich_presence_state.start_on

        rich_presence_state.args = rpc_args

    def checkbox_enable_time_counter_on_change(self):
        if self.checkbox_enable_time_counter.isChecked():
            self.button_update.show()

        else:
            self.button_update.hide()

    def checkbox_enable_small_icon_on_change(self):
        state = self.checkbox_enable_small_icon.isChecked()
        self.small_icon_key.setDisabled(not state)
        self.small_icon_text.setDisabled(not state)

        if state:
            self.small_icon_key.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.small_icon_key.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.small_icon_key.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.small_icon_key.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        if state:
            self.small_icon_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.small_icon_text.setCursor(QtGui.QCursor(
                QtCore.Qt.IBeamCursor))

        else:
            self.small_icon_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.small_icon_text.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def checkbox_enable_big_icon_on_change(self):
        state = self.checkbox_enable_big_icon.isChecked()
        self.big_icon_key.setDisabled(not state)
        self.big_icon_text.setDisabled(not state)

        if state:
            self.big_icon_key.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.big_icon_key.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.big_icon_key.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.big_icon_key.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        if state:
            self.big_icon_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.big_icon_text.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.big_icon_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.big_icon_text.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def checkbox_enable_button_2_on_change(self):
        state = self.checkbox_enable_button_2.isChecked()
        self.button_2_text.setDisabled(not state)
        self.button_2_link.setDisabled(not state)

        if state:
            self.button_2_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_2_text.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.button_2_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_2_text.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        if state:
            self.button_2_link.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_2_link.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.button_2_link.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_2_link.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def checkbox_enable_button_1_on_change(self):
        state = self.checkbox_enable_button_1.isChecked()
        self.button_1_text.setDisabled(not state)
        self.button_1_link.setDisabled(not state)

        if state:
            self.button_1_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_1_text.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.button_1_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_1_text.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        if state:
            self.button_1_link.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_1_link.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.button_1_link.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.button_1_link.setCursor(
                QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

    def checkbox_enable_line_2_on_change(self):
        state = self.checkbox_enable_line_2.isChecked()
        self.line_2_text.setDisabled(not state)

        if state:
            self.line_2_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.line_2_text.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.line_2_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.line_2_text.setCursor(QtGui.QCursor(
                QtCore.Qt.ForbiddenCursor))

    def checkbox_enable_line_1_on_change(self):
        state = self.checkbox_enable_line_1.isChecked()
        self.line_1_text.setDisabled(not state)

        if state:
            self.line_1_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(255, 255, 255);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.line_1_text.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        else:
            self.line_1_text.setStyleSheet(
                'background-color: rgb(64, 68, 75);\n'
                'color: rgb(130, 130, 130);\n'
                'border-radius: 5;\n'
                'font: 87 10pt \'Segoe UI Black\';\n'
                'padding-left: 5;\n'
                'padding-right: 5')

            self.line_1_text.setCursor(QtGui.QCursor(
                QtCore.Qt.ForbiddenCursor))

    def change_work_state(self, state):
        if state:
            self.button_main.setText('Остановить')

        else:
            self.button_main.setText('Запустить')

    def throw_error(self, text):
        QtWidgets.QMessageBox.warning(self, 'Ошибка', text)

    def run_in_exception_handler(self):
        try:
            self.run()

        except Exception as e:
            print(f'Error: {e}')

    def save_config(self):
        rpc_args = {}
        rich_presence_state.application_id = self.application_id.text()

        if not self.application_id.text().isdigit():
            QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                          'ID приложения указано неверно')
            return

        if self.checkbox_enable_line_1.isChecked():
            rpc_args.update({
                'line_1_text':
                self.line_1_text.text()
                if self.line_1_text.text() != '' else None
            })
            rpc_args.update({
                'line_2_text':
                self.line_2_text.text()
                if self.line_2_text.text() != '' else None
            })

        else:
            rpc_args.update({'line_1_text': ''})
            rpc_args.update({'line_2_text': ''})

        if self.checkbox_enable_button_1.isChecked():
            rpc_args.update({
                'button_1_text': self.button_1_text.text(),
                'button_1_link': self.button_1_link.text()
            })

        else:
            rpc_args.update({'button_1_text': '', 'button_1_link': ''})

        if self.checkbox_enable_button_2.isChecked():
            rpc_args.update({
                'button_2_text': self.button_2_text.text(),
                'button_2_link': self.button_2_link.text()
            })

        else:
            rpc_args.update({'button_2_text': '', 'button_2_link': ''})

        if self.checkbox_enable_big_icon.isChecked():
            rpc_args.update({
                'big_icon_key': self.big_icon_key.text(),
                'big_icon_text': self.big_icon_text.text()
            })

        else:
            rpc_args.update({'big_icon_key': '', 'big_icon_text': ''})

        if self.checkbox_enable_small_icon.isChecked():
            rpc_args.update({
                'small_icon_key': self.small_icon_key.text(),
                'small_icon_text': self.small_icon_text.text()
            })

        else:
            rpc_args.update({'small_icon_key': '', 'small_icon_text': ''})

        rpc_args.update({
            'checkbox_enable_line_1':
            self.checkbox_enable_line_1.isChecked()
        })
        rpc_args.update({
            'checkbox_enable_line_2':
            self.checkbox_enable_line_2.isChecked()
        })
        rpc_args.update({
            'checkbox_enable_button_1':
            self.checkbox_enable_button_1.isChecked()
        })
        rpc_args.update({
            'checkbox_enable_button_2':
            self.checkbox_enable_button_2.isChecked()
        })
        rpc_args.update({
            'checkbox_enable_big_icon':
            self.checkbox_enable_big_icon.isChecked()
        })
        rpc_args.update({
            'checkbox_enable_small_icon':
            self.checkbox_enable_small_icon.isChecked()
        })
        rpc_args.update({
            'checkbox_enable_time_counter':
            self.checkbox_enable_time_counter.isChecked()
        })
        rpc_args.update({'application_id': self.application_id.text()})

        if not self.application_id.text().isdigit():
            QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                          'ID приложения указано неверно')
            return

        if self.checkbox_enable_line_2.isChecked() and (
                not self.checkbox_enable_line_1.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить линию #2, если не включена линия #1')
            return

        if self.checkbox_enable_button_1.isChecked():
            link = self.button_1_link.text()

            if self.checkbox_enable_button_2.isChecked() and (
                    not self.checkbox_enable_button_1.isChecked()):
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка',
                    'Нельзя включить кнопку #2, если не включена кнопка #1')
                return

            if link == 'https://':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Ссылка кнопки #1 не может быть пустой')
                return

            if self.button_1_text.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Текст кнопки #1 не может быть пустым')
                return

        if self.checkbox_enable_button_2.isChecked():
            link = self.button_2_link.text()

            if not (link.startswith('https://') or link.startswith('http://')):
                link = 'https://' + link

            if link == 'https://':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Ссылка кнопки #2 не может быть пустой')
                return

            if self.button_2_text.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Текст кнопки #2 не может быть пустым')
                return

        if self.checkbox_enable_big_icon.isChecked():
            if self.big_icon_key.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка',
                    'Требуется ключ (Asset Key) большой иконки')
                return

        if self.checkbox_enable_small_icon.isChecked() and (
                not self.checkbox_enable_big_icon.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить маленькую иконку, если не включена большая')
            return

        if self.checkbox_enable_small_icon.isChecked():
            if self.small_icon_key.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка',
                    'Требуется ключ (Asset Key) маленькой иконки')
                return

        path = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Сохранить конфигурацию DiscordRPC',
            home + sep + 'discordrpc.json', 'JSON файлы (*.json)')

        if path[0] == '':
            return

        path = path[0]

        file = open(path, 'w')

        json.dump(rpc_args, file, indent=4)

    def open_config(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Открыть конфигурацию DiscordRPC', home,
            'JSON файлы (*.json)')

        if path[0] == '':
            return

        try:
            path = path[0]

            file = open(path, 'r')
            config = json.load(file)

            self.line_1_text.setText(config['line_1_text'])
            self.line_2_text.setText(config['line_2_text'])
            self.button_1_text.setText(config['button_1_text'])
            self.button_1_link.setText(config['button_1_link'])
            self.button_2_text.setText(config['button_2_text'])
            self.button_2_link.setText(config['button_2_link'])
            self.big_icon_key.setText(config['big_icon_key'])
            self.big_icon_text.setText(config['big_icon_text'])

            self.checkbox_enable_line_1.setChecked(
                config['checkbox_enable_line_1'])
            self.checkbox_enable_line_2.setChecked(
                config['checkbox_enable_line_2'])
            self.checkbox_enable_button_1.setChecked(
                config['checkbox_enable_button_1'])
            self.checkbox_enable_button_2.setChecked(
                config['checkbox_enable_button_2'])
            self.checkbox_enable_big_icon.setChecked(
                config['checkbox_enable_big_icon'])
            self.checkbox_enable_small_icon.setChecked(
                config['checkbox_enable_small_icon'])
            self.checkbox_enable_time_counter.setChecked(
                config['checkbox_enable_time_counter'])

            self.application_id.setText(config['application_id'])

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', str(e))
            return

        self.checkbox_enable_line_1_on_change()
        self.checkbox_enable_line_2_on_change()
        self.checkbox_enable_button_1_on_change()
        self.checkbox_enable_button_2_on_change()
        self.checkbox_enable_big_icon_on_change()
        self.checkbox_enable_small_icon_on_change()

    def update_default_stylesheet(self):
        self.button_update.setStyleSheet(
            'background-color: rgb(96, 102, 113);\n'
            'border-radius: 3;\n')

        self.button_update.setEnabled(True)

    def default_stylesheet(self):
        self.button_main.setStyleSheet('background-color: rgb(96, 102, 113);\n'
                                       'border-radius: 3;\n'
                                       'color: white;\n'
                                       'font: 87 10pt \'Segoe UI Black\';')

        self.button_main.setEnabled(True)

    def prepare_stylesheet(self):
        self.button_main.setStyleSheet('background-color: rgb(74, 79, 88);\n'
                                       'border-radius: 3;\n'
                                       'color: white;\n'
                                       'font: 87 10pt \'Segoe UI Black\';')

        self.button_main.setEnabled(False)

    def run(self, update_time=True):
        if rich_presence_state.is_running:
            rich_presence_state.is_running = False
            rich_presence_state.presence.close()
            self.button_main.setText('Запустить')

            self.button_main.setStyleSheet(
                'background-color: rgb(96, 102, 113);\n'
                'border-radius: 3;\n'
                'color: white;\n'
                'font: 87 10pt \'Segoe UI Black\';')
            
            self.button_update.setStyleSheet('background-color: rgb(74, 79, 88);\n'
                                         'border-radius: 3;\n')
            self.button_update.setEnabled(False)

            return

        rpc_args = {}
        rich_presence_state.application_id = self.application_id.text()

        if not self.application_id.text().isdigit():
            QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                          'ID приложения указано неверно')
            return

        if self.checkbox_enable_line_1.isChecked():
            rpc_args.update({'details': self.line_1_text.text()})

        if self.checkbox_enable_line_2.isChecked():
            rpc_args.update({'state': self.line_2_text.text()})

        if self.checkbox_enable_line_2.isChecked() and (
                not self.checkbox_enable_line_1.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить линию #2, если не включена линия #1')
            return

        if self.checkbox_enable_button_2.isChecked() and (
                not self.checkbox_enable_button_1.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить кнопку #2, если не включена кнопка #1')
            return

        if self.checkbox_enable_button_1.isChecked():
            link = self.button_1_link.text()
            if not (link.startswith('https://') or link.startswith('http://')):
                link = 'https://' + link

            if link == 'https://':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Ссылка кнопки #1 не может быть пустой')
                return

            if self.button_1_text.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Текст кнопки #1 не может быть пустым')
                return

            rpc_args.update({
                'buttons': [{
                    'label': self.button_1_text.text(),
                    'url': link
                }]
            })

        if self.checkbox_enable_button_2.isChecked():
            link = self.button_2_link.text()
            if not (link.startswith('https://') or link.startswith('http://')):
                link = 'https://' + link

            if link == 'https://':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Ссылка кнопки #2 не может быть пустой')
                return

            if self.button_2_text.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка', 'Текст кнопки #2 не может быть пустым')
                return

            rpc_args['buttons'].append({
                'label': self.button_2_text.text(),
                'url': link
            })

        if self.checkbox_enable_big_icon.isChecked():
            if self.big_icon_key.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка',
                    'Требуется ключ (Asset Key) большой иконки')
                return

            rpc_args['large_image'] = self.big_icon_key.text()

            if self.big_icon_text.text() != '':
                rpc_args['large_text'] = self.big_icon_text.text()

        if self.checkbox_enable_small_icon.isChecked() and (
                not self.checkbox_enable_big_icon.isChecked()):
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка',
                'Нельзя включить маленькую иконку, если не включена большая')
            return

        if self.checkbox_enable_small_icon.isChecked():
            if self.small_icon_key.text() == '':
                QtWidgets.QMessageBox.warning(
                    self, 'Ошибка',
                    'Требуется ключ (Asset Key) маленькой иконки')
                return

            rpc_args['small_image'] = self.small_icon_key.text()

            if self.big_icon_text.text() != '':
                rpc_args['small_text'] = self.small_icon_text.text()

        if self.checkbox_enable_time_counter.isChecked():
            if update_time:
                rich_presence_state.start_on = round(time())

            rpc_args['start'] = rich_presence_state.start_on

        if update_time:
            Thread(target=lambda: rich_presence(rpc_args)).start()

        else:
            rich_presence_state.args = rpc_args


class main_window(ui_main_window):

    def __init__(self):
        super().__init__()
        self.initialize_ui(self)

    def closeEvent(self, *args):
        rich_presence_state.is_running = False

        try:
            rich_presence_state.presence.close()

        except:
            pass

        _exit(0)


application = QtWidgets.QApplication(argv)
window = main_window()
window.show()
_exit(application.exec_())