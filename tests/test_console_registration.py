import console_registration


def setup_function():
    console_registration.database.clear()


def test_console_register_success():
    success, message = console_registration.register_team(
        "Console Alpha",
        "RoV",
        ["A", "B", "C"],
    )

    assert success is True
    assert message == "ลงทะเบียนสำเร็จ!"
    assert console_registration.database["Console Alpha"] == {
        "game": "RoV",
        "members": ["A", "B", "C"],
    }


def test_console_reject_unknown_game():
    success, message = console_registration.register_team(
        "Console Beta",
        "Unknown",
        ["A", "B", "C"],
    )

    assert success is False
    assert message == "ไม่มีเกมนี้ในการแข่งขัน"


def test_console_reject_duplicate_team():
    console_registration.register_team("Console Gamma", "Valorant", ["A", "B", "C"])
    success, message = console_registration.register_team(
        "Console Gamma",
        "FC Online",
        ["D", "E", "F"],
    )

    assert success is False
    assert message == "ชื่อทีมนี้ถูกใช้ไปแล้ว"


def test_console_reject_too_few_members():
    success, message = console_registration.register_team(
        "Console Delta",
        "FC Online",
        ["A", "B"],
    )

    assert success is False
    assert message == "สมาชิกไม่ครบ 3 คน"
