-- Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

-- TEXT statt varchar(n):
-- "There is no performance difference among these three types, apart from a few extra CPU cycles
-- to check the length when storing into a length-constrained column"
-- ggf. CHECK(char_length(nachname) <= 255)

-- https://www.postgresql.org/docs/current/sql-createtable.html
-- https://www.postgresql.org/docs/current/datatype.html
-- https://www.postgresql.org/docs/current/sql-createtype.html
-- https://www.postgresql.org/docs/current/datatype-enum.html
CREATE TYPE carrier_type AS ENUM ('AIRCRAFT_CARRIER', 'HELICOPTER_CARRIER');

CREATE TABLE IF NOT EXISTS carrier (
    id            INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version       INTEGER NOT NULL DEFAULT 0,
    name          TEXT NOT NULL UNIQUE,
    nation        TEXT NOT NULL,
    carrier_type  carrier_type NOT NULL,
    erzeugt       TIMESTAMP NOT NULL,
    aktualisiert  TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS command_center (
    id              INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    code_name       TEXT NOT NULL,
    security_level  INTEGER NOT NULL CHECK (security_level >= 1 AND security_level <= 5),
    carrier_id      INTEGER NOT NULL UNIQUE REFERENCES carrier ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS aircraft (
    id            INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    model         TEXT NOT NULL,
    manufacturer  TEXT NOT NULL,
    carrier_id    INTEGER NOT NULL REFERENCES carrier ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS carrier_name_idx ON carrier(name);
CREATE INDEX IF NOT EXISTS aircraft_carrier_id_idx ON aircraft(carrier_id);
CREATE INDEX IF NOT EXISTS command_center_carrier_id_idx ON command_center(carrier_id);
