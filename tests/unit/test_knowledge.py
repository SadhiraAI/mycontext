"""
Tests for Knowledge Layer - Session and Archive
"""

from datetime import datetime

from mycontext.knowledge import (
    FileArchive,
    MemoryArchive,
    Message,
    Session,
)

# ============================================================================
# Session Tests
# ============================================================================

def test_session_creation():
    """Test creating a session"""
    session = Session()

    assert session.id is not None
    assert len(session.messages) == 0
    assert session.max_tokens == 4000


def test_session_add_message():
    """Test adding messages"""
    session = Session()

    msg = session.add_message("user", "Hello")

    assert len(session.messages) == 1
    assert msg.role == "user"
    assert msg.content == "Hello"
    assert msg.id is not None


def test_session_convenience_methods():
    """Test convenience methods for adding messages"""
    session = Session()

    session.add_user_message("User message")
    session.add_assistant_message("Assistant message")
    session.add_system_message("System message")

    assert len(session.messages) == 3
    assert session.messages[0].role == "user"
    assert session.messages[1].role == "assistant"
    assert session.messages[2].role == "system"


def test_session_get_messages():
    """Test getting messages with filters"""
    session = Session()

    session.add_user_message("User 1")
    session.add_assistant_message("Assistant 1")
    session.add_user_message("User 2")
    session.add_assistant_message("Assistant 2")

    # Get all messages
    all_msgs = session.get_messages()
    assert len(all_msgs) == 4

    # Get limited messages
    last_2 = session.get_messages(limit=2)
    assert len(last_2) == 2
    assert last_2[0].content == "User 2"

    # Get by role
    user_msgs = session.get_messages(role="user")
    assert len(user_msgs) == 2
    assert all(msg.role == "user" for msg in user_msgs)


def test_session_render_messages():
    """Test rendering messages"""
    session = Session()

    session.add_user_message("Hello")
    session.add_assistant_message("Hi!")

    rendered = session.render_messages()

    assert len(rendered) == 2
    assert rendered[0] == {"role": "user", "content": "Hello"}
    assert rendered[1] == {"role": "assistant", "content": "Hi!"}


def test_session_estimate_tokens():
    """Test token estimation"""
    session = Session()

    # Add message with known length
    session.add_message("user", "a" * 400)  # 400 chars ≈ 100 tokens

    estimated = session.estimate_tokens()
    assert 90 <= estimated <= 110  # Allow some variance


def test_session_clear():
    """Test clearing session"""
    session = Session()

    session.add_user_message("Message 1")
    session.add_user_message("Message 2")

    assert len(session.messages) == 2

    session.clear()

    assert len(session.messages) == 0


def test_session_pruning_by_count():
    """Test pruning by message count"""
    session = Session(max_messages=3)

    session.add_system_message("System")
    session.add_user_message("User 1")
    session.add_user_message("User 2")
    session.add_user_message("User 3")  # Should trigger pruning

    # Should keep system message + 2 most recent
    assert len(session.messages) <= 3

    # System message should be preserved
    assert any(msg.role == "system" for msg in session.messages)


def test_session_pruning_by_tokens():
    """Test pruning by token count"""
    session = Session(max_tokens=100)  # Very small limit

    # Add large messages
    session.add_user_message("x" * 200)  # ~50 tokens
    session.add_user_message("y" * 200)  # ~50 tokens
    session.add_user_message("z" * 200)  # ~50 tokens (should trigger pruning)

    # Should prune to stay under limit
    estimated = session.estimate_tokens()
    assert estimated <= session.max_tokens or len(session.messages) == 1


def test_session_to_context_string():
    """Test converting session to context string"""
    session = Session()

    session.add_user_message("Hello")
    session.add_assistant_message("Hi!")

    context_str = session.to_context_string()

    assert "USER: Hello" in context_str
    assert "ASSISTANT: Hi!" in context_str


def test_session_len():
    """Test session length"""
    session = Session()

    assert len(session) == 0

    session.add_user_message("Message")

    assert len(session) == 1


# ============================================================================
# Message Tests
# ============================================================================

def test_message_creation():
    """Test creating a message"""
    msg = Message(role="user", content="Hello")

    assert msg.role == "user"
    assert msg.content == "Hello"
    assert msg.id is not None
    assert isinstance(msg.timestamp, datetime)


def test_message_render():
    """Test rendering a message"""
    msg = Message(role="user", content="Hello")

    rendered = msg.render()

    assert rendered == {"role": "user", "content": "Hello"}


# ============================================================================
# FileArchive Tests
# ============================================================================

def test_file_archive_creation(tmp_path):
    """Test creating a file archive"""
    archive = FileArchive(str(tmp_path / "archive"))

    assert archive.directory.exists()
    assert (archive.directory / "sessions").exists()
    assert (archive.directory / "index").exists()


def test_file_archive_save_and_load(tmp_path):
    """Test saving and loading sessions"""
    archive = FileArchive(str(tmp_path / "archive"))

    # Create session
    session = Session()
    session.add_user_message("Hello")
    session.add_assistant_message("Hi!")

    # Save it
    entry_id = archive.save_session(session)
    assert entry_id == session.id

    # Load it back
    loaded = archive.load_session(session.id)

    assert loaded is not None
    assert loaded.id == session.id
    assert len(loaded.messages) == 2
    assert loaded.messages[0].content == "Hello"


def test_file_archive_list_sessions(tmp_path):
    """Test listing sessions"""
    archive = FileArchive(str(tmp_path / "archive"))

    # Create and save multiple sessions
    session1 = Session()
    session1.add_user_message("Session 1")
    archive.save_session(session1, tags=["test"])

    session2 = Session()
    session2.add_user_message("Session 2")
    archive.save_session(session2, tags=["prod"])

    # List all
    all_entries = archive.list_sessions()
    assert len(all_entries) == 2

    # List with tag filter
    test_entries = archive.list_sessions(tags=["test"])
    assert len(test_entries) == 1


def test_file_archive_delete_session(tmp_path):
    """Test deleting a session"""
    archive = FileArchive(str(tmp_path / "archive"))

    # Create and save session
    session = Session()
    session.add_user_message("Hello")
    archive.save_session(session)

    # Delete it
    deleted = archive.delete_session(session.id)
    assert deleted is True

    # Try to load it
    loaded = archive.load_session(session.id)
    assert loaded is None

    # Try to delete again
    deleted_again = archive.delete_session(session.id)
    assert deleted_again is False


def test_file_archive_search(tmp_path):
    """Test searching sessions"""
    archive = FileArchive(str(tmp_path / "archive"))

    # Create sessions with different content
    session1 = Session()
    session1.add_user_message("I love Python programming")
    archive.save_session(session1)

    session2 = Session()
    session2.add_user_message("JavaScript is great too")
    archive.save_session(session2)

    # Search for Python
    results = archive.search("Python")
    assert len(results) == 1
    assert session1.id in [e.session_id for e in results]


def test_file_archive_stats(tmp_path):
    """Test getting archive statistics"""
    archive = FileArchive(str(tmp_path / "archive"))

    # Add some sessions
    for i in range(3):
        session = Session()
        session.add_user_message(f"Message {i}")
        archive.save_session(session)

    stats = archive.get_stats()

    assert stats["total_sessions"] == 3
    assert stats["total_messages"] == 3


# ============================================================================
# MemoryArchive Tests
# ============================================================================

def test_memory_archive_creation():
    """Test creating a memory archive"""
    archive = MemoryArchive()

    assert archive is not None


def test_memory_archive_save_and_load():
    """Test saving and loading in memory"""
    archive = MemoryArchive()

    # Create session
    session = Session()
    session.add_user_message("Hello")

    # Save it
    entry_id = archive.save_session(session)

    # Load it back
    loaded = archive.load_session(session.id)

    assert loaded is not None
    assert loaded.id == session.id
    assert len(loaded.messages) == 1


def test_memory_archive_clear():
    """Test clearing memory archive"""
    archive = MemoryArchive()

    # Add sessions
    session1 = Session()
    session1.add_user_message("Session 1")
    archive.save_session(session1)

    session2 = Session()
    session2.add_user_message("Session 2")
    archive.save_session(session2)

    assert len(archive.list_sessions()) == 2

    # Clear
    archive.clear()

    assert len(archive.list_sessions()) == 0


def test_memory_archive_search():
    """Test searching memory archive"""
    archive = MemoryArchive()

    # Create sessions
    session1 = Session()
    session1.add_user_message("I love Python")
    archive.save_session(session1)

    session2 = Session()
    session2.add_user_message("Ruby is cool")
    archive.save_session(session2)

    # Search
    results = archive.search("Python")
    assert len(results) == 1
