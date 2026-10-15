# Observer Pattern & EventBus in Python

This project demonstrates the Observer Design Pattern using an EventBus in Python.

## Features

- Publish articles with a title, tags, and body
- Register subscribers with different interests
- Automatically notify interested subscribers
- Subscribe and unsubscribe from events
- Prevent duplicate notifications
- Test the implementation with Python assertions

## Project Structure

**event.py** – Main Python implementation

The project contains four classes:

- **EventBus:** Manages event listeners using `on()`, `off()`, and `emit()`.
- **Article:** Stores the title, tags, and body of an article.
- **Publisher:** Publishes articles and triggers events.
- **Subscriber:** Filters articles by tags and receives notifications.

## How to Run

Make sure Python 3 is installed.

Run:

`python event.py`

## Testing

The project includes automatic tests for article storage, subscriptions, notification filtering, unsubscribe behavior, and duplicate notifications.

## Learning Purpose

This project was created to practice event-driven programming and better understand how the Observer Design Pattern works.
