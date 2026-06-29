"""Project service — CRUD operations for projects"""

from app.database import get_db


class ProjectService:
    def list_projects(self) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM projects ORDER BY updated_at DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_project(self, project_id: int) -> dict | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM projects WHERE id = ?", (project_id,)
            ).fetchone()
            return dict(row) if row else None

    def create_project(self, name: str, description: str = "", model: str = "", system_prompt: str = "") -> dict:
        with get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO projects (name, description, model, system_prompt) VALUES (?, ?, ?, ?)",
                (name, description, model, system_prompt),
            )
            conn.commit()
            row = conn.execute(
                "SELECT * FROM projects WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(row)

    def update_project(self, project_id: int, **kwargs) -> dict | None:
        existing = self.get_project(project_id)
        if not existing:
            return None

        fields = {k: v for k, v in kwargs.items() if v is not None and k in ("name", "description", "model", "system_prompt")}
        if not fields:
            return existing

        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [project_id]

        with get_db() as conn:
            conn.execute(
                f"UPDATE projects SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                values,
            )
        return self.get_project(project_id)

    def delete_project(self, project_id: int) -> bool:
        with get_db() as conn:
            cursor = conn.execute(
                "DELETE FROM projects WHERE id = ?", (project_id,)
            )
            return cursor.rowcount > 0

    def get_project_chats(self, project_id: int) -> list[dict]:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM chats WHERE project_id = ? ORDER BY created_at ASC",
                (project_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def save_chat_message(self, project_id: int | None, role: str, content: str, model: str = "", provider: str = "ollama") -> dict:
        with get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO chats (project_id, role, content, model, provider) VALUES (?, ?, ?, ?, ?)",
                (project_id, role, content, model, provider),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM chats WHERE id = ?", (cursor.lastrowid,)).fetchone()
            return dict(row)


project_service = ProjectService()
