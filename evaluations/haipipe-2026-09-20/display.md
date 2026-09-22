# HAI-Pipe Toolkit Display 技能评估

评估日期：2026-09-20

## 快照、范围与限制

- 当前 HEAD：f9a8f0b8e8941f23a1c0b5a8a45d2780a756f217，与 BRIEF.md 所列基线一致。
- 当前 Display 技能目录无工作树改动。工作区其余部分有并行改动：references/cite-guard、grant-writer-skills、paper-rag-skill、paperspine、reprorun、research-agent-skills、research-co-pilot、scipilot-figure-skill。evaluations/haipipe-2026-09-20/ 是已有的未跟踪评估材料；本次只新增指定的 display.md。
- 初始清单的 10 份现行 SKILL.md 均存在。_todo/ 下另有四套海报/幻灯片技能，家族 README 明确标为已退休并停放，故不计入现行清单。
- 本文是静态文档评估。没有执行所审技能、脚本、外部服务或测试。使用场景是桌面走查，不是实时用户测试，也不代表已观察运行行为。
- html-ppt 是 MIT 上游 vendored runtime。评估覆盖技能说明、README、参考说明和模板交互文案；CSS、动画模块、字体与第三方实现只在核对文案含义时抽查，不作完整代码审计。

## 总体判断

Display 的基本职责划分值得保留：一个入口按类型路由到五个 renderer；数据与概念图分开；输入快照、recipe、候选稿、胜出资产和人类验收各自有归属。值得保留的例子包括：display-unit-agent 明确要求生产者不要给自己的 claim 背书，且不代替人勾选 accepted；icon-to-svg 也说明自动评分不能代替视觉检查。

目前最妨碍可靠执行的问题是写入位置和共享契约已经分叉。Page 现行契约将 payload 放在 Result 下，而 Display 多份文件仍指导写入 Page 已弃用的目录，另一个 agent 收据又使用第三种目录。TeX 不能由当前 intake 模板声明；概念图数字规则互相冲突；若干范例命令与脚本签名不一致，表格示例甚至会输出假的 Observations=0。用户还需要知道何时看候选、谁批准构图、谁决定晋升；部分技能把评分阈值写成“接受”条件，却未将评分与人的决定分开。

### 值得保留的写法

- display/README.md:7-20 用一张短图交代 door、五个 renderer、共享合约、转换器与 vendored runtime 的关系。
- haipipe-display/SKILL.md:15-31 的按种类路由表易扫读，且说明数据 renderer 与概念 renderer 的区别。
- agents/haipipe-display-unit-agent.md:81-119 将缺少 Intake 作为 HOLD、禁止二次拉取、生产者不能评估自己的 claim 写得具体。
- figure-to-svg/SKILL.md:198-200 与 icon-to-svg/SKILL.md:83-90 均指出分数不是签收依据；fresh-eyes 检视有助于降低自我确认偏误。

## 覆盖清单

| 现行技能 | 完整阅读的主说明 | 支持材料及交互文案 | 范围外或未逐项审阅 |
|---|---|---|---|
| figure-to-svg | SKILL.md | fn/lesson.md、feedback.md、digest.md；sam_optional.md；legacy-crop-path.md 状态；lesson 13、14、16 和相关反馈；grid/slice/compose 等被文档调用脚本 | 旧 lesson 档案未逐份通读；已退休 crop 流程仅确认退休标记；未执行脚本 |
| haipipe-display | SKILL.md | display/README.md、两个共享合约、Page-side evidence 合约、Paper assembler 写入说明 | 外部 Paper 工具不在 Display 主技能清单 |
| haipipe-display-diagram | SKILL.md | FigureSpec 示例、renderer 入口与 feedback README/当前条目；与 Mermaid 的路由关系 | 不执行渲染；不作 SVG 渲染器代码审计 |
| haipipe-display-figure | SKILL.md | intake/output 合约、feedback README/条目、输入与导出说明 | 不执行示例图脚本 |
| haipipe-display-illustration | SKILL.md | feedback README 与两条历史反馈；paper_illustration_image2.py 中 preflight/finalize 行为 | 不调用 Codex image bridge；历史反馈不是当前运行证据 |
| haipipe-display-table | SKILL.md | feedback README、表格生成和质量审阅示例 | 不执行 Python 或 TeX 范例 |
| haipipe-display-tex | SKILL.md | 共享 unit contract；TeX 双编译与 asset/float 说明 | SKILL 指向的旧工作单元未作为当前规范逐个审计 |
| html-ppt | SKILL.md | README.md、README.zh-CN.md、全部 6 篇 references、15 个 full-deck README、主题及 full-deck 展示页、基础 deck 和 cover/gantt/timeline 示例、脚手架与 PNG 导出脚本、讲者备注相关 runtime/CSS | vendored 主题、动画资产和第三方实现未完整审计 |
| html-to-svg | SKILL.md | figure-to-svg Lesson 16、HTML SVG/PDF/PPTX 构建器及相应脚本接口；与 html-ppt 的导出关系 | 文档所列的 REACH-SPACE collaborations 示例路径在当前工作区不存在 |
| icon-to-svg | SKILL.md | compare、score、center 脚本入口及其检查说明；由 figure-to-svg 子图使用的方式 | 不运行图像评分或导出 |

另完整阅读了 display/ref/display-intake-contract.md、display-unit-output-contract.md、intake-manifest.template.yaml、agents/haipipe-display-unit-agent.md 及 display/README.md。各子技能 CHANGELOG 与 dated feedback 是历史材料，不作为当前行为证据；仅在现行 SKILL.md 引用它们或需判断材料是否仍生效时抽查。assets/ 视为依赖，未逐个审核。初始 10 项全部覆盖；没有遗漏的现行 SKILL.md。

## 优先发现

### P1 — Page Display 的写入位置在 Display、Page 与 Paper 文档间冲突

现行 Display door 说：

> display/haipipe-display/SKILL.md:74-80：“A BOARD PAGE's unit lands at <page>/outline/evidence/display/...”

intake 合约也把 Local Input 写到旧路径（display/ref/display-intake-contract.md:104-118）；unit-agent 收据却变成：

> display/agents/haipipe-display-unit-agent.md:124：“unit: <page>/display/<stem>-Display<N>-<slug>/”

当前 Page evidence 文档规定 Result payload 在 <page>/results/<re-run>/payload/<unit>/（page/haipipe-workbench-page/ref/evidence/displays.md:16-24），并明确 outline/evidence/display 和 flat display 都已退休（同文件:180-185）。但 Paper assembler 仍声明旧目录是当前 Section Page 的入口（paper/haipipe-paper-assemble/SKILL.md:69-78、221-235）。这是跨家族协议尚未统一，不宜只在 Display 文件中任意挑一个路径替换。

**影响：**Page producer 可照 Display/agent 说明写出文件，但现行 Page reader 看不到它；Paper 的旧读取器又和 Page Result 新地址争夺写入权。新上下文 agent 没有可信唯一目标。

**建议：**先由 Page、Paper、Display 所有者统一 canonical 地址、Result envelope 与 renderer 输入路径，再更新 door、intake contract、agent 收据、adapters 和构建说明。若当前文档无法给出一致地址，技能应 HOLD 并报告冲突来源。

**English before / after：**

> Before: “A BOARD PAGE's unit lands at <page>/outline/evidence/display/<stem>-DisplayN-<slug>/.”
>
> After: “Write to the unit directory supplied by the owning Page Result contract. If the Page and Paper adapters resolve different locations, stop and report the conflicting owner paths before creating files.”

### P1 — Renderer 说明与 manifest 无法表达五种 renderer，TeX 的 wrapper 契约也冲突

共享输出合约开头声称所有 renderer 中只有 table、figure、diagram、illustration 四种（display/ref/display-unit-output-contract.md:3-8），asset/recipe 表也未列 TeX（:59-70）；稍后 sibling table 却包含 haipipe-display-tex（:136-148）。输入模板允许的 kind 只有 figure、table、diagram、illustration（display/ref/intake-manifest.template.yaml:5-8），TeX 单元无正确值可填。通用 contract 说 float.tex “references the asset only”（display/ref/display-unit-output-contract.md:69-70），TeX 技能说 float.tex 使用 LaTeX 输入 recipe 源文件（haipipe-display-tex/SKILL.md:33、50-53）。两者不是同一机制。

**影响：**代理无法为 TeX 单元填写匹配的 manifest.kind；若照通用合约写 float.tex，仅引用 PDF，就失去 TeX 文档共享字体与宏的 native 路径。照 TeX 技能输入源文件则违反“asset only”。

**建议：**将五种 renderer 都列入合约和 schema；明确 TeX 的两种消费路径（源 TeX 输入与编译后的 PDF asset），不能用普通 renderer 规则覆盖 TeX delta。另需澄清 consumer fixture 使用 manifest.json 是 Intake manifest.yaml 的投影还是另一份权威文件（output contract:19-20 与 :29-37）。

**English before / after：**

> Before: “Every renderer (-display-table, -display-figure, -display-diagram, -display-illustration) writes into a unit directory.”
>
> After: “All five renderers, including haipipe-display-tex, write into the caller-supplied unit. The TeX adapter may expose both its native source and the compiled PDF asset; its float behavior is defined in the TeX-specific contract.”

### P1 — 概念 renderer 是否可以呈现经核实数字，入口与合约给出相反答案

门面说：

> haipipe-display/SKILL.md:29-31：“Concept kinds ... carry no numbers at all”

但 intake 合约写明：概念图通常省略 values source；若包含真实计数，则添加单独的 role: values（display/ref/display-intake-contract.md:77-82）。diagram 要求读 manifest 中批准的真实数值（haipipe-display-diagram/SKILL.md:23-26）；输出合约也说 schematic 的 real counts 可由 caller 提供（display/ref/display-unit-output-contract.md:118-125）。

**影响：**“不能带数字”会让代理删掉已批准的 N，也可能使其忽略真实数字来源规则；同一请求经过 door 与 diagram 会得到不同结果。

**建议：**规则应禁止概念 renderer 推算或编造值，而不是禁止画出有 provenance 的值。

**English before / after：**

> Before: “Concept kinds carry no numbers at all; their input is the spec or prompt they draw.”
>
> After: “Concept renderers do not calculate values. They may include a count or estimate only when it comes from a declared, verified role: values intake source.”

### P1 — 表格示例会悄悄写出错误的 Observations=0，且文档运行目录不成立

表格样例用 df.attrs.get('n1', 0) 和 df.attrs.get('n2', 0) 输出 Observations（haipipe-display-table/SKILL.md:128-145），但示例 CSV 只列 term 与各模型 coef/SE/p 列（:108-114），不会自动产生 n1/n2 attrs。无额外逻辑时会打印 0；同一技能又要求数字必须来自文件、不能硬编码（:103-106）。

脚本放在 recipe/，相对输入和输出却是 intake/、assets/；随后只说明运行 “python gen_table*.py”（:103-105、149-155）。在 unit 根目录找不到脚本；在 recipe/ 内运行又会找错输入输出。figure 也在 recipe/ 创建脚本，却用相同的相对路径与 glob（haipipe-display-figure/SKILL.md:136-137、178-187）。

**影响：**表格可能错误报告零样本量；照文字操作则找不到脚本或文件。

**建议：**明确唯一工作目录，按该目录解析输入输出；Observation 必须来自快照列。字段缺失就省略该行或 HOLD，不能把未知数写成零。

**English before / after：**

> Before: “Observations & {%d} & {%d}” using df.attrs.get('n1', 0) and df.attrs.get('n2', 0).
>
> After: “Read N from declared snapshot columns. If N is absent, omit the row or stop for a corrected snapshot; never substitute zero. From the unit root, run python recipe/gen_table2_main_regression.py, with paths resolved from that root.”

### P1 — 构图方向、候选晋升和“接受”没有统一的人类决定者

门面要求先选构图方向、记录 approved composition，并将晋升留给 caller（haipipe-display/SKILL.md:33-64；output contract:89-100）。但插画技能让生成者自评 1–10，低于 9 就重生成，“When accepted” 后直接 finalize（haipipe-display-illustration/SKILL.md:243-286）；未定义是谁接受、何时把图展示给 caller，也没有要求候选状态直到 caller 决定。helper 可以按给定 caption/label/placement 写 float.tex（paper_illustration_image2.py:142-185）。

**影响：**模型评分或 agent 自评容易被当作最终验收；生成候选、caller promotion 与 Page 的人类 accepted tick 混成一个状态。

**建议：**分开三件事：agent 自检、候选交 caller 检视、caller 选择晋升。构图 freeze 要记录由谁作出 ruling；accepted: 仍由获授权的人填写。分数只是诊断。

**English before / after：**

> Before: “Score it from 1-10. If score < 9, refine. When accepted, finalize into the display unit.”
>
> After: “Score and refine the candidate as an internal quality check. Show the current candidate and its review notes to the caller. Keep it in candidates/ until the caller approves promotion; a score of 9 does not mean accepted.”

### P1 — figure-to-svg 的 slicing 指令与实际脚本签名不匹配

现行说明调用：

> figure-to-svg/SKILL.md:154-156：“slice_grid.py part1_grid.png cropped_icon_raw/ --grid 3x3”

当前脚本签名是 slice_grid.py <grid.png> <rows> <cols> <out_dir> '<names_json>'（figure-to-svg/scripts/slice_grid.py:10-13），并将第二、第三参数直接解析成整数（:21-24）。技能树把生成网格放在 redraw_icon/（SKILL.md:73-80），gen_icon_grid.py 实际写到 <workspace>/figures/ai_generated/（scripts/gen_icon_grid.py:10-16、51-62）。后续也没有 names_json 示例，未将 bridge 输出移到切图命令期望位置。

**影响：**代理照文档会在切第一张图时因参数类型不符而退出，也不知道 manifest 中 cell/id 如何转换成行优先名称数组。

**建议：**让 SKILL、bridge 实际落点与 slice 签名一致，给完整可复制命令，明确空单元如何表达。

**English before / after：**

> Before: “slice_grid.py part1_grid.png cropped_icon_raw/ --grid 3x3”
>
> After: “Read icon IDs from the manifest in row-major order, using an empty string for unused cells. Call slice_grid.py <grid.png> 3 3 <out_dir> '<ids_json>'. Use the exact generated path under <workspace>/figures/ai_generated/ as <grid.png>.”

### P2 — Workflow / Run 模型：单次 renderer 操作可作为一个 Run，但技能未说明边界；仍有一个活跃 Phase

多数显示/转换技能描述的是一个用户目标的程序说明。依照要求，不应把每个内部 Step、compile、review、脚本调用或反馈轮次改成 Run；共同完成同一 unit 的操作通常留在一个 renderer Run 内。origin.run 指上游 source provenance，语义合理，不应机械改名。

技能的 Workflow 标题和有序步骤未声明一次技能调用对应什么 Run，也未说明什么时候多个 display unit 应独立成 Runs。唯一显式 Phase 词不是兼容字段，而是 diagram 的现行集成说明：

> haipipe-display-diagram/SKILL.md:237-239：“/paper-writing Workflow 3, this skill handles Phase 2b when illustration: figurespec.”

它指向 ARIS 外部 paper-writing 文档的旧阶段名；该名称仍可见于 references/aris/skills/paper-writing/SKILL.md:32、194-202。因此这是当前 Display skill 中的活跃外部集成标签，不是仓储层历史字段。Display 不应继续复制它；外部 ARIS 文件归其维护方处理。

**总体 Verdict：部分通过。**没有跨技能的 Phase 字段体系；唯一命中是 diagram 的外部集成标签。其他技能未发现此词。九份单目标技能通常可自然映射为一个 Run，但没有清楚写出边界，其 Workflow 多指内部说明步骤，并非多 Run 的正式 Workflow 定义。

| Skill | Workflow / Run | 证据与说明 |
|---|---|---|
| figure-to-svg | 部分通过 | 一张源图到一个 master SVG 是一个转换 Run；分割、切图、迭代和 subagent 工作是内部步骤/子工作，需声明边界。 |
| haipipe-display | 部分通过 | 单个 unit 的路由与构图 gate 不是多 Run Workflow；应说明一项 unit 工作归一个 Run。 |
| haipipe-display-diagram | 不通过 | 唯一当前 Phase 2b 引用；FigureSpec 中 Step 1/2 是被绘制流程的节点示例，不应自动当作 HAI-Pipe Run。 |
| haipipe-display-figure | 部分通过 | 多张图若共同服务一个 unit，仍可属于一次绘图 Run；manifest 的 origin.run 是上游 provenance。 |
| haipipe-display-illustration | 部分通过 | 一幅概念图的 prompt、生成、复核、重试可在一个 Run；不应把每次 bridge 调用都另立 Run。 |
| haipipe-display-table | 部分通过 | 一张表的代码、编译、检查通常是一项目标 Run；不需要把技能步骤拆成 Runs。 |
| haipipe-display-tex | 部分通过 | 一个 TeX unit 的源文件和 asset 编译是同一目标 Run 的内部动作；先厘清消费路径。 |
| html-to-svg | 部分通过 | 一个 deck 到多页 SVG/PDF/PPTX 可是一项转换 Run；单页文件不是自动独立 Runs。 |
| icon-to-svg | 部分通过 | 一个源 icon 到一个 SVG 是有界 Run；比较、打分和居中是内部 Steps。 |
| html-ppt | 不适用（形式化 HAI-Pipe Workflow 对象） | 这是通用 deck authoring 说明而非 HAI-Pipe Workflow/Run 定义；一次成稿是一项 deck 工作，未发现概念性 Phase。 |

如需共用英文澄清句：

> “One invocation of this renderer produces one bounded unit and may be modeled as one Run in a parent Workflow. The numbered Steps, review turns, and tool calls are internal to that Run unless they have their own independently closable target and receipt.”

### P2 — 数据图技能对“不做什么”的说明互相矛盾，并引用旧平面图目录

figure 的 scope 表把 Architecture/pipeline diagrams 标为 “manual”（haipipe-display-figure/SKILL.md:41），但随后要求经 Display stage 路由给 diagram/illustration（:45-47、172-176）；门面已经将其列为 renderer。它也允许无 paper 时使用 flat figures/（:59-60、237-240），但共享合约要求 renderer 接收 unit，不能遗留平面资产（display/ref/display-unit-output-contract.md:3-8、104-114）。

**影响：**概念图请求可能不会被路由到相应 renderer；无 paper 用户会得到与共享 unit contract 不一致的路径。

**建议：**将 diagrams 标成“此技能不渲染，路由到 diagram 或 illustration”；无 paper 时仍由 caller 提供 unit，或由共享合约明确许可 scratch 模式，不应由技能覆盖共同规则。

### P2 — HTML/PPT 家族身份、模板数量和脚手架输出位置不明

display/README.md:17-19 把 html-ppt 定义为 Board slide decks 的 vendored runtime，并在 :29 说 Board talk 属于 slide plugin；html-ppt/SKILL.md:3、32-35 却对“任何 presentation/PPT/slides/deck”触发且建议优先于从头制作。两个入口可能争夺 Board talk。目录数也不一致：SKILL.md:23 称 15 个 full-deck，但 :112、:216 称 14；README 和模板索引也分别出现 15 与 14。templates/deck.html:19 的 starter 副标题仍写 24 themes、30 layouts、25 animations，quick start 会把它作为新 deck 起点（SKILL.md:126-154）。脚手架默认把产物放在 skill 目录下，quick start 却示意用户项目的 examples/my-talk（SKILL.md:128-132；scripts/new-deck.sh:18-37）。

presenter mode 另有保密误解风险：模板说观众永远看不到 .notes（presenter-mode-reveal/README.md:100-101），但 notes 仍在共享 HTML 中且 runtime 会读取它（assets/runtime.js:367-388）。

**建议：**限定 html-ppt 为独立通用 deck，让 Board talk 归 slide plugin；统一实际模板数、清理 starter 的旧功能数字；将输出目录作为用户项目中的显式路径并回显；说明 notes 只在观众画面隐藏、不能存放机密。

**English before / after：**

> Before: “Use when the user asks for any kind of slide-based output. Prefer this over building from scratch.”
>
> After: “Use for standalone HTML decks. For a Board Page talk, use the Page slide plugin. Create the deck in the user-supplied output directory and report that path.”

### P2 — HTML-to-SVG 没有明确 SVG-only 请求要检查什么，且范例链接失效

html-to-svg/SKILL.md:38-58 只要求预览 “a few layout-heavy slides”，每页 PDF 审阅则是 PPTX build 前的门槛；结尾把 SVG、PDF、PPTX 串成 full loop（:60-92）。用户只要 SVG 时，不知道是否需检查每页或是否默认还会有 PPTX。Reference implementation 一节指向当前不存在的 collaborations/Event-JHU-ADHD-NIH-Team 示例（:114-120）。

**建议：**一次 deck 转换 Run 中先生成 SVG 和 review PDF，逐页检查；只有用户请求时才生成 PPTX。修复或删除失效示例链接；最终回复说明 SVG 目录、检查过的 PDF 与实际导出的格式。

### P2 — figure-to-svg 对 fidelity 的承诺超过默认方法，且未说明如何装配母图

技能称 master SVG 是 “faithful copy”（figure-to-svg/SKILL.md:15-20），默认却重生成 icons（:129-150）；被引用 lesson 13 已说明生成 icon 是 look-alikes、不是 exact pixel copy，也不适用于 exact-fidelity 要求（figure-to-svg/lesson/13-260701-regenerate-icons-not-crop-from-source.md:28-32）。此外技能承诺 Figure1_replica.svg 由多个 part 构成（SKILL.md:69-82），compose 示例每次只由一个 inventory 合成一个 SVG（:202-223；scripts/compose_svg.py:2-15、284-323），未给出如何将 part 放回原母图坐标的操作。

**影响：**要求逐项复现的用户可能拿到重画图标；代理完成各 part 后可能交不出承诺的 master。

**建议：**称为 reconstructed master，默认明确图标只是近似；若要求精确图标，先找原始 vector 或询问是否接受近似。补充母图坐标、缩放参数和可执行的 master 组装命令。

**English before / after：**

> Before: “The output is a single master SVG that reads as a faithful copy of the source.”
>
> After: “The output is a reconstructed master SVG. By default, icons are regenerated look-alikes and may differ from the source. If exact icon artwork matters, locate source vectors or ask whether approximate icons are acceptable.”

### P2 — converter 与 display-unit 的晋升边界没有说明

family README 将 figure-to-svg、icon-to-svg、html-to-svg 列为 converters（display/README.md:17-20），而共享合约只约束 renderer：caller 提供 unit，recipe 与 assets 写入 unit（display/ref/display-unit-output-contract.md:3-8、102-114）。转换器输出到源文件旁或 deck/svg 目录，没有说何时它们是独立文件交付、何时应进入 first-class display unit。

**建议：**加一段边界说明：converter 默认只产 standalone 文件，不创建或晋升 display unit；若结果要成为 Page/View/Paper display，由 caller 将批准输入、recipe 和胜出 SVG 放入规定 unit，再走候选与接受流程。

### P2 — review 被写成模型自评，却没有共同的预览与用户回传约定

共享合约把包括 caption、label、placement 的 preview.pdf 作为 review artifact（display/ref/display-unit-output-contract.md:79-82）。unit agent 要求查看 PDF；table 主要 spot-check 数据并送模型审阅（table/SKILL.md:149-177）；figure checklist 没要求编译、查看 unit preview（figure/SKILL.md:219-240）；diagram 允许 Codex review 并用 7/10 迭代（diagram/SKILL.md:145-171）；illustration 用 9/10 控制重生成。工具评审、人工视觉检查、caller 接受和 accepted tick 没形成一致状态。

**建议：**共用最终回传说明应指出：哪些由 agent 检查、哪一个 preview 供用户检视、何种缺项让 build 保持 pending、candidate 由谁晋升、accepted: 由谁填写。评分只能是自检或建议。

## 桌面走查（非运行时测试）

### 1. Page 用户说“把这些结果画成图”

门面路由到 haipipe-display-figure 后，renderer 会查 intake manifest；但 door 指向 outline/evidence/display，现行 Page contract 认为该目录 retired。Page intake 还可能要求由 page-service values.yaml 来，而不是 renderer 自己选 CSV。真正影响的是能否定位本次结果，以及图会不会写进 reader 忽略的目录。

**建议回复：**

> “我已选数据图 renderer。开始前需要这个 Page 已批准的 Local Input 和 Result unit 地址；我不会从任意 Task CSV 拉数据。当前 Display 与 Page 文档列出的写入路径不一致，我会先报告并等待统一的 owner path，再创建候选。”

### 2. 用户要“画方法概念图，标 N=120”

门面禁止所有概念数字；intake contract 与 diagram 却允许来自 verified values source 的 N=120。构图阶段就会得到相反指令。

**建议回复：**

> “这张图走 concept-diagram 路线。我可以标 N=120，但需要它出现在已声明并校验的 values intake 中；不在该来源里的数量不会写进图。先给你看构图候选，确认模块关系后再制作胜出资产。”

### 3. 用户要“把这个 regression CSV 做成表”

generator 示例默认缺失的 N 为 0，且运行命令的 cwd 与 inputs/assets 相对路径不兼容。可能产生虚假统计行，或根本无法从 clean context 执行。

**建议处理：**

> “先核对 manifest 中声明的快照和表格 claim。若快照无 N 字段，我会暂停并标出缺失列，不会用零代替。运行时从 unit root 调用 recipe 下的脚本，并从同一 root 定位 intake 与 assets。”

### 4. 用户要“先看构图方向，再决定是否精修”

door 说构图应先 approved，但只在用户明确要求先讨论方向时才停止；插画技能没有把 9 分和 caller acceptance 分开，代理可能自动 finalize。

**建议交互：**

> “这是方向草案，不是最终图。请确认模块次序、箭头方向、必须保留元素和图面语言。收到你的 ruling 后，我会记录构图并继续；最终资产仍保留为 candidate，直到你明确选择晋升。”

### 5. 用户给出 8 页技术分享 outline，并说“做成小红书 3:4 幻灯片”

html-ppt 仍要求先确认内容/观众、主题和模板，即使用户已提供 outline；示例主题也未采用 house default。模板为 3:4，但 PNG 脚本默认为 1920×1080。用户可能被重复询问，并拿到横画布图。

**建议回复：**

> “我会复用你给的 outline，先用最接近的 xhs-post 模板。导出目标是 810×1080；如果你要其他平台尺寸，请告诉我。交付 HTML、逐页预览 PNG，以及我检查后的画布尺寸与裁切结果。”

### 6. 用户说“把这个 PNG 里的图标转成可编辑 SVG”

icon-to-svg 的单图说明要求源图与渲染并排查看，并提醒 PASS 不是最终证据；figure-to-svg 则把整图重建称为 faithful copy，且 slice 命令照抄会失败。

**建议回复：**

> “这是一个单图标，走 icon-to-svg。默认会按形状重画，不保证逐像素相同。我会给你看源图和 SVG 的并排对比，并报告哪些细节有意简化；你可据此决定是否接受或要求重画。”

## 跨家族边界

- **Page / Paper / Display：**Page 当前 evidence contract 规定 Result payload 地址；Paper assemble 仍读旧 outline/evidence/display；Display 和 unit-agent 又使用两个不同旧地址。canonical write target 需要三方共同定案。Display 是 worker，不能单方面更改 Page Result owner 或 Paper delivery loader。
- **View caller：**共享 output contract 将 View 作为 first-class caller（display-unit-output-contract.md:13-20），但 Display README 入口只指向 Board Page 与 Paper stage（README.md:26-29）。可在家族 map 增加 View 调用路径。
- **html-ppt / slide plugin：**HTML-PPT 触发词包括任意 presentation 与 Board talk，而 family map 说 Board talk 属于 slide plugin。建议限定独立 deck 的职责，让 slide plugin 保留 Page talk 入口。
- **Insight 与 Design：**Display family map 没有声明 Application parent，也未把 Insight 或 Design 归为 Display 子类。本范围未发现违反“Insight/Design 独立一等 family”的结构。若这些 family 的 Run 结果可作为 Display 来源，应在 intake origin schema 定义 provenance，而不是新设 Application 层。

## 建议修正顺序

1. 由 Page、Paper、Display owner 统一 canonical unit 地址、Result/manifest/adapter 关系；更新所有 live write-target、agent receipt 与 preview 读取说明。
2. 修正共享 Intake/Output contract：补足 TeX kind、TeX source/PDF 两条输出机制、View/Page/Paper caller，以及有效的 Page Local Input 样例；统一 concept values 规则。
3. 修复会阻断执行的范例：table 的 N 与运行目录、figure 的 script cwd、figure-to-svg 的 bridge 落点、slice 参数与 master 装配命令。
4. 统一 visual review 与人类决策：candidate、caller promotion、human accepted tick；各 renderer 明确需要查看的 preview。
5. 梳理路由边界与文案：diagram/figure scope、Mermaid 路由、html-ppt 与 Page slide plugin 边界、converter 到 unit 的 handoff。
6. 清理数量、模板与呈现信息：html-ppt 模板数、starter 旧计数、输出路径、讲者稿计数单位和 notes 非机密提示；修正失效示例链接。
