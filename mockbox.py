import sqlite3
import json
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from typing import Optional
import uvicorn

app = FastAPI(
    title="MockBox",
    description="JSON yükle → anında çalışan REST API",
    version="2.0.0"
)

DB_FILE = "mockbox.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            resource  TEXT NOT NULL,
            data      TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def paginate(items: list, page: int, limit: int) -> dict:
    total = len(items)
    total_pages = max(1, (total + limit - 1) // limit)
    offset = (page - 1) * limit
    return {
        "data": items[offset: offset + limit],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        }
    }


def fetch_items(resource: str) -> list:
    conn = get_db()
    rows = conn.execute(
        "SELECT id, data FROM records WHERE resource = ?", (resource,)
    ).fetchall()
    conn.close()

    if not rows:
        raise HTTPException(404, f"'{resource}' bulunamadı ya da boş")

    items = []
    for row in rows:
        item = json.loads(row["data"])
        item["id"] = row["id"]
        items.append(item)
    return items


@app.post("/mockbox/load", summary="JSON verini yükle")
async def load_json(payload: dict):
    conn = get_db()
    summary = {}

    for resource, items in payload.items():
        if not isinstance(items, list):
            raise HTTPException(400, f"'{resource}' bir liste olmalı")

        conn.execute("DELETE FROM records WHERE resource = ?", (resource,))
        for item in items:
            conn.execute(
                "INSERT INTO records (resource, data) VALUES (?, ?)",
                (resource, json.dumps(item, ensure_ascii=False))
            )
        summary[resource] = len(items)

    conn.commit()
    conn.close()

    return {
        "message": "Yüklendi ✓",
        "summary": summary,
        "tip": "Filtreleme için /{resource}/search?alan=deger kullan"
    }


@app.get("/{resource}", summary="Tüm kayıtları getir")
async def get_all(
    resource: str,
    page:   int           = Query(default=1,   ge=1,          description="Sayfa numarası"),
    limit:  int           = Query(default=10,  ge=1,  le=100, description="Sayfa başına kayıt"),
    search: Optional[str] = Query(default=None,               description="Tüm alanlarda ara"),
):
    if resource in ("mockbox", "favicon.ico"):
        raise HTTPException(404, "Bulunamadı")

    items = fetch_items(resource)

    if search:
        s = search.lower()
        items = [i for i in items if any(s in str(v).lower() for v in i.values())]

    return paginate(items, page, limit)


@app.get("/{resource}/search", summary="Alan bazlı filtrele")
async def field_search(resource: str, request: Request):
    if resource == "mockbox":
        raise HTTPException(404, "Bu endpoint özel")

    params = dict(request.query_params)
    page   = max(1,   int(params.pop("page",   1)))
    limit  = min(100, max(1, int(params.pop("limit", 10))))
    search = params.pop("search", None)

    items = fetch_items(resource)

    if search:
        s = search.lower()
        items = [i for i in items if any(s in str(v).lower() for v in i.values())]

    for field, value in params.items():
        items = [i for i in items if str(i.get(field, "")).lower() == value.lower()]

    result = paginate(items, page, limit)
    result["filters"] = params
    if search:
        result["search"] = search
    return result


@app.get("/{resource}/{item_id}", summary="Tek kayıt getir")
async def get_one(resource: str, item_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT id, data FROM records WHERE resource = ? AND id = ?",
        (resource, item_id)
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(404, f"#{item_id} bulunamadı")

    item = json.loads(row["data"])
    item["id"] = row["id"]
    return item


@app.post("/{resource}", summary="Yeni kayıt ekle", status_code=201)
async def create_one(resource: str, payload: dict):
    conn = get_db()
    exists = conn.execute(
        "SELECT 1 FROM records WHERE resource = ? LIMIT 1", (resource,)
    ).fetchone()

    if not exists:
        raise HTTPException(404, f"'{resource}' yok. Önce /mockbox/load ile yükle")

    cursor = conn.execute(
        "INSERT INTO records (resource, data) VALUES (?, ?)",
        (resource, json.dumps(payload, ensure_ascii=False))
    )
    conn.commit()
    payload["id"] = cursor.lastrowid
    conn.close()
    return payload


@app.put("/{resource}/{item_id}", summary="Kayıt güncelle")
async def update_one(resource: str, item_id: int, payload: dict):
    conn = get_db()
    row = conn.execute(
        "SELECT id FROM records WHERE resource = ? AND id = ?",
        (resource, item_id)
    ).fetchone()

    if not row:
        raise HTTPException(404, f"#{item_id} bulunamadı")

    conn.execute(
        "UPDATE records SET data = ? WHERE resource = ? AND id = ?",
        (json.dumps(payload, ensure_ascii=False), resource, item_id)
    )
    conn.commit()
    conn.close()

    payload["id"] = item_id
    return payload


@app.delete("/{resource}/{item_id}", summary="Kayıt sil")
async def delete_one(resource: str, item_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT id FROM records WHERE resource = ? AND id = ?",
        (resource, item_id)
    ).fetchone()

    if not row:
        raise HTTPException(404, f"#{item_id} bulunamadı")

    conn.execute(
        "DELETE FROM records WHERE resource = ? AND id = ?",
        (resource, item_id)
    )
    conn.commit()
    conn.close()
    return {"message": f"#{item_id} silindi"}


if __name__ == "__main__":
    init_db()
    print("\n🚀 MockBox v2.0 çalışıyor → http://localhost:8000")
    print("📄 Dokümantasyon        → http://localhost:8000/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
