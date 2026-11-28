s01 · Landscape: Candidate landscape
=======================================================
view: overview

**Tags:** `Landscape`

## Shared question

Which failures should a model address before its deployment population changes?

| Candidate Job | Intervention or test | Main alternative explanation |
| --- | --- | --- |
| [Calibration](/_board/workbench?path=examples%2FProject-Ladder%2Fpaper%2FIdea-Example&layout=focus&section=jobs&group=j01) | Adjust predictions after a population shift | The calibration sample leaks information from evaluation |
| [Missingness](/_board/workbench?path=examples%2FProject-Ladder%2Fpaper%2FIdea-Example&layout=focus&section=jobs&group=j02) | Train against incomplete inputs | The training mask differs from deployment omissions |
| [Subgroup testing](/_board/workbench?path=examples%2FProject-Ladder%2Fpaper%2FIdea-Example&layout=focus&section=jobs&group=j11) | Evaluate prespecified population slices | Small samples produce unstable apparent gaps |

Calibration and missingness propose interventions. Subgroup testing evaluates whether an intervention helps across the intended population.
