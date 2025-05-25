import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox

# --- Funkcje do wczytywania/zapisywania z poprzednich tasków ---

def get_file_format(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".json", ".xml", ".yml", ".yaml"]:
        return ext[1:]
    else:
        raise ValueError(f"Nieobsługiwany format: {ext}")

def read_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_yaml_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_yaml_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

def read_xml_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return {child.tag: child.text for child in root}

def write_xml_file(path, data):
    root = ET.Element("root")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)

# --- UI PyQt5 ---

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter plików")
        self.setGeometry(100, 100, 400, 200)

        self.input_path = ""
        self.output_path = ""

        layout = QVBoxLayout()

        self.label = QLabel("Wybierz pliki do konwersji:")
        layout.addWidget(self.label)

        btn_input = QPushButton("Wybierz plik wejściowy")
        btn_input.clicked.connect(self.choose_input_file)
        layout.addWidget(btn_input)

        btn_output = QPushButton("Wybierz plik wyjściowy")
        btn_output.clicked.connect(self.choose_output_file)
        layout.addWidget(btn_output)

        btn_convert = QPushButton("Konwertuj")
        btn_convert.clicked.connect(self.convert)
        layout.addWidget(btn_convert)

        self.setLayout(layout)

    def choose_input_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik wejściowy")
        if path:
            self.input_path = path
            self.label.setText(f"Wejście: {os.path.basename(path)}")

    def choose_output_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Wybierz plik wyjściowy")
        if path:
            self.output_path = path
            self.label.setText(self.label.text() + f"\nWyjście: {os.path.basename(path)}")

    def convert(self):
        try:
            input_format = get_file_format(self.input_path)
            output_format = get_file_format(self.output_path)

            # Wczytaj dane
            if input_format == "json":
                data = read_json_file(self.input_path)
            elif input_format in ["yml", "yaml"]:
                data = read_yaml_file(self.input_path)
            elif input_format == "xml":
                data = read_xml_file(self.input_path)
            else:
                raise Exception("Nieobsługiwany format wejściowy.")

            # Zapisz dane
            if output_format == "json":
                write_json_file(self.output_path, data)
            elif output_format in ["yml", "yaml"]:
                write_yaml_file(self.output_path, data)
            elif output_format == "xml":
                write_xml_file(self.output_path, data)
            else:
                raise Exception("Nieobsługiwany format wyjściowy.")

            QMessageBox.information(self, "Sukces", "Konwersja zakończona sukcesem!")

        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))

# --- Uruchomienie aplikacji ---

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
