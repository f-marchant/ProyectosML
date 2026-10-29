# Contexto de Dominio: {{PROJECT_NAME}}

## 1. Definición del Problema de Negocio
- **Contexto**: Describe el contexto operativo y el problema que se busca resolver.
- **Objetivo Cuantitativo**: ¿Qué métrica de negocio o impacto se espera mover?
- **Variable Objetivo ($y$)**: Nombre de la variable dependiente y tipo (binaria, multiclase, continua).

---

## 2. Diccionario de Datos (Variables)

| Variable | Tipo de Dato | Rol (Feature / Target / ID) | Descripción y Rango Esperado |
| :--- | :--- | :--- | :--- |
| `id` | Entero / String | Identificador | Clave única de la entidad |
| `variable_1` | Numérico | Feature | Descripción técnica |
| `target` | Binario (0/1) | Target | Indicador del evento de interés |

---

## 3. Restricciones y Reglas del Dominio
- Variables que no pueden ser usadas por confidencialidad o sesgo ético.
- Umbrales de negocio o puntos de corte operativos.
