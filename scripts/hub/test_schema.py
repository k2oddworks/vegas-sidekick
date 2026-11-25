import sqlite3
from pathlib import Path

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys=ON")
db.executescript(Path(__file__).with_name("0001_tasks.sql").read_text())
def reject(sql):
    try:
        db.execute(sql)
    except sqlite3.IntegrityError:
        return
    raise AssertionError(sql)

db.execute("INSERT INTO projects(id,title,department) VALUES('p','Project','shows')")
db.execute("INSERT INTO tasks(id,title,department,project_id) VALUES('t','Task','shows','p')")
db.execute("INSERT INTO tasks(id,title,department,project_id,parent_task_id) VALUES('s','Subtask','shows','p','t')")
reject("INSERT INTO tasks(id,title,department,project_id,parent_task_id) VALUES('x','Too deep','shows','p','s')")
reject("UPDATE tasks SET parent_task_id='s' WHERE id='t'")
reject("UPDATE tasks SET priority=5 WHERE id='t'")
reject("UPDATE tasks SET status='completed' WHERE id='t'")
db.execute("UPDATE tasks SET status='completed',completed_at='2026-11-25T00:00:00Z',completed_by='test' WHERE id='t'")
db.execute("UPDATE tasks SET status='todo',completed_at=NULL,completed_by=NULL WHERE id='t'")
db.execute("INSERT INTO recurrence_rules(id,title,department,frequency,next_due_on) VALUES('r','Audit','shows','weekly','2026-11-25')")
db.execute("INSERT INTO tasks(id,title,department,recurrence_id,occurrence_on) VALUES('r1','Audit','shows','r','2026-11-25')")
reject("INSERT INTO tasks(id,title,department,recurrence_id,occurrence_on) VALUES('r2','Audit','shows','r','2026-12-02')")
db.execute("UPDATE tasks SET issue_key='photo:show' WHERE id='t'")
reject("UPDATE tasks SET issue_key='photo:show' WHERE id='s'")
db.execute("INSERT INTO activity(id,task_id,department,event_type,actor_type,actor_id) VALUES('a','t','shows','created','manual','test')")
reject("DELETE FROM activity WHERE id='a'")
reject("UPDATE activity SET event_type='changed' WHERE id='a'")
assert not db.execute("PRAGMA foreign_key_check").fetchall()
print("Hub schema smoke tests passed")
