#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian笔记生成脚本 - 正确处理frontmatter格式
"""

import sys
import os
import argparse
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def get_vault_path(cli_vault=None):
    """从CLI参数或环境变量获取vault路径"""
    if cli_vault:
        return cli_vault
    env_path = os.environ.get('OBSIDIAN_VAULT_PATH')
    if env_path:
        return env_path
    logger.error("未指定 vault 路径。请通过 --vault 参数或 OBSIDIAN_VAULT_PATH 环境变量设置。")
    sys.exit(1)


def generate_note_content(paper_id, title, authors, domain, date):
    """生成笔记的 Markdown 内容"""
    domain_tags = {
        "大模型": ["大模型", "LLM"],
        "多模态技术": ["多模态", "Vision-Language"],
        "智能体": ["智能体", "Agent"],
    }
    tags = ["论文笔记"] + domain_tags.get(domain, [domain])
    tags_yaml = "\n".join(f'  - {tag}' for tag in tags)

    return f'''---
date: "{date}"
paper_id: "{paper_id}"
title: "{title}"
authors: "{authors}"
domain: "{domain}"
tags:
{tags_yaml}
related_papers: []
created: "{date}"
updated: "{date}"
status: draft
analysis_status: not-assessed
assessment:
  evaluator: ""
  criteria_version: "paper-analyzer@0.2.1"
  assessed_at: ""
  input:
    run_readable: ""
    run_compact: ""
    snapshot_uri: ""
    snapshot_sha256: ""
---

# {title}

## 核心信息
- **论文ID**：{paper_id}
- **作者**：{authors}
- **机构**：[从作者推断或查看论文]
- **发布时间**：{date}
- **会议/期刊**：[从categories推断]
- **链接**：[arXiv](https://arxiv.org/abs/{paper_id}) | [PDF](https://arxiv.org/pdf/{paper_id})
- **引用**：[如果可获取]

## 研究问题
[问题描述中文翻译和解释]

## 来源与阅读范围
- **规范身份**：[DOI / arXiv ID / 其他稳定标识]
- **核验方式**：[发布者或索引及核验日期]
- **阅读深度**：[元数据 / 摘要 / 指定章节 / 全文]
- **本次评估问题**：[明确的问题；未提供则写“未评估项目相关性”]
- **覆盖范围**：[实际查看的章节、页码或表图；未查看处不要推断]

## 方法概述

### 核心方法

1. [方法1]
   - [详细描述]
   - [关键步骤]
   - [创新点]

### 方法架构
[架构描述和图片引用]

### 关键创新

1. [创新点1] - [为什么重要]
2. [创新点2] - [为什么重要]
3. [创新点3] - [为什么重要]

## 实验结果

### 数据集
- [数据集1]：[规模、特点]
- [数据集2]：[规模、特点]

### 实验设置
- **基线方法**：[列出对比方法]
- **评估指标**：[列出指标]
- **实验环境**：[硬件、超参数]

### 主要结果
[实验结果表格和关键发现]

## 深度分析

对下列评估逐项使用 `supported`、`partially-supported`、`not-supported`、
`not-assessed` 或 `not-applicable`，写明页码、章节或表格位置，并说明缺失
或相反证据。`not-assessed` 表示未查看所需内容，不代表负面结论；
`not-applicable` 仅用于研究设计确实不适用的标准，并说明原因。

### 研究价值
- **作者声称的贡献**：[原文主张与页码/章节]
- **与本次问题的关系**：[direct / adjacent / out-of-scope / unresolved；按上面的范围规则说明]
- **可迁移范围**：[研究对象、设置或结果在哪些范围内可用；给证据位置]

### 优势
- **作者声称**：[主张 + 位置]
- **读者判断**：[判断 + 所依据的结果/设计位置]

### 局限性
- **作者明确承认**：[限制 + 位置；没有则写“未找到”并说明已查看范围]
- **读者推断**：[限制 + 位置 + 推理所依赖的证据；没有则留空]

### 适用场景
- [适用场景1]
- [适用场景2]

## 与相关论文对比

### [[相关论文1]] - [对比关系]
- **差异**：[本文方法的不同之处]
- **改进**：[相比的改进点]
- **性能对比**：[如果可用]

### [[相关论文2]] - [对比关系]
[类似格式]

### [[相关论文3]] - [对比关系]
[类似格式]

## 技术路线定位

本文属于[技术路线]，主要关注[具体子方向]。

## 未来工作建议

1. [作者建议1]
2. [作者建议2]
3. [基于分析的延伸建议]

## 证据化评估

判定口径：`supported` 表示已查看内容直接给出该标准所需证据；
`partially-supported` 表示有部分证据，但缺少明确列出的细节；
`not-supported` 表示已查看相关内容但没有支持证据，或报告了相反证据；
`not-assessed` 表示来源/章节不可用或未查看；`not-applicable` 表示该标准
不适用于论文类型并须说明原因。不可访问或未读内容不能作为“没有证据”的
依据。方法透明度检查研究设计/理论假设、数据与对象（如适用）及追踪主张
所需的程序细节；评估覆盖检查主要主张是否有对应分析/证明，并对实证主张
检查比较对象、结果指标和不确定性；主张可追溯要求每个重要结论连到结果或
证明的位置。

| Criterion | State | Evidence locator | Finding and missing evidence |
|---|---|---|---|
| 与问题/人群匹配 | [direct / adjacent / out-of-scope / unresolved] | [页码/章节] | [对照本次问题与纳入规则] |
| 方法透明度 | [supported / partially-supported / not-supported / not-assessed / not-applicable] | [页码/章节] | [说明已报告或缺失的设计细节] |
| 评估覆盖 | [supported / partially-supported / not-supported / not-assessed / not-applicable] | [表格/章节] | [说明研究对象、对照、结果指标及其不确定性] |
| 主张与结果可追溯 | [supported / partially-supported / not-supported / not-assessed / not-applicable] | [页码/表格] | [将重要主张连到对应的报告结果] |

不要将这些标准合并成总分。区分作者报告的主张与读者解释；若未查看来源或
相关章节，保留草稿状态并标记未评估。

## 我的笔记

[用户阅读后手动补充的内容]

## 相关论文
- [[相关论文1]] - [对比关系]
- [[相关论文2]] - [对比关系]
- [[相关论文3]] - [对比关系]

## 外部资源
- [论文链接]
- [代码链接（如果有）]
- [项目主页（如果有）]
- [相关资源]
'''


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S',
        stream=sys.stderr,
    )

    parser = argparse.ArgumentParser(description='生成论文分析笔记')
    parser.add_argument('--paper-id', type=str, default='[PAPER_ID]', help='论文 arXiv ID')
    parser.add_argument('--title', type=str, default='[论文标题]', help='论文标题')
    parser.add_argument('--authors', type=str, default='[Authors]', help='论文作者')
    parser.add_argument('--domain', type=str, default='其他', help='论文领域')
    parser.add_argument('--vault', type=str, default=None, help='Obsidian vault 路径')
    args = parser.parse_args()

    vault_root = get_vault_path(args.vault)
    papers_dir = os.path.join(vault_root, "20_Research", "Papers")
    date = datetime.now().strftime("%Y-%m-%d")
    paper_title_safe = args.title
    for ch in ' /\\:*?"<>|':
        paper_title_safe = paper_title_safe.replace(ch, "_")

    note_dir = os.path.join(papers_dir, args.domain)
    os.makedirs(note_dir, exist_ok=True)

    note_path = os.path.join(note_dir, f"{paper_title_safe}.md")
    content = generate_note_content(args.paper_id, args.title, args.authors, args.domain, date)

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"笔记已生成: {note_path}")
    print(f"请手动编辑笔记内容，替换占位符为实际分析结果")


if __name__ == '__main__':
    main()
