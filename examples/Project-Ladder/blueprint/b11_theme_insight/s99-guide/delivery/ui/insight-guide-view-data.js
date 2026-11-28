const GUIDE = {
 "description": "The Insight Workbench reads one dataset, version by version, and answers questions about it from Data and Information up to Knowledge and Wisdom. The questions and their scripts live in a Question Book, released and signed as pN; the insight Board runs one release on one data version per Job, one Task per question and one run per segment. The runs compute the tables; an agent then writes each question's page, a takeaway per segment, and another agent checks it. The workbench shows what each Job found, the runs behind each answer, and what still needs a check or a signature.",
 "skills": [
  {
   "skill": "hai-insight",
   "role": "The Insight Block: one task per question, its file, its script and its runs"
  },
  {
   "skill": "hai-insight-evidence-plan",
   "role": "A question's evidence needs, agreed by a reviewer"
  },
  {
   "skill": "hai-insight-check",
   "role": "Question rules and each cell's status from receipts and checks"
  },
  {
   "skill": "hai-draft-workflow",
   "role": "One page per question, checked by an agent that did not write it"
  },
  {
   "skill": "workbench-insight",
   "role": "Scope, Question Book, Insight, Check and Delivery over the Block"
  }
 ],
 "levels": {
  "Block": {
   "role": "one insight topic over one growing dataset: a Job per pair (release × data version)",
   "spaces": {
    "Description": {
     "is": "one dataset, its versions, and the Question Book it runs: the Map of Jobs",
     "reads": "board.md · meta/ · the release"
    },
    "Idea Studio": {
     "is": "the Board's drawings, one topic after another",
     "reads": "sNN-<topic>/"
    },
    "Audience Report": {
     "is": "the Block's own questions over the Jobs: Coverage · Tracks · Consistency · Findings",
     "reads": "reports/qNN_<topic>/"
    },
    "Work Details": {
     "is": "the Jobs, each opening to its Tasks' quick results",
     "reads": "jNN_prototype-pN-<slug>_data-<d>vM/"
    },
    "Runs": {
     "is": "the Board's own soft Runs, and its Jobs' from below",
     "reads": "runs/run-<type>-<target>/"
    },
    "Delivery": {
     "is": "the signed Wisdom counsel, naming the Job it came from",
     "reads": "delivery/"
    }
   }
  },
  "Job": {
   "role": "one Question Book release run on one data version; frozen once closed",
   "spaces": {
    "Description": {
     "is": "its two pins: the Question Book release and the data version",
     "reads": "jNN_prototype-…_data-<d>vM.md · the release · <d>vM"
    },
    "Idea Studio": {
     "is": "optional: a drawing about this pair",
     "reads": "studio/"
    },
    "Audience Report": {
     "is": "the Overall Report (its Executive answers, one document), then Question │ Work │ Report by D · I · K · W, filtered by Segment × Period",
     "reads": "tNN_<L><NN>_<q>.md · reports/vs-<prev>.md"
    },
    "Work Details": {
     "is": "the J-T-R tree: its Tasks, each open to its Runs",
     "reads": "tNN_<L><NN>_<q>/runs/"
    },
    "Runs": {
     "is": "its own soft Runs, then its Tasks' hard and soft",
     "reads": "runs/ · tNN_…/runs/"
    },
    "Delivery": {
     "is": "only the latest Job's Wisdom counsel, to the Board",
     "reads": "→ Board › Delivery"
    }
   }
  },
  "Task": {
   "role": "one question on one Job's pair: its runs per segment and its page",
   "spaces": {
    "Description": {
     "is": "its question, read only from the release, and its records",
     "reads": "…/j0N_pN/tNN_<L><NN>_<q>/question.md"
    },
    "Idea Studio": {
     "is": "optional: a drawing about this question",
     "reads": "studio/"
    },
    "Audience Report": {
     "is": "its page: the answer, a part per partition",
     "reads": "tNN_<L><NN>_<q>.md"
    },
    "Work Details": {
     "is": "one Run per segment, and Cross",
     "reads": "runs/rNN_<segment>/"
    },
    "Runs": {
     "is": "hard: one per segment · soft: write, check",
     "reads": "runs/"
    },
    "Delivery": {
     "is": "none of its own: its answer goes up as a cite need",
     "reads": "—"
    }
   }
  }
 },
 "steps": [
  {
   "n": "1",
   "name": "Ask the question",
   "board": "Question Book",
   "what": "one ask at its DIKW level, why now, and what would answer it; question-asking methods (§ 2)",
   "where": "Scope › Questions (Ask) · Question Book › Data … Wisdom (Review the questions)",
   "who": "a person signs the question"
  },
  {
   "n": "2",
   "name": "Plan and agree",
   "board": "Question Book",
   "what": "the steps that would answer it, written before any data is read; then the script, written and reviewed; tests T0-T3 (§ 5)",
   "where": "Question Book › Data … Wisdom (Plan the evidence · Review the evidence plan · Write and Review the script)",
   "who": "a different agent agrees the plan"
  },
  {
   "n": "3",
   "name": "Run each segment",
   "board": "Instance",
   "what": "the script runs once on each segment; question-answering methods (§ 3)",
   "where": "Insight › each segment (Run a segment)",
   "who": "the run's own receipt"
  },
  {
   "n": "4",
   "name": "Check the run",
   "board": "Instance",
   "what": "the run is checked against its plan; tests T4 and T7 (§ 5)",
   "where": "Insight › each segment (Check alignment)",
   "who": "an agent that did not write the run"
  },
  {
   "n": "5",
   "name": "Write the page",
   "board": "Instance",
   "what": "one page per question, a section per segment, read into an answer at its DIKW level; question-results reading methods (§ 4); tests T5 and T6 (§ 5)",
   "where": "Insight › each segment (Write the report) · Check › Checks (Review an answer)",
   "who": "an agent that did not write the page"
  },
  {
   "n": "6",
   "name": "Hand off",
   "board": "Instance",
   "what": "a Wisdom answer goes to Design; test T8 when new data comes (§ 5)",
   "where": "Delivery › Handoff (Write the counsel · Draft the handoff)",
   "who": "a person signs the handoff"
  }
 ],
 "cards": {
  "asking": [
   {
    "name": "By level",
    "move": "Place the question on its DIKW level first; the level decides which claim the answer may make and which words of the ask are refused.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/01-by-level.md"
   },
   {
    "name": "By goal-question-metric",
    "move": "Derive questions from a stated goal and measures from each question, top down; no measure is collected that no question asks for.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/02-by-goal-question-metric.md"
   },
   {
    "name": "By question type",
    "move": "Name the question's type first (descriptive, exploratory, inferential, predictive, causal or mechanistic), then compute only the analysis that type allows.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/03-by-question-type.md"
   },
   {
    "name": "By estimand",
    "move": "Name the target quantity in words, its unit, population, measure and summary, before any model or task is chosen.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/04-by-estimand.md"
   },
   {
    "name": "By target trial",
    "move": "For a causal ask on data already collected, write the protocol of the randomised trial that would answer it, then say how the data emulate each part.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/05-by-target-trial.md"
   },
   {
    "name": "By analysis plan",
    "move": "Write the questions, the analysis and the rule that decides the answer before the outcome is seen, and keep every later change visible as a deviation.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/06-by-analysis-plan.md"
   },
   {
    "name": "By partition and power",
    "move": "Before any outcome is seen, declare the partitions (the cuts of the data a question is asked on), why the question keeps its meaning in each, and the smallest effect worth acting on; then compute each partition's minimum detectable effect.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/07-by-partition-and-power.md"
   },
   {
    "name": "By protocol reuse",
    "move": "Write the questions and their code once, as a Question Book board, then run the same protocol unchanged on each dataset and compare the answers.",
    "file": "plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/asking-methods/08-by-protocol-reuse.md"
   }
  ],
  "answering": [
   {
    "name": "By exploring",
    "move": "Look at the extract with simple displays and summaries before any model, and write down what is seen as an observation, not yet a finding.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/answer/01-by-exploring.md"
   },
   {
    "name": "By automated insight search",
    "move": "Enumerate the segments of the extract, score each candidate pattern by how interesting it is, and return the top k.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/answer/02-by-automated-insight-search.md"
   },
   {
    "name": "By pattern mining",
    "move": "Run a pattern search (association rules, subgroups of a target) over the extract, and keep only the patterns that pass a test with false discoveries controlled.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/answer/03-by-pattern-mining.md"
   },
   {
    "name": "By model comparison",
    "move": "Fit an explanatory model and a predictive model to the same question, score both on held-out data against a simple benchmark, and say which goal each answers.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/answer/04-by-model-comparison.md"
   },
   {
    "name": "By hypothesis test",
    "move": "State the hypothesis, its test, its alpha (the false-positive rate allowed) and its power before the run, then report the test's result whatever it is.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/answer/05-by-hypothesis-test.md"
   }
  ],
  "reading": [
   {
    "name": "By multiverse",
    "move": "Run one question through every reasonable analysis (each defensible segment, exclusion, coding and model), and report how much the answer moves.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/read/01-by-multiverse.md"
   },
   {
    "name": "By heterogeneity",
    "move": "Ask whether the answer differs across segments, and test the difference itself, not each partition's significance.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/read/02-by-heterogeneity.md"
   },
   {
    "name": "By sensemaking",
    "move": "Hold several explanations of a result at once, fit each to the evidence, and keep the one the evidence does not rule out, with its rivals named.",
    "file": "plugins/haipipe-toolkit/servers/workbench-insight/guide/methods/read/03-by-sensemaking.md"
   }
  ]
 },
 "papers": [
  {
   "group": "all methods (question-answering)",
   "role": "classic",
   "key": true,
   "paper": "Tukey 1962 · The future of data analysis",
   "venue": "The Annals of Mathematical Statistics",
   "doi": "10.1214/aoms/1177704711",
   "why": "data analysis as its own science: procedures for analysing data, ways to interpret their results, and plans for gathering data"
  },
  {
   "group": "all methods (question-answering)",
   "role": "review",
   "key": false,
   "paper": "Donoho 2017 · 50 years of data science",
   "venue": "Journal of Computational and Graphical Statistics",
   "doi": "10.1080/10618600.2017.1384734",
   "why": "data science as learning from data, from Tukey's call to Breiman's emphasis on prediction"
  },
  {
   "group": "all methods (question-answering)",
   "role": "classic",
   "key": false,
   "paper": "Ioannidis 2005 · Why most published research findings are false",
   "venue": "PLoS Medicine",
   "doi": "10.1371/journal.pmed.0020124",
   "why": "a finding is less likely true when effects are small, many relationships are tested and designs, outcomes and analyses are flexible"
  },
  {
   "group": "all methods (question-answering)",
   "role": "review",
   "key": false,
   "paper": "Gelman & Loken 2014 · The statistical crisis in science",
   "venue": "American Scientist",
   "doi": "10.1511/2014.111.460",
   "why": "the garden of forking paths: choices made after seeing the data make a result look stronger than it is"
  },
  {
   "group": "all methods (question-answering)",
   "role": "evidence",
   "key": true,
   "paper": "Majumder, Surana, Agarwal et al. 2024 · DiscoveryBench: towards data-driven discovery with large language models",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2407.01725",
   "why": "264 discovery tasks from published papers, each a dataset, its metadata and a goal; the best LLM system scores only 25%"
  },
  {
   "group": "all methods (question-answering)",
   "role": "evidence",
   "key": false,
   "paper": "Chen, Chen, Ning et al. 2024 · ScienceAgentBench: toward rigorous assessment of language agents for data-driven scientific discovery",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2410.05080",
   "why": "102 tasks from 44 publications; the best agent solves 32.4% alone and 34.3% with expert knowledge"
  },
  {
   "group": "by exploring",
   "role": "classic",
   "key": true,
   "paper": "Tukey 1977 · Exploratory Data Analysis",
   "venue": "Addison-Wesley",
   "doi": "",
   "why": "look at the data first, with simple displays and summaries, before any model"
  },
  {
   "group": "by exploring",
   "role": "review",
   "key": false,
   "paper": "Behrens 1997 · Principles and procedures of exploratory data analysis",
   "venue": "Psychological Methods",
   "doi": "10.1037/1082-989X.2.2.131",
   "why": "the heuristics and tools of exploratory analysis, and how they complement confirmatory tests"
  },
  {
   "group": "by exploring",
   "role": "review",
   "key": false,
   "paper": "Battle & Heer 2019 · Characterizing exploratory visual analysis: a literature review and evaluation of analytic provenance in Tableau",
   "venue": "Computer Graphics Forum",
   "doi": "10.1111/cgf.13678",
   "why": "a definition of exploratory visual analysis; 27 analysts on 3 datasets were over 80% accurate on focused tasks and overlapped in what they did"
  },
  {
   "group": "by exploring",
   "role": "evidence",
   "key": true,
   "paper": "Zgraggen, Zhao, Zeleznik & Kraska 2018 · Investigating the effect of the multiple comparisons problem in visual analysis",
   "venue": "Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems",
   "doi": "10.1145/3173574.3174053",
   "why": "on synthetic data with known truth, over 60% of the insights users reported while exploring were false"
  },
  {
   "group": "by exploring",
   "role": "review",
   "key": false,
   "paper": "Pu & Kay 2018 · The garden of forking paths in visualization: a design space for reliable exploratory visual analytics",
   "venue": "2018 IEEE Evaluation and Beyond: Methodological Approaches for Visualization (BELIV)",
   "doi": "10.1109/beliv.2018.8634103",
   "why": "taking exploratory findings as confirmatory is the forking paths problem; correction and regularization as remedies"
  },
  {
   "group": "by exploring",
   "role": "review",
   "key": false,
   "paper": "Hullman & Gelman 2021 · Designing for interactive exploratory data analysis requires theories of graphical inference",
   "venue": "Harvard Data Science Review",
   "doi": "10.1162/99608f92.3ab8a587",
   "why": "exploration is not model free: a look at the data is a model check that compares it to a reference distribution"
  },
  {
   "group": "by automated insight search",
   "role": "classic",
   "key": true,
   "paper": "Tang, Han, Yiu et al. 2017 · Extracting top-k insights from multi-dimensional data",
   "venue": "Proceedings of the 2017 ACM International Conference on Management of Data (SIGMOD)",
   "doi": "10.1145/3035918.3035922",
   "why": "an insight as an interesting observation from aggregates over several steps; a search returns the top k"
  },
  {
   "group": "by automated insight search",
   "role": "classic",
   "key": false,
   "paper": "Vartak, Rahman, Madden et al. 2015 · SeeDB: efficient data-driven visualization recommendations to support visual analytics",
   "venue": "Proceedings of the VLDB Endowment",
   "doi": "10.14778/2831360.2831371",
   "why": "rank candidate views of a data subset by how far they deviate from a reference, and show the most interesting"
  },
  {
   "group": "by automated insight search",
   "role": "evidence",
   "key": false,
   "paper": "Ding, Han, Xu et al. 2019 · QuickInsights: quick and automatic discovery of insights from multi-dimensional data",
   "venue": "Proceedings of the 2019 International Conference on Management of Data (SIGMOD)",
   "doi": "10.1145/3299869.3314037",
   "why": "one formulation of insight types and a mining framework, evaluated on 447 real datasets and with expert and non-expert users"
  },
  {
   "group": "by automated insight search",
   "role": "review",
   "key": false,
   "paper": "Law, Endert & Stasko 2020 · Characterizing automated data insights",
   "venue": "2020 IEEE Visualization Conference (VIS)",
   "doi": "10.1109/VIS47514.2020.00041",
   "why": "a systematic review of insight-recommending tools: 12 types of automated insight and four purposes"
  },
  {
   "group": "by automated insight search",
   "role": "evidence",
   "key": false,
   "paper": "Ma, Ding, Wang et al. 2023 · InsightPilot: an LLM-empowered automated data exploration system",
   "venue": "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
   "doi": "10.18653/v1/2023.emnlp-demo.31",
   "why": "an LLM issues a sequence of analysis actions from a question and returns insights; a user study and a case study"
  },
  {
   "group": "by automated insight search",
   "role": "evidence",
   "key": true,
   "paper": "Sahu, Puri, Rodriguez et al. 2024 · InsightBench: evaluating business analytics agents through multi-step insight generation",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2407.06423",
   "why": "100 datasets with planted insights; agents are scored on end-to-end analysis, from posing questions to a summary of insights"
  },
  {
   "group": "by pattern mining",
   "role": "classic",
   "key": true,
   "paper": "Fayyad, Piatetsky-Shapiro & Smyth 1996 · From data mining to knowledge discovery in databases",
   "venue": "AI Magazine",
   "doi": "10.1609/aimag.v17i3.1230",
   "why": "the knowledge discovery process, of which mining patterns is one step among selection, preprocessing and interpretation"
  },
  {
   "group": "by pattern mining",
   "role": "classic",
   "key": false,
   "paper": "Agrawal, Imieliński & Swami 1993 · Mining association rules between sets of items in large databases",
   "venue": "Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data",
   "doi": "10.1145/170035.170072",
   "why": "find every association rule between items in a large transaction database"
  },
  {
   "group": "by pattern mining",
   "role": "classic",
   "key": false,
   "paper": "Webb 2007 · Discovering significant patterns",
   "venue": "Machine Learning",
   "doi": "10.1007/s10994-007-5006-x",
   "why": "pattern search carries an extreme risk of false discoveries; statistical tests put a strict limit on experimentwise error"
  },
  {
   "group": "by pattern mining",
   "role": "review",
   "key": true,
   "paper": "Hämäläinen & Webb 2019 · A tutorial on statistically sound pattern discovery",
   "venue": "Data Mining and Knowledge Discovery",
   "doi": "10.1007/s10618-018-0590-x",
   "why": "test each pattern, and control false discoveries when many patterns are evaluated"
  },
  {
   "group": "by pattern mining",
   "role": "review",
   "key": false,
   "paper": "Herrera, Carmona, González & del Jesus 2011 · An overview on subgroup discovery: foundations and applications",
   "venue": "Knowledge and Information Systems",
   "doi": "10.1007/s10115-010-0356-2",
   "why": "subgroup discovery: its foundations, algorithms and applications"
  },
  {
   "group": "by pattern mining",
   "role": "review",
   "key": false,
   "paper": "Atzmueller 2015 · Subgroup discovery",
   "venue": "WIREs Data Mining and Knowledge Discovery",
   "doi": "10.1002/widm.1144",
   "why": "subgroup discovery as a pattern mining method for interesting subgroups of a target"
  },
  {
   "group": "by question type",
   "role": "classic",
   "key": true,
   "paper": "Leek & Peng 2015 · What is the question?",
   "venue": "Science",
   "doi": "10.1126/science.aaa6146",
   "why": "six question types (descriptive, exploratory, inferential, predictive, causal, mechanistic); mistaking the type is the most common error in data analysis"
  },
  {
   "group": "by question type",
   "role": "classic",
   "key": true,
   "paper": "Hernán, Hsu & Healy 2019 · A second chance to get causal inference right: a classification of data science tasks",
   "venue": "CHANCE",
   "doi": "10.1080/09332480.2019.1579578",
   "why": "three data science tasks: description, prediction and counterfactual prediction (causal inference); causal analysis also needs expert knowledge"
  },
  {
   "group": "by question type",
   "role": "evidence",
   "key": false,
   "paper": "Jun, Birchfield, De Moura et al. 2022 · Hypothesis formalization: empirical findings, software limitations, and design implications",
   "venue": "ACM Transactions on Computer-Human Interaction",
   "doi": "10.1145/3476980",
   "why": "in a lab study, analysts fixed on implementation and fit their analyses to familiar approaches, even when sub-optimal"
  },
  {
   "group": "by question type",
   "role": "evidence",
   "key": false,
   "paper": "Hu, Zhao, Wei et al. 2024 · InfiAgent-DABench: evaluating agents on data analysis tasks",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2401.05507",
   "why": "257 data analysis questions on 52 files, put in closed form so 34 LLMs could be scored automatically"
  },
  {
   "group": "by model comparison",
   "role": "classic",
   "key": true,
   "paper": "Breiman 2001 · Statistical modeling: the two cultures",
   "venue": "Statistical Science",
   "doi": "10.1214/ss/1009213726",
   "why": "a data model assumes how the data were generated; an algorithmic model treats it as unknown and is judged by prediction"
  },
  {
   "group": "by model comparison",
   "role": "classic",
   "key": true,
   "paper": "Shmueli 2010 · To explain or to predict?",
   "venue": "Statistical Science",
   "doi": "10.1214/10-STS330",
   "why": "explanatory and predictive modelling differ at every step; high explanatory power does not imply high predictive power"
  },
  {
   "group": "by model comparison",
   "role": "review",
   "key": false,
   "paper": "Yarkoni & Westfall 2017 · Choosing prediction over explanation in psychology: lessons from machine learning",
   "venue": "Perspectives on Psychological Science",
   "doi": "10.1177/1745691617693393",
   "why": "intricate mechanism theories often have little or unknown predictive accuracy; machine learning tools can test it"
  },
  {
   "group": "by model comparison",
   "role": "review",
   "key": false,
   "paper": "Hofman, Watts, Athey et al. 2021 · Integrating explanation and prediction in computational social science",
   "venue": "Nature",
   "doi": "10.1038/s41586-021-03659-0",
   "why": "how explanation and prediction approaches differ, and how to combine them"
  },
  {
   "group": "by model comparison",
   "role": "evidence",
   "key": false,
   "paper": "Salganik, Lundberg, Kindel et al. 2020 · Measuring the predictability of life outcomes with a scientific mass collaboration",
   "venue": "Proceedings of the National Academy of Sciences",
   "doi": "10.1073/pnas.1915006117",
   "why": "160 teams predicted six outcomes; the best were only slightly better than a simple benchmark"
  },
  {
   "group": "by model comparison",
   "role": "evidence",
   "key": false,
   "paper": "Jing, Huang, Wang et al. 2024 · DSBench: how far are data science agents from becoming data science experts?",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2409.07703",
   "why": "466 analysis and 74 modelling tasks; the best agent solves 34.12% of the analysis tasks"
  },
  {
   "group": "by hypothesis test",
   "role": "classic",
   "key": true,
   "paper": "Neyman & Pearson 1933 · On the problem of the most efficient tests of statistical hypotheses",
   "venue": "Philosophical Transactions of the Royal Society of London. Series A",
   "doi": "10.1098/rsta.1933.0009",
   "why": "a test fixes its error rate against a stated alternative before the data decide"
  },
  {
   "group": "by hypothesis test",
   "role": "classic",
   "key": true,
   "paper": "Wagenmakers, Wetzels, Borsboom et al. 2012 · An agenda for purely confirmatory research",
   "venue": "Perspectives on Psychological Science",
   "doi": "10.1177/1745691612463078",
   "why": "only analyses stated in advance are confirmatory, and only for them are the usual tests valid"
  },
  {
   "group": "by hypothesis test",
   "role": "classic",
   "key": false,
   "paper": "Benjamini & Hochberg 1995 · Controlling the false discovery rate: a practical and powerful approach to multiple testing",
   "venue": "Journal of the Royal Statistical Society Series B",
   "doi": "10.1111/j.2517-6161.1995.tb02031.x",
   "why": "control the expected share of false discoveries when many tests are run"
  },
  {
   "group": "by hypothesis test",
   "role": "review",
   "key": false,
   "paper": "Wasserstein & Lazar 2016 · The ASA statement on p-values: context, process, and purpose",
   "venue": "The American Statistician",
   "doi": "10.1080/00031305.2016.1154108",
   "why": "what a p-value does and does not say"
  },
  {
   "group": "by hypothesis test",
   "role": "evidence",
   "key": true,
   "paper": "Button, Ioannidis, Mokrysz et al. 2013 · Power failure: why small sample size undermines the reliability of neuroscience",
   "venue": "Nature Reviews Neuroscience",
   "doi": "10.1038/nrn3475",
   "why": "low power lowers the chance that a significant result is true, and inflates effect sizes"
  },
  {
   "group": "by hypothesis test",
   "role": "evidence",
   "key": false,
   "paper": "Scheel, Schijen & Lakens 2021 · An excess of positive results: comparing the standard psychology literature with registered reports",
   "venue": "Advances in Methods and Practices in Psychological Science",
   "doi": "10.1177/25152459211007467",
   "why": "96% positive first hypotheses in standard reports against 44% in registered reports"
  },
  {
   "group": "by hypothesis test",
   "role": "evidence",
   "key": false,
   "paper": "Huang, Jin, Li et al. 2025 · Automated hypothesis validation with agentic sequential falsifications",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2502.09858",
   "why": "LLM agents design falsification tests for a hypothesis under sequential Type-I error control, in six domains"
  },
  {
   "group": "by multiverse",
   "role": "classic",
   "key": true,
   "paper": "Steegen, Tuerlinckx, Gelman & Vanpaemel 2016 · Increasing transparency through a multiverse analysis",
   "venue": "Perspectives on Psychological Science",
   "doi": "10.1177/1745691616658637",
   "why": "run the analysis on every reasonably processed dataset and see how much the conclusion moves"
  },
  {
   "group": "by multiverse",
   "role": "classic",
   "key": true,
   "paper": "Simonsohn, Simmons & Nelson 2020 · Specification curve analysis",
   "venue": "Nature Human Behaviour",
   "doi": "10.1038/s41562-020-0912-z",
   "why": "list the justified specifications, plot their results and infer jointly; of three findings, one was robust, one weak, one not robust"
  },
  {
   "group": "by multiverse",
   "role": "evidence",
   "key": false,
   "paper": "Simmons, Nelson & Simonsohn 2011 · False-positive psychology: undisclosed flexibility in data collection and analysis allows presenting anything as significant",
   "venue": "Psychological Science",
   "doi": "10.1177/0956797611417632",
   "why": "flexibility in collection, analysis and reporting greatly raises the false-positive rate, in simulations and two experiments"
  },
  {
   "group": "by multiverse",
   "role": "evidence",
   "key": false,
   "paper": "Silberzahn, Uhlmann, Martin et al. 2018 · Many analysts, one data set: making transparent how variations in analytic choices affect results",
   "venue": "Advances in Methods and Practices in Psychological Science",
   "doi": "10.1177/2515245917747646",
   "why": "29 teams, one question: odds ratios from 0.89 to 2.93, and 20 of 29 found a significant effect"
  },
  {
   "group": "by multiverse",
   "role": "evidence",
   "key": false,
   "paper": "Botvinik-Nezer, Holzmeister, Camerer et al. 2020 · Variability in the analysis of a single neuroimaging dataset by many teams",
   "venue": "Nature",
   "doi": "10.1038/s41586-020-2314-9",
   "why": "70 teams, 9 hypotheses: no two workflows alike, and sizeable variation in the tests' results"
  },
  {
   "group": "by multiverse",
   "role": "evidence",
   "key": false,
   "paper": "Breznau, Rinke, Wuttke et al. 2022 · Observing many researchers using the same data and hypothesis reveals a hidden universe of uncertainty",
   "venue": "Proceedings of the National Academy of Sciences",
   "doi": "10.1073/pnas.2203150119",
   "why": "73 teams diverged in numbers and conclusions; over 95% of the variance stayed unexplained by their coded decisions"
  },
  {
   "group": "by multiverse",
   "role": "classic",
   "key": false,
   "paper": "Liu, Kale, Althoff & Heer 2021 · Boba: authoring and visualizing multiverse analyses",
   "venue": "IEEE Transactions on Visualization and Computer Graphics",
   "doi": "10.1109/TVCG.2020.3028985",
   "why": "write the shared analysis once with its alternative decisions, and compile every path into a script"
  },
  {
   "group": "by multiverse",
   "role": "evidence",
   "key": false,
   "paper": "Gu, Shang, Jiang et al. 2024 · BLADE: benchmarking language model agents for data-driven science",
   "venue": "Findings of the Association for Computational Linguistics: EMNLP 2024",
   "doi": "10.18653/v1/2024.findings-emnlp.815",
   "why": "12 research questions with expert analyses as ground truth; agents often stop at basic analyses and their analytic decisions are not diverse enough"
  },
  {
   "group": "by heterogeneity",
   "role": "classic",
   "key": true,
   "paper": "Gelman & Stern 2006 · The difference between \"significant\" and \"not significant\" is not itself statistically significant",
   "venue": "The American Statistician",
   "doi": "10.1198/000313006X152649",
   "why": "a significant effect in one group and none in another is not evidence that the groups differ"
  },
  {
   "group": "by heterogeneity",
   "role": "review",
   "key": true,
   "paper": "Kent, Paulus, van Klaveren et al. 2020 · The Predictive Approaches to Treatment effect Heterogeneity (PATH) statement",
   "venue": "Annals of Internal Medicine",
   "doi": "10.7326/M18-3667",
   "why": "one variable at a time subgroups against risk modelling and effect modelling of heterogeneity"
  },
  {
   "group": "by heterogeneity",
   "role": "review",
   "key": false,
   "paper": "Rothwell 2005 · Subgroup analysis in randomised controlled trials: importance, indications, and interpretation",
   "venue": "The Lancet",
   "doi": "10.1016/S0140-6736(05)17709-5",
   "why": "subgroup analyses predefined, justified and few; post-hoc ones treated with scepticism"
  },
  {
   "group": "by heterogeneity",
   "role": "review",
   "key": false,
   "paper": "Sun, Briel, Walter & Guyatt 2010 · Is a subgroup effect believable? Updating criteria to evaluate the credibility of subgroup analyses",
   "venue": "BMJ",
   "doi": "10.1136/bmj.c117",
   "why": "a checklist for judging whether a subgroup effect is real"
  },
  {
   "group": "by heterogeneity",
   "role": "classic",
   "key": false,
   "paper": "Wager & Athey 2018 · Estimation and inference of heterogeneous treatment effects using random forests",
   "venue": "Journal of the American Statistical Association",
   "doi": "10.1080/01621459.2017.1319839",
   "why": "causal forests estimate effect heterogeneity with valid confidence intervals"
  },
  {
   "group": "by heterogeneity",
   "role": "evidence",
   "key": false,
   "paper": "Wallach, Sullivan, Trepanowski et al. 2017 · Evaluation of evidence of statistical support and corroboration of subgroup claims in randomized clinical trials",
   "venue": "JAMA Internal Medicine",
   "doi": "10.1001/jamainternmed.2016.9125",
   "why": "of 117 subgroup claims, 46 had a significant interaction test; all 5 later corroboration attempts found no subgroup effect"
  },
  {
   "group": "by sensemaking",
   "role": "classic",
   "key": true,
   "paper": "Pirolli & Card 2005 · The sensemaking process and leverage points for analyst technology as identified through cognitive task analysis",
   "venue": "Proceedings of the International Conference on Intelligence Analysis",
   "doi": "",
   "why": "analysts move between a foraging loop that gathers evidence and a sensemaking loop that builds and tests a story"
  },
  {
   "group": "by sensemaking",
   "role": "classic",
   "key": true,
   "paper": "Klein, Moon & Hoffman 2006 · Making sense of sensemaking 2: a macrocognitive model",
   "venue": "IEEE Intelligent Systems",
   "doi": "10.1109/MIS.2006.100",
   "why": "the data/frame model: a frame explains the data, and the data can question, elaborate or replace the frame"
  },
  {
   "group": "by sensemaking",
   "role": "classic",
   "key": false,
   "paper": "Russell, Stefik, Pirolli & Card 1993 · The cost structure of sensemaking",
   "venue": "Proceedings of the SIGCHI Conference on Human Factors in Computing Systems",
   "doi": "10.1145/169059.169209",
   "why": "sensemaking searches for a representation and encodes the data in it to answer a task's questions"
  },
  {
   "group": "by sensemaking",
   "role": "classic",
   "key": false,
   "paper": "Platt 1964 · Strong inference",
   "venue": "Science",
   "doi": "10.1126/science.146.3642.347",
   "why": "devise alternative hypotheses and the test that would exclude some of them"
  },
  {
   "group": "by sensemaking",
   "role": "classic",
   "key": false,
   "paper": "Chamberlin 1890 · The method of multiple working hypotheses",
   "venue": "Science",
   "doi": "10.1126/science.ns-15.366.92",
   "why": "hold several explanations at once rather than one favoured one"
  },
  {
   "group": "by sensemaking",
   "role": "evidence",
   "key": false,
   "paper": "Dhami, Belton & Mandel 2019 · The \"analysis of competing hypotheses\" in intelligence analysis",
   "venue": "Applied Cognitive Psychology",
   "doi": "10.1002/acp.3550",
   "why": "50 analysts randomized: those trained in competing hypotheses skipped steps, showed mixed reduction of confirmation bias and may have been less consistent"
  },
  {
   "group": "tests (after the run)",
   "role": "classic",
   "key": false,
   "paper": "Sandve, Nekrutenko, Taylor & Hovig 2013 · Ten simple rules for reproducible computational research",
   "venue": "PLoS Computational Biology",
   "doi": "10.1371/journal.pcbi.1003285",
   "why": "T4: record how every result was produced, so the analysis can be repeated from the original data"
  },
  {
   "group": "tests (after the run)",
   "role": "classic",
   "key": false,
   "paper": "Peng 2011 · Reproducible research in computational science",
   "venue": "Science",
   "doi": "10.1126/science.1213847",
   "why": "T4: reproducibility as the minimum standard when independent replication is not possible"
  },
  {
   "group": "tests (after the run)",
   "role": "evidence",
   "key": false,
   "paper": "Maynez, Narayan, Bohnet & McDonald 2020 · On faithfulness and factuality in abstractive summarization",
   "venue": "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
   "doi": "10.18653/v1/2020.acl-main.173",
   "why": "T5: human raters found unfaithful content in all model summaries; entailment measures track faithfulness better than overlap metrics"
  },
  {
   "group": "tests (after the run)",
   "role": "evidence",
   "key": false,
   "paper": "Zheng, Chiang, Sheng et al. 2023 · Judging LLM-as-a-judge with MT-Bench and Chatbot Arena",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2306.05685",
   "why": "T6: strong LLM judges agree with human preferences over 80% of the time, but show position, verbosity and self-enhancement biases"
  },
  {
   "group": "tests (after the run)",
   "role": "evidence",
   "key": false,
   "paper": "Panickssery, Bowman & Feng 2024 · LLM evaluators recognize and favor their own generations",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2404.13076",
   "why": "T6: an LLM evaluator scores its own outputs higher than others' that human raters judge equal, and can tell its own outputs apart"
  },
  {
   "group": "tests (after the run)",
   "role": "evidence",
   "key": false,
   "paper": "Huang, Chen, Mishra et al. 2023 · Large language models cannot self-correct reasoning yet",
   "venue": "arXiv",
   "doi": "10.48550/arXiv.2310.01798",
   "why": "T6: without outside feedback, models struggle to correct their own reasoning and sometimes get worse"
  },
  {
   "group": "tests (after the run)",
   "role": "evidence",
   "key": true,
   "paper": "Open Science Collaboration 2015 · Estimating the reproducibility of psychological science",
   "venue": "Science",
   "doi": "10.1126/science.aac4716",
   "why": "T8: 97% of 100 original studies were significant, 36% of their replications; effects halved"
  },
  {
   "group": "tests (after the run)",
   "role": "evidence",
   "key": false,
   "paper": "Camerer, Dreber, Holzmeister et al. 2018 · Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015",
   "venue": "Nature Human Behaviour",
   "doi": "10.1038/s41562-018-0399-z",
   "why": "T8: 13 of 21 replicated in the same direction, at about half the original effect size"
  },
  {
   "group": "all methods (question-asking)",
   "role": "review",
   "key": false,
   "paper": "Munafò, Nosek, Bishop et al. 2017 · A manifesto for reproducible science",
   "venue": "Nature Human Behaviour",
   "doi": "10.1038/s41562-016-0021",
   "why": "measures across methods, reporting, reproducibility, evaluation and incentives, preregistration among them"
  },
  {
   "group": "all methods (question-asking)",
   "role": "evidence",
   "key": false,
   "paper": "Gu, Shang, Althoff, Wang & Drucker 2024 · How do analysts understand and verify AI-assisted data analyses?",
   "venue": "Proceedings of the CHI Conference on Human Factors in Computing Systems",
   "doi": "10.1145/3613904.3642497",
   "why": "a qualitative study (n=22) of how analysts check AI-generated analyses that can look right and mislead"
  },
  {
   "group": "by level",
   "role": "classic",
   "key": true,
   "paper": "Ackoff 1989 · From data to wisdom",
   "venue": "Journal of Applied Systems Analysis",
   "doi": "",
   "why": "the hierarchy of data, information, knowledge, understanding and wisdom"
  },
  {
   "group": "by level",
   "role": "review",
   "key": true,
   "paper": "Rowley 2007 · The wisdom hierarchy: representations of the DIKW hierarchy",
   "venue": "Journal of Information Science",
   "doi": "10.1177/0165551506070706",
   "why": "how textbooks define each DIKW level, and where they agree and dissent"
  },
  {
   "group": "by level",
   "role": "review",
   "key": false,
   "paper": "Frické 2009 · The knowledge pyramid: a critique of the DIKW hierarchy",
   "venue": "Journal of Information Science",
   "doi": "10.1177/0165551508094050",
   "why": "argues the hierarchy is unsound and methodologically undesirable; the method's limit"
  },
  {
   "group": "by level",
   "role": "classic",
   "key": false,
   "paper": "Hernán 2018 · The C-word: scientific euphemisms do not improve causal inference from observational data",
   "venue": "American Journal of Public Health",
   "doi": "10.2105/AJPH.2018.304337",
   "why": "say a causal goal openly rather than hide it behind \"association\"; why a causal ask is routed, not reworded"
  },
  {
   "group": "by level",
   "role": "evidence",
   "key": false,
   "paper": "Haber, Wieten, Rohrer et al. 2022 · Causal and associational language in observational health research: a systematic evaluation",
   "venue": "American Journal of Epidemiology",
   "doi": "10.1093/aje/kwac137",
   "why": "1,170 articles: linking words read as causal to different degrees, recommendations often more causal than the finding"
  },
  {
   "group": "by level",
   "role": "evidence",
   "key": false,
   "paper": "Yu, Li & Wang 2019 · Detecting causal language use in science findings",
   "venue": "Proceedings of EMNLP-IJCNLP 2019",
   "doi": "10.18653/v1/D19-1473",
   "why": "a BERT classifier of causal language (accuracy 0.90); 32.4% of 38,000 observational conclusions used some direct causal language"
  },
  {
   "group": "by goal-question-metric",
   "role": "classic",
   "key": true,
   "paper": "Basili, Caldiera & Rombach 1994 · The goal question metric approach",
   "venue": "Encyclopedia of Software Engineering (Wiley)",
   "doi": "",
   "why": "goal, question, metric: measurement defined top down from a stated goal"
  },
  {
   "group": "by goal-question-metric",
   "role": "review",
   "key": false,
   "paper": "van Solingen, Basili, Caldiera & Rombach 2002 · Goal Question Metric (GQM) approach",
   "venue": "Encyclopedia of Software Engineering",
   "doi": "10.1002/0471028959.sof142",
   "why": "the method's later entry: why metric-driven bottom-up measurement does not work"
  },
  {
   "group": "by goal-question-metric",
   "role": "classic",
   "key": false,
   "paper": "Basili & Weiss 1984 · A methodology for collecting valid software engineering data",
   "venue": "IEEE Transactions on Software Engineering",
   "doi": "10.1109/TSE.1984.5010301",
   "why": "goal-directed data collection: the claims to test set the goals and the questions"
  },
  {
   "group": "by goal-question-metric",
   "role": "review",
   "key": false,
   "paper": "Basili, Lindvall, Regardie, Seaman et al. 2010 · Linking software development and business strategy through measurement",
   "venue": "Computer",
   "doi": "10.1109/MC.2010.108",
   "why": "GQM+Strategies: measurement goals tied to organisational goals and strategies"
  },
  {
   "group": "by goal-question-metric",
   "role": "evidence",
   "key": false,
   "paper": "van Solingen & Berghout 2001 · Integrating goal-oriented measurement in industrial software engineering: industrial experiences with and additions to the Goal/Question/Metric method (GQM)",
   "venue": "Proceedings Seventh International Software Metrics Symposium",
   "doi": "10.1109/metric.2001.915533",
   "why": "industrial experience with the method"
  },
  {
   "group": "by estimand",
   "role": "classic",
   "key": true,
   "paper": "Lundberg, Johnson & Stewart 2021 · What is your estimand? Defining the target quantity connects statistical evidence to theory",
   "venue": "American Sociological Review",
   "doi": "10.1177/00031224211004187",
   "why": "state the theoretical estimand outside any model, link it to an empirical one, then learn from data"
  },
  {
   "group": "by estimand",
   "role": "classic",
   "key": true,
   "paper": "ICH 2019 · E9(R1) addendum on estimands and sensitivity analysis in clinical trials to the guideline on statistical principles for clinical trials",
   "venue": "International Council for Harmonisation",
   "doi": "",
   "why": "the estimand framework: population, treatment, variable, intercurrent events, summary"
  },
  {
   "group": "by estimand",
   "role": "review",
   "key": false,
   "paper": "Kahan, Hindley, Edwards et al. 2024 · The estimands framework: a primer on the ICH E9(R1) addendum",
   "venue": "BMJ",
   "doi": "10.1136/bmj-2023-076316",
   "why": "a primer on the framework and its five attributes"
  },
  {
   "group": "by estimand",
   "role": "review",
   "key": false,
   "paper": "Petersen & van der Laan 2014 · Causal models and learning from data: integrating causal modeling and statistical estimation",
   "venue": "Epidemiology",
   "doi": "10.1097/EDE.0000000000000078",
   "why": "the causal roadmap: from question to causal model to estimand to estimate"
  },
  {
   "group": "by estimand",
   "role": "evidence",
   "key": false,
   "paper": "Kahan, Morris, White et al. 2021 · Estimands in published protocols of randomised trials: urgent improvement needed",
   "venue": "Trials",
   "doi": "10.1186/s13063-021-05644-4",
   "why": "none of 50 protocols stated the primary estimand; 74% could not be inferred"
  },
  {
   "group": "by estimand",
   "role": "evidence",
   "key": false,
   "paper": "Cro, Kahan, Rehal et al. 2022 · Evaluating how clear the questions being investigated in randomised trials are: systematic review of estimands",
   "venue": "BMJ",
   "doi": "10.1136/bmj-2022-070146",
   "why": "of 255 trials none stated every attribute; the primary estimand could be determined in 46%"
  },
  {
   "group": "by target trial",
   "role": "classic",
   "key": true,
   "paper": "Hernán & Robins 2016 · Using big data to emulate a target trial when a randomized trial is not available",
   "venue": "American Journal of Epidemiology",
   "doi": "10.1093/aje/kwv254",
   "why": "make the target trial explicit and emulate it with observational data"
  },
  {
   "group": "by target trial",
   "role": "classic",
   "key": false,
   "paper": "Hernán, Sauer, Hernández-Díaz et al. 2016 · Specifying a target trial prevents immortal time bias and other self-inflicted injuries in observational analyses",
   "venue": "Journal of Clinical Epidemiology",
   "doi": "10.1016/j.jclinepi.2016.04.014",
   "why": "align eligibility, assignment and the start of follow-up"
  },
  {
   "group": "by target trial",
   "role": "review",
   "key": false,
   "paper": "Cashin, Hansford, Hernán et al. 2025 · Transparent reporting of observational studies emulating a target trial: the TARGET statement",
   "venue": "JAMA",
   "doi": "10.1001/jama.2025.13350",
   "why": "the consensus reporting guideline for target trial emulation"
  },
  {
   "group": "by target trial",
   "role": "evidence",
   "key": false,
   "paper": "Hansford, Cashin, Jones et al. 2023 · Reporting of observational studies explicitly aiming to emulate randomized trials: a systematic review",
   "venue": "JAMA Network Open",
   "doi": "10.1001/jamanetworkopen.2023.36023",
   "why": "200 studies; 57% did not describe the target trial protocol and its emulation"
  },
  {
   "group": "by target trial",
   "role": "evidence",
   "key": true,
   "paper": "Wang, Schneeweiss, RCT-DUPLICATE Initiative et al. 2023 · Emulation of randomized clinical trials with nonrandomized database analyses: results of 32 clinical trials",
   "venue": "JAMA",
   "doi": "10.1001/jama.2023.4221",
   "why": "agreement with 32 trials: r = 0.82 overall, 0.93 when emulated closely, 0.53 when not"
  },
  {
   "group": "by target trial",
   "role": "evidence",
   "key": false,
   "paper": "Kim, Kim, Kim & You 2026 · From study design to executable code: automating target trial emulation with large language models",
   "venue": "JAMIA Open",
   "doi": "10.1093/jamiaopen/ooag131",
   "why": "8 language models turned study descriptions into structured specifications and code; accuracy 0.93 to 0.97 in a common data model"
  },
  {
   "group": "by analysis plan",
   "role": "review",
   "key": true,
   "paper": "Nosek, Ebersole, DeHaven & Mellor 2018 · The preregistration revolution",
   "venue": "Proceedings of the National Academy of Sciences",
   "doi": "10.1073/pnas.1708274114",
   "why": "define the questions and the analysis plan before observing outcomes"
  },
  {
   "group": "by analysis plan",
   "role": "classic",
   "key": false,
   "paper": "Kerr 1998 · HARKing: hypothesizing after the results are known",
   "venue": "Personality and Social Psychology Review",
   "doi": "10.1207/s15327957pspr0203_4",
   "why": "names the practice a plan written first prevents"
  },
  {
   "group": "by analysis plan",
   "role": "evidence",
   "key": true,
   "paper": "Kaplan & Irvin 2015 · Likelihood of null effects of large NHLBI clinical trials has increased over time",
   "venue": "PLOS ONE",
   "doi": "10.1371/journal.pone.0132382",
   "why": "trials showing a benefit fell from 17 of 30 to 2 of 25 once outcomes had to be registered first"
  },
  {
   "group": "by analysis plan",
   "role": "evidence",
   "key": false,
   "paper": "Claesen, Gomes, Tuerlinckx & Vanpaemel 2021 · Comparing dream to reality: an assessment of adherence of the first generation of preregistered studies",
   "venue": "Royal Society Open Science",
   "doi": "10.1098/rsos.211037",
   "why": "2 of 27 preregistered studies had no deviations; 9 disclosed none"
  },
  {
   "group": "by analysis plan",
   "role": "evidence",
   "key": false,
   "paper": "Sarafoglou, Hoogeveen & Wagenmakers 2023 · Comparing analysis blinding with preregistration in the many-analysts religion project",
   "venue": "Advances in Methods and Practices in Psychological Science",
   "doi": "10.1177/25152459221128319",
   "why": "120 teams: planning on blinded data gave fewer deviations than preregistration, for the same time"
  },
  {
   "group": "by segment and power",
   "role": "review",
   "key": true,
   "paper": "Schandelmaier, Briel, Varadhan et al. 2020 · Development of the Instrument to assess the Credibility of Effect Modification Analyses (ICEMAN) in randomized controlled trials and meta-analyses",
   "venue": "Canadian Medical Association Journal",
   "doi": "10.1503/cmaj.200077",
   "why": "5 core questions for trials, 8 for meta-analyses, to rate a claimed effect modification"
  },
  {
   "group": "by segment and power",
   "role": "evidence",
   "key": false,
   "paper": "Sun, Briel, Busse et al. 2012 · Credibility of claims of subgroup effects in randomised controlled trials: systematic review",
   "venue": "BMJ",
   "doi": "10.1136/bmj.e1553",
   "why": "of 64 subgroup claims, 84% met four or fewer of 10 credibility criteria"
  },
  {
   "group": "by protocol reuse",
   "role": "classic",
   "key": true,
   "paper": "Hripcsak, Duke, Shah et al. 2015 · Observational Health Data Sciences and Informatics (OHDSI): opportunities for observational researchers",
   "venue": "Studies in Health Technology and Informatics",
   "doi": "10.3233/978-1-61499-564-7-574",
   "why": "an open network of databases on one common data model, so one protocol runs everywhere"
  },
  {
   "group": "by protocol reuse",
   "role": "review",
   "key": false,
   "paper": "Schuemie, Ryan, Pratt et al. 2020 · Principles of large-scale evidence generation and evaluation across a network of databases (LEGEND)",
   "venue": "Journal of the American Medical Informatics Association",
   "doi": "10.1093/jamia/ocaa103",
   "why": "10 principles: many questions at once, prespecified, shared code, consistency across databases"
  },
  {
   "group": "by protocol reuse",
   "role": "evidence",
   "key": true,
   "paper": "Madigan, Ryan, Schuemie et al. 2013 · Evaluating the impact of database heterogeneity on observational study results",
   "venue": "American Journal of Epidemiology",
   "doi": "10.1093/aje/kwt010",
   "why": "same design, 10 databases: opposite significant estimates for 21% of drug-outcome pairs in cohort designs"
  },
  {
   "group": "by protocol reuse",
   "role": "evidence",
   "key": false,
   "paper": "Hripcsak, Ryan, Duke et al. 2016 · Characterizing treatment pathways at scale using the OHDSI network",
   "venue": "Proceedings of the National Academy of Sciences",
   "doi": "10.1073/pnas.1510502113",
   "why": "one analysis on 11 data sources in four countries; significant heterogeneity among sources"
  },
  {
   "group": "by protocol reuse",
   "role": "evidence",
   "key": false,
   "paper": "Suchard, Schuemie, Krumholz et al. 2019 · Comprehensive comparative effectiveness and safety of first-line antihypertensive drug classes: a systematic, multinational, large-scale analysis",
   "venue": "The Lancet",
   "doi": "10.1016/S0140-6736(19)32317-7",
   "why": "one network study: 22,000 calibrated hazard ratios across classes, outcomes and databases"
  },
  {
   "group": "by protocol reuse",
   "role": "evidence",
   "key": false,
   "paper": "Klein, Vianello, Hasselman et al. 2018 · Many Labs 2: investigating variation in replicability across samples and settings",
   "venue": "Advances in Methods and Practices in Psychological Science",
   "doi": "10.1177/2515245918810225",
   "why": "28 protocols reviewed in advance, run across 125 samples; heterogeneity in 39% of effects"
  },
  {
   "group": "tests (before the run)",
   "role": "classic",
   "key": false,
   "paper": "Gotel & Finkelstein 1994 · An analysis of the requirements traceability problem",
   "venue": "Proceedings of IEEE International Conference on Requirements Engineering",
   "doi": "10.1109/ICRE.1994.292398",
   "why": "T0: trace every requirement to what meets it"
  },
  {
   "group": "tests (before the run)",
   "role": "review",
   "key": true,
   "paper": "Gamble, Krishan, Stocken et al. 2017 · Guidelines for the content of statistical analysis plans in clinical trials",
   "venue": "JAMA",
   "doi": "10.1001/jama.2017.18556",
   "why": "T1: the minimum content of an analysis plan"
  },
  {
   "group": "tests (before the run)",
   "role": "review",
   "key": false,
   "paper": "Chan, Tetzlaff, Altman et al. 2013 · SPIRIT 2013 statement: defining standard protocol items for clinical trials",
   "venue": "Annals of Internal Medicine",
   "doi": "10.7326/0003-4819-158-3-201302050-00583",
   "why": "T1: a 33-item checklist of what a protocol must say"
  },
  {
   "group": "tests (before the run)",
   "role": "evidence",
   "key": false,
   "paper": "Jafari, Chu, Lange et al. 2026 · From protocol to analysis plan: development and validation of a large language model pipeline for statistical analysis plan generation using artificial intelligence (SAPAI)",
   "venue": "medRxiv (preprint)",
   "doi": "10.64898/2026.03.19.26348626",
   "why": "T1 by AI: drafts scored 77% to 78% overall, 67% to 72% on statistical items, with invented sensitivity analyses"
  },
  {
   "group": "tests (before the run)",
   "role": "classic",
   "key": true,
   "paper": "Chambers 2013 · Registered Reports: a new publishing initiative at Cortex",
   "venue": "Cortex",
   "doi": "10.1016/j.cortex.2012.12.016",
   "why": "T2: the design is reviewed and agreed before results exist"
  },
  {
   "group": "tests (before the run)",
   "role": "classic",
   "key": false,
   "paper": "Cohen 1992 · A power primer",
   "venue": "Psychological Bulletin",
   "doi": "10.1037/0033-2909.112.1.155",
   "why": "T3: conventional effect sizes and the sample each needs"
  },
  {
   "group": "tests (before the run)",
   "role": "review",
   "key": false,
   "paper": "Lakens 2022 · Sample size justification",
   "venue": "Collabra: Psychology",
   "doi": "10.1525/collabra.33267",
   "why": "T3: justify n from the smallest effect size of interest"
  }
 ],
 "roadmap": [
  {
   "name": "Spaces, runs and skills",
   "png": "img/roadmap-1.png",
   "open": "/_excalidraw/?board=plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.excalidraw#Spaces, runs and skills"
  },
  {
   "name": "The workbench",
   "png": "img/roadmap-2.png",
   "open": "/_excalidraw/?board=plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.excalidraw#The workbench"
  },
  {
   "name": "Where things live",
   "png": "img/roadmap-3.png",
   "open": "/_excalidraw/?board=plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.excalidraw#Where things live"
  },
  {
   "name": "How a question is asked",
   "png": "img/roadmap-4.png",
   "open": "/_excalidraw/?board=plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.excalidraw#How a question is asked"
  }
 ],
 "methods_drawing": [
  {
   "name": "methods",
   "png": "img/methods-1.png",
   "open": "/_excalidraw/?board=plugins/haipipe-toolkit/servers/workbench-insight/guide/methods.excalidraw"
  }
 ],
 "sources": {
  "guide": "plugins/haipipe-toolkit/servers/workbench-insight/guide/guide.yaml",
  "method": "plugins/haipipe-toolkit/servers/workbench-insight/guide/method.md",
  "papers": "plugins/haipipe-toolkit/servers/workbench-insight/related/papers.md",
  "roadmap": "plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.excalidraw"
 }
};
