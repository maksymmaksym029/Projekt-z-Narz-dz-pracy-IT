import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

# ---------- Funkcje konwersji ----------

def get_file_format(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".json", ".xml", ".yml", ".yaml"]:
        return ext[1:]
    raise ValueError(f"Nieobsługiwany format: {ext}")

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

def read_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return {child.tag: child.text for child in root}

def write_xml(path, data):
    root = ET.Element("root")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)

# ---------- Wątek konwersji ----------

class ConverterThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            input_format = get_file_format(self.input_path)
            output_format = get_file_format(self.output_path)

            if input_format == "json":
                data = read_json(self.input_path)
            elif input_format in ["yml", "yaml"]:
                data = read_yaml(self.input_path)
            elif input_format == "xml":
                data = read_xml(self.input_path)
            else:
                raise Exception("Nieobsługiwany format wejściowy")

            if output_format == "json":
                write_json(self.output_path, data)
            elif output_format in ["yml", "yaml"]:
                write_yaml(self.output_path, data)
            elif output_format == "xml":
                write_xml(self.output_path, data)
            else:
                raise Exception("Nieobsługiwany format wyjściowy")

            self.finished.emit("Konwersja zakończona sukcesem!")

        except Exception as e:
            self.error.emit(str(e))

# ---------- Interfejs użytkownika ----------

class ConverterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asynchroniczny konwerter plików")
        self.setGeometry(200, 200, 400, 200)

        self.input_path = ""
        self.output_path = ""

        layout = QVBoxLayout()

        self.label = QLabel("Wybierz pliki:")
        layout.addWidget(self.label)

        btn_in = QPushButton("Wybierz plik wejściowy")
        btn_in.clicked.connect(self.select_input)
        layout.addWidget(btn_in)

        btn_out = QPushButton("Wybierz plik wyjściowy")
        btn_out.clicked.connect(self.select_output)
        layout.addWidget(btn_out)

        btn_run = QPushButton("Konwertuj")
        btn_run.clicked.connect(self.run_conversion)
        layout.addWidget(btn_run)

        self.setLayout(layout)

    def select_input(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik wejściowy")
        if path:
            self.input_path = path
            self.label.setText(f"Wejście: {os.path.basename(path)}")

    def select_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "Wybierz plik wyjściowy")
        if path:
            self.output_path = path
            self.label.setText(self.label.text() + f"\nWyjście: {os.path.basename(path)}")

    def run_conversion(self):
        if not self.input_path or not self.output_path:
            QMessageBox.warning(self, "Uwaga", "Wybierz oba pliki.")
            return

        self.thread = ConverterThread(self.input_path, self.output_path)
        self.thread.finished.connect(self.show_success)
        self.thread.error.connect(self.show_error)
        self.thread.start()

    def show_success(self, msg):
        QMessageBox.information(self, "Sukces", msg)

    def show_error(self, err):
        QMessageBox.critical(self, "Błąd", err)

# ---------- Uruchomienie ----------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterUI()
    window.show()
    sys.exit(app.exec_())
