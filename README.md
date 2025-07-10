# Metodologias de Diseno Taller 2

Este repositorio implementa un sistema de pagos siguiendo arquitectura hexagonal.

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
