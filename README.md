# SIMULADOR DE BOLSA

![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=4000&pause=1000&center=true&vCenter=true&multiline=true&repeat=false&width=800&height=100&lines=Invierte,+Aprende,+Gana;Simula+tu+Éxito+en+la+Bolsa)



![Static Badge](https://img.shields.io/badge/Version-v1.0.0-green)
![Static Badge](https://img.shields.io/badge/Colaboradores-4-pink)


# Descripción
Este simulador permitirá a los usuarios:

· Comprar y vender acciones en base a datos reales del mercado.

· Analizar el rendimiento de sus inversiones con gráficos.

· Simular estrategais de inversión a corto y largo plazo.

# Qué necesitas saber antes de probar nuestro código
Para que no haya errores a la hora de probar nuestro código, te recomendamos ejecutar todo el interior de requirements.txt
En este archivo se incluye la instalación de todas las librerías necesarias para la ejecución del *SIMULADOR DE BOLSA DE VALORES*.

# Distribución de tareas
Patricia tiene como función principal desarrollar la API REST, para ello utiliza Flask para crear los distintos puntos finales requeridos: gestión de inversores, acciones y transacciones. Su trabajo también incluye el manejo de excepciones en las rutas con `abort` para asegurar que las respuestas sean claras y controladas en caso de errores. También se encarga de el desarrollo y la actualización de todas las pruebas automáticas, tanto unitarias como de integración.

Mohamed, en cambio, se enfoca en el núcleo del mercado financiero simulado. Su tarea principal es diseñar e implementar las clases `Accion` y `Mercado`. Estas clases ayudan a modelar el comportamiento de los valores del mercado, mostrando su evolución en el tiempo, ya sea de manera aleatoria o con datos reales obtenidos a través de yfinance. Además, Mohamed se asegura de manejar posibles errores en este proceso, como problemas al conseguir precios o acciones que no existen. 

Niko se encarga de la creación del módulo de inversión y operaciones financieras. Él crea la clase base `Inversor` y sus especializaciones `InversorConservador` e `InversorAgresivo` que se encuentran en el apartado de estrategias, utilizando principios de herencia para reflejar diferentes tipos de inversión. También incorpora la sobrecarga de operadores como `__ add __` y `__ sub __` para realizar compras y ventas en el código. Además, es responsable de la clase `Transaccion`, que guarda el historial de operaciones, y gestiona archivos, tanto en formato de texto para crear registros, como en binario mediante pickle para serializar objetos como carteras completas.

Por último, Adrián se ocupa de todo lo relacionado con la persistencia de datos, implementando una base de datos relacional en SQLite. ha diseñado las tablas necesarias para inversores, acciones y transacciones, y desarrolla funciones CRUD para operar sobre ellas desde el código. También maneja las excepciones específicas de la base de datos, asegurando la integridad de los datos.

# Estructura

```mermaid
classDiagram
    %% Definición de clases
    class Accion {
        -nombre: str
        -precio_actual: float
        +actualizar_precio(): void
    }

    class Mercado {
        -acciones: List<Accion>
        +simular(): void
        +registrar_accion(accion: Accion): void
    }

    class Inversor {
        -nombre: str
        -capital: float
        +comprar(): void
        +vender(): void
    }

    class Transaccion {
        -fecha: datetime
        -accion: Accion
        -inversor: Inversor
        -cantidad: int
        -precio: float
    }

    class InversorConservador {
        +estrategia(): str
    }

    class InversorAgresivo {
        +estrategia(): str
    }

    class IA {
        +predecir(): float
    }

    class db_manager {
        +conectar(): Connection
        +insertar_transaccion(): void
        +leer_transacciones(): List~Transaccion~
    }

    class JWT {
        +crear_token(): str
        +verificar_token(): bool
    }

    class accion_router
    class inversor_router
    class transaccion_router

    %% Agrupación por paquetes usando namespaces
    namespace models {
        Accion
        Mercado
        Inversor
        Transaccion
    }

    namespace estrategias {
        InversorConservador
        InversorAgresivo
        IA
    }

    namespace database {
        db_manager
    }

    namespace auth {
        JWT
    }

    namespace routers {
        accion_router
        inversor_router
        transaccion_router
    }

    %% Relaciones
    InversorConservador --|> Inversor
    InversorAgresivo --|> Inversor
    Transaccion --> Accion
    Transaccion --> Inversor
    Mercado --> Accion
    Inversor --> Accion
    main --> accion_router
    main --> inversor_router
    main --> transaccion_router
    accion_router --> Accion
    inversor_router --> Inversor
    transaccion_router --> Transaccion
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
