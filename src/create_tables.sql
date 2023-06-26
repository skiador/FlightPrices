CREATE TABLE airline (
  airline_iata VARCHAR(5) PRIMARY KEY NOT NULL,
  airline_icao VARCHAR(5) NOT NULL,
  airline_name VARCHAR(30) NOT NULL
);

CREATE TABLE airports (
  airport_iata VARCHAR(5) PRIMARY KEY NOT NULL,
  airport_icao VARCHAR(5) NOT NULL,
  coordinates_latitude DECIMAL(9,7) NOT NULL,
  coordinates_longitude DECIMAL(9,7) NOT NULL
);


CREATE TABLE prices (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    airline_iata VARCHAR(5) NOT NULL,
    flight_number VARCHAR(10) NOT NULL,
    departure_airport_iata VARCHAR(5) NOT NULL,
    destination_airport_iata VARCHAR(5) NOT NULL,
    departure_datetime DATETIME NOT NULL,
    arrival_datetime DATETIME NOT NULL,
    price_date_time DATETIME NOT NULL,
    price DECIMAL(10,2),
    time_till_departure INT AS (DATEDIFF(departure_datetime, price_date_time)) STORED,
    FOREIGN KEY (airline_iata) REFERENCES airline(airline_iata),
    FOREIGN KEY (departure_airport_iata) REFERENCES airports(airport_iata),
    FOREIGN KEY (destination_airport_iata) REFERENCES airports(airport_iata),
    CONSTRAINT prices UNIQUE (flight_number, departure_datetime, price_date_time)
);



--Example values for airports and airlines
INSERT INTO airports
VALUES ('BCN', 'LEBL', 0, 0);

INSERT INTO airports
VALUES ('AGP', 'LEMG', 0, 0);

INSERT INTO airline
VALUES ('VY', 'VLG', 'Vueling Airlines');

INSERT INTO airports
VALUES ('MAD', 'LEMD', 0, 0);