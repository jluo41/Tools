// Local design fixture. No production state or signatures are written.
window.BOOK = {
  title: '组间差异 · Question Book',
  goal: '把“有没有差异”推进到“差异在什么条件下成立”。',
  current: 'v2',
  versions: {
    v1: {name:'第一版 · 建立基础问题', state:'已冻结（示例）', goal:'描述数据、组间差异和每日变化。', previous:null, questionIds:['I02'], findingIds:[], motivation:'先建立可复用的基础问题和分析方法。'},
    v2: {name:'第二版 · 检查时间稳定性', state:'草稿', goal:'补齐差异随时间变化的检验，并明确解释边界。', previous:'v1', questionIds:['I02','K02'], findingIds:['F01','F02'], motivation:'上一版的 K01 聚焦分组汇总，而 I02 描述每日变化。仍需要一个问题，直接检验前后两个时间窗口的组间差异。'}
  },
  questions: {
    I02: {id:'I02', title:'结果如何随日期变化？', level:'Information', owner:'v1', state:'沿用', goal:'描述每天的结果变化，为时间稳定性问题提供背景。', why:'先描述变化，再判断组间差异是否随时间改变。', method:'按日期汇总结果并查看变化；描述趋势不直接回答组间差异是否稳定。', needs:['日期与结果字段','按日汇总的结果表'], output:'每日结果图表与解释规则', findingIds:[], steps:[{title:'检查沿用范围', expected:'确认原方法仍适用于新版问题集', result:'原 Task 保持不变；本版只引用', state:'沿用'}], source:'q-I02'},
    K02: {id:'K02', title:'组间差异在前后两个时间窗口都成立吗？', level:'Knowledge', owner:'v2', state:'待审查', goal:'区分总体组间差异与时间变化可能带来的不同解释。', why:'已有问题覆盖总体差异和每日变化，但缺少直接的跨时间检验。', method:'比较前后半段各自的组间差异，并检验两段差异的变化；按预先约定的规则解释。', needs:['I01：整体组间差异','I02：每日变化','E3：两段差异、区间和差异变化的检验','E4：整合上述证据形成判断'], output:'halves.csv 与 verdict.json；本页只定义方法，不展示数据结论', findingIds:['F01'], steps:[{title:'定义问题',expected:'明确对象、时间范围与可回答的边界',result:'K02 问题定义草稿',state:'已起草'},{title:'准备证据计划',expected:'列出 E1–E4，并说明计算结果的验收条件',result:'证据计划草稿，等待独立审查',state:'待审查'},{title:'准备并审查脚本',expected:'实现已审定的方法，并留下审查记录',result:'等待证据计划通过',state:'未开始'}],source:'q-K02'}
  },
  findings: {
    F01:{id:'F01',title:'描述每日变化，不能替代跨时间的差异检验',body:'I02 负责描述每日变化；K02 需要直接比较两个时间窗口的组间差异。问题之间应连接证据，而不是用趋势图代替检验。',owner:'K02',version:'v2',state:'待评审',evidenceIds:['q-K02','proposal'],consequence:'保留 I02，新增 K02；把 I02 的结果作为 K02 的引用证据。',source:'j02/findings/F01.md（拟议路径）'},
    F02:{id:'F02',title:'本版的目标是补齐解释范围，不是预先认定结果稳定',body:'版本目标应描述需要检验的缺口。只有应用到固定数据版本并完成分析后，才能判断差异是否稳定。',owner:'v2',version:'v2',state:'待评审',evidenceIds:['q-K02'],consequence:'整版评审检查解释边界；数据答案留在 Insight Job 中。',source:'j02/findings/F02.md（拟议路径）'}
  },
  plans:[
    {id:'P01',version:'v2',title:'沿用每日变化问题',why:'保留基础描述，避免重复定义同一问题。',question:'I02',expected:'沿用原问题与方法，明确与 K02 的关系',result:'引用第一版 I02；原 Task 不复制',state:'沿用',findingIds:[]},
    {id:'P02',version:'v2',title:'补齐跨时间的差异检验',why:'回应上一版尚未覆盖的时间稳定性问题。',question:'K02',expected:'明确问题、证据需求、计算产物和解释规则',result:'问题与证据计划已起草，仍需审查',state:'待审查',findingIds:['F01']},
    {id:'P03',version:'v2',title:'整版评审与发布',why:'单个问题完成，不代表整套问题已经一致。',question:null,expected:'检查目标覆盖、问题依赖、方法审查及发布条件',result:'尚未进入发布；K02 证据计划和脚本审查未完成',state:'等待',findingIds:['F02']}
  ],
  ideas:[{title:'增加跨时间的差异问题',why:'总体差异与每日变化还没有被同一个检验连接起来。',state:'纳入第二版',target:'K02',source:'proposal'},{title:'检查不同分组的时间变化',why:'先确认数据量是否支持，再决定是否进入后续版本。',state:'待讨论',target:null,source:null}],
  sources:{
    'q-K02':{name:'K02 · 问题与证据计划',path:'blueprints/Project-Ladder/insight/InsightQuestionBook-Example/j02_question-v2_example-follow-up/t09_K02_gap-over-the-window/question.md',text:'原文件定义 E1 总体差异、E2 每日变化、E3 两段差异与检验、E4 综合判断；agreed 为未确认。本原型使用中文摘要。'},
    'q-I02':{name:'I02 · 原版本问题',path:'blueprints/Project-Ladder/insight/InsightQuestionBook-Example/j01_question-v1_example-questions/t04_I02_outcome-by-day/question.md',text:'第二版 release.yaml 通过 task 路径引用第一版 I02，change: kept。这里沿用同一 Task，不生成展示副本。'},
    proposal:{name:'时间稳定性改进建议',path:'blueprints/Project-Ladder/insight/InsightQuestionBook-Example/proposals/gap-over-the-window.md',text:'K02 的 question.md 将此建议列为来源。原型用它展示“来源 → 动机 → 计划 → 问题”的路径。'},
    release:{name:'第二版问题清单',path:'blueprints/Project-Ladder/insight/InsightQuestionBook-Example/j02_question-v2_example-follow-up/release.yaml',text:'现有第二版沿用 D01、D02、I01、I02、K01、W01、X01、X02，并新增 K02。本原型聚焦 I02 与 K02 两个条目；不是完整版本清单。'}
  }
};
