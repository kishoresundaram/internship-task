from app.database.database import save_memory, get_memories


def save_user_memory(
    user_id: str,
    memory_key: str,
    memory_value: str
):

    save_memory(
        user_id=user_id,
        memory_key=memory_key,
        memory_value=memory_value
    )


def get_user_memories(user_id: str):

    memories = get_memories(user_id)

    return {
        key: value
        for key, value in memories
    }