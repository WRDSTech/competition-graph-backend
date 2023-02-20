from dependency_injector.wiring import Provide, inject
from quart import Blueprint, request, abort
from app.services.comp_graph_service import CompGraphService
from app.container import ApplicationContainer
from app.entities.graph_entities import Graph, Entity

comp_graph_controller = Blueprint("CompGraph", __name__)


@comp_graph_controller.get("/api/comp/surrouding")
@inject
async def get_surrouding_by_node(
    comp_graph_service: CompGraphService = Provide[
        ApplicationContainer.comp_graph_bp.comp_graph_svc
    ],
) -> str:
    try:
        node_id = request.args.get("node_id", type=str)
        assert node_id is not None
        expand_number_of_layers = request.args.get(
            "expand_number_of_layers", type=str)
        assert expand_number_of_layers is not None
        result = await comp_graph_service.get_surrouding_by_node(node_id, expand_number_of_layers)

        return result.json()
    except Exception as e:
        abort(400, {'message': str(e)})
