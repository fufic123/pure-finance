from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import (
    get_create_rule,
    get_current_user,
    get_delete_rule,
    get_list_rules,
)
from src.api.dtos.rules.create_request import CreateRuleRequest
from src.api.dtos.rules.response import RuleResponse
from src.app.services.categorization_rules.create_rule import CreateRule
from src.app.services.categorization_rules.delete_rule import DeleteRule
from src.app.services.categorization_rules.list_rules import ListRules
from src.db.models.user import User

router = APIRouter()


@router.get("/categorization-rules", response_model=list[RuleResponse])
async def list_rules(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListRules, Depends(get_list_rules)],
) -> list[RuleResponse]:
    rules = await service(user.id)
    return [RuleResponse.from_rule(r) for r in rules]


@router.post("/categorization-rules", response_model=RuleResponse, status_code=201)
async def create_rule(
    body: CreateRuleRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CreateRule, Depends(get_create_rule)],
) -> RuleResponse:
    rule = await service(user_id=user.id, category_id=body.category_id, keyword=body.keyword)
    return RuleResponse.from_rule(rule)


@router.delete("/categorization-rules/{rule_id}", status_code=204)
async def delete_rule(
    rule_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[DeleteRule, Depends(get_delete_rule)],
) -> None:
    await service(rule_id=rule_id, user_id=user.id)
