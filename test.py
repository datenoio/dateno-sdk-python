#!/usr/bin/env python3
from __future__ import annotations

import json
from dateno import SDK, errors

API_KEY = "MaKsBdyuwHfsXNa2OL6N7L9TkQoX0LrQ"
ENTRY_ID = "89dab920d0ff1f03ae44885e7ff021358cb0f531cc81b61579f06b0d4ff4ee28"
LIMIT = 5


def safe_get(dct: object, *path: str):
    """Безопасно достаёт вложенные поля из dict."""
    cur = dct
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def main() -> int:
    with SDK(api_key_query=API_KEY) as sdk:
        try:
            similar = sdk.search_api.get_similar_datasets(
                entry_id=ENTRY_ID,
                limit=LIMIT,
                # fields можно не передавать — эндпоинт и так вернёт похожее.
                # Если захочешь: fields=["dataset.title", "dataset.description"]
            )
        except errors.ErrorResponse as e:
            print("API error:", e)
            return 2
        except Exception as e:
            print("Unexpected error:", repr(e))
            return 3

    # 1) Печать “шапки”
    total_val = getattr(similar.total, "value", None)
    total_rel = getattr(similar.total, "relation", None)
    print(f"Total similar: {total_val} ({total_rel})")
    print(f"Max score: {similar.max_score}")
    print(f"Returned hits: {len(similar.hits)}")
    print("-" * 100)

    # 2) Печать хитов
    for i, h in enumerate(similar.hits, start=1):
        title = safe_get(h.source, "dataset", "title")
        url = safe_get(h.source, "dataset", "url")
        print(f"[{i}] id:    {h.id}")
        print(f"    score: {h.score}")
        print(f"    title: {title}")
        print(f"    url:   {url}")
        print("-" * 100)

    # 3) Проверка дампов (ключевая часть для диагностики алиасов)
    dump_internal = similar.model_dump()
    dump_alias = similar.model_dump(by_alias=True)

    # Смотрим первый hit, чтобы быстро понять, не теряются ли поля
    first_internal = (dump_internal.get("hits") or [{}])[0]
    first_alias = (dump_alias.get("hits") or [{}])[0]

    print("\nDEBUG: first hit keys check")
    print("model_dump() keys:", sorted(first_internal.keys()))
    print("model_dump(by_alias=True) keys:", sorted(first_alias.keys()))

    # В alias-дампе должны появиться _id/_index/_source/_score
    # Если после правок всё ок — они НЕ будут None.
    print("\nDEBUG: first hit alias fields")
    print("_id:", first_alias.get("_id"))
    print("_index:", first_alias.get("_index"))
    print("_score:", first_alias.get("_score"))
    _source = first_alias.get("_source")
    print("_source.dataset.title:", safe_get(_source, "dataset", "title"))

    # Если хочется — можно вывести полный JSON (осторожно, объёмный)
    # print(json.dumps(dump_alias, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
