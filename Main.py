import sys
import os

def get_file_format(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".json", ".xml", ".yml", ".yaml"]:
        return ext[1:]  # usuń kropkę z rozszerzenia
    else:
        raise ValueError(f"Nieobsługiwany format pliku: {ext}")

def main():
    if len(sys.argv) != 3:
        print("Użycie: python main.py pathFile1.x pathFile2.y")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        input_format = get_file_format(input_path)
        output_format = get_file_format(output_path)

        print(f"[OK] Plik wejściowy: {input_path} ({input_format})")
        print(f"[OK] Plik wyjściowy: {output_path} ({output_format})")

    except ValueError as e:
        print(f"[BŁĄD] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
