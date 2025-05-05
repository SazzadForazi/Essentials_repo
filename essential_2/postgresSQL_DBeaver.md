
# PostgreSQL & DBeaver Setup Guide

## 1. Install PostgreSQL

### Ubuntu (APT-based systems)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Verify PostgreSQL Installation
```bash
psql --version
```

## 2. Start PostgreSQL Service
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 3. Access PostgreSQL Command Line
```bash
sudo -u postgres psql
```
- To exit: `\q`

## 4. Create a New Database and User
```sql
CREATE DATABASE your_db_name;
CREATE USER your_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
```

## 5. Install DBeaver

### Ubuntu
```bash
sudo apt install ./dbeaver-ce_latest_amd64.deb
```
(Download from https://dbeaver.io/download/ if needed)

## 6. Connect PostgreSQL with DBeaver

### Connection Settings
| Field     | Value                     |
|-----------|---------------------------|
| Host      | localhost (or IP address) |
| Port      | 5432                      |
| Database  | your_db_name              |
| Username  | your_user                 |
| Password  | your_password             |

1. Open DBeaver.
2. Click `New Database Connection`.
3. Choose **PostgreSQL**.
4. Enter the details as per above.
5. Test Connection → Finish.

## 7. Common SQL Queries

### View All Databases
```sql
\l
```

### Connect to a Database
```sql
\c your_db_name
```

### List All Tables
```sql
\dt
```

### Count Specific Column (e.g., student_name)
```sql
SELECT COUNT(student_name) FROM students;
```

---
