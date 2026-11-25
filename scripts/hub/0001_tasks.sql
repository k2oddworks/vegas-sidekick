-- D1 migration 0001: operational task records. All timestamps UTC.
CREATE TABLE projects (
 id TEXT PRIMARY KEY NOT NULL,
 title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 200),
 description TEXT NOT NULL DEFAULT '',
 department TEXT NOT NULL CHECK(department IN ('command','tasks','shows','index','actions','analytics','marketing','partnerships')),
 archived_at TEXT,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
 updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE recurrence_rules (
 id TEXT PRIMARY KEY NOT NULL,
 title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 200),
 department TEXT NOT NULL CHECK(department IN ('command','tasks','shows','index','actions','analytics','marketing','partnerships')),
 priority INTEGER NOT NULL DEFAULT 3 CHECK(priority BETWEEN 1 AND 4),
 frequency TEXT NOT NULL CHECK(frequency IN ('daily','weekly','monthly')),
 interval_count INTEGER NOT NULL DEFAULT 1 CHECK(interval_count >= 1),
 timezone TEXT NOT NULL DEFAULT 'America/Los_Angeles',
 next_due_on TEXT NOT NULL,
 paused INTEGER NOT NULL DEFAULT 0 CHECK(paused IN (0,1)),
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE tasks (
 id TEXT PRIMARY KEY NOT NULL,
 title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 200),
 description TEXT NOT NULL DEFAULT '',
 notes TEXT NOT NULL DEFAULT '',
 department TEXT NOT NULL CHECK(department IN ('command','tasks','shows','index','actions','analytics','marketing','partnerships')),
 priority INTEGER NOT NULL DEFAULT 3 CHECK(priority BETWEEN 1 AND 4),
 status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('backlog','todo','in_progress','awaiting','verification','completed')),
 source TEXT NOT NULL DEFAULT 'manual' CHECK(source IN ('manual','chatgpt','automation')),
 project_id TEXT REFERENCES projects(id) ON DELETE RESTRICT,
 parent_task_id TEXT REFERENCES tasks(id) ON DELETE RESTRICT,
 recurrence_id TEXT REFERENCES recurrence_rules(id) ON DELETE RESTRICT,
 occurrence_on TEXT,
 due_on TEXT,
 issue_key TEXT,
 verification TEXT,
 completed_at TEXT,
 completed_by TEXT,
 archived_at TEXT,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
 updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
 revision INTEGER NOT NULL DEFAULT 1 CHECK(revision >= 1),
 CHECK(parent_task_id IS NULL OR parent_task_id <> id),
 CHECK((recurrence_id IS NULL) = (occurrence_on IS NULL)),
 CHECK((status = 'completed' AND completed_at IS NOT NULL AND completed_by IS NOT NULL) OR
       (status <> 'completed' AND completed_at IS NULL AND completed_by IS NULL)),
 UNIQUE(recurrence_id, occurrence_on)
);
CREATE UNIQUE INDEX tasks_one_open_recurrence ON tasks(recurrence_id)
 WHERE recurrence_id IS NOT NULL AND status <> 'completed' AND archived_at IS NULL;
CREATE UNIQUE INDEX tasks_one_open_issue ON tasks(issue_key)
 WHERE issue_key IS NOT NULL AND status <> 'completed' AND archived_at IS NULL;
CREATE INDEX tasks_workload ON tasks(archived_at,status,priority,due_on);
CREATE INDEX tasks_project ON tasks(project_id);
CREATE INDEX tasks_parent ON tasks(parent_task_id);
CREATE TRIGGER tasks_parent_insert BEFORE INSERT ON tasks WHEN NEW.parent_task_id IS NOT NULL
BEGIN
 SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM tasks p WHERE p.id=NEW.parent_task_id AND p.parent_task_id IS NULL AND p.project_id IS NEW.project_id AND p.archived_at IS NULL)
 THEN RAISE(ABORT,'Invalid parent task or project') END;
END;
CREATE TRIGGER tasks_parent_update BEFORE UPDATE OF parent_task_id,project_id ON tasks
BEGIN
 SELECT CASE WHEN NEW.parent_task_id IS NOT NULL AND NOT EXISTS
 (SELECT 1 FROM tasks p WHERE p.id=NEW.parent_task_id AND p.id<>NEW.id AND p.parent_task_id IS NULL AND p.project_id IS NEW.project_id AND p.archived_at IS NULL)
 THEN RAISE(ABORT,'Invalid parent task or project') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM tasks c WHERE c.parent_task_id=NEW.id AND (NEW.parent_task_id IS NOT NULL OR c.project_id IS NOT NEW.project_id))
 THEN RAISE(ABORT,'Cannot invalidate child tasks') END;
END;
CREATE TABLE activity (
 id TEXT PRIMARY KEY NOT NULL,
 task_id TEXT REFERENCES tasks(id) ON DELETE RESTRICT,
 project_id TEXT REFERENCES projects(id) ON DELETE RESTRICT,
 department TEXT NOT NULL CHECK(department IN ('command','tasks','shows','index','actions','analytics','marketing','partnerships')),
 event_type TEXT NOT NULL,
 actor_type TEXT NOT NULL CHECK(actor_type IN ('manual','chatgpt','automation')),
 actor_id TEXT NOT NULL,
 importance INTEGER NOT NULL DEFAULT 3 CHECK(importance BETWEEN 1 AND 4),
 detail_json TEXT NOT NULL DEFAULT '{}' CHECK(json_valid(detail_json)),
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX activity_recent ON activity(created_at DESC);
CREATE INDEX activity_task ON activity(task_id,created_at DESC);
CREATE TRIGGER activity_no_update BEFORE UPDATE ON activity BEGIN SELECT RAISE(ABORT,'Activity is append-only'); END;
CREATE TRIGGER activity_no_delete BEFORE DELETE ON activity BEGIN SELECT RAISE(ABORT,'Activity is append-only'); END;
