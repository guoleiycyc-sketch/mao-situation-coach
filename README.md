# 毛选教练（Mao Situation Coach）

> 帮助使用者看清复杂现实局面，而不是替使用者给答案。

毛选教练是一个可独立运行的 Skill（支持 Codex 与 Claude Code），能够在自身目录内完成信息入口、整理、分析与收束。它把历史文本中的认识方法整理为有条件、有证据边界的现代局面分析工具，帮助使用者区分事实与解释、看见关系和变化，并保留可被新证据修正的判断。

## 它解决什么问题

当事实、转述、解释和愿望混在一起，问题往往不是“缺一个结论”，而是尚未形成一张可靠的局面图。毛选教练适合协助梳理：

- 事情到底发生了什么，哪些仍未核实；
- 多个参与者、资源、限制和结果如何相互影响；
- 当前真正阻塞判断的中心、阶段或力量变化是什么；
- 应该继续观察什么，哪些事实会推翻暂时判断；
- 何时已有条件讨论行动，何时必须停在“尚不可判断”。

默认产出是可持续校正的**动态局面图**，不是裁决或定论，也不是把某个模型名当成确定答案。

## 核心原则

- **先调查，后判断**：不发明事实、动机、数据、期限或确定性。
- **分清认识层次**：把陈述分别标为已确认事实、他人转述、使用者解释、预测或假设、感受和愿望。
- **最小模型路由**：每轮最多使用 1 个主模型和 1 个辅助模型，只处理当前最先阻塞判断的认知障碍。
- **门槛先于结论**：信息门槛不足时，指出缺口、冲突证据和不同结果将如何改变判断，而不是强行套模型。
- **判断与行动分开**：仅当使用者明确要求，且相关模型的信息门槛满足时，才提供条件式行动、调查、验证或决策建议。
- **切换须经确认**：先说明新证据、切换理由及结论范围的变化，征得使用者同意后再更换模型。
- **普通语言优先**：先说清发生了什么、为什么暂时这样看、还不知道什么，再标注模型和来源。
- **现代边界明确**：普通人际、职业、用户、组织、合作或竞争关系不用敌我、消灭、歼灭、战争、根据地或阵营类语言。

详细执行约束见 [Skill 入口](skill/mao-situation-coach/SKILL.md) 与 [安全边界](skill/mao-situation-coach/references/boundaries.md)。

## 方法论结构

Skill 包含四个模型族、共 31 个模型。下面仅列名称；模型的命题、适用条件、失效条件、证据与转译边界以仓库中的模型卡为准。

1. **认识论（5）**：客观实际约束、调查先于判断、感性认识到理性认识、实践—认识—再实践、一般理论具体化。
2. **矛盾分析（8）**：内部矛盾驱动发展、外因通过内因起作用、普遍性寓于特殊性、全面联系地认识对象、主要矛盾、矛盾主要方面、发展阶段、条件转化。
3. **战略分析（12）**：动态力量对比、客观可能性与主观能动性、全局与局部、时间作为战略变量、空间作为战略变量、持久战、战略防御—相持—反攻、整体劣势中的局部优势、集中优势力量、积小胜为大胜、主动性、灵活性与计划性、保存和发展核心力量。
4. **组织方法（6）**：从群众中来、到群众中去、领导骨干与广大群众结合、一般号召与个别指导结合、统一战线、统一中的独立自主、群众路线。

[模型路由器](skill/mao-situation-coach/references/model-router.md)依据认知障碍而非关键词选择模型，包含 10 条确定性分支：

1. 事实与判断混在一起；
2. 多个问题相互作用；
3. 中心或阶段无法确定；
4. 不清楚变化原因；
5. 不知道坚持还是调整；
6. 资源稀缺、任务过多；
7. 多方利益或合作边界复杂；
8. 管理层与一线脱节；
9. 计划没有落实；
10. 判断反复失败。

默认分析次序是：事实可靠性 → 关系结构 → 主要矛盾 → 阶段 → 力量趋势 → 可改变条件。前序证据不足时不会为了形式完整而强行走完后续步骤。

## 一次讨论如何进行

1. **进入问题**：信息稀少时，从 5 个核心问题开始——最想看清什么、发生了什么、涉及谁及其利益与资源、有哪些不同判断、做过什么及结果如何。使用者已经说过的信息不会重复询问。
2. **定向补充**：核心五问之外，根据问题结构最多增加 2 个定向问题；此后每轮只问 1—2 个最能推翻判断或区分竞争假设的问题。
3. **建立底图**：对陈述分类，并检查问题对象、时间线、关键事实、参与者、力量与条件、行动与反馈六个维度。
4. **选择模型**：先复述问题、证据与不确定性，再按认知障碍选择本轮 1 个主模型；只有第二个独立缺口会直接改变结论时，才加入 1 个辅助模型。
5. **动态更新**：关键事实、关系、阶段或模型改变后更新局面图；每 2—4 轮做阶段小结。切换模型前解释原因、影响并等待确认。
6. **收束复盘**：当局面已较清楚、继续判断需要新证据、使用者希望暂停或触及边界时，以动态局面图和方法复盘结束。

完整对话规则见 [Dialogue Protocol](skill/mao-situation-coach/references/dialogue-protocol.md)。

## 输出长什么样

一次阶段性输出通常包含：

- 当前问题及过程边界；
- 陈述与证据分层；
- 参与者的利益、资源、限制、依赖和影响；
- 竞争假设及各自的支持证据、反对证据、缺失证据和判别信息；
- 矛盾结构、阶段与力量趋势；
- 可能改变局面的条件；
- 当前较有把握、暂时倾向、证据不足和仍然未知的部分；
- 本轮主模型、辅助模型的有限用途、来源、证据等级和表达方式；
- 哪些反证或现实反馈会促使判断更新。

收束时还会说明本次如何分层信息、为何选择或不选择某个模型，帮助使用者带走可复用的思考方法。

## 适用场景

- 创业或产品方向很多，不清楚哪些是真需求、哪些只是机会噪声；
- 团队协作、组织推进或跨方合作中，信息、利益和执行反馈相互矛盾；
- 长期投入已经产生部分反馈，但尚不确定应坚持、调整还是停止；
- 资源有限、任务过多，需要先看清全局价值、依赖与底线能力；
- 对同一事件存在多种解释，想用证据区分假设而非凭感觉选答案；
- 希望对一段复杂经历做多轮、可修正的结构化复盘。

## 不适用与安全边界

- 它不是法律、医疗、心理、财务、安全或其他专业服务，不能替代现实世界的合格支持。
- 出现即时或持续的安全、医疗、心理危机、法律、财务、伦理或权利风险时，应停止常规模型推演，先处理相应现实风险。
- 不支持以历史概念为普通关系贴敌我标签，也不支持操纵、胁迫、歧视或伤害他人。
- 不会用“主要矛盾”等术语合理化牺牲健康、安全、伦理或权利。
- 信息不足、候选解释无法区分、过程边界不明或继续调查会造成不可接受风险时，不给确定判断。
- 历史含义、模型抽象和现代转译必须分开；模型是组织认识的工具，不是永恒定律或确定答案。

更完整的停止条件与专业边界见 [安全边界](skill/mao-situation-coach/references/boundaries.md)。

## 使用示例

在 Codex 或 Claude Code 中安装后，直接用自然语言描述局面，例如：

```text
请用毛选教练帮我梳理这个局面：我们有三个潜在产品方向，团队对用户需求的判断彼此冲突。我不想马上选方向，想先分清哪些是事实、哪些是假设，以及还缺什么证据。
```

也可以明确限制本轮目标：

```text
先不要给行动建议。请帮我画出动态局面图，并指出最可能推翻当前判断的两个问题。
```

如果希望讨论行动，需要主动说明：

```text
如果现有信息已经达到相关模型的门槛，请给我条件式选项、风险边界和停止条件；如果没有，请只指出缺失证据。
```

## 示范对话（节选）

下面是一段按对话协议写成的示意文本（非真实会话记录），展示几个关键装置：开场不预置判断并告知权利、陈述分层复述、每轮至多两个追问、竞争假设并列、信息不足时不设主模型、先白话后标注模型与证据等级。场景承接上面的例子：三个方向之争。

**使用者：**

我们是个五人小团队，做小商户经营工具。现在卡在三个方向上：A 是给现有老客户做深度定制，有三家老客户反复提需求；B 是做一个面向更多商户的自助版产品，创始人认为这个市场大；C 是接一个熟人介绍的外包项目先回血。上周开会讨论了一次，没有结论。我自己的感觉是 B 可能是伪需求，但拿不出证据；同事觉得我太保守。账上现金按现在的支出还能撑十个月左右。我不想马上拍板，想先把哪些是事实、哪些只是猜测分清楚。

**教练：**

我们先不急着在这三个方向里做选择。按流程，我需要先把事实、你的理解和真正的未知分开，再谈判断。

先说明你的两项权利：一、你可以在任何环节随时暂停或中止，已说的内容只用于本次对话的分析；二、你可以随时更正给过的事实、撤回某个解释，或否决我对局面的归纳——下面每次复述后的确认，就是为纠错而设的。

我先复述一遍。听起来这几个月你一边扛着现金流的约束，一边要在几种意见之间拿主意——你现在最想弄清的是：这三个方向里，哪些判断有事实支撑，哪些还只是猜测。具体分层：

- 已确认事实：五人团队；三家老客户反复提出深度定制需求；上周开会没有达成结论；按当前支出，现金约可支撑十个月。
- 他人转述：创始人认为自助版面向的市场大——这目前是创始人本人的判断，还未经过独立验证。
- 你目前的理解是：B 可能是伪需求；你也说明了自己目前拿不出证据。
- 感受：被同事评价为“保守”带来压力；你不想在信息分清之前拍板。

以上复述有偏差吗？另外补两个当前还缺的信息：

1. 三个方向各自做过什么尝试，实际结果如何？
2. 它们要解决的是同一个问题吗——找下一个增长点，还是先解决现金流？

本轮不设分析模型：底图还没经你确认，流程是先建底图、后选模型。

**使用者：**

复述没有偏差。补一下：A 上个月给其中一家老客户做过一次两周的小定制，交付后一直在用，上周还问下季度能不能继续；B 今年初上过一个介绍页，留下联系方式的有 137 个，真正注册试用的不到 10 个，后来没再推进；C 完全没试过，只是那个熟人一直在催。要说解决什么问题——A 和 B 都是找增长点，C 只是回血。

**教练：**

底图更新：A 有了一项实践反馈（一家客户的定制持续在用并主动询问续期）；B 有一次低转化记录（留资 137、试用不足 10）；C 没有尝试记录。“创始人认为市场大”与“B 转化弱”目前是并存的材料，还不能相互否定。

围绕“B 是不是伪需求”，目前有两个都能解释现有材料的假设，先并列保留：

```text
假设一：自助版没有真实需求
├── 支持证据：留资 137、试用不足 10，转化很低
├── 反对证据：留资数量本身不算小，说明有人被吸引
├── 缺失证据：留资商户是谁、出于什么动机留下联系方式
└── 能区分该假设与其他假设的关键信息：留资商户后续的实际行为

假设二：需求存在，但介绍页或产品入口没有匹配到目标商户
├── 支持证据：留资数量不低，来源可以被追溯
├── 反对证据：试用者无一推进使用
├── 缺失证据：试用者在哪里停下、为什么停
└── 能区分该假设与其他假设的关键信息：试用流失的具体环节和原因
```

本轮只问两个问题，都用于区分上面两个假设：

1. 137 个留资的商户，你们了解他们的构成吗——规模、行业、从哪里找到介绍页？
2. 试用的用户停在哪一步——注册后没有配置，还是配置后没有再用？

本轮仍不设主模型：两个解释目前依赖同一批数据，缺的是能区分它们的独立证据；按流程停在这一环，不用模型名填补空白。

**使用者：**

查了下记录：留资的大半不是老客户那种小店，是规模稍大的连锁门店，多数是从一篇行业文章找过来的。试用的几个全卡在第一步——产品要求先绑定他们的收银系统，多数人说太麻烦，就没下文了。

**教练：**

先说结论，注明确定程度：暂时倾向假设二——市场里有商户对这类工具感兴趣，但“先绑定收银系统”的入口把其中最积极的一批挡在了门外。依据是两条相互独立的材料：留资者画像（连锁门店为主、来源可溯）与试用者的卡点（全部停在绑定一步）。“B 是伪需求”目前证据不足。

这个判断可以被推翻：

- 如果换一种更轻的接入方式后，留资商户仍不愿试用，“没有真实需求”的解释会明显增强；
- 如果连锁门店愿意为省掉绑定麻烦支付额外费用，“入口太重”会进一步坐实。

另外，A 方向的定制反馈回答的是“老客户愿不愿付费加深”，不回答“陌生市场有没有需求”——两个判断先不要合并。三个方向如何排序，需要现金净消耗与各方向反馈节奏的证据，现在还不齐；够格讨论时我会先说明理由、征得你确认后再引入相应模型。

主模型：客观实际约束；来源：第一卷《反对本本主义》（1930年5月）与《实践论》（1937年7月）综合归纳；证据等级：B 级；表达方式：有来源释义。本轮无辅助模型：判别信息刚到位，一个模型足够组织本轮判断。

对话到此为节选。真实使用中，后续每轮仍只保留 1 个主模型和至多 1 个辅助模型，每 2—4 轮做阶段小结，收束时输出动态局面图与方法复盘；切换模型前会先说明理由并等待确认。

## 安装

仓库地址为 `https://github.com/guoleiycyc-sketch/mao-situation-coach`（已公开），Skill 位于 `skill/mao-situation-coach` 子目录，可直接克隆或让 Codex 安装。使用 Codex 的按方式一或方式二安装；使用 Claude Code 的见下方[安装到 Claude Code](#安装到-claude-code)一节。

**前置条件**：macOS / Linux 与 `bash`；`git`；`python3`（「验证安装」需要——裸 macOS 没有该命令时，先运行 `xcode-select --install` 装 Command Line Tools）。安装脚本里的 `CODEX_HOME` 是 Codex 的主目录变量，默认取 `$HOME/.codex`，skill 会装到它下面的 `skills/` 里；只有你的 Codex 数据目录不在默认位置时才需要设置它。

### 方式一：让 Codex 从 GitHub 安装

在 Codex 中原样发送：

```text
请从 https://github.com/guoleiycyc-sketch/mao-situation-coach 的 skill/mao-situation-coach 子目录安装这个 Skill。
```

装完建议运行下方「验证安装」的完整代码块自证一次（它会确认入口文件、结构校验与内容验证器全部通过）。如果 Codex 端安装失败或不可用，改用方式二手动安装，效果相同。

### 方式二：手动安装

先 `cd` 到你想长期存放代码的目录（这个克隆目录以后「更新」时还要用到，不要放在临时位置），然后复制下面整个代码块，并把它作为一个单元运行。子 shell 启用 fail-fast；`git clone` 或 `cd` 失败时不会继续复制，目标已存在时也会明确停止：

```bash
(
  set -eu
  git clone https://github.com/guoleiycyc-sketch/mao-situation-coach.git
  cd mao-situation-coach
  CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
  TARGET="$CODEX_ROOT/skills/mao-situation-coach"
  if [ -e "$TARGET" ]; then
    echo "安装目标已存在：$TARGET" >&2
    echo "请先备份或按更新步骤处理，已停止安装。" >&2
    exit 1
  fi
  mkdir -p "$CODEX_ROOT/skills"
  cp -R skill/mao-situation-coach "$TARGET"
)
```

这是一段完整的脚本流程：已有目标会明确报错并以非零状态停止，不会继续复制或产生嵌套目录。请不要删除终止分支；需要替换已有安装时，按“更新”章节先备份或移走旧目录。

### 安装到 Claude Code

Claude Code 使用同样的 Skill 包，目标目录是 `~/.claude/skills/mao-situation-coach/`。Claude Code 按目录内的 `SKILL.md` 发现技能，文件放好后即可使用，无需额外注册步骤。它安装到独立目录，与按方式二装入 Codex 的副本互不影响，可以并存。

首次安装时，复制下面整个代码块并作为一个单元运行（说明与方式二相同：子 shell 启用 fail-fast，`git clone` 或 `cd` 失败时不会继续复制，目标已存在时会明确停止）。已按方式二克隆过仓库的，把前两行换成进入那个克隆目录，再运行其余部分——更新时还需要它：

```bash
(
  set -eu
  git clone https://github.com/guoleiyc-sketch/mao-situation-coach.git
  cd mao-situation-coach
  TARGET="$HOME/.claude/skills/mao-situation-coach"
  if [ -e "$TARGET" ]; then
    echo "安装目标已存在：$TARGET" >&2
    echo "请先备份或按更新步骤处理，已停止安装。" >&2
    exit 1
  fi
  mkdir -p "$HOME/.claude/skills"
  cp -R skill/mao-situation-coach "$TARGET"
)
```

装完运行下面的代码块自证一次。它与「验证安装」是同一套流程，只是目标目录换成 Claude Code 的路径：

```bash
(
  set -eu
  TARGET="$HOME/.claude/skills/mao-situation-coach"
  export TARGET
  test -f "$TARGET/SKILL.md"
  python3 - <<'PY'
import os
import re
from pathlib import Path

target = Path(os.environ["TARGET"])
skill = target / "SKILL.md"
content = skill.read_text(encoding="utf-8")
assert content.startswith("---\n"), "SKILL.md must begin with frontmatter"
frontmatter = content.split("---\n", 2)[1]
assert re.search(r"^name:\s*mao-situation-coach\s*$", frontmatter, re.MULTILINE), "unexpected skill name"
references = re.findall(r"`(references/[^`]+\.md)`", content)
missing = [reference for reference in references if not (target / reference).is_file()]
assert references, "SKILL.md does not mention any reference files"
assert not missing, f"missing referenced files: {missing}"
print("quick structure validation passed")
PY
  python3 "$TARGET/scripts/validate_content.py" "$TARGET"
)
```

更新与卸载沿用「更新」「卸载」两章的完整流程，只把其中定义 `CODEX_ROOT` 与 `TARGET` 的两行换成：

```bash
TARGET="$HOME/.claude/skills/mao-situation-coach"
```

其余行为不变：更新仍在当初的克隆目录内运行并留下带时间戳的备份；卸载同样要求输入 `DELETE` 确认，备份目录的清理路径按同样方式替换。

## 验证安装

复制下面整个代码块，并把它作为一个单元运行。它会定位实际安装目录，确认入口文件存在，检查 frontmatter、名称和入口引用，最后运行安装包自带的内容验证器：

```bash
(
  set -eu
  CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
  TARGET="$CODEX_ROOT/skills/mao-situation-coach"
  export TARGET
  test -f "$TARGET/SKILL.md"
  python3 - <<'PY'
import os
import re
from pathlib import Path

target = Path(os.environ["TARGET"])
skill = target / "SKILL.md"
content = skill.read_text(encoding="utf-8")
assert content.startswith("---\n"), "SKILL.md must begin with frontmatter"
frontmatter = content.split("---\n", 2)[1]
assert re.search(r"^name:\s*mao-situation-coach\s*$", frontmatter, re.MULTILINE), "unexpected skill name"
references = re.findall(r"`(references/[^`]+\.md)`", content)
missing = [reference for reference in references if not (target / reference).is_file()]
assert references, "SKILL.md does not mention any reference files"
assert not missing, f"missing referenced files: {missing}"
print("quick structure validation passed")
PY
  python3 "$TARGET/scripts/validate_content.py" "$TARGET"
)
```

## 更新

复制下面整个代码块，并把它作为一个单元运行。**运行前提**：脚本第一行 `cd mao-situation-coach` 是相对路径——请在当初用方式二克隆仓库的位置运行；用方式一安装、本地没有克隆的客户，更新时请先按「卸载」移除旧目录，再按「安装·方式二」重装最新版。`cd` 和 `git pull --ff-only` 都在移动旧安装之前执行；任一步失败，子 shell 都会立即停止。更新成功时会保留一个带时间戳的备份，并拒绝覆盖同名备份：

```bash
(
  set -eu
  cd mao-situation-coach
  git pull --ff-only
  CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
  TARGET="$CODEX_ROOT/skills/mao-situation-coach"
  BACKUP="$TARGET.backup.$(date +%Y%m%d%H%M%S)"
  if [ ! -e "$TARGET" ]; then
    echo "没有找到旧安装：$TARGET" >&2
    exit 1
  fi
  if [ -e "$BACKUP" ]; then
    echo "备份目标已存在：$BACKUP" >&2
    exit 1
  fi
  mv "$TARGET" "$BACKUP"
  cp -R skill/mao-situation-coach "$TARGET"
)
```

更新后重新运行“验证安装”中的完整流程。确认新版本可用后，再自行决定是否删除备份。

## 卸载

卸载目标由当前 Codex 根目录确定：

```text
${CODEX_HOME:-$HOME/.codex}/skills/mao-situation-coach
```

下面是删除操作，会移除计算出的精确 `TARGET` 及其中全部内容，且不能通过本仓库恢复未备份的本地修改。复制整个代码块并把它作为一个单元运行；先核对脚本显示的路径，只有明确输入 `DELETE` 才会执行删除：

```bash
(
  set -eu
  CODEX_ROOT="${CODEX_HOME:-$HOME/.codex}"
  TARGET="$CODEX_ROOT/skills/mao-situation-coach"
  echo "即将删除：$TARGET" >&2
  printf '确认删除请输入 DELETE：' >&2
  IFS= read -r CONFIRM
  if [ "$CONFIRM" != "DELETE" ]; then
    echo "未确认，已取消卸载。" >&2
    exit 1
  fi
  rm -rf -- "$TARGET"
)
```

卸载只删除 `TARGET` 本身；「更新」留下的备份目录（`mao-situation-coach.backup.<时间戳>`）不会被一并清理，确认不再需要时请手动删除：

```bash
rm -rf -- "${CODEX_HOME:-$HOME/.codex}"/skills/mao-situation-coach.backup.*
```

## 仓库结构

```text
.
├── README.md                         # 项目介绍、安装与使用指南
├── ATTRIBUTION.md                    # 引用与来源说明
├── LICENSE                           # 许可证
├── skill/
│   └── mao-situation-coach/          # 可安装的独立 Skill
│       ├── SKILL.md                  # 执行入口
│       ├── agents/                   # Codex 展示元数据
│       ├── references/               # 路由、模型卡、对话、来源与边界
│       └── scripts/                  # 内容验证器
├── tests/                            # 自动化测试与行为案例
└── evals/                            # 发布后行为回归：单轮判卷、对抗用例与量规
```

关键文件：

- [Skill 入口](skill/mao-situation-coach/SKILL.md)
- [模型路由器](skill/mao-situation-coach/references/model-router.md)
- [对话协议](skill/mao-situation-coach/references/dialogue-protocol.md)
- [来源目录](skill/mao-situation-coach/references/source-catalog.md)
- [安全边界](skill/mao-situation-coach/references/boundaries.md)
- [行为案例](tests/mao-situation-coach-cases.md)
- [内容验证器](skill/mao-situation-coach/scripts/validate_content.py)

## 开发与测试

仓库当前有 **50 项自动化测试**，提供 5 组多轮行为案例与 16 组行为 eval 用例（单轮 9 + 对抗 7）；内容验证器检查 **31 个模型**，路由器定义 **10 条认知障碍分支**。

从仓库根目录创建隔离环境、安装测试工具并运行 50 项自动化测试：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest -q
```

内容验证器只使用 Python 标准库，无需额外安装依赖：

```bash
python3 skill/mao-situation-coach/scripts/validate_content.py skill/mao-situation-coach
```

行为案例及其验收点见 [tests/mao-situation-coach-cases.md](tests/mao-situation-coach-cases.md)。新增或修改模型时，应保持模型字段完整、来源等级与表达方式分离、路由门槛明确，并补充相应测试。

## 证据与引用原则

证据强度与表达形式是两个不同维度，不能混为一谈。

**证据强度：**

- **A 级**：原文直接提出对应命题、变量关系或操作步骤；可用逐字引文，也可用有来源释义。
- **B 级**：同一逻辑在多篇原著中稳定重复后形成的综合判断；必须列出相互支持的篇目，不能伪装成某一篇的原句。
- **C 级**：面向现代情境的转译工具，只用于帮助理解或操作，不表述为原著概念、术语或结论。

**表达形式：**

- **逐字引文**：必须按核心版本逐字核验，只支持引文直接陈述的命题。
- **有来源释义**：明确标注卷次、篇名和日期的概括或重述，并明确它不是逐字引文。
- **现代转译**：当代工具语言，必须保留适用条件与边界，不冒充原文或历史结论。

引文不能代替对当前现实的调查，一条引文的等级也不会自动传递给由它延伸出的相关结论。版本政策、篇目登记和完整规则见 [Source Catalog](skill/mao-situation-coach/references/source-catalog.md)。

## 当前状态

当前成熟度：**可测试版本**。

现阶段已有完整 Skill 入口、四族 31 个模型、10 条路由、对话协议、边界、来源目录、50 项自动化测试、行为案例与行为 eval 套件。仓库已公开。接口、文案和模型卡在 1.0 之前仍可能调整，请以当前版本的验证结果和 Git 历史为准。

## 引用与来源说明

本项目的方法论与对话工艺有明确的来源谱系：《毛选》引用与版本政策、对话工艺出处、姊妹项目与许可声明，统一见 [ATTRIBUTION.md](ATTRIBUTION.md)。

## License

本项目使用 **MIT License**。在保留许可证及版权声明的条件下，可以使用、复制、修改和分发本项目；软件按“原样”提供，不附带任何明示或默示担保，作者或版权持有人不对使用本软件产生的索赔、损害或其他责任负责。完整条款见仓库根目录 `LICENSE` 文件。

本项目不声称获得任何官方机构、出版方或历史人物的背书。
