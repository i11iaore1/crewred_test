import httpx


async def are_valid_place_ids(place_ids: list[str | int]) -> bool:
    """
    Validates if all provided place IDs exist in the Art Institute of Chicago API.
    Uses the `ids` parameter to check multiple IDs in a single request.
    """
    if not place_ids:
        return True

    unique_ids = list(set(place_ids))
    ids_param = ",".join(str(pid) for pid in unique_ids)
    url = f"https://api.artic.edu/api/v1/artworks?ids={ids_param}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            if response.status_code != 200:
                return False
            data = response.json().get("data", [])
            return len(data) == len(unique_ids)
    except httpx.RequestError:
        return False
