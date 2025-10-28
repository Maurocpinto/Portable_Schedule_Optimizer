import sqlite3

DATABASE_FILE = "portable_schedule.db"


def insert_initial_data():
    """Inserts all reference data (Roles, Competencies, Vehicles, and Composition) into the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # --- 1. ROLES (Cargos) ---
        # Defines the 3 assignable positions and their hierarchy level (3 being the highest)
        roles_data = [
            (1, 'OPS'),
            (2, 'OPSC'),
            (3, 'CE'),
            (4, 'CT')
        ]
        # Using INSERT OR REPLACE to ensure data integrity
        cursor.executemany("INSERT OR REPLACE INTO Roles (role_id, denomination) VALUES (?, ?)",
                           roles_data)

        # --- 2. COMPETENCIES (Competências) ---
        competencies_data = [
            (1, 'OSKOSH'),
            (2, 'ROSENBAUER'),
            (3, 'COMMAND'),
            (4, 'EXTRICATION')
        ]
        cursor.executemany("INSERT OR REPLACE INTO Competencies (competency_id, denomination) VALUES (?, ?)",
                           competencies_data)

        # --- 3. VEHICLES (Viaturas) ---
        vehicles_data = [
            (1, '01', 'COMMAND'),
            (2, '02', 'OSKOSH'),
            (3, '03', 'OSKOSH'),
            (4, '04', 'OSKOSH'),
            (5, '05', 'OSKOSH'),
            (6, '06', 'ROSENBAUER'),
            (7, '07', 'EXTRICATION')
        ]
        cursor.executemany("INSERT OR REPLACE INTO Vehicles (vehicle_id, denomination, description) VALUES (?, ?, ?)",
                           vehicles_data)

        composition_data = [
            # VTR 1, 2, 3 (Total 3 Lugares: 1 TL, 2 OP)
            (1, 4),
            (1, 2),
            (2, 1),
            (2, 2),
            (2, 3),
            (3, 1),
            (3, 2),
            (3, 3),
            (4, 1),
            (4, 2),
            (4, 3),
            (5, 1),
            (5, 2),
            (5, 3),
            (6, 1),
            (6, 2),
            (6, 3),
            (7, 2),
            (7, 3)
        ]

        # Clear existing composition data to prevent duplicates on re-run
        cursor.execute("DELETE FROM Vehicle_Composition")
        cursor.executemany("INSERT INTO Vehicle_Composition (vehicle_id, role_id) VALUES (?, ?)",
                           composition_data)

        # --- 5. SHIFTS (Turnos) ---
        # Shifts A, B, C, D (fixed_ct_id will be updated in the next script)
        shifts_data = [
            (1, 'A', None),
            (2, 'B', None),
            (3, 'C', None),
            (4, 'D', None)
        ]
        cursor.executemany("INSERT OR REPLACE INTO Shifts (shift_id, letter, fixed_ct_id) VALUES (?, ?, ?)",
                           shifts_data)

        conn.commit()
        print("Initial data (Roles, Competencies, Vehicles, Composition, Shifts) inserted successfully.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro durante a inserção de dados: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    insert_initial_data()