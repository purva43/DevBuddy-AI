from vector_store import add_document, search

add_document("1", "I love my dog, he's a golden retriever")
add_document("2", "The stock market crashed today")
add_document("3", "My puppy learned a new trick")
add_document("4", "Interest rates are rising this year")

results = search("Tell me about my pet")
print(results)