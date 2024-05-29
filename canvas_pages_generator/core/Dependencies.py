from canvas_pages_generator.core.Config import Config
from canvas_pages_generator.services.ApiService import ApiService
from canvas_pages_generator.services.DatabaseService import DatabaseService
from canvas_pages_generator.services.SqliteRepository import SqliteRepository

class Dependencies:

  config: Config = Config()
  apiService: ApiService = ApiService(config)
  databaseService: DatabaseService = DatabaseService(config)
  repository: SqliteRepository = SqliteRepository(databaseService)
  
