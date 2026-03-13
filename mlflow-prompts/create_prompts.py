"""
Script to create multiple prompt versions in MLflow Prompt Storage.
Run after MLflow server is started: python create_prompts.py
"""
import mlflow
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

client = mlflow.MlflowClient()


def create_prompt_version(name: str, template: str, tags: dict = None):
    """Register a prompt version in MLflow Prompt Storage."""
    try:
        # Try to create registered model for the prompt
        try:
            client.create_registered_model(
                name=f"prompt.{name}",
                tags={"type": "prompt", **(tags or {})}
            )
        except Exception:
            pass  # Model already exists

        with mlflow.start_run(run_name=f"prompt_{name}"):
            mlflow.log_param("prompt_name", name)
            mlflow.log_text(template, f"prompts/{name}.txt")
            if tags:
                for k, v in tags.items():
                    mlflow.log_param(k, v)

        print(f"Created prompt '{name}'")
    except Exception as e:
        print(f"Error creating prompt '{name}': {e}")


# Prompt 1: Credit scoring system prompt v1 - basic
create_prompt_version(
    name="credit_scoring_system_v1",
    template="""You are a credit analyst assistant. Analyze the applicant's data and provide a credit assessment.

Applicant data: {applicant_data}

Provide:
1. Risk assessment (Low/Medium/High)
2. Key risk factors
3. Recommendation""",
    tags={"version": "1", "use_case": "credit_scoring", "language": "en"}
)

# Prompt 2: Credit scoring system prompt v2 - detailed with scoring criteria
create_prompt_version(
    name="credit_scoring_system_v2",
    template="""You are an expert credit risk analyst with 10+ years of experience.
Evaluate the credit application based on the following criteria:

**Applicant Profile:**
{applicant_data}

**Scoring Criteria:**
- Payment History (35%): Past payment behavior
- Credit Utilization (30%): Amount of credit used vs available
- Credit History Length (15%): Duration of credit history
- Credit Mix (10%): Types of credit accounts
- New Credit (10%): Recent credit inquiries

**Your Analysis:**
1. Score each criterion (1-10)
2. Calculate weighted score
3. Risk classification: AAA (>8), AA (7-8), A (6-7), BBB (5-6), BB (4-5), B (<4)
4. Decision with justification
5. Conditions or requirements if applicable""",
    tags={"version": "2", "use_case": "credit_scoring", "language": "en", "model": "detailed"}
)

# Prompt 3: Russian language version
create_prompt_version(
    name="credit_scoring_system_ru",
    template="""Вы - эксперт по кредитному анализу. Оцените кредитную заявку.

**Данные заявителя:**
{applicant_data}

**Анализ:**
1. Оценка кредитоспособности (1-10)
2. Ключевые факторы риска
3. Рекомендация: Одобрить / Отклонить / Требует дополнительной проверки
4. Условия выдачи кредита (если применимо)

Предоставьте структурированный анализ на русском языке.""",
    tags={"version": "1", "use_case": "credit_scoring", "language": "ru"}
)

# Prompt 4: Explanation prompt for model decisions
create_prompt_version(
    name="model_explanation_prompt",
    template="""Explain the credit scoring model decision to the applicant in simple, clear language.

**Model Output:**
- Score: {score}
- Decision: {decision}
- Key Features: {feature_importance}

**Instructions:**
- Use plain language, avoid technical jargon
- Be empathetic and professional
- If rejected, explain what can be improved
- Keep the explanation under 200 words
- Do not reveal internal model details""",
    tags={"version": "1", "use_case": "explanation", "audience": "customer"}
)

# Prompt 5: Fraud detection prompt
create_prompt_version(
    name="fraud_detection_prompt_v1",
    template="""Analyze the following transaction and applicant data for potential fraud indicators.

**Data:**
{transaction_data}

**Red Flags to Check:**
- Inconsistent income vs. lifestyle indicators
- Unusual application patterns
- Identity verification issues
- Address/employment verification issues

**Output Format:**
- Fraud Risk Score: 0-100
- Detected Red Flags: [list]
- Recommended Action: [Approve/Review/Reject/Escalate]
- Confidence: [Low/Medium/High]""",
    tags={"version": "1", "use_case": "fraud_detection", "language": "en"}
)

print("\nAll prompts created successfully!")
print(f"View them at: {MLFLOW_TRACKING_URI}")
