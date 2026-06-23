"""
Food-to-Description Pipeline Orchestrator.

Runs 4 stages in sequence:
  1. Decompose: parse food strings → components + grams
  2. Retrieve: find USDA matches via FTS5 (62.8% rank-1)
  3. LLM Rerank: Claude fixes WEAK/MISS cases (90-95% expected)
  4. Aggregate: sum nutrition, write parquet

Supports resumable execution via statusline tracking.
"""
import argparse
import collections
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

# Import stages and utilities
from stages import stage_1_decompose
from stages import stage_2_retrieve
from stages import stage_3_llm_rerank
from stages import stage_4_aggregate_writeback
from utils import Statusline, USDADatabase


class FoodToDescriptionPipeline:
    """Orchestrate food-to-description pipeline with status tracking."""

    def __init__(self, verbose: bool = False):
        self.statusline = Statusline("food-to-description")
        self.verbose = verbose
        self.food_to_fdc_id: Dict[str, Optional[int]] = {}

    def run(
        self,
        input_parquet: Path,
        output_parquet: Path,
        stages: str = "1-4",
        from_stage: Optional[int] = None
    ):
        """Run pipeline stages.

        Args:
            input_parquet: Input Diet.parquet path
            output_parquet: Output path for nutrition-filled parquet
            stages: Which stages to run, e.g., "1-4", "2-3", or "1"
            from_stage: Resume from this stage (skip prior completed ones)
        """
        # Parse stage specification
        stage_nums = self._parse_stages(stages)
        if from_stage:
            stage_nums = [s for s in stage_nums if s >= from_stage]

        print(f"📥 Loading input: {input_parquet}")
        df = pd.read_parquet(input_parquet)
        print(f"   Loaded {len(df)} meal entries")

        # Stage 1: Decompose
        if 1 in stage_nums:
            self._run_stage1(df)

        # Stage 2: Retrieve
        if 2 in stage_nums:
            self._run_stage2(df)

        # Stage 3: LLM Rerank
        if 3 in stage_nums:
            self._run_stage3()

        # Stage 4: Aggregate & Write-back
        if 4 in stage_nums:
            self._run_stage4(df, output_parquet)

        print(f"\n{self.statusline.get_dashboard()}")
        print(f"\n✅ Pipeline complete!")

    def _parse_stages(self, stages_str: str) -> list:
        """Parse stage specification like '1-4' or '2,3'."""
        if "-" in stages_str:
            start, end = map(int, stages_str.split("-"))
            return list(range(start, end + 1))
        return [int(s) for s in stages_str.split(",")]

    def _run_stage1(self, df: pd.DataFrame):
        """Stage 1: Decompose."""
        print("\n" + "=" * 70)
        print("📥 Stage 1: Decompose")
        print("=" * 70)

        self.statusline.update(1, "running")

        component_counter = collections.Counter()
        total_unparsed = 0

        for food_name in df["FoodName"]:
            components = stage_1_decompose.decompose(food_name)
            for food, amt in components:
                component_counter[food] += 1
                if amt is None:
                    total_unparsed += 1

        print(f"  Total food-lines: {sum(component_counter.values())}")
        print(f"  Unique components: {len(component_counter)}")
        print(f"  Unparsed (no g/ml): {total_unparsed}")

        self.statusline.update(
            1,
            "done",
            count=len(component_counter),
            metric=f"{len(component_counter)} unique components"
        )

    def _run_stage2(self, df: pd.DataFrame):
        """Stage 2: Retrieve USDA matches."""
        print("\n" + "=" * 70)
        print("📊 Stage 2: Retrieve (USDA FTS5 Match)")
        print("=" * 70)

        self.statusline.update(2, "running")

        # Collect all unique foods
        unique_foods = set()
        for food_name in df["FoodName"]:
            components = stage_1_decompose.decompose(food_name)
            for food, amt in components:
                unique_foods.add(food)

        # Retrieve candidates for each food
        print(f"  Retrieving {len(unique_foods)} unique foods...")
        good_count = ok_count = weak_count = miss_count = 0

        for food in sorted(unique_foods):
            cands = stage_2_retrieve.retrieve(food, k=10)
            if not cands:
                top = None
            else:
                top = cands[0]

            self.food_to_fdc_id[food] = top["fdc_id"] if top else None

            # Classify
            quality = stage_2_retrieve.classify(food, top)
            if quality == "GOOD":
                good_count += 1
            elif quality == "OK":
                ok_count += 1
            elif quality == "WEAK":
                weak_count += 1
            else:
                miss_count += 1

        total = good_count + ok_count + weak_count + miss_count
        good_pct = 100 * (good_count + ok_count) / total if total else 0

        print(f"  Results:")
        print(f"    GOOD:  {good_count:>4}")
        print(f"    OK:    {ok_count:>4}")
        print(f"    WEAK:  {weak_count:>4}")
        print(f"    MISS:  {miss_count:>4}")
        print(f"    ---")
        print(f"    Rank-1 hit rate: {good_pct:.1f}%")

        self.statusline.update(
            2,
            "done",
            count=len(unique_foods),
            metric=f"{good_pct:.1f}% rank-1 match"
        )

    def _run_stage3(self):
        """Stage 3: LLM Rerank weak/miss cases."""
        print("\n" + "=" * 70)
        print("🧠 Stage 3: LLM Rerank (Claude)")
        print("=" * 70)

        self.statusline.update(3, "running")

        # Identify WEAK/MISS foods that need reranking
        weak_miss_foods = {
            food: fdc_id
            for food, fdc_id in self.food_to_fdc_id.items()
            if fdc_id is None
        }

        print(f"  Found {len(weak_miss_foods)} WEAK/MISS foods to rerank")

        if not weak_miss_foods:
            print("  (skipping stage 3 — no weak/miss cases)")
            self.statusline.update(
                3,
                "done",
                count=0,
                metric="no weak/miss cases"
            )
            return

        # Rerank each WEAK/MISS food
        reranked = 0
        for i, food in enumerate(sorted(weak_miss_foods.keys()), 1):
            if self.verbose:
                print(f"  [{i}/{len(weak_miss_foods)}] Reranking '{food}'...")

            # Get candidates from Stage 2
            cands = stage_2_retrieve.retrieve(food, k=10)
            if not cands:
                continue

            # Use Claude to pick best
            result = stage_3_llm_rerank.rerank_via_claude(food, cands)
            if result:
                self.food_to_fdc_id[food] = result["fdc_id"]
                reranked += 1
                if self.verbose:
                    print(f"      → fdc_id={result['fdc_id']}, confidence={result['confidence']:.2f}")

        print(f"  Reranked: {reranked}/{len(weak_miss_foods)}")

        self.statusline.update(
            3,
            "done",
            count=reranked,
            metric=f"{reranked}/{len(weak_miss_foods)} reranked"
        )

    def _run_stage4(self, df: pd.DataFrame, output_parquet: Path):
        """Stage 4: Aggregate nutrition and write parquet."""
        print("\n" + "=" * 70)
        print("📤 Stage 4: Aggregate & Write-back")
        print("=" * 70)

        self.statusline.update(4, "running")

        print(f"  Aggregating nutrition for {len(df)} meals...")

        # Use Stage 4 to write parquet
        output_parquet = Path(output_parquet)
        df_result = stage_4_aggregate_writeback.write_nutrition_to_parquet(
            df.copy(),
            df["FoodName"],
            self.food_to_fdc_id,
            output_parquet
        )

        print(f"  Wrote: {output_parquet}")
        print(f"  Shape: {df_result.shape}")
        print(f"  Columns: {', '.join(df_result.columns)}")

        self.statusline.update(
            4,
            "done",
            count=len(df),
            metric=f"filled {len(df)} meal rows"
        )

    def report_status(self):
        """Print current pipeline status."""
        print(self.statusline.get_dashboard())


def main():
    parser = argparse.ArgumentParser(
        description="Food-to-Description Pipeline: Shanghai diet → USDA nutrition"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input Diet.parquet path"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output parquet path (default: input_filled.parquet)"
    )
    parser.add_argument(
        "--stages",
        default="1-4",
        help="Stages to run, e.g., '1-4', '2-3', '1' (default: 1-4)"
    )
    parser.add_argument(
        "--from-stage",
        type=int,
        default=None,
        help="Resume from this stage (skip prior completed stages)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status and exit (don't run)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    pipeline = FoodToDescriptionPipeline(verbose=args.verbose)

    if args.status:
        pipeline.report_status()
        return

    if not args.input.exists():
        print(f"❌ Input file not found: {args.input}")
        return

    output = args.output or args.input.parent / f"{args.input.stem}_filled.parquet"

    pipeline.run(
        args.input,
        output,
        stages=args.stages,
        from_stage=args.from_stage
    )


if __name__ == "__main__":
    main()
