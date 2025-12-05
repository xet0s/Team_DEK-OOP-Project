from peewee import SqliteDatabase
from core.settings import DB_PATH

#Veritabanı nesnesi [connection yok]
db=SqliteDatabase(DB_PATH,pragmas={"foreign_keys":1}) 
