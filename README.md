# SIMULADOR DE BOLSA

<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=4000&pause=1000&center=true&vCenter=true&multiline=true&repeat=false&width=800&height=100&lines=Invierte,+Aprende,+Gana;Simula+tu+Éxito+en+la+Bolsa+🚀📈" alt="Typing SVG" />
  </a>
</p>



![Static Badge](https://img.shields.io/badge/Version-v1.0.0-green)
![Static Badge](https://img.shields.io/badge/Colaboradores-4-pink)


# DESCRIPCIÓN
Este simulador permitirá a los usuarios:

· Comprar y vender acciones en base a datos reales del mercado.

· Analizar el rendimiento de sus inversiones con gráficos.

· Simular estrategais de inversión a corto y largo plazo.

# Qué necesitas saber antes de probar nuestro código
Para que no haya errores a la hora de probar nuestro código, te recomendamos ejecutar todo el interior de requirements.txt
En este archivo se incluye la instalación de todas las librerías necesarias para la ejecución del *SIMULADOR DE BOLSA DE VALORES*.

# Distribución de tareas
1. *******
2. *******
3. *******
4. *******

# Estructura
- ![#00ff00](https://placehold.co/15x15/00ff00/00ff00.png) `Done`
- ![#ffff00](https://placehold.co/15x15/ffff00/ffff00.png) `In process`
- ![#ff0000](https://placehold.co/15x15/ff0000/ff0000.png) `Not started`

```mermaid
classDiagram
    class Inversor {
        +string nombre
        +float capital
        +List~Accion~ cartera
        +comprar(accion: Accion, cantidad: int)
        +vender(accion: Accion, cantidad: int)
        +mostrar_cartera() str
        +_str_() str
    }
    
    class Accion {
        +string simbolo
        +string nombre
        +float precio_actual
        +float historial_precios[]
        +actualizar_precio(nuevo_precio: float)
        +_str_() str
    }
    
    class Mercado {
        +List~Accion~ lista_acciones
        +registrar_accion(accion: Accion)
        +obtener_precio(simbolo: str) float
        +simular_movimientos()
    }
    
    class Transaccion {
        +Inversor inversor
        +Accion accion
        +int cantidad
        +float precio
        +_str_() str
    }
    
    class IA {
        +recomendar_inversion(inversor: Inversor) List~Accion~
    }
    
    class InversorConservador {
        +recomendar_compra() List~Accion~
    }
    
    class InversorAgresivo {
        +recomendar_compra() List~Accion~
    }
    
    Inversor <|-- InversorConservador
    Inversor <|-- InversorAgresivo
    Inversor "1" -- "*" Accion : "posee"
    Inversor "1" -- "*" Transaccion : "realiza"
    Mercado "1" -- "*" Accion : "gestiona"
    IA "1" -- "*" Accion : "recomienda"
```
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
