import json

def getModifyNameItemMailSql(gbId):
    mailWealth = {'resItemList': [], 'bagItemList': [{'itemId': 30001010, 'itemNum': 1, 'bindType': 0}], 'bagItemObjList': []}
    mailWealth = json.dumps(mailWealth)
    args = '{}|{}|{}'.format(37000046, mailWealth, '')
    sql = """INSERT INTO game_offline_cmds (gbId, cmd, args,opUUID,srcType,srcSubType,desp,idipSource, cmdTime) VALUES (%s,'%s','%s',%s,%s,%s,'%s',%s,%s)"""
    sql = sql % (gbId, 'sendMail', args, 0, 0, 0, '', 0, 0)
    return sql


if __name__ == '__main__':
    _sql = getModifyNameItemMailSql(1234)
    print(_sql)