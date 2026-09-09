from user_service import UserService

service = UserService(storage_path="users.json")
service.register("alice@example.com", "Password123")
print(service.count_users())  # должно вывести 1
