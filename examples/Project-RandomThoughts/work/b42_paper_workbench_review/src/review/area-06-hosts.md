# 🖥️ Hosts and reliability

- **5602 hung three times in one night** · fixed 11-15 by WorkBench-Project-UI
  - Draft pages polled every 4 s, each walking the whole Task folder including results/.
  - Now results/ is skipped, the answer is shared for 3 s, and a request past 30 s logs its stack ("[slow]").
- **A Story view crash, mine** · 11-15
  - A variable name in the item-card change broke the Venues part; fixed with a regression test the same hour.
- **Files under 600 lines** · `62c6baad9`, `be94d2606`
  - The paper and Draft Lab code split by responsibility; Draft Lab now has 83 files.
