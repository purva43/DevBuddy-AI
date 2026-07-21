from memory_db import init_db, save_message, load_all_messages

init_db()
save_message("user", "My name is Purva")
save_message("model", "Nice to meet you, Purva!")

print(load_all_messages())