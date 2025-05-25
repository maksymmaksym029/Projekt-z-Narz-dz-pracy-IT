import sys
import os
import json

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
        print("[BŁĄD] Plik wejściowy nie istnieje.")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Użycie: python JSON.py pathFile1.x pathFile2.y")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        input_format = get_file_format(input_path)
        output_format = get_file_format(output_path)

        print(f"[OK] Plik wejściowy: {input_path} ({input_format})")
        print(f"[OK] Plik wyjściowy: {output_path} ({output_format})")

        if input_format == "json":
            data = read_json_file(input_path)



    except ValueError as e:
        print(f"[BŁĄD] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
