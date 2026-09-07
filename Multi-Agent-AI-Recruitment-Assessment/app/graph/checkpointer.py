from langgraph.checkpoint.memory import InMemorySaver


_checkpointer = InMemorySaver()


def get_checkpointer():
    return _checkpointer