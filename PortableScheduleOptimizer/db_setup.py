import sqlite3

# O script SQL completo (em inglês)
SQL_SETUP_SCRIPT = """
-- 1. REFERENCE TABLE: HIERARCHY OF ROLES/POSITIONS
CREATE TABLE Roles (
    role_id INTEGER PRIMARY KEY,
    denomination TEXT NOT NULL UNIQUE
);

-- 2. REFERENCE TABLE: VEHICLES
CREATE TABLE Vehicles (
    vehicle_id INTEGER PRIMARY KEY,
    denomination TEXT NOT NULL UNIQUE,
    description TEXT
);

-- 3. LINKING TABLE: DEFINES THE REQUIRED CREW COMPOSITION FOR EACH VEHICLE
CREATE TABLE Vehicle_Composition (
    id INTEGER PRIMARY KEY,
    vehicle_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id),
    UNIQUE (vehicle_id, role_id)
);

-- 4. REFERENCE TABLE: WORKERS
CREATE TABLE Workers (
    worker_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    role_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

-- 5. REFERENCE TABLE: SHIFTS (A, B, C, D)
CREATE TABLE Shifts (
    shift_id INTEGER PRIMARY KEY,
    letter TEXT NOT NULL UNIQUE,
    fixed_ct_id INTEGER,
    FOREIGN KEY (fixed_ct_id) REFERENCES Workers(worker_id)
);

-- 6. REFERENCE TABLE: DRIVING COMPETENCIES
CREATE TABLE Competencies (
    competency_id INTEGER PRIMARY KEY,
    denomination TEXT NOT NULL UNIQUE
);

-- 7. LINKING TABLE: WHAT COMPETENCIES EACH WORKER HAS
CREATE TABLE Worker_Competency (
    worker_id INTEGER NOT NULL,
    competency_id INTEGER NOT NULL,
    PRIMARY KEY (worker_id, competency_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id),
    FOREIGN KEY (competency_id) REFERENCES Competencies(competency_id)
);

-- 8. INPUT TABLE: WHO IS ON DUTY
CREATE TABLE Schedule_Input (
    id INTEGER PRIMARY KEY,
    schedule_date DATE NOT NULL,
    shift_id INTEGER NOT NULL,
    worker_id INTEGER NOT NULL,
    FOREIGN KEY (shift_id) REFERENCES Shifts(shift_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id),
    UNIQUE (schedule_date, shift_id, worker_id)
);

CREATE TABLE Positions(
    position_id INTEGER PRIMARY KEY,
    denomination TEXT NOT NULL UNIQUE
);

-- 9. OUTPUT/HISTORY TABLE: THE OPTIMIZED SCHEDULE
CREATE TABLE Schedule_History (
    id INTEGER PRIMARY KEY,
    schedule_date DATE NOT NULL,
    shift_id INTEGER NOT NULL,
    worker_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    position_id INTEGER NOT NULL,
    assigned_role_id INTEGER NOT NULL,
    FOREIGN KEY (shift_id) REFERENCES Shifts(shift_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (position_id) REFERENCES Positions(position_id),
    FOREIGN KEY (assigned_role_id) REFERENCES Roles(role_id),
    UNIQUE (schedule_date, shift_id, worker_id)
);
"""

# Nome do ficheiro da base de dados (o seu ficheiro portátil)
DATABASE_FILE = "portable_schedule.db"


def setup_database():
    """Conecta à base de dados SQLite e cria todas as tabelas."""
    conn = None
    try:
        # Habilita a integridade referencial (Foreign Keys)
        conn = sqlite3.connect(DATABASE_FILE)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Executa todo o script de criação das tabelas
        cursor.executescript(SQL_SETUP_SCRIPT)

        conn.commit()
        print(f"Base de dados configurada com sucesso. Ficheiro '{DATABASE_FILE}' criado com todas as tabelas.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro durante a configuração da base de dados: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    setup_database()