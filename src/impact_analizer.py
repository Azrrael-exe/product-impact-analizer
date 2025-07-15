import openai
from enum import Enum
from typing import Optional
import os
from langfuse.openai import openai as langfuse_openai
from langfuse import observe

class BusinessObjective(Enum):
    """Enum para los objetivos de negocio disponibles"""
    REVENUE_GROWTH = "revenue_growth"
    COST_REDUCTION = "cost_reduction"
    CUSTOMER_SATISFACTION = "customer_satisfaction"
    OPERATIONAL_EFFICIENCY = "operational_efficiency"
    MARKET_EXPANSION = "market_expansion"
    INNOVATION = "innovation"
    RISK_MITIGATION = "risk_mitigation"

class ImpactAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el analizador de impacto
        
        Args:
            api_key: API key de OpenAI (opcional, se puede obtener del entorno)
        """
        # Configurar cliente OpenAI con Langfuse para monitoreo automático
        self.client = langfuse_openai.OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
    
    @observe(name="analyze_initiative_impact")
    def analyze_initiative_impact(
        self, 
        initial_investment: float,
        business_objective: BusinessObjective,
        expected_impact: float,
        initiative_name: str
    ) -> str:
        """
        Analiza el impacto de una iniciativa de negocio usando OpenAI
        
        Args:
            initial_investment: Inversión inicial (número positivo)
            business_objective: Objetivo de negocio (enum)
            expected_impact: Impacto esperado (valor entre 0 y 10)
            initiative_name: Nombre de la iniciativa
            
        Returns:
            str: Análisis de impacto generado por OpenAI
            
        Raises:
            ValueError: Si los parámetros no son válidos
            Exception: Si hay error en la llamada a OpenAI
        """
        
        # Validaciones
        if initial_investment <= 0:
            raise ValueError("La inversión inicial debe ser un número positivo")
        
        if not isinstance(business_objective, BusinessObjective):
            raise ValueError("El objetivo de negocio debe ser un valor válido del enum BusinessObjective")
        
        if not (0 <= expected_impact <= 10):
            raise ValueError("El impacto esperado debe estar entre 0 y 10")
        
        if not initiative_name or not initiative_name.strip():
            raise ValueError("El nombre de la iniciativa no puede estar vacío")
        
        # PLACEHOLDER: System prompt - personaliza según tus necesidades
        system_prompt = """
        Eres un consultor experto en análisis de impacto de iniciativas de negocio.
        Tu tarea es analizar iniciativas y proporcionar insights valiosos sobre:
        - Potencial retorno de inversión
        - Riesgos y beneficios
        - Recomendaciones estratégicas
        - Métricas clave de seguimiento
        
        Proporciona un análisis detallado pero conciso en español.
        """
        
        # Construir el prompt con la información de la iniciativa
        user_prompt = f"""
        Por favor, analiza la siguiente iniciativa de negocio:

        **Nombre de la iniciativa:** {initiative_name}
        **Inversión inicial:** ${initial_investment:,.2f}
        **Objetivo de negocio:** {business_objective.value.replace('_', ' ').title()}
        **Impacto esperado:** {expected_impact}/10

        Proporciona un análisis comprensivo que incluya:
        1. Evaluación del potencial de la iniciativa
        2. Análisis de la relación inversión-impacto
        3. Riesgos potenciales y factores de éxito
        4. Recomendaciones estratégicas
        5. Métricas clave para medir el éxito
        """
        
        try:
            # Llamada a OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Error al llamar a OpenAI: {str(e)}")

