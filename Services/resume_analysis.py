import re
from io import BytesIO
from uuid import UUID

import httpx
from fastapi import HTTPException
from pypdf import PdfReader
from sqlalchemy.orm import Session

from Models.user import User
from Services.storage_service import get_file_by_path

ACTION_VERBS = {
    "desenvolvi", "desenvolveu", "liderei", "liderou", "implementei", "implementou",
    "criei", "criou", "gerenciei", "gerenciou", "otimizei", "otimizou", "construi",
    "construiu", "projetei", "projetou", "coordenei", "coordenou", "automatizei",
    "automatizou", "reduzi", "reduziu", "aumentei", "aumentou", "entreguei", "entregou",
    "desenhei", "desenhou", "arquitetei", "planejei", "planejou", "treinei", "treinou",
    "migrei", "migrou", "refatorei", "refatorou", "lancei", "lancou",
    "developed", "led", "implemented", "created", "managed", "optimized", "built",
    "designed", "coordinated", "automated", "reduced", "increased", "delivered",
    "architected", "planned", "trained", "launched", "improved", "drove", "shipped",
    "migrated", "refactored", "engineered", "streamlined",
}

SECTION_KEYWORDS = {
    "experiência": ["experiência", "experience", "experiencia", "atuação profissional", "atuacao profissional"],
    "formação": ["formação", "education", "academic", "graduação", "formacao", "acadêmic"],
    "habilidades": ["habilidades", "skills", "competências", "competencias", "tecnologias", "technologies"],
}

CLICHE_PHRASES = [
    "trabalho em equipe", "team player", "proativo", "proactive",
    "hard worker", "esforçado", "dinâmico", "dynamic", "comprometido",
    "fora da caixa", "outside the box",
]

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s.-]?)?\(?\d{2,3}\)?[\s.-]?\d{4,5}[\s.-]?\d{4}")
METRIC_RE = re.compile(r"\d+([.,]\d+)?\s?(%|x\b|anos|meses|mil\b|k\b)", re.IGNORECASE)
LINKEDIN_RE = re.compile(r"linkedin\.com/in/", re.IGNORECASE)
WORD_RE = re.compile(r"[a-zà-úA-ZÀ-Ú]+")


def download_pdf(pdf_url: str) -> bytes:
    try:
        resp = httpx.get(pdf_url, timeout=15, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Não foi possível baixar o PDF do currículo: {e}")
    return resp.content


def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        pages_text = [page.extract_text() or "" for page in reader.pages]
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Não foi possível ler o PDF (arquivo corrompido ou inválido): {e}")

    return "\n".join(pages_text)


def _finding(category: str, message: str) -> dict:
    return {"category": category, "message": message}


def analyze_resume_text(text: str) -> dict:
    critical: list[dict] = []
    suggestions: list[dict] = []
    positives: list[str] = []
    score = 100

    words = WORD_RE.findall(text)
    word_count = len(words)
    has_extractable_text = word_count >= 20

    if not has_extractable_text:
        critical.append(_finding(
            "Extração de Texto",
            "Não foi possível extrair texto de verdade do PDF — provavelmente é uma imagem escaneada. "
            "Sistemas de ATS reais não conseguem ler currículos assim, e isso pode eliminar o currículo "
            "automaticamente antes mesmo de um recrutador ver."
        ))
        return {
            "score": 20,
            "word_count": word_count,
            "has_extractable_text": False,
            "critical": critical,
            "suggestions": suggestions,
            "positives": positives,
        }

    lower = text.lower()

    # Tamanho
    if word_count < 150:
        critical.append(_finding("Tamanho", f"O currículo tem só {word_count} palavras — muito curto pra transmitir experiência suficiente. Detalhe mais suas conquistas."))
        score -= 15
    elif word_count > 1200:
        suggestions.append(_finding("Tamanho", f"O currículo tem {word_count} palavras — considere resumir. A maioria dos recrutadores gasta menos de 10 segundos na primeira leitura."))
        score -= 5
    else:
        positives.append(f"Tamanho adequado ({word_count} palavras).")

    # Contato
    has_email = bool(EMAIL_RE.search(text))
    has_phone = bool(PHONE_RE.search(text))
    has_linkedin = bool(LINKEDIN_RE.search(lower))

    if not has_email:
        critical.append(_finding("Contato", "Não encontrei um e-mail no currículo. Isso é essencial — sem ele, o recrutador (ou o ATS) não consegue te contatar."))
        score -= 15
    else:
        positives.append("E-mail de contato encontrado.")

    if not has_phone:
        suggestions.append(_finding("Contato", "Não encontrei um telefone no currículo. Considere incluir um."))
        score -= 5
    else:
        positives.append("Telefone de contato encontrado.")

    if not has_linkedin:
        suggestions.append(_finding("Contato", "Não encontrei um link do LinkedIn (linkedin.com/in/...). Recrutadores costumam checar o perfil — vale incluir."))
        score -= 5

    # Seções
    missing_sections = [
        section for section, keywords in SECTION_KEYWORDS.items()
        if not any(kw in lower for kw in keywords)
    ]
    if missing_sections:
        suggestions.append(_finding(
            "Estrutura",
            f"Não identifiquei uma seção clara de: {', '.join(missing_sections)}. ATS costuma procurar por títulos de seção assim pra categorizar as informações."
        ))
        score -= 5 * len(missing_sections)
    else:
        positives.append("Seções principais (experiência, formação, habilidades) identificadas.")

    # Verbos de ação
    action_count = sum(1 for w in words if w.lower() in ACTION_VERBS)
    if action_count == 0:
        suggestions.append(_finding("Linguagem", "Não encontrei verbos de ação fortes (ex: \"desenvolvi\", \"liderei\", \"implementei\"). Eles deixam as conquistas mais concretas e são bem vistos por ATS e recrutadores."))
        score -= 10
    elif action_count < 3:
        suggestions.append(_finding("Linguagem", "Poucos verbos de ação encontrados — tente começar mais frases de experiência com verbos fortes no passado."))
        score -= 5
    else:
        positives.append(f"Bom uso de verbos de ação ({action_count} encontrados).")

    # Métricas quantificáveis
    metric_count = len(METRIC_RE.findall(text))
    if metric_count == 0:
        suggestions.append(_finding("Impacto", "Não encontrei números ou métricas (%, quantidades, tempo). Resultados quantificados (ex: \"reduziu o tempo de resposta em 30%\") têm muito mais impacto que descrições genéricas."))
        score -= 10
    else:
        positives.append(f"{metric_count} métrica(s)/número(s) de impacto encontrados.")

    # Clichês
    found_cliches = [c for c in CLICHE_PHRASES if c in lower]
    if found_cliches:
        suggestions.append(_finding("Linguagem", f'Encontrei termos genéricos como "{found_cliches[0]}" — prefira mostrar essas qualidades através de exemplos concretos, em vez de só declará-las.'))
        score -= 3 * len(found_cliches)

    score = max(0, min(100, score))
    return {
        "score": score,
        "word_count": word_count,
        "has_extractable_text": True,
        "critical": critical,
        "suggestions": suggestions,
        "positives": positives,
    }


class ResumeAnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def analyze(self, user_id: UUID, lang: str = "pt") -> dict:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        pdf_url = user.curriculum_en_url if lang == "en" else user.curriculum_url
        if not pdf_url:
            raise HTTPException(status_code=404, detail="Nenhum currículo cadastrado para esse idioma")

        # Currículo enviado pelo /admin fica no próprio banco (/files/...);
        # links externos antigos continuam sendo baixados.
        stored = get_file_by_path(self.db, pdf_url)
        pdf_bytes = stored.data if stored else download_pdf(pdf_url)

        text = extract_pdf_text(pdf_bytes)
        return analyze_resume_text(text)
