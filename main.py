#!/usr/bin/env python3

import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                             QVBoxLayout, QLineEdit, QLabel, QScrollArea,
                             QDialog, QFormLayout, QDialogButtonBox, QMenu, QMessageBox)
from PyQt6.QtCore import Qt, QPoint


class CharacterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.dirname(os.path.abspath(__file__));
        self.file_path = os.path.join(self.base_dir, 'chara.json');

        self.all_chars = self.load_data()
        self.buttons = []
        self.init_ui()

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.all_chars, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar: {e}")

    def init_ui(self):
        self.setWindowTitle(" Char Helper ")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(340, 500)

        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; }
            QLineEdit { 
                background-color: #3c3f41; color: white; 
                border: 1px solid #5e81ac; border-radius: 5px; 
                padding: 8px; font-size: 14px; margin-bottom: 5px;
            }
            QPushButton { 
                background-color: #3c3f41; color: #ffffff; 
                border-radius: 8px; font-size: 20px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5e81ac; }
            QLabel { color: #888888; }
        """)

        self.main_layout = QVBoxLayout()


        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar símbolo... ej: arroba")
        self.search_bar.textChanged.connect(self.filter_chars)
        self.main_layout.addWidget(self.search_bar)

        self.info_label = QLabel("Hecho por Jumacode")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.info_label)

        self.link_label = QLabel(
            '<a href="https://github.com/Yormenxx" style="color: #5e81ac; text-decoration: none;">GitHub</a>')
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.link_label)

        self.info_label = QLabel("Click Izquierdo: Copiar | Click Derecho: Eliminar")
        self.info_label.setStyleSheet("font-size: 10px; color: #666666;")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.info_label)


        self.add_btn = QPushButton("+ Añadir Carácter")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32; color: white; 
                font-size: 13px; padding: 12px; margin: 5px 0px;
            }
            QPushButton:hover { background-color: #388e3c; }
        """)
        self.add_btn.clicked.connect(self.add_new_character)
        self.main_layout.addWidget(self.add_btn)


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid = QGridLayout(self.scroll_content)
        self.grid.setSpacing(10)
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)

        self.render_buttons(self.all_chars)
        self.setLayout(self.main_layout)

    def render_buttons(self, char_list):
        for btn in self.buttons:
            self.grid.removeWidget(btn)
            btn.deleteLater()
        self.buttons.clear()

        for i, item in enumerate(char_list):
            btn = QPushButton(item['char'])
            btn.setFixedSize(80, 65)
            btn.setToolTip(item['name'])


            btn.clicked.connect(lambda checked, c=item['char']: self.copy_to_clipboard(c))


            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, it=item: self.show_context_menu(pos, it))

            self.grid.addWidget(btn, i // 3, i % 3)
            self.buttons.append(btn)

    def show_context_menu(self, pos, item):

        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #3c3f41; color: white; border: 1px solid #555; }")

        delete_action = menu.addAction(f"Eliminar '{item['char']}'")


        action = menu.exec(self.sender().mapToGlobal(pos))

        if action == delete_action:
            self.confirm_deletion(item)

    def confirm_deletion(self, item):

        confirm = QMessageBox.question(
            self, 'Confirmar', f"¿Seguro que quieres eliminar el símbolo '{item['char']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:

            self.all_chars = [c for c in self.all_chars if c != item]

            self.save_data()

            self.render_buttons(self.all_chars)

    def filter_chars(self, text):
        query = text.lower()
        filtered = [c for c in self.all_chars if query in c['name'].lower() or query in c['char'].lower()]
        self.render_buttons(filtered)

    def copy_to_clipboard(self, char):
        QApplication.clipboard().setText(char)

    def add_new_character(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Carácter")
        dialog.setFixedSize(250, 150)

        layout = QFormLayout(dialog)
        char_in = QLineEdit()
        name_in = QLineEdit()

        layout.addRow("Símbolo:", char_in)
        layout.addRow("Nombre:", name_in)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        layout.addRow(btns)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            c, n = char_in.text(), name_in.text()
            if c and n:
                self.all_chars.append({"char": c, "name": n})
                self.save_data()
                self.render_buttons(self.all_chars)
                self.search_bar.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CharacterApp()
    window.show()
    sys.exit(app.exec())