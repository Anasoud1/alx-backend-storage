-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.


DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE average DECIMAL(10, 2); 
	SELECT AVG(score) INTO average FROM corrections WHERE corrections.user_id = user_id;
	IF average != 0 THEN
		UPDATE users SET average_score = average WHERE id = user_id; 
	END IF;
END $$

DELIMITER ;
