import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET

def get_file_format(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".json", ".xml", ".yml", ".yaml"]:
        return ext[1:]
    else:
        raise ValueError(f"Nieobsługiwany format pliku: {ext}")

def read_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print("[OK] JSON poprawnie wczytany.")
            print("[INFO] Podgląd danych:", data)
            return data
    except json.JSONDecodeError as e:
        print(f"[BŁĄD] Niepoprawny JSON: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[BŁĄD] Plik wejściowy nie istnieje: {path}")
        sys.exit(1)

def write_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"[OK] Dane zapisane do pliku JSON: {path}")
    except Exception as e:
        print(f"[BŁĄD] Nie udało się zapisać pliku JSON: {e}")
        sys.exit(1)

def read_yaml_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            print("[OK] YAML poprawnie wczytany.")
            print("[INFO] Podgląd danych:", data)
            return data
    except yaml.YAMLError as e:
        print(f"[BŁĄD] Niepoprawny YAML: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[BŁĄD] Plik wejściowy nie istnieje: {path}")
        sys.exit(1)

def write_yaml_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            print(f"[OK] Dane zapisane do pliku YAML: {path}")
    except Exception as e:
        print(f"[BŁĄD] Nie udało się zapisać pliku YAML: {e}")
        sys.exit(1)

def read_xml_file(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        data = {}

        for child in root:
            data[child.tag] = child.text

        print("[OK] XML poprawnie wczytany.")
        print("[INFO] Podgląd danych:", data)
        return data

    except ET.ParseError as e:
        print(f"[BŁĄD] Niepoprawny XML: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[BŁĄD] Plik wejściowy nie istnieje: {path}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Użycie: python Task6.py pathFile1.x pathFile2.y")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        input_format = get_file_format(input_path)
        output_format = get_file_format(output_path)

        print(f"[OK] Plik wejściowy: {input_path} ({input_format})")
        print(f"[OK] Plik wyjściowy: {output_path} ({output_format})")

        data = None

        if input_format == "json":
            data = read_json_file(input_path)
        elif input_format in ["yml", "yaml"]:
            data = read_yaml_file(input_path)
        elif input_format == "xml":
            data = read_xml_file(input_path)

        if output_format == "json" and data is not None:
            write_json_file(output_path, data)
        elif output_format in ["yml", "yaml"] and data is not None:
            write_yaml_file(output_path, data)

    except ValueError as e:
        print(f"[BŁĄD] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
