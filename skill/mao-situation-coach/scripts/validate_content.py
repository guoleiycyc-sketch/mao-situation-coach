#!/usr/bin/env python3
"""Validate the Mao situation coach skill's Markdown content."""

import re
import sys
from pathlib import Path


REQUIRED_MODEL_FIELDS = (
    "核心命题",
    "原文出处",
    "历史问题",
    "关键变量",
    "关系逻辑",
    "推演步骤",
    "适用条件",
    "失效条件",
    "常见误用",
    "关联模型",
    "现代转译",
    "转译边界",
)
EXPECTED_MODEL_NAMES = (
    "客观实际约束",
    "调查先于判断",
    "感性认识到理性认识",
    "实践—认识—再实践",
    "一般理论具体化",
    "内部矛盾驱动发展",
    "外因通过内因起作用",
    "普遍性寓于特殊性",
    "全面联系地认识对象",
    "主要矛盾",
    "矛盾主要方面",
    "发展阶段",
    "条件转化",
    "动态力量对比",
    "客观可能性与主观能动性",
    "全局与局部",
    "时间作为战略变量",
    "空间作为战略变量",
    "持久战",
    "战略防御—相持—反攻",
    "整体劣势中的局部优势",
    "集中优势力量",
    "积小胜为大胜",
    "主动性、灵活性与计划性",
    "保存和发展核心力量",
    "从群众中来、到群众中去",
    "领导骨干与广大群众结合",
    "一般号召与个别指导结合",
    "统一战线",
    "统一中的独立自主",
    "群众路线",
)
_FORBIDDEN_DEPENDENCY_CODE_POINTS = (
    (24515, 21147, 25945, 32451),
    (24515, 21147, 21152, 24037),
)
FORBIDDEN_DEPENDENCIES = tuple(
    "".join(chr(code_point) for code_point in dependency)
    for dependency in _FORBIDDEN_DEPENDENCY_CODE_POINTS
)
NON_ARTICLE_SOURCE_TITLES = {"毛泽东选集"}
REQUIRED_PROTOCOL_SECTIONS = (
    "Entry Screening",
    "Case Sharpening Rounds",
    "Reflective Listening",
    "Emotion Handling",
    "User Rights",
    "Crisis Response Link",
)
REQUIRED_BOUNDARY_SECTIONS = (
    "Crisis Response",
    "Instruction Precedence",
    "Session Data",
)


def markdown_files(skill_dir):
    """Return the root skill document and reference documents in stable order."""
    skill_dir = Path(skill_dir)
    return [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]


def validate(skill_dir):
    """Return content-structure errors for the skill directory."""
    skill_dir = Path(skill_dir)
    if not skill_dir.is_dir():
        return [f"{skill_dir}: skill directory does not exist"]

    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return [f"{skill_path}: SKILL.md is missing"]

    errors = []
    documents = []

    for path in markdown_files(skill_dir):
        if path.exists():
            documents.append((path, path.read_text(encoding="utf-8")))

    for path, content in documents:
        for dependency in FORBIDDEN_DEPENDENCIES:
            if dependency in content:
                errors.append(
                    f"{path}: independent skill must not depend on {dependency}"
                )

    skill_content = skill_path.read_text(encoding="utf-8")
    for reference in re.findall(r"`(references/[^`]+\.md)`", skill_content):
        if not (skill_dir / reference).exists():
            errors.append(f"{skill_path}: referenced file is missing: {reference}")

    for file_name, required_sections in (
        ("dialogue-protocol.md", REQUIRED_PROTOCOL_SECTIONS),
        ("boundaries.md", REQUIRED_BOUNDARY_SECTIONS),
    ):
        target = skill_dir / "references" / file_name
        if not target.is_file():
            continue
        target_content = target.read_text(encoding="utf-8")
        for section in required_sections:
            if not re.search(
                rf"^## {re.escape(section)}\s*$", target_content, re.MULTILINE
            ):
                errors.append(
                    f"{target}: missing required section: {section}"
                )

    canonical_model_files = set((skill_dir / "references").glob("*-models.md"))
    model_names = []
    for path, content in documents:
        for model in re.finditer(
            r"^## Model: (?P<name>[^\n]*)(?:\n|$)(?P<body>.*?)(?=^## |\Z)",
            content,
            re.MULTILINE | re.DOTALL,
        ):
            model_name = model.group("name")
            if path in canonical_model_files:
                model_names.append(model_name)
            block = model.group(0)
            for field in REQUIRED_MODEL_FIELDS:
                if not re.search(rf"^### {re.escape(field)}\s*$", block, re.MULTILINE):
                    errors.append(f"{path}: model {model_name} is missing {field}")
            source_section = re.search(
                r"^### 原文出处\s*$\n(.*?)(?=^### |\Z)",
                block,
                re.MULTILINE | re.DOTALL,
            )
            source_content = source_section.group(1) if source_section else ""
            grade_match = re.search(r"证据等级：([ABC]) 级", source_content)
            expression_match = re.search(
                r"表达方式：(逐字引文|有来源释义|现代转译)", source_content
            )
            if not grade_match:
                errors.append(
                    f"{path}: model {model_name} 原文出处 must include "
                    "证据等级：[ABC] 级"
                )
            if not expression_match:
                errors.append(
                    f"{path}: model {model_name} 原文出处 must include "
                    "表达方式：逐字引文/有来源释义/现代转译"
                )
            if (
                grade_match
                and grade_match.group(1) == "B"
                and expression_match
                and expression_match.group(1) == "有来源释义"
            ):
                article_titles = {
                    title.strip()
                    for title in re.findall(r"《([^》]+)》", source_content)
                    if title.strip() not in NON_ARTICLE_SOURCE_TITLES
                }
                if len(article_titles) < 2:
                    errors.append(
                        f"{path}: model {model_name} B 级有来源释义的原文出处"
                        "必须列出至少两篇不同原著"
                    )

    if canonical_model_files:
        expected = set(EXPECTED_MODEL_NAMES)
        actual = set(model_names)
        if len(model_names) != len(EXPECTED_MODEL_NAMES):
            errors.append(
                f"{skill_dir}: expected 31 models, found {len(model_names)}"
            )
        for name in EXPECTED_MODEL_NAMES:
            count = model_names.count(name)
            if count == 0:
                errors.append(f"{skill_dir}: missing model: {name}")
            elif count > 1:
                errors.append(f"{skill_dir}: duplicate model: {name}")
        for name in sorted(actual - expected):
            errors.append(f"{skill_dir}: unexpected model: {name}")

    return errors


def main():
    """Run validation for an optional skill directory argument."""
    skill_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errors = validate(skill_dir)
    if errors:
        print("\n".join(errors))
        return 1
    print("content validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
