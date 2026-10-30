# CONTEXT.md — Arquitectura y Contratos: {{PROJECT_NAME}}

Este archivo define la estructura y contratos operativos de la Aplicación de Datos / Dashboard MVP.

---

## 1. Mapa de Contexto

| Carpeta / Archivo | Tipo de Información | Cuándo consultarlo |
| :--- | :--- | :--- |
| `_context/product.md` | Audiencia, problema y valor del MVP | Al agregar vistas o replantear objetivos |
| `_context/design.md` | Tokens visuales, colores y anti-patrones | Al estilizar componentes o gráficos |
| `_context/data_dictionary.md` | Esquemas y reglas de datos | Al incorporar nuevas fuentes de datos |
| `src/app.py` | Entrada principal y layout de la app | Al modificar la estructura global de vistas |
| `src/components/` | Componentes modulares (KPIs, gráficos, filtros) | Al enriquecer o ajustar componentes |
| `src/data_loader.py` | Ingesta, caching y transformaciones | Al modificar cómo se cargan los datos |
| `src/styles/custom.css`| Hoja de estilos de la interfaz | Al refinar el estilo visual |
| `.agents/skills/impeccable/` | Catálogo de skills de diseño Impeccable | Al auditar, criticar o pulir la UI |
| `tests/` | Suites de validación de carga e higiene | Antes de cada entrega |

---

## 2. Flujo de Desarrollo del MVP
1. **Definir el Contrato de Producto**: Especificar audiencia y preguntas de negocio en `_context/product.md`.
2. **Definir el Contrato Visual**: Confirmar tokens de color y tipografía en `_context/design.md`.
3. **Carga y Validación de Datos**: Implementar la lógica en `src/data_loader.py` con test en `tests/test_data_loader.py`.
4. **Construcción Modular de la UI**: Ensamblar componentes desacoplados en `src/components/` e integrarlos en `src/app.py`.
5. **Auditoría Impeccable**: Ejecutar revisión con `/impeccable audit` o `polish` para garantizar una experiencia sin "AI slop".
