# Plantilla de WORKER

#### WORKER: WorkerName

[DEFINE_WORKER: WorkerName]

**Objetivo**:
[Resultado operacional.]

[INPUTS]

- [Entrada.]
- [Variable.]
- [Referencia.]

[END_INPUTS]

[OUTPUTS]

- [Salida.]
- [Estado.]

[END_OUTPUTS]

[SEQUENTIAL_BLOCK]

1. Validar entradas.
2. Recuperar antecedentes.
3. Ejecutar actividad.
4. Generar resultado.
5. Validar resultado.
6. Registrar error o estado.

[END_SEQUENTIAL_BLOCK]

[VALIDATION]

- Input validation.
- Output validation.
- Fidelity validation.
- Provenance validation.

[END_VALIDATION]

[EXCEPTIONS]

- STRUCTURAL:
- RECORD:
- CONTENT:

[END_EXCEPTIONS]

[DEFINE_CONSTRAINTS:]

- MUST: Declarar inputs.
- MUST: Declarar outputs.
- MUST: Mantener invariantes.
- FORBID: Utilizar fuentes no declaradas.
- FORBID: Mezclar casos.
- FORBID: Completar información por inferencia.

[END_CONSTRAINTS]

[END_WORKER]
