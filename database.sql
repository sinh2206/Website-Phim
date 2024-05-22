-- Tạo các bảng dữ liệu
CREATE DATABASE MovieDB;
USE MovieDB;

CREATE TABLE Movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255),
    release_date DATE,
    video_release_date DATE,
    IMDb_URL VARCHAR(255),
    unknown BOOLEAN,
    Action BOOLEAN,
    Adventure BOOLEAN,
    Animation BOOLEAN,
    Children BOOLEAN,
    Comedy BOOLEAN,
    Crime BOOLEAN,
    Documentary BOOLEAN,
    Drama BOOLEAN,
    Fantasy BOOLEAN,
    Film-Noir BOOLEAN,
    Horror BOOLEAN,
    Musical BOOLEAN,
    Mystery BOOLEAN,
    Romance BOOLEAN,
    Sci-Fi BOOLEAN,
    Thriller BOOLEAN,
    War BOOLEAN,
    Western BOOLEAN
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    age INT,
    gender CHAR(1),
    occupation VARCHAR(50),
    zip_code VARCHAR(10)
);

CREATE TABLE Ratings (
    user_id INT,
    movie_id INT,
    rating FLOAT,
    timestamp BIGINT,
    PRIMARY KEY(user_id, movie_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id),
    FOREIGN KEY(movie_id) REFERENCES Movies(movie_id)
);

-- Nhập dữ liệu từ các tệp CSV vào bảng
LOAD DATA LOCAL INFILE 'path_to/u.item' INTO TABLE Movies
FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n'
(movie_id, title, release_date, video_release_date, IMDb_URL, unknown, Action, Adventure, Animation, Children, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western);

LOAD DATA LOCAL INFILE 'path_to/u.user' INTO TABLE Users
FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n'
(user_id, age, gender, occupation, zip_code);

LOAD DATA LOCAL INFILE 'path_to/u.data' INTO TABLE Ratings
FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
(user_id, item_id, rating, timestamp);
