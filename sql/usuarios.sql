CREATE TABLE usuarios (
    username varchar,
    password varchar,
    token varchar,
    timestamp timestamp
);

INSERT INTO usuarios (username, password, token, timestamp) 
VALUES ('oppie@gmail.com', 'a88730092144187f8d7b4d940456154a', '09b0ac835fe70eb1dc6d20d927af958d', CURRENT_TIMESTAMP);