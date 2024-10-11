from dataclasses import dataclass
from chalicelib.src.seedwork.application.queries import Query, QueryResult, execute_query
from chalicelib.src.modules.application.queries.base import QueryBaseHandler
from chalicelib.src.modules.domain.repository import UserRepository


@dataclass
class GetUsersQuery(Query):
    ...


class GetUsersHandler(QueryBaseHandler):
    def handle(self, query: GetUsersQuery):
        repository = self.user_factory.create_object(UserRepository.__class__)
        result = repository.get_all()
        return QueryResult(result=result)


@execute_query.register(GetUsersQuery)
def execute_get_incidents(query: GetUsersQuery):
    handler = GetUsersHandler()
    return handler.handle(query)