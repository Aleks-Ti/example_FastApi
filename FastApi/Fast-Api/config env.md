# app/core/config.py

^02ce2d

```python
from pydantic import BaseSettings
class Settings(BaseSettings):
	app_title: str = 'Бронирование переговорок'
    database_url: str
	class Config:
		env_file = '.env'
```

