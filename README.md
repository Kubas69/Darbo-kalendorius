# Darbo kalendorius 2024

Ši programa leidžia vartotojui tvarkyti darbo užduotis, jas planuoti pagal datą ir valandą bei peržiūrėti svarbius įvykius.

## Kaip naudotis programa?

1. **Paleidimas**: Paleiskite programą, vykdant kodą `python darbo_kalendorius.py`.

2. **Įrašų valdymas**: Programoje galite pridėti naujų įrašų, juos redaguoti, ištrinti arba peržiūrėti visus esamus įrašus.

3. **Kalendorius**: Naudojant kalendorių, galite pasirinkti norimą datą ir peržiūrėti susijusius įrašus.

4. **Šios dienos informacija**: Programa pateikia informaciją apie dabartinę datą, įskaitant šios dienos pavadinimą lietuvių kalba ir šventes, jei jos yra.

## Reikalingos bibliotekos

- `tkinter`: Sukuria grafinę sąsają.
- `tkcalendar`: Kalendoriaus komponentui.
- `sqlite3`: Duomenų bazės valdymui.
- `datetime`: Darbo su datos ir laiku funkcijoms.

## Pagrindinės funkcijos

- `add_data()`: Pridėti naują įrašą į duomenų bazę.
- `edit_data()`: Redaguoti esamą įrašą.
- `delete_data()`: Ištrinti pasirinktą įrašą iš duomenų bazės.
- `show_all_data()`: Rodyti visus įrašus sąraše.
- `show_data()`: Rodyti įrašus pagal pasirinktą datą kalendoriuje.
- `new_entry()`: Sukurti naują įrašą.

