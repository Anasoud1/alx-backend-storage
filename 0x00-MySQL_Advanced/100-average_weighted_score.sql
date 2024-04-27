-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.

DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
    DECLARE total_weight FLOAT DEFAULT 0 ;
    DECLARE weight FLOAT DEFAULT 0;
    DECLARE result FLOAT;

    SELECT SUM(projects.weight) INTO total_weight FROM projects;

    SELECT SUM(projects.weight * corrections.score) INTO weight
    FROM corrections
    INNER JOIN projects ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id;

    IF total_weight = 0 THEN
        SET result = 0;
    ELSE
        SET result = weight / total_weight;
    END IF;

    update users set average_score = result where users.id = user_id;
END $$

DELIMITER ;
