import aiosqlite

DB = "data.db"

async def setup():
    async with aiosqlite.connect(DB) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            guild_id INTEGER,
            reason TEXT
        );

        CREATE TABLE IF NOT EXISTS automod (
            guild_id INTEGER PRIMARY KEY,
            spam INTEGER DEFAULT 1,
            caps INTEGER DEFAULT 1,
            links INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS bypass_roles (
            guild_id INTEGER,
            role_id INTEGER
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            action TEXT,
            actor INTEGER,
            target INTEGER,
            reason TEXT,
            timestamp TEXT
        );
        """)
        await db.commit()

async def log_action(gid, action, actor, target, reason):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO audit_logs VALUES (NULL, ?, ?, ?, ?, ?, datetime('now'))",
            (gid, action, actor, target, reason)
        )
        await db.commit()

async def add_warning(uid, gid, reason):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO warnings (user_id, guild_id, reason) VALUES (?, ?, ?)",
            (uid, gid, reason)
        )
        await db.commit()

async def get_warnings(uid, gid):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT id, reason FROM warnings WHERE user_id=? AND guild_id=?",
            (uid, gid)
        )
        return await cur.fetchall()

async def get_automod(gid):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT spam, caps, links FROM automod WHERE guild_id=?",
            (gid,)
        )
        return await cur.fetchone() or (1,1,1)

async def get_bypass_roles(gid):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT role_id FROM bypass_roles WHERE guild_id=?",
            (gid,)
        )
        return [r[0] for r in await cur.fetchall()]
