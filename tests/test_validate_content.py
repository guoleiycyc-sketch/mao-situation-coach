import importlib.util
import re
import shutil
import subprocess
import sys
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
证据等级：A 级；表达方式：有来源释义。第一卷《反对本本主义》（1930年5月）；未作人民出版社1991年第二版逐字引文。
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
    (tmp_path / "references").mkdir(parents=True)
    (tmp_path / "SKILL.md").write_text(
        "---\nname: mao-situation-coach\ndescription: 验证模型内容。\n---\n"
        f"{references}\n{body}",
        encoding="utf-8",
    )


def test_valid_skill_content_has_no_errors(tmp_path):
    write_skill(tmp_path)
    models_path = tmp_path / "references" / "models.md"
    models_path.write_text(
        "## Model: 调查研究\n" + REQUIRED_FIELDS, encoding="utf-8"
    )

    documents = [(models_path, models_path.read_text(encoding="utf-8"))]
    errors, model_names = MODULE.validate_model_documents(documents, {models_path})

    assert errors == []
    assert model_names == ["调查研究"]


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


def replace_model_field_body(content, model_name, field, body):
    """Replace one field's body inside one model block, keeping the heading."""
    return re.sub(
        rf"(## Model: {model_name}\n(?:(?!## Model:)[\s\S])*?### {field}\n)"
        r"(?:(?!### |## Model: )[^\n]*\n?)*",
        lambda match: match.group(1) + body + "\n",
        content,
        count=1,
    )


def blank_model_field(content, model_name, field):
    """Blank the body of one field inside one model block, keeping the heading."""
    return replace_model_field_body(content, model_name, field, "")


def fields_with_source(source):
    """Return REQUIRED_FIELDS with the 原文出处 body replaced by source."""
    return re.sub(r"(?<=### 原文出处\n).*?(?=\n### 历史问题)", source, REQUIRED_FIELDS)


def test_model_field_with_empty_body_is_reported(tmp_path):
    write_skill(tmp_path)
    headings_only = re.sub(
        r"(?m)^(### [^\n]+)\n[^\n]+", r"\1\n", REQUIRED_FIELDS
    )
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + headings_only, encoding="utf-8"
    )

    errors = MODULE.validate(tmp_path)

    assert any("empty content for 核心命题" in error for error in errors)
    assert any("empty content for 转译边界" in error for error in errors)


def test_model_field_with_whitespace_only_body_is_reported(tmp_path):
    write_skill(tmp_path)
    content = REQUIRED_FIELDS.replace("从实践中检验认识。", "   \n\t\n")
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + content, encoding="utf-8"
    )

    errors = MODULE.validate(tmp_path)

    assert any("empty content for 核心命题" in error for error in errors)


def test_real_skill_copy_with_blank_field_body_is_reported(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    models_path = skill_copy / "references" / "strategy-models.md"
    content = blank_model_field(
        models_path.read_text(encoding="utf-8"), "动态力量对比", "转译边界"
    )
    models_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any(
        "model 动态力量对比 has empty content for 转译边界" in error for error in errors
    )


def test_minimal_skill_directory_is_rejected_as_incomplete(tmp_path):
    write_skill(tmp_path)
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + REQUIRED_FIELDS, encoding="utf-8"
    )

    errors = MODULE.validate(tmp_path)

    assert any(
        "required file is missing: dialogue-protocol.md" in error for error in errors
    )
    assert any("expected 31 models, found 0" in error for error in errors)


def test_unexpected_model_name_is_reported_for_real_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    models_path = skill_copy / "references" / "epistemology-models.md"
    content = models_path.read_text(encoding="utf-8").replace(
        "## Model: 调查先于判断", "## Model: 未登记模型", 1
    )
    models_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any("missing model: 调查先于判断" in error for error in errors)
    assert any("unexpected model: 未登记模型" in error for error in errors)


def test_missing_model_family_file_is_reported(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    (skill_copy / "references" / "strategy-models.md").unlink()

    errors = MODULE.validate(skill_copy)

    assert any(
        "required file is missing: strategy-models.md" in error for error in errors
    )
    assert any("expected 31 models, found 19" in error for error in errors)


def test_renamed_model_family_cannot_silence_completeness_check(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    for family in ("epistemology", "contradiction", "strategy", "organization"):
        source = skill_copy / "references" / f"{family}-models.md"
        source.rename(source.with_name(f"{family}-cards.md"))
    skill_doc = skill_copy / "SKILL.md"
    skill_doc.write_text(
        skill_doc.read_text(encoding="utf-8").replace("-models.md", "-cards.md"),
        encoding="utf-8",
    )

    errors = MODULE.validate(skill_copy)

    assert any(
        "required file is missing: strategy-models.md" in error for error in errors
    )
    assert any("expected 31 models, found 0" in error for error in errors)


def test_emptied_required_reference_file_is_reported(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    (skill_copy / "references" / "boundaries.md").write_text("   \n", encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any(
        "required file is empty: boundaries.md" in error for error in errors
    )


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


def write_model_with_source(tmp_path, source):
    write_skill(tmp_path)
    (tmp_path / "references" / "models.md").write_text(
        "## Model: 调查研究\n" + fields_with_source(source), encoding="utf-8"
    )


def test_a_grade_without_source_metadata_is_reported(tmp_path):
    write_model_with_source(tmp_path, "证据等级：A 级；表达方式：有来源释义。")

    errors = MODULE.validate(tmp_path)

    assert any("缺少卷次" in error for error in errors)
    assert any("缺少篇名" in error for error in errors)
    assert any("缺少写作日期" in error for error in errors)
    assert any("缺少核心版本" in error for error in errors)


def test_b_grade_verbatim_expression_still_requires_two_articles(tmp_path):
    write_model_with_source(
        tmp_path,
        "证据等级：B 级；表达方式：逐字引文。"
        "依据第一卷《实践论》（1937年7月）；人民出版社1991年第二版。",
    )

    errors = MODULE.validate(tmp_path)

    assert any("至少两篇不同原著" in error for error in errors)


def test_c_grade_cannot_be_labeled_verbatim_quotation(tmp_path):
    write_model_with_source(tmp_path, "证据等级：C 级；表达方式：逐字引文。")

    errors = MODULE.validate(tmp_path)

    assert any("C 级不能搭配表达方式 逐字引文" in error for error in errors)


def test_c_grade_cannot_be_labeled_sourced_paraphrase(tmp_path):
    write_model_with_source(tmp_path, "证据等级：C 级；表达方式：有来源释义。")

    errors = MODULE.validate(tmp_path)

    assert any("C 级不能搭配表达方式 有来源释义" in error for error in errors)


def test_modern_translation_expression_requires_c_grade(tmp_path):
    for grade in ("A", "B"):
        write_model_with_source(
            tmp_path / grade,
            f"证据等级：{grade} 级；表达方式：现代转译。",
        )

        errors = MODULE.validate(tmp_path / grade)

        assert any(
            f"{grade} 级不能搭配表达方式 现代转译" in error for error in errors
        )


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


def model_card(content, model_name):
    """Return one model card's full text block from a family document."""
    return re.search(
        rf"## Model: {re.escape(model_name)}\n.*?(?=\n## Model: |\Z)",
        content,
        re.DOTALL,
    ).group(0)


def field_section(card, field):
    """Return one field's body text inside a model card, or empty string."""
    match = re.search(
        rf"### {re.escape(field)}\n(.*?)(?=\n### |\Z)", card, re.DOTALL
    )
    return match.group(1) if match else ""


def test_composite_models_register_internal_expansion_whitelists():
    strategy = (SKILL_DIR / "references" / "strategy-models.md").read_text(
        encoding="utf-8"
    )
    organization = (SKILL_DIR / "references" / "organization-models.md").read_text(
        encoding="utf-8"
    )

    for content, model_name, mechanisms in (
        (
            strategy,
            "持久战",
            (
                "全面联系地认识对象",
                "全局与局部",
                "空间作为战略变量",
                "动态力量对比",
                "从群众中来、到群众中去",
            ),
        ),
        (
            organization,
            "群众路线",
            (
                "从群众中来、到群众中去",
                "领导骨干与广大群众结合",
                "一般号召与个别指导结合",
            ),
        ),
    ):
        expansion = field_section(model_card(content, model_name), "内部展开")

        assert expansion, f"{model_name} card must register an 内部展开 whitelist"
        assert "不计入每轮主、辅模型名额" in expansion
        assert "不得借内部展开读取未登记模型" in expansion
        for name in mechanisms:
            assert name in expansion


def test_top_level_model_counting_is_fixed_in_entry_and_router():
    skill_content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    router_content = ROUTER.read_text(encoding="utf-8")

    for content in (skill_content, router_content):
        assert "顶层模型" in content
        assert "不得借内部展开" in content


def test_principal_contradiction_does_not_presuppose_a_named_stage():
    content = (SKILL_DIR / "references" / "contradiction-models.md").read_text(
        encoding="utf-8"
    )
    principal = model_card(content, "主要矛盾")

    assert "在过程边界与当前状态范围明确的多重矛盾中" in principal
    assert "边界和阶段明确" not in principal
    assert "当前状态范围" in principal
    assert "阶段命名是主要矛盾判断的输出之一，不是其前提" in principal


def test_stage_naming_is_output_of_principal_contradiction_analysis():
    content = (SKILL_DIR / "references" / "contradiction-models.md").read_text(
        encoding="utf-8"
    )
    stage = model_card(content, "发展阶段")

    assert "阶段命名是主要矛盾判断的输出之一，不是其前提" in stage


def test_router_default_order_matches_state_range_threshold():
    content = ROUTER.read_text(encoding="utf-8")

    assert "在同一过程和当前状态范围内比较已成立的候选矛盾" in content
    assert "在同一过程和阶段内" not in content


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


def test_power_imbalance_screening_section_is_guarded_for_real_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    boundaries_path = skill_copy / "references" / "boundaries.md"
    content = re.sub(
        r"^## Power Imbalance Screening\n.*?(?=^## |\Z)",
        "",
        boundaries_path.read_text(encoding="utf-8"),
        flags=re.MULTILINE | re.DOTALL,
    )
    boundaries_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any(
        "missing required section: Power Imbalance Screening" in error
        for error in errors
    )


def test_boundaries_cover_power_imbalance_screening_for_absent_third_parties():
    boundaries_content = (SKILL_DIR / "references" / "boundaries.md").read_text(
        encoding="utf-8"
    )

    assert "## Power Imbalance Screening" in boundaries_content
    assert "not present in this conversation" in boundaries_content
    assert "one the absent third party could review" in boundaries_content
    assert "informed consent, fair process, or legitimate duty" in boundaries_content

    protocol_content = (SKILL_DIR / "references" / "dialogue-protocol.md").read_text(
        encoding="utf-8"
    )
    assert "Power Imbalance Screening" in protocol_content
    assert "和 TA 本人核对过" in protocol_content


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


def test_real_skill_copy_with_renamed_field_heading_is_reported(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    models_path = skill_copy / "references" / "strategy-models.md"
    content = re.sub(
        r"(## Model: 动态力量对比\n(?:(?!## Model:)[\s\S])*?)### 转译边界\n",
        r"\1### 转译边界（旧）\n",
        models_path.read_text(encoding="utf-8"),
        count=1,
    )
    models_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any(
        "model 动态力量对比 is missing 转译边界" in error for error in errors
    )


def test_real_skill_copy_with_illegal_source_combo_is_reported(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    models_path = skill_copy / "references" / "strategy-models.md"
    content = replace_model_field_body(
        models_path.read_text(encoding="utf-8"),
        "动态力量对比",
        "原文出处",
        "证据等级：C 级；表达方式：逐字引文。",
    )
    models_path.write_text(content, encoding="utf-8")

    errors = MODULE.validate(skill_copy)

    assert any("C 级不能搭配表达方式 逐字引文" in error for error in errors)


def test_local_card_sample_and_full_package_use_distinct_checks(tmp_path):
    write_skill(tmp_path)
    models_path = tmp_path / "references" / "models.md"
    models_path.write_text(
        "## Model: 调查研究\n" + REQUIRED_FIELDS, encoding="utf-8"
    )
    documents = [(models_path, models_path.read_text(encoding="utf-8"))]

    local_errors, model_names = MODULE.validate_model_documents(
        documents, {models_path}
    )
    full_errors = MODULE.validate(tmp_path)

    assert local_errors == []
    assert model_names == ["调查研究"]
    assert any("required file is missing" in error for error in full_errors)


def test_script_entry_agrees_with_default_test_validation():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)], capture_output=True, text=True
    )

    assert result.returncode == 0
    assert "content validation passed" in result.stdout


def test_script_entry_rejects_corrupted_skill_copy(tmp_path):
    skill_copy = tmp_path / "mao-situation-coach"
    shutil.copytree(SKILL_DIR, skill_copy)
    models_path = skill_copy / "references" / "strategy-models.md"
    models_path.write_text(
        blank_model_field(
            models_path.read_text(encoding="utf-8"), "动态力量对比", "转译边界"
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(skill_copy)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "empty content for 转译边界" in result.stdout
