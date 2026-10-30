---
name: diagnose
description: Bucle de diagnóstico metódico y riguroso para bugs difíciles, discrepancias en pipelines, fallos de inferencia o regresiones de rendimiento. Úsalo cuando el usuario diga "diagnostica", "depura esto", o reporte fallos silenciosos, lentitud o excepciones.
---

# Diagnosing Bugs & Pipeline Regressions

Una disciplina sistemática para resolver errores complejos. No te saltes fases sin justificación explícita.

Antes de comenzar a explorar, consulta `CONTEXT.md` y `_context/` (si existen) para comprender el modelo mental del dominio y las restricciones vigentes.

## Protección de Secretos (Redact)

Durante este diagnóstico mostrarás comandos, salidas y artefactos capturados. **Redacta cualquier secreto antes de mostrarlo**: reemplázalo por `<REDACTED>`. Si una salida redactada no es suficiente para aislar la causa raíz, indícaselo explícitamente al usuario.

---

## Fase 1: Construir un Bucle de Retroalimentación (Feedback Loop)

**Este es el núcleo de la skill.** Todo lo demás es mecánico. Si cuentas con una señal binaria (pasa/falla) estricta y rápida para este bug exacto, encontrarás la causa raíz. Si intentas adivinar leyendo código sin reproducir, fracasarás.

Invierte el esfuerzo necesario aquí:

### Métodos para construir el bucle (en orden de preferencia):
1. **Test unitario o de integración fallando** en la juntura exacta del error (ej. pytest sobre la función o transformación).
2. **Script de invocación CLI/curl mínimo** con una entrada sintética controlada que reproduzca el error o compare contra un snapshot conocido.
3. **Reproducción de trace o payload capturado**: guarda el payload o fila defectuosa y ejecútala de forma aislada a través del pipeline.
4. **Harness descartable**: levanta un subconjunto mínimo del sistema (una clase, un módulo aislado) que dispare la ruta del código con una sola llamada.
5. **Bucle de bisección**: si el problema apareció entre versiones o commits específicos, automatiza la verificación para correr `git bisect`.
6. **Script Human-in-the-Loop (HITL)** como último recurso mediante `scripts/hitl-loop.template.sh` si se requiere intervención manual obligatoria.

### Criterio de Término de la Fase 1:
La Fase 1 termina únicamente cuando puedes nombrar **un solo comando ejecutable** (un test, un script, una invocación) que:
- [ ] Sea **capaz de fallar en rojo** ante este síntoma exacto, y ponerse en verde al solucionarse.
- [ ] Sea **determinista** (mismo resultado en cada ejecución).
- [ ] Sea **rápido** (segundos, no minutos).
- [ ] Sea **ejecutable por el agente** de forma desatendida.

> ⚠️ **Regla de Oro**: Si te descubres formulando hipótesis o leyendo código sin tener este comando fallando en rojo, **DETENTE**. Saltar directo a formular teorías es el fallo que esta disciplina previene.

---

## Fase 2: Reproducir y Minimizar

Ejecuta el bucle y observa cómo falla en rojo:
- [ ] Confirma que la falla coincide exactamente con el síntoma reportado por el usuario, no un error tangencial colateral.
- [ ] Reduce la entrada o el escenario al **caso mínimo reproducible**: elimina filas, columnas, dependencias y pasos no esenciales uno a uno, verificando que siga fallando.
- [ ] El caso mínimo es aquel donde cada elemento restante es imprescindible (si quitas algo más, pasa a verde).

---

## Fase 3: Formular Hipótesis Falsables

Genera entre **3 y 5 hipótesis jerarquizadas** antes de modificar código. Generar una sola hipótesis ancla el pensamiento en la primera idea plausible.

Cada hipótesis debe ser **falsable** y seguir este formato estricto:
> *"Si [X] es la causa raíz, entonces al [cambiar Y] el bug desaparecerá / al [cambiar Z] el síntoma se agravará."*

Muestra la lista jerarquizada al usuario o en tu log de trabajo antes de instrumentar.

---

## Fase 4: Instrumentación Selectiva

Cada sonda o log debe verificar una predicción específica de la Fase 3:
- **Cambia una sola variable a la vez**.
- Etiqueta cada log temporal con un prefijo único identificable: `[DEBUG-XXXX]`.
- En problemas de rendimiento o inferencia lenta: no adivines con logs; establece una medición base con profiler/tiempos de ejecución y compara.

---

## Fase 5: Corrección y Test de Regresión

1. Convierte el caso mínimo reproducible en un test de regresión automatizado formal.
2. Comprueba que el test falla en rojo.
3. Aplica la corrección mínima y necesaria (cumpliendo YAGNI).
4. Comprueba que el test de regresión pasa a verde.
5. Re-ejecuta el bucle de retroalimentación de la Fase 1 contra el escenario completo inicial.

---

## Fase 6: Limpieza y Documentación

Antes de dar la tarea por concluida:
- [ ] El bug original ya no se reproduce en el escenario real.
- [ ] El test de regresión está integrado y pasando.
- [ ] Toda la instrumentación temporal `[DEBUG-XXXX]` ha sido eliminada (`grep` de prefijo).
- [ ] Cualquier script temporal de prueba ha sido eliminado o movido a `scratch/`.
- [ ] La causa raíz confirmada y la solución quedan explicadas con claridad en el commit o reporte.
