import http

from dependency_injector.wiring import Provide, inject
from quart import Blueprint, request
from quart_schema import RequestSchemaValidationError, validate_querystring

from app.entities.graph_dto import GetSurroundingByNodeRequest
from app.services.comp_graph_service import CompGraphService
from app.container import ApplicationContainer

comp_graph_controller = Blueprint("CompGraph", __name__)


@comp_graph_controller.errorhandler(RequestSchemaValidationError)
async def handle_request_validation_error(arg):
    return {"message": "Request parameter should be an integer"}, 400


@comp_graph_controller.get("/api/comp/surrounding")
@validate_querystring(GetSurroundingByNodeRequest)
@inject
async def get_surrounding_by_node(
    query_args: GetSurroundingByNodeRequest,
    comp_graph_service: CompGraphService = Provide[
        ApplicationContainer.comp_graph_bp.comp_graph_svc
    ],
):
    node_id = query_args.node_id
    expand_number_of_layers = query_args.expand_number_of_layers
    if node_id is None:
        return {"message": "node_id can not be empty"}, http.HTTPStatus.BAD_REQUEST
    if expand_number_of_layers is None:
        return {"message": "expand_number_of_layers can not be empty"}, http.HTTPStatus.BAD_REQUEST

    result = await comp_graph_service.get_surrounding_by_node(node_id, expand_number_of_layers)

    return result.dict()


@comp_graph_controller.get("/api/comp/surrounding/new")
@validate_querystring(GetSurroundingByNodeRequest)
@inject
async def bfs(
        query_args: GetSurroundingByNodeRequest,
        comp_graph_service: CompGraphService = Provide[
            ApplicationContainer.comp_graph_bp.comp_graph_svc
        ],
):
    node_id = query_args.node_id
    expand_number_of_layers = query_args.expand_number_of_layers
    if node_id is None:
        return {"message": "node_id can not be empty"}, http.HTTPStatus.BAD_REQUEST
    if expand_number_of_layers is None:
        return {"message": "expand_number_of_layers can not be empty"}, http.HTTPStatus.BAD_REQUEST

    # below flags are true by default if not included in the request
    competition = query_args.competition
    product = query_args.product
    other = query_args.other
    unknown = query_args.unknown
    flags = [competition, product, other, unknown]

    result = await comp_graph_service.bfs(node_id, expand_number_of_layers, flags)

    return result
