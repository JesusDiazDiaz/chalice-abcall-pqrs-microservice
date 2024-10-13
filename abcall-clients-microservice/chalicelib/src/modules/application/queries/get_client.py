from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import ClientRepository


@dataclass
class GetClientQuery(Query):
    client_id:str

class GetUserHandler(QueryBaseHandler):
    def handle(self, query: GetClientQuery):
        repository = self.user_factory.create_object(ClientRepository.__class__)
        result = repository.get(query.client_id)
        return QueryResult(result=result)

@execute_query.register(GetClientQuery)
def execute_get_user(query: GetClientQuery):
    handler = GetUserHandler()
    return handler.handle(query)