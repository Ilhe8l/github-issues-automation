import json
import redis

REDIS_URL = "redis://localhost:6379/0"

def get_redis_client():
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)

def main():
    r = get_redis_client()

    with open("squads.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for team in data.get("teams", []):
        squad_id = team["id"]

        r.set(
            f"squad:{squad_id}",
            json.dumps(team, ensure_ascii=False)
        )

        print(f"[OK] squad '{squad_id}' salva no Redis (JSON completo)")

if __name__ == "__main__":
    main()
