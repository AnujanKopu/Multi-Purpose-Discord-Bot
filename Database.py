from replit import db

class Database():
  def update(serverId:str,name,data,assign=False):
    if not serverId in db.keys():
      db[serverId] = []
    if name in db[serverId]:
      temp = db[str(serverId)+"_"+name]
      if not assign:
        temp.append(data)
        if len(temp) == 50:
          del temp[0]
      else:
        temp = data
      db[str(serverId)+"_"+name] = temp
    else:
      if not assign:
        db[str(serverId)+"_"+name] = [data]
      else:
         db[str(serverId)+"_"+name] = data
      temp = db[serverId]
      temp.append(name)
      db[serverId] = temp

  def delete(serverId:str,name,index):
    if name in db[serverId]:
      temp = db[str(serverId)+"_"+name]
      del temp[index]
      db[str(serverId)+"_"+name] = temp
  
  def get_data(serverId:str,name):
    if serverId in db.keys():
      if name in db[serverId]:
        return db[str(serverId)+"_"+name]
      else:
        return None
    else:
      db[serverId] = []
      return None

  def new_server(serverId:str):
    if not serverId in db.keys():
      db[serverId] = []

  
  



