import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "permesso.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                language TEXT NOT NULL DEFAULT 'ru',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tracked_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                case_number TEXT NOT NULL,
                last_status TEXT,
                last_checked_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id, case_number)
            )
        """)
        await db.commit()


async def upsert_user(user_id: int, chat_id: int, language: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO users (user_id, chat_id, language)
               VALUES (?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET chat_id=excluded.chat_id, language=excluded.language""",
            (user_id, chat_id, language),
        )
        await db.commit()


async def set_language(user_id: int, language: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET language=? WHERE user_id=?",
            (language, user_id),
        )
        await db.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def add_case(user_id: int, case_number: str, initial_status: str | None) -> bool:
    """Add a case. Returns False if duplicate or limit reached."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM tracked_cases WHERE user_id=?", (user_id,)
        ) as cursor:
            (count,) = await cursor.fetchone()
            if count >= 10:
                return False
        try:
            await db.execute(
                """INSERT INTO tracked_cases (user_id, case_number, last_status, last_checked_at)
                   VALUES (?, ?, ?, CURRENT_TIMESTAMP)""",
                (user_id, case_number, initial_status),
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def remove_case(user_id: int, case_number: str) -> bool:
    """Remove a case. Returns False if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM tracked_cases WHERE user_id=? AND case_number=?",
            (user_id, case_number),
        )
        await db.commit()
        return cursor.rowcount > 0


async def get_user_cases(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM tracked_cases WHERE user_id=? ORDER BY created_at",
            (user_id,),
        ) as cursor:
            return [dict(row) async for row in cursor]


async def get_all_cases() -> list[dict]:
    """Get all cases joined with user info for the scheduler."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT tc.id, tc.user_id, tc.case_number, tc.last_status,
                      u.chat_id, u.language
               FROM tracked_cases tc
               JOIN users u ON tc.user_id = u.user_id"""
        ) as cursor:
            return [dict(row) async for row in cursor]


async def update_case_status(case_id: int, new_status: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE tracked_cases SET last_status=?, last_checked_at=CURRENT_TIMESTAMP WHERE id=?",
            (new_status, case_id),
        )
        await db.commit()
