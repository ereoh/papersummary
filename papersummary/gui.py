# pylint: disable=no-name-in-module,too-many-instance-attributes,too-many-statements,broad-exception-caught
"""Launches papersummry GUI"""

import sys
from pathlib import Path
import pyperclip
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QFileDialog,
    QFrame,
    QCheckBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor, QFontDatabase

from papersummary.main import run, SUPPORTED_FILETYPES
from papersummary.utils import DEFAULT_PROMPT


THIS_DIR = Path(__file__).parent
TITLE_FONT_PATH = THIS_DIR / 'fonts' / 'Jua-Regular.ttf'

# PySide application class
class PaperSummaryApp(QMainWindow):
    """papersummary GUI Window"""

    def __init__(self):
        """Initializes GUI Window"""
        super().__init__()
        self.filepath = ""
        self.output_to_copy = ""
        self.setWindowTitle("papersummary")
        self.setMinimumSize(700, 1000)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self._init_ui()

    def _init_ui(self) -> None:
        """
        Initializes the user interface.
        """
        # 1. Title Label
        title_label = QLabel("papersummary")
        title_font = QFont("Arial", 20, QFont.Bold)
        font_id = QFontDatabase.addApplicationFont(str(TITLE_FONT_PATH))
        if font_id != -1:
            font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
            title_font = QFont(font_name, 16)
        else:
            print("Failed to load font. Using Arial as a fallback.")

        title_font.setUnderline(True)
            
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)

        # 2. File Browsing Section (QHBoxLayout)
        file_browse_layout = QHBoxLayout()

        browse_button = QPushButton("Browse for File")
        browse_button.setFont(QFont("Arial", 10, QFont.Bold))
        browse_button.clicked.connect(self.browse_file)
        file_browse_layout.addWidget(browse_button)

        self.file_path_label = QLabel("No file selected.")
        self.file_path_label.setWordWrap(True)
        self.file_path_label.setStyleSheet("padding: 5px;")
        self.file_path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        file_browse_layout.addWidget(self.file_path_label)

        self.main_layout.addLayout(file_browse_layout)

        # 3. Prompt Text Area
        prompt_label = QLabel("Custom Prompt (optional):")
        prompt_label.setFont(QFont("Arial", 10))
        self.main_layout.addWidget(prompt_label)

        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText("Enter your custom summary request here...")
        self.prompt_text.setFixedHeight(80)
        self.prompt_text.setText(DEFAULT_PROMPT)
        self.main_layout.addWidget(self.prompt_text)

        # 4. Options
        options_layout = QHBoxLayout()
        self.clipboard_checkbox = QCheckBox("Copy to Clipboard")
        self.clipboard_checkbox.setChecked(True)
        options_layout.addWidget(self.clipboard_checkbox)
        options_layout.addStretch(1)  # Push checkbox to the left
        self.main_layout.addLayout(options_layout)

        # Separator Line (QFrame)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(separator)

        # 5. Generate Button
        self.generate_button = QPushButton("Generate Summary")
        self.generate_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.generate_button.setStyleSheet(
            "QPushButton { background-color: #0078D4; color: white; padding: 10px; border-radius: 5px; }"
            "QPushButton:hover { background-color: #005A9E; }"
            "QPushButton:pressed { background-color: #003C8F; }"
        )
        self.generate_button.clicked.connect(self.start_generation)
        self.main_layout.addWidget(self.generate_button)

        # 6. Status and Output Label
        self.generate_label = QLabel("No summary generated yet. Select a file and click 'Generate Summary'.")
        self.generate_label.setWordWrap(True)
        glf = QFont("Arial", 10)
        glf.setItalic(True)
        self.generate_label.setFont(glf)
        self.generate_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.generate_label)

        # 7. Copy Output Button
        self.copy_button = QPushButton("Copy Last Output to Clipboard")
        self.copy_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        self.copy_button.clicked.connect(self.copy_output)
        self.main_layout.addWidget(self.copy_button)

        # Add stretch to push content to the top
        self.main_layout.addStretch(1)

        # 8. Footer (at the bottom of the window, outside main_layout stretch)
        self._init_footer()

    def _init_footer(self) -> None:
        """
        Initializes the footer of the GUI window.
        """
        # Footer is typically added to the main window's status bar or as a separate section
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(10, 5, 10, 5)

        # Author Label
        author_label = QLabel("Created by Ere Oh")
        alf = QFont("Helvetica", 9)
        alf.setItalic(True)
        author_label.setFont(alf)
        author_label.setStyleSheet("color: grey;")
        footer_layout.addWidget(author_label)

        # Github Link Label
        link_label = QLabel('<a href="https://github.com/ereoh/papersummary">GitHub Repository</a>')
        link_label.setOpenExternalLinks(True)  # PySide handles this automatically for <a> tags
        link_label.setStyleSheet("color: blue; text-decoration: underline;")
        link_label.setCursor(QCursor(Qt.PointingHandCursor))
        footer_layout.addWidget(link_label)

        # Add the footer layout to the main window's central widget layout
        self.main_layout.addWidget(footer_widget)

    def browse_file(self) -> None:
        """Opens a file dialog to select a file."""
        wildcard_extensions = [f"*{ext}" for ext in SUPPORTED_FILETYPES]
        joined_extensions = " ".join(wildcard_extensions)
        filter_str = f"Supported Files ({joined_extensions});;all files (* . *)"

        selected_path, _ = QFileDialog.getOpenFileName(self, "Select a Document File", "./", filter=filter_str)

        if selected_path:
            self.filepath = selected_path
            self.file_path_label.setText(self.filepath)
            self.generate_label.setText(f"File selected: {self.filepath}")

    def start_generation(self) -> None:
        """
        Gathers input and calls the external run function.
        """
        # Reset output
        self.output_to_copy = ""

        if not self.filepath:
            self.generate_label.setText("Please select a file first.")
            return

        prompt = self.prompt_text.toPlainText().strip()
        copy_to_clipboard = self.clipboard_checkbox.isChecked()

        try:
            self.generate_label.setText("Processing file... Please wait.")
            QApplication.processEvents()  # Update GUI immediately

            results = run(
                file_paths=[self.filepath],
                prompt=prompt,
                copy_to_clipoard=copy_to_clipboard,
            )

            success, msg, output = results[0]

            if not success:
                self.generate_label.setText(f"Error generating summary: {msg}")
            else:
                self.output_to_copy = output
                status_message = f"Summary successfully generated: {msg}"
                if copy_to_clipboard:
                    pyperclip.copy(output)
                    status_message += "\n(Output copied to clipboard.)"

                self.generate_label.setText(status_message)

        except Exception as e:
            error_msg = f"Unknown Exception: {e}"
            print(error_msg)
            self.generate_label.setText(f"A critical error occurred. Details: {e}")

    def copy_output(self) -> None:
        """Copies the last generated output to the system clipboard."""
        if len(self.output_to_copy) > 0:
            pyperclip.copy(self.output_to_copy)
            current_text = self.generate_label.text().split("\n")[0]  # Get the main status line
            self.generate_label.setText(f"{current_text}\n(Output successfully copied to clipboard again.)")
        else:
            self.generate_label.setText("No output generated yet. Click 'Generate Summary' first.")


def main():
    """
    Initializes and runs the main application.
    """
    app = QApplication(sys.argv)
    window = PaperSummaryApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
