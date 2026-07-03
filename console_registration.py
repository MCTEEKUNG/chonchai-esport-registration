allowed_games = ("RoV", "Valorant", "FC Online")
database = {}


def show_games():
    print(f"เกมที่เปิดรับสมัคร: {', '.join(allowed_games)}")


def register_team(team_name, game, members_list):
    if game not in allowed_games:
        return False, f"ไม่มีเกมนี้ในการแข่งขัน"

    if team_name in database:
        return False, "ชื่อทีมนี้ถูกใช้ไปแล้ว"

    if len(members_list) < 3:
        return False, "สมาชิกไม่ครบ 3 คน"

    database[team_name] = {
        "game": game,
        "members": members_list,
    }
    return True, "ลงทะเบียนสำเร็จ!"


def main():
    print("ยินดีต้อนรับสู่ระบบลงทะเบียน ชลชาย E-Sports")
    show_games()
    print("-" * 40)

    while True:
        print("\nกรอกข้อมูลทีมใหม่ หรือพิมพ์ 'exit' ที่ชื่อทีมเพื่อปิดระบบ")
        team_name = input("ชื่อทีม: ")
        if team_name.lower() == "exit":
            break

        game = input("ระบุเกมที่จะแข่ง (RoV/Valorant/FC Online): ")

        members = []
        print("กรอกชื่อสมาชิก (พิมพ์ 'done' เมื่อครบ):")
        while True:
            member_name = input("- ชื่อสมาชิก: ")
            if member_name.lower() == "done":
                break
            members.append(member_name)

        is_success, message = register_team(team_name, game, members)

        print("\n" + message)
        if is_success:
            print("ฐานข้อมูลปัจจุบัน:", database)

    print("\nปิดระบบรับสมัคร")


if __name__ == "__main__":
    main()
