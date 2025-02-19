# FOOTBALL MANAGER





# Descripción
Una pequeña descripción de lo que trata nuestro proyecto


# Qué necesitas saber antes de probar nuestro código
Todas las cosas que serán decesarias para el correcto funcionamiento de nuestro proyecto a la hora de corregir

ej:
pip install numpy # Para instalar la librería numpy


# Distribución de tareas
1. *******
2. *******
3. *******
4. *******

# Estructura
graph TD;
    Weave --> Neuro_Storage;
    Weave --> Neuro_Dataset;
    Weave --> Optimization;
    Weave --> Neuro_Functions;
    Weave --> Neural_Network;
    Weave --> Visualization;
    
    Neuro_Storage --> Saver;
    Neuro_Dataset --> Loader;
    Neural_Network --> Modules;
    
    classDef done fill:#00ff00,stroke:#000,stroke-width:2px;
    classDef inprocess fill:#ffff00,stroke:#000,stroke-width:2px;
    classDef notstarted fill:#ff0000,stroke:#000,stroke-width:2px;
    
    class Weave,Neuro_Storage,Neuro_Dataset,Optimization,Neuro_Functions,Neural_Network,Visualization done;
    class Saver,Loader,Modules done;
# Colaboradores

<!-- readme: collaborators -start -->
<table>
<tr>
    <td align="center">
        <a href="https://github.com/alg204">
            <img src="https://avatars.githubusercontent.com/u/198967558?v=4" width="100;" alt="alg204"/>
            <br />
            <sub><b>Adrián</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://https://github.com/ppf30">
            <img src="https://avatars.githubusercontent.com/u/198932016?v=4" width="100;" alt="ppf30"/>
            <br />
            <sub><b>Patricia</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/NikolasKaplan1">
            <img src="https://avatars.githubusercontent.com/u/199594735?v=4" width="100;" alt="nmk8"/>
            <br />
            <sub><b>Nikolas</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/Mohamed-Arahouani">
            <img src="https://avatars.githubusercontent.com/u/199315152?v=4" width="100;" alt="mak5"/>
            <br />
            <sub><b>Mohamed</b></sub>
        </a>
    </td></tr>
</table>


# Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.
