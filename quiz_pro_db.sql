CREATE DATABASE quiz_pro;
USE quiz_pro;

CREATE TABLE quiz_creator(
   QCId INT AUTO_INCREMENT PRIMARY KEY,
   user_name VARCHAR(50),
   mobile_number VARCHAR(15),
   email VARCHAR(50),
   password VARCHAR(50)
);

CREATE TABLE quiz_player(
   QPId INT AUTO_INCREMENT,
   player_name VARCHAR(50),
   mobile_number VARCHAR(15),
   email VARCHAR(50),
   password VARCHAR(50),
   PRIMARY KEY (QPId)
);

CREATE TABLE quiz_category_name(
   QId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   QCId INT,
   Q_catagory_name VARCHAR(50),
   No_of_players INT,
   FOREIGN KEY (QCId) REFERENCES quiz_creator(QCId)
);

CREATE TABLE quiz_question(
   QsId INT AUTO_INCREMENT PRIMARY KEY,
   QId INT,
   Question_text VARCHAR(500) NOT NULL,
   FOREIGN KEY (QId) REFERENCES quiz_category_name(QId)
);

CREATE TABLE quiz_options_ans(
   OId INT AUTO_INCREMENT PRIMARY KEY,
   QId INT,
   QsId INT,
   Option1 VARCHAR(100),
   Option2 VARCHAR(100),
   Option3 VARCHAR(100),
   Option4 VARCHAR(100),
   Answer VARCHAR(100),
   FOREIGN KEY (QsId) REFERENCES quiz_question(QsId),
   FOREIGN KEY (QId) REFERENCES quiz_category_name(QId)
);

CREATE TABLE quiz_ques_options_ans(
   QSId INT AUTO_INCREMENT PRIMARY KEY,
   QId INT,
   Question_text VARCHAR(500) NOT NULL,
   Option1 VARCHAR(100),
   Option2 VARCHAR(100),
   Option3 VARCHAR(100),
   Option4 VARCHAR(100),
   Answer VARCHAR(100),
   FOREIGN KEY (QId) REFERENCES quiz_category_name(QId)
);

CREATE TABLE quiz_result(
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    QPId INT,
    QId INT,
    QCId INT,
    Score INT,
    isPlayerPlayed INT,
    FOREIGN KEY (QPId) REFERENCES quiz_player(QPId),
    FOREIGN KEY (QId) REFERENCES quiz_category_name(QId),
    FOREIGN KEY (QCId) REFERENCES quiz_creator(QCId)
);


SHOW TABLES;
SELECT * FROM quiz_creator;
SELECT * FROM quiz_player;
SELECT * FROM quiz_category_name;
SELECT * FROM quiz_question;
SELECT * FROM quiz_options_ans;
SELECT * FROM quiz_ques_options_ans;
SELECT * FROM quiz_result;

SELECT user_name FROM quiz_creator,quiz_category_name WHERE quiz_creator.QCId = quiz_category_name.QCId;
SELECT * FROM quiz_category_name,quiz_question,quiz_options_ans;
SELECT * FROM quiz_creator WHERE user_name ='Binu' AND password = '123456789';
SELECT * FROM quiz_category_name WHERE QCId = 1;
SELECT Question_text FROM quiz_question WHERE QId = 13;
SELECT Option1,Option2,Option3,Option4 FROM quiz_options_ans WHERE QId = 13;
SELECT QsId,Question_text FROM quiz_question , quiz_category_name WHERE quiz_question.QId = quiz_category_name.QId;
(SELECT Question_text FROM quiz_question , quiz_category_name WHERE quiz_question.QId = quiz_category_name.QId)
UNION 
(SELECT Answer FROM quiz_question , quiz_options_ans WHERE quiz_question.QsId = quiz_options_ans.QsId);
SELECT count(*) FROM quiz_ques_options_ans WHERE QId = 18;
SELECT count(*) AS Number_of_records,Answer FROM quiz_ques_options_ans WHERE QId = 18 GROUP BY Answer;
SELECT QCId FROM quiz_category_name WHERE QId = 13;
SELECT * FROM quiz_player,quiz_category_name,quiz_result WHERE quiz_player.QPId =quiz_result.QPId;
SELECT user_name,Q_catagory_name,score FROM quiz_creator,quiz_category_name,quiz_result WHERE quiz_creator.QCId =quiz_category_name.QCId;
SELECT Q_catagory_name,Score FROM quiz_category_name INNER JOIN quiz_result ON quiz_category_name.QCId = quiz_result.QCId;
SELECT count(*) FROM quiz_category_name INNER JOIN quiz_result ON quiz_category_name.QCId = quiz_result.QCId;
SELECT * FROM quiz_player, quiz_result WHERE quiz_player.QPId = quiz_result.QPId ;
SELECT * FROM quiz_category_name, quiz_result WHERE quiz_category_name.QId = quiz_result.QId and QPId = 1 and isPlayerPlayed = 1;
SELECT * FROM quiz_category_name q_c_n JOIN  quiz_result q_r ON q_c_n.QCId = q_r.QCId WHERE q_r.QPId = 1 and q_r.isPlayerPlayed = 1;
SELECT * FROM quiz_category_name, quiz_result WHERE quiz_category_name.QId = quiz_result.QId;
SELECT DISTINCT q_c_n.Q_catagory_name, q_r.Score FROM quiz_category_name q_c_n, quiz_result q_r WHERE q_c_n.QCId = q_r.QCId;
SELECT a.*, b.*
FROM quiz_category_name a
JOIN (
    SELECT DISTINCT QCId, isPlayerPlayed
    FROM quiz_result 
) b ON a.QCId = b.QCId;

SELECT q_c_n.Q_catagory_name, q_r.Score
FROM quiz_category_name q_c_n
JOIN quiz_result q_r ON q_c_n.QCId = q_r.QCId
GROUP BY q_c_n.Q_catagory_name;

SELECT q_c_n.Q_catagory_name, q_r.Score
FROM quiz_category_name q_c_n
JOIN (
    SELECT QCId, Score
    FROM quiz_result
    GROUP BY QCId
) q_r ON q_c_n.QCId = q_r.QCId;
SELECT QCId, COUNT(*)
FROM quiz_category_name
GROUP BY QCId
HAVING COUNT(*) > 1;
SELECT q_c_n.Q_catagory_name, q_r.Score
FROM quiz_category_name q_c_n
JOIN quiz_result q_r ON q_c_n.QId = q_r.QId
WHERE q_c_n.QId = q_r.QId;
SELECT * FROM quiz_ques_options_ans WHERE QId = 1;

SET SQL_SAFE_UPDATES = 0;

SHOW TABLES;
DROP TABLE quiz_creator;
DROP TABLE quiz_player;
DROP TABLE quiz_category_name;
DROP TABLE quiz_question;
DROP TABLE quiz_options_ans;
DROP TABLE quiz_ques_options_ans;
DROP TABLE quiz_result;

DELETE FROM quiz_creator;
DELETE FROM quiz_player;
DELETE FROM quiz_category_name;
DELETE FROM quiz_question;
DELETE FROM quiz_options_ans;
DELETE FROM quiz_ques_options_ans;
DELETE FROM quiz_result;

ALTER TABLE quiz_options_ans ADD QId INT;
ALTER TABLE quiz_options_ans ADD FOREIGN KEY (QId) REFERENCES quiz_category_name(QId);

UPDATE quiz_options_ans
SET QId = 13;

ALTER TABLE quiz_category_name
MODIFY COLUMN No_of_players INT;

ALTER TABLE quiz_result  ADD isPlayerPlayed BIT;
ALTER TABLE quiz_result
MODIFY COLUMN isPlayerPlayed INT;
UPDATE quiz_result SET isPlayerPlayed = 1 WHERE Id = 1 and Id =2;

GRANT ALL PRIVILEGES ON quiz_pro.* TO user IDENTIFIED BY 'Mysql_02';
FLUSH PRIVILEGES;