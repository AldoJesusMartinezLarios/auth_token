CREATE TABLE usuarios (
    username varchar,
    password varchar,
    token varchar,
    timestamp timestamp
);

INSERT INTO usuarios (username, password, token, timestamp) 
VALUES ('oppie@gmail.com', 'oppie', '12345_asdf', CURRENT_TIMESTAMP);