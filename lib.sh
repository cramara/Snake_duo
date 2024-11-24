#!/bin/bash

echo "Installation des bibliothèques..."

# Assurez-vous que pip est à jour
python3 -m pip install --upgrade pip

# Installe les bibliothèques
python3 -m pip install tk
python3 -m pip install pillow
python3 -m pip install matplotlib

# Vérifie si l'installation a réussi
python3 -c "import tk, os, io, PIL, matplotlib; print('Installation des bibliothèques réussie.')"

#autorise l'execution des codes python
chmod +x Menu.py
chmod +x Snake_final.py
chmod +x Intermediaire.py
chmod +x Player.py
chmod +x Final_Bot.py


echo "Installation terminée."
read -p "Appuyez sur Entrée pour quitter."