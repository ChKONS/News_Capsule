create database news_capsule;
use news_capsule;

CREATE TABLE `login_info` (
  `person_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `user_password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`person_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);
  
  CREATE TABLE `user_preferences` (
  `user_id` INT NOT NULL,
  `crypto` TINYINT NULL,
  `tesla` TINYINT NULL,
  `ml/ai` TINYINT NULL,
  `faang/general_tech` TINYINT NULL,
  `hardware` TINYINT NULL,
  PRIMARY KEY (`user_id`));

  ALTER TABLE `news_capsule`.`user_preferences`
ADD CONSTRAINT `user_id`
  FOREIGN KEY (`user_id`)
  REFERENCES `news_capsule`.`login_info` (`person_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

CREATE TABLE `news_articles` (
  `News_ID` INT NOT NULL AUTO_INCREMENT,
  `News_Title` VARCHAR(255) NOT NULL,
  `News_URL` VARCHAR(255) NOT NULL,
  `News_Date` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`News_ID`));
ALTER TABLE `news_articles`
ADD UNIQUE INDEX `News_Title_UNIQUE` (`News_Title` ASC) VISIBLE,
ADD UNIQUE INDEX `News_URL_UNIQUE` (`News_URL` ASC) VISIBLE;
;

--Below is code for nice-to-have additions; we would have liked to store news into different tables based on the
--news topic. This would have been a point to expand had we had more time.

--  CREATE TABLE `crypto` (
--	`Articles` VARCHAR(50) NOT NULL,
--    `Publish_date` DATETIME NOT NULL,
--    `C_ID` INT NOT NULL auto_increment,
--    `Article_url` VARCHAR(100) NOT NULL,
--   PRIMARY KEY (`C_ID` ));
--
--	CREATE TABLE `machine learning/ AI` (
--	`Articles` VARCHAR(50) NOT NULL,
--    `Publish_date` DATETIME NOT NULL,
--    `M_ID` INT NOT NULL auto_increment,
--    `Article_url` VARCHAR(100) NOT NULL,
--	PRIMARY KEY (`M_ID` ));
--
--    CREATE TABLE `FAANG/tech` (
--	`Articles` VARCHAR(50) NOT NULL,
--    `Publish_date` DATETIME NOT NULL,
--    `F_ID` INT NOT NULL auto_increment,
--    `Article_url` VARCHAR(100) NOT NULL,
--	PRIMARY KEY (`F_ID` ));
--
--    CREATE TABLE `coding languages` (
--	`Articles` VARCHAR(50) NOT NULL,
--    `Publish_date` DATETIME NOT NULL,
--    `Languages` VARCHAR(50) NOT NULL,
--    `L_ID` INT NOT NULL auto_increment,
--    `Article_url` VARCHAR(100) NOT NULL,
--	PRIMARY KEY (`L_ID` ));
--
--    CREATE TABLE `GitHub` (
--	`Articles` VARCHAR(50) NOT NULL,
--    `Publish_date` DATETIME NOT NULL,
--    `G_ID` INT NOT NULL auto_increment,
--    `Profile_url` VARCHAR(100) NOT NULL,
--	PRIMARY KEY (`G_ID` ));
--
--
--   SELECT *
--   FROM login_info
--   INNER JOIN crypto ON crypto.C_ID = login_info.person_ID
--   INNER JOIN machine learning ON machine_learning.M_ID = login_info.person_ID
--   INNER JOIN FAANG ON FAANG.F_ID = login_info.person_ID
--   INNER JOIN coding languages ON coding_languages.L_ID = login_info.person_ID
--   INNER JOIN GitHub ON GitHub.G_ID = login_info.person_ID;
--
--DELIMITER $$
--
--CREATE PROCEDURE auth_id(
--    IN  `person_id` INT,
--    OUT username  VARCHAR(45))
--BEGIN
--    DECLARE compare VARCHAR(50);
--
--    SELECT person_id
--    INTO compare
--    FROM login_info
--    WHERE person_id = username ;
--
--    IF person_id != username THEN
--        SELECT `Sorry you cannot continue`;
--    END IF;
--END$$
--
--DELIMITER ;
