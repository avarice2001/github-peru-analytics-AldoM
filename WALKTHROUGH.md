# GitHub Peru Analytics — Walkthrough Completo

## Resumen del Proyecto

Se desarrolló el proyecto **GitHub Peru Analytics** siguiendo las indicaciones del [issue #9](https://github.com/alexanderquispe/prompt_engineering/issues/9). El proyecto analiza el ecosistema de desarrolladores peruanos en GitHub, incluyendo extracción de datos, clasificación por industria con GPT-4, cálculo de métricas y un dashboard interactivo.

- **Repositorio:** [github-peru-analytics-AldoM](https://github.com/avarice2001/github-peru-analytics-AldoM)
- **Dashboard desplegado en:** Streamlit Community Cloud
- **Ubicación local:** `E:\1_cursos\2_qlab\2_summer_school_2026\4_prompt\qlab_proyect_homework2`

---

## Fase 1: Setup del Proyecto

- Creada estructura de directorios completa (`src/`, `scripts/`, `app/`, `tests/`, `data/`, `demo/`)
- Configurados archivos base: `requirements.txt`, `.env.example`, `.gitignore`, `README.md`
- Creado entorno virtual `.venv` e instaladas dependencias
- Ejecutado Easter Egg `antigravity` y capturado screenshot

---

## Fase 2: Extracción de Datos (GitHub API)

### Archivos implementados
- [github_client.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/src/extraction/github_client.py) — Cliente API con auth, rate-limit y retry
- [user_extractor.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/src/extraction/user_extractor.py) — Búsqueda de usuarios por ubicación (Perú)
- [repo_extractor.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/src/extraction/repo_extractor.py) — Extracción de READMEs y lenguajes
- [extract_data.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/scripts/extract_data.py) — Orquestador con `ThreadPoolExecutor`

### Resultados
- **46 desarrolladores** extraídos de Perú
- **1,219 repositorios** con READMEs y datos de lenguajes
- Tiempo de ejecución: ~17 minutos (optimizado con concurrencia)

### Desafíos resueltos
- Rate limiting de la API de GitHub → Implementado `sleep` adaptativo
- Velocidad lenta con procesamiento secuencial → Migrado a `ThreadPoolExecutor(max_workers=10)`

---

## Fase 3: Clasificación con GPT-4

### Archivos implementados
- [industry_classifier.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/src/classification/industry_classifier.py) — Clasificador con 21 códigos CIIU peruanos
- [classify_repos.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/scripts/classify_repos.py) — Script de clasificación batch

### Resultados
- **1,219 repos clasificados** en **18 industrias CIIU**
- Top industrias: Information & Communication (698), Professional/Scientific (143), Education (119)
- Tiempo: ~8 minutos (optimizado con `ThreadPoolExecutor`)

---

## Fase 4: Métricas

### Archivos implementados
- [user_metrics.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/src/metrics/user_metrics.py) — Métricas de actividad, influencia y técnicas
- [ecosystem_metrics.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/src/metrics/ecosystem_metrics.py) — Métricas agregadas del ecosistema
- [calculate_metrics.py](file:///E:/1_cursos/2_qlab/2_summer_school_2026/4_prompt/qlab_proyect_homework2/scripts/calculate_metrics.py) — Orquestador

### Métricas del Ecosistema

| Métrica | Valor |
|---------|-------|
| Total Developers | 46 |
| Total Repositories | 1,219 |
| Total Stars | 12,009 |
| Total Forks | 3,106 |

### Bugs corregidos
- `int64` de pandas no serializable a JSON → Cast a `int()` nativo
- `owner` campo string-ificado en CSV → Parsing con `ast.literal_eval()`

---

## Fase 5: Dashboard Streamlit

### Páginas implementadas
1. **Main** — Overview del ecosistema con métricas generales
2. **Overview** — Top developers y repositorios
3. **Developers** — Explorador de desarrolladores con filtros
4. **Repositories** — Browser de repos con búsqueda
5. **Industries** — Distribución por industria (gráfico de torta con Plotly)
6. **Languages** — Distribución de lenguajes de programación

### Screenshot del Dashboard
![Dashboard principal](file:///C:/Users/user/.gemini/antigravity/brain/7b7b7f6d-4442-40b9-9109-a4bdd49b3a47/streamlit_dashboard_main_1773118550923.png)

---

## Fase 6: Testing

```
============================= test session starts =============================
tests/test_extraction.py::test_github_client_init PASSED                 [ 25%]
tests/test_extraction.py::test_user_extractor_search PASSED              [ 50%]
tests/test_metrics.py::test_user_metrics_influence PASSED                [ 75%]
tests/test_metrics.py::test_ecosystem_metrics_totals PASSED              [100%]
============================== 4 passed in 0.81s ==============================
```

---

## Fase 7: Despliegue

1. **Git init** y commit de 31 archivos de código
2. **Repositorio GitHub** creado vía API: `avarice2001/github-peru-analytics-AldoM`
3. **Push de datos procesados** (1.26 MB) para Streamlit Cloud
4. **Deploy en Streamlit Community Cloud** — App pública accesible por URL

---

## Estructura Final del Proyecto

```
qlab_proyect_homework2/
├── app/
│   ├── main.py
│   └── pages/
│       ├── 1_Overview.py
│       ├── 2_Developers.py
│       ├── 3_Repositories.py
│       ├── 4_Industries.py
│       └── 5_Languages.py
├── data/
│   ├── metrics/
│   │   ├── ecosystem_metrics.json
│   │   └── user_metrics.csv
│   ├── processed/
│   │   ├── classifications.csv (679 KB)
│   │   ├── repositories.csv (7.6 MB)
│   │   └── users.csv (41 KB)
│   └── raw/
├── demo/
│   ├── antigravity_screenshot.png
│   └── video_link.md
├── scripts/
│   ├── calculate_metrics.py
│   ├── capture_antigravity.py
│   ├── classify_repos.py
│   └── extract_data.py
├── src/
│   ├── agents/insights_agent.py
│   ├── classification/industry_classifier.py
│   ├── extraction/
│   │   ├── github_client.py
│   │   ├── repo_extractor.py
│   │   └── user_extractor.py
│   └── metrics/
│       ├── ecosystem_metrics.py
│       └── user_metrics.py
├── tests/
│   ├── test_extraction.py
│   └── test_metrics.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## APIs y Tokens Utilizados
- **GitHub API** — Token personal (`ghp_...`) para extracción de datos
- **OpenAI API** — GPT-4 para clasificación de repositorios por industria CIIU
