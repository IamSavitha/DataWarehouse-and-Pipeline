from pinecone import Pinecone
pc = Pinecone(api_key='key')  #<---- need to insert the key and check 
print(pc.list_indexes())
