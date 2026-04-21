from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RequisitionInfo:
    requisition_id: str
    link: str
