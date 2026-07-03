# Chonchai E-Sport Tournament Registration

ระบบลงทะเบียนทีมแข่งขัน E-Sport ตามโจทย์กิจกรรม Backend Developer

## Features

- แสดงรายชื่อเกมที่เปิดแข่งขัน: RoV, Valorant, FC Online
- สมัครทีมเข้าแข่งขันผ่านหน้าเว็บ
- ตรวจสอบเกมที่เลือก ชื่อทีมซ้ำ และจำนวนสมาชิกขั้นต่ำ 3 คน
- แสดงทีมที่ลงทะเบียนล่าสุด
- เก็บข้อมูลใน SQLite local database ที่ `data/registration.db`

## Run

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

เปิดเว็บที่:

```text
http://127.0.0.1:8000
```

## Run Console Version

ไฟล์ `console_registration.py` เป็นเวอร์ชัน console ตามตัวอย่างใน PDF

```powershell
python console_registration.py
```

- พิมพ์ `done` เมื่อกรอกสมาชิกครบ
- พิมพ์ `exit` ในช่องชื่อทีมเพื่อปิดระบบ
- ถ้า Windows terminal แสดงภาษาไทยไม่ได้ ให้ตั้ง `$env:PYTHONIOENCODING = "utf-8"` ก่อนรัน

เปิด Dashboard ที่:

```text
http://127.0.0.1:8000/dashboard/
```

## API

- `GET /games`
- `POST /register`
- `GET /teams`
- `GET /stats`

## Local Database

ระบบใช้ SQLite ผ่าน Python standard library โดยอัตโนมัติเมื่อเปิด Backend

```text
data/registration.db
```

ถ้าต้องการใช้ไฟล์ database อื่น สามารถกำหนด environment variable:

```powershell
$env:DATABASE_PATH = "data/my-registration.db"
uvicorn app.main:app --reload
```

ตัวอย่าง `POST /register`:

```json
{
  "team_name": "Chonchai Alpha",
  "game": "RoV",
  "members": ["A", "B", "C"]
}
```

## Test

```powershell
pytest
```
