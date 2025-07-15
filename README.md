# Product Impact Analyzer

Una API FastAPI para analizar el impacto de iniciativas de negocio utilizando OpenAI.

## Descripción

Esta aplicación proporciona un endpoint para analizar iniciativas de negocio y generar insights sobre su potencial impacto, retorno de inversión, riesgos y recomendaciones estratégicas.

## Instalación

```bash
# Instalar dependencias
uv sync

# Configurar variables de entorno
cp env.example .env
# Edita el archivo .env con tus credenciales reales
```

## Uso

### Ejecutar la aplicación

Con `uv` (recomendado):

```bash
uv run src/main.py
```

O usando Python directamente:

```bash
python src/main.py
```

La aplicación estará disponible en `http://localhost:8000`

## Endpoints

### 1. Health Check

**GET** `/`

Verifica que la aplicación está funcionando correctamente.

#### Ejemplo de curl:

```bash
curl -X GET "http://localhost:8000/"
```

#### Respuesta esperada:

```json
{
  "message": "Hello World"
}
```

### 2. Análisis de Impacto

**POST** `/impact-analysis`

Analiza el impacto de una iniciativa de negocio.

#### Parámetros:

- `initial_investment` (float): Inversión inicial (debe ser positiva)
- `business_objective` (string): Objetivo de negocio. Valores válidos:
  - `revenue_growth`
  - `cost_reduction`
  - `customer_satisfaction`
  - `operational_efficiency`
  - `market_expansion`
  - `innovation`
  - `risk_mitigation`
- `expected_impact` (float): Impacto esperado (0-10)
- `initiative_name` (string): Nombre de la iniciativa

#### Ejemplo de curl:

```bash
curl -X POST "http://localhost:8000/impact-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "initial_investment": 50000.0,
    "business_objective": "revenue_growth",
    "expected_impact": 8.5,
    "initiative_name": "Campaña de Marketing Digital Q1"
  }'
```

#### Otro ejemplo con objetivo de reducción de costos:

```bash
curl -X POST "http://localhost:8000/impact-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "initial_investment": 25000.0,
    "business_objective": "cost_reduction",
    "expected_impact": 7.0,
    "initiative_name": "Automatización de Procesos Administrativos"
  }'
```

#### Respuesta esperada:

La respuesta será un análisis detallado generado por OpenAI que incluirá:

- Evaluación del potencial de la iniciativa
- Análisis de la relación inversión-impacto
- Riesgos potenciales y factores de éxito
- Recomendaciones estratégicas
- Métricas clave para medir el éxito

## Configuración

La aplicación utiliza variables de entorno para la configuración. Puedes configurarlas de dos maneras:

### Opción 1: Archivo .env (Recomendado para desarrollo)

```bash
# Copia el archivo de ejemplo
cp env.example .env

# Edita el archivo .env con tus credenciales reales
```

### Opción 2: Variables de entorno del sistema

#### OpenAI (Requerido)
```bash
export OPENAI_API_KEY="tu-api-key-aqui"
```

#### Langfuse (Requerido para monitoreo)
```bash
export LANGFUSE_SECRET_KEY="tu-langfuse-secret-key"
export LANGFUSE_PUBLIC_KEY="tu-langfuse-public-key"
export LANGFUSE_HOST="https://cloud.langfuse.com"  # o tu instancia self-hosted
```

#### Opcional - Variables de configuración adicionales:
```bash
export LANGFUSE_ENABLED=true      # Habilitar/deshabilitar Langfuse
export LANGFUSE_DEBUG=false       # Modo debug de Langfuse
export PORT=8000                  # Puerto de la aplicación
export ENVIRONMENT=development    # Entorno de la aplicación
```

### Obtener las credenciales:

#### OpenAI:
1. Ve a [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crea una nueva API key
3. Copia la key y pégala en tu archivo `.env`

#### Langfuse:
1. Regístrate en [Langfuse](https://langfuse.com/)
2. Crea un nuevo proyecto
3. Ve a Settings > API Keys
4. Copia tu `SECRET_KEY` y `PUBLIC_KEY`
5. Pégalos en tu archivo `.env`

## Gestión de Variables de Entorno

La aplicación utiliza `python-dotenv` para cargar automáticamente las variables de entorno desde un archivo `.env` en la raíz del proyecto.

### Archivo .env
- El archivo `.env` se carga automáticamente al iniciar la aplicación
- Nunca debe ser committeado al repositorio (está en `.gitignore`)
- Utiliza el archivo `env.example` como plantilla

### Prioridad de Variables
1. Variables de entorno del sistema (exportadas)
2. Variables del archivo `.env`
3. Valores por defecto (si los hay)

## Tecnologías

- FastAPI
- OpenAI API
- Langfuse (monitoreo y observabilidad)
- python-dotenv (gestión de variables de entorno)
- Uvicorn
- Python 3.9+

## Funcionalidades de Monitoreo

La aplicación incluye monitoreo con Langfuse que proporciona:

- **Trazabilidad completa**: Seguimiento de todas las llamadas a OpenAI
- **Métricas de rendimiento**: Latencia, tokens utilizados, costos
- **Logging automático**: Logs detallados de requests y responses
- **Dashboard visual**: Visualización de métricas en tiempo real
- **Debugging**: Capacidad de revisar y debuggear llamadas problemáticas

Para acceder al dashboard de Langfuse:
1. Ve a [cloud.langfuse.com](https://cloud.langfuse.com) (o tu instancia)
2. Selecciona tu proyecto
3. Revisa las métricas en tiempo real del endpoint `/impact-analysis`