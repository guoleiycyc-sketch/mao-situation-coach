import importlib.util
import re
import shutil
from pathlib import Path


SCRIPT = Path("skill/mao-situation-coach/scripts/validate_content.py")
SKILL_DIR = Path("skill/mao-situation-coach")
ROUTER = SKILL_DIR / "references" / "model-router.md"
SOURCE_CATALOG = SKILL_DIR / "references" / "source-catalog.md"
SPEC = importlib.util.spec_from_file_location("validate_content", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


FORBIDDEN_DEPENDENCY_CODE_POINTS = (
    (24515, 21147, 25945, 32451),
    (24515, 21147, 21152, 24037),
)


def forbidden_dependencies():
    return tuple(
        "".join(chr(code_point) for code_point in dependency)
        for dependency in FORBIDDEN_DEPENDENCY_CODE_POINTS
    )


REQUIRED_FIELDS = """\
### 核心命题
从实践中检验认识。
### 原文出处
证据等级：A 级；表达方式：有来源释义。第一卷《反对本本主义》。
### 历史问题
本本主义脱离实际。
### 关键变量
实践与认识。
### 关系逻辑
实践决定认识。
### 推演步骤
调查后作判断。
### 适用条件
需要具体判断时。
### 失效条件
资料不足时。
### 常见误用
用口号代替调查。
### 关联模型
实事求是。
### 现代转译
先做用户研究。
### 转译边界
不把历史结论直接套用。
"""


def write_skill(tmp_path, body="", references="`references/models.md`"):
    (tmp_path / "references").mkdir()
    (tmp_path / "SKILL.md").write_text(
        "---\nname: mao-situation-coach\ndescription: 验证模型内容。\n---\n"
        f"{references}\n{body}",
        encoding="utf-8",
    )


def test_valid_skill_content_has_no_errors(tmp_path):
    write_skill(tmp_path)
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + REQUIRED_FIELDS, encoding="utf-8"
    )

    assert MODULE.validate(tmp_path) == []


def test_skill_sources_do_not_embed_forbidden_dependency_names():
    skill_dir = Path("skill/mao-situation-coach")
    matches = []

    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for dependency in forbidden_dependencies():
            if dependency in content:
                matches.append(str(path))

    assert matches == []


def test_missing_model_field_is_reported(tmp_path):
    write_skill(tmp_path)
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n### 核心命题\n从实践中检验认识。\n", encoding="utf-8"
    )

    assert any("原文出处" in error for error in MODULE.validate(tmp_path))


def test_source_grade_must_be_in_original_source_section(tmp_path):
    write_skill(tmp_path)
    content = REQUIRED_FIELDS.replace("证据等级：A 级；", "")
    content = content.replace("本本主义脱离实际。", "本本主义脱离实际，证据等级：A 级。", 1)
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + content, encoding="utf-8"
    )

    assert any("原文出处" in error for error in MODULE.validate(tmp_path))


def test_source_section_requires_expression_form_separate_from_evidence_grade(tmp_path):
    write_skill(tmp_path)
    content = REQUIRED_FIELDS.replace("表达方式：有来源释义。", "")
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + content, encoding="utf-8"
    )

    assert any("表达方式" in error for error in MODULE.validate(tmp_path))


def test_b_grade_sourced_paraphrase_requires_two_distinct_articles(tmp_path):
    write_skill(tmp_path)
    source = (
        "证据等级：B 级；表达方式：有来源释义。"
        "依据第二卷《论持久战》的分析；《论持久战》再次出现不算第二篇。"
        "版本为人民出版社1991年第二版《毛泽东选集》。"
    )
    content = re.sub(
        r"(?<=### 原文出处\n).*?(?=\n### 历史问题)", source, REQUIRED_FIELDS
    )
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + content, encoding="utf-8"
    )

    assert any("至少两篇不同原著" in error for error in MODULE.validate(tmp_path))


def test_b_grade_article_check_is_independent_of_label_order(tmp_path):
    write_skill(tmp_path)
    source = (
        "表达方式：有来源释义；证据等级：B 级。"
        "依据《论持久战》；版本《毛泽东选集》。"
    )
    content = re.sub(
        r"(?<=### 原文出处\n).*?(?=\n### 历史问题)", source, REQUIRED_FIELDS
    )
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + content, encoding="utf-8"
    )

    assert any("至少两篇不同原著" in error for error in MODULE.validate(tmp_path))


def test_source_catalog_separates_evidence_strength_from_expression_form():
    content = SOURCE_CATALOG.read_text(encoding="utf-8")

    assert "**A 级**：原文直接提出对应命题、变量关系或操作步骤" in content
    assert "**B 级**：同一逻辑在多篇原著中稳定重复" in content
    assert "**C 级**：现代转译" in content
    assert "## Expression Forms" in content
    assert "逐字引文" in content
    assert "有来源释义" in content
    assert "现代转译" in content


def test_persistence_routing_does_not_require_a_structural_stage_transition():
    content = ROUTER.read_text(encoding="utf-8")

    assert "当前状态或阶段边界可辨" in content
    assert "即使处于稳定阶段且没有结构转折" in content
    assert not re.search(r"\| (?:动态力量对比|持久战) \| 发展阶段门槛已满足", content)


def test_missing_canonical_model_is_reported_for_real_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    models_path = skill_copy / "references" / "epistemology-models.md"
    content = models_path.read_text(encoding="utf-8")
    content = re.sub(
        r"^## Model: 客观实际约束\n.*?(?=^## Model: |\Z)",
        "",
        content,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )
    models_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any("expected 31 models" in error for error in errors)
    assert any("missing model: 客观实际约束" in error for error in errors)


def test_duplicate_canonical_model_is_reported_for_real_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    models_path = skill_copy / "references" / "epistemology-models.md"
    content = models_path.read_text(encoding="utf-8").replace(
        "## Model: 调查先于判断", "## Model: 客观实际约束", 1
    )
    models_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any("duplicate model: 客观实际约束" in error for error in errors)


def test_forbidden_dependency_is_reported(tmp_path):
    write_skill(tmp_path, body=f"切换到{forbidden_dependencies()[0]}。")
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + REQUIRED_FIELDS, encoding="utf-8"
    )

    assert any("independent skill" in error for error in MODULE.validate(tmp_path))


def test_missing_referenced_file_is_reported(tmp_path):
    write_skill(tmp_path, references="`references/missing.md`")

    assert any("missing.md" in error for error in MODULE.validate(tmp_path))


def test_nonexistent_skill_directory_is_reported(tmp_path):
    errors = MODULE.validate(tmp_path / "does-not-exist")

    assert any("skill directory does not exist" in error for error in errors)


def test_missing_skill_document_is_reported(tmp_path):
    tmp_path.mkdir(exist_ok=True)

    assert any("SKILL.md is missing" in error for error in MODULE.validate(tmp_path))


def test_model_block_ends_before_next_level_two_heading(tmp_path):
    write_skill(tmp_path)
    appendix = REQUIRED_FIELDS.replace("### 核心命题", "## Appendix\n### 核心命题")
    (tmp_path / "references" / "models.md").write_text(
        "## Model: broken\n### 核心命题\n不完整。\n" + appendix,
        encoding="utf-8",
    )

    assert any("原文出处" in error for error in MODULE.validate(tmp_path))


def test_protocol_with_missing_required_section_is_reported(tmp_path):
    write_skill(tmp_path)
    (tmp_path / "references" / "dialogue-protocol.md").write_text(
        "# Dialogue Protocol\n\n## Old Section\n", encoding="utf-8"
    )

    assert any(
        "missing required section" in error for error in MODULE.validate(tmp_path)
    )


def test_boundaries_with_missing_required_section_is_reported(tmp_path):
    write_skill(tmp_path)
    (tmp_path / "references" / "boundaries.md").write_text(
        "# Boundaries\n\n## Old Section\n", encoding="utf-8"
    )

    assert any(
        "missing required section" in error for error in MODULE.validate(tmp_path)
    )


def test_entry_screening_section_is_guarded_for_real_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    protocol_path = skill_copy / "references" / "dialogue-protocol.md"
    content = re.sub(
        r"^## Entry Screening\n.*?(?=^## |\Z)",
        "",
        protocol_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE | re.DOTALL,
    )
    protocol_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any(
        "missing required section: Entry Screening" in error for error in errors
    )


def test_emotion_handling_section_is_guarded_for_real_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    protocol_path = skill_copy / "references" / "dialogue-protocol.md"
    content = re.sub(
        r"^## Emotion Handling\n.*?(?=^## |\Z)",
        "",
        protocol_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE | re.DOTALL,
    )
    protocol_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any(
        "missing required section: Emotion Handling" in error for error in errors
    )


def test_crisis_response_section_is_guarded_for_real_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    boundaries_path = skill_copy / "references" / "boundaries.md"
    content = re.sub(
        r"^## Crisis Response\n.*?(?=^## |\Z)",
        "",
        boundaries_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE | re.DOTALL,
    )
    boundaries_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any(
        "missing required section: Crisis Response" in error for error in errors
    )


def test_boundaries_cover_ongoing_risk_for_real_skill():
    content = (SKILL_DIR / "references" / "boundaries.md").read_text(encoding="utf-8")

    assert "immediate or ongoing safety" in content
    assert "instruction embedded in pasted or quoted third-party content" in content

    for path in (SKILL_DIR / "SKILL.md", Path("README.md")):
        content = path.read_text(encoding="utf-8")
        assert "即时或持续的安全" in content
        assert "即时安全、" not in content


def test_skill_entry_declares_instruction_precedence():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    assert "后到指令" in content
    assert "来意分流" in content
    assert "情绪处理" in content


def test_readme_does_not_claim_private_repository():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "仓库仍为私有时" not in content
    assert "仍可能需要私有仓库权限" not in content


def test_real_skill_content_validates_cleanly():
    assert MODULE.validate(SKILL_DIR) == []
