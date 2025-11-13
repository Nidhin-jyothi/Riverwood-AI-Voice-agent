import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

DATA_DIR = Path("../data/histories")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_user_path(user_id: str) -> Path:
    
    return DATA_DIR / f"{user_id}.json"


def load_user(user_id: str) -> Dict[str, Any]:
   
    p = get_user_path(user_id)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    
    return {
        "user_id": user_id,
        "conversations": [],
        "daily_summaries": {},
        "meta": {},
    }


def save_user(user_data: Dict[str, Any]):
   
    p = get_user_path(user_data["user_id"])
    p.write_text(json.dumps(user_data, ensure_ascii=False, indent=2), encoding="utf-8")


def append_message(
    user_id: str,
    direction: str,
    text: str,
    audio_path: Optional[str] = None,
    tags: Optional[List[str]] = None,
):
    
    user_data = load_user(user_id)
    user_data["conversations"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "direction": direction,
            "text": text,
            "audio_path": audio_path,
            "summary_tags": tags or [],
        }
    )
    save_user(user_data)


def get_recent_context(user_id: str, n: int = 6) -> List[Dict[str, Any]]:
    
    user_data = load_user(user_id)
    return user_data.get("conversations", [])[-n:]


def get_recent_summary(user_id: str, days: int = 7):
    
    user_data = load_user(user_id)
    return user_data.get("daily_summaries", {})
