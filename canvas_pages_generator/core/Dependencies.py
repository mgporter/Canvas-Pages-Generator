from canvas_pages_generator.core.Config import Config
from canvas_pages_generator.services.ApiService import ApiService
from canvas_pages_generator.services.DatabaseService import DatabaseService
from canvas_pages_generator.services.SqliteRepository import SqliteRepository

class Dependencies:

  apiService: ApiService = ApiService()
  databaseService: DatabaseService = DatabaseService()
  repository: SqliteRepository = SqliteRepository(databaseService)
  config: Config = Config()
