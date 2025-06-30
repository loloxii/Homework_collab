cd backend
uvicorn main:app --reload

cd ../frontend
npm run dev

database:
Terminal:
mongosh
show dbs                      // 查看所有数据库
use mydb                      // 切换/创建数据库
db.createCollection("users") // 创建集合
db.users.insertOne({ name: "Alice", age: 25 }) // 插入文档
db.users.find()              // 查询文档
exit