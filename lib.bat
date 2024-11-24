@echo off
echo Installation des bibliotheques...

REM Assurez-vous que pip est à jour
python -m pip install --upgrade pip

REM Installe les bibliothèques
python -m pip install tkinter
python -m pip install pillow
python -m pip install matplotlib

REM Vérifie si l'installation a réussi
python -c "import tkinter, os, io, PIL, matplotlib; print('Installation des bibliotheques reussie.')"

echo Installation terminee.
pause
