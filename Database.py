from replit import db

class Database():
  def update(serverId,name,data,assign=False):
    if serverId in db.keys() and name in db[serverId]:
      temp = db[serverId+"_"+name]
      if not assign:
        temp.append(data)
        if len(temp) == 50:
          del temp[0]
      else:
        temp = data
      db[serverId+"_"+name] = temp
    else:
      if not assign:
        db[serverId+"_"+name] = [data]
      else:
         db[serverId+"_"+name] = data
      temp = db[serverId]
      temp.append(name)
      db[serverId] = temp

  def delete(serverId,name,index):
    if name in db[serverId]:
      temp = db[serverId+"_"+name]
      del temp[index]
      db[serverId+"_"+name] = temp
  
  def get_data(serverId,name):
    if serverId in db.keys():
      if name in db[serverId]:
        return db[serverId+"_"+name]
      else:
        return None
    else:
      db[serverId] = []
      return None

  def new_server(serverId):
    if not serverId in db.keys():
      db[serverId] = []


  
  



