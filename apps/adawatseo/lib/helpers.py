def loop_in_chunks(text: str, chunk_size=80):
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]
