
# step 1: event bus

class EventBus:
    def __init__(self):
        self.handlers = {}

    def on(self, event_name, handler):
        handlers = self.handlers.setdefault(event_name, [])
        if handler not in handlers:
            handlers.append(handler)

    def off(self, event_name, handler):
        handlers = self.handlers.get(event_name, [])
        if handler in handlers:
            handlers.remove(handler)

    def emit(self, event_name, data=None):
        for handler in list(self.handlers.get(event_name, [])):
            handler(data)


# step 2: article class

class Article:
    def __init__(self, title, tags, body):
        self.title = title
        self.tags = tags
        self.body = body


# step 3: subscriber class

class Subscriber:
    def __init__(self, name, tags):
        self.name = name
        self.tags = set(tags)
        self.notifications = []

    def notify(self, article):
        if self.tags & set(article.tags):
            self.notifications.append(article.title)
            print(f"{self.name} received notification: {article.title}")


# step 4: publisher class

class Publisher:
    def __init__(self):
        self.articles = []
        self.subscribers = []
        self.bus = EventBus()

    def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            self.bus.on("article_published", subscriber.notify)
            print(f"{subscriber.name} subscribed successfully.")

    def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            self.bus.off("article_published", subscriber.notify)
            print(f"{subscriber.name} unsubscribed successfully.")

    def publish(self, article):
        self.articles.append(article)
        print(f"\nNew article published: {article.title}")
        self.bus.emit("article_published", article)


# step 5: create articles

article1 = Article(
    "Learning Python",
    ["Python", "Programming"],
    "This article explains Python basics."
)

article2 = Article(
    "Arduino Sensors",
    ["Arduino", "Electronics"],
    "How to read sensor data using Arduino."
)

article3 = Article(
    "Introduction to AI",
    ["AI", "Robotics"],
    "This article explains artificial intelligence."
)


# step 6: create publisher

blog = Publisher()


# step 7: create subscribers

adrian = Subscriber("Adrian", ["Python", "Arduino"])
alex = Subscriber("Alex", ["AI", "Robotics"])


# step 8: register subscribers

blog.subscribe(adrian)
blog.subscribe(alex)


# step 9: publish articles

blog.publish(article1)
blog.publish(article2)
blog.publish(article3)


# step 10: unsubscribe test

print("\n--- Unsubscribe Test ---")

blog.unsubscribe(adrian)

article4 = Article(
    "Advanced Python",
    ["Python"],
    "Learn advanced Python programming."
)

blog.publish(article4)


# step 11: resubscribe test

print("\n--- Resubscribe Test ---")

blog.subscribe(adrian)

article5 = Article(
    "Raspberry Pi and Arduino",
    ["Arduino", "Raspberry Pi"],
    "Communication between Raspberry Pi and Arduino."
)

blog.publish(article5)


# step 12: multiple tags test

print("\n--- Multiple Tags Test ---")

article6 = Article(
    "Python for Arduino",
    ["Python", "Arduino"],
    "Using Python with Arduino."
)

blog.publish(article6)


# step 13: final results

print("\nTotal articles:", len(blog.articles))
print("Total subscribers:", len(blog.subscribers))


# step 14: automatic tests

print("\n--- FINAL AUTOMATIC TESTS ---")

assert len(blog.articles) == 6
print("Test 1 passed: All articles stored")

assert len(blog.subscribers) == 2
print("Test 2 passed: Both subscribers active")

assert "Advanced Python" not in adrian.notifications
print("Test 3 passed: Unsubscribe works")

assert alex.notifications == ["Introduction to AI"]
print("Test 4 passed: Tag filtering works")

assert adrian.notifications.count("Python for Arduino") == 1
print("Test 5 passed: No duplicate notifications")

assert adrian.notifications == [
    "Learning Python",
    "Arduino Sensors",
    "Raspberry Pi and Arduino",
    "Python for Arduino"
]
print("Test 6 passed: Adrian received correct notifications")

print("\nAll automatic tests passed!")
