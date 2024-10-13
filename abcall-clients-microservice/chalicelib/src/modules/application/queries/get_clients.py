from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import ClientRepository


@dataclass
class GetClientsQuery(Query):
    ...

class GetClientsHandler(QueryBaseHandler):
    def handle(self, query: GetClientsQuery):
        repository = self.client_factory.create_object(ClientRepository.__class__)
        result = repository.get_all()
        return QueryResult(result=result)


@execute_query.register(GetClientsQuery)
def execute_get_users(query: GetClientsQuery):
    handler = GetUsersHandler()
    return handler.handle(query)