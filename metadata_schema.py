"""Draft metadata schema for OpenBIS lab experiments.

This schema mirrors the lab rules used by the Streamlit metadata tools and the
current API payload shape. It keeps the hierarchy recursive through `parents`
and validates the lab-specific parent-child constraints.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TYPE_ALIASES = {
    "SIXTEEN_HEADERS": "16HEADERS",
}

OBJECT_TYPES = [
    "CORE",
    "SEDIMENT",
    "ROCK",
    "SOLID_SAMPLE_BLOCK",
    "SOLID_SAMPLE_HOLLOWCYLINDER",
    "SOLID_SAMPLE_CYLINDER",
    "POWDER",
    "POWDER_PROPORTION",
    "POWDER_MIXTURE",
    "POWDERED_SAMPLE",
    "POWDERED_SAMPLE_BLOCK",
    "POWDERED_SAMPLE_HOLLOWCYLINDER",
    "POWDERED_SAMPLE_CYLINDER",
    "APPARATUS",
    "EQUIPMENT",
    "ACTUATOR",
    "ASSEMBLY",
    "COMPONENT",
    "SENSOR",
    "PERSON",
    "ARTIFICIAL",
    "FLUID",
    "POINT_MEASUREMENT",
    "STEP",
    "STEP_TRAPZ_TIMELIMITED",
    "STEP_TRAPZ_SLIPLIMITED",
    "STEP_HOLD",
    "STEP_RAMP",
    "STEP_STEPS",
    "STEP_STEPS_TORQUE",
    "STEP_TOUCHPOINT",
    "STEP_CONSTANT",
    "STEP_SINUSOIDAL",
    "STEP_TRIANGLE",
    "STEP_REGYOFFE",
    "STEP_BOXCAR",
    "16HEADERS",
    "IMAGE",
]

SPECIALIZED_STEPS = [
    "STEP_TRAPZ_TIMELIMITED",
    "STEP_TRAPZ_SLIPLIMITED",
    "STEP_HOLD",
    "STEP_RAMP",
    "STEP_STEPS",
    "STEP_STEPS_TORQUE",
    "STEP_TOUCHPOINT",
    "STEP_CONSTANT",
    "STEP_SINUSOIDAL",
    "STEP_TRIANGLE",
    "STEP_REGYOFFE",
    "STEP_BOXCAR",
]

VALID_STEP_TYPES = ["STEP"] + SPECIALIZED_STEPS

TYPE_GROUPS = {
    "Basic materials": ["SEDIMENT", "CORE", "ROCK", "ARTIFICIAL", "FLUID"],
    "Powders": ["POWDER", "POWDER_PROPORTION", "POWDER_MIXTURE"],
    "Solid specimens": ["SOLID_SAMPLE_BLOCK", "SOLID_SAMPLE_HOLLOWCYLINDER", "SOLID_SAMPLE_CYLINDER"],
    "Powdered specimens": ["POWDERED_SAMPLE", "POWDERED_SAMPLE_BLOCK", "POWDERED_SAMPLE_HOLLOWCYLINDER", "POWDERED_SAMPLE_CYLINDER"],
    "Instruments": ["APPARATUS", "EQUIPMENT", "ASSEMBLY", "COMPONENT", "ACTUATOR", "SENSOR"],
    "People": ["PERSON"],
    "Measurements": ["POINT_MEASUREMENT"],
    "Basic steps": ["STEP"],
    "Trapezoidal steps": ["STEP_TRAPZ_TIMELIMITED", "STEP_TRAPZ_SLIPLIMITED"],
    "Control steps": ["STEP_HOLD", "STEP_RAMP", "STEP_STEPS", "STEP_STEPS_TORQUE", "STEP_TOUCHPOINT"],
    "Periodic steps": ["STEP_CONSTANT", "STEP_SINUSOIDAL", "STEP_TRIANGLE"],
    "Special steps": ["STEP_REGYOFFE", "STEP_BOXCAR"],
    "Data": ["16HEADERS", "IMAGE"],
}

PARENT_CHILD_RELATIONSHIPS = {
    "POWDER": {"SEDIMENT", "CORE", "ROCK", "ARTIFICIAL"},
    "SOLID_SAMPLE_BLOCK": {"CORE", "ROCK", "ARTIFICIAL"},
    "SOLID_SAMPLE_CYLINDER": {"CORE", "ROCK", "ARTIFICIAL"},
    "SOLID_SAMPLE_HOLLOWCYLINDER": {"CORE", "ROCK", "ARTIFICIAL"},
    "POWDER_MIXTURE": "POWDER_PROPORTION",
    "POWDERED_SAMPLE": {"POWDER", "POWDER_MIXTURE"},
    "POWDERED_SAMPLE_BLOCK": {"POWDER", "POWDER_MIXTURE"},
    "POWDERED_SAMPLE_CYLINDER": {"POWDER", "POWDER_MIXTURE"},
    "POWDERED_SAMPLE_HOLLOWCYLINDER": {"POWDER", "POWDER_MIXTURE"},
    "ASSEMBLY": "APPARATUS",
    "COMPONENT": {"ASSEMBLY", "ARTIFICIAL"},
    "ACTUATOR": "APPARATUS",
    "SENSOR": "APPARATUS",
    "STEP": {"EQUIPMENT", "APPARATUS", "ASSEMBLY", "ACTUATOR", "SENSOR", "PERSON", "FLUID", "SOLID_SAMPLE_BLOCK", "SOLID_SAMPLE_CYLINDER", "SOLID_SAMPLE_HOLLOWCYLINDER", "POWDERED_SAMPLE", "POWDERED_SAMPLE_BLOCK", "POWDERED_SAMPLE_CYLINDER", "POWDERED_SAMPLE_HOLLOWCYLINDER", "STEP"},
    "POINT_MEASUREMENT": "STEP",
    "STEP_TRAPZ_TIMELIMITED": "STEP",
    "STEP_TRAPZ_SLIPLIMITED": "STEP",
    "STEP_HOLD": "STEP",
    "STEP_RAMP": "STEP",
    "STEP_STEPS": "STEP",
    "STEP_STEPS_TORQUE": "STEP",
    "STEP_TOUCHPOINT": "STEP",
    "STEP_CONSTANT": "STEP",
    "STEP_SINUSOIDAL": "STEP",
    "STEP_TRIANGLE": "STEP",
    "STEP_REGYOFFE": "STEP",
    "STEP_BOXCAR": "STEP",
}

ALL_OBJECT_TYPES: Set[str] = {TYPE_ALIASES.get(t, t) for t in OBJECT_TYPES}
STEP_TYPES: Set[str] = {TYPE_ALIASES.get(t, t) for t in VALID_STEP_TYPES}
SPECIALIZED_STEP_TYPES: Set[str] = {TYPE_ALIASES.get(t, t) for t in SPECIALIZED_STEPS}
ROOT_SPECIMEN_TYPES: Set[str] = {
    TYPE_ALIASES.get(t, t) for t in TYPE_GROUPS["Solid specimens"] + TYPE_GROUPS["Powdered specimens"]
}


def normalize_type_name(type_name: str) -> str:
    return TYPE_ALIASES.get(type_name, type_name)


def normalize_parent_rules() -> dict[str, set[str]]:
    normalized: dict[str, set[str]] = {}
    for child_type, parent_types in PARENT_CHILD_RELATIONSHIPS.items():
        if isinstance(parent_types, str):
            normalized[normalize_type_name(child_type)] = {normalize_type_name(parent_types)}
        else:
            normalized[normalize_type_name(child_type)] = {normalize_type_name(parent) for parent in parent_types}
    return normalized


PARENT_RULES = normalize_parent_rules()


class MetadataNode(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    code: str = Field(alias="sample_code")
    type: str
    identifier: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    parents: List["MetadataNode"] = Field(default_factory=list)

    @field_validator("type")
    @classmethod
    def _normalize_type(cls, value: str) -> str:
        normalized = normalize_type_name(value)
        if normalized not in ALL_OBJECT_TYPES:
            raise ValueError(f"Unsupported object type: {value}")
        return normalized

    def _parent_types(self) -> set[str]:
        return {parent.type for parent in self.parents}

    def _is_step_type(self) -> bool:
        return self.type in STEP_TYPES

    def _validate_parent_rule(self) -> None:
        if self.type in SPECIALIZED_STEP_TYPES:
            return

        allowed_parents = PARENT_RULES.get(self.type)
        if allowed_parents is None:
            return

        parent_types = self._parent_types()
        if not parent_types.intersection(allowed_parents):
            raise ValueError(f"{self.code} ({self.type}) requires at least one parent in {sorted(allowed_parents)}")

    def _validate_specialized_step(self) -> None:
        if self.type not in SPECIALIZED_STEP_TYPES:
            return

        parent_types = self._parent_types()
        if "ACTUATOR" not in parent_types:
            raise ValueError(f"{self.code} ({self.type}) requires an ACTUATOR parent")

        actuator_parents = [parent for parent in self.parents if parent.type == "ACTUATOR"]
        if not any("APPARATUS" in {gp.type for gp in actuator.parents} for actuator in actuator_parents):
            raise ValueError(f"{self.code} ({self.type}) requires ACTUATOR -> APPARATUS")

    def _validate_root_step(self) -> None:
        if not self._is_step_type():
            return

        parent_types = self._parent_types()
        if "PERSON" not in parent_types:
            raise ValueError(f"{self.code} requires a PERSON parent")
        if "APPARATUS" not in parent_types:
            raise ValueError(f"{self.code} requires an APPARATUS parent")
        if not parent_types.intersection(ROOT_SPECIMEN_TYPES):
            raise ValueError(f"{self.code} requires at least one solid or powdered specimen parent")

    def _validate_step_parent_chain(self) -> None:
        if not self._is_step_type():
            return

        if not self.parents:
            return

        # A nested step can be attached to another step type; the config also
        # allows direct root steps, so we only validate the chain if a step parent exists.
        if any(parent.type in STEP_TYPES for parent in self.parents):
            return

    @model_validator(mode="after")
    def _validate_node(self) -> "MetadataNode":
        self._validate_parent_rule()
        self._validate_specialized_step()
        return self


class ExperimentMetadata(BaseModel):
    """Canonical laboratory experiment metadata.

    `steps` is the collection of step nodes in the experiment graph. Each step
    can recursively embed its parents, which are validated against the lab rules.
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str = Field(description="Internal experiment identifier, e.g. s0020")
    experiment_type: Literal["DEFAULT_EXPERIMENT"] = Field(default="DEFAULT_EXPERIMENT", alias="type")
    space: Optional[str] = None
    project: Optional[str] = None
    identifier: Optional[str] = None
    permId: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    steps: List[MetadataNode] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_experiment(self) -> "ExperimentMetadata":
        if not self.steps:
            raise ValueError("DEFAULT_EXPERIMENT must contain at least one step")

        if any(step.type not in STEP_TYPES for step in self.steps):
            raise ValueError("Experiment steps must be STEP or specialized step objects")

        if self.properties.get("$NAME") and self.properties["$NAME"] != self.name:
            raise ValueError("Experiment name must match properties['$NAME']")

        root_steps = [step for step in self.steps if not any(parent.type in STEP_TYPES for parent in step.parents)]
        if not root_steps:
            raise ValueError("At least one root step is required")

        for root_step in root_steps:
            root_step._validate_root_step()

        return self


MetadataNode.model_rebuild()
ExperimentMetadata.model_rebuild()
