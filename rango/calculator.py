from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from .standards import STANDARDS, LEVEL_ORDER, EXERCISE_NAMES



@dataclass
class CalculationResult:
    one_rm: float
    multiplier: float
    level: str          # 'elite' | 'advanced' | 'intermediate' | 'novice' | 'beginner' | 'untrained'
    label: str
    targets: dict[str, float] = field(default_factory=dict)

    def __str__(self) -> str:
        lines = [
            f"  Estimated 1RM      : {self.one_rm:.1f} kg",
            f"  Multiplyer (1RM/BW)  : {self.multiplier:.2f}x",
            f"  Strength Level     : {self.label}",
        ]
        if self.targets:
            lines.append("  Target Weights :")
            for lvl in LEVEL_ORDER:
                if lvl in self.targets:
                    marker = " <-- you are here" if lvl == self.level else ""
                    lines.append(f"    {lvl.capitalize():<14}: {self.targets[lvl]} kg{marker}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# calculate1RM
# ---------------------------------------------------------------------------

def calculate_1rm(weight: float, reps: int) -> float:

    if reps <= 1:
        return float(weight)

    if reps < 10:
        # Brzycki Formülü
        return weight / (1.0278 - 0.0278 * reps)
    else:
        # Epley Formülü
        return weight * (1 + reps / 30)


# ---------------------------------------------------------------------------
# getByBodyweight
# ---------------------------------------------------------------------------

def get_targets_by_bodyweight(
    exercise_slug: str,
    gender: str,
    bodyweight: float,
) -> dict[str, float]:

    exercise_data = STANDARDS.get(exercise_slug, {}).get(gender, {})
    if not exercise_data:
        return {}

    closest_bw = min(exercise_data.keys(), key=lambda bw: abs(bw - bodyweight))
    return exercise_data[closest_bw]


# ---------------------------------------------------------------------------
# getStrengthLevel
# ---------------------------------------------------------------------------

def get_strength_level(
    one_rm: float,
    bodyweight: float,
    exercise_slug: str,
    gender: str = "male",
) -> CalculationResult:

    if exercise_slug not in STANDARDS:
        return CalculationResult(
            one_rm=round(one_rm, 1),
            multiplier=round(one_rm / bodyweight, 2),
            level="untrained",
            label="Untrained",
        )

    targets = get_targets_by_bodyweight(exercise_slug, gender, bodyweight)
    multiplier = round(one_rm / bodyweight, 2)

    for level in LEVEL_ORDER:          # elite → beginner
        if level in targets and one_rm >= targets[level]:
            return CalculationResult(
                one_rm=round(one_rm, 1),
                multiplier=multiplier,
                level=level,
                label=level.capitalize(),
                targets=targets,
            )

    return CalculationResult(
        one_rm=round(one_rm, 1),
        multiplier=multiplier,
        level="untrained",
        label="Untrained",
        targets=targets,
    )




def calculate(
    exercise_slug: str,
    weight: float,
    reps: int,
    bodyweight: float,
    gender: str = "male",
) -> CalculationResult:

    if weight <= 0:
        raise ValueError("Weight should be more than 0")
    if reps <= 0:
        raise ValueError("Rep number should be more than 0")
    if bodyweight <= 0:
        raise ValueError("Body weight should be more than 0")
    if gender not in ("male", "female"):
        raise ValueError("Sex should be male or female")

    one_rm = calculate_1rm(weight, reps)
    return get_strength_level(one_rm, bodyweight, exercise_slug, gender)
