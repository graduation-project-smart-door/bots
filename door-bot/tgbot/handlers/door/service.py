import logging
import requests

from aiogram.types import File


logger = logging.getLogger(__name__)


def create_user(first_name: str, last_name: str, video: File, base_url: str) -> None:
    logger.info(f"send from bot to {base_url}")

    requests.post(
        base_url,
        json={
            "video": {
                "file_path": video.file_path,
            },
            "first_name": first_name,
            "last_name": last_name
        },
        verify=False,
    )
