import logging
import uuid
import requests

from aiogram.types import File


logger = logging.getLogger(__name__)


def create_user(
    first_name: str,
    last_name: str,
    position: str,
    video: File,
    base_url: str,
    person_id: uuid.UUID,
) -> None:
    logger.info(f"send from bot to {base_url}")

    return requests.post(
        base_url,
        json={
            "video": {
                "file_path": video.file_path,
            },
            "first_name": first_name,
            "last_name": last_name,
            "position": position,
            "person_id": str(person_id),
        },
        verify=False,
    )
