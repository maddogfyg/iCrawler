
import sqlite3

class sqlite:
    def insertContent(self, url, title, content):
        cxn = sqlite3.connect('../data.sqlite')
        insertContentSql = 'INSERT INTO "main"."content" ("url","title","content") VALUES ("'\
        +url+'","'+title+'","'+content+'")'
        cur = cxn.cursor()
        cur.execute(insertContentSql)
        cur.close()
        cxn.commit()
        cxn.close()