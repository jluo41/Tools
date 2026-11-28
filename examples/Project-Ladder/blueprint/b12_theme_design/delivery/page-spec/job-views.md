A Design Board execution Job pins one goal, one signed method version and one frozen inputs version. Method, inputs version and workflow state are variants of this contract. Report combines actions and results; old Work links select the corresponding Report view. Human release approval stays at the Job.

| Category | Job Type | Use Cases | Setup | Ideas | Designs | Ranking | Release | MindMap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Design | Design Job | SMS design<br>Checklist design | 🎯 Goal<br>🧩 Method<br>📥 Inputs | 🔗 Where each design came from<br>🔗 Chains<br>💡 The ideas | ✏️ The designs, as they read | 🏆 Ranking<br>🧭 Coverage | 📄 Released designs<br>🔒 Frozen predictions<br>🎯 Predicted vs observed | 🧠 MindMap |

A Design Method Book's Job owns one method type and its signed `mK.md` versions. This is a second Job contract, not an execution Job or one Job per version. The embedded Main renders Steps, Versions and Used by from those records; the method type has no execution Tasks.

| Category | Job Type | Use Cases | Main |
| --- | --- | --- | --- |
| Design | 📘 Design method | Method development | 🪜 Steps<br>🔗 Used by |

## Embedded Jobs

The shared selector renders Job topic → Job → Main / Task topic → Task; Main hides the Task row. Design Board Jobs group by the pinned goal, with method version and inputs version on each Job button. Task topics are Ideas, Designs and Review. Method Book Jobs use an authored family when present, otherwise Methods.

Board Job Main contains Brief, Tasks, kept designs and their predictions, Ranking, observed results when recorded, the existing human approval gate when ready, Delivery when released, Workflow and Runs. Workflow retains Setup, Ideas, Designs, Ranking and Release as left tabs. Empty result sections are omitted. Task rows select the actual Task in place.

Each selected Task has its full role-specific steps as left tabs, followed by its original Runs. The open dot reaches the standalone page. Run identities, results and passes are unchanged.

A method Job Main reads its latest signed steps, frozen versions and consuming Board Jobs; proposals appear only when their front matter explicitly names this method. It creates no Tasks for the five method steps. The standalone method Job route remains the generic fallback; use [Method Main](/_board/workbench?path=examples%2FProject-Ladder%2Fdesign%2FDesignMethodBook-Example&layout=focus&section=jobs&group=j02) in the Book's Jobs section. The matrix does not offer the generic standalone fallback as its Main example.

Studio Page embeds current examples through s12-design-job.html and s13-design-task.html. Task preview links select their Task directly. Effect remains the place for pending alternatives. Browser acceptance and remaining limitations are recorded in the frontend Trace.
