# Metodologias de Diseño Taller 2

Este repositorio implementa un sistema de pagos siguiendo arquitectura hexagonal.

Actualmente, el programa no está acoplado, lo que facilita la incorporación de nuevas funcionalidades. Al utilizar puertos y adaptadores, podemos crear pruebas para cada componente de forma independiente, mejorando así la legibilidad y mantenibilidad del código.

## Ejectuar

```bash
uvicorn app.main:app --reload
```

## Instalar dependencias

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Sin env

```bash
pip install -r requirements.txt
```

## Suposiciones

- En la lista de casos de uso no se incluyó la opción de actualizar un pago. Consideramos añadirla, pero para mantener el proyecto simple, decidimos omitirla. Dado el diseño del sistema, su implementación sería sencilla: solo se modificarían los puertos y se añadiría la nueva funcionalidad.

## Endpoints

Con la url por defecto:

```bash
http://127.0.0.1:8000
```

### Crear Pago

```bash
POST /payments
```

Body:

```bash
{
  "nombre_cliente": "Pepe",
  "monto": 20
}
```

### Obtener pagos

```bash
GET /payments
```

### Obtener pagos por nombre de cliente

```bash
GET /payments/client/{nombre}
```

### Eliminar pagos

```bash
DELETE /payments/{id_del_pago}
```

### Estado del programa

```bash
GET /
```

## Miembros

- Martín Vásquez Medel
- Maycol Zincker Lazarú
