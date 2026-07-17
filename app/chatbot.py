def create_bot(name, database_uri):
    # Imported lazily so code paths that inject a fake bot (tests) don't
    # need chatterbot/spaCy installed.
    from chatterbot import ChatBot

    bot = ChatBot(
        name,
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=database_uri,
    )
    _train_if_untrained(bot)
    return bot


def _train_if_untrained(bot):
    from chatterbot.trainers import ChatterBotCorpusTrainer

    # Training the full English corpus takes real time; skip it on every
    # restart once the storage already has statements in it.
    if bot.storage.count() == 0:
        ChatterBotCorpusTrainer(bot).train("chatterbot.corpus.english")
