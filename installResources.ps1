# installResources.ps1
# Instalacja wymaganych bibliotek

# Upewnij się, że pip jest dostępny
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Instalacja z pliku requirements.txt
pip install -r requirements.txt

# Dodatkowe biblioteki (jeśli nie są w requirements.txt)
pip install lxml         
pip install xmltodict    
pip install jsonschema   
